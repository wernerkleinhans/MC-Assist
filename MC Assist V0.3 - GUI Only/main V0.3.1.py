# GUI
from __future__ import annotations

import customtkinter
#from pycparser.ply.yacc import restart
from tktooltip import ToolTip

# Backend
import os
import re
import sys
import shutil
import winreg
import ctypes
import threading
import subprocess
import tkinter as tk
from tkinter import messagebox
from typing import Callable, Optional

# Backend var and setup -------------------------------------------------------

UNINSTALL_TIMEOUT_SECONDS = 3600
PLACEHOLDER_OPTIONS = ("Select MC Version...", "No Mastercam installations detected")
PROGRAM_FILES_ROOTS = (r"C:\Program Files", r"C:\Program Files (x86)")
ICON_BASENAMES = ("MC Assist V0.3", "MC Assist V0.1")
MSI_PRODUCT_CODE_RE = re.compile(
    r"\{[0-9A-Fa-f]{8}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{4}-[0-9A-Fa-f]{12}\}"
)

UNINSTALL_SEARCH_PATHS = [
    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
    (winreg.HKEY_CURRENT_USER, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
]


# CTK Var --------------------------------------------------------------------
text_color = "#ffffff"
main_color = "#99e0ff"
dropdown_button_color = "#00db96"
hover_color = "#3d3d3d"
background_color = "#242424"
background_color_light = "#333333"
progressbar_var = 0.0
restart_text_color = background_color



# region -- Backend

def _app_directory() -> str:
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def _resource_directory() -> str:
    """Return the folder containing bundled assets such as the application icon."""
    if getattr(sys, "frozen", False):
        return getattr(sys, "_MEIPASS", _app_directory())
    return os.path.dirname(os.path.abspath(__file__))


def _icon_path(extension: str) -> Optional[str]:
    for basename in ICON_BASENAMES:
        for directory in (_resource_directory(), _app_directory()):
            icon_path = os.path.join(directory, f"{basename}{extension}")
            if os.path.exists(icon_path):
                return icon_path
    return None


def set_app_icon(window) -> None:
    """Apply the custom MC Assist icon to a Tk window (title bar and taskbar)."""
    ico_path = _icon_path(".ico")
    if ico_path:
        try:
            window.iconbitmap(ico_path)
            return
        except tk.TclError:
            pass

    png_path = _icon_path(".png")
    if png_path:
        try:
            icon_image = tk.PhotoImage(file=png_path)
            window.iconphoto(True, icon_image)
            window._mc_assist_icon = icon_image
        except tk.TclError:
            pass


def is_admin() -> bool:
    """
    Checks if the script process currently possesses Windows administrative tokens.
    Uses ctypes to query the Windows shell32 API directly.
    """
    try:
        return bool(ctypes.windll.shell32.IsUserAnAdmin())
    except (AttributeError, OSError):
        return False


def run_as_admin() -> None:
    """
    Forces the script to relaunch itself using the 'runas' verb to trigger a
    Windows User Account Control (UAC) prompt if it is not already running with
    elevated permissions.
    """
    if not is_admin():
        if getattr(sys, "frozen", False):
            params = subprocess.list2cmdline(sys.argv[1:])
        else:
            params = subprocess.list2cmdline(sys.argv)
        ret = ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
        if ret <= 32:
            ctypes.windll.user32.MessageBoxW(
                None,
                f"Elevation failed (ShellExecuteW code {ret}). The application will not start.",
                "MC Assist",
                0x10,
            )
            return
        sys.exit()


def _open_in_explorer(path: str) -> None:
    subprocess.Popen(["explorer.exe", "/select,", os.path.normpath(path)])


def _hive_sam_flags(hive) -> list[int]:
    if hive == winreg.HKEY_LOCAL_MACHINE:
        return [winreg.KEY_WOW64_64KEY, winreg.KEY_WOW64_32KEY]
    return [0]


def _iter_uninstall_entries():
    """Yield (display_name, uninstall_string) from the standard Windows uninstall registry hives."""
    for hive, base_path in UNINSTALL_SEARCH_PATHS:
        try:
            with winreg.OpenKey(hive, base_path) as key:
                for i in range(winreg.QueryInfoKey(key)[0]):
                    try:
                        sub_key_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, sub_key_name) as sub_key:
                            display_name, _ = winreg.QueryValueEx(sub_key, "DisplayName")
                            uninstall_cmd, _ = winreg.QueryValueEx(sub_key, "UninstallString")
                            yield str(display_name), str(uninstall_cmd)
                    except OSError:
                        continue
        except OSError:
            continue


def _version_from_display_name(display_name: str) -> Optional[str]:
    """Extract a Mastercam year from a registry DisplayName, or return None."""
    match = re.match(r"^Mastercam (\d{4})(?:\s|$)", display_name)
    return match.group(1) if match else None


def _registry_mastercam_versions(hive, subkey: str = r"SOFTWARE\CNC Software") -> set[str]:
    """Return Mastercam year strings found under a CNC Software registry key."""
    versions: set[str] = set()
    for sam in _hive_sam_flags(hive):
        try:
            with winreg.OpenKey(hive, subkey, 0, winreg.KEY_READ | sam) as key:
                for i in range(winreg.QueryInfoKey(key)[0]):
                    name = winreg.EnumKey(key, i)
                    match = re.match(r"^Mastercam (\d{4})$", name)
                    if match:
                        versions.add(match.group(1))
        except OSError:
            continue
    return versions


def _program_files_mastercam_versions() -> set[str]:
    """Return Mastercam year strings found from Mastercam folders in Program Files."""
    versions: set[str] = set()
    for program_files in PROGRAM_FILES_ROOTS:
        if not os.path.isdir(program_files):
            continue
        for folder_name in os.listdir(program_files):
            match = re.match(r"^Mastercam (\d{4})$", folder_name)
            if match:
                versions.add(match.group(1))
    return versions


def _mastercam_versions_updater() -> set[str]:
    """Return Mastercam year strings found from Mastercam Updater folders in Program Files."""
    versions: set[str] = set()
    for program_files in PROGRAM_FILES_ROOTS:
        if not os.path.isdir(program_files):
            continue
        for folder_name in os.listdir(program_files):
            match = re.match(r"^Mastercam (\d{4}) Updater$", folder_name)
            if match:
                versions.add(match.group(1))
    return versions


def _my_mastercam_versions() -> set[str]:
    """Return Mastercam year strings found strictly in user Documents (ignoring backups)."""
    versions: set[str] = set()
    user_profile = os.environ.get("USERPROFILE", "")

    doc_paths = [
        os.path.join(user_profile, "Documents"),
        #os.path.join(user_profile, "OneDrive", "Documents"),
    ]

    #Dynamically check for Corporate and Personal OneDrive paths (New code added)
    for env_key in ["OneDriveCommercial", "OneDrive"]:
        onedrive_root = os.environ.get(env_key)
        if onedrive_root:
            onedrive_docs = os.path.join(onedrive_root, "Documents")
            # Avoid adding duplicates if paths happen to overlap
            if onedrive_docs not in doc_paths:
                doc_paths.append(onedrive_docs)


    for my_docs in doc_paths:
        if os.path.isdir(my_docs):
            for folder_name in os.listdir(my_docs):
                match = re.match(r"^(?:My )?Mastercam (\d{4})$", folder_name)
                if match:
                    versions.add(match.group(1))
    return versions


def _shared_mastercam_paths(version: str) -> list[str]:
    public_profile = os.environ.get("PUBLIC", r"C:\Users\Public")
    public_docs = os.path.join(public_profile, "Documents")
    return [
        os.path.join(public_docs, f"Shared Mastercam {version}"),
        os.path.join(public_docs, f"Shared Mcam{version}"),
    ]


def _shared_mastercam_versions() -> set[str]:
    """Return Mastercam year strings found strictly in Public Documents (ignoring backups)."""
    versions: set[str] = set()
    public_profile = os.environ.get("PUBLIC", r"C:\Users\Public")
    public_docs = os.path.join(public_profile, "Documents")

    if os.path.isdir(public_docs):
        for folder_name in os.listdir(public_docs):
            match = re.match(r"^Shared Mastercam (\d{4})$", folder_name)
            if match:
                versions.add(match.group(1))
                continue
            match = re.match(r"^Shared Mcam(\d{4})$", folder_name)
            if match:
                versions.add(match.group(1))
    return versions


def _registered_uninstall_versions() -> set[str]:
    """Return Mastercam year strings that still have Windows uninstall registry entries."""
    versions: set[str] = set()
    for display_name, _ in _iter_uninstall_entries():
        version = _version_from_display_name(display_name)
        if version:
            versions.add(version)
    return versions


def get_version_cleanup_info(version: str) -> dict:
    """
    Inspect the machine for leftover Mastercam artifacts for one version.
    Returns a dict describing what was found and whether force cleanup is needed.
    """
    has_uninstaller = version in _registered_uninstall_versions()
    has_program_files = version in _program_files_mastercam_versions()
    has_program_updater_files = version in _mastercam_versions_updater()
    has_registry = (
        version in _registry_mastercam_versions(winreg.HKEY_LOCAL_MACHINE)
        or version in _registry_mastercam_versions(winreg.HKEY_CURRENT_USER)
    )
    has_shared_documents = version in _shared_mastercam_versions()
    has_my_documents = version in _my_mastercam_versions()

    leftovers: list[str] = []
    if has_program_files:
        leftovers.extend(
            os.path.join(root, f"Mastercam {version}")
            for root in PROGRAM_FILES_ROOTS
            if os.path.exists(os.path.join(root, f"Mastercam {version}"))
        )
        if not leftovers:
            leftovers.append(os.path.join(PROGRAM_FILES_ROOTS[0], f"Mastercam {version}"))
    if has_program_updater_files:
        leftovers.extend(
            os.path.join(root, f"Mastercam {version} Updater")
            for root in PROGRAM_FILES_ROOTS
            if os.path.exists(os.path.join(root, f"Mastercam {version} Updater"))
        )
        if not any("Updater" in item for item in leftovers):
            leftovers.append(os.path.join(PROGRAM_FILES_ROOTS[0], f"Mastercam {version} Updater"))
    if has_registry:
        leftovers.append("CNC Software registry keys")
    if has_my_documents:
        leftovers.append("user document folder")
    if has_shared_documents:
        leftovers.append("shared document folder")

    if has_uninstaller:
        status = "installed"
    elif leftovers:
        status = "leftover"
    else:
        status = "none"

    return {
        "version": version,
        "status": status,
        "has_uninstaller": has_uninstaller,
        "has_program_files": has_program_files,
        "has_program_updater_files": has_program_updater_files,
        "has_registry": has_registry,
        "has_shared_documents": has_shared_documents,
        "has_my_documents": has_my_documents,
        "leftovers": leftovers,
    }


def get_installed_versions() -> list[str]:
    """
    Detect Mastercam versions that are installed or still have leftover artifacts.
    Returns sorted year strings such as ['2024', '2025'].
    """
    versions: set[str] = set()
    versions.update(_registered_uninstall_versions())
    versions.update(_program_files_mastercam_versions())
    versions.update(_registry_mastercam_versions(winreg.HKEY_LOCAL_MACHINE))
    versions.update(_registry_mastercam_versions(winreg.HKEY_CURRENT_USER))
    versions.update(_my_mastercam_versions())
    versions.update(_shared_mastercam_versions())
    versions.update(_mastercam_versions_updater())
    return sorted(versions, reverse=True)


def format_version_option(version: str) -> str:
    """Build a dropdown label that distinguishes installed products from leftover artifacts."""
    info = get_version_cleanup_info(version)
    if info["status"] == "installed":
        return version
    if info["status"] == "leftover":
        return f"{version} (leftover cleanup)"
    return version


def parse_version_option(option_text: str) -> str:
    """Extract the year string from a dropdown label."""
    match = re.match(r"^(\d{4})", option_text)
    return match.group(1) if match else option_text


def _make_silent_uninstall_cmd(uninstall_cmd: str) -> str:
    """Convert a Windows uninstall command into a silent, unattended form."""
    cmd = uninstall_cmd.strip()
    lower_cmd = cmd.lower()

    if "msiexec" in lower_cmd:
        guid_match = MSI_PRODUCT_CODE_RE.search(cmd)
        if guid_match:
            return f"msiexec /x {guid_match.group(0)} /qn /norestart"
        cmd = re.sub(r"(?i)\s/I\s", " /X ", cmd)
        if "/qn" not in lower_cmd and "/quiet" not in lower_cmd:
            cmd = f"{cmd} /qn /norestart"
        return cmd

    if "-silent" not in lower_cmd and " /s" not in lower_cmd and " -s" not in lower_cmd:
        cmd = f"{cmd} -silent"
    return cmd


def get_uninstall_commands(version: str) -> list[tuple[str, str]]:
    """
    Collect silent uninstallation commands for the selected Mastercam version and its
    related components (language packs, updaters). InstallShield entries are preferred
    over duplicate MSI registrations for the main product.
    """
    components = []
    seen = set()

    for display_name, uninstall_cmd in _iter_uninstall_entries():
        if not re.match(rf"^Mastercam {version}(\s|$)", display_name):
            continue

        silent_cmd = _make_silent_uninstall_cmd(uninstall_cmd)
        if silent_cmd in seen:
            continue
        seen.add(silent_cmd)

        is_main_product = display_name == f"Mastercam {version}"
        is_installshield = "installshield" in uninstall_cmd.lower()
        components.append((display_name, silent_cmd, is_main_product, is_installshield))

    if not components:
        return []

    def sort_key(item):
        display_name, _, is_main_product, is_installshield = item
        if is_main_product and is_installshield:
            return (0, display_name)
        if is_main_product:
            return (1, display_name)
        if "Updater" in display_name:
            return (2, display_name)
        if "Language Pack" in display_name:
            return (3, display_name)
        return (4, display_name)

    components.sort(key=sort_key)

    main_installshield = next(
        (item for item in components if item[2] and item[3]),
        None,
    )
    if main_installshield:
        components = [
            item for item in components
            if not (item[2] and not item[3])
        ]

    return [(display_name, silent_cmd) for display_name, silent_cmd, _, _ in components]


def _delete_registry_key_with_access(root, subkey: str, access: int, log=None) -> bool:
    def report(message: str) -> None:
        if log:
            log(message)

    try:
        with winreg.OpenKey(root, subkey, 0, access) as key:
            while True:
                try:
                    child_name = winreg.EnumKey(key, 0)
                    _delete_registry_key_with_access(root, f"{subkey}\\{child_name}", access, log=log)
                except OSError:
                    break
    except FileNotFoundError:
        return True
    except OSError as e:
        if getattr(e, "winerror", None) == 2:
            return True
        report(f"Error dropping registry key {subkey}: {type(e).__name__}: {e}")
        return False

    try:
        wow_view = access & (winreg.KEY_WOW64_64KEY | winreg.KEY_WOW64_32KEY)
        if wow_view:
            winreg.DeleteKeyEx(root, subkey, wow_view, 0)
        else:
            winreg.DeleteKey(root, subkey)
        report(f"Deleted registry key: {subkey}")
        return True
    except FileNotFoundError:
        return True
    except OSError as e:
        report(f"Error dropping registry key {subkey}: {type(e).__name__}: {e}")
        return False


def delete_registry_key(root, subkey: str, log=None) -> bool:
    """
    Recursively delete a registry key and all nested subkeys.
    Returns True when the key is removed or already absent.
    """
    ok = True
    for sam in _hive_sam_flags(root):
        access = winreg.KEY_READ | winreg.KEY_WRITE | sam
        if not _delete_registry_key_with_access(root, subkey, access, log=log):
            ok = False
    return ok


def _run_uninstall_command(silent_cmd: str) -> tuple[Optional[int], bool]:
    """Run an uninstallation command and return (returncode, timed_out)."""
    try:
        process = subprocess.run(
            silent_cmd,
            shell=True,
            timeout=UNINSTALL_TIMEOUT_SECONDS,
        )
        return process.returncode, False
    except subprocess.TimeoutExpired:
        return None, True


def _purge_directory(path: str, log) -> bool:
    """Delete a directory tree. Returns True on success or if already absent."""
    if not os.path.exists(path):
        log(f"Folder already clean: {path}")
        return True
    try:
        shutil.rmtree(path)
        log(f"Deleted folder: {path}")
        return True
    except OSError as e:
        log(f"Error deleting program files ({type(e).__name__}): {e}")
        return False


def execute_uninstall(
    version: str,
    log_widget,
    flags: Optional[dict] = None,
    on_progress: Optional[Callable[[float], None]] = None,
    on_step: Optional[Callable[[str, str], None]] = None,
) -> None:
    """
    Orchestrates the sequential steps of the automated clean uninstallation.
    Outputs progress in real-time to the main Tkinter console widget.
    Must be called from a background thread so long-running uninstallers do not freeze the GUI.
    """
    if flags is None:
        flags = {
            "uninstall_mc": False,
            "backup_my_mc": False,
            "backup_shared_mc": False,
            "delete_program_files": False,
            "delete_registry": False,
        }

    root = log_widget.winfo_toplevel()

    def log(message: str) -> None:
        def append():
            log_widget.insert(tk.END, message + "\n")
            log_widget.see(tk.END)

        root.after(0, append)

    def progress(value: float) -> None:
        if on_progress:
            root.after(0, lambda v=value: on_progress(v))

    def step(name: str, state: str) -> None:
        if on_step:
            root.after(0, lambda n=name, s=state: on_step(n, s))

    def show_success(had_errors: bool) -> None:
        if had_errors:
            messagebox.showwarning(
                "Completed With Warnings",
                f"Mastercam {version} cleanup finished, but some steps reported errors.\n\n"
                "Review the log for details and rerun as Administrator if registry cleanup failed.",
            )
        else:
            messagebox.showinfo("Success", f"Mastercam {version} uninstallation and cleanup process complete.")

    log(f"--- Starting Mastercam {version} Removal Process ---")
    had_errors = False
    cleanup_info = get_version_cleanup_info(version)
    leftover_mode = cleanup_info["status"] == "leftover"
    if leftover_mode:
        log("Force cleanup mode: no Windows uninstaller found for this version.")
        if cleanup_info["leftovers"]:
            log("Detected leftover artifacts:")
            for leftover in cleanup_info["leftovers"]:
                log(f"  - {leftover}")

    progress(0.0)

    # ==========================================
    # STEP 1: NATIVE WINDOWS APP UNINSTALLATION
    # ==========================================
    if leftover_mode and flags.get("uninstall_mc"):
        log("Skipping Step 1 (no registered Windows uninstaller).")
        step("uninstall_mc", "skipped")
    elif flags.get("uninstall_mc"):
        step("uninstall_mc", "active")
        log("Step 1: Running silent Windows uninstallers...")
        uninstall_commands = get_uninstall_commands(version)
        if uninstall_commands:
            for display_name, silent_cmd in uninstall_commands:
                try:
                    log(f"Removing: {display_name}")
                    log(f"Executing: {silent_cmd}")
                    returncode, timed_out = _run_uninstall_command(silent_cmd)
                    if timed_out:
                        log(f"Warning: {display_name} timed out. Continuing with cleanup...")
                        had_errors = True
                    elif returncode == 0:
                        log(f"Finished: {display_name}")
                    elif returncode == 3010:
                        log(f"Finished: {display_name} (reboot may be required)")
                    else:
                        log(f"Warning: {display_name} returned exit code {returncode}")
                        had_errors = True
                except OSError as e:
                    log(f"Error removing {display_name}: {type(e).__name__}: {e}")
                    had_errors = True
            log("Windows uninstall phase finished.")
        else:
            log("No Windows uninstall entries found. Moving to manual cleanup...")
        step("uninstall_mc", "error" if had_errors else "done")
    else:
        step("uninstall_mc", "skipped")
    progress(0.25)

    # ==========================================
    # STEP 2: RE-NAME & BACKUP CONFIG DIRECTORIES
    # ==========================================
    log("\nStep 2: Checking optional folders for backup...")
    user_profile = os.environ.get("USERPROFILE", "")

    # 1. Dynamically gather all potential base "Documents" directories
    base_docs_folders = [
        os.path.join(user_profile, "Documents")
    ]

    # Check for corporate and personal OneDrive environments
    for env_key in ["OneDriveCommercial", "OneDrive"]:
        onedrive_root = os.environ.get(env_key)
        if onedrive_root:
            onedrive_docs = os.path.join(onedrive_root, "Documents")
            if onedrive_docs not in base_docs_folders:
                base_docs_folders.append(onedrive_docs)

    def _perform_backup(target: str) -> None:
        nonlocal had_errors
        if os.path.exists(target):
            backup_path = f"{target}_backup"
            counter = 1
            while os.path.exists(backup_path):
                backup_path = f"{target}_backup_{counter}"
                counter += 1
            try:
                os.rename(target, backup_path)
                log(f"Backed up to: {backup_path}")
            except OSError as e:
                log(f"Failed to backup {target}: {type(e).__name__}: {e}")
                had_errors = True

    if flags.get("backup_my_mc"):
        step("backup_my_mc", "active")
        log("Processing 'My Mastercam' user directories...")
        my_mc_targets = []
        for base_doc in base_docs_folders:
            my_mc_targets.append(os.path.join(base_doc, f"My Mastercam {version}"))
            my_mc_targets.append(os.path.join(base_doc, f"Mastercam {version}"))
        for target in my_mc_targets:
            _perform_backup(target)
        step("backup_my_mc", "done")
    else:
        step("backup_my_mc", "skipped")

    if flags.get("backup_shared_mc"):
        step("backup_shared_mc", "active")
        log("Processing 'Shared Mastercam' public directories...")
        for target in _shared_mastercam_paths(version):
            _perform_backup(target)
        step("backup_shared_mc", "done")
    else:
        step("backup_shared_mc", "skipped")
    progress(0.50)

    # ==========================================
    # STEP 3: RESIDUAL PROGRAM FILES PURGE
    # ==========================================
    if flags.get("delete_program_files"):
        step("delete_program_files", "active")
        log("\nStep 3: Deleting Install Files directory...")
        step3_ok = True
        for root_dir in PROGRAM_FILES_ROOTS:
            if not _purge_directory(os.path.join(root_dir, f"Mastercam {version}"), log):
                step3_ok = False
                had_errors = True

        log("\nStep 3.5: Deleting Updater Files directory...")
        for root_dir in PROGRAM_FILES_ROOTS:
            if not _purge_directory(os.path.join(root_dir, f"Mastercam {version} Updater"), log):
                step3_ok = False
                had_errors = True
        step("delete_program_files", "done" if step3_ok else "error")
    else:
        step("delete_program_files", "skipped")
    progress(0.75)

    # ==========================================
    # STEP 4: ORPHANED REGISTRY DEEP CLEAN
    # ==========================================
    if flags.get("delete_registry"):
        step("delete_registry", "active")
        log("\nStep 4: Cleaning registry entries...")
        reg_suffix = f"Software\\CNC Software\\Mastercam {version}"
        registry_ok = True
        if not delete_registry_key(winreg.HKEY_CURRENT_USER, reg_suffix, log=log):
            had_errors = True
            registry_ok = False
        if not delete_registry_key(winreg.HKEY_LOCAL_MACHINE, reg_suffix, log=log):
            had_errors = True
            registry_ok = False
        step("delete_registry", "done" if registry_ok else "error")
    else:
        step("delete_registry", "skipped")


    progress(1.0)
    log("\n--- Process Finished! ---")
    progressbar_var = 1
    print(progressbar_var)
    final_error_status = had_errors
    root.after(0, lambda: show_success(final_error_status))



# endregion


def launch_gui() -> None:
    global uninstall_mc_var, uninstall_program_files_delete_var, uninstall_registry_delete_var
    global uninstall_shared_backup_var, uninstall_my_backup_var, dropdown, log_text, restart_app, main_app

    main_app = customtkinter.CTk()
    main_app.title("MC Assist V0.3")
    main_app.geometry("800x600")
    main_app.resizable(False, False)
    main_app.configure(fg_color=background_color_light)
    main_app.configure(bg_color=background_color)

    uninstall_thread: Optional[threading.Thread] = None



    def configure_show_button(widget, enabled: bool) -> None:
        if enabled:
            widget.configure(state="normal", border_color=main_color, border_width=1, fg_color="transparent")
        else:
            widget.configure(
                state="disabled",
                border_color=background_color_light,
                border_width=2,
                fg_color="transparent",
            )

    def any_uninstall_flag() -> bool:
        return (
            uninstall_mc_var.get() == "on"
            or uninstall_my_backup_var.get() == "on"
            or uninstall_shared_backup_var.get() == "on"
            or uninstall_program_files_delete_var.get() == "on"
            or uninstall_registry_delete_var.get() == "on"
        )

    def collect_flags() -> dict:
        return {
            "uninstall_mc": uninstall_mc_var.get() == "on",
            "backup_my_mc": uninstall_my_backup_var.get() == "on",
            "backup_shared_mc": uninstall_shared_backup_var.get() == "on",
            "delete_program_files": uninstall_program_files_delete_var.get() == "on",
            "delete_registry": uninstall_registry_delete_var.get() == "on",
        }

    def update_start_uninstall_state() -> None:
        busy = uninstall_thread is not None and uninstall_thread.is_alive()
        if busy or dropdown.get() in PLACEHOLDER_OPTIONS or not any_uninstall_flag():
            start_uninstall.configure(state="disabled", border_color=background_color_light, border_width=2)
        else:
            start_uninstall.configure(state="normal", border_color=main_color, border_width=1)

    def dropdown_callback_f(choice: str) -> None:
        selected_option = choice

        if selected_option in PLACEHOLDER_OPTIONS:
            uninstall_select_all.configure(
                state="disabled", border_color=background_color_light, border_width=2, fg_color=background_color_light
            )
            uninstall_mc.configure(
                state="disabled", border_color=background_color_light, border_width=2, fg_color=background_color_light
            )
            uninstall_my_backup.configure(
                state="disabled", border_color=background_color_light, border_width=2, fg_color=background_color_light
            )
            uninstall_shared_backup.configure(
                state="disabled", border_color=background_color_light, border_width=2, fg_color=background_color_light
            )
            uninstall_program_files_delete.configure(
                state="disabled", border_color=background_color_light, border_width=2, fg_color=background_color_light
            )
            uninstall_registry_delete.configure(
                state="disabled", border_color=background_color_light, border_width=2, fg_color=background_color_light
            )
            configure_show_button(show_files_my_mc, False)
            configure_show_button(show_files_shared_mc, False)
            configure_show_button(show_files_program_files, False)
            configure_show_button(show_files_update_files, False)
            configure_show_button(show_files_registry, False)
            update_start_uninstall_state()
            return

        uninstall_select_all.configure(state="normal", border_color=main_color, border_width=1, fg_color=main_color)
        uninstall_mc.configure(state="normal", border_color=main_color, border_width=1, fg_color=main_color)
        uninstall_my_backup.configure(state="normal", border_color=main_color, border_width=1, fg_color=main_color)
        uninstall_shared_backup.configure(state="normal", border_color=main_color, border_width=1, fg_color=main_color)
        uninstall_program_files_delete.configure(
            state="normal", border_color=main_color, border_width=1, fg_color=main_color
        )
        uninstall_registry_delete.configure(
            state="normal", border_color=main_color, border_width=1, fg_color=main_color
        )

        version = parse_version_option(selected_option)
        info = get_version_cleanup_info(version)
        configure_show_button(show_files_my_mc, info["has_my_documents"])
        configure_show_button(show_files_shared_mc, info["has_shared_documents"])
        configure_show_button(show_files_program_files, info["has_program_files"])
        configure_show_button(show_files_update_files, info["has_program_updater_files"])
        configure_show_button(show_files_registry, info["has_registry"])
        update_start_uninstall_state()

    def uninstall_select_all_f() -> None:
        if uninstall_select_all_var.get() == "on":
            uninstall_mc.select()
            uninstall_my_backup.select()
            uninstall_shared_backup.select()
            uninstall_program_files_delete.select()
            uninstall_registry_delete.select()
        else:
            uninstall_mc.deselect()
            uninstall_my_backup.deselect()
            uninstall_shared_backup.deselect()
            uninstall_program_files_delete.deselect()
            uninstall_registry_delete.deselect()
        update_start_uninstall_state()

    def sync_select_all() -> None:
        all_checked = (
            uninstall_mc_var.get() == "on"
            and uninstall_my_backup_var.get() == "on"
            and uninstall_shared_backup_var.get() == "on"
            and uninstall_program_files_delete_var.get() == "on"
            and uninstall_registry_delete_var.get() == "on"
        )
        if all_checked:
            uninstall_select_all.select()
        else:
            uninstall_select_all.deselect()
        update_start_uninstall_state()

    import os

    def show_files_my_mc_f() -> None:
        version = parse_version_option(dropdown.get())
        user_profile = os.environ.get("USERPROFILE", "")

        # 1. Gather all potential base "Documents" directories dynamically
        base_doc_paths = [
            os.path.join(user_profile, "Documents")
        ]

        # Check for corporate and personal OneDrive environments
        for env_key in ["OneDriveCommercial", "OneDrive"]:
            onedrive_root = os.environ.get(env_key)
            if onedrive_root:
                onedrive_docs = os.path.join(onedrive_root, "Documents")
                if onedrive_docs not in base_doc_paths:
                    base_doc_paths.append(onedrive_docs)

        # 2. Construct the specific subfolder variations for each base path
        possible_paths = []
        for doc_path in base_doc_paths:
            possible_paths.append(os.path.join(doc_path, f"My Mastercam {version}"))
            possible_paths.append(os.path.join(doc_path, f"Mastercam {version}"))

        # 3. Find the first path that actually exists on disk
        found_path = next((p for p in possible_paths if os.path.exists(p)), None)

        if found_path:
            _open_in_explorer(found_path)
        else:
            messagebox.showinfo(title="Not Found", message=f"Original Mastercam folder for {version} no longer exists.")

    def show_files_shared_mc_f() -> None:
        version = parse_version_option(dropdown.get())
        found_path = next((p for p in _shared_mastercam_paths(version) if os.path.exists(p)), None)
        if found_path:
            _open_in_explorer(found_path)
        else:
            messagebox.showinfo("Not Found", f"Original Shared Mastercam folder for {version} no longer exists.")

    def show_files_program_files_f() -> None:
        version = parse_version_option(dropdown.get())
        possible_paths = [os.path.join(root, f"Mastercam {version}") for root in PROGRAM_FILES_ROOTS]
        found_path = next((p for p in possible_paths if os.path.exists(p)), None)
        if found_path:
            _open_in_explorer(found_path)
        else:
            messagebox.showinfo("Not Found", f"Program Files folder for Mastercam {version} no longer exists.")

    def show_files_update_files_f() -> None:
        version = parse_version_option(dropdown.get())
        possible_paths = [os.path.join(root, f"Mastercam {version} Updater") for root in PROGRAM_FILES_ROOTS]
        found_path = next((p for p in possible_paths if os.path.exists(p)), None)
        if found_path:
            _open_in_explorer(found_path)
        else:
            messagebox.showinfo("Not Found", f"Updater folder for Mastercam {version} no longer exists.")

    def show_files_registry_f() -> None:
        try:
            subprocess.Popen(["regedit.exe"])
        except OSError as e:
            messagebox.showerror("Error", f"Failed to open Registry Editor: {type(e).__name__}: {e}")

    def apply_step_state(name: str, state: str) -> None:
        widget = step_buttons.get(name)
        if widget is None:
            return
        if state == "active":
            widget.configure(fg_color=main_color, border_color=main_color)
        elif state == "done":
            widget.configure(fg_color=dropdown_button_color, border_color=dropdown_button_color)
        elif state == "error":
            widget.configure(fg_color="#ff5901", border_color="#ff5901")
        else:
            widget.configure(fg_color="transparent", border_color=main_color)

    def reset_step_buttons() -> None:
        for widget in step_buttons.values():
            widget.configure(fg_color="transparent", border_color=main_color)

    # def function_restart() -> None:
    #     dropdown.configure(state="disabled", border_color=background_color_light, border_width=2, button_color=background_color_light)
    #     dropdown.update()
    #     restart_app.configure(text_color="Red")
    #     restart_app.update()
    #
    # if progressbar_var == 1:
    #     function_restart()




    # region -- Background features --------------
    ribbon_bar = customtkinter.CTkFrame(master=main_app, width=776, height=70, corner_radius=0, fg_color=background_color)
    ribbon_bar.place(relx=0.5, rely=0.012, anchor="n")

    uninstall_box = customtkinter.CTkFrame(master=main_app, width=380, height=320, corner_radius=0, fg_color=background_color)
    uninstall_box.place(relx=0.49, rely=0.14, anchor="ne")

    install_box = customtkinter.CTkFrame(master=main_app, width=380, height=320, corner_radius=0, fg_color=background_color)
    install_box.place(relx=0.51, rely=0.14, anchor="nw")

    progress_box = customtkinter.CTkFrame(master=main_app, width=776, height=181, corner_radius=0, fg_color=background_color)
    progress_box.place(relx=0.5, rely=0.988, anchor="s")
    # endregion

    # region --Uninstall Label----------------------------------
    uninstall_reinstall_uninstall_options = customtkinter.CTkLabel(
        main_app,
        text="Uninstall Options",
        fg_color="transparent",
        text_color=main_color,
        font=("Arial", 20, "bold"),
        bg_color=background_color,
    )
    uninstall_reinstall_uninstall_options.place(relx=0.05, rely=0.18, anchor="w")
    # endregion

    # region -- Uninstall Check Boxes-----------------------
    uninstall_select_all_var = customtkinter.StringVar(value="on")
    uninstall_select_all = customtkinter.CTkCheckBox(
        main_app,
        text="Select All",
        command=uninstall_select_all_f,
        variable=uninstall_select_all_var,
        onvalue="on",
        offvalue="off",
        hover_color=hover_color,
        checkbox_width=20,
        checkbox_height=20,
        checkmark_color=background_color,
        corner_radius=0,
        border_width=1,
        fg_color=main_color,
        border_color=main_color,
        bg_color=background_color,
    )
    uninstall_select_all.place(relx=0.05, rely=0.23, anchor="w")

    uninstall_mc_var = customtkinter.StringVar(value="on")
    uninstall_mc = customtkinter.CTkCheckBox(
        main_app,
        text="Uninstall Mastercam",
        command=sync_select_all,
        variable=uninstall_mc_var,
        onvalue="on",
        offvalue="off",
        hover_color=hover_color,
        checkbox_width=20,
        checkbox_height=20,
        checkmark_color=background_color,
        corner_radius=0,
        border_width=1,
        fg_color=main_color,
        border_color=main_color,
        bg_color=background_color,
    )
    uninstall_mc.place(relx=0.1, rely=0.28, anchor="w")

    uninstall_my_backup_var = customtkinter.StringVar(value="on")
    uninstall_my_backup = customtkinter.CTkCheckBox(
        main_app,
        text="Backup My Mastercam Folder",
        command=sync_select_all,
        variable=uninstall_my_backup_var,
        onvalue="on",
        offvalue="off",
        hover_color=hover_color,
        checkbox_width=20,
        checkbox_height=20,
        checkmark_color=background_color,
        corner_radius=0,
        border_width=1,
        fg_color=main_color,
        border_color=main_color,
        bg_color=background_color,
    )
    uninstall_my_backup.place(relx=0.1, rely=0.36, anchor="w")

    uninstall_shared_backup_var = customtkinter.StringVar(value="on")
    uninstall_shared_backup = customtkinter.CTkCheckBox(
        main_app,
        text="Backup Shared Mastercam Folder",
        command=sync_select_all,
        variable=uninstall_shared_backup_var,
        onvalue="on",
        offvalue="off",
        hover_color=hover_color,
        checkbox_width=20,
        checkbox_height=20,
        checkmark_color=background_color,
        corner_radius=0,
        border_width=1,
        fg_color=main_color,
        border_color=main_color,
        bg_color=background_color,
    )
    uninstall_shared_backup.place(relx=0.1, rely=0.44, anchor="w")

    uninstall_program_files_delete_var = customtkinter.StringVar(value="on")
    uninstall_program_files_delete = customtkinter.CTkCheckBox(
        main_app,
        text="Delete Program Files",
        command=sync_select_all,
        variable=uninstall_program_files_delete_var,
        onvalue="on",
        offvalue="off",
        hover_color=hover_color,
        checkbox_width=20,
        checkbox_height=20,
        checkmark_color=background_color,
        corner_radius=0,
        border_width=1,
        fg_color=main_color,
        border_color=main_color,
        bg_color=background_color,
    )
    uninstall_program_files_delete.place(relx=0.1, rely=0.52, anchor="w")

    uninstall_registry_delete_var = customtkinter.StringVar(value="on")
    uninstall_registry_delete = customtkinter.CTkCheckBox(
        main_app,
        text="Delete Registries",
        command=sync_select_all,
        variable=uninstall_registry_delete_var,
        onvalue="on",
        offvalue="off",
        hover_color=hover_color,
        checkbox_width=20,
        checkbox_height=20,
        checkmark_color=background_color,
        corner_radius=0,
        border_width=1,
        fg_color=main_color,
        border_color=main_color,
        bg_color=background_color,
    )
    uninstall_registry_delete.place(relx=0.1, rely=0.60, anchor="w")
    # endregion

    # region -- Progressbar----------------------------------------------
    label = customtkinter.CTkLabel(
        main_app, text="Progress", fg_color="transparent", text_color=text_color, bg_color=background_color
    )
    label.place(relx=0.06, rely=0.73, anchor="w")

    progressbar = customtkinter.CTkProgressBar(
        main_app, orientation="horizontal", width=280, height=12, corner_radius=0, progress_color=main_color
    )
    progressbar.set(progressbar_var)
    progressbar.place(relx=0.24, rely=0.78, anchor="center")
    # endregion

    # region -- Uninstall Process----------------------------------------
    label_uninstall = customtkinter.CTkLabel(
        main_app, text="Uninstall steps", fg_color="transparent", text_color=text_color, bg_color=background_color
    )
    label_uninstall.place(relx=0.06, rely=0.83, anchor="w")

    button_uninstall_process = customtkinter.CTkButton(
        main_app,
        text="",
        fg_color="transparent",
        hover_color=hover_color,
        width=16 * 3,
        height=16,
        corner_radius=8,
        border_color=main_color,
        border_width=1,
        state="disabled",
    )
    button_uninstall_process.place(relx=0.09, rely=0.88, anchor="center")
    ToolTip(button_uninstall_process, msg="Mastercam Uninstall", delay=0.0)

    button_my_mastercam_backup = customtkinter.CTkButton(
        main_app,
        text="",
        fg_color="transparent",
        hover_color=hover_color,
        width=16 * 3,
        height=16,
        corner_radius=8,
        border_color=main_color,
        border_width=1,
        state="disabled",
    )
    button_my_mastercam_backup.place(relx=0.17, rely=0.88, anchor="center")
    ToolTip(button_my_mastercam_backup, msg="My Mastercam Backup", delay=0.0)

    button_shared_mastercam_backup = customtkinter.CTkButton(
        main_app,
        text="",
        fg_color="transparent",
        hover_color=hover_color,
        width=16 * 3,
        height=16,
        corner_radius=8,
        border_color=main_color,
        border_width=1,
        state="disabled",
    )
    button_shared_mastercam_backup.place(relx=0.25, rely=0.88, anchor="center")
    ToolTip(button_shared_mastercam_backup, msg="Shared Mastercam Backup", delay=0.0)

    button_program_files_delete = customtkinter.CTkButton(
        main_app,
        text="",
        fg_color="transparent",
        hover_color=hover_color,
        width=16 * 3,
        height=16,
        corner_radius=8,
        border_color=main_color,
        border_width=1,
        state="disabled",
    )
    button_program_files_delete.place(relx=0.33, rely=0.88, anchor="center")
    ToolTip(button_program_files_delete, msg="Program Files Delete", delay=0.0)

    button_registry_delete = customtkinter.CTkButton(
        main_app,
        text="",
        fg_color="transparent",
        hover_color=hover_color,
        width=16 * 3,
        height=16,
        corner_radius=8,
        border_color=main_color,
        border_width=1,
        state="disabled",
    )
    button_registry_delete.place(relx=0.41, rely=0.88, anchor="center")
    ToolTip(button_registry_delete, msg="Registry Delete", delay=0.0)

    step_buttons = {
        "uninstall_mc": button_uninstall_process,
        "backup_my_mc": button_my_mastercam_backup,
        "backup_shared_mc": button_shared_mastercam_backup,
        "delete_program_files": button_program_files_delete,
        "delete_registry": button_registry_delete,
    }
    # endregion

    # region -- Show Left over files on PC
    show_files_files_on_pc = customtkinter.CTkLabel(
        main_app,
        text="Files On PC",
        fg_color="transparent",
        text_color=main_color,
        font=("Arial", 20, "bold"),
        bg_color=background_color,
    )
    show_files_files_on_pc.place(relx=0.55, rely=0.18, anchor="w")

    show_files_my_mc = customtkinter.CTkButton(
        main_app,
        text="My Mastercam",
        command=show_files_my_mc_f,
        fg_color="transparent",
        hover_color=hover_color,
        text_color=text_color,
        width=200,
        height=28,
        border_color=main_color,
        border_width=1,
    )
    show_files_my_mc.place(relx=0.75, rely=0.25, anchor="center")
    ToolTip(show_files_my_mc, msg="Show Files Location", delay=0.5)

    show_files_shared_mc = customtkinter.CTkButton(
        main_app,
        text="Shared Mastercam",
        command=show_files_shared_mc_f,
        fg_color="transparent",
        hover_color=hover_color,
        text_color=text_color,
        width=200,
        height=28,
        border_color=main_color,
        border_width=1,
    )
    show_files_shared_mc.place(relx=0.75, rely=0.34, anchor="center")
    ToolTip(show_files_shared_mc, msg="Show Files Location", delay=0.5)

    show_files_program_files = customtkinter.CTkButton(
        main_app,
        text="Installation on PC",
        command=show_files_program_files_f,
        fg_color="transparent",
        hover_color=hover_color,
        text_color=text_color,
        width=200,
        height=28,
        border_color=main_color,
        border_width=1,
    )
    show_files_program_files.place(relx=0.75, rely=0.43, anchor="center")
    ToolTip(show_files_program_files, msg="Show Files Location", delay=0.5)

    show_files_update_files = customtkinter.CTkButton(
        main_app,
        text="Program Update Files",
        command=show_files_update_files_f,
        fg_color="transparent",
        hover_color=hover_color,
        text_color=text_color,
        width=200,
        height=28,
        border_color=main_color,
        border_width=1,
    )
    show_files_update_files.place(relx=0.75, rely=0.52, anchor="center")
    ToolTip(show_files_update_files, msg="Show Files Location", delay=0.5)

    show_files_registry = customtkinter.CTkButton(
        main_app,
        text="Registry",
        command=show_files_registry_f,
        fg_color="transparent",
        hover_color=hover_color,
        text_color=text_color,
        width=200,
        height=28,
        border_color=main_color,
        border_width=1,
    )
    show_files_registry.place(relx=0.75, rely=0.61, anchor="center")
    ToolTip(show_files_registry, msg="Open Registry Editor", delay=0.5)
    # endregion

    # region -- Dropdown----------------------------------------------------
    version_var = customtkinter.StringVar(value="Select MC Version...")
    dropdown = customtkinter.CTkOptionMenu(
        main_app,
        variable=version_var,
        fg_color=hover_color,
        button_color=main_color,
        button_hover_color=hover_color,
        width=200,
        height=28,
        command=dropdown_callback_f,
        bg_color=background_color,
    )
    dropdown.place(relx=0.2, rely=0.07, anchor="center")

    def refresh_version_list() -> None:
        refreshed_versions = get_installed_versions()
        if refreshed_versions:
            formatted_options = [format_version_option(v) for v in refreshed_versions]
            dropdown.configure(values=formatted_options)
            dropdown.set("Select MC Version...")
        else:
            dropdown.configure(values=["No Mastercam installations detected"])
            dropdown.set("No Mastercam installations detected")
        dropdown_callback_f(dropdown.get())

    installed_versions = get_installed_versions()
    if installed_versions:
        formatted_options = [format_version_option(v) for v in installed_versions]
        dropdown.configure(values=formatted_options)
        dropdown.set("Select MC Version...")
    else:
        dropdown.configure(values=["No Mastercam installations detected"])
        dropdown.set("No Mastercam installations detected")
    # endregion

    log_text = tk.Text(
        main_app,
        height=8,
        width=42,
        font=("Consolas", 9),
        bg=background_color,
        fg=text_color,
        insertbackground=text_color,
        relief="flat",
        highlightthickness=0,
    )
    log_text.place(relx=0.98, rely=0.73, anchor="ne", width=360, height=140)

    def start_uninstall_f() -> None:
        nonlocal uninstall_thread
        selected_option = version_var.get()
        if selected_option in PLACEHOLDER_OPTIONS:
            messagebox.showinfo(
                "Nothing to Uninstall",
                "No installed Mastercam versions were detected, or no version is selected.",
            )
            return

        flags = collect_flags()
        if not any(flags.values()):
            messagebox.showinfo("No Steps Selected", "Select at least one uninstall option before continuing.")
            return

        selected_version = parse_version_option(selected_option)
        if not re.match(r"^\d{4}$", selected_version):
            messagebox.showinfo("Invalid Selection", "Select a Mastercam version from the dropdown.")
            return

        cleanup_info = get_version_cleanup_info(selected_version)
        if cleanup_info["status"] == "leftover":
            leftover_lines = "\n".join(f"- {item}" for item in cleanup_info["leftovers"])
            confirm_message = (
                f"Mastercam {selected_version} is no longer registered in Windows, but leftover "
                f"files or registry entries were found.\n\n"
                f"Detected leftovers:\n{leftover_lines}\n\n"
                "Run force cleanup for this version?"
            )
        else:
            confirm_message = (
                f"Are you sure you want to completely remove Mastercam {selected_version}?\n\n"
                "This will run silent uninstallers and then clean remaining files and registry entries."
            )

        if not messagebox.askyesno("Confirm Action", confirm_message):
            return

        start_uninstall.configure(state="disabled")
        reset_step_buttons()
        progressbar.set(0.0)
        log_text.delete("1.0", tk.END)

        def worker():
            try:
                execute_uninstall(
                    selected_version,
                    log_text,
                    flags,
                    on_progress=progressbar.set,
                    on_step=apply_step_state,
                )
            finally:
                def cleanup_gui():
                    refresh_version_list()

                main_app.after(0, cleanup_gui)

        uninstall_thread = threading.Thread(target=worker, daemon=False)
        uninstall_thread.start()

    start_uninstall = customtkinter.CTkButton(
        main_app,
        text="Uninstall",
        command=start_uninstall_f,
        fg_color="transparent",
        hover_color=hover_color,
        text_color=text_color,
        width=125,
        height=28,
        border_color=main_color,
        border_width=1,
        bg_color=background_color,
    )
    start_uninstall.place(relx=0.45, rely=0.07, anchor="center")

    restart_app = customtkinter.CTkLabel(
        main_app,
        text="Please restart app",
        fg_color="transparent",
        text_color=restart_text_color,
        font=("Arial", 20, "bold"),
        bg_color=background_color,
    )
    restart_app.place(relx=0.65, rely=0.07, anchor="w")

    def on_close() -> None:
        if uninstall_thread is not None and uninstall_thread.is_alive():
            if not messagebox.askyesno(
                "Uninstall in progress",
                "An uninstall is still running. Closing will interrupt it and may leave files half-removed.\n\nQuit anyway?",
            ):
                return
        main_app.destroy()

    main_app.protocol("WM_DELETE_WINDOW", on_close)
    dropdown_callback_f(dropdown.get())
    set_app_icon(main_app)
    main_app.mainloop()


if __name__ == "__main__":

    run_as_admin()
    if is_admin():
        launch_gui()
