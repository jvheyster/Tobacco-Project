import streamlit as st

st.set_page_config(
    page_title="QUIT – Global Tobacco Control",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# Correct title formatting: QUIT–QUantifying the Impact of Tobacco control measures
st.markdown("""
<h1 style='font-size: 50px;'>
<span style='font-weight:bold; font-size:60px;'>Q</span><span style='font-weight:bold; font-size:60px;'>U</span><span style='font-weight:bold; font-size:60px;'>I</span><span style='font-weight:bold; font-size:60px;'>T</span>–<span style='font-weight:bold;'>QU</span>antifying the Impact of Tobacco control measures
</h1>
""", unsafe_allow_html=True)

# Updated Banner Image with full width
st.image("Streamlit Pics/Homepage.png", use_container_width=True)

st.markdown("""
---

## About the Project  
**QUIT** – *Quantifying the Impact of Tobacco control measures* – is a collaborative public health assessment by **Jef van Heijster**, **Owen Molloy**, and **Kathrin Müller**.  
This project explores how effective MPOWER policies and tobacco taxation are in reducing smoking prevalence globally, while accounting for differences by **region**, **income group**, and **gender**.
""")

st.markdown("""
---

## What This Presentation Covers
""")

with st.expander("Introduction"):
    st.markdown("This section provides a brief overview of tobacco use globally, introduces the MPOWER policies by WHO, and outlines the objectives and relevance of our QUIT Project.")

with st.expander("Data Sources"):
    st.markdown("Detailed description of WHO tobacco-related datasets used in the project, the variables involved, and an initial exploration of key characteristics and trends in tobacco prevalence.")

with st.expander("Exploratory Analysis"):
    st.markdown("Visual and statistical exploration of global tobacco use trends, highlighting differences by region, income group, and gender. Key insights from early analyses are discussed.")

with st.expander("Data Preprocessing"):
    st.markdown("Description of data cleaning processes, merging strategies, handling of missing data through interpolation, and preparation steps for subsequent modeling.")

with st.expander("Machine Learning Analysis"):
    st.markdown("In-depth evaluation of machine learning models predicting tobacco use prevalence. This includes performance metrics, model limitations, and critical insights from feature importance analyses.")

with st.expander("Statistical Modeling"):
    st.markdown("Robust statistical methods evaluating the causal impacts of tobacco control measures. Explanation of fixed effects regression models, clustered standard errors, and stratified analyses by income, continent, and gender.")

with st.expander("Conclusion and Outlook"):
    st.markdown("Final summary of project findings, implications for tobacco control policy, methodological limitations encountered, and recommendations for future research.")

st.success("Use the sidebar to navigate through each section, starting with 'Introduction'.")
