import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from PIL import Image

st.set_page_config(
    page_title="QUIT – Global Tobacco Control",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------
# Conclusion and Policy Insights
# -------------------------------------------

# Display banner image at the top of the page
banner = Image.open("Streamlit Pics/Conclusion.png")
st.image(banner, use_container_width=True)

# Main heading
st.markdown("## Conclusion and Policy Insights")

st.markdown("""
This project explored global tobacco use trends and the impact of control policies through both machine learning and statistical modeling. Our findings reaffirm well-documented trends—such as a global decline in tobacco use and higher prevalence among males—while also revealing region-specific policy effects and modeling limitations.
""")

st.markdown("### Key Findings")

st.markdown("""
- Country-specific factors were more predictive of tobacco use than policy measures or cigarette prices.
- Linear models outperformed complex ML models, pointing to overfitting and limited generalizability.
- Stratification by income group and region improved model accuracy and revealed differing policy impacts.
- Risk warnings consistently showed strong negative associations with tobacco use.
- Tax and price effects were only clearly negative in high-income countries; in low-income contexts, the effects were inconsistent.
""")

# -------------------------------------------
# MPOWER Policy Effectiveness Heatmap (Simplified)
# -------------------------------------------
st.markdown("### Linking Policy Implementation to Impact")
st.markdown("This heatmap shows where increased policy implementation scores coincide with reduced tobacco use from 2008 to 2022. Green indicates desired policy effects (↑ implementation, ↓ prevalence), while red signals unintended trends.")

@st.cache_data
def load_effectiveness_data():
    df = pd.read_csv("Data/merged_tobacco_data.csv")
    df.columns = [col.strip() for col in df.columns]

    policy_columns = ["Monitor", "exposure_protect", "cessation_support", "risk_warning", "advertisement_ban", "tax_increase", "media_campaign"]
    df[policy_columns] = df[policy_columns].apply(pd.to_numeric, errors='coerce')
    df['average_policy'] = df[policy_columns].mean(axis=1)

    df[['average_policy', 'Overall use']] = df[['average_policy', 'Overall use']].apply(pd.to_numeric, errors='coerce')
    df = df.dropna(subset=['Region', 'Year', 'average_policy', 'Overall use'])

    df_2008 = df[df['Year'] == 2008].set_index('Region')
    df_2022 = df[df['Year'] == 2022].set_index('Region')

    common_regions = df_2008.index.intersection(df_2022.index)
    df_2008 = df_2008.loc[common_regions]
    df_2022 = df_2022.loc[common_regions]

    result_df = pd.DataFrame(index=common_regions)
    result_df['policy_diff'] = df_2022['average_policy'] - df_2008['average_policy']
    result_df['prevalence_diff'] = df_2022['Overall use'] - df_2008['Overall use']
    result_df['effect'] = result_df['policy_diff'].apply(lambda x: "↑" if x > 0 else ("↓" if x < 0 else "=")) + \
                          result_df['prevalence_diff'].apply(lambda x: "↓" if x < 0 else ("↑" if x > 0 else "="))
    result_df['Region'] = result_df.index
    return result_df.reset_index(drop=True)

effect_df = load_effectiveness_data()

color_map = {
    "↑↓": "green",
    "↑↑": "red",
    "↓↓": "orange",
    "↓↑": "purple",
    "==": "gray",
    "↑=": "lightgreen",
    "↓=": "pink",
    "=↓": "yellow",
    "=↑": "lightblue"
}

fig_effect = px.choropleth(
    effect_df,
    locations="Region",
    locationmode="country names",
    color="effect",
    color_discrete_map=color_map
)
fig_effect.update_layout(margin=dict(l=0, r=0, t=40, b=0))
st.plotly_chart(fig_effect, use_container_width=True)

# -------------------------------------------
# Policy Implications Section
# -------------------------------------------
st.markdown("### Policy Implications")

with st.expander("1. Implementation quality and reach matter"):
    st.markdown("Risk warnings stood out for their simplicity and impact—especially in LMICs—highlighting the value of high-fidelity implementation and broad coverage.")

with st.expander("2. Policies should be designed as integrated packages"):
    st.markdown("Policies operate in synergy; effectiveness improves when multiple MPOWER measures are implemented together rather than in isolation.")

with st.expander("3. Context matters"):
    st.markdown("Policy success varies by region and income level. Price-based policies were more effective in high-income contexts but weaker in LICs.")

with st.expander("4. Targeting matters"):
    st.markdown("Gender-specific and culturally sensitive approaches are needed to ensure policies are inclusive and reach underserved populations.")

st.markdown("### Reflections & Future Directions")

st.markdown("""
- Overfitting was a major challenge—future studies should include broader and more diverse datasets.
- Additional variables (e.g., enforcement data, public attitudes, lung cancer rates) would improve modeling depth.
- Cost-effectiveness analysis could not be completed due to data gaps. Future research should aim to standardize and collect more detailed financial inputs.
""")

st.markdown("Ultimately, global tobacco control is advancing—but its success depends on how well policies are adapted, integrated, and implemented in diverse contexts.")

