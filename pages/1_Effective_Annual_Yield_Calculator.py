import streamlit as st

st.set_page_config(page_title="Effective Annual Yield Calculator")

st.title("Effective Annual Yield Calculator")

r"""
- [Real Estate Finance & Investments](https://www.amazon.com/Estate-Finance-Investments-McGraw-Hill-Insurance/dp/0073377333): Page 46

$FV = PV ( 1 + \frac{i}{m})^{n \cdot m}$

where

- $n$ = years
- $i$ = annual interest rate
- $PV$ = present value
- $FV$ = future value
"""

interval_map = {
    "Annually": 1,
    "Semiannually": 2,
    "Quarterly": 4,
    "Monthly": 12,
    "Daily": 365,
}

# Initial results
fv = None
eay = None

with_pv = st.checkbox("With Present Value")

with st.form("EffectiveAnnualYield"):
    # Present Value
    if with_pv:
        pv = st.number_input(
            "Present Value", min_value=0, value=200000, disabled=not with_pv
        )
    else:
        pv = 1

    i = (
        st.number_input(
            "Nominal Annual Interest Rate",
            min_value=0,
            max_value=100,
            value=3,
        )
        / 100
    )

    compounding_interval = st.selectbox(
        "Compounding Interval", interval_map.keys(), index=3
    )
    m = interval_map[compounding_interval]

    if submit := st.form_submit_button("Calculate"):
        fv = pv * (1 + i / m) ** (m)
        eay = (fv - pv) / pv

    if with_pv:
        st.metric("Future Value", fv)
    st.metric(
        "Effective Annual Yield (EAY) (%)", eay * 100 if eay is not None else None
    )
    st.caption("Note. EAY also known as Annual Percentage Yield (APY)")
