import streamlit as st

home_page = st.Page("Streamlit_Homepage.py", title="Home", icon="🏠")
intro_page = st.Page("Pages/01_Introduction.py", title="Introduction", icon="📚")
presentation_page = st.Page("Pages/02_Data_Presentation.py", title = "Data Presentation", icon="🗂️")
exp_page = st.Page("Pages/03_Exploratory_Analysis.py", title = "Exploratory Analysis", icon="📊")
pre_page =st.Page("Pages/04_Preprocessing.py", title = "Preprocessing", icon="🧹")
ml_page = st.Page("Pages/05_ML_Modeling.py", title="Machine Learning", icon="🤖")
stats_page = st.Page("Pages/06_Statistical_Modeling.py", title="Statistical Analysis", icon="📈")
conc_page = st.Page("Pages/08_Conclusion_and_Outlook.py", title="Conclusion", icon="🏁")

pg = st.navigation([home_page, intro_page, presentation_page, exp_page, pre_page, ml_page, stats_page, conc_page])
pg.run()