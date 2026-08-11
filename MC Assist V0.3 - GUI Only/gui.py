import customtkinter
from tktooltip import ToolTip
from tkinter import filedialog

#CTK Var
text_color = "#ffffff"
main_color = "#99e0ff"
#8a12ff(dark purple) #b366ff(light purple) #c78fff (supper light purple)
#ff5901 (orange) #ff6919 (light orange)
#00ffae(snow)
#99e0ff (light blue)
#fff494 (light yello)
dropdown_button_color = "#00db96"
hover_color = "#3d3d3d" #3d3d3d (gray)  #a64dff purple
background_color = "#242424"
background_color_light = "#333333"
progressbar_var = 0.2 #temp


main_app = customtkinter.CTk()
main_app.title("MC Assist V0.2")
main_app.geometry("800x600")
main_app.resizable(False,False)  # Freezes application aspect ratio dimensions
main_app.configure(fg_color=background_color_light)
main_app.configure(bg_color=background_color)
#set_app_icon(main_app)


#Uninstall Settings Window
def start_uninstall_f():
    print("start_uninstall_f")

#Uninstall/Reinstall button
def start_install_f():
    print("start_reinstall_f")

#Show Left over files in a new window
def show_files_on_pc_window_f():
    print("show_files_on_pc_window_f")
    # Create the top-level window
    files_window = customtkinter.CTkToplevel(master=main_app)
    files_window.geometry("350x400")
    files_window.resizable(False, False)
    files_window.title("Left Over Files")
    customtkinter.set_appearance_mode("dark")

    # Lift it to the top so it doesn't hide behind the main window
    files_window.lift()

    # FORCE INTERACTION FOCUS TO THIS WINDOW ONLY
    files_window.focus_set()  # Grabs keyboard focus
    files_window.grab_set()

    def show_files_my_mc_f():
        print("show_files_my_mc_f")

    def show_files_shared_mc_f():
        print("show_files_shared_mc_f")

    def show_files_program_files_f():
        print("show_files_program_files_f")

    def show_files_registry_f():
        print("show_files_registry_f")

    # Exit Buttons------------------------------------------------
    show_files_cancel = customtkinter.CTkButton(files_window, text="X",command=files_window.destroy,
                                            fg_color="transparent",
                                            hover_color=hover_color, text_color="#c900b2", width=75, height=40,
                                            border_color="#c900b2", border_width=1)
    show_files_cancel.place(relx=0.835, rely=0.9, anchor="center")
    ToolTip(show_files_cancel, msg="Cancel", delay=0.5)

    #Left Over Files label----------------------------------------------
    show_files_files_on_pc = customtkinter.CTkLabel(files_window, text="Files On PC", fg_color="transparent",
                                                     text_color=main_color, font=("Arial", 20, "bold"))
    show_files_files_on_pc.place(relx=0.05, rely=0.1, anchor="w")

    #folder buttons------------------------------------------------
    show_files_my_mc = customtkinter.CTkButton(files_window, text="My Mastercam", command=show_files_my_mc_f,
                                               fg_color="transparent",
                                               hover_color=hover_color, text_color=main_color, width=200, height=28,
                                               border_color=main_color, border_width=1)
    show_files_my_mc.place(relx=0.5, rely=0.25, anchor="center")
    ToolTip(show_files_my_mc, msg="Show Files Location", delay=0.5)

    show_files_shared_mc = customtkinter.CTkButton(files_window, text="Shared Mastercam", command=show_files_shared_mc_f,
                                               fg_color="transparent",
                                               hover_color=hover_color, text_color=main_color, width=200, height=28,
                                               border_color=main_color, border_width=1)
    show_files_shared_mc.place(relx=0.5, rely=0.35, anchor="center")
    ToolTip(show_files_shared_mc, msg="Show Files Location", delay=0.5)

    show_files_program_files = customtkinter.CTkButton(files_window, text="Program Files", command=show_files_program_files_f,
                                               fg_color="transparent",
                                               hover_color=hover_color, text_color=main_color, width=200, height=28,
                                               border_color=main_color, border_width=1)
    show_files_program_files.place(relx=0.5, rely=0.45, anchor="center")
    ToolTip(show_files_program_files, msg="Show Files Location", delay=0.5)

    show_files_registry = customtkinter.CTkButton(files_window, text="Registry", command=show_files_registry_f,
                                               fg_color="transparent",
                                               hover_color=hover_color, text_color=main_color, width=200, height=28,
                                               border_color=main_color, border_width=1)
    show_files_registry.place(relx=0.5, rely=0.55, anchor="center")
    ToolTip(show_files_registry, msg="Open Registry Editor", delay=0.5)

#Select mastercam Version on pc
def dropdown_callback_f(choice):
    print(f"dropdown_callback_f: {choice}")
    if choice == "Select MC Version...":
        #install_enable.configure(state="disabled", border_color=background_color_light, border_width=2)
        uninstall_enable.configure(state="disabled", border_color=background_color_light, border_width=2)
        start_uninstall.configure(state="disabled", border_color=background_color_light, border_width=2)
        start_install.configure(state="disabled", border_color=background_color_light, border_width=2)

        uninstall_select_all.configure(state="disabled", border_color=background_color_light, border_width=2,fg_color=background_color_light)
        uninstall_mc.configure(state="disabled", border_color=background_color_light, border_width=2,fg_color=background_color_light)
        uninstall_my_backup.configure(state="disabled", border_color=background_color_light, border_width=2,fg_color=background_color_light)
        uninstall_shared_backup.configure(state="disabled", border_color=background_color_light, border_width=2,fg_color=background_color_light)
        uninstall_program_files_delete.configure(state="disabled", border_color=background_color_light, border_width=2,fg_color=background_color_light)
        uninstall_registry_delete.configure(state="disabled", border_color=background_color_light, border_width=2,fg_color=background_color_light)

        install_language_select.configure(state="disabled", selected_color=background_color_light)
        install_unit_select.configure(state="disabled", selected_color=background_color_light)
        install_users_select.configure(state="disabled", selected_color=background_color_light)
        install_license.configure(state="disabled", border_color=background_color_light, border_width=2,fg_color=background_color_light)
        install_restore_backup.configure(state="disabled", border_color=background_color_light, border_width=2,fg_color=background_color_light)
        install_select_install_file.configure(state="disabled", border_color=background_color_light, border_width=2)
        install_select_language_file.configure(state="disabled", border_color=background_color_light, border_width=2)
        install_file_entry_language.configure(state="disabled", border_color=background_color_light, border_width=2)
        install_file_entry_install.configure(state="disabled", border_color=background_color_light, border_width=2)

        show_files_on_pc_window.configure(state="disabled", border_color=background_color_light, border_width=2)
    else:
        install_enable.configure(state="normal", border_color=main_color, border_width=1)
        uninstall_enable.configure(state="normal", border_color=main_color, border_width=1)
        show_files_on_pc_window.configure(state="normal", border_color=main_color, border_width=1)



# Callback Uninstall
def uninstall_enable_f():
    print("uninstall_enable_f:", uninstall_enable.get())
    if uninstall_enable.get() == "off":
        start_uninstall.configure(state="disabled",border_color=background_color_light, border_width=2)

        uninstall_select_all.configure(state="disabled", border_color=background_color_light, border_width=2, fg_color=background_color_light)
        uninstall_mc.configure(state="disabled", border_color=background_color_light, border_width=2,fg_color=background_color_light)
        uninstall_my_backup.configure(state="disabled", border_color=background_color_light, border_width=2,fg_color=background_color_light)
        uninstall_shared_backup.configure(state="disabled", border_color=background_color_light, border_width=2,fg_color=background_color_light)
        uninstall_program_files_delete.configure(state="disabled", border_color=background_color_light, border_width=2,fg_color=background_color_light)
        uninstall_registry_delete.configure(state="disabled", border_color=background_color_light, border_width=2,fg_color=background_color_light)
    else:
        start_uninstall.configure(state="normal", border_color=main_color, border_width=1)

        uninstall_select_all.configure(state="normal", border_color=main_color, border_width=1, fg_color=main_color)
        uninstall_mc.configure(state="normal", border_color=main_color, border_width=1, fg_color=main_color)
        uninstall_my_backup.configure(state="normal", border_color=main_color, border_width=1, fg_color=main_color)
        uninstall_shared_backup.configure(state="normal", border_color=main_color, border_width=1, fg_color=main_color)
        uninstall_program_files_delete.configure(state="normal", border_color=main_color, border_width=1, fg_color=main_color)
        uninstall_registry_delete.configure(state="normal", border_color=main_color, border_width=1, fg_color=main_color)

    if uninstall_enable.get() == "on" and install_enable.get() == "on":
        start_install.configure(text="Uninstall/Install")
        start_uninstall.configure(state="disabled", border_color=background_color_light, border_width=2)
    else:
        start_install.configure(text="Install")


def uninstall_select_all_f():
    print("uninstall_select_all_f:", uninstall_select_all.get())
    # Check what state the "Select All" master variable is currently in
    if uninstall_select_all_var.get() == "on":
        # If master is checked, force select ALL sub-checkboxes
        uninstall_mc.select()
        uninstall_my_backup.select()
        uninstall_shared_backup.select()
        uninstall_program_files_delete.select()
        uninstall_registry_delete.select()
    else:
        # If master is unchecked, force deselect ALL sub-checkboxes
        uninstall_mc.deselect()
        uninstall_my_backup.deselect()
        uninstall_shared_backup.deselect()
        uninstall_program_files_delete.deselect()
        uninstall_registry_delete.deselect()

def uninstall_mc_f():
    print("uninstall_mc_f:", uninstall_mc.get())

    """Unchecks 'Select All' if the user manually unchecks any single option."""
    # List of all your sub-variables
    all_checked = (
            uninstall_mc_var.get() == "on" and
            uninstall_my_backup_var.get() == "on" and
            uninstall_shared_backup_var.get() == "on" and
            uninstall_program_files_delete_var.get() == "on" and
            uninstall_registry_delete.get() == "on"
    )

    if all_checked:
        uninstall_select_all.select()
    else:
        # If even one item is manually unchecked, turn off the "Select All" checkmark
        uninstall_select_all.deselect()

def uninstall_my_backup_f():
    print("uninstall_my_backup_f:", uninstall_my_backup.get())

    """Unchecks 'Select All' if the user manually unchecks any single option."""
    # List of all your sub-variables
    all_checked = (
            uninstall_mc_var.get() == "on" and
            uninstall_my_backup_var.get() == "on" and
            uninstall_shared_backup_var.get() == "on" and
            uninstall_program_files_delete_var.get() == "on" and
            uninstall_registry_delete.get() == "on"
    )

    if all_checked:
        uninstall_select_all.select()
    else:
        # If even one item is manually unchecked, turn off the "Select All" checkmark
        uninstall_select_all.deselect()

def uninstall_shared_backup_f():
    print("uninstall_shared_backup_f:", uninstall_shared_backup.get())

    """Unchecks 'Select All' if the user manually unchecks any single option."""
    # List of all your sub-variables
    all_checked = (
            uninstall_mc_var.get() == "on" and
            uninstall_my_backup_var.get() == "on" and
            uninstall_shared_backup_var.get() == "on" and
            uninstall_program_files_delete_var.get() == "on" and
            uninstall_registry_delete.get() == "on"
    )

    if all_checked:
        uninstall_select_all.select()
    else:
        # If even one item is manually unchecked, turn off the "Select All" checkmark
        uninstall_select_all.deselect()

def uninstall_program_files_delete_f():
    print("uninstall_program_files_delete_f:", uninstall_program_files_delete.get())

    """Unchecks 'Select All' if the user manually unchecks any single option."""
    # List of all your sub-variables
    all_checked = (
            uninstall_mc_var.get() == "on" and
            uninstall_my_backup_var.get() == "on" and
            uninstall_shared_backup_var.get() == "on" and
            uninstall_program_files_delete_var.get() == "on" and
            uninstall_registry_delete.get() == "on"
    )

    if all_checked:
        uninstall_select_all.select()
    else:
        # If even one item is manually unchecked, turn off the "Select All" checkmark
        uninstall_select_all.deselect()

def uninstall_registry_delete_f():
    print("uninstall_registry_delete_f:", uninstall_registry_delete.get())

    """Unchecks 'Select All' if the user manually unchecks any single option."""
    # List of all your sub-variables
    all_checked = (
            uninstall_mc_var.get() == "on" and
            uninstall_my_backup_var.get() == "on" and
            uninstall_shared_backup_var.get() == "on" and
            uninstall_program_files_delete_var.get() == "on" and
            uninstall_registry_delete.get() == "on"
    )

    if all_checked:
        uninstall_select_all.select()
    else:
        # If even one item is manually unchecked, turn off the "Select All" checkmark
        uninstall_select_all.deselect()

# Callback Install
def install_enable_f():
    print("install_enable_f:", install_enable.get())
    if install_enable.get() == "off":
        start_install.configure(state="disabled",border_color=background_color_light, border_width=2)

        install_language_select.configure(state="disabled",selected_color=background_color_light)
        install_unit_select.configure(state="disabled", selected_color=background_color_light)
        install_users_select.configure(state="disabled", selected_color=background_color_light)
        install_license.configure(state="disabled", border_color=background_color_light, border_width=2,fg_color=background_color_light)
        install_restore_backup.configure(state="disabled", border_color=background_color_light, border_width=2,fg_color=background_color_light)
        install_select_install_file.configure(state="disabled", border_color=background_color_light, border_width=2)
        install_select_language_file.configure(state="disabled", border_color=background_color_light, border_width=2)
        install_file_entry_language.configure(state="disabled", border_color=background_color_light, border_width=2)
        install_file_entry_install.configure(state="disabled", border_color=background_color_light, border_width=2)
    else:
        start_install.configure(state="normal", border_color=main_color, border_width=1)

        install_language_select.configure(state="normal", selected_color=main_color)
        install_unit_select.configure(state="normal", selected_color=main_color)
        install_users_select.configure(state="normal", selected_color=main_color)
        install_license.configure(state="normal", border_color=main_color, border_width=1,fg_color=main_color)
        install_restore_backup.configure(state="normal", border_color=main_color, border_width=1, fg_color=main_color)
        install_select_install_file.configure(state="normal", border_color=main_color, border_width=1)
        install_select_language_file.configure(state="normal", border_color=main_color, border_width=1)
        install_file_entry_language.configure(state="normal", border_color=main_color, border_width=1)
        install_file_entry_install.configure(state="normal", border_color=main_color, border_width=1)



    if uninstall_enable.get() == "on" and install_enable.get() == "on":
        start_install.configure(text="Uninstall/Install")
        start_uninstall.configure(state="disabled", border_color=background_color_light, border_width=2)
    else:
        start_install.configure(text="Install")
        if uninstall_enable.get() == "on":
            start_uninstall.configure(state="normal", border_color=main_color, border_width=1)
        else:
            start_uninstall.configure(state="disabled", border_color=background_color_light, border_width=2)


def install_language_select_f(values):
    print(f"install_language_select_f: {values}")

    # if values == "English":
    #     print("Loading English language translation profiles...")
    #     # Add your English text changes here
    # elif values == "Other":
    #     print("Loading alternative language translation profiles...")
    #     # Add your alternative text changes here

def install_unit_select_f(values):
    print(f"install_unit_select_f: {values}")

def install_users_select_f(values):
    print(f"install_users_select_f: {values}")

def install_license_f():
    print("install_license_f")

def install_restore_backup_f():
    print("install_restore_backup_f")

def install_select_install_file_f():
    print("install_select_install_file_f")
    # Opens the OS file picker dialog
    file_path = filedialog.askopenfilename(
        title="Select Mastercam File",
        # Optional: restrict types (e.g., all files, executables, text)
        filetypes=[("All Files", "*.*"), ("Executables", "*.exe")]
    )

    # If the user selected a file (didn't click cancel)
    if file_path:
        # Clear the old path text inside the input entry field
        install_file_entry_install.delete(0, "end")
        # Insert the newly selected file path text string
        install_file_entry_install.insert(0, file_path)

def install_select_language_file_f():
    print("install_select_language_file_f")
    # Opens the OS file picker dialog
    file_path = filedialog.askopenfilename(
        title="Select Language File",
        # Optional: restrict types (e.g., all files, executables, text)
        filetypes=[("All Files", "*.*"), ("Executables", "*.exe")]
    )

    # If the user selected a file (didn't click cancel)
    if file_path:
        # Clear the old path text inside the input entry field
        install_file_entry_language.delete(0, "end")
        # Insert the newly selected file path text string
        install_file_entry_language.insert(0, file_path)

# region -- Background features --------------

#Ribbon Bar
ribbon_bar = customtkinter.CTkFrame(master=main_app, width=776, height=70, corner_radius=0,fg_color=background_color)
ribbon_bar.place(relx=0.5, rely=0.012, anchor="n")

#Uninstall box
uninstall_box = customtkinter.CTkFrame(master=main_app, width=380, height=320, corner_radius=0, fg_color=background_color)
uninstall_box.place(relx=0.49, rely=0.14, anchor="ne")

#Install box
install_box = customtkinter.CTkFrame(master=main_app, width=380, height=320, corner_radius=0, fg_color=background_color)
install_box.place(relx=0.51, rely=0.14, anchor="nw")

#progress box
progress_box = customtkinter.CTkFrame(master=main_app, width=776, height=181, corner_radius=0,fg_color=background_color)
progress_box.place(relx=0.5, rely=0.988, anchor="s")

# endregion

###Uninstall functions-------------------------------------------------------

# region -- uninstall_enable------------------------------------------------
uninstall_enable_var = customtkinter.StringVar(value="off")
uninstall_enable = customtkinter.CTkCheckBox(main_app, text="", command=uninstall_enable_f,
                                      variable=uninstall_enable_var, onvalue="on", offvalue="off", hover_color=hover_color,
                                      checkbox_width=20, checkbox_height=20, checkmark_color=background_color,
                                      corner_radius=0, border_width=1, fg_color=main_color, border_color=main_color, bg_color=background_color, width=20)
uninstall_enable.place(relx=0.45, rely=0.175, anchor="w")

# endregion

# region --Uninstall Label----------------------------------
uninstall_reinstall_uninstall_options = customtkinter.CTkLabel(main_app, text="Uninstall Options", fg_color="transparent",
                                                 text_color=main_color, font=("Arial", 20, "bold"), bg_color=background_color)
uninstall_reinstall_uninstall_options.place(relx=0.05, rely=0.17, anchor="w")
# endregion

# region -- Uninstall Check Boxes-----------------------
# Uninstall Check Boxes----------------------------------

uninstall_select_all_var = customtkinter.StringVar(value="on")
uninstall_select_all = customtkinter.CTkCheckBox(main_app, text="Select All", command=uninstall_select_all_f,
                                      variable=uninstall_select_all_var, onvalue="on", offvalue="off", hover_color=hover_color,
                                      checkbox_width=20, checkbox_height=20, checkmark_color=background_color,
                                      corner_radius=0, border_width=1, fg_color=main_color, border_color=main_color, bg_color=background_color)
uninstall_select_all.place(relx=0.05, rely=0.23, anchor="w")

uninstall_mc_var = customtkinter.StringVar(value="on")
uninstall_mc = customtkinter.CTkCheckBox(main_app, text="Uninstall Mastercam",
                                               command=uninstall_mc_f,
                                               variable=uninstall_mc_var, onvalue="on", offvalue="off",
                                               hover_color=hover_color,
                                               checkbox_width=20, checkbox_height=20,
                                               checkmark_color=background_color,
                                               corner_radius=0, border_width=1, fg_color=main_color,
                                               border_color=main_color,bg_color=background_color)
uninstall_mc.place(relx=0.1, rely=0.28, anchor="w")

uninstall_my_backup_var = customtkinter.StringVar(value="on")
uninstall_my_backup = customtkinter.CTkCheckBox(main_app, text="Backup My Mastercam Folder",
                                            command=uninstall_my_backup_f,
                                            variable=uninstall_my_backup_var, onvalue="on", offvalue="off",
                                            hover_color=hover_color,
                                            checkbox_width=20, checkbox_height=20, checkmark_color=background_color,
                                            corner_radius=0, border_width=1, fg_color=main_color,
                                            border_color=main_color, bg_color=background_color)
uninstall_my_backup.place(relx=0.1, rely=0.36, anchor="w")

uninstall_shared_backup_var = customtkinter.StringVar(value="on")
uninstall_shared_backup = customtkinter.CTkCheckBox(main_app, text="Backup Shared Mastercam Folder",
                                                command=uninstall_shared_backup_f,
                                                variable=uninstall_shared_backup_var, onvalue="on", offvalue="off",
                                                hover_color=hover_color,
                                                checkbox_width=20, checkbox_height=20,
                                                checkmark_color=background_color,
                                                corner_radius=0, border_width=1, fg_color=main_color,
                                                border_color=main_color, bg_color=background_color)
uninstall_shared_backup.place(relx=0.1, rely=0.44, anchor="w")

uninstall_program_files_delete_var = customtkinter.StringVar(value="on")
uninstall_program_files_delete = customtkinter.CTkCheckBox(main_app, text="Delete Program Files",
                                                       command=uninstall_program_files_delete_f,
                                                       variable=uninstall_program_files_delete_var, onvalue="on",
                                                       offvalue="off", hover_color=hover_color,
                                                       checkbox_width=20, checkbox_height=20,
                                                       checkmark_color=background_color,
                                                       corner_radius=0, border_width=1, fg_color=main_color,
                                                       border_color=main_color, bg_color=background_color)
uninstall_program_files_delete.place(relx=0.1, rely=0.52, anchor="w")

uninstall_registry_delete_var = customtkinter.StringVar(value="on")
uninstall_registry_delete = customtkinter.CTkCheckBox(main_app, text="Delete Registries",
                                                  command=uninstall_registry_delete_f,
                                                  variable=uninstall_registry_delete_var, onvalue="on", offvalue="off",
                                                  hover_color=hover_color,
                                                  checkbox_width=20, checkbox_height=20,
                                                  checkmark_color=background_color,
                                                  corner_radius=0, border_width=1, fg_color=main_color,
                                                  border_color=main_color, bg_color=background_color)
uninstall_registry_delete.place(relx=0.1, rely=0.60, anchor="w")

#endregion


###Install functions-------------------------------------------------------

# region -- install_enable-----------------------------------------------

install_enable_var = customtkinter.StringVar(value="off")
install_enable = customtkinter.CTkCheckBox(main_app, text="", command=install_enable_f,
                                      variable=install_enable_var, onvalue="on", offvalue="off", hover_color=hover_color,
                                      checkbox_width=20, checkbox_height=20, checkmark_color=background_color,
                                      corner_radius=0, border_width=1, fg_color=main_color, border_color=main_color, bg_color=background_color, width=20)
install_enable.place(relx=0.945, rely=0.175, anchor="w")

# endregion

# region -- Install Label-------------------------------------------------
# Install options Label------------------------------------
label_install_options = customtkinter.CTkLabel(main_app, text="Install Options", fg_color="transparent",
                                               text_color=main_color, font=("Arial", 20, "bold"), bg_color=background_color)
label_install_options.place(relx=0.55, rely=0.17, anchor="w")
# endregion

# region-- Segmente button----------------------------------
install_language_select = customtkinter.CTkSegmentedButton(main_app, values=["English", "Other"],
                                                     command=install_language_select_f, fg_color=background_color,
                                                    selected_color=main_color, unselected_color=background_color,
                                                    selected_hover_color=main_color, unselected_hover_color=hover_color,
                                                    text_color=text_color, bg_color=background_color)
install_language_select.set("English")
install_language_select.place(relx=0.55, rely=0.23, anchor="w")


install_unit_select = customtkinter.CTkSegmentedButton(main_app, values=["Metric", "U.S."],
                                                     command=install_unit_select_f, fg_color=background_color,
                                                    selected_color=main_color, unselected_color=background_color,
                                                    selected_hover_color=main_color, unselected_hover_color=hover_color,
                                                    text_color=text_color, bg_color=background_color)
install_unit_select.set("Metric")
install_unit_select.place(relx=0.55, rely=0.3, anchor="w")

install_users_select = customtkinter.CTkSegmentedButton(main_app, values=["All Users", "Only For Me"],
                                                     command=install_users_select_f, fg_color=background_color,
                                                    selected_color=main_color, unselected_color=background_color,
                                                    selected_hover_color=main_color, unselected_hover_color=hover_color,
                                                    text_color=text_color, bg_color=background_color)
install_users_select.set("All Users")
install_users_select.place(relx=0.55, rely=0.37, anchor="w")

# endregion

# region -- Install Check Boxes----------------------------------

install_license_var = customtkinter.StringVar(value="off")
install_license = customtkinter.CTkCheckBox(main_app, text="Yes, I accept the terms of the license agreement",
                                                       command=install_license_f,
                                                       variable=install_license_var, onvalue="on",
                                                       offvalue="off", hover_color=hover_color,
                                                       checkbox_width=20, checkbox_height=20,
                                                       checkmark_color=background_color,
                                                       corner_radius=0, border_width=1, fg_color=main_color,
                                                       border_color=main_color, bg_color=background_color)
install_license.place(relx=0.55, rely=0.44, anchor="w")

install_restore_backup_var = customtkinter.StringVar(value="on")
install_restore_backup = customtkinter.CTkCheckBox(main_app, text="Restore Backups",
                                                       command=install_restore_backup_f,
                                                       variable=install_restore_backup_var, onvalue="on",
                                                       offvalue="off", hover_color=hover_color,
                                                       checkbox_width=20, checkbox_height=20,
                                                       checkmark_color=background_color,
                                                       corner_radius=0, border_width=1, fg_color=main_color,
                                                       border_color=main_color, bg_color=background_color)
install_restore_backup.place(relx=0.55, rely=0.51, anchor="w")

# endregion

# region -- file select install
install_file_entry_install = customtkinter.CTkEntry(main_app,width=250,placeholder_text="Select MC Install File...",border_color=main_color, border_width=1, bg_color=background_color)
install_file_entry_install.place(relx=0.77, rely=0.6, anchor="center")

install_select_install_file = customtkinter.CTkButton(main_app, text="O",
                                                           command=install_select_install_file_f,
                                                           fg_color="transparent",
                                                           hover_color=hover_color, text_color=main_color, width=28,
                                                           height=28,
                                                           border_color=main_color, border_width=1, bg_color=background_color)
install_select_install_file.place(relx=0.57, rely=0.6, anchor="center")

# endregion

# region -- file select language ------install------------------------
install_file_entry_language = customtkinter.CTkEntry(main_app,width=150,placeholder_text="Select Language File...",border_color=main_color, border_width=1, bg_color=background_color)
install_file_entry_language.place(relx=0.73, rely=0.23, anchor="w")

install_select_language_file = customtkinter.CTkButton(main_app, text="O",
                                                           command=install_select_language_file_f,
                                                           fg_color="transparent",
                                                           hover_color=hover_color, text_color=main_color, width=28,
                                                           height=28,
                                                           border_color=main_color, border_width=1, bg_color=background_color)
install_select_language_file.place(relx=0.70, rely=0.23, anchor="center")

# endregion

###Main window

# region -- Dropdown----------------------------------------------------

# Predefined list of options
dropdown_options = ["Mastercam (version1)", "Mastercam (version2)", "Mastercam (version3)"]

# Create the OptionMenu widget
dropdown = customtkinter.CTkOptionMenu(main_app,values=dropdown_options,fg_color=hover_color,button_color=main_color,
                                       button_hover_color=hover_color,width=200,height=28 ,command=dropdown_callback_f, bg_color=background_color)
dropdown.set("Select MC Version...")
dropdown.place(relx=0.15, rely=0.07, anchor="center")





# endregion

# region -- Buttons Uninstall and Reinstall-----------------------------
start_uninstall = customtkinter.CTkButton(main_app, text="Uninstall", command=lambda: start_uninstall_f(),
                                                fg_color="transparent",
                                                hover_color=hover_color, text_color=text_color, width=125, height=28,
                                                border_color=main_color, border_width=1, bg_color=background_color)
start_uninstall.place(relx=0.45, rely=0.07, anchor="center")

start_install = customtkinter.CTkButton(main_app, text="Install",
                                                command=lambda: start_install_f(), fg_color="transparent",
                                                hover_color=hover_color, text_color=text_color, width=125, height=28,
                                                border_color=main_color, border_width=1, bg_color=background_color)
start_install.place(relx=0.64, rely=0.07, anchor="center")
# endregion

# region -- Show files Button------------------------------------------
show_files_on_pc_window = customtkinter.CTkButton(main_app, text="FOP", command=lambda: show_files_on_pc_window_f(),
                                                 fg_color="transparent",
                                                 hover_color=hover_color, text_color=text_color, width=28, height=28,
                                                 border_color=main_color, border_width=1, bg_color=background_color)
show_files_on_pc_window.place(relx=0.32, rely=0.07, anchor="center")
ToolTip(show_files_on_pc_window, msg="Files On PC", delay=0.5)
# endregion

# region -- Progressbar----------------------------------------------
label = customtkinter.CTkLabel(main_app, text="Progress  label", fg_color="transparent", text_color=text_color, bg_color=background_color)
label.place(relx=0.25, rely=0.73, anchor="w")

progressbar = customtkinter.CTkProgressBar(main_app, orientation="horizontal", width=400, height=12, corner_radius=0,
                                           progress_color=main_color)
progressbar.set(progressbar_var)
progressbar.place(relx=0.5, rely=0.78, anchor="center")
# endregion

# region -- #Unistall Process----------------------------------------
label_uninstall = customtkinter.CTkLabel(main_app, text="label_uninstall", fg_color="transparent",
                                         text_color=text_color, bg_color=background_color)
label_uninstall.place(relx=0.06, rely=0.83, anchor="w")

button_uninstall_process = customtkinter.CTkButton(main_app, text="", fg_color="transparent", hover_color=hover_color,
                                                   width=16 * 3, height=16, corner_radius=8,
                                                   border_color=main_color, border_width=1, state="disabled")
button_uninstall_process.place(relx=0.09, rely=0.88, anchor="center")
ToolTip(button_uninstall_process, msg="Mastercam Uninstall", delay=0.0)

button_my_mastercam_backup = customtkinter.CTkButton(main_app, text="", fg_color="transparent", hover_color=hover_color,
                                                     width=16 * 3, height=16, corner_radius=8,
                                                     border_color=main_color, border_width=1, state="disabled")
button_my_mastercam_backup.place(relx=0.17, rely=0.88, anchor="center")
ToolTip(button_my_mastercam_backup, msg="My Mastercam Backup", delay=0.0)

button_shared_mastercam_backup = customtkinter.CTkButton(main_app, text="", fg_color="transparent",
                                                         hover_color=hover_color, width=16 * 3, height=16,
                                                         corner_radius=8,
                                                         border_color=main_color, border_width=1, state="disabled")
button_shared_mastercam_backup.place(relx=0.25, rely=0.88, anchor="center")
ToolTip(button_shared_mastercam_backup, msg="Shared Mastercam Backup", delay=0.0)

button_program_files_delete = customtkinter.CTkButton(main_app, text="", fg_color="transparent",
                                                      hover_color=hover_color, width=16 * 3, height=16, corner_radius=8,
                                                      border_color=main_color, border_width=1, state="disabled")
button_program_files_delete.place(relx=0.33, rely=0.88, anchor="center")
ToolTip(button_program_files_delete, msg="Program Files Delete", delay=0.0)

button_registry_delete = customtkinter.CTkButton(main_app, text="", fg_color="transparent", hover_color=hover_color,
                                                 width=16 * 3, height=16, corner_radius=8,
                                                 border_color=main_color, border_width=1, state="disabled")
button_registry_delete.place(relx=0.41, rely=0.88, anchor="center")
ToolTip(button_registry_delete, msg="Registry Delete", delay=0.0)

# endregion

# region -- Reinstall Process buttons---------------------------------
# Run Executable
# Yes to run exe
# Press top button (Masercam install)
# Select language
# Select units and users (All users or only for Me)
# License agreement
# Install

label_reinstall = customtkinter.CTkLabel(main_app, text="label_reinstall", fg_color="transparent",
                                         text_color=text_color, bg_color=background_color)
label_reinstall.place(relx=0.55, rely=0.83, anchor="w")

# Language Selected
button_language = customtkinter.CTkButton(main_app, text="", fg_color="transparent", hover_color=hover_color,
                                          width=16 * 3, height=16, corner_radius=8,
                                          border_color=main_color, border_width=1, state="disabled")
button_language.place(relx=0.58, rely=0.88, anchor="center")
ToolTip(button_language, msg="Language Select (english)", delay=0.0)

# Units Selected
button_units = customtkinter.CTkButton(main_app, text="", fg_color="transparent", hover_color=hover_color, width=16 * 3,
                                       height=16, corner_radius=8,
                                       border_color=main_color, border_width=1, state="disabled")
button_units.place(relx=0.66, rely=0.88, anchor="center")
ToolTip(button_units, msg="Units Select", delay=0.0)

# users Selected
button_users = customtkinter.CTkButton(main_app, text="", fg_color="transparent", hover_color=hover_color, width=16 * 3,
                                       height=16, corner_radius=8,
                                       border_color=main_color, border_width=1, state="disabled")
button_users.place(relx=0.74, rely=0.88, anchor="center")
ToolTip(button_users, msg="Users Select", delay=0.0)

# License agreement
button_license = customtkinter.CTkButton(main_app, text="", fg_color="transparent", hover_color=hover_color,
                                         width=16 * 3, height=16, corner_radius=8,
                                         border_color=main_color, border_width=1, state="disabled")
button_license.place(relx=0.82, rely=0.88, anchor="center")
ToolTip(button_license, msg="License agreement", delay=0.0)

# Restore Backup
button_restore_backup = customtkinter.CTkButton(main_app, text="", fg_color="transparent", hover_color=hover_color,
                                                width=16 * 3, height=16, corner_radius=8,
                                                border_color=main_color, border_width=1, state="disabled")
button_restore_backup.place(relx=0.90, rely=0.88, anchor="center")
ToolTip(button_restore_backup, msg="Restore Backup", delay=0.0)
# endregion

dropdown_callback_f(dropdown.get())

main_app.mainloop()
