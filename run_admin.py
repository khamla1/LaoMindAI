
import tkinter as tk
from src.ui_admin import AdminApp

if __name__ == "__main__":
    try:
        root = tk.Tk()
        app = AdminApp(root)
        root.mainloop()
    except Exception as e:
        print(f"Error: {e}")
        input("Press Enter to close...")
