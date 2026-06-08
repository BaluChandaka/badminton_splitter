# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

A single-page Streamlit web app that splits badminton session expenses among participants with the fewest possible transactions (greedy debt-settlement algorithm).

## Running the App

```powershell
# Activate the virtual environment
.venv\Scripts\Activate.ps1

# Run the app (opens in browser at http://localhost:8501)
streamlit run app.py
```

No `requirements.txt` exists — the only runtime dependency is `streamlit` (1.58.0 installed in `.venv`).

## Architecture

Everything lives in `app.py` — there are no modules, helpers, or config files. The app follows a linear Streamlit flow:

1. **Input** — comma-separated names → dynamic `st.number_input` fields per participant
2. **Calculation** — total cost ÷ headcount gives equal share; net balance = paid − share
3. **Settlement** — greedy matching: iterates debtors against creditors, transferring `min(debt, credit)` until settled

The settlement loop mutates lists in place (`creditor[1] -= transfer`) rather than using immutable structures — keep that in mind when modifying the algorithm.
