import streamlit as st
from PIL import Image

# -------------------------------------------
# 📊 Data and Project Discovery
# -------------------------------------------

# Display banner image at the top of the page
banner = Image.open("Streamlit Pics/Data_Presentation.png")
st.image(banner, use_container_width=True)

st.markdown("## Data and Project Discovery")

st.markdown("""
### Sources and Datasets

We use publicly available [**WHO Global Tobacco Control Data (2000–2022)**](https://apps.who.int/gho/data/node.main.Tobacco?lang=en), covering:

- MPOWER Overview – Policy compliance scores  
- National tobacco control programmes – Tobacco resource allocation figures  
- Retail price + national tax – Prices and taxes on tobacco  
- Non-age-standardized estimates of current tobacco use  
- Age-standardised estimates of current tobacco use  

We also added publicly available [**World Bank Open Data**](https://databank.worldbank.org/source/world-development-indicators) in the cleaning and pre-processing phase, covering:

- CLASS – Income Group and Continental Classification

📎 All datasets were audited and previewed in a combined summary table.  
🔎 *Note: “Region” refers to countries, territories, or areas (renamed from ‘country’ for consistency).*
""")

st.markdown("---")

st.markdown("""
### Variable Structure
""")

with st.expander("📍 Identification Variables"):
    st.markdown("""
    * **Region** – 162 countries, territories or areas (renamed from "country")  
      → Example: Germany, Kenya, Brazil  
    * **Continental Classification** – Countries grouped by continent  
      → South Asia, Europe & Central Asia, MENA, East Asia & Pacific, Sub-Saharan Africa, Latin America & Caribbean, North America  
    * **Income Group** – World Bank classification of countries by income  
      → Low, Lower Middle, Upper Middle, High
    """)

with st.expander("🧩 Explanatory Variables"):
    st.markdown("""
    * **Tobacco Control Measures (MPOWER)** – Six key policy areas scored on a 1–5 scale  
      → Monitor, Protect, Offer, Warn, Enforce, Raise  
    * **Tobacco Pricing & Taxation** – Pricing per pack, tax share, and structure  
      → Assesses economic deterrents to smoking (e.g., affordability, excise taxes, price levels)  
    * **Resource Allocation & Governance** – National strategy and capacity  
      → Annual budget (USD), staff numbers, and existence of a tobacco control agency
    """)

with st.expander("📈 Outcome Variables"):
    st.markdown("""
    * **Non-age-standardised Tobacco Use Prevalence (%)**  
      → Direct prevalence estimates for smoking  
    * **Age-standardised Tobacco Use Prevalence (%)**  
      → Adjusted for demographic differences  
    * **Gender-Stratified Tobacco Use Prevalence (%)**  
      → Separate estimates for males and females
    """)

st.markdown("---")
