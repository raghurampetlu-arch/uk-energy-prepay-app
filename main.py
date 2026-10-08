import os
import customtkinter as ctk
from core_backend.database import initialize_database
from app_frontend.mobile_ui import DesktopApp

if __name__ == "__main__":
    # 1. Initialize local SQLite tables schema
    initialize_database()
    
    # 2. Setup Master Desktop Window
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("blue")
    
    root = ctk.CTk()
    root.title("PocketPay UK - Desktop Console")
    root.geometry("1100x700")
    
    # 🔒 FIX: Configured absolute system mapping path rules
    # This prevents directory drops if launched from an outside environment layer.
    base_dir = r"C:\GitHub\uk-energy-prepay-app"
    icon_path = os.path.join(base_dir, "pp.ico")
    
    if os.path.exists(icon_path):
        root.iconbitmap(icon_path)
        print(f"[SYSTEM]: Successfully linked asset icon layer from: {icon_path}")
    else:
        print(f"[SYSTEM WARNING]: Icon file not found at '{icon_path}'.")
        print("Please ensure your 'pp.ico' file is saved inside that exact folder.")
    
    # 3. Load UI Canvas Layers
    app = DesktopApp(root)
    
    print("[SYSTEM]: Desktop Dashboard active (Native Rendering)")
    root.mainloop()
