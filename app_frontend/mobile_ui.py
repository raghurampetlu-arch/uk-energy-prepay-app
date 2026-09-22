import flet as ft
import sqlite3
import random

def build_mobile_screen(page: ft.Page):
    page.title = "PocketPay UK"
    page.window_width = 390
    page.window_height = 844
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = ft.ScrollMode.AUTO

    # Form components
    utility_toggle = ft.RadioGroup(content=ft.Row([
        ft.Radio(value="Gas", label="🔥 Gas Card"),
        ft.Radio(value="Electricity", label="⚡ Electric Key")
    ], alignment=ft.MainAxisAlignment.CENTER))
    utility_toggle.value = "Gas"

    account_input = ft.TextField(label="UK Card/Key Number", border_radius=10, keyboard_type=ft.KeyboardType.NUMBER)
    amount_input = ft.TextField(label="Top-Up Amount (£)", value="20", prefix_text="£ ", border_radius=10)
    status_box = ft.Column(spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER)

    def trigger_payment(e):
        status_box.controls.clear()
        raw_card = "".join(account_input.value.split())
        
        if not raw_card.isdigit():
            status_box.controls.append(ft.Text("❌ Numbers only.", color=ft.colors.RED))
            page.update()
            return
            
        # Mock payment layout for visual update
        status_box.controls.extend([
            ft.Icon(name=ft.icons.CHECK_CIRCLE, color=ft.colors.GREEN, size=40),
            ft.Text("Top-Up Processing...", weight=ft.FontWeight.BOLD),
            ft.Text(f"Amount Sent: £{amount_input.value}")
        ])
        page.update()

    pay_button = ft.ElevatedButton("Process Top-Up", width=300, height=45, on_click=trigger_payment)

    page.add(
        ft.Container(content=ft.Text("PocketPay", size=24, color=ft.colors.BLUE_700, weight=ft.FontWeight.BOLD), padding=20),
        ft.Card(content=ft.Container(content=ft.Column([utility_toggle, account_input, amount_input, pay_button]), padding=20)),
        status_box
    )