import customtkinter as ctk
from tkinter import simpledialog
import hashlib
import sqlite3
import datetime
from markdown import markdown

# Initialize the database
def init_db():
    conn = sqlite3.connect('markdown_app.db')
    c = conn.cursor()
    # Create users table
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, password TEXT NOT NULL)''')
    # Create notes table
    c.execute('''CREATE TABLE IF NOT EXISTS notes
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT NOT NULL,
                  title TEXT NOT NULL,
                  content TEXT NOT NULL,
                  timestamp TEXT NOT NULL,
                  FOREIGN KEY (username) REFERENCES users(username) ON DELETE CASCADE)''')
    conn.commit()
    conn.close()

# Hash passwords
def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Main application class
class MarkdownAppGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Markdown Note App")
        self.root.geometry("1200x800")
        self.current_user = None

        # Initialize the database
        init_db()

        # Start with the login screen
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

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        hashed_password = hash_password(password)

        # Verify the user
        conn = sqlite3.connect('markdown_app.db')
        c = conn.cursor()
        c.execute("SELECT password FROM users WHERE username=?", (username,))
        result = c.fetchone()
        conn.close()

        if result and result[0] == hashed_password:
            self.current_user = username
            self.setup_main_screen()
        else:
            self.error_label.configure(text="Invalid username or password")

    def register(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        hashed_password = hash_password(password)

        # Add the user to the database
        conn = sqlite3.connect('markdown_app.db')
        c = conn.cursor()
        try:
            c.execute("INSERT INTO users (username, password) VALUES (?, ?)",
                      (username, hashed_password))
            conn.commit()
            self.error_label.configure(text="Registration successful", text_color="green")
        except sqlite3.IntegrityError:
            self.error_label.configure(text="Username already exists", text_color="red")
        conn.close()

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
        content = self.text_area.get("1.0", "end-1c")
        if not content.strip():
            self.error_label.configure(text="Cannot save an empty note")
            return

        title = simpledialog.askstring("Save Note", "Enter a title for your note:")
        if title:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            conn = sqlite3.connect('markdown_app.db')
            c = conn.cursor()
            c.execute("INSERT INTO notes (username, title, content, timestamp) VALUES (?, ?, ?, ?)",
                      (self.current_user, title, content, timestamp))
            conn.commit()
            conn.close()
            self.error_label.configure(text="Note saved successfully", text_color="green")

    def open_file(self):
        conn = sqlite3.connect('markdown_app.db')
        c = conn.cursor()
        c.execute("SELECT title, content FROM notes WHERE username=?", (self.current_user,))
        notes = c.fetchall()
        conn.close()

        if notes:
            note_titles = [note[0] for note in notes]
            selected_title = simpledialog.askstring("Open Note", "Enter the title of the note to open:",
                                                   initialvalue=note_titles[0])
            if selected_title:
                for note in notes:
                    if note[0] == selected_title:
                        self.text_area.delete("1.0", "end")
                        self.text_area.insert("1.0", note[1])
                        self.error_label.configure(text="Note loaded successfully", text_color="green")
                        break
        else:
            self.error_label.configure(text="No notes found", text_color="red")

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


# Run the application
if __name__ == "__main__":
    root = ctk.CTk()
    app = MarkdownAppGUI(root)
    root.mainloop()