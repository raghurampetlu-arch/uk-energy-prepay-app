import customtkinter as ctk
from core_backend.database import execute_topup

class DesktopApp:
    def __init__(self, root):
        self.root = root
        self.root.configure(fg_color="#120F26") # Deep Indigo

        # Main Layout: Sidebar and Content
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # LEFT PANEL: Top-Up Console
        self.side_panel = ctk.CTkFrame(self.root, width=350, fg_color="#2A244E", corner_radius=20)
        self.side_panel.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        ctk.CTkLabel(self.side_panel, text="Quick Top-Up", font=("Arial", 22, "bold")).pack(pady=30)
        
        self.card_entry = ctk.CTkEntry(self.side_panel, placeholder_text="Enter 19-digit Gas Card", width=280, height=45)
        self.card_entry.pack(pady=10)
        
        self.amount_entry = ctk.CTkEntry(self.side_panel, placeholder_text="Amount (£)", width=280, height=45)
        self.amount_entry.insert(0, "20")
        self.amount_entry.pack(pady=10)

        self.pay_btn = ctk.CTkButton(self.side_panel, text="Process Transaction", command=self.do_pay, 
                                     fg_color="#5E35B1", hover_color="#4527A0", height=50, width=280)
        self.pay_btn.pack(pady=30)
        
        self.status_label = ctk.CTkLabel(self.side_panel, text="", text_color="cyan")
        self.status_label.pack(pady=10)

        # RIGHT PANEL: PhonePe Style Grid
        self.main_panel = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_panel.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        ctk.CTkLabel(self.main_panel, text="Utility Services", font=("Arial", 24, "bold")).pack(anchor="w", pady=(0, 20))

        # Icon Grid
        self.grid_frame = ctk.CTkFrame(self.main_panel, fg_color="#2A244E", corner_radius=20)
        self.grid_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Mock Icons (Using text for compatibility)
        services = [("⚡", "Electric"), ("🔥", "Gas"), ("💧", "Water"), ("📱", "Mobile"), 
                    ("🏠", "Rent"), ("📡", "WiFi"), ("📺", "Cable"), ("🛡️", "Insurance")]
        
        for i, (icon, name) in enumerate(services):
            btn = ctk.CTkButton(self.grid_frame, text=f"{icon}\n{name}", font=("Arial", 14),
                                fg_color="#1E1A3A", width=140, height=120, corner_radius=15)
            btn.grid(row=i//4, column=i%4, padx=20, pady=20)

    def do_pay(self):
        card = self.card_entry.get()
        amt = self.amount_entry.get()
        res = execute_topup(card, amt)
        
        if res["success"]:
            self.status_label.configure(text=f"Success! New Balance: £{res['new_balance']}", text_color="green")
        else:
            self.status_label.configure(text="Error: Card not found", text_color="red")
