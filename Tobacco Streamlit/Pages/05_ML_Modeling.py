import streamlit as st
from PIL import Image
import pandas as pd
import json
import os

# Set up the page
st.set_page_config(
    page_title="QUIT – Global Tobacco Control",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Try relative path first
relative_json_path = os.path.join("..", "Data", "model.json")
absolute_json_path = "/Users/kathrinmuller/Desktop/Tabacco Project/Tobacco Streamlit/Data/model.json"
json_path = relative_json_path if os.path.exists(relative_json_path) else absolute_json_path

# Debug info
st.write("🔍 Using model file:", os.path.abspath(json_path))
st.write("✅ File found:", os.path.exists(json_path))

@st.cache_data
def load_feature_importance(filepath):
    with open(filepath, "r") as f:
        return json.load(f)

feature_importance_data = load_feature_importance(json_path)

# Load banner image
banner_path = os.path.join("..", "Streamlit Pics", "MLandStats.png")
if os.path.exists(banner_path):
    ml_banner = Image.open(banner_path)
    st.image(ml_banner, use_container_width=True)

# Page content
st.title("Machine Learning Analysis")

with st.expander("Methodology & Preprocessing"):
    st.markdown("""
    **Methodology:**  
    - Regression models to predict tobacco use prevalence and evaluate feature importance:  
      **Linear Regression**, **Decision Tree Regressor**, and **Random Forest Regressor**

    **Preprocessing:**  
    - **Encoding:** OneHotEncoding for low-cardinality variables (e.g., Continental Classification), Leave-One-Out for high-cardinality like Region  
    - **Scaling:** StandardScaler for linear models  
    - **Train-Test Split:** GroupShuffleSplit by country to prevent data leakage  
    """)

with st.expander("Initial Models"):
    st.markdown("""
    **MAE Performance:**  
    - **Linear Regression:** Train = 1.02, Test = 1.09  
    - **Decision Tree Regressor:** Train = 0.00, Test = 1.61  
    - **Random Forest Regressor:** Train = 0.24, Test = 1.22  

    **Observations:**  
    - Tree models overfit; linear regression is more generalizable  
    - Region dominated the prediction (>95% importance), skewing results  
    """)

with st.expander("Model Optimisation"):
    st.markdown("""
    - **Leave-One-Out Encoding** tried to reduce Region dominance  
    - **Clustering & Lag Features** had limited impact  
    - **XGBoost & Hyperparameter tuning** didn’t outperform simple Linear Regression  
    - **Conclusion:** Region removed to highlight policy variable impact
    """)

with st.expander("Feature Importance"):
    st.markdown("Explore how tobacco control features performed under different stratifications:")

    stratification_type = st.radio(
        "Select Stratification Type:",
        ["Gender", "Income Level", "Continent"]
    )

    if stratification_type == "Gender":
        st.subheader("Tobacco Use by Gender")
        st.dataframe(pd.DataFrame({
            "Train": [
                feature_importance_data["Gender"]["Female"]["Train MAE"],
                feature_importance_data["Gender"]["Male"]["Train MAE"]
            ],
            "Test": [
                feature_importance_data["Gender"]["Female"]["Test MAE"],
                feature_importance_data["Gender"]["Male"]["Test MAE"]
            ]
        }, index=["Female", "Male"]).T)

        gender = st.selectbox("Select Gender", ["Female", "Male"])
        fi = feature_importance_data["Gender"][gender]["Feature Importance"]
        st.dataframe(pd.DataFrame(fi.items(), columns=["Feature", "Importance"]).set_index("Feature"))

    elif stratification_type == "Income Level":
        st.subheader("Tobacco Use by Income Level")
        st.dataframe(pd.DataFrame({
            "Train": [
                feature_importance_data["Income"]["Low Income Group"]["Train MAE"],
                feature_importance_data["Income"]["High Income Group"]["Train MAE"]
            ],
            "Test": [
                feature_importance_data["Income"]["Low Income Group"]["Test MAE"],
                feature_importance_data["Income"]["High Income Group"]["Test MAE"]
            ]
        }, index=["Low Income Group", "High Income Group"]).T)

        income = st.selectbox("Select Income Group", ["Low Income Group", "High Income Group"])
        fi = feature_importance_data["Income"][income]["Feature Importance"]
        st.dataframe(pd.DataFrame(fi.items(), columns=["Feature", "Importance"]).set_index("Feature"))

    elif stratification_type == "Continent":
        st.subheader("Tobacco Use by Continent")
        continents = list(feature_importance_data["Continent"].keys())

        st.dataframe(pd.DataFrame({
            "Train": [feature_importance_data["Continent"][c]["Train MAE"] for c in continents],
            "Test": [feature_importance_data["Continent"][c]["Test MAE"] for c in continents]
        }, index=continents).T)

        selected = st.selectbox("Select Continent", continents)
        fi = feature_importance_data["Continent"][selected]["Feature Importance"]
        st.dataframe(pd.DataFrame(fi.items(), columns=["Feature", "Importance"]).set_index("Feature"))
