from typing import Literal
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Monthly Payment Calculator")

st.title("Monthly Payment Calculator")

# Initial results
monthly_interest = None
monthly_principal = None
monthly_payment = None
cash_flow = pd.DataFrame()


with st.form("MonthlyPaymentCalculator"):
    loan_type: Literal["Equal Principal and Interest Loan"] = st.selectbox(
        "Loan Type", ["Equal Principal and Interest Loan"]
    )
    present_value = st.number_input(
        "Loan Principal (Total Amount) [Present Value]", min_value=0, value=188445
    )

    nominal_interest_rate = (
        st.number_input(
            "Nominal Annual Interest Rate",
            min_value=0,
            max_value=100,
            value=3,
        )
        / 100
    )

    period = st.number_input(
        "Total Period (months) [# of compounding periods]", min_value=1, value=60
    )

    monthly_interest_rate = nominal_interest_rate / 12

    if submit := st.form_submit_button("Calculate"):
        if loan_type == "Equal Principal and Interest Loan":
            monthly_interest = monthly_interest_rate * present_value
            monthly_principal = present_value / period
            monthly_payment = monthly_principal + monthly_interest
            # https://numpy.org/numpy-financial/latest/pmt.html

            cash_flow = pd.DataFrame(
                {
                    "period": list(range(1, period + 1)),
                    "monthly_payment": [monthly_payment] * period,
                    "monthly_principal": [monthly_principal] * period,
                    "monthly_interest": [monthly_interest] * period,
                }
            )

            cash_flow["money_paid"] = cash_flow["monthly_payment"].cumsum().fillna(0)
            cash_flow["principal_returned"] = (
                cash_flow["monthly_principal"].cumsum().fillna(0)
            )
            cash_flow["principal_left"] = (
                present_value - cash_flow["principal_returned"]
            )


if loan_type == "Equal Principal and Interest Loan":
    st.metric("Monthly Principal", monthly_principal)
    col1, col2 = st.columns(2)
    col1.metric("Monthly Interest", monthly_interest)
    col2.metric(
        "Monthly Interest Rate (%)",
        monthly_interest_rate * 100 if monthly_interest_rate is not None else None,
    )
st.metric("Monthly Payment", monthly_payment)
if not cash_flow.empty:
    st.dataframe(cash_flow, hide_index=True)
    fig, ax = plt.subplots()
    # ax = cash_flow.plot(x="period", y=["monthly_payment", "monthly_principal"], ax=ax)
    ax.fill_between(
        cash_flow["period"],
        cash_flow["monthly_payment"],
        cash_flow["monthly_principal"],
        color="red",
        alpha=0.3,
    )
    ax.fill_between(
        cash_flow["period"],
        cash_flow["monthly_principal"],
        0,
        color="green",
        alpha=0.3,
    )
    # TODO: https://stackoverflow.com/questions/67488191/how-to-add-text-inside-a-filled-area-in-matplotlib
    plt.title("Principal and Interest over Time")
    st.pyplot(fig)
    st.caption("Red area is interest. Green area is principal")
