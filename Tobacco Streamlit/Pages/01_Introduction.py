import streamlit as st
from PIL import Image

st.set_page_config(
    page_title="QUIT – Global Tobacco Control",
    page_icon=None,
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------
# 📖 Introduction
# -------------------------------------------

# Display banner image at the top of the page
banner = Image.open("Streamlit Pics/Introduction.png")
st.image(banner, use_container_width=True)

# Main heading
st.markdown("## Introduction")

# Background
st.markdown("### Background")

with st.expander("🚬 Tobacco Use and Health Risks"):
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("""
        Tobacco use is one of the leading causes of preventable death, causing over 8 million deaths annually.

        It is linked to severe health issues such as:
        - Lung cancer
        - Cardiovascular diseases
        - Respiratory conditions
        - Stroke

        In addition to health impacts, tobacco use places a significant economic burden on healthcare systems and reduces global productivity.  
        Smoking prevalence varies widely—from **0.4% to 35.7%** across countries.
        """)
    with col2:
        st.image("Streamlit Pics/LungCancer.png", use_column_width=True)

with st.expander("🧱 WHO MPOWER Framework"):
    col_top1, col_top2 = st.columns([3, 2])
    with col_top1:
        st.markdown("""
        The **MPOWER** framework was introduced by the **World Health Organization (WHO)** in **2008** to help countries implement the **WHO Framework Convention on Tobacco Control (FCTC)**, the first international public health treaty.
        """)
    st.markdown("""
    The overall goal of the MPOWER strategy is to provide countries with a structured, evidence-based approach to reduce tobacco use, prevent initiation—particularly among youth—and ultimately reduce morbidity and mortality linked to tobacco consumption, thus improving public health outcomes on a global scale.
    """)

    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("""
        Each letter in the acronym MPOWER represents a policy measure:

        - **M – Monitor**: Regularly monitor tobacco use and prevention policies through reliable surveillance systems.
        - **P – Protect**: Enact and enforce smoke-free laws to protect people from second-hand smoke.
        - **O – Offer**: Provide support for tobacco users to quit through accessible cessation programs and health systems.
        - **W – Warn**: Use strong graphic warnings on packaging and conduct impactful public awareness campaigns.
        - **E – Enforce**: Ban tobacco advertising, promotion, and sponsorship across all media platforms.
        - **R – Raise**: Increase tobacco taxes to reduce affordability and consumption, especially among youth.
        """)
    with col2:
        rotated_image = Image.open("Streamlit Pics/NoSmoking.png").rotate(90, expand=True)
        st.image(rotated_image, use_column_width=True)

    st.markdown("""
    MPOWER policies are **evaluated using standardized compliance indicators**, allowing for cross-country comparison and tracking over time. These indicators guide national governments in measuring progress and identifying areas for improvement.
    """)

# QUIT Project Framework
st.markdown("### QUIT Project Framework")

st.markdown("""
#### Goal
To assess the effectiveness of tobacco control measures and tobacco pricing on tobacco use prevalence,  
with a focus on **regional and gender differences**, to identify best practices for policy design.
""")

# Display as matching tabs per research question
st.markdown("#### Research Questions and Objectives")

with st.expander("🔍 Explore Research Questions & Objectives"):
    tabs = st.tabs(["RQ1", "RQ2", "RQ3"])

    with tabs[0]:
        st.markdown("##### RQ1: How effective are tobacco control measures, and which are most impactful?")
        st.markdown("""
        **Objectives Addressed:**  
        - **O1:** Assess global tobacco use prevalence and MPOWER policy coverage.  
        - **O2:** Evaluate how effective MPOWER measures and taxation are in reducing smoking.
        """)

    with tabs[1]:
        st.markdown("##### RQ2: What role do region and income level play in shaping tobacco use?")
        st.markdown("""
        **Objective Addressed:**  
        - **O3:** Analyze how effectiveness varies by **region** and **income group**.
        """)

    with tabs[2]:
        st.markdown("##### RQ3: How does gender affect the effectiveness of policies?")
        st.markdown("""
        **Objective Addressed:**  
        - **O4:** Explore **gender-specific** impacts of tobacco control policies.
        """)
