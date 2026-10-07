---
name: notebook-to-streamlit
description: Port the decision logic from rosa_analysis.ipynb into the Streamlit app (app.py) for Rosa's Pizza, keeping the notebook functions unchanged and building the UI the assignment requires. Use when creating or updating app.py from the notebook.
---

# notebook-to-streamlit

Turn the analysis in `rosa_analysis.ipynb` into a Streamlit web app (`app.py`) that helps Rosa choose the best promised delivery time for one zone and time block.

## 1. Find the logic to reuse

Open `rosa_analysis.ipynb` and locate the Part II functions. These are the only functions the app needs:

| Function | Notebook section | What it does |
|---|---|---|
| `cost_per_late_order(costs)` | Part II (a) | refund + churn_orders × margin |
| `net_profit(zone, time_block, promise, costs, seed=1)` | Part II (b) | returns `(profit, orders, late)` for one promise |
| `best_promise(zone, time_block, promises, costs, seed=1)` | Part II (b) | returns `(best_promise, best_profit, results)`; `results` is a list of `(promise, orders, late, profit)` |

Part I functions (`late_percentage`, `average_delivery_time`) and exploration and printing cells are not ported.

## 2. Copy the functions faithfully

- Copy the function bodies **exactly as they are in the notebook**, including `seed=1` defaults and docstrings. Do not rewrite or "improve" the logic. The app must give the same answer as the notebook for the same inputs.
- Import the given data from the starter package. Never redefine it:
  `from starter import ZONES, TIME_BLOCKS, COSTS, delivery_times`
- Keep the core logic to plain Python and NumPy, as the assignment allows.
- `best_promise` uses `print()` for its edge-of-range warning. In the app that text only goes to the server log, so the app must check the edge itself and show `st.warning(...)` (see step 3). The function stays unchanged.
- At the top of the copied block, add a comment saying that the functions are copied from the notebook, naming the sections.

## 3. Build the UI the assignment requires

All inputs go in the sidebar, and results go in the main area.

1. **Dropdowns** (`st.selectbox`) for the zone (options `ZONES`) and the time block (options `TIME_BLOCKS`). Always use the starter lists as options; names are case-sensitive.
2. **Range of promises to try:** a range slider (`st.slider` with a `(low, high)` tuple value) for the shortest and longest promise, plus a step size input. Default to the range chosen in the notebook: **20 to 100 minutes, step 5**. Build the list with `list(range(low, high + 1, step))`.
3. **Cost inputs** (`st.number_input`): profit margin per order, churn (lost future orders) per late order, and refund per late order. Use `COSTS['margin']`, `COSTS['churn_orders']` and `COSTS['refund']` as the defaults. Build a dict with the same keys as `COSTS` and pass it to `best_promise`.
4. **A button** (`st.button`). Only run the search and show results after the button is clicked.
5. **Results** after the click:
   - The recommended promise and its net profit (`st.metric`), plus the cost per late order.
   - A comparison with today's 45-minute promise for the same pair, using `net_profit`.
   - `st.warning` if the best promise is the first or last value of the range ("widen the range").
   - A table of every promise tried: promise, orders, late orders, late %, net profit.

## 4. Check

- `requirements.txt` must contain `streamlit`, `numpy` and `git+https://github.com/zhouy185/rosa-starter.git` so Streamlit Community Cloud can install the starter.
- Run `.venv/Scripts/streamlit run app.py` and confirm that the defaults (Far West, Fri/Sat eve, 20–100 step 5, default costs) recommend the same promise and net profit as the notebook's Part II(b) test (55 minutes, $1,212.40).
- The app must not contain personal information, because the repository may be public.
