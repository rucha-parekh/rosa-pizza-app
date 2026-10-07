import numpy as np
import streamlit as st

from starter import ZONES, TIME_BLOCKS, COSTS, delivery_times


# ---------------------------------------------------------------------------
# Logic copied unchanged from rosa_analysis.ipynb (Part II (a) and Part II (b))
# ---------------------------------------------------------------------------

def cost_per_late_order(costs):
    """Total cost of one late order: the refund plus the profit lost from future orders."""
    return costs['refund'] + costs['churn_orders'] * costs['margin']


def net_profit(zone, time_block, promise, costs, seed=1):
    """Net profit for one zone, time block and promise.

    Returns (net_profit, number_of_orders, number_of_late_orders).
    """
    times = delivery_times(zone, time_block, promise, seed=seed)
    orders = len(times)
    late = int(np.sum(times > promise))
    profit = orders * costs['margin'] - late * cost_per_late_order(costs)
    return profit, orders, late


def best_promise(zone, time_block, promises, costs, seed=1):
    """Try every promise in `promises` and return the one with the highest net profit.

    Returns (best_promise, best_net_profit, results), where results is a list of
    (promise, orders, late_orders, net_profit) tuples, one per promise tried.
    """
    promises = sorted(promises)
    results = []
    best_p = None
    best_profit = None
    for promise in promises:
        profit, orders, late = net_profit(zone, time_block, promise, costs, seed=seed)
        results.append((promise, orders, late, profit))
        if best_profit is None or profit > best_profit:
            best_p = promise
            best_profit = profit

    if len(promises) > 1 and best_p in (promises[0], promises[-1]):
        print(f"Warning: the best promise ({best_p} min) is at the edge of the range "
              f"{promises[0]}-{promises[-1]} min; consider widening the range.")

    return best_p, best_profit, results


# ---------------------------------------------------------------------------
# Streamlit app
# ---------------------------------------------------------------------------

TODAY_PROMISE = 45


def money(x):
    """Format a dollar amount, putting the minus sign before the $ sign."""
    return f"-${-x:,.2f}" if x < 0 else f"${x:,.2f}"


st.set_page_config(page_title="Rosa's Pizza: Best Delivery Promise", page_icon="🍕")
st.title("🍕 Rosa's Pizza: Best Delivery Promise")
st.write(
    "Pick a zone and a time block, set the promises to try and the cost figures, "
    "then click the button to find the promised delivery time with the highest net profit "
    "(over four weeks of orders)."
)

with st.sidebar:
    st.header("Where and when")
    zone = st.selectbox("Zone", ZONES, index=ZONES.index("Far West"))
    time_block = st.selectbox("Time block", TIME_BLOCKS, index=TIME_BLOCKS.index("Fri/Sat eve"))

    st.header("Promises to try (minutes)")
    low, high = st.slider("Shortest and longest promise", min_value=5, max_value=150,
                          value=(20, 100), step=1)
    step = st.number_input("Step size", min_value=1, max_value=30, value=5, step=1)

    st.header("Costs")
    margin = st.number_input("Profit margin per order ($)", min_value=0.0,
                             value=float(COSTS['margin']), step=0.5)
    churn = st.number_input("Lost future orders per late order (churn)", min_value=0.0,
                            value=float(COSTS['churn_orders']), step=0.1)
    refund = st.number_input("Refund per late order ($)", min_value=0.0,
                             value=float(COSTS['refund']), step=1.0)

promises = list(range(low, high + 1, int(step)))
costs = {'refund': refund, 'churn_orders': churn, 'margin': margin}

st.caption(f"Promises to try: {promises[0]} to {promises[-1]} minutes in steps of {int(step)} "
           f"({len(promises)} promises).")

if st.button("Find the best promise", type="primary"):
    best_p, best_profit, results = best_promise(zone, time_block, promises, costs)
    profit_today, orders_today, late_today = net_profit(zone, time_block, TODAY_PROMISE, costs)

    st.subheader(f"Recommendation for {zone}, {time_block}")
    col1, col2, col3 = st.columns(3)
    col1.metric("Recommended promise", f"{best_p} min")
    col2.metric("Net profit", money(best_profit),
                delta=f"{money(best_profit - profit_today)} vs {TODAY_PROMISE} min")
    col3.metric("Cost per late order", money(cost_per_late_order(costs)))

    st.write(
        f"With today's {TODAY_PROMISE}-minute promise, this zone and time block would make "
        f"**{money(profit_today)}** ({orders_today} orders, {late_today} late)."
    )

    if len(promises) > 1 and best_p in (promises[0], promises[-1]):
        st.warning(
            f"The best promise ({best_p} min) is at the edge of the range you tried "
            f"({promises[0]}–{promises[-1]} min). The true best may lie outside it, "
            "so try widening the range."
        )

    st.subheader("Every promise tried")
    table = []
    for promise, orders, late, profit in results:
        table.append({
            "Promise (min)": promise,
            "Orders": orders,
            "Late orders": late,
            "Late %": round(100 * late / orders, 1) if orders > 0 else 0.0,
            "Net profit ($)": round(profit, 2),
        })
    st.dataframe(table, hide_index=True, width='stretch')
