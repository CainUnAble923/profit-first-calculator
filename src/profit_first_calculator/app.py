# print("DEBUG: importing app.py from:", __file__)
# print("DEBUG: starting app.py import...")

import json
import os
import tkinter as tk
from tkinter import ttk, messagebox
from dataclasses import dataclass, asdict

def get_settings_path():
    appdata = os.getenv("APPDATA")
    app_folder = os.path.join(appdata, "ProfitFirstCalculator")
    os.makedirs(app_folder, exist_ok=True)
    return os.path.join(app_folder, "profit_first_defaults.json")

APP_DEFAULTS_FILE = get_settings_path()


# ---------------- SETTINGS ----------------
@dataclass
class Settings:
    # Profit First defaults (editable + saved)
    pf_profit_percent: float = 5.0
    pf_owner_pay_percent: float = 50.0
    pf_income_tax_percent: float = 15.0
    pf_opex_percent: float = 30.0

    # Behavior toggles
    back_out_processing_fees: bool = True
    back_out_sales_tax_before_pf: bool = True

    # Sales tax is now a manual amount (user enters from report)
    sales_tax_amount: float = 0.0


# ---------------- HELPERS ----------------
def money(x: float) -> str:
    return f"${x:,.2f}"


def safe_float(s) -> float:
    s = str(s).replace("$", "").replace(",", "").strip()
    if s == "":
        return 0.0
    return float(s)


def load_settings() -> Settings:
    if not os.path.exists(APP_DEFAULTS_FILE):
        return Settings()
    try:
        with open(APP_DEFAULTS_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return Settings(**data)
    except Exception:
        return Settings()


def save_settings(s: Settings) -> None:
    with open(APP_DEFAULTS_FILE, "w", encoding="utf-8") as f:
        json.dump(asdict(s), f, indent=2)


# ---------------- MAIN APP ----------------
# print("DEBUG: about to define ProfitFirstApp")
class ProfitFirstApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Profit First + Sales Tax Calculator")
        self.geometry("940x700")
        self.minsize(940, 700)

        self.settings = load_settings()

        self._build_ui()
        self._apply_settings_to_ui()
        self.calculate()  # initial calc

    # ---------------- UI ----------------
    def _build_ui(self):
        pad = {"padx": 10, "pady": 6}

        # Deposit Inputs
        inputs = ttk.LabelFrame(self, text="Deposit Inputs")
        inputs.pack(fill="x", padx=12, pady=10)

        ttk.Label(inputs, text="Estimated bank deposit (amount that hit the bank):").grid(row=0, column=0, sticky="w", **pad)
        self.deposit_var = tk.StringVar(value="0.00")
        ttk.Entry(inputs, textvariable=self.deposit_var, width=18).grid(row=0, column=1, sticky="w", **pad)

        ttk.Label(inputs, text="Processing fees (optional):").grid(row=1, column=0, sticky="w", **pad)
        self.fees_var = tk.StringVar(value="0.00")
        ttk.Entry(inputs, textvariable=self.fees_var, width=18).grid(row=1, column=1, sticky="w", **pad)

        ttk.Label(inputs, text="Sales tax amount (from your report):").grid(row=2, column=0, sticky="w", **pad)
        self.sales_tax_amount_var = tk.StringVar(value="0.00")
        ttk.Entry(inputs, textvariable=self.sales_tax_amount_var, width=18).grid(row=2, column=1, sticky="w", **pad)

        # Toggles
        self.backout_fees_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            inputs,
            text="Back out processing fees before PF base (optional)",
            variable=self.backout_fees_var
        ).grid(row=0, column=2, columnspan=2, sticky="w", padx=12, pady=6)

        self.backout_sales_tax_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(
            inputs,
            text="Back out SALES TAX amount before Profit First allocations (recommended)",
            variable=self.backout_sales_tax_var
        ).grid(row=1, column=2, columnspan=2, sticky="w", padx=12, pady=6)

        # Actions row (always visible)
        actions = ttk.Frame(inputs)
        actions.grid(row=3, column=0, columnspan=4, sticky="ew", padx=10, pady=(8, 10))
        for i in range(4):
            actions.grid_columnconfigure(i, weight=1)

        ttk.Button(actions, text="Calculate", command=self.calculate).grid(row=0, column=0, sticky="ew", padx=6)
        ttk.Button(actions, text="Clear Inputs", command=self._clear_inputs).grid(row=0, column=1, sticky="ew", padx=6)
        ttk.Button(actions, text="Copy Summary", command=self._copy_summary).grid(row=0, column=2, sticky="ew", padx=6)
        ttk.Button(actions, text="Exit", command=self.destroy).grid(row=0, column=3, sticky="ew", padx=6)

        inputs.grid_columnconfigure(0, weight=1)
        inputs.grid_columnconfigure(1, weight=0)
        inputs.grid_columnconfigure(2, weight=1)
        inputs.grid_columnconfigure(3, weight=0)

        # Profit First Percentages
        pf = ttk.LabelFrame(self, text="Profit First Percentages (must total 100%)")
        pf.pack(fill="x", padx=12, pady=6)

        self.pf_profit_var = tk.StringVar(value="5")
        self.pf_owner_var = tk.StringVar(value="50")
        self.pf_income_tax_var = tk.StringVar(value="15")
        self.pf_opex_var = tk.StringVar(value="30")

        ttk.Label(pf, text="Profit %").grid(row=0, column=0, sticky="w", **pad)
        ttk.Entry(pf, textvariable=self.pf_profit_var, width=10).grid(row=0, column=1, sticky="w", **pad)

        ttk.Label(pf, text="Owner Pay %").grid(row=0, column=2, sticky="w", **pad)
        ttk.Entry(pf, textvariable=self.pf_owner_var, width=10).grid(row=0, column=3, sticky="w", **pad)

        ttk.Label(pf, text="Income Tax %").grid(row=1, column=0, sticky="w", **pad)
        ttk.Entry(pf, textvariable=self.pf_income_tax_var, width=10).grid(row=1, column=1, sticky="w", **pad)

        ttk.Label(pf, text="Opex %").grid(row=1, column=2, sticky="w", **pad)
        ttk.Entry(pf, textvariable=self.pf_opex_var, width=10).grid(row=1, column=3, sticky="w", **pad)

        ttk.Button(pf, text="Save as New Defaults", command=self._save_defaults_from_ui).grid(row=0, column=4, rowspan=2, sticky="ns", padx=12, pady=6)
        ttk.Button(pf, text="Reset to Starter Defaults", command=self._reset_to_starter_defaults).grid(row=0, column=5, rowspan=2, sticky="ns", padx=6, pady=6)

        # Results
        out = ttk.LabelFrame(self, text="Results")
        out.pack(fill="both", expand=True, padx=12, pady=10)

        self.results = tk.Text(out, height=18, wrap="word")
        self.results.pack(fill="both", expand=True, padx=10, pady=10)
        self.results.configure(font=("Consolas", 11))

    def _apply_settings_to_ui(self):
        s = self.settings
        self.pf_profit_var.set(str(s.pf_profit_percent))
        self.pf_owner_var.set(str(s.pf_owner_pay_percent))
        self.pf_income_tax_var.set(str(s.pf_income_tax_percent))
        self.pf_opex_var.set(str(s.pf_opex_percent))

        self.backout_fees_var.set(bool(s.back_out_processing_fees))
        self.backout_sales_tax_var.set(bool(s.back_out_sales_tax_before_pf))

        self.sales_tax_amount_var.set(str(s.sales_tax_amount))

    def _clear_inputs(self):
        self.deposit_var.set("0.00")
        self.fees_var.set("0.00")
        self.sales_tax_amount_var.set(str(self.settings.sales_tax_amount))
        self.calculate()

    def _reset_to_starter_defaults(self):
        self.settings = Settings()
        save_settings(self.settings)
        self._apply_settings_to_ui()
        self.calculate()
        messagebox.showinfo("Defaults reset", "Starter defaults restored and saved.")

    def _copy_summary(self):
        text = self.results.get("1.0", "end").strip()
        self.clipboard_clear()
        self.clipboard_append(text)
        messagebox.showinfo("Copied", "Summary copied to clipboard.")

    def _save_defaults_from_ui(self):
        try:
            s = Settings(
                pf_profit_percent=safe_float(self.pf_profit_var.get()),
                pf_owner_pay_percent=safe_float(self.pf_owner_var.get()),
                pf_income_tax_percent=safe_float(self.pf_income_tax_var.get()),
                pf_opex_percent=safe_float(self.pf_opex_var.get()),
                back_out_processing_fees=bool(self.backout_fees_var.get()),
                back_out_sales_tax_before_pf=bool(self.backout_sales_tax_var.get()),
                sales_tax_amount=safe_float(self.sales_tax_amount_var.get()),
            )

            total_pct = s.pf_profit_percent + s.pf_owner_pay_percent + s.pf_income_tax_percent + s.pf_opex_percent
            if abs(total_pct - 100.0) > 0.01:
                raise ValueError(f"Profit First percentages must total 100%. Yours total {total_pct:.2f}%.")

            save_settings(s)
            self.settings = s
            messagebox.showinfo("Saved", f"New defaults saved to:\n{os.path.abspath(APP_DEFAULTS_FILE)}")
        except Exception as e:
            messagebox.showerror("Save error", str(e))

    # ---------------- CALCULATION ----------------
    def calculate(self):
        try:
            deposit = safe_float(self.deposit_var.get())
            fees = safe_float(self.fees_var.get())
            sales_tax_hold = safe_float(self.sales_tax_amount_var.get())

            profit_pct = safe_float(self.pf_profit_var.get())
            owner_pct = safe_float(self.pf_owner_var.get())
            income_tax_pct = safe_float(self.pf_income_tax_var.get())
            opex_pct = safe_float(self.pf_opex_var.get())

            if deposit < 0 or fees < 0 or sales_tax_hold < 0:
                raise ValueError("Deposit, fees, and sales tax amount must be >= 0.")

            # Step 1: net after fees (if toggled)
            net_used = (deposit - fees) if self.backout_fees_var.get() else deposit
            if net_used < 0:
                net_used = 0.0

            # Step 2: PF base (optionally back out sales tax amount)
            if self.backout_sales_tax_var.get():
                pf_base = net_used - sales_tax_hold
            else:
                pf_base = net_used

            if pf_base < 0:
                raise ValueError(
                    f"Sales tax amount ({money(sales_tax_hold)}) is greater than Net Used ({money(net_used)})."
                )

            # Step 3: enforce PF % = 100
            total_pct = profit_pct + owner_pct + income_tax_pct + opex_pct
            if abs(total_pct - 100.0) > 0.01:
                raise ValueError(f"Profit First percentages must total 100%. Yours total {total_pct:.2f}%.")

            # Step 4: allocations FROM PF BASE ONLY
            profit_amt = pf_base * (profit_pct / 100.0)
            owner_amt = pf_base * (owner_pct / 100.0)
            income_tax_amt = pf_base * (income_tax_pct / 100.0)  # income tax ONLY
            opex_amt = pf_base * (opex_pct / 100.0)

            pf_total = profit_amt + owner_amt + income_tax_amt + opex_amt

            # Output
            lines = []
            lines.append("PROFIT FIRST ALLOCATION")
            lines.append("=" * 30)
            lines.append("")
            lines.append(f"Deposit: {money(deposit)}")

            if self.backout_fees_var.get():
                lines.append(f"Fees Removed: {money(fees)}")
                lines.append(f"Net Used (after fees): {money(net_used)}")
            else:
                lines.append("Fees NOT removed (treated as Opex expense).")
                lines.append(f"Net Used: {money(net_used)}")

            lines.append(f"Sales Tax Hold (MANUAL, separate): {money(sales_tax_hold)}")
            lines.append(f"PF Base Used: {money(pf_base)}")
            lines.append("")
            lines.append("MOVE MONEY TO ACCOUNTS (from PF Base):")
            lines.append("-" * 30)
            lines.append(f"Profit Account: {money(profit_amt)}")
            lines.append(f"Owner Pay: {money(owner_amt)}")
            lines.append(f"Tax Account (INCOME tax): {money(income_tax_amt)}")
            lines.append(f"Operating Expenses: {money(opex_amt)}")
            lines.append("")
            lines.append("CHECKS:")
            lines.append("-" * 30)
            lines.append(f"PF allocations total: {money(pf_total)} (should equal PF Base)")
            lines.append(f"PF Base + Sales Tax Hold: {money(pf_base + sales_tax_hold)} (should equal Net Used)")

            self.results.delete("1.0", tk.END)
            self.results.insert("1.0", "\n".join(lines))

        except Exception as e:
            messagebox.showerror("Error", str(e))


# ---------------- RUN ----------------
if __name__ == "__main__":
    app = ProfitFirstApp()
    app.mainloop()