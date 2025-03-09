# RMBS Prepayment and Cash Flow Analyzer 

- This Python tool models the cash flows of a Residential Mortgage-Backed Security (RMBS) based on a pool of mortgages.
- It incorporates a PSA (Public Securities Association) prepayment model to estimate early repayments, calculates monthly cash flows, and allocates them to senior and junior tranches.
- A GUI enables users to input mortgage pool parameters and visualize cash flows over time.

![Uploading output.png…]()

---

## Files
- `rmbs_analyzer.py`: Main script for modeling RMBS cash flows and displaying an interactive GUI with a cash flow plot.
- `output.png`: Plot.

---

## Libraries Used
- `numpy`
- `pandas`
- `tkinter`
- `matplotlib`
- `matplotlib.backends.backend_tkagg`

---

## Features
- **Input**: Users enter pool size ($M), interest rate (%), term (months), and PSA prepayment speed (%) via a GUI.
- **Prepayment Model**: Implements PSA prepayment speed to calculate monthly Single Monthly Mortality (SMM) rates based on CPR.
- **Cash Flow Calculation**: Computes principal, interest, and prepayments, then splits cash flows into senior (80%) and junior (20%) tranches.
- **Visualization**: Displays a real-time plot of total, senior, and junior tranche cash flows (in $M) over time.
- **Metrics**: Shows the total cash flow across the pool’s life.

