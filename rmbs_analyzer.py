import numpy as np
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

# Step 1: Define mortgage pool calculator class
class MortgagePool:
    def __init__(self, P, R, T, S):
        self.P = P
        self.R = R / 12  # Monthly rate
        self.T = T
        self.S = S / 100  # PSA speed as decimal
        self.ma = P * (self.R * (1 + self.R)**T) / ((1 + self.R)**T - 1)  # Monthly payment

# Step 2: Compute cash flows with prepayment
    def get_flows(self):
        X = np.arange(1, self.T + 1)
        B = self.P
        df = {'t': [], 'P': [], 'I': [], 'PP': [], 'CF': []}

        for x in X:
            C = min(0.06 * self.S * (x / 30), 0.06 * self.S) if x <= 30 else 0.06 * self.S  # CPR
            M = 1 - (1 - C)**(1/12)  # SMM

            I = B * self.R
            SP = self.ma - I
            PP = B * M if B > 0 else 0
            TP = min(SP + PP, B)

            df['t'].append(x)
            df['P'].append(TP)
            df['I'].append(I)
            df['PP'].append(PP)
            df['CF'].append(I + TP)

            B -= TP
            if B <= 0:
                break

        return pd.DataFrame(df)

# Step 3: Split cash flows into tranches
    def split_tranches(self, df):
        S = df['CF'] * 0.8  # Senior tranche (80%)
        J = df['CF'] * 0.2  # Junior tranche (20%)
        return pd.DataFrame({'Senior': S, 'Junior': J})

# Step 4: Update GUI with results
def update_plot():
    try:
        P = float(e1.get()) * 1e6  # Pool size in millions
        R = float(e2.get()) / 100  # Rate as decimal
        T = int(e3.get())  # Term in months
        S = float(e4.get())  # PSA speed

        # Step 5: Check input validity
        if P <= 0 or R <= 0 or T <= 0 or S <= 0:
            raise ValueError("All inputs must be positive")

        # Step 6: Run mortgage pool model
        mp = MortgagePool(P, R, T, S)
        df = mp.get_flows()
        tr = mp.split_tranches(df)

        # Step 7: Plot cash flows
        ax.clear()
        ax.stackplot(df['t'], tr['Senior'] / 1e6, tr['Junior'] / 1e6, 
                     labels=['Senior (80%)', 'Junior (20%)'], 
                     colors=['#4ECDC4', '#45B7D1'], alpha=0.8)
        ax.plot(df['t'], df['CF'] / 1e6, color='#FF6B6B', lw=1.5, label='Total CF', linestyle='--')
        ax.set_xlabel('Month', color='white')
        ax.set_ylabel('Cash Flow ($M)', color='white')
        ax.set_title('Mortgage Pool Cash Flows (PSA Prepayment)', color='white')
        ax.set_facecolor('#2B2B2B')
        fig.set_facecolor('#1E1E1E')
        ax.grid(True, ls='--', color='#555555', alpha=0.3)
        ax.legend(loc='upper right', facecolor='#333333', edgecolor='white', labelcolor='white')
        ax.tick_params(colors='white')
        ax.set_ylim(0, max(df['CF'].max() / 1e6, 1) * 1.2)
        canv.draw()

        # Step 8: Update total cash flow display
        Z = df['CF'].sum() / 1e6
        lbl.config(text=f"Total CF: ${Z:.2f}M")

    except ValueError as e:
        messagebox.showerror("Error", str(e))

# Step 9: Set up GUI window
root = tk.Tk()
root.title("Mortgage Pool Analyzer")
root.configure(bg='#1E1E1E')

frm = ttk.Frame(root, padding=10)
frm.pack()
frm.configure(style='Dark.TFrame')

# Step 10: Initialize plot canvas
fig, ax = plt.subplots(figsize=(7, 5))
canv = FigureCanvasTkAgg(fig, master=frm)
canv.get_tk_widget().pack(side=tk.LEFT)

# Step 11: Create input frame
pf = ttk.Frame(frm)
pf.pack(side=tk.RIGHT, padx=10)
pf.configure(style='Dark.TFrame')

# Step 12: Apply dark theme
style = ttk.Style()
style.theme_use('default')
style.configure('Dark.TFrame', background='#1E1E1E')
style.configure('Dark.TLabel', background='#1E1E1E', foreground='white')
style.configure('TButton', background='#333333', foreground='white')
style.configure('TEntry', fieldbackground='#333333', foreground='white')

# Step 13: Add input fields
ttk.Label(pf, text="Pool Size ($M):", style='Dark.TLabel').pack(pady=3)
e1 = ttk.Entry(pf); e1.pack(pady=3); e1.insert(0, "100")
ttk.Label(pf, text="Rate (%):", style='Dark.TLabel').pack(pady=3)
e2 = ttk.Entry(pf); e2.pack(pady=3); e2.insert(0, "4")
ttk.Label(pf, text="Term (Months):", style='Dark.TLabel').pack(pady=3)
e3 = ttk.Entry(pf); e3.pack(pady=3); e3.insert(0, "360")
ttk.Label(pf, text="PSA Speed (%):", style='Dark.TLabel').pack(pady=3)
e4 = ttk.Entry(pf); e4.pack(pady=3); e4.insert(0, "100")

# Step 14: Add button and result label
ttk.Button(pf, text="Calculate", command=update_plot).pack(pady=10)
lbl = ttk.Label(pf, text="Total CF: ", style='Dark.TLabel'); lbl.pack(pady=2)

# Step 15: Run initial calculation
update_plot()
root.mainloop()
