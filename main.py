import customtkinter as ctk
from core_backend.database import initialize_database
from app_frontend.mobile_ui import DesktopApp

if __name__ == "__main__":
    # 1. Initialize DB
    initialize_database()
    
    # 2. Setup Window
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    root = ctk.CTk()
    root.title("PocketPay UK - Desktop Console")
    root.geometry("1100x700")
    
    # 3. Load UI
    app = DesktopApp(root)
    
    print("[SYSTEM]: Desktop Dashboard active (Native Rendering)")
    root.mainloop()
