# Profit First Calculator (Desktop App)

A simple Windows desktop application that calculates **Profit First allocations from real bank deposits** while correctly separating sales tax and optional processing fees.

This tool is designed for small business owners who follow the Profit First method and are tired of guessing how much money they can safely move after deposits hit the bank.

---

## Why This Exists

Most bookkeeping systems show gross sales, but your bank receives:

- processor fees already removed
- sales tax mixed into deposits
- multiple transactions batched together

That makes Profit First allocations confusing and error-prone.

Many business owners accidentally allocate **sales-tax money as profit**.

This app solves that problem.

You enter what actually hit your bank account and the sales-tax amount from your report.  
The calculator determines the **true Profit First base** and tells you exactly what to move to each account.

---

## What the App Calculates

From a single bank deposit the program determines:

- Profit allocation
- Owner Pay allocation
- Income Tax reserve
- Operating Expense allocation
- Sales Tax Hold (separate from Profit First)

Your Profit First allocations will always total the **PF Base**, not the deposit.

---

## Features

- Desktop GUI (no browser or internet required)
- Manual sales-tax entry from POS/processor reports
- Optional processing fee back-out
- Saves your default percentages
- Prevents allocating tax money as profit
- One-click summary you can copy into bookkeeping notes

---

## How It Works

1. Enter the bank deposit amount
2. Enter processing fees (optional)
3. Enter the sales tax total from your report
4. Click **Calculate**

The program calculates:

PF Base = Deposit  
      − Processing Fees (optional)  
      − Sales Tax Amount

Then it allocates:

Profit  
Owner Pay  
Income Tax  
Operating Expenses

Sales tax is displayed separately so it can be transferred to a liability account.

---

## Example

Bank deposit: $50.82  
Sales tax report: $3.66  

PF Base: $47.16

The app then calculates allocations based on your saved percentages.

---

## Running From Source

Requires Python 3.10 or newer.

Run:

python src/main.py

If you cloned the repo but have no environment yet:

python -m venv .venv  
.venv\Scripts\activate  
python src/main.py

(Tkinter is included with normal Windows Python installs.)

---

## Building the Windows EXE

Install PyInstaller:

pip install pyinstaller

Build:

pyinstaller --noconsole --onefile --name "Profit First Calculator" src/main.py

The executable will appear in:

dist/

---

## Intended Users

This tool is especially useful for:

- Etsy / Shopify sellers
- craft businesses
- service businesses
- side hustles
- small retail shops
- anyone using the Profit First method manually

---

## Important Note

This application is a calculation aid only and does not replace bookkeeping or accounting advice.  
Always confirm your accounting practices with a qualified accountant or tax professional.

---

## License

This project is licensed under the MIT License.

You are free to use, modify, and distribute this software.

---

## Author

Created by Chase Fleming

---

## Future Ideas

- CSV deposit import
- QuickBooks/Wave helper export
- macOS build
- allocation history tracking