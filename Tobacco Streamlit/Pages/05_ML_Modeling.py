import streamlit as st
from PIL import Image
import pandas as pd
import json



file_path = "Data/model.json"
@st.cache_data
def load_feature_importance(file_path):
    with open("Data/model.json", "r") as f:
        return json.load(f)

feature_importance_data = load_feature_importance("Data/model.json")

# If you have a banner image for the machine learning section, load it:
ml_banner = Image.open("Streamlit Pics/MLandStats.png")
st.image(ml_banner, use_column_width=True)

# Section Title
st.title("Machine Learning Analysis")

# Expander: Methodology & Preprocessing
with st.expander("### 📊 Methodology & Preprocessing"):
    st.markdown("""
    **Methodology:**  
    - We used regression models to predict tobacco use prevalence and determine the relative importance of our explanatory variables, starting with **Linear Regression**, **Decision Tree Regressor**, and **Random Forest Regressor**.
    - As **Linear Regression** performed the best of all models, we determined **feature importance** using **Linear Regression coefficient values**
    
    **Preprocessing:**  
    - **Encoding:** Applied different encoding methods based on variable type. For example, OneHotEncoding for Continental Classification because of its low-cardinality and Target Encoding to represent Region.   
    - **Scaling:** Standard Scaler was used on our data to ensure it was compatible with Linear Regression.  
    - **Test-Train Split:** We used GroupShuffleSplit to ensure all data points from a given country stayed in the same set, to avoid data leakage from our interpolation. 
    """)

# Expander: Model Performance
with st.expander("### 🔧 Initial Models"):
    st.markdown("""
    **Observations:**  
    - **Linear Regression** provided stable performance with minimal overfitting.  
    - **Tree-based models** (Decision Tree and Random Forest) achieved lower training errors but suffered from overfitting, reducing their generalizability.
    - The **'Region'** variable dominated model predictions (>95% feature importance for Region and Year together), overshadowing the impact of specific tobacco control measures.
    - Models trained without **Region** had significantly decreased performance, and still largely relied on **Continental Classification**.
    - Models trained without **either** had the lowest performance.   
    """)

    region_select = st.selectbox(
            "Select Initial Model",
            options=["Initial Models", "Without Region", "Without Region or Continent"],
            index=0  
        )
    if region_select == "Initial Models":
        st.write("**Performance Metrics (Mean Absolute Error, MAE):**")
        st.dataframe(pd.DataFrame({
                "Train": [feature_importance_data["Linear Regression"]["Initial Model"]["Train MAE"],
                        feature_importance_data["Decision Tree Regressor"]["Initial Model"]["Train MAE"],
                        feature_importance_data["Random Forest Regressor"]["Initial Model"]["Train MAE"]],
                "Test":  [feature_importance_data["Linear Regression"]["Initial Model"]["Test MAE"],
                        feature_importance_data["Decision Tree Regressor"]["Initial Model"]["Test MAE"],
                        feature_importance_data["Random Forest Regressor"]["Initial Model"]["Test MAE"]]
            }, index=["Linear Regression", "Decision Tree Regressor", "Random Forest Regressor"]).T)
        
        st.write("**Feature Importance:**")
        feature_importance = feature_importance_data["Linear Regression"]["Initial Model"]["Feature Importance"]
        df = pd.DataFrame(feature_importance.items(), columns=["Feature", "Importance"]).set_index("Feature")
        expand = st.checkbox("Show full table", value=False, key="expand")
        if expand:
            st.dataframe(df)
        else:
            st.dataframe(df.head()) 

    if region_select == "Without Region":
        st.write("**Performance Metrics (Mean Absolute Error, MAE):**")
        st.dataframe(pd.DataFrame({
                "Train": [feature_importance_data["Linear Regression"]["Models Without Region"]["Train MAE"],
                        feature_importance_data["Decision Tree Regressor"]["Models Without Region"]["Train MAE"],
                        feature_importance_data["Random Forest Regressor"]["Models Without Region"]["Train MAE"]],
                "Test":  [feature_importance_data["Linear Regression"]["Models Without Region"]["Test MAE"],
                        feature_importance_data["Decision Tree Regressor"]["Models Without Region"]["Test MAE"],
                        feature_importance_data["Random Forest Regressor"]["Models Without Region"]["Test MAE"]]
            }, index=["Linear Regression", "Decision Tree Regressor", "Random Forest Regressor"]).T)

        feature_importance = feature_importance_data["Linear Regression"]["Models Without Region"]["Feature Importance"]
        df = pd.DataFrame(feature_importance.items(), columns=["Feature", "Importance"]).set_index("Feature")
        expand1 = st.checkbox("Show full table", value=False, key = "expand1")
        if expand1:
            st.dataframe(df)
        else:
            st.dataframe(df.head())

    if region_select == "Without Region or Continent":
        st.write("**Performance Metrics (Mean Absolute Error, MAE):**")
        st.dataframe(pd.DataFrame({
                "Train": [feature_importance_data["Linear Regression"]["Without Region or Continent"]["Train MAE"],
                        feature_importance_data["Decision Tree Regressor"]["Without Region or Continent"]["Train MAE"],
                        feature_importance_data["Random Forest Regressor"]["Without Region or Continent"]["Train MAE"]],
                "Test":  [feature_importance_data["Linear Regression"]["Without Region or Continent"]["Test MAE"],
                        feature_importance_data["Decision Tree Regressor"]["Without Region or Continent"]["Test MAE"],
                        feature_importance_data["Random Forest Regressor"]["Without Region or Continent"]["Test MAE"]]
            }, index=["Linear Regression", "Decision Tree Regressor", "Random Forest Regressor or Continent"]).T)

        feature_importance = feature_importance_data["Linear Regression"]["Without Region or Continent"]["Feature Importance"]
        df = pd.DataFrame(feature_importance.items(), columns=["Feature", "Importance"]).set_index("Feature")
        expand2 = st.checkbox("Show full table", value=False, key = "expand2")
        if expand2:
            st.dataframe(df)
        else:
            st.dataframe(df.head())    

# Expander: Feature Importance & Model Tuning
with st.expander("### ⚙️ Model Optimisation"):
    st.markdown("""
    **Methods:**  
    - **Leave One Out Encoding** was implemented instead of target encoding to reduce overfitting; however ‘Region’ still played a dominant role.
    - **K-means clustering** to group countries as an alternative to encoding Region was tested, but did little to improve model performance. 
    - **Time lag variables** were introduced to better capture policy delay impact, but also did little to improve model performance. 
    - **Hyperparameter optimisation** was introduced for **Random Forest Regressor** and **XGBoost models**, but these models were still outperformed by simple **Linear Regression**. 
    - **Ridge regression regularisation** was not able to overcome the importance of Region in predictions. 
 
    
    **Observation**  
    - The predictive importance of **Region** could not be retained without reducing the importance of other explanatory variables.  
    - We therefore decided to drop **Region** and **Continental Classification** to proceed with analysing feature importance
    - **Linear Regression** performed the best of all models, so we selected this model for our feature importance analysis.          
    """)

    optimisation_choice = st.selectbox(
            "Select Optimisation Choice",
            options=["Leave One Out Encoded", "K-Means Clustering", "Time Lag Variables", "Hyperparameter Optimisation", "Ridge Regression"],
            index=0  
        )
    if optimisation_choice == "Leave One Out Encoded":
        st.write("**Mean Absolute Error (MAE) Scores:**")
        st.dataframe(pd.DataFrame({
            "Train": [feature_importance_data["Linear Regression"]["Leave One Out Encoded"]["Train MAE"]],
            "Test":  [feature_importance_data["Linear Regression"]["Leave One Out Encoded"]["Test MAE"]]
        }, index=["Leave One Out Encoded"]).T)

        feature_importance = feature_importance_data["Linear Regression"]["Leave One Out Encoded"]["Feature Importance"]
        df = pd.DataFrame(feature_importance.items(), columns=["Feature", "Importance"]).set_index("Feature")
        expand3 = st.checkbox("Show full table", value=False)
        

    # Display first 5 rows by default, or full DataFrame if expanded
        if expand3:
            st.dataframe(df)
        else:
            st.dataframe(df.head())  # Shows only the first 5 rows
    
    if optimisation_choice == "K-Means Clustering":
        st.write("**Mean Absolute Error (MAE) Scores:**")
        st.dataframe(pd.DataFrame({
            "Train": [feature_importance_data["Linear Regression"]["Clusters"]["Train MAE"]],
            "Test":  [feature_importance_data["Linear Regression"]["Clusters"]["Test MAE"]]
        }, index=["K-Means Clustering"]).T)

        feature_importance = feature_importance_data["Linear Regression"]["Clusters"]["Feature Importance"]
        df = pd.DataFrame(feature_importance.items(), columns=["Feature", "Importance"]).set_index("Feature")
        expand4 = st.checkbox("Show full table", value=False, key="expand4")
        if expand4:
            st.dataframe(df)
        else:
            st.dataframe(df.head()) 
    
    if optimisation_choice == "Time Lag Variables":
        st.write("**Mean Absolute Error (MAE) Scores:**")
        st.dataframe(pd.DataFrame({
            "Train": [feature_importance_data["Linear Regression"]["Lag"]["Train MAE"]],
            "Test":  [feature_importance_data["Linear Regression"]["Lag"]["Test MAE"]]
        }, index=["Time Lag Variables"]).T)

        feature_importance = feature_importance_data["Linear Regression"]["Lag"]["Feature Importance"]
        df = pd.DataFrame(feature_importance.items(), columns=["Feature", "Importance"]).set_index("Feature")
        expand5 = st.checkbox("Show full table", value=False, key="expand5")
        if expand5:
            st.dataframe(df)
        else:
            st.dataframe(df.head()) 
    
    if optimisation_choice == "Hyperparameter Optimisation":
        st.write("**Mean Absolute Error (MAE) Scores:**")
        st.dataframe(pd.DataFrame({
            "Train": [feature_importance_data["Linear Regression"]["Without Region or Continent"]["Train MAE"],
                      feature_importance_data["Random Forest Regressor"]["Without Region or Continent"]["Train MAE"],
                      feature_importance_data["Random Forest Regressor"]["Optimised"]["Train MAE"],
                      feature_importance_data["XGBoost"]["Optmised"]["Train MAE"]],
            "Test":  [feature_importance_data["Linear Regression"]["Without Region or Continent"]["Test MAE"],
                      feature_importance_data["Random Forest Regressor"]["Without Region or Continent"]["Test MAE"],
                      feature_importance_data["Random Forest Regressor"]["Optimised"]["Test MAE"],
                      feature_importance_data["XGBoost"]["Optmised"]["Test MAE"]]
        }, index=["Linear Regression", "Random Forest Regressor (Original)", "Random Forest Regressor (Tuned)", "XGBoost (Tuned)"]).T)
    
    if optimisation_choice == "Ridge Regression":
        Coeffgraph = Image.open("Streamlit Pics/coeffvalue.png")
        st.image(Coeffgraph, use_container_width=False)

        MAEgraph = Image.open("Streamlit Pics/maevalue.png")
        st.image(MAEgraph, use_container_width=False)

# Expander: Stratification Analysis & Conclusions
with st.expander("### 🔍 Feature Importance"):
    st.markdown("""
    **Stratification Analysis:**
    - **Gender**: Training models to predict Female tobacco use and Male tobacco use  
    - **Income Level:** Separate models for high- and low-income countries revealed differing sensitivities to policy measures.  
    - **Continental Stratification:** Training models for each continent uncovered region-specific policy effects.
    """)

    # Selection box for user to choose analysis type
    stratification_type = st.radio(
        "Select Stratification Type:",
        ["Gender", "Income Level", "Continent"]
    )

    # Load corresponding feature importances dynamically
    if stratification_type == "Gender":
        st.markdown("#### **Tobacco Use by Gender**")
        st.write("""
        **Key Observations**:
        - **Cigarette prices** had a stronger **negative** effect on male tobacco use, indicating higher price sensitivity.
        - **Cessation support** showed greater impact on women.
        - **Exposure protection** had modest effects across all groups.
        - **Income group** was **positively** associated with female tobacco use, suggesting cultural or socioeconomic influences.
        """)
        
        # Display MAE scores for Female and Male
        st.write("**Mean Absolute Error (MAE) Scores:**")
        st.dataframe(pd.DataFrame({
            "Train": [feature_importance_data["Gender"]["Female"]["Train MAE"], feature_importance_data["Gender"]["Male"]["Train MAE"]],
            "Test": [feature_importance_data["Gender"]["Female"]["Test MAE"], feature_importance_data["Gender"]["Male"]["Test MAE"]]
        }, index=["Female", "Male"]).T)

         # Dropdown to select feature importance for either Male or Female
        feature_choice = st.selectbox(
            "Select Gender for Feature Importance",
            options=["Female", "Male"],
            index=0  # Default to "Female"
        )

        if feature_choice == "Female":
            st.subheader(f"Feature Importance for {feature_choice}")
            feature_importance = feature_importance_data["Gender"]["Female"]["Feature Importance"]
        elif feature_choice == "Male":
            st.subheader(f"Feature Importance for {feature_choice}")
            feature_importance = feature_importance_data["Gender"]["Male"]["Feature Importance"]

        df = pd.DataFrame(feature_importance.items(), columns=["Feature", "Importance"]).set_index("Feature")
        expand6 = st.checkbox("Show full table", value=False, key="expand6")
        if expand6:
            st.dataframe(df)
        else:
            st.dataframe(df.head()) 

    elif stratification_type == "Income Level":
        st.markdown("#### **Tobacco Use by Income Level**")
        st.write("""
        **Key Observations**:
        - Some policies had similar predictive importance across income groups.
        - **Raise taxes** was positively correlated with tobacco use in both models, suggesting it to be lagging indicator. 
        - **Cessation support** was similarly negatively correlated with tobacco use across both groups.
        - Counterintuitively, **cigarette prices** were negatively correlated with tobacco use in **high income countries** and positively correlated in **low income countries**. It is possible that black market alternatives may play a greater role in the latter group.
        """)

        # Display MAE scores for Low and High income groups
        st.write("**Mean Absolute Error (MAE) Scores by Income Level:**")
        st.dataframe(pd.DataFrame({
            "Train": [feature_importance_data["Income"]["Low Income Group"]["Train MAE"], 
                    feature_importance_data["Income"]["High Income Group"]["Train MAE"]],
            "Test": [feature_importance_data["Income"]["Low Income Group"]["Test MAE"], 
                    feature_importance_data["Income"]["High Income Group"]["Test MAE"]]
        }, index=["Low Income Group", "High Income Group"]).T)

        # Radio buttons to select feature importance for Low or High income levels
        income_choice = st.selectbox(
            "Select Income Level for Feature Importance",
            options=["Low Income Group", "High Income Group"],
            index=0  # Default to "Low"
        )

        # Display the selected feature importance table for the selected income level
        st.subheader(f"Feature Importance for {income_choice}")
        income_importance = feature_importance_data["Income"][income_choice]["Feature Importance"]
        df = pd.DataFrame(income_importance.items(), columns=["Feature", "Importance"]).set_index("Feature")
        expand7 = st.checkbox("Show full table", value=False, key="expand7")
        if expand7:
            st.dataframe(df)
        else:
            st.dataframe(df.head()) 

    elif stratification_type == "Continent":
        st.markdown("#### **Tobacco Use By Continent**")
        st.write("""
        **Key Observations**: 
        - **Tax increase** appears as an important factor for 4 out of the 6 continents, and is positive in all of them, suggesting it to be a lagging indicator.
        - **Cigarette prices** are an important factor in **Europe & Central Asia**, but not universally. In areas like **Sub-Saharan Africa**, the coefficient for cigarette prices is positive, reflecting what we found in our income stratified models. 
        - **Risk warnings** are important globally, appearing for 5 of the 6 continents, and while the impact varies, on the whole it is negatively associated with tobacco use. 
        - The importance of **Year** in **South Asia** suggests a natural decline in tobacco use independent of policy interventions, unlike for other continents.
        """)
    
        st.write("**Mean Absolute Error (MAE) Scores by Continent:**")
        st.dataframe(pd.DataFrame({
            "Train": [feature_importance_data["Continent"]["South Asia"]["Train MAE"], 
                    feature_importance_data["Continent"]["Europe & Central Asia"]["Train MAE"],
                    feature_importance_data["Continent"]["Middle East & North Africa"]["Train MAE"],
                    feature_importance_data["Continent"]["East Asia & Pacific"]["Train MAE"],
                    feature_importance_data["Continent"]["Americas"]["Train MAE"],
                    feature_importance_data["Continent"]["Sub-Saharan Africa"]["Train MAE"]],
            "Test": [feature_importance_data["Continent"]["South Asia"]["Test MAE"],
                     feature_importance_data["Continent"]["Europe & Central Asia"]["Test MAE"],
                     feature_importance_data["Continent"]["Middle East & North Africa"]["Test MAE"],
                     feature_importance_data["Continent"]["East Asia & Pacific"]["Test MAE"],
                     feature_importance_data["Continent"]["Americas"]["Test MAE"],
                     feature_importance_data["Continent"]["Sub-Saharan Africa"]["Test MAE"]]
                }, index=["South Asia", "Europe & Central Asia", "Middle East & North Africa", "East Asia & Pacific", "Americas", "Sub-Saharan Africa"]).T)
        # Radio buttons to select feature importance for Low or High income levels
        continent_choice = st.selectbox(
            "Select Continent for Feature Importance",
            options=["South Asia", "Europe & Central Asia", "Middle East & North Africa", "East Asia & Pacific", "Americas", "Sub-Saharan Africa"],
            index=0  # Default to "South Asia"
        )

        # Display the selected feature importance table for the selected income level
        st.subheader(f"Feature Importance for {continent_choice}")
        continent_choice = feature_importance_data["Continent"][continent_choice]["Feature Importance"]
        df = pd.DataFrame(continent_choice.items(), columns=["Feature", "Importance"]).set_index("Feature")
        expand8 = st.checkbox("Show full table", value=False, key="expand8")
        if expand8:
            st.dataframe(df)
        else:
            st.dataframe(df.head()) 
        