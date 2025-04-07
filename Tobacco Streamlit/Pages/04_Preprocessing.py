import streamlit as st
import pandas as pd
from PIL import Image
from io import StringIO

# Image at the top
image = Image.open('Streamlit Pics/Preprocessing.png')
st.image(image, use_column_width=True)

# Introduction text
st.write("""
In order to proceed with machine learning and statistical modeling we needed to clean, pre-process and merge our data-sets. Below are the cleaned tables and descriptions of the key steps that were taken:
""")

# Data Cleaning section
st.subheader("Data Cleaning")

# MPOWER Table dropdown
with st.expander('MPOWER Table'):
    st.write("""
    Policy implementation was originally rated on a 1-5 scale, with 1 indicating no data. To improve clarity, we adjusted the scale to 0-4, where 0 now represents no data.
    """)
    emp = pd.read_csv("Data/CleanMPOWER.csv")
    st.dataframe(emp)

# Tobacco Control Table dropdown
with st.expander('Tobacco Control Table'):
    st.write("""
    While there were a number of columns that contained potentially relevant information such as the budget that countries were able to allocate to tobacco control and the number of staff in their national tobacco control agency, it was ultimately decided to drop these variables as there were too many missing values as well as currency standardisation issues.
    """)
    tob_ctrl = pd.read_csv("Data/CleanTobaccoControl.csv")
    st.dataframe(tob_ctrl)

# Cigarette Price dropdown
with st.expander('Cigarette Price'):
    st.write("""
    The table originally included both taxes and cigarette prices, but we kept only the latter, as taxes expressed as a percentage of prices did not provide additional meaningful insights. We also removed cigarette prices in local currency and US dollars, opting instead for prices in international dollars—a hypothetical unit that reflects the same purchasing power parity (PPP) as the US dollar at a given point in time. This allows for more accurate cross-country comparisons without exchange rate distortions.
    """)
    price = pd.read_csv('Data/CleanCigarettePrice.csv')
    st.dataframe(price)

# Age Standardised dropdown
with st.expander('Age Standardised Tobacco Prevalence'):
    st.write("""
    Tobacco usage tables included predictions beyond 2022 and data before 2007, which lacked corresponding policy or price data. These were removed. To maintain consistency, we kept only countries present across all datasets, reducing the total from 195 to 162 countries.
    """)
    age = pd.read_csv('Data/CleanTobaccoUseStandardised.csv')
    st.dataframe(age)

# Merging Datasets Section
st.subheader("Merging Datasets")

# Interpolation
df = pd.read_csv('Data/CleanTobaccoUseStandardised.csv')  

# Filter the dataset to keep relevant years
df = df[(df["Year"] >= 2007) & (df["Year"] <= 2022)]
df = df[df["Year"] != 2021]  # Drop 2021
df = df.drop(['Male', 'Female'], axis=1)  # Remove unnecessary columns

# Separate the real 2020 data
Real2020 = df[df["Year"] == 2020]

# Remove 2020 from the dataset for interpolation
Pred = df[df["Year"] != 2020]

# Create a DataFrame ensuring all Regions have 2020 in the dataset
year = [2020]
regions = Pred['Region'].unique()
all_combinations = pd.MultiIndex.from_product([regions, year], names=['Region', 'Year'])
complete_df = pd.DataFrame(index=all_combinations).reset_index()

# Merge with existing data to create the missing 2020 rows
Pred2020_interpolated = complete_df.merge(Pred, on=['Region', 'Year'], how='outer')

# Interpolate missing 2020 values
Pred2020_interpolated['Overall use'] = (
Pred2020_interpolated.groupby('Region')['Overall use']
.transform(lambda x: x.interpolate(method='linear', limit_direction='both'))
)

# Merge interpolated values into the original dataset
compare_df = df.copy()
compare_df = compare_df[compare_df['Year'] == 2020]
compare_df = compare_df.merge(
Pred2020_interpolated[['Region', 'Year', 'Overall use']],
on=['Region', 'Year'],
how='left',
suffixes=('', ' (2020 interpolated)')
)

with st.expander('Handling Missing Values'):
    st.write("""
    Our explanatory variable tables contained data at two-year intervals (2008-2022), but tobacco usage data had mismatched years. Instead of dropping large portions of data, we applied linear interpolation to estimate missing values. Testing on 2020 data showed a mean accuracy within 0.6%, validating this approach. The real 2020 values are compared with the interpolated 2020 values in the table below:
    """)
    st.markdown("<h5 style='font-size: 16px;'>Interpolation Test</h5>", unsafe_allow_html=True)

    # Compute and display mean and max differences
    compare_df_2020 = compare_df[compare_df["Year"] == 2020]
    compare_df_2020['Difference'] = compare_df_2020['Overall use'] - compare_df_2020['Overall use (2020 interpolated)']
    compare_df_2020['Difference'] = compare_df_2020['Difference'].abs()
    mean_diff = compare_df_2020['Difference'].mean()
    max_diff = compare_df_2020['Difference'].max()

    # Display table
    st.dataframe(compare_df_2020)

    st.markdown(f"<h3 style='font-size: 16px;'>Mean Difference between Overall Use and Overall Use (2020 interpolated)(where Year in both columns == 2020): {mean_diff:.4f}</h3>", unsafe_allow_html=True)

# Enhancing Data with New Variables dropdown
with st.expander('Enhancing Data with New Variables'):
    st.write("""
    With WHO datasets for 162 countries ('Region'), we aimed to categorize them into smaller groups by integrating World Bank data on Income Group (Low, Lower Middle, Upper Middle, High) and Continental Classification (South Asia, Europe & Central Asia, Middle East & North Africa, East Asia & Pacific, Sub-Saharan Africa, Latin America & Caribbean, North America). Since naming conventions differed, we used FuzzyWuzzy for approximate matching and filled unmatched entries using a dictionary linking countries to their income group and continent.
    """)
    country = pd.read_csv('Data/CleanCountryClassification.csv', index_col = 0)
    st.dataframe(country)

# Display .info() of merged dataset
with st.expander("Merged Dataset Preview"):
    st.markdown("<h5 style='font-size: 16px;'>Merged Dataset .info Screenshot</h5>", unsafe_allow_html=True)
    merged = pd.read_csv('Data/merged_tobacco_data.csv')
    merged = merged.drop(['Unnamed: 0'], axis = 1)
    st.image("Streamlit Pics/merged_info.png")
    st.markdown("<h5 style='font-size: 16px;'>Merged Dataset</h5>", unsafe_allow_html=True)
    st.dataframe(merged)

