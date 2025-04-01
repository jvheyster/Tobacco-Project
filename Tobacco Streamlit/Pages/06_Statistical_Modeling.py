import streamlit as st
import pandas as pd

st.set_page_config(page_title="Statistical Analysis Overview", layout="wide")

# Banner Image
st.image("Streamlit Pics/MLandStats.png")

# Title
st.title("Statistical Analysis and Policy Insights")

# Introduction
st.markdown("""
### Overview
Our statistical analysis aimed to identify the **individual impacts of tobacco control policies** on tobacco use prevalence. We used Fixed Effects regression models with clustered standard errors, interaction terms, and stratifications by income, continent, and gender to provide robust and policy-relevant insights.
""")

# Methods Overview
st.markdown("## Statistical Methods Explained")
method = st.radio("Choose a method to see its explanation:", ["Fixed Effects Regression", "Clustered Standard Errors", "Interaction Terms", "Stratification"])

method_descriptions = {
    "Fixed Effects Regression": "Controls for time-invariant characteristics (like culture or geography), allowing us to isolate the impact of policy changes within each country.",
    "Clustered Standard Errors": "Adjusts for within-country correlations and heteroskedasticity, improving the reliability of statistical estimates.",
    "Interaction Terms": "Identifies combined effects of policies that might enhance or diminish their individual impacts (e.g., media campaigns reinforcing risk warnings).",
    "Stratification": "Analyzes data separately by income, continent, or gender, uncovering nuanced, context-specific effects."
}
st.info(method_descriptions[method])

# Load key results data
@st.cache_data
def load_results():
    data = {
        'Policy': ['Risk Warnings', 'Advertisement Ban', 'Cigarette Prices', 'Media Campaigns', 'Cessation Support', 'Exposure Protection', 'Tax Increases'],
        'Overall Effect': ['Strong', 'Mixed', 'Limited', 'Mixed', 'Limited', 'Limited', 'None'],
        'Significant in': ['LMICs, East Asia & Pacific', 'Europe & Central Asia, MENA (counterintuitive)', 'HICs (women only)', 'HICs, Europe & Central Asia (men)', 'Americas (counterintuitive women)', 'Sub-Saharan Africa (women)', 'No significant effect'],
    }
    return pd.DataFrame(data)

results_df = load_results()

# Main Findings
st.markdown("## Main Statistical Findings")
view_choice = st.selectbox("Choose an analysis view:", ["Overall Results", "Income Stratification", "Continent Stratification", "Gender-specific"])

if view_choice == "Overall Results":
    st.markdown("#### Overall Policy Impact Summary")
    st.dataframe(results_df.set_index('Policy'))

elif view_choice == "Income Stratification":
    st.markdown("#### Policy Impact by Income Group")
    income_data = {
        'Income Group': ['High Income (HIC)', 'Upper-Middle Income (UMIC)', 'Lower-Middle Income (LMIC)', 'Low Income (LIC)'],
        'Significant Policies': ['Cigarette Prices (women), Media Campaigns', 'No significant effect', 'Risk Warnings', 'No significant effect']
    }
    income_df = pd.DataFrame(income_data)
    st.dataframe(income_df.set_index('Income Group'))

elif view_choice == "Continent Stratification":
    st.markdown("#### Policy Impact by Continent")
    continent_data = {
        'Continent': ['Europe & Central Asia', 'Middle East & North Africa', 'East Asia & Pacific', 'South Asia', 'Americas', 'Sub-Saharan Africa'],
        'Significant Policies': ['Advertisement Bans (counterintuitive)', 'Advertisement Bans (counterintuitive)', 'Risk Warnings', 'No significant effect', 'No significant effect', 'Exposure Protection (women)']
    }
    continent_df = pd.DataFrame(continent_data)
    st.dataframe(continent_df.set_index('Continent'))

elif view_choice == "Gender-specific":
    st.markdown("#### Policy Impact by Gender")
    gender_data = {
        'Gender': ['Men', 'Women'],
        'Significant Policies': ['Risk Warnings (LMICs, East Asia & Pacific)', 'Cigarette Prices (HIC), Risk Warnings (LMICs, East Asia & Pacific), Exposure Protection (Sub-Saharan Africa, mixed effects)']
    }
    gender_df = pd.DataFrame(gender_data)
    st.dataframe(gender_df.set_index('Gender'))

# Key Takeaways
st.markdown("## Key Takeaways & Policy Insights")
st.success("""
- **Risk Warnings**: Most consistent and effective globally, particularly in LMICs and East Asia & Pacific.
- **Advertisement Bans**: Often associated with unintended increases, potentially due to enforcement gaps or industry adaptations.
- **Pricing & Taxation**: Effective primarily in High-Income contexts; less impactful elsewhere.
- **Gender Considerations**: Women show specific responsiveness to cigarette pricing in high-income countries.
- **Context-Sensitivity**: Policy effectiveness varies greatly by region and economic contexts.
""")

# Reflection and Outlook
with st.expander("Reflection & Future Research"):
    st.markdown("""
    **Limitations:**
    - High multicollinearity between policies.
    - Limited data points for certain stratifications.
    - Potential omitted variable bias.

    **Future Directions:**
    - Expand dataset with additional countries and historical data.
    - Include enforcement quality, illicit markets, and public attitude surveys.
    - Conduct cost-effectiveness analyses.
    """)