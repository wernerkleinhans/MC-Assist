import os
import re
import sys
import shutil
import winreg
import ctypes
import threading
import subprocess
import tkinter as tk
from tkinter import messagebox, ttk

UNINSTALL_TIMEOUT_SECONDS = 3600

UNINSTALL_SEARCH_PATHS = [
    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall"),
    (winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\Wow6432Node\Microsoft\Windows\CurrentVersion\Uninstall"),
]

INSTRUCTIONS_FILENAME = "MC Assist V0.1 Instructions.txt"
ICON_BASENAME = "MC Assist V0.1"

# Embedded fallback used when the instructions file is not found (e.g. compiled .exe).
INSTRUCTIONS_TEXT = """MC ASSIST V0.1 - QUICK INSTRUCTIONS
====================================

BEFORE YOU START
  - Close Mastercam and any related software (CIMCO, etc.).
  - Accept the Administrator (UAC) prompt when the app opens.
  - Read the log window as each step runs.


USING THE APP
  1. Select a Mastercam year from the dropdown.
  2. Click "Begin Clean Uninstall" and confirm.
  3. Wait until the log shows "Process Finished!".


WHAT THE DROPDOWN MEANS
  2025              = Fully installed; runs silent uninstall + cleanup.
  2024 (leftover)   = Already removed from Windows, but files/registry
                      remain. Runs cleanup only (no uninstall wizard).


WHAT HAPPENS (4 STEPS)
  Step 1  Silent Windows uninstall (skipped for leftover cleanup).
  Step 2  Your document folders are RENAMED with _backup (not deleted).
          Posts, machines, and configs are preserved.
  Step 3  Deletes C:\\Program Files\\Mastercam <Version>
  Step 4  Removes CNC Software registry keys for that version.


AFTER CLEANUP
  - Reboot if Windows asks, or if licensing issues persist.
  - To restore user data: rename the _backup folder back after reinstalling
    the same version, or copy files into the new Mastercam user folder.


IF SOMETHING FAILS
  - "Access is denied" on Step 4: rerun the app and accept the UAC prompt.
  - Close any Mastercam processes in Task Manager and try again.
  - Check the log for details. A warning dialog means some steps had errors
    but cleanup may still have partially completed.


NOTE
  Only one Mastercam version is removed per run. Other installed versions
  on the same PC are not affected.
"""


def _app_directory():
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def _resource_directory():
    """Return the folder containing bundled assets such as the application icon."""
    if getattr(sys, "frozen", False):
        return getattr(sys, "_MEIPASS", _app_directory())
    return os.path.dirname(os.path.abspath(__file__))


def _icon_path(extension):
    for directory in (_resource_directory(), _app_directory()):
        icon_path = os.path.join(directory, f"{ICON_BASENAME}{extension}")
        if os.path.exists(icon_path):
            return icon_path
    return None


def set_app_icon(window):
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


def load_instructions_text():
    instructions_path = os.path.join(_app_directory(), INSTRUCTIONS_FILENAME)
    try:
        with open(instructions_path, encoding="utf-8") as instructions_file:
            return instructions_file.read()
    except OSError:
        return INSTRUCTIONS_TEXT


def is_admin():
    """
    Checks if the script process currently possesses Windows administrative tokens.
    Uses ctypes to query the Windows shell32 API directly.
    """
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False


def run_as_admin():
    """
    Forces the script to relaunch itself using the 'runas' verb to trigger a
    Windows User Account Control (UAC) prompt if it is not already running with
    elevated permissions.
    """
    if not is_admin():
        # Quote paths correctly so the script works when run directly via python.exe
        # (e.g. project folders containing spaces) as well as from a compiled .exe.
        if getattr(sys, "frozen", False):
            params = subprocess.list2cmdline(sys.argv[1:])
        else:
            params = subprocess.list2cmdline(sys.argv)
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, params, None, 1)
        sys.exit()  # Kill the non-privileged initial instance immediately.


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


def _version_from_display_name(display_name):
    """Extract a Mastercam year from a registry DisplayName, or return None."""
    match = re.match(r"^Mastercam (\d{4})(?:\s|$)", display_name)
    return match.group(1) if match else None


def _registry_mastercam_versions(hive, subkey=r"SOFTWARE\CNC Software"):
    """Return Mastercam year strings found under a CNC Software registry key."""
    versions = set()
    try:
        with winreg.OpenKey(hive, subkey) as key:
            for i in range(winreg.QueryInfoKey(key)[0]):
                name = winreg.EnumKey(key, i)
                match = re.match(r"^Mastercam (\d{4})$", name)
                if match:
                    versions.add(match.group(1))
    except OSError:
        pass
    return versions


def _program_files_mastercam_versions():
    """Return Mastercam year strings found from Mastercam folders in Program Files."""
    versions = set()
    for program_files in (r"C:\Program Files", r"C:\Program Files (x86)"):
        if not os.path.isdir(program_files):
            continue
        for folder_name in os.listdir(program_files):
            match = re.match(r"^Mastercam (\d{4})$", folder_name)
            if match:
                versions.add(match.group(1))
    return versions


def _documents_mastercam_versions():
    """Return Mastercam year strings found from user and shared document folders."""
    versions = set()
    user_profile = os.environ.get("USERPROFILE", "")
    public_profile = os.environ.get("PUBLIC", r"C:\Users\Public")

    doc_roots = [
        os.path.join(user_profile, "OneDrive", "Documents"),
        os.path.join(user_profile, "Documents"),
        os.path.join(public_profile, "Documents"),
    ]

    for doc_root in doc_roots:
        if not os.path.isdir(doc_root):
            continue
        for folder_name in os.listdir(doc_root):
            match = re.match(r"^(?:My )?Mastercam (\d{4})$|^Shared Mastercam (\d{4})$", folder_name)
            if match:
                versions.add(match.group(1) or match.group(2))

    return versions


def _registered_uninstall_versions():
    """Return Mastercam year strings that still have Windows uninstall registry entries."""
    versions = set()
    for display_name, _ in _iter_uninstall_entries():
        version = _version_from_display_name(display_name)
        if version:
            versions.add(version)
    return versions


def get_version_cleanup_info(version):
    """
    Inspect the machine for leftover Mastercam artifacts for one version.
    Returns a dict describing what was found and whether force cleanup is needed.
    """
    has_uninstaller = version in _registered_uninstall_versions()
    has_program_files = version in _program_files_mastercam_versions()
    has_registry = (
        version in _registry_mastercam_versions(winreg.HKEY_LOCAL_MACHINE)
        or version in _registry_mastercam_versions(winreg.HKEY_CURRENT_USER)
    )
    has_documents = version in _documents_mastercam_versions()

    leftovers = []
    if has_program_files:
        leftovers.append(f"C:\\Program Files\\Mastercam {version}")
    if has_registry:
        leftovers.append("CNC Software registry keys")
    if has_documents:
        leftovers.append("user/shared document folders")

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
        "leftovers": leftovers,
    }


def get_installed_versions():
    """
    Detect Mastercam versions that are installed or still have leftover artifacts.
    Returns sorted year strings such as ['2024', '2025'].
    """
    versions = set()
    versions.update(_registered_uninstall_versions())
    versions.update(_program_files_mastercam_versions())
    versions.update(_registry_mastercam_versions(winreg.HKEY_LOCAL_MACHINE))
    versions.update(_registry_mastercam_versions(winreg.HKEY_CURRENT_USER))
    versions.update(_documents_mastercam_versions())
    return sorted(versions, reverse=True)


def format_version_option(version):
    """Build a dropdown label that distinguishes installed products from leftover artifacts."""
    info = get_version_cleanup_info(version)
    if info["status"] == "installed":
        return version
    if info["status"] == "leftover":
        return f"{version} (leftover cleanup)"
    return version


def parse_version_option(option_text):
    """Extract the year string from a dropdown label."""
    match = re.match(r"^(\d{4})", option_text)
    return match.group(1) if match else option_text


def _make_silent_uninstall_cmd(uninstall_cmd):
    """Convert a Windows uninstall command into a silent, unattended form."""
    cmd = uninstall_cmd.strip()
    lower_cmd = cmd.lower()

    if lower_cmd.startswith("msiexec"):
        if "/qn" not in lower_cmd and "/quiet" not in lower_cmd:
            cmd = f"{cmd} /qn /norestart"
        return cmd

    if "-silent" not in lower_cmd and " /s" not in lower_cmd and " -s" not in lower_cmd:
        cmd = f"{cmd} -silent"
    return cmd


def get_uninstall_commands(version):
    """
    Collect silent uninstall commands for the selected Mastercam version and its
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


def delete_registry_key(root, subkey, log=None):
    """
    Recursively delete a registry key and all nested subkeys.
    Returns True when the key is removed or already absent.
    """
    access = winreg.KEY_READ | winreg.KEY_WRITE

    def report(message):
        if log:
            log(message)

    try:
        with winreg.OpenKey(root, subkey, 0, access) as key:
            while True:
                try:
                    child_name = winreg.EnumKey(key, 0)
                    delete_registry_key(root, f"{subkey}\\{child_name}", log=log)
                except OSError:
                    break
    except FileNotFoundError:
        return True
    except OSError as e:
        if getattr(e, "winerror", None) == 2:
            return True
        report(f"Error dropping registry key {subkey}: {e}")
        return False

    try:
        winreg.DeleteKey(root, subkey)
        report(f"Deleted registry key: {subkey}")
        return True
    except FileNotFoundError:
        return True
    except OSError as e:
        report(f"Error dropping registry key {subkey}: {e}")
        return False


def _run_uninstall_command(silent_cmd):
    """Run an uninstall command and return (returncode, timed_out)."""
    try:
        process = subprocess.run(
            silent_cmd,
            shell=True,
            timeout=UNINSTALL_TIMEOUT_SECONDS,
        )
        return process.returncode, False
    except subprocess.TimeoutExpired:
        return None, True


def execute_uninstall(version, log_widget):
    """
    Orchestrates the sequential steps of the automated clean uninstallation.
    Outputs progress in real-time to the main Tkinter console widget.
    Must be called from a background thread so long-running uninstallers do not freeze the GUI.
    """
    root = log_widget.winfo_toplevel()

    def log(message):
        def append():
            log_widget.insert(tk.END, message + "\n")
            log_widget.see(tk.END)

        root.after(0, append)

    def show_success(had_errors):
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
    if cleanup_info["status"] == "leftover":
        log("Force cleanup mode: no Windows uninstaller found for this version.")
        if cleanup_info["leftovers"]:
            log("Detected leftover artifacts:")
            for leftover in cleanup_info["leftovers"]:
                log(f"  - {leftover}")
        log("Skipping Step 1 and proceeding with backup, folder purge, and registry cleanup.")

    # ==========================================
    # STEP 1: NATIVE WINDOWS APP UNINSTALLATION
    # ==========================================
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
            except Exception as e:
                log(f"Error removing {display_name}: {e}")
                had_errors = True
        log("Windows uninstall phase finished.")
    else:
        log("No Windows uninstall entries found. Moving to manual cleanup...")

    # ==========================================
    # STEP 2: RE-NAME & BACKUP CONFIG DIRECTORIES
    # ==========================================
    log("\nStep 2: Checking optional folders for backup...")
    user_profile = os.environ.get("USERPROFILE", "")  # Resolves to: C:\Users\Werner
    public_profile = os.environ.get("PUBLIC", r"C:\Users\Public")  # Resolves to: C:\Users\Public

    # Define all possible base document roots on the system
    base_docs_folders = [
        os.path.join(user_profile, "OneDrive", "Documents"),  # OneDrive path
        os.path.join(user_profile, "Documents"),  # Standard local path
    ]

    # Initialize a clean list to store all verified targets found across the paths
    backup_targets = []

    # Loop through our base paths and build the specific versioned folders to check
    for base_doc in base_docs_folders:
        # Check both the 2024 legacy name and the 2025+ name format for each base path
        backup_targets.append(os.path.join(base_doc, f"My Mastercam {version}"))
        backup_targets.append(os.path.join(base_doc, f"Mastercam {version}"))

    # Always include the Public Documents path as well
    backup_targets.append(os.path.join(public_profile, "Documents", f"Shared Mastercam {version}"))

    # Process every target path. If it exists in multiple directories, it will back up both.
    for target in backup_targets:
        if os.path.exists(target):
            backup_path = f"{target}_backup"

            # Collision Check: If a backup folder from a prior run is already there,
            # increment the name suffix sequentially so no data gets over-written.
            counter = 1
            while os.path.exists(backup_path):
                backup_path = f"{target}_backup_{counter}"
                counter += 1
            try:
                # os.rename alters the directory namespace instantaneously
                os.rename(target, backup_path)
                log(f"Backed up to: {backup_path}")
            except Exception as e:
                log(f"Failed to backup {target}: {e}")
                had_errors = True
        # We don't print "Folder not found" for every path to keep the log window clean,
        # since it's normal for half of these variants to not exist.

    # ==========================================
    # STEP 3: RESIDUAL PROGRAM FILES PURGE
    # ==========================================
    log("\nStep 3: Deleting Program Files directory...")
    prog_files = os.path.join(r"C:\Program Files", f"Mastercam {version}")
    if os.path.exists(prog_files):
        try:
            # shutil.rmtree deletes the folder along with all files and nested child trees inside it
            shutil.rmtree(prog_files)
            log(f"Deleted folder: {prog_files}")
        except Exception as e:
            log(f"Error deleting program files: {e}")
            had_errors = True
    else:
        log(f"Folder already clean: {prog_files}")

    # ==========================================
    # STEP 4: ORPHANED REGISTRY DEEP CLEAN
    # ==========================================
    log("\nStep 4: Cleaning registry entries...")
    reg_suffix = f"Software\\CNC Software\\Mastercam {version}"
    if not delete_registry_key(winreg.HKEY_CURRENT_USER, reg_suffix, log=log):
        had_errors = True
    if not delete_registry_key(winreg.HKEY_LOCAL_MACHINE, reg_suffix, log=log):
        had_errors = True

    log("\n--- Process Finished! ---")
    root.after(0, lambda: show_success(had_errors))


# ==========================================
# STEP 5: INTERFACE WINDOW SPAWNING LOGIC
# ==========================================
def show_readme_window():
    """
    Spawns a secondary, top-level independent window displaying the quick instructions.
    """
    readme_win = tk.Toplevel()
    readme_win.title("MC Assist - Quick Instructions")
    readme_win.geometry("520x420")
    set_app_icon(readme_win)

    text_area = tk.Text(readme_win, wrap=tk.WORD, font=("Consolas", 9))
    text_area.insert(tk.END, load_instructions_text())
    text_area.config(state=tk.DISABLED)
    text_area.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)


def launch_gui():
    """
    Builds and anchors the core primary GUI components for the utility tool.
    """
    root = tk.Tk()
    root.title("MC Assist V0.1")
    root.geometry("550x500")
    root.resizable(False, False)  # Freezes application aspect ratio dimensions
    set_app_icon(root)

    lbl_version = tk.Label(root, text="Select Mastercam Version to Uninstall:", font=("Arial", 11, "bold"))
    lbl_version.pack(pady=10)

    version_var = tk.StringVar()
    version_combo = ttk.Combobox(root, textvariable=version_var, state="readonly", font=("Arial", 10))
    version_combo.pack(pady=5)

    installed_versions = get_installed_versions()
    if installed_versions:
        version_combo["values"] = tuple(format_version_option(v) for v in installed_versions)
        version_combo.current(0)
    else:
        version_combo["values"] = ("No Mastercam installations detected",)
        version_combo.current(0)
        lbl_version.config(text="No installed Mastercam versions were detected:")

    log_text = tk.Text(root, height=15, width=60, font=("Consolas", 9))
    log_text.pack(pady=10)

    def refresh_version_list():
        refreshed_versions = get_installed_versions()
        if refreshed_versions:
            version_combo["values"] = tuple(format_version_option(v) for v in refreshed_versions)
            version_combo.current(0)
            lbl_version.config(text="Select Mastercam Version to Uninstall:")
        else:
            version_combo["values"] = ("No Mastercam installations detected",)
            version_combo.current(0)
            lbl_version.config(text="No installed Mastercam versions were detected:")

    def on_uninstall_click():
        selected_option = version_var.get()
        if selected_option == "No Mastercam installations detected":
            messagebox.showwarning("Nothing to Uninstall", "No installed Mastercam versions were detected on this machine.")
            return

        selected_version = parse_version_option(selected_option)
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

        if messagebox.askyesno("Confirm Action", confirm_message):
            btn_start.config(state=tk.DISABLED)

            def worker():
                try:
                    execute_uninstall(selected_version, log_text)
                finally:
                    root.after(0, lambda: (btn_start.config(state=tk.NORMAL), refresh_version_list()))

            threading.Thread(target=worker, daemon=True).start()

    # FIXED: Replaced standard padding parameter with tkinter native 'padx' and 'pady' arguments
    btn_start = tk.Button(root, text="Begin Clean Uninstall", command=on_uninstall_click, bg="#d9534f", fg="white",
                          font=("Arial", 10, "bold"), padx=5, pady=5)
    btn_start.pack(pady=5)

    btn_readme = tk.Button(root, text="View Readme / Instructions", command=show_readme_window, bg="#0275d8",
                           fg="white", font=("Arial", 9), padx=3, pady=3)
    btn_readme.pack(pady=5)

    # Structural loop thread that waits on events and keeps the desktop framework window interactive
    root.mainloop()


if __name__ == "__main__":
    # Assert administrative privileges straight at boot initialization
    run_as_admin()
    # If passed, display the control deck dashboard
    launch_gui()