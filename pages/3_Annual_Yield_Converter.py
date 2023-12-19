from typing import Literal
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import numpy_financial as npf

st.set_page_config(page_title="Annual Yield Converter")

st.title("Annual Yield To Any Period Converter")


def annualized_rate_of_return(
    profit: float = None,
    capital: float = None,
    ratio: float = None,
    period: float = None,
) -> float:
    assert period is not None
    if ratio is None:
        assert profit is not None and capital is not None
        ratio = profit / capital
    return ratio * 365 / period


with st.form("ToAnnualYieldByProfit"):
    st.subheader("Convert using Profit")
    st.caption("NOTE: currently this value is approximate")
    capital = st.number_input("Capital", min_value=0.0, value=100000.0)
    profit = st.number_input("Profit", min_value=0.0, value=1000.0)
    period = st.number_input("Days", min_value=1, value=30)
    if submit := st.form_submit_button("Calculate"):
        st.metric(
            "Annualized Rate of Return (%)",
            annualized_rate_of_return(profit=profit, capital=capital, period=period)
            * 100,
        )


with st.form("ToAnnualYieldByRatio"):
    st.subheader("Convert using Profit Ratio")
    st.caption("NOTE: currently this value is approximate")
    capital2 = st.number_input("Capital", min_value=0.0, value=100000.0)
    ratio2 = st.number_input("Profit Ratio (%)", min_value=0.0, value=1.0)
    period2 = st.number_input("Days", min_value=1, value=30)
    if submit2 := st.form_submit_button("Calculate"):
        st.metric(
            "Annualized Rate of Return (%)",
            annualized_rate_of_return(
                capital=capital2, ratio=ratio2 / 100, period=period2
            )
            * 100,
        )

with st.form("AnnualYieldToOtherPeriod"):
    st.subheader("Convert Annual Yield To Other Periods")
    capital3 = st.number_input("Capital", min_value=0.0, value=100000.0)
    arr = st.number_input("Annualized Rate of Return (%)", min_value=0.0, value=3.880)
    period3 = st.number_input("New Period in Days", min_value=1, value=14)
    if submit3 := st.form_submit_button("Calculate"):
        new_rate = (1 + arr / 100) ** (period3 / 365) - 1
        st.metric("Total Profit Rate (%)", new_rate * 100)
        st.metric("Total Profit", new_rate * capital3)
