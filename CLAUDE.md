# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

MMGMT 722 (Data Analytics using Python) Assignment 1: "Finding the Best Delivery Promise for Rosa's Pizza". The full spec is the PDF in the repo root — read it before making structural decisions. Deliverables:

1. `rosa_analysis.ipynb` — Jupyter notebook for Part I (describe: late rate / average delivery time by zone × time block) and Part II (cost per late order; search for the profit-maximizing promise). Work must be explained in markdown cells, and the notebook must end with an AI-use appendix listing key prompts, plus links to the GitHub repo and the deployed Streamlit app.
2. `app.py`, a Streamlit app (Part III) that reuses the notebook's logic: dropdowns for zone and time block, inputs for the range of promises to try, inputs for margin / churn / refund, and a button that shows the recommended promise. Deployed to Streamlit Community Cloud.
3. A project skill at `.github/skills/notebook-to-streamlit/SKILL.md` that describes how to port notebook logic into the Streamlit app. The assignment requires explicitly invoking this skill when building the app.

Allowed tools per the spec: basic Python data structures, loops, functions, if/else, and NumPy. Avoid pulling in pandas or other analysis libraries for the core logic.

## Conventions

- Always pass `seed=1` to every `delivery_times(...)` call (notebook and app) so results are reproducible.
- In the notebook, always add markdown cells explaining each step: what is being computed and why before the code, and what the output means after it.

## Environment and commands

- Local venv in `.venv/` (Python 3.10, Windows). Use `.venv/Scripts/python` / `.venv/Scripts/pip`.
- Install deps: `.venv/Scripts/pip install -r requirements.txt`
- Run the app: `.venv/Scripts/streamlit run app.py`
- Execute the notebook headless (Bash): `PATH="$PWD/.venv/Scripts:$PATH" .venv/Scripts/jupyter nbconvert --to notebook --execute --inplace rosa_analysis.ipynb`. The venv's kernel.json launches bare `python`, so without the PATH prefix it picks up the system Python and fails with `No module named 'starter'`.
- `requirements.txt` is also what Streamlit Community Cloud installs, so it must keep the `git+https://github.com/zhouy185/rosa-starter.git` line.
- In the notebook, the first cell should install the starter (`%pip install -q git+https://github.com/zhouy185/rosa-starter.git`) so it also runs in Colab.

## The `starter` module (external, do not reimplement or edit)

Installed from the `rosa-starter` package, imported as `from starter import ZONES, TIME_BLOCKS, COSTS, PROMISE, delivery_times`. The spec forbids writing your own versions of these.

- `ZONES = ['Central', 'North', 'Far West']`
- `TIME_BLOCKS = ['Lunch', 'Weekday eve', 'Fri/Sat eve', 'Other']` (names are case-sensitive; loop over these lists rather than retyping)
- `COSTS = {'refund': 10.0, 'churn_orders': 1.8, 'margin': 9.0}`
- `PROMISE = 45` (minutes)
- `delivery_times(zone, time_block, promise=45, seed=None)` returns a NumPy array of delivery times (minutes) for every order over four weeks. It is a stochastic simulator: pass `seed=` for reproducible results. The array length is the order count.

Modelling points that drive the analysis:
- A longer promise reduces demand (fewer orders), and fewer orders make deliveries faster. So late rate and order count both depend on the promise, and the best-promise search must call `delivery_times` for each candidate promise rather than reusing a single array.
- An order is late when its delivery time exceeds the promise.
- "all" aggregation (Part I a/c) should pool the orders across the relevant zones/time blocks (concatenate the arrays), not average the per-cell percentages, because cells have different order counts.
- Cost per late order = refund + churn_orders × margin. Net profit for a promise = orders × margin − late_orders × cost per late order.
- The best-promise function's signature is fixed by the spec: `(zone, time_block, promises, costs)`. Keep it importable/copyable so the Streamlit app can reuse it unchanged.
