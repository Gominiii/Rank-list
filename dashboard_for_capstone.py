# -*- coding: utf-8 -*-
"""dashboard for capstone.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1B7jBvEW-8lV9DKdvXUSpRk46Kvy8rdbm
"""

!pip install streamlit

!pip install textblob

import streamlit as st
import pandas as pd
from textblob import TextBlob
import matplotlib.pyplot as plt

hospital_data = pd.read_excel("/content/hospital_data_v3 (2).xlsx")
ranked_hospitals = pd.read_excel("/content/ranked_hospitals_weighted_with_metrics (1).xlsx")
sentiment_scores = pd.read_excel("/content/sentiment score rank list.xlsx")

st.title("Hospital Reviews Sentiment Analysis Dashboard")

# Sidebar filters
st.sidebar.title("Filter Hospitals")
localities = st.sidebar.multiselect(
    'Select Locality',
    hospital_data['Locality'].unique(),
    default=hospital_data['Locality'].unique()
)
price_range = st.sidebar.slider(
    'Select Price Range',
    int(hospital_data['Min_price'].min()),
    int(hospital_data['Max_price'].max()),
    (int(hospital_data['Min_price'].min()), int(hospital_data['Max_price'].max()))
)
speciality_count = st.sidebar.slider(
    'Minimum Number of Specialities',
    int(hospital_data['Specialities'].min()),
    int(hospital_data['Specialities'].max()),
    (int(hospital_data['Specialities'].min()), int(hospital_data['Specialities'].max()))
)

# Filtering data based on user input
filtered_data = hospital_data[
    (hospital_data['Locality'].isin(localities)) &
    (hospital_data['Min_price'] >= price_range[0]) &
    (hospital_data['Max_price'] <= price_range[1]) &
    (hospital_data['Specialities'] >= speciality_count[0])
]

# Display hospital data
st.subheader("Filtered Hospital Data")
st.dataframe(filtered_data)

# Visualizing sentiment scores
st.subheader("Hospital Sentiment Scores")
st.bar_chart(filtered_data[['Name', 'Score']].set_index('Name'))

# Displaying ranked hospital details
st.subheader("Hospital Ranking Details")
st.dataframe(ranked_hospitals)

# Display sentiment score ranks
st.subheader("Sentiment Score Rankings")
st.dataframe(sentiment_scores)

# Add filters for more granular sentiment analysis and hospital comparison
st.sidebar.subheader("Compare Hospitals by Score")
selected_hospitals = st.sidebar.multiselect(
    'Select Hospitals for Comparison',
    hospital_data['Name'].unique()
)
if selected_hospitals:
    comparison_data = sentiment_scores[sentiment_scores['Name'].isin(selected_hospitals)]
    st.subheader("Comparison of Selected Hospitals")
    st.bar_chart(comparison_data[['Name', 'Score']].set_index('Name'))