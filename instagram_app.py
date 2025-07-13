import streamlit as st
import pandas as pd
import os

# Full path to the CSV file
DATA_FILE = r"D:\business\research market\instagram_research_data.csv"

COLUMNS = {
    'Business_Name': str,
    'Industry': str,
    'Followers': int,
    'Posts_Count': int,
    'Avg_Likes': float,
    'Avg_Comments': float,
    'Response_Time_Hours': float,
    'DM_Centric': bool,
    'Notes': str
}

@st.cache_data
def load_data():
    if os.path.exists(DATA_FILE):
        df = pd.read_csv(DATA_FILE)
        for col, dtype in COLUMNS.items():
            if col in df.columns:
                try:
                    df[col] = df[col].astype(dtype)
                except:
                    pass
        return df
    else:
        return pd.DataFrame({col: pd.Series(dtype=dtype) for col, dtype in COLUMNS.items()})

def save_data(df):
    df.to_csv(DATA_FILE, index=False)

def analyze_research(df):
    if df.empty:
        return "No data to analyze."
    industry_stats = df.groupby('Industry').agg({
        'Followers': 'mean',
        'Response_Time_Hours': 'mean',
        'DM_Centric': lambda x: sum(x) / len(x) * 100
    }).rename(columns={'DM_Centric': '% Using DMs'})
    return industry_stats

# Streamlit App Interface
st.title("📊 Instagram Business Research Tool")
menu = st.sidebar.radio("Menu", ["Add New Entry", "View Data", "Analyze Data"])
df = load_data()

if menu == "Add New Entry":
    st.subheader("➕ Add New Business Data")
    with st.form("business_form"):
        business_name = st.text_input("Business Name")
        industry = st.selectbox("Industry", ["Clothing", "Food", "Beauty", "Other"])
        followers = st.number_input("Number of Followers", min_value=0, step=1)
        posts = st.number_input("Number of Posts", min_value=0, step=1)
        avg_likes = st.number_input("Average Likes per Post", min_value=0.0)
        avg_comments = st.number_input("Average Comments per Post", min_value=0.0)
        response_time = st.number_input("Response Time (hours)", min_value=0.0)
        dm_centric = st.checkbox("DM-Centric Business?")
        notes = st.text_area("Additional Notes", "")
        submitted = st.form_submit_button("Submit")

        if submitted:
            new_entry = pd.DataFrame([{
                'Business_Name': business_name,
                'Industry': industry,
                'Followers': followers,
                'Posts_Count': posts,
                'Avg_Likes': avg_likes,
                'Avg_Comments': avg_comments,
                'Response_Time_Hours': response_time,
                'DM_Centric': dm_centric,
                'Notes': notes
            }])

            df = pd.concat([df, new_entry], ignore_index=True)
            save_data(df)
            st.success("✅ Business data added successfully!")

elif menu == "View Data":
    st.subheader("📁 All Collected Data")
    if df.empty:
        st.info("No data available.")
    else:
        st.dataframe(df)

elif menu == "Analyze Data":
    st.subheader("📈 Industry Analysis")
    if df.empty:
        st.info("No data to analyze.")
    else:
        st.dataframe(analyze_research(df))

