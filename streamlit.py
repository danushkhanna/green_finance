import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
from transformers import pipeline
import PyPDF2
import io

# Initialize BERT pipeline for text classification
@st.cache_resource
def load_model():
    return pipeline("text-classification", 
                   model="yiyanghkust/finbert-esg",
                   return_all_scores=True)

classifier = load_model()

# Function to extract text from PDF or TXT
def extract_text(file, file_type):
    if file_type == "pdf":
        pdf_reader = PyPDF2.PdfReader(file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        return text
    else:  # txt file
        return file.getvalue().decode("utf-8")

# Function to analyze ESG components
def analyze_esg(text):
    # Split text into chunks (BERT has token limits)
    chunks = [text[i:i+512] for i in range(0, len(text), 512)]
    
    results = []
    for chunk in chunks:
        result = classifier(chunk)[0]
        results.append(result)
    
    # Average scores across chunks
    esg_scores = {
        'Environmental': np.mean([r[0]['score'] for r in results]) * 100,
        'Social': np.mean([r[1]['score'] for r in results]) * 100,
        'Governance': np.mean([r[2]['score'] for r in results]) * 100
    }
    
    return esg_scores

# Streamlit App
st.markdown("<h1 style='text-align: center;'>Green Finance Optimiser</h1>", unsafe_allow_html=True)

# Modified file upload to accept both PDF and TXT
uploaded_file = st.file_uploader("Upload Project Document", type=["pdf", "txt"])

if uploaded_file is not None:
    # Determine file type and extract text
    file_type = uploaded_file.name.split('.')[-1].lower()
    text = extract_text(uploaded_file, file_type)
    
    # Analyze ESG components
    esg_scores = analyze_esg(text)
    
    # Calculate risk score (simplified example)
    risk_score = 1 - (sum(esg_scores.values()) / (100 * 3))
    
    # Create DataFrame for visualization
    projects = ['Current Project']
    data = pd.DataFrame({
        'Project': projects,
        'Environmental Score': [esg_scores['Environmental']],
        'Social Score': [esg_scores['Social']],
        'Governance Score': [esg_scores['Governance']],
        'Risk (Low = Good)': [risk_score],
    })

    # Budget slider
    budget = st.slider("Adjust Budget", min_value=50000, max_value=100000, step=5000, value=75000)
    st.write(f"#### Current Budget: ₹{budget:,}")

    # Visualizations
    st.write("### ESG Component Scores")
    fig_bar = px.bar(
        data.melt(id_vars=['Project'], 
                  value_vars=['Environmental Score', 'Social Score', 'Governance Score']),
        x='variable',
        y='value',
        title="ESG Component Analysis",
        labels={'value': 'Score', 'variable': 'Component'}
    )
    st.plotly_chart(fig_bar)

    # Risk Analysis
    st.write("### Risk Analysis")
    fig_gauge = px.bar(data, x='Project', y='Risk (Low = Good)', 
                      title="Project Risk Assessment")
    st.plotly_chart(fig_gauge)

    # Display detailed breakdown
    st.write("### Detailed Project Breakdown")
    st.table(data)