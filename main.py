import hashlib
import customtkinter as ctk
from tkinter import filedialog
from markdown import markdown


# Database logic placeholder
class Database:
    def __init__(self):
        self.users = {}  # Temporary storage

    def add_user(self, username, hashed_password):
        self.users[username] = hashed_password

    def verify_user(self, username, hashed_password):
        return self.users.get(username) == hashed_password


# Markdown App GUI
class MarkdownAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Markdown Note App")
        self.root.geometry("1200x800")
        self.db = Database()
        self.current_user = None

        self.setup_login_screen()

    def setup_login_screen(self):
        self.clear_screen()

        self.login_frame = ctk.CTkFrame(self.root)
        self.login_frame.pack(fill="both", expand=True)

        # Left Panel
        self.left_panel = ctk.CTkFrame(self.login_frame, width=400, fg_color="#5C4B51")
        self.left_panel.pack(side="left", fill="both", expand=False)
        self.left_label = ctk.CTkLabel(self.left_panel, text="AUTHENTICATE", font=("Arial", 24, "bold"),
                                       text_color="white")
        self.left_label.place(relx=0.5, rely=0.5, anchor="center")

        # Right Panel
        self.right_panel = ctk.CTkFrame(self.login_frame, fg_color="#F4F4F4")
        self.right_panel.pack(side="right", fill="both", expand=True)

        self.username_entry = ctk.CTkEntry(self.right_panel, placeholder_text="user name", width=300)
        self.username_entry.pack(pady=20)

        self.password_entry = ctk.CTkEntry(self.right_panel, placeholder_text="Password", show="*", width=300)
        self.password_entry.pack(pady=20)

        self.login_button = ctk.CTkButton(self.right_panel, text="LOGIN", command=self.login, width=200,
                                          fg_color="#5C4B51")
        self.login_button.pack(pady=10)

        self.register_button = ctk.CTkButton(self.right_panel, text="REGISTER NOW", command=self.register, width=200,
                                             fg_color="#5C4B51")
        self.register_button.pack(pady=10)

        self.error_label = ctk.CTkLabel(self.right_panel, text="", text_color="red")
        self.error_label.pack(pady=10)

    def setup_main_screen(self):
        self.clear_screen()

        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(fill="both", expand=True)

        # Left Panel
        self.left_panel = ctk.CTkFrame(self.main_frame, fg_color="#5C4B51", width=400)
        self.left_panel.pack(side="left", fill="both", expand=False)

        self.save_button = ctk.CTkButton(self.left_panel, text="SAVE", command=self.save_file, fg_color="#7E6A70")
        self.save_button.pack(pady=20)

        self.open_button = ctk.CTkButton(self.left_panel, text="OPEN", command=self.open_file, fg_color="#7E6A70")
        self.open_button.pack(pady=20)

        self.preview_button = ctk.CTkButton(self.left_panel, text="PREVIEW", command=self.update_preview,
                                            fg_color="#7E6A70")
        self.preview_button.pack(pady=20)

        self.logout_button = ctk.CTkButton(self.left_panel, text="LOGOUT", command=self.logout, fg_color="#7E6A70")
        self.logout_button.pack(pady=20)

        # Right Panel
        self.right_panel = ctk.CTkFrame(self.main_frame, fg_color="#F4F4F4")
        self.right_panel.pack(side="right", fill="both", expand=True)

        self.text_area = ctk.CTkTextbox(self.right_panel, wrap="word", width=500, height=500)
        self.text_area.pack(side="left", fill="both", expand=True, padx=10, pady=10)

        self.preview_text = ctk.CTkTextbox(self.right_panel, wrap="word", state="disabled", width=500, height=500)
        self.preview_text.pack(side="right", fill="both", expand=True, padx=10, pady=10)

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        if self.db.verify_user(username, hashed_password):
            self.current_user = username
            self.setup_main_screen()
        else:
            self.error_label.configure(text="Invalid username or password")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        hashed_password = hashlib.sha256(password.encode()).hexdigest()

        if username in self.db.users:
            self.error_label.configure(text="Username already exists")
        else:
            self.db.add_user(username, hashed_password)
            self.error_label.configure(text="Registration successful", text_color="green")

    def save_file(self):
        content = self.text_area.get("1.0", "end-1c")
        if not content.strip():
            self.error_label.configure(text="Cannot save an empty note")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".md", filetypes=[("Markdown Files", "*.md")])
        if file_path:
            with open(file_path, "w") as file:
                file.write(content)
            self.error_label.configure(text="File saved successfully", text_color="green")

    def open_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Markdown Files", "*.md")])
        if file_path:
            try:
                with open(file_path, "r") as file:
                    content = file.read()
                self.text_area.delete("1.0", "end")
                self.text_area.insert("1.0", content)
                self.error_label.configure(text="File loaded successfully", text_color="green")
            except Exception as e:
                self.error_label.configure(text=f"Error: {str(e)}")

    def update_preview(self):
        content = self.text_area.get("1.0", "end-1c")
        html_content = markdown(content)
        self.preview_text.configure(state="normal")
        self.preview_text.delete("1.0", "end")
        self.preview_text.insert("1.0", html_content)
        self.preview_text.configure(state="disabled")

    def logout(self):
        self.current_user = None
        self.setup_login_screen()


# Main Execution
if __name__ == "__main__":
    root = ctk.CTk()
    app_gui = MarkdownAppGUI(root)
    root.mainloop()
