import customtkinter as ctk
from tkinter import messagebox
from markdown import markdown
from database import save_note, get_notes, delete_note
from authenticate import Auth
import datetime

# Initialize customtkinter
ctk.set_appearance_mode("System")  # Set appearance mode
ctk.set_default_color_theme("blue")  # Set default color theme


class MarkdownAppGUI:
    def __init__(self, root):
        self.note_dropdown = None
        self.note_selection_window = None
        self.new_note_entry = None
        self.save_note_window = None
        self.preview_text = None
        self.text_area = None
        self.logout_button = None
        self.preview_button = None
        self.error_label = None
        self.open_button = None
        self.save_button = None
        self.main_frame = None
        self.register_button = None
        self.login_button = None
        self.password_entry = None
        self.username_entry = None
        self.right_panel = None
        self.left_label = None
        self.left_panel = None
        self.login_frame = None
        self.root = root
        self.root.title("Markdown Note App")
        self.root.geometry("1200x800")
        self.auth = Auth()
        self.setup_login_screen()

    def setup_login_screen(self):
        # Clear the screen
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create the login frame
        self.login_frame = ctk.CTkFrame(self.root)
        self.login_frame.pack(fill="both", expand=True)

        # Left panel (for aesthetics)
        self.left_panel = ctk.CTkFrame(self.login_frame, width=400, fg_color="#5C4B51")
        self.left_panel.pack(side="left", fill="both", expand=False)
        self.left_label = ctk.CTkLabel(self.left_panel, text="AUTHENTICATE", font=("Arial", 24, "bold"),
                                       text_color="white")
        self.left_label.place(relx=0.5, rely=0.5, anchor="center")

        # Right panel (for login/register form)
        self.right_panel = ctk.CTkFrame(self.login_frame, fg_color="#F4F4F4")
        self.right_panel.pack(side="right", fill="both", expand=True)

        # Username entry
        self.username_entry = ctk.CTkEntry(self.right_panel, placeholder_text="Username", width=300)
        self.username_entry.pack(pady=20)

        # Password entry
        self.password_entry = ctk.CTkEntry(self.right_panel, placeholder_text="Password", show="*", width=300)
        self.password_entry.pack(pady=20)

        # Login button
        self.login_button = ctk.CTkButton(self.right_panel, text="LOGIN", command=self.login, width=200,
                                          fg_color="#5C4B51")
        self.login_button.pack(pady=10)

        # Register button
        self.register_button = ctk.CTkButton(self.right_panel, text="REGISTER NOW", command=self.register, width=200,
                                             fg_color="#5C4B51")
        self.register_button.pack(pady=10)

        # Error label
        self.error_label = ctk.CTkLabel(self.right_panel, text="", text_color="red")
        self.error_label.pack(pady=10)

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.auth.register(username, password):
            self.error_label.configure(text="Registration successful", text_color="green")
        else:
            self.error_label.configure(text="Username already exists", text_color="red")

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        if self.auth.login(username, password):
            self.setup_main_screen()
        else:
            self.error_label.configure(text="Invalid username or password")

    def setup_main_screen(self):
        # Clear the screen
        for widget in self.root.winfo_children():
            widget.destroy()

        # Create the main frame
        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        # Left panel (for buttons)
        self.left_panel = ctk.CTkFrame(self.main_frame, fg_color="#5C4B51", width=400)
        self.left_panel.pack(side="left", fill="both", expand=False)

        # Save button
        self.save_button = ctk.CTkButton(self.left_panel, text="SAVE", command=self.save_file, fg_color="#7E6A70")
        self.save_button.pack(pady=20)

        # Open button
        self.open_button = ctk.CTkButton(self.left_panel, text="OPEN", command=self.open_file, fg_color="#7E6A70")
        self.open_button.pack(pady=20)

        # Preview button
        self.preview_button = ctk.CTkButton(self.left_panel, text="PREVIEW", command=self.update_preview,
                                            fg_color="#7E6A70")
        self.preview_button.pack(pady=20)

        # Logout button
        self.logout_button = ctk.CTkButton(self.left_panel, text="LOGOUT", command=self.logout, fg_color="#7E6A70")
        self.logout_button.pack(pady=20)

        # Right panel (for text areas)
        self.right_panel = ctk.CTkFrame(self.main_frame, fg_color="#F4F4F4")
        self.right_panel.pack(side="right", fill="both", expand=True)

        # Text area for Markdown input
        self.text_area = ctk.CTkTextbox(self.right_panel, wrap="word", width=500, height=500)
        self.text_area.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        # Text area for HTML preview
        self.preview_text = ctk.CTkTextbox(self.right_panel, wrap="word", state="disabled", width=500, height=500)
        self.preview_text.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    def save_file(self):
        # Create a new window for saving notes
        self.save_note_window = ctk.CTkToplevel(self.root)
        self.save_note_window.title("Save Note")
        self.save_note_window.geometry("400x200")

        # Ensure the window stays on top
        self.save_note_window.lift()  # Bring the window to the front
        self.save_note_window.grab_set()  # Focus the window
        self.save_note_window.transient(self.root)  # Associate with the main window

        # Label
        ctk.CTkLabel(self.save_note_window, text="Save your note:").pack(pady=10)

        # Entry for new note title
        self.new_note_entry = ctk.CTkEntry(self.save_note_window, placeholder_text="Enter a title for your note")
        self.new_note_entry.pack(pady=10)

        # Button to save the note
        ctk.CTkButton(self.save_note_window, text="Save", command=self.save_selected_note).pack(pady=10)

    def save_selected_note(self):
        content = self.text_area.get("1.0", "end-1c")
        if not content.strip():
            messagebox.showerror("Error", "Cannot save an empty note")
            return

        # Get the new title
        new_title = self.new_note_entry.get().strip()
        if not new_title:
            messagebox.showerror("Error", "Please enter a title for your note")
            return

        # Save the note
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        save_note(self.auth.current_user, new_title, content, timestamp)
        messagebox.showinfo("Success", "Note saved successfully")
        self.save_note_window.destroy()

    def open_file(self):
        notes = get_notes(self.auth.current_user)
        if notes:
            # Create a new window for note selection
            self.note_selection_window = ctk.CTkToplevel(self.root)
            self.note_selection_window.title("Open Note")
            self.note_selection_window.geometry("400x250")

            # Ensure the window stays on top
            self.note_selection_window.lift()  # Bring the window to the front
            self.note_selection_window.grab_set()  # Focus the window
            self.note_selection_window.transient(self.root)  # Associate with the main window

            # Label
            ctk.CTkLabel(self.note_selection_window, text="Select a note to open:").pack(pady=10)

            # Dropdown (OptionMenu) to display note titles
            self.note_dropdown = ctk.CTkOptionMenu(self.note_selection_window, values=[note[0] for note in notes])
            self.note_dropdown.pack(pady=10)

            # Button to open the selected note
            ctk.CTkButton(self.note_selection_window, text="Open", command=self.load_selected_note).pack(pady=10)

            # Button to delete the selected note
            ctk.CTkButton(self.note_selection_window, text="Delete", command=self.delete_selected_note,
                          fg_color="red").pack(pady=10)
        else:
            messagebox.showinfo("Info", "No notes found")

    def load_selected_note(self):
        selected_title = self.note_dropdown.get()
        if selected_title:
            notes = get_notes(self.auth.current_user)
            for note in notes:
                if note[0] == selected_title:
                    self.text_area.delete("1.0", "end")
                    self.text_area.insert("1.0", note[1])
                    messagebox.showinfo("Success", "Note loaded successfully")
                    self.note_selection_window.destroy()
                    break

    def delete_selected_note(self):
        selected_title = self.note_dropdown.get()
        if selected_title:
            confirm = messagebox.askyesno("Confirm", f"Are you sure you want to delete '{selected_title}'?")
            if confirm:
                delete_note(self.auth.current_user, selected_title)
                messagebox.showinfo("Success", "Note deleted successfully")
                self.note_selection_window.destroy()

    def update_preview(self):
        content = self.text_area.get("1.0", "end-1c")
        html_content = markdown(content)
        self.preview_text.configure(state="normal")
        self.preview_text.delete("1.0", "end")
        self.preview_text.insert("1.0", html_content)
        self.preview_text.configure(state="disabled")

    def logout(self):
        self.auth.logout()
        self.setup_login_screen()
