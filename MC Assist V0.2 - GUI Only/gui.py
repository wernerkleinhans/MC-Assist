import customtkinter
from tktooltip import ToolTip
from tkinter import filedialog

#CTK Var
text_color = "#ffffff"
main_color = "#00ffae"    #8a12ff(dark purple) #b366ff(light purple) #ff5901 (orange) #ff6919 (light orange) #00ffae(snow)
dropdown_button_color = "#00db96"
hover_color = "#3d3d3d" #3d3d3d (gray)  #a64dff purple
background_color = "#242424"
progressbar_var = 0.2 #temp


main_app = customtkinter.CTk()
main_app.title("MC Assist V0.2")
main_app.geometry("600x500")
main_app.resizable(False,False)  # Freezes application aspect ratio dimensions
#set_app_icon(main_app)


#Uninstall Settings Window
def open_uninstall_settings_f(main_app):
    print("open_uninstall_settings_f")
    #Create the top-level window
    uninstall_window = customtkinter.CTkToplevel(master=main_app)
    uninstall_window.geometry("350x400")
    uninstall_window.resizable(False,False)
    uninstall_window.title("Uninstall settings")
    customtkinter.set_appearance_mode("dark")


    #Lift it to the top so it doesn't hide behind the main window
    uninstall_window.lift()

    #FORCE INTERACTION FOCUS TO THIS WINDOW ONLY
    uninstall_window.focus_set()  # Grabs keyboard focus
    uninstall_window.grab_set()

    #Callback
    def start_uninstall_f():
        print("start_uninstall_f")

    def uninstall_select_all_f():
        print("uninstall_select_all_f:", uninstall_select_all.get())
        # Check what state the "Select All" master variable is currently in
        if uninstall_select_all_var.get() == "on":
            # If master is checked, force select ALL sub-checkboxes
            uninstall_select_mc.select()
            uninstall_select_my_backup.select()
            uninstall_select_shared_backup.select()
            uninstall_select_program_files_delete.select()
            uninstall_select_registry_delete.select()
        else:
            # If master is unchecked, force deselect ALL sub-checkboxes
            uninstall_select_mc.deselect()
            uninstall_select_my_backup.deselect()
            uninstall_select_shared_backup.deselect()
            uninstall_select_program_files_delete.deselect()
            uninstall_select_registry_delete.deselect()

    def uninstall_select_mc_f():
        print("uninstall_select_mc_f:", uninstall_select_mc.get())

        """Unchecks 'Select All' if the user manually unchecks any single option."""
        # List of all your sub-variables
        all_checked = (
                uninstall_select_mc_var.get() == "on" and
                uninstall_select_my_backup_var.get() == "on" and
                uninstall_select_shared_backup_var.get() == "on" and
                uninstall_select_program_files_delete_var.get() == "on" and
                uninstall_select_registry_delete_var.get() == "on"
        )

        if all_checked:
            uninstall_select_all.select()
        else:
            # If even one item is manually unchecked, turn off the "Select All" checkmark
            uninstall_select_all.deselect()
    def uninstall_select_my_backup_f():
        print("uninstall_select_my_backup_f:", uninstall_select_my_backup.get())

        """Unchecks 'Select All' if the user manually unchecks any single option."""
        # List of all your sub-variables
        all_checked = (
                uninstall_select_mc_var.get() == "on" and
                uninstall_select_my_backup_var.get() == "on" and
                uninstall_select_shared_backup_var.get() == "on" and
                uninstall_select_program_files_delete_var.get() == "on" and
                uninstall_select_registry_delete_var.get() == "on"
        )

        if all_checked:
            uninstall_select_all.select()
        else:
            # If even one item is manually unchecked, turn off the "Select All" checkmark
            uninstall_select_all.deselect()
    def uninstall_select_shared_backup_f():
        print("uninstall_select_shared_backup_f:",uninstall_select_shared_backup.get())

        """Unchecks 'Select All' if the user manually unchecks any single option."""
        # List of all your sub-variables
        all_checked = (
                uninstall_select_mc_var.get() == "on" and
                uninstall_select_my_backup_var.get() == "on" and
                uninstall_select_shared_backup_var.get() == "on" and
                uninstall_select_program_files_delete_var.get() == "on" and
                uninstall_select_registry_delete_var.get() == "on"
        )

        if all_checked:
            uninstall_select_all.select()
        else:
            # If even one item is manually unchecked, turn off the "Select All" checkmark
            uninstall_select_all.deselect()
    def uninstall_select_program_files_delete_f():
        print("uninstall_select_program_files_delete_f:", uninstall_select_program_files_delete.get())

        """Unchecks 'Select All' if the user manually unchecks any single option."""
        # List of all your sub-variables
        all_checked = (
                uninstall_select_mc_var.get() == "on" and
                uninstall_select_my_backup_var.get() == "on" and
                uninstall_select_shared_backup_var.get() == "on" and
                uninstall_select_program_files_delete_var.get() == "on" and
                uninstall_select_registry_delete_var.get() == "on"
        )

        if all_checked:
            uninstall_select_all.select()
        else:
            # If even one item is manually unchecked, turn off the "Select All" checkmark
            uninstall_select_all.deselect()
    def uninstall_select_registry_delete_f():
        print("uninstall_select_registry_delete_f:", uninstall_select_registry_delete.get())

        """Unchecks 'Select All' if the user manually unchecks any single option."""
        # List of all your sub-variables
        all_checked = (
                uninstall_select_mc_var.get() == "on" and
                uninstall_select_my_backup_var.get() == "on" and
                uninstall_select_shared_backup_var.get() == "on" and
                uninstall_select_program_files_delete_var.get() == "on" and
                uninstall_select_registry_delete_var.get() == "on"
        )

        if all_checked:
            uninstall_select_all.select()
        else:
            # If even one item is manually unchecked, turn off the "Select All" checkmark
            uninstall_select_all.deselect()


    #Exit Buttons------------------------------------------------
    start_uninstall = customtkinter.CTkButton(uninstall_window, text="O", command=start_uninstall_f,
                                               fg_color="transparent",
                                               hover_color=hover_color, text_color=main_color, width=75, height=40,
                                               border_color=main_color, border_width=1)
    start_uninstall.place(relx=0.6, rely=0.9, anchor="center")
    ToolTip(start_uninstall, msg="Start Uninstall", delay=0.5)

    cancel_uninstall = customtkinter.CTkButton(uninstall_window, text="X", command=uninstall_window.destroy,
                                               fg_color="transparent",
                                               hover_color=hover_color, text_color="#c900b2", width=75, height=40,
                                               border_color="#c900b2", border_width=1)
    cancel_uninstall.place(relx=0.835, rely=0.9, anchor="center")
    ToolTip(cancel_uninstall, msg="Cancel", delay=0.5)

    #Uninstall settings Label------------------------------------
    uninstall_options = customtkinter.CTkLabel(uninstall_window, text="Uninstall Options", fg_color="transparent",
                                             text_color=main_color, font=("Arial", 20, "bold"))
    uninstall_options.place(relx=0.1, rely=0.1, anchor="w")

    #Check Boxes----------------------------------
    uninstall_select_all_var = customtkinter.StringVar(value="on")
    uninstall_select_all = customtkinter.CTkCheckBox(uninstall_window, text="Select All", command=uninstall_select_all_f,
                                         variable=uninstall_select_all_var, onvalue="on", offvalue="off",hover_color=hover_color,
                                          checkbox_width= 20, checkbox_height=20,checkmark_color=background_color,
                                          corner_radius=0,border_width=1,fg_color=main_color,border_color=main_color)
    uninstall_select_all.place(relx=0.1, rely=0.2, anchor="w")


    uninstall_select_mc_var = customtkinter.StringVar(value="on")
    uninstall_select_mc = customtkinter.CTkCheckBox(uninstall_window, text="Uninstall Mastercam", command=uninstall_select_mc_f,
                                          variable=uninstall_select_mc_var, onvalue="on", offvalue="off", hover_color=hover_color,
                                          checkbox_width=20, checkbox_height=20, checkmark_color=background_color,
                                          corner_radius=0, border_width=1, fg_color=main_color, border_color=main_color)
    uninstall_select_mc.place(relx=0.2, rely=0.3, anchor="w")


    uninstall_select_my_backup_var = customtkinter.StringVar(value="on")
    uninstall_select_my_backup = customtkinter.CTkCheckBox(uninstall_window, text="Backup My Mastercam Folder", command=uninstall_select_my_backup_f,
                                          variable=uninstall_select_my_backup_var, onvalue="on", offvalue="off", hover_color=hover_color,
                                          checkbox_width=20, checkbox_height=20, checkmark_color=background_color,
                                          corner_radius=0, border_width=1, fg_color=main_color, border_color=main_color)
    uninstall_select_my_backup.place(relx=0.2, rely=0.4, anchor="w")


    uninstall_select_shared_backup_var = customtkinter.StringVar(value="on")
    uninstall_select_shared_backup = customtkinter.CTkCheckBox(uninstall_window, text="Backup Shared Mastercam Folder", command=uninstall_select_shared_backup_f,
                                          variable=uninstall_select_shared_backup_var, onvalue="on", offvalue="off", hover_color=hover_color,
                                          checkbox_width=20, checkbox_height=20, checkmark_color=background_color,
                                          corner_radius=0, border_width=1, fg_color=main_color, border_color=main_color)
    uninstall_select_shared_backup.place(relx=0.2, rely=0.5, anchor="w")

    uninstall_select_program_files_delete_var = customtkinter.StringVar(value="on")
    uninstall_select_program_files_delete = customtkinter.CTkCheckBox(uninstall_window, text="Delete Program Files", command=uninstall_select_program_files_delete_f,
                                          variable=uninstall_select_program_files_delete_var, onvalue="on", offvalue="off", hover_color=hover_color,
                                          checkbox_width=20, checkbox_height=20, checkmark_color=background_color,
                                          corner_radius=0, border_width=1, fg_color=main_color, border_color=main_color)
    uninstall_select_program_files_delete.place(relx=0.2, rely=0.6, anchor="w")

    uninstall_select_registry_delete_var = customtkinter.StringVar(value="on")
    uninstall_select_registry_delete = customtkinter.CTkCheckBox(uninstall_window, text="Delete Registrys", command=uninstall_select_registry_delete_f,
                                          variable=uninstall_select_registry_delete_var, onvalue="on", offvalue="off", hover_color=hover_color,
                                          checkbox_width=20, checkbox_height=20, checkmark_color=background_color,
                                          corner_radius=0, border_width=1, fg_color=main_color, border_color=main_color)
    uninstall_select_registry_delete.place(relx=0.2, rely=0.7, anchor="w")

#Uninstall/Reinstall settings Window
def open_uninstall_reinstall_settings_f(main_app):
    print("open_uninstall_reinstall_settings_f")
    # Create the top-level window
    install_window = customtkinter.CTkToplevel(master=main_app)
    install_window.geometry("700x400")
    install_window.resizable(False,False)
    install_window.title("Uninstall/Reinstall settings")
    customtkinter.set_appearance_mode("dark")

    # Lift it to the top so it doesn't hide behind the main window
    install_window.lift()

    # FORCE INTERACTION FOCUS TO THIS WINDOW ONLY
    install_window.focus_set()  # Grabs keyboard focus
    install_window.grab_set()

    # Callback
    def start_uninstall_reinstall_f():
        print("start_uninstall_reinstall_f")

    def uninstall_reinstall_uninstall_select_all_f():
        print("uninstall_reinstall_uninstall_select_all_f:", uninstall_reinstall_uninstall_select_all.get())
        # Check what state the "Select All" master variable is currently in
        if uninstall_reinstall_uninstall_select_all_var.get() == "on":
            # If master is checked, force select ALL sub-checkboxes
            uninstall_reinstall_uninstall_mc.select()
            uninstall_reinstall_my_backup.select()
            uninstall_reinstall_shared_backup.select()
            uninstall_reinstall_program_files_delete.select()
            uninstall_reinstall_registry_delete.select()
        else:
            # If master is unchecked, force deselect ALL sub-checkboxes
            uninstall_reinstall_uninstall_mc.deselect()
            uninstall_reinstall_my_backup.deselect()
            uninstall_reinstall_shared_backup.deselect()
            uninstall_reinstall_program_files_delete.deselect()
            uninstall_reinstall_registry_delete.deselect()

    def uninstall_reinstall_uninstall_mc_f():
        print("uninstall_reinstall_uninstall_mc_f:", uninstall_reinstall_uninstall_mc.get())

        """Unchecks 'Select All' if the user manually unchecks any single option."""
        # List of all your sub-variables
        all_checked = (
                uninstall_reinstall_uninstall_mc_var.get() == "on" and
                uninstall_reinstall_my_backup_var.get() == "on" and
                uninstall_reinstall_shared_backup_var.get() == "on" and
                uninstall_reinstall_program_files_delete_var.get() == "on" and
                uninstall_reinstall_registry_delete.get() == "on"
        )

        if all_checked:
            uninstall_reinstall_uninstall_select_all.select()
        else:
            # If even one item is manually unchecked, turn off the "Select All" checkmark
            uninstall_reinstall_uninstall_select_all.deselect()

    def uninstall_reinstall_my_backup_f():
        print("uninstall_reinstall_my_backup_f:", uninstall_reinstall_my_backup.get())

        """Unchecks 'Select All' if the user manually unchecks any single option."""
        # List of all your sub-variables
        all_checked = (
                uninstall_reinstall_uninstall_mc_var.get() == "on" and
                uninstall_reinstall_my_backup_var.get() == "on" and
                uninstall_reinstall_shared_backup_var.get() == "on" and
                uninstall_reinstall_program_files_delete_var.get() == "on" and
                uninstall_reinstall_registry_delete.get() == "on"
        )

        if all_checked:
            uninstall_reinstall_uninstall_select_all.select()
        else:
            # If even one item is manually unchecked, turn off the "Select All" checkmark
            uninstall_reinstall_uninstall_select_all.deselect()

    def uninstall_reinstall_shared_backup_f():
        print("uninstall_reinstall_shared_backup_f:", uninstall_reinstall_shared_backup.get())

        """Unchecks 'Select All' if the user manually unchecks any single option."""
        # List of all your sub-variables
        all_checked = (
                uninstall_reinstall_uninstall_mc_var.get() == "on" and
                uninstall_reinstall_my_backup_var.get() == "on" and
                uninstall_reinstall_shared_backup_var.get() == "on" and
                uninstall_reinstall_program_files_delete_var.get() == "on" and
                uninstall_reinstall_registry_delete.get() == "on"
        )

        if all_checked:
            uninstall_reinstall_uninstall_select_all.select()
        else:
            # If even one item is manually unchecked, turn off the "Select All" checkmark
            uninstall_reinstall_uninstall_select_all.deselect()

    def uninstall_reinstall_program_files_delete_f():
        print("uninstall_reinstall_program_files_delete_f:", uninstall_reinstall_program_files_delete.get())

        """Unchecks 'Select All' if the user manually unchecks any single option."""
        # List of all your sub-variables
        all_checked = (
                uninstall_reinstall_uninstall_mc_var.get() == "on" and
                uninstall_reinstall_my_backup_var.get() == "on" and
                uninstall_reinstall_shared_backup_var.get() == "on" and
                uninstall_reinstall_program_files_delete_var.get() == "on" and
                uninstall_reinstall_registry_delete.get() == "on"
        )

        if all_checked:
            uninstall_reinstall_uninstall_select_all.select()
        else:
            # If even one item is manually unchecked, turn off the "Select All" checkmark
            uninstall_reinstall_uninstall_select_all.deselect()

    def uninstall_reinstall_registry_delete_f():
        print("uninstall_reinstall_registry_delete_f:", uninstall_reinstall_registry_delete.get())

        """Unchecks 'Select All' if the user manually unchecks any single option."""
        # List of all your sub-variables
        all_checked = (
                uninstall_reinstall_uninstall_mc_var.get() == "on" and
                uninstall_reinstall_my_backup_var.get() == "on" and
                uninstall_reinstall_shared_backup_var.get() == "on" and
                uninstall_reinstall_program_files_delete_var.get() == "on" and
                uninstall_reinstall_registry_delete.get() == "on"
        )

        if all_checked:
            uninstall_reinstall_uninstall_select_all.select()
        else:
            # If even one item is manually unchecked, turn off the "Select All" checkmark
            uninstall_reinstall_uninstall_select_all.deselect()

    # Exit Buttons------------------------------------------------
    start_uninstall_reinstall = customtkinter.CTkButton(install_window, text="O", command=start_uninstall_reinstall_f,
                                        fg_color="transparent",
                                        hover_color=hover_color, text_color=main_color, width=75, height=40,
                                        border_color=main_color, border_width=1)
    start_uninstall_reinstall.place(relx=0.79, rely=0.9, anchor="center")
    ToolTip(start_uninstall_reinstall, msg="Start Uninstall/Reinstall", delay=0.5)

    cancel_uninstall_reinstall = customtkinter.CTkButton(install_window, text="X", command=install_window.destroy,
                                            fg_color="transparent",
                                            hover_color=hover_color, text_color="#c900b2", width=75, height=40,
                                            border_color="#c900b2", border_width=1)
    cancel_uninstall_reinstall.place(relx=0.91, rely=0.9, anchor="center")
    ToolTip(cancel_uninstall_reinstall, msg="Cancel", delay=0.5)

    #Uninstall options Label------------------------------------
    uninstall_reinstall_uninstall_options = customtkinter.CTkLabel(install_window, text="Uninstall Options", fg_color="transparent",
                                                     text_color=main_color, font=("Arial", 20, "bold"))
    uninstall_reinstall_uninstall_options.place(relx=0.05, rely=0.1, anchor="w")


    # Uninstall Check Boxes----------------------------------
    uninstall_reinstall_uninstall_select_all_var = customtkinter.StringVar(value="on")
    uninstall_reinstall_uninstall_select_all = customtkinter.CTkCheckBox(install_window, text="Select All", command=uninstall_reinstall_uninstall_select_all_f,
                                          variable=uninstall_reinstall_uninstall_select_all_var, onvalue="on", offvalue="off", hover_color=hover_color,
                                          checkbox_width=20, checkbox_height=20, checkmark_color=background_color,
                                          corner_radius=0, border_width=1, fg_color=main_color, border_color=main_color)
    uninstall_reinstall_uninstall_select_all.place(relx=0.05, rely=0.2, anchor="w")

    uninstall_reinstall_uninstall_mc_var = customtkinter.StringVar(value="on")
    uninstall_reinstall_uninstall_mc = customtkinter.CTkCheckBox(install_window, text="Uninstall Mastercam",
                                                   command=uninstall_reinstall_uninstall_mc_f,
                                                   variable=uninstall_reinstall_uninstall_mc_var, onvalue="on", offvalue="off",
                                                   hover_color=hover_color,
                                                   checkbox_width=20, checkbox_height=20,
                                                   checkmark_color=background_color,
                                                   corner_radius=0, border_width=1, fg_color=main_color,
                                                   border_color=main_color)
    uninstall_reinstall_uninstall_mc.place(relx=0.1, rely=0.3, anchor="w")

    uninstall_reinstall_my_backup_var = customtkinter.StringVar(value="on")
    uninstall_reinstall_my_backup = customtkinter.CTkCheckBox(install_window, text="Backup My Mastercam Folder",
                                                command=uninstall_reinstall_my_backup_f,
                                                variable=uninstall_reinstall_my_backup_var, onvalue="on", offvalue="off",
                                                hover_color=hover_color,
                                                checkbox_width=20, checkbox_height=20, checkmark_color=background_color,
                                                corner_radius=0, border_width=1, fg_color=main_color,
                                                border_color=main_color)
    uninstall_reinstall_my_backup.place(relx=0.1, rely=0.4, anchor="w")

    uninstall_reinstall_shared_backup_var = customtkinter.StringVar(value="on")
    uninstall_reinstall_shared_backup = customtkinter.CTkCheckBox(install_window, text="Backup Shared Mastercam Folder",
                                                    command=uninstall_reinstall_shared_backup_f,
                                                    variable=uninstall_reinstall_shared_backup_var, onvalue="on", offvalue="off",
                                                    hover_color=hover_color,
                                                    checkbox_width=20, checkbox_height=20,
                                                    checkmark_color=background_color,
                                                    corner_radius=0, border_width=1, fg_color=main_color,
                                                    border_color=main_color)
    uninstall_reinstall_shared_backup.place(relx=0.1, rely=0.5, anchor="w")

    uninstall_reinstall_program_files_delete_var = customtkinter.StringVar(value="on")
    uninstall_reinstall_program_files_delete = customtkinter.CTkCheckBox(install_window, text="Delete Program Files",
                                                           command=uninstall_reinstall_program_files_delete_f,
                                                           variable=uninstall_reinstall_program_files_delete_var, onvalue="on",
                                                           offvalue="off", hover_color=hover_color,
                                                           checkbox_width=20, checkbox_height=20,
                                                           checkmark_color=background_color,
                                                           corner_radius=0, border_width=1, fg_color=main_color,
                                                           border_color=main_color)
    uninstall_reinstall_program_files_delete.place(relx=0.1, rely=0.6, anchor="w")

    uninstall_reinstall_registry_delete_var = customtkinter.StringVar(value="on")
    uninstall_reinstall_registry_delete = customtkinter.CTkCheckBox(install_window, text="Delete Registrys",
                                                      command=uninstall_reinstall_registry_delete_f,
                                                      variable=uninstall_reinstall_registry_delete_var, onvalue="on", offvalue="off",
                                                      hover_color=hover_color,
                                                      checkbox_width=20, checkbox_height=20,
                                                      checkmark_color=background_color,
                                                      corner_radius=0, border_width=1, fg_color=main_color,
                                                      border_color=main_color)
    uninstall_reinstall_registry_delete.place(relx=0.1, rely=0.7, anchor="w")


    ###Install functions-------------------------------------------------------
    # Install options Label------------------------------------
    label_install_options = customtkinter.CTkLabel(install_window, text="Install Options", fg_color="transparent",
                                                   text_color=main_color, font=("Arial", 20, "bold"))
    label_install_options.place(relx=0.5, rely=0.1, anchor="w")

    def uninstall_reinstall_language_select_f(values):
        print(f"uninstall_reinstall_language_select_f: {values}")

        # if values == "English":
        #     print("Loading English language translation profiles...")
        #     # Add your English text changes here
        # elif values == "Other":
        #     print("Loading alternative language translation profiles...")
        #     # Add your alternative text changes here

    def uninstall_reinstall_unit_select_f(values):
        print(f"uninstall_reinstall_unit_select_f: {values}")

    def uninstall_reinstall_users_select_f(values):
        print(f"uninstall_reinstall_users_select_f: {values}")

    def uninstall_reinstall_license_f():
        print("uninstall_reinstall_license_f")

    def uninstall_reinstall_restore_backup_f():
        print("uninstall_reinstall_restore_backup_f")

    def uninstall_reinstall_select_install_file_f():
        print("uninstall_reinstall_select_install_file_f")
        # Opens the OS file picker dialog
        file_path = filedialog.askopenfilename(
            title="Select Mastercam File",
            # Optional: restrict types (e.g., all files, executables, text)
            filetypes=[("All Files", "*.*"), ("Executables", "*.exe")]
        )

        # If the user selected a file (didn't click cancel)
        if file_path:
            # Clear the old path text inside the input entry field
            uninstall_reinstall_file_entry_install.delete(0, "end")
            # Insert the newly selected file path text string
            uninstall_reinstall_file_entry_install.insert(0, file_path)

    def uninstall_reinstall_select_language_file_f():
        print("uninstall_reinstall_select_language_file_f")
        # Opens the OS file picker dialog
        file_path = filedialog.askopenfilename(
            title="Select Language File",
            # Optional: restrict types (e.g., all files, executables, text)
            filetypes=[("All Files", "*.*"), ("Executables", "*.exe")]
        )

        # If the user selected a file (didn't click cancel)
        if file_path:
            # Clear the old path text inside the input entry field
            uninstall_reinstall_file_entry_language.delete(0, "end")
            # Insert the newly selected file path text string
            uninstall_reinstall_file_entry_language.insert(0, file_path)


    # segemented button----------------------------------

    uninstall_reinstall_language_select = customtkinter.CTkSegmentedButton(install_window, values=["English", "Other"],
                                                         command=uninstall_reinstall_language_select_f, fg_color=background_color,
                                                        selected_color=main_color, unselected_color=background_color,
                                                        selected_hover_color=main_color, unselected_hover_color=hover_color,
                                                        text_color="#c900b2")
    uninstall_reinstall_language_select.set("English")
    uninstall_reinstall_language_select.place(relx=0.55, rely=0.2, anchor="w")


    uninstall_reinstall_unit_select = customtkinter.CTkSegmentedButton(install_window, values=["Metric", "U.S."],
                                                         command=uninstall_reinstall_unit_select_f, fg_color=background_color,
                                                        selected_color=main_color, unselected_color=background_color,
                                                        selected_hover_color=main_color, unselected_hover_color=hover_color,
                                                        text_color="#c900b2")
    uninstall_reinstall_unit_select.set("Metric")
    uninstall_reinstall_unit_select.place(relx=0.55, rely=0.3, anchor="w")

    uninstall_reinstall_users_select = customtkinter.CTkSegmentedButton(install_window, values=["All Users", "Only For Me"],
                                                         command=uninstall_reinstall_users_select_f, fg_color=background_color,
                                                        selected_color=main_color, unselected_color=background_color,
                                                        selected_hover_color=main_color, unselected_hover_color=hover_color,
                                                        text_color="#c900b2")
    uninstall_reinstall_users_select.set("All Users")
    uninstall_reinstall_users_select.place(relx=0.55, rely=0.4, anchor="w")

    # Install Check Boxes----------------------------------

    uninstall_reinstall_license_var = customtkinter.StringVar(value="off")
    uninstall_reinstall_license = customtkinter.CTkCheckBox(install_window, text="Yes, I accept the terms of the license agreement",
                                                           command=uninstall_reinstall_license_f,
                                                           variable=uninstall_reinstall_license_var, onvalue="on",
                                                           offvalue="off", hover_color=hover_color,
                                                           checkbox_width=20, checkbox_height=20,
                                                           checkmark_color=background_color,
                                                           corner_radius=0, border_width=1, fg_color=main_color,
                                                           border_color=main_color)
    uninstall_reinstall_license.place(relx=0.55, rely=0.5, anchor="w")

    uninstall_reinstall_restore_backup_var = customtkinter.StringVar(value="on")
    uninstall_reinstall_restore_backup = customtkinter.CTkCheckBox(install_window, text="Restore Backups",
                                                           command=uninstall_reinstall_restore_backup_f,
                                                           variable=uninstall_reinstall_restore_backup_var, onvalue="on",
                                                           offvalue="off", hover_color=hover_color,
                                                           checkbox_width=20, checkbox_height=20,
                                                           checkmark_color=background_color,
                                                           corner_radius=0, border_width=1, fg_color=main_color,
                                                           border_color=main_color)
    uninstall_reinstall_restore_backup.place(relx=0.55, rely=0.6, anchor="w")


    #file select install
    uninstall_reinstall_file_entry_install = customtkinter.CTkEntry(install_window,width=250,placeholder_text="Select MC Install File...",border_color=main_color, border_width=1)
    uninstall_reinstall_file_entry_install.place(relx=0.5, rely=0.9, anchor="center")

    uninstall_reinstall_select_install_file = customtkinter.CTkButton(install_window, text="O",
                                                               command=uninstall_reinstall_select_install_file_f,
                                                               fg_color="transparent",
                                                               hover_color=hover_color, text_color=main_color, width=28,
                                                               height=28,
                                                               border_color=main_color, border_width=1,)
    uninstall_reinstall_select_install_file.place(relx=0.29, rely=0.9, anchor="center")

    #file select language
    uninstall_reinstall_file_entry_language = customtkinter.CTkEntry(install_window,width=150,placeholder_text="Select Language File...",border_color=main_color, border_width=1)
    uninstall_reinstall_file_entry_language.place(relx=0.75, rely=0.2, anchor="w")

    uninstall_reinstall_select_language_file = customtkinter.CTkButton(install_window, text="O",
                                                               command=uninstall_reinstall_select_language_file_f,
                                                               fg_color="transparent",
                                                               hover_color=hover_color, text_color=main_color, width=28,
                                                               height=28,
                                                               border_color=main_color, border_width=1,)
    uninstall_reinstall_select_language_file.place(relx=0.72, rely=0.2, anchor="center")

#Show Left over files in a new window
def show_files_on_pc_window_f(main_app):
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

def dropdown_callback_f(choice):
    print(f"dropdown_callback_f: {choice}")
    if choice == "Select MC Version...":
        open_uninstall_settings.configure(state="disabled")
        open_uninstall_reinstall_settings.configure(state="disabled")
        show_files_on_pc_window.configure(state="disabled")
    else:
        open_uninstall_settings.configure(state="normal")
        open_uninstall_reinstall_settings.configure(state="normal")
        show_files_on_pc_window.configure(state="normal")


# region -- Dropdown----------------------------------------------------

# Predefined list of options
dropdown_options = ["Mastercam (vercion1)", "Mastercam (vercion2)", "Mastercam (vercion3)"]

# Create the OptionMenu widget
dropdown = customtkinter.CTkOptionMenu(main_app,values=dropdown_options,fg_color=hover_color,button_color=dropdown_button_color,
                                       button_hover_color=hover_color,width=200,height=28 ,command=dropdown_callback_f)
dropdown.set("Select MC Version...")
dropdown.place(relx=0.226, rely=0.1, anchor="center")



# endregion

# region -- Buttons Uninstall and Reinstall-----------------------------
open_uninstall_settings = customtkinter.CTkButton(main_app, text="Uninstall", command=lambda: open_uninstall_settings_f(main_app),
                                                fg_color="transparent",
                                                hover_color=hover_color, text_color=main_color, width=125, height=28,
                                                border_color=main_color, border_width=1)
open_uninstall_settings.place(relx=0.6, rely=0.1, anchor="center")

open_uninstall_reinstall_settings = customtkinter.CTkButton(main_app, text="Uninstall/Reinstall",
                                                command=lambda: open_uninstall_reinstall_settings_f(main_app), fg_color="transparent",
                                                hover_color=hover_color, text_color=main_color, width=125, height=28,
                                                border_color=main_color, border_width=1)
open_uninstall_reinstall_settings.place(relx=0.835, rely=0.1, anchor="center")
# endregion

# region -- Show files Button------------------------------------------
show_files_on_pc_window = customtkinter.CTkButton(main_app, text="FOP", command=lambda: show_files_on_pc_window_f(main_app),
                                                 fg_color="transparent",
                                                 hover_color=hover_color, text_color=main_color, width=28, height=28,
                                                 border_color=main_color, border_width=1)
show_files_on_pc_window.place(relx=0.445, rely=0.1, anchor="center")
ToolTip(show_files_on_pc_window, msg="Files On PC", delay=0.5)
# endregion

# region -- Text box-------------------------------------------------
# frame = customtkinter.CTkFrame(master=main_app, width=530, height=250)
# frame.place(relx=0.5, rely=0.15, anchor="n")
messagebox = customtkinter.CTkTextbox(main_app, width=530, height=250, fg_color=hover_color, )
messagebox.place(relx=0.5, rely=0.15, anchor="n")
messagebox.configure(state="disabled")
# endregion

# region -- Progressbar----------------------------------------------
label = customtkinter.CTkLabel(main_app, text="Prograce label", fg_color="transparent", text_color=main_color)
label.place(relx=0.17, rely=0.7, anchor="w")

progressbar = customtkinter.CTkProgressBar(main_app, orientation="horizontal", width=400, height=12, corner_radius=0,
                                           progress_color=main_color)
progressbar.set(progressbar_var)
progressbar.place(relx=0.5, rely=0.74, anchor="center")
# endregion

# region -- #Unistall Process----------------------------------------
label_uninstall = customtkinter.CTkLabel(main_app, text="label_uninstall", fg_color="transparent",
                                         text_color=main_color)
label_uninstall.place(relx=0.17, rely=0.8, anchor="w")

button_uninstall_process = customtkinter.CTkButton(main_app, text="", fg_color="transparent", hover_color=hover_color,
                                                   width=16 * 3, height=16, corner_radius=8,
                                                   border_color=main_color, border_width=1, state="disabled")
button_uninstall_process.place(relx=0.21, rely=0.85, anchor="center")
ToolTip(button_uninstall_process, msg="Mastercam Uninstall", delay=0.0)

button_my_mastercam_backup = customtkinter.CTkButton(main_app, text="", fg_color="transparent", hover_color=hover_color,
                                                     width=16 * 3, height=16, corner_radius=8,
                                                     border_color=main_color, border_width=1, state="disabled")
button_my_mastercam_backup.place(relx=0.31, rely=0.85, anchor="center")
ToolTip(button_my_mastercam_backup, msg="My Mastercam Backup", delay=0.0)

button_shared_mastercam_backup = customtkinter.CTkButton(main_app, text="", fg_color="transparent",
                                                         hover_color=hover_color, width=16 * 3, height=16,
                                                         corner_radius=8,
                                                         border_color=main_color, border_width=1, state="disabled")
button_shared_mastercam_backup.place(relx=0.41, rely=0.85, anchor="center")
ToolTip(button_shared_mastercam_backup, msg="Shared Mastercam Backup", delay=0.0)

button_program_files_delete = customtkinter.CTkButton(main_app, text="", fg_color="transparent",
                                                      hover_color=hover_color, width=16 * 3, height=16, corner_radius=8,
                                                      border_color=main_color, border_width=1, state="disabled")
button_program_files_delete.place(relx=0.51, rely=0.85, anchor="center")
ToolTip(button_program_files_delete, msg="Program Files Delete", delay=0.0)

button_registry_delete = customtkinter.CTkButton(main_app, text="", fg_color="transparent", hover_color=hover_color,
                                                 width=16 * 3, height=16, corner_radius=8,
                                                 border_color=main_color, border_width=1, state="disabled")
button_registry_delete.place(relx=0.61, rely=0.85, anchor="center")
ToolTip(button_registry_delete, msg="Registry Delete", delay=0.0)

# endregion

# region -- Reistall Process buttons---------------------------------
# Run Executibel
# Yes to run exe
# Press top button (Masercam install)
# Select language
# Select units and users (All users or only for Me)
# Lcense agreement
# Install

label_reinstall = customtkinter.CTkLabel(main_app, text="label_reinstall", fg_color="transparent",
                                         text_color=main_color)
label_reinstall.place(relx=0.17, rely=0.9, anchor="w")

# Language Selected
button_language = customtkinter.CTkButton(main_app, text="", fg_color="transparent", hover_color=hover_color,
                                          width=16 * 3, height=16, corner_radius=8,
                                          border_color=main_color, border_width=1, state="disabled")
button_language.place(relx=0.21, rely=0.95, anchor="center")
ToolTip(button_language, msg="Language Select (english)", delay=0.0)

# Units Selected
button_units = customtkinter.CTkButton(main_app, text="", fg_color="transparent", hover_color=hover_color, width=16 * 3,
                                       height=16, corner_radius=8,
                                       border_color=main_color, border_width=1, state="disabled")
button_units.place(relx=0.31, rely=0.95, anchor="center")
ToolTip(button_units, msg="Units Select", delay=0.0)

# users Selected
button_users = customtkinter.CTkButton(main_app, text="", fg_color="transparent", hover_color=hover_color, width=16 * 3,
                                       height=16, corner_radius=8,
                                       border_color=main_color, border_width=1, state="disabled")
button_users.place(relx=0.41, rely=0.95, anchor="center")
ToolTip(button_users, msg="Users Select", delay=0.0)

# License agreement
button_license = customtkinter.CTkButton(main_app, text="", fg_color="transparent", hover_color=hover_color,
                                         width=16 * 3, height=16, corner_radius=8,
                                         border_color=main_color, border_width=1, state="disabled")
button_license.place(relx=0.51, rely=0.95, anchor="center")
ToolTip(button_license, msg="License agreement", delay=0.0)

# Restore Backup
button_restore_backup = customtkinter.CTkButton(main_app, text="", fg_color="transparent", hover_color=hover_color,
                                                width=16 * 3, height=16, corner_radius=8,
                                                border_color=main_color, border_width=1, state="disabled")
button_restore_backup.place(relx=0.61, rely=0.95, anchor="center")
ToolTip(button_restore_backup, msg="Restore Backup", delay=0.0)
# endregion

dropdown_callback_f(dropdown.get())

main_app.mainloop()
