import customtkinter as ctk
from AppGUI import MarkdownAppGUI

if __name__ == "__main__":
    root = ctk.CTk()
    app = MarkdownAppGUI(root)
    root.mainloop()