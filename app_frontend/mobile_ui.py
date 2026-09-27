import customtkinter as ctk
import random
from datetime import datetime
from core_backend.database import execute_topup
from etl_pipeline import run_etl_processing
from analytics import generate_spending_chart, predict_days_remaining

class DesktopApp:
    def __init__(self, root):
        self.root = root
        self.root.configure(fg_color="#120F26")

        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        # 🏦 LEFT SIDEBAR PANEL: Core Vending Console
        self.side_panel = ctk.CTkFrame(self.root, width=350, fg_color="#2A244E", corner_radius=20)
        self.side_panel.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")
        
        ctk.CTkLabel(self.side_panel, text="Secure Vending Console", font=("Arial", 22, "bold"), text_color="#FFFFFF").pack(pady=(30, 25))
        
        self.utility_var = ctk.StringVar(value="Gas")
        
        # 🔒 FIX: Cleaned up option label text strings to prevent radio icon clipping overlaps
        self.gas_radio = ctk.CTkRadioButton(self.side_panel, text="Gas Card (19-digit)", font=("Arial", 13), variable=self.utility_var, value="Gas", text_color="#FFFFFF")
        self.gas_radio.pack(pady=8)
        
        self.elec_radio = ctk.CTkRadioButton(self.side_panel, text="Electric Key (13-digit)", font=("Arial", 13), variable=self.utility_var, value="Electricity", text_color="#FFFFFF")
        self.elec_radio.pack(pady=8)
        
        self.card_entry = ctk.CTkEntry(self.side_panel, placeholder_text="Enter UK Token/Key Number", width=280, height=45)
        self.card_entry.pack(pady=20)
        
        self.amount_entry = ctk.CTkEntry(self.side_panel, placeholder_text="Top-Up Credit Amount (£)", width=280, height=45)
        self.amount_entry.insert(0, "20")
        self.amount_entry.pack(pady=10)

        self.pay_btn = ctk.CTkButton(self.side_panel, text="Authorize Grid Top-Up", command=self.do_pay, 
                                     fg_color="#5E35B1", hover_color="#4527A0", height=50, width=280, font=("Arial", 14, "bold"))
        self.pay_btn.pack(pady=25)
        
        self.status_label = ctk.CTkLabel(self.side_panel, text="", text_color="cyan", font=("Arial", 12))
        self.status_label.pack(pady=10)

        # 🏢 RIGHT MAIN PANEL: Unified UK Smart Meter Hub
        self.main_panel = ctk.CTkFrame(self.root, fg_color="transparent")
        self.main_panel.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        
        ctk.CTkLabel(self.main_panel, text="UK Smart Metering & Grid Infrastructure", font=("Arial", 24, "bold"), text_color="#FFFFFF").pack(anchor="w", pady=(10, 15))

        self.grid_frame = ctk.CTkFrame(self.main_panel, fg_color="#2A244E", corner_radius=20)
        self.grid_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # 🔒 FIX: Re-engineered layout grid with explicit padding formatting rules
        self.add_feature_button(0, 0, "⚡", "SMETS2 Electric", lambda: self.trigger_log_view("Electricity"))
        self.add_feature_button(0, 1, "🔥", "SMETS2 Gas", lambda: self.trigger_log_view("Gas"))
        self.add_feature_button(0, 2, "🖧", "DCC Network Log", lambda: self.trigger_log_view("DCC"))
        self.add_feature_button(0, 3, "📈", "Usage Forecasts", self.open_predictive_radar_window)
        
        self.add_feature_button(1, 0, "📱", "Mobile Top-Up", self.open_mobile_etl_window)
        self.add_feature_button(1, 1, "💳", "Payment Methods", lambda: self.trigger_log_view("Payments"))
        self.add_feature_button(1, 2, "📋", "Vending History", generate_spending_chart)
        self.add_feature_button(1, 3, "⚙", "Meter Diagnostics", lambda: self.trigger_log_view("Diagnostics"))

    def add_feature_button(self, row, col, icon, name, command_func):
        # 🔒 FIX: Added font layout scaling rules to ensure icons never overlap with card label texts
        btn = ctk.CTkButton(self.grid_frame, text=f"{icon}\n\n{name}", font=("Arial", 13, "bold"),
                            fg_color="#1E1A3A", hover_color="#231A4A", width=160, height=130, corner_radius=15, command=command_func)
        btn.grid(row=row, column=col, padx=20, pady=25)

    def open_predictive_radar_window(self):
        raw_val = self.amount_entry.get()
        current_wallet_balance = float(raw_val) if raw_val.replace('.', '', 1).isdigit() else 45.00
        
        prediction = predict_days_remaining(current_wallet_balance)

        popup = ctk.CTkToplevel(self.root)
        popup.title("Grid Forecasting System")
        popup.geometry("460x380")
        popup.configure(fg_color="#1E1A3A")
        popup.attributes("-topmost", True)

        ctk.CTkLabel(popup, text="📊 DATA SCIENCE PREDICTIVE RADAR", font=("Arial", 16, "bold"), text_color="cyan").pack(pady=20)
        
        metrics_frame = ctk.CTkFrame(popup, fg_color="#2A244E", corner_radius=15, width=400, height=220)
        metrics_frame.pack(padx=20, pady=10, fill="both", expand=True)
        metrics_frame.pack_propagate(False)

        ctk.CTkLabel(metrics_frame, text=f"Analyzed Prepayment Credit: £{current_wallet_balance:.2f}", font=("Arial", 13, "bold"), text_color="#FFFFFF").pack(pady=12)
        ctk.CTkLabel(metrics_frame, text=f"• Seasonally Adjusted Burn:  £{prediction['average_daily_burn_gbp']}/day", font=("Arial", 13), text_color="#B3B0CD").pack(anchor="w", padx=40, pady=6)
        ctk.CTkLabel(metrics_frame, text=f"• Estimated Utility Lifespan: {prediction['estimated_days_left']} Days", font=("Arial", 14, "bold"), text_color="orange").pack(anchor="w", padx=40, pady=6)
        ctk.CTkLabel(metrics_frame, text=f"• Predicted Outage Date:    {prediction['predicted_depletion_date']}", font=("Arial", 13, "bold"), text_color="red").pack(anchor="w", padx=40, pady=6)

        ctk.CTkButton(popup, text="Close Report Panel", command=popup.destroy, fg_color="#5E35B1").pack(pady=20)

    def open_mobile_etl_window(self):
        popup = ctk.CTkToplevel(self.root)
        popup.title("UK Mobile Data Quality Gate")
        popup.geometry("450x400")
        popup.configure(fg_color="#1E1A3A")
        popup.attributes("-topmost", True)

        ctk.CTkLabel(popup, text="UK Mobile Vending Ingestion Gate", font=("Arial", 16, "bold")).pack(pady=20)
        
        phone_entry = ctk.CTkEntry(popup, placeholder_text="Enter Mobile Number (e.g. 07123456789)", width=320, height=40)
        phone_entry.pack(pady=10)
        
        amount_entry = ctk.CTkEntry(popup, placeholder_text="Recharge Value (£)", width=320, height=40)
        amount_entry.insert(0, "15")
        amount_entry.pack(pady=10)

        output_label = ctk.CTkLabel(popup, text="Awaiting data entry submission...", text_color="grey")

        def execute_pipeline_run():
            phone = phone_entry.get()
            val = amount_entry.get()
            
            mock_payload = {
                "transaction_id": f"TXN-{random.randint(100000, 999999)}",
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "user_id": phone,
                "location": "Liverpool, UK",
                "device_type": "Desktop Console Client",
                "service_type": "Mobile",
                "supplier_name": "EE UK Network",
                "amount": float(val) if val.isdigit() else 10.0,
                "status": "Success"
            }
            
            passed_gate = run_etl_processing(mock_payload)
            if passed_gate:
                output_label.configure(text="✅ Approved & Loaded into analytics_warehouse.db", text_color="green")
            else:
                output_label.configure(text="❌ Quality Gate Rejection: Failed UK Validation Curve", text_color="red")

        ctk.CTkButton(popup, text="Submit Data Payload", command=execute_pipeline_run, fg_color="#5E35B1").pack(pady=20)
        output_label.pack(pady=10)

    def trigger_log_view(self, service_name):
        self.status_label.configure(text=f"Logs active for: {service_name}", text_color="cyan")

    def do_pay(self):
        card = self.card_entry.get()
        amt = self.amount_entry.get()
        utility = self.utility_var.get()
        
        if not card.isdigit():
            self.status_label.configure(text="❌ Error: Numeric characters only.", text_color="red")
            return
            
        if utility == "Gas" and len(card) != 19:
            self.status_label.configure(text="⚠️ Notice: Gas cards must contain 19 digits.", text_color="orange")
            return
        elif utility == "Electricity" and len(card) != 13:
            self.status_label.configure(text="⚠️ Notice: Electric keys must contain 13 digits.", text_color="orange")
            return

        res = execute_topup(card, amt)
        if res["success"]:
            self.status_label.configure(text=f"✅ Approved: {res['name']}\nBalance: £{res['new_balance']:.2f}", text_color="green")
        else:
            self.status_label.configure(text=f"❌ Rejected: {res['message']}", text_color="red")
