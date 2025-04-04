import streamlit as st
import pandas as pd

# --- Page Configuration ---
st.set_page_config(page_title="Statistical Analysis Overview", layout="wide")

# --- Banner Image ---
st.image("Streamlit Pics/MLandStats.png")

# --- Title ---
st.title("Statistical Analysis and Policy Insights")

# --- Introduction ---
st.markdown("""
Our statistical analysis aimed to identify the individual impacts of tobacco control policies on tobacco use prevalence.
We used a series of fixed effects regression models, adjusted for multicollinearity, interaction effects, and stratified by
income level, region, and gender to assess the robustness and policy relevance of each intervention.
""")

# --- Statistical Methods Section ---
st.header("Statistical Methods")

methods = [
    "Fixed Effects Regression",
    "Multicollinearity Check",
    "Interaction Terms",
    "Clustered Standard Errors",
    "Stratified Models"
]

selected_method = st.radio("Select a modeling step:", methods, horizontal=True)

if selected_method == "Fixed Effects Regression":
    with st.container():
        st.info("""
        ### Fixed Effects Regression
        Estimate the within-country impact of policy changes by controlling for unobserved, time-invariant country characteristics and global time trends through fixed effects.

        #### Result
        * Model fit was high (R² = 0.982), suggesting potential overfitting.
        * **Risk Warnings** were the only policy with a robust, negative, and statistically significant effect.
        * **Advertisement Bans** had a significant but unexpected positive association.
        * All other policy coefficients were statistically insignificant or borderline.
        """)
        df_pooled = pd.read_csv("Data/policy_results_pooled.csv")
        st.dataframe(df_pooled)

elif selected_method == "Multicollinearity Check":
    with st.container():
        st.info("""
        ### Multicollinearity Check
        Assess whether correlations among predictors inflate standard errors and mask individual policy effects by computing Variance Inflation Factors (VIF).

        #### Result
        * High multicollinearity detected, especially for **Cessation Support** (VIF = 11.3) and **Risk Warnings** (VIF = 10.4).
        * Instead of excluding variables, interaction terms were introduced to capture potential policy synergies.
        """)

elif selected_method == "Interaction Terms":
    with st.container():
        st.info("""
        ### Interaction Terms
        Explore whether combinations of policies — particularly those with theoretical synergy and empirical correlation — have compounded effects that single policies do not capture.

        #### Result
        * **Media Campaign × Risk Warning** demonstrated a significant negative interaction.
        * Other combinations (e.g., Price × Ad Ban, Cessation Support × Risk Warning) were borderline significant but unstable in multivariate interaction models.
        * Instability indicated persistent multicollinearity.
        """)

elif selected_method == "Clustered Standard Errors":
    with st.container():
        st.info("""
        ### Clustered Standard Errors
        Improve statistical inference by adjusting standard errors for within-country autocorrelation and heteroskedasticity across time.

        #### Result
        * **Risk Warnings** remained statistically significant (p = 0.034).
        * **Media–Risk Warning interaction** became borderline (p = 0.105).
        * Other policy coefficients lost statistical significance.
        """)

elif selected_method == "Stratified Models":
    with st.container():
        st.info("""
        ### Stratified Models
        Explore model performance in more homogenous subsets to uncover contextual variation: data were stratified by income group, continent, and gender. Models retained fixed effects and clustered standard errors.

        #### Result
        * **By Income Group**:
            * LMIC: Risk Warnings were highly effective (p = 0.003).
            * HIC: Media Campaigns showed borderline effect (p = 0.092).
            * UMIC & LIC: No significant policy effects observed.
        * **By Continent**:
            * East Asia & Pacific: Risk Warnings (p = 0.004) highly effective.
            * Europe & Central Asia: Advertisement Bans reduced tobacco use (p = 0.037).
            * MENA: Ad Bans (p = 0.015), Cessation Support showed borderline increase (p = 0.079).
        * **Gender-Stratified**:
            * LMIC: Risk Warnings significant for both men (p = 0.008) and women (p = 0.026).
            * HIC: Cigarette Prices reduced female smoking (p = 0.027).
            * ECA & SSA: Advertisement Bans increased smoking among women (p = 0.035–0.041).
        """)

# --- Results Dashboard ---
st.header("Results Dashboard")

stratification_level = st.selectbox("Choose stratification level:", [
    "None (Pooled)", "By Income Group", "By Continent"
])

gender_filter = st.selectbox("Choose gender filter:", [
    "All", "Male", "Female"
])

st.markdown("""
👉 Based on your selections above, a table of coefficients, p-values, and effect direction will appear here.
""")

# Conditional display
table_mapping = {
    ("None (Pooled)", "All"): "Data/policy_results_pooled.csv",
    ("By Income Group", "All"): "Data/policy_results_income.csv",
    ("By Continent", "All"): "Data/policy_results_continent.csv",
    ("By Income Group", "Male"): "Data/gender_income_results.csv",
    ("By Income Group", "Female"): "Data/gender_income_results.csv",
    ("By Continent", "Male"): "Data/gender_continent_results.csv",
    ("By Continent", "Female"): "Data/gender_continent_results.csv"
}

key = (stratification_level, gender_filter)

if key in table_mapping:
    try:
        df_result = pd.read_csv(table_mapping[key])
        st.dataframe(df_result)
    except FileNotFoundError:
        st.warning("Results table not found. Please upload the file: {}".format(table_mapping[key]))
else:
    st.info("This combination is currently not available.")

# --- Key Takeaways and Interpretation ---
st.header("Key Takeaways and Interpretation")

with st.expander("Most Effective Policies"):
    st.markdown("""
    **Risk Warnings**: Consistently effective, especially in LMICs and East Asia & Pacific — likely due to low-cost, standardized design (e.g., pack labeling) and strong impact in low-awareness settings.

    **Cigarette Prices**: Only significant among women in HICs, suggesting gendered price sensitivity and effective enforcement; no effect in LMICs may reflect illicit trade or poor tax pass-through.
    """)

with st.expander("Unexpected Findings"):
    st.markdown("""
    **Advertisement Bans**: Often linked to higher smoking rates — possibly due to weak enforcement, policy loopholes, or reactive adoption in response to rising use.

    **Cessation Support**: Correlated with increased smoking in some female models; may reflect targeting of high-risk groups or unsuccessful quit attempts.
    """)

with st.expander("Context-Limited Policies"):
    st.markdown("""
    **Media Campaigns**: Borderline impact only in HICs and European men; likely due to inconsistent quality, reach, or audience engagement.

    **Tax Increases**: No significant effect overall — possibly due to low tax rates, compensatory strategies, or illicit markets undermining policy impact.
    """)

with st.expander("Policy Interactions"):
    st.markdown("""
    **Media Campaign × Risk Warning**: Showed a robust joint effect in isolation, indicating the benefit of combining awareness tools — though significance weakened in full models, likely due to multicollinearity.
    """)

# --- Strengths and Limitations ---
st.header("Strengths and Limitations")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Strengths")
    st.markdown("""
    * Robust fixed effects model to control for country-specific factors and global trends.
    * Stratified and gender-specific models uncovered contextual differences in policy effectiveness.
    * Clustered standard errors improved statistical reliability by accounting for within-country correlation.
    """)

with col2:
    st.subheader("Limitations")
    st.markdown("""
    * High multicollinearity made it difficult to isolate individual policy effects.
    * Small sample sizes in stratified models reduced statistical power.
    * Potential omitted variable bias, such as unmeasured enforcement quality or informal tobacco markets.
    """)
