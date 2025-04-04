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
# 📊 Data Exploration and Visualizations
# -------------------------------------------

# Display banner image at the top of the page
banner = Image.open("Streamlit Pics/Visualisation.png")
st.image(banner, use_container_width=True)

# Main heading
st.markdown("## Data Exploration and Visualizations")

st.markdown("To better understand patterns in tobacco control and smoking prevalence, we visualized key variables to show differences across time, gender, geography, and policy implementation.")

# -------------------------------------------
# Load Data
# -------------------------------------------
@st.cache_data
def load_age_standard_data():
    df = pd.read_csv("Data/Non_age_standardised_smoking_prevalence.csv")
    df = df.rename(columns={
        "Unnamed: 0": "Region",
        "Unnamed: 1": "Year",
        "Estimate of current tobacco use prevalence (%)": "Overall use",
        "Estimate of current tobacco use prevalence (%).1": "Male",
        "Estimate of current tobacco use prevalence (%).2": "Female"
    })
    df = df.drop(index=0)
    df = df[["Region", "Year", "Overall use", "Male", "Female"]].copy()
    for col in ["Overall use", "Male", "Female"]:
        df[col] = df[col].str.split(" ").str[0].astype(float)
    df["Year"] = df["Year"].astype(int)
    return df

@st.cache_data
def load_mpower_data():
    emp = pd.read_csv("Data/MPOWER.csv")
    emp = emp.rename(columns={
        "Countries, territories and areas": "Region",
        "Protect from tobacco smoke": "exposure_protect",
        "Offer help to quit tobacco use": "cessation_support",
        "Warn about the dangers of tobacco": "risk_warning",
        "Enforce bans on tobacco advertising": "advertisement_ban",
        "Raise taxes on tobacco": "tax_increase",
        "Anti-tobacco mass media campaigns": "media_campaign"
    })
    policies = ['exposure_protect', 'cessation_support', 'risk_warning', 'advertisement_ban', 'tax_increase', 'media_campaign']
    for policy in policies:
        emp[policy] = pd.to_numeric(emp[policy], errors='coerce')
    emp = emp[emp["Year"].isin([2010, 2022])]
    return emp, policies

@st.cache_data
def load_price_data():
    price = pd.read_csv("Data/tobaccoprice.csv")
    price = price.rename(columns={"Location": "Region", "Period": "Year", "Value": "Cigarette_price"})
    price["Jittered_Year"] = price["Year"] + np.random.uniform(-0.5, 0.5, size=len(price))
    return price

age_df = load_age_standard_data()
emp, policy_cols = load_mpower_data()
price_df = load_price_data()

# The rest of your visualizations and interpretation text go here...

st.markdown("---")

# -------------------------------------------
# Graph 1: Global Map
# -------------------------------------------
st.markdown("### Global Smoking Prevalence Over Time")
age_filtered = age_df[(age_df["Year"] >= 2007) & (age_df["Year"] <= 2022)].copy()
age_filtered = age_filtered.sort_values("Year")

fig_map = px.choropleth(
    age_filtered,
    locations="Region",
    locationmode="country names",
    color="Overall use",
    animation_frame="Year",
    color_continuous_scale="Turbo",
    range_color=[age_filtered["Overall use"].min(), age_filtered["Overall use"].max()],
    labels={"Overall use": "Smoking Prevalence (%)"}
)
fig_map.update_layout(margin=dict(l=0, r=0, t=0, b=0), width=1000, height=600)
st.plotly_chart(fig_map)
st.markdown("*This animated choropleth map highlights the changing landscape of smoking prevalence from 2007 to 2022. Red shades indicate high prevalence, while green and blue denote low levels. Most countries follow a downward trend over time.*")

st.markdown("---")

# -------------------------------------------
# Graph 2: Distribution + Trends
# -------------------------------------------
st.markdown("### Tobacco Use by Group and Over Time")
group = st.radio("Select group to view:", ["Overall use", "Male", "Female"])
colors = {"Overall use": "#4169E1", "Male": "#2ECC71", "Female": "#9B59B6"}
col1, col2 = st.columns(2)

with col1:
    st.markdown("**Distribution across all years**")
    fig1, ax1 = plt.subplots(figsize=(6, 4))
    sns.histplot(age_df[group], kde=True, color=colors[group], ax=ax1)
    ax1.set_xlabel("Tobacco Use Prevalence (%)")
    ax1.set_ylabel("Frequency")
    st.pyplot(fig1)

with col2:
    st.markdown("**Trends over time (2000–2030)**")
    fig2, ax2 = plt.subplots(figsize=(7, 4))
    sns.boxplot(x="Year", y=group, data=age_df, color=colors[group], ax=ax2)
    ax2.set_ylabel("Tobacco Use Prevalence (%)")
    ax2.set_xlabel("Year")
    ax2.tick_params(axis='x', rotation=45)
    st.pyplot(fig2)

st.markdown("*These plots highlight differences in tobacco use distribution by gender, and trends over time. Male tobacco use remains significantly higher, with all groups showing a consistent decline over the observed period.*")

st.markdown("---")

# -------------------------------------------
# Graph 3: Top 10 Trends
# -------------------------------------------
st.markdown("### Tobacco Use Trends in Heaviest Smoking Countries")
top_users = ['Kiribati', 'Myanmar', 'Nepal', 'Nauru', 'Bangladesh', 'Greece', 'India', 'Papua New Guinea', 'Madagascar', 'Timor-Leste']
heaviest_users = age_df[age_df["Region"].isin(top_users)]

fig3, ax3 = plt.subplots(figsize=(10, 5))
sns.lineplot(data=heaviest_users, x="Year", y="Overall use", hue="Region", ax=ax3)
ax3.set_ylabel("Prevalence (%)")
ax3.set_xlabel("Year")
ax3.legend(title="Country", bbox_to_anchor=(1.05, 1), loc='upper left')
st.pyplot(fig3)
st.markdown("*This time series focuses on countries with the highest initial smoking prevalence. All selected regions exhibit downward trends, confirming global progress in tobacco control.*")

st.markdown("---")

# -------------------------------------------
# Graph 4: MPOWER Policy
# -------------------------------------------
st.markdown("### MPOWER Policy Implementation Scores")
unique_countries = sorted(emp["Region"].unique())
selected_countries = st.multiselect("Select countries:", options=unique_countries, default=["India", "New Zealand", "Kenya", "France", "Colombia"])
selected_year = st.selectbox("Select year:", options=[2010, 2022])

filtered = emp[(emp["Region"].isin(selected_countries)) & (emp["Year"] == selected_year)]
melted = filtered.melt(id_vars=["Region"], value_vars=policy_cols, var_name="Policy", value_name="Score")

fig4, ax4 = plt.subplots(figsize=(10, 6))
sns.barplot(data=melted, x="Score", y="Policy", hue="Region", ax=ax4, palette="muted")
ax4.set_xlabel("Implementation Score (0–5)")
ax4.set_ylabel("MPOWER Policy")
ax4.legend(title="Country", bbox_to_anchor=(1.05, 1), loc="upper left")
st.pyplot(fig4)
st.markdown("*This visual compares tobacco control policy implementation across countries in 2010 and 2022. Improvements are uneven—risk warnings and smoke-free policies advanced most, while taxation and media campaigns saw limited change.*")

st.markdown("---")

# -------------------------------------------
# Graph 5: Cigarette Prices
# -------------------------------------------
st.markdown("### International Cigarette Prices Over Time")
all_countries = sorted(price_df["Region"].unique())
default = ["New Zealand", "Sri Lanka", "Australia"]
options = ["All countries"] + all_countries
selection = st.multiselect("Select countries to compare:", options=options, default=default)

if "All countries" in selection:
    filtered_price = price_df
else:
    filtered_price = price_df[price_df["Region"].isin(selection)]

fig5 = px.scatter(
    filtered_price,
    x="Jittered_Year",
    y="Cigarette_price",
    color="Region",
    hover_name="Region",
    opacity=0.7,
    range_y=[0, 20],
    labels={"Jittered_Year": "Year", "Cigarette_price": "Price (Intl $)"}
)
fig5.update_layout(width=1000, height=500, legend_title="Country")
st.plotly_chart(fig5)
st.markdown("*This scatterplot tracks changes in cigarette prices by country over time. Price increases vary widely, with some countries clustering near the median and others demonstrating sharp increases.*")

st.markdown("---")
