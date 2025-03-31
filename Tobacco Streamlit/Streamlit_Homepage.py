import streamlit as st

st.set_page_config(
    page_title="QUIT – Global Tobacco Control",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("# Welcome to the QUIT Project")

st.image("Streamlit Pics/Frontpage.png", caption="QUIT: Quantifying the Impact of Tobacco control measures", use_column_width=True)

st.markdown("""
---

## 🔍 About the Project  
**QUIT** – *Quantifying the Impact of Tobacco control measures* – is a collaborative public health assessment by **Jef van Heijster**, **Owen Molloy**, and **Kathrin Müller**.  
This project explores how effective MPOWER policies and tobacco taxation are in reducing smoking prevalence globally, while accounting for differences by **region**, **income group**, and **gender**.
""")

st.markdown("""
---

## 🧭 What This Presentation Covers
""")

with st.expander("🌍 Background"):
    st.markdown("Global tobacco use and MPOWER policy overview, plus an introduction to the project")

with st.expander("🔍 Presentation and Exploration of Data"):
    st.markdown("Initial trends and distribution patterns")

with st.expander("🧹 Data Preprocessing"):
    st.markdown("Cleaning and preparing the dataset")

with st.expander("📊 Regression Modeling"):
    st.markdown("Impact assessment of control measures")

with st.expander("👥 Statistical Models"):
    st.markdown("Gender-, region-, and income-specific analysis")

with st.expander("💡 Proof-of-Concept Dashboard"):
    st.markdown("Simulating potential policy impacts")

with st.expander("📌 Conclusion, Recommendations & Outlook"):
    st.markdown("Summary and future directions")

st.success("⬅️ Use the sidebar to begin with '01_Introduction' and follow through each section.")