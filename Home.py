import streamlit as st
import pandas as pd
import plotly.express as px 
import seaborn as sns 
import matplotlib.pyplot as plt


st.set_page_config(page_title="Netflix Dashboard", layout="wide")
# Custom CSS Styling for Light Theme
st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #f9fafc, #e9ecef);
        color: #222;
        font-family: 'Trebuchet MS', sans-serif;
    }
    .title-style {
        font-size: 48px;
        font-weight: bold;
        color: #e50914;
        text-shadow: 1px 1px 4px #fff2f2;
        animation: glow 2s ease-in-out infinite alternate;
    }
        @keyframes glow {
        from { text-shadow: 0 0 10px #ffe5e5; }
        to { text-shadow: 0 0 20px #e50914, 0 0 30px #e50914; }
    }
    .metric-style {
        background-color: #fff;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 0 10px #e0e0e0;
        color: #e50914;
        transition: transform 0.2s ease-in-out;
    }
    .metric-style:hover {
        transform: scale(1.05);
        box-shadow: 0 0 20px #ffd6d6;
    }
    .stDataFrame {
        font-family: 'Trebuchet MS', sans-serif;
        background-color: #f9f9f9;
        color: #333;
    }
    /* Sidebar styling */
    section[data-testid="stSidebar"] {
        background-color: #f5f6fa;
        padding: 20px;
        color: #222;
    }
    .sidebar .sidebar-content {
        color: #222;
    }
    .sidebar .sidebar-content h1 {
        color: #e50914;
    }
    /* Button styling */
    div.stButton > button {
        background: linear-gradient(to right, #e50914, #ff6363);
        color: white;
        border: none;
        padding: 0.75em 2em;
        border-radius: 30px;
        font-size: 16px;
        font-weight: bold;
        transition: all 0.3s ease-in-out;
        box-shadow: 0 4px 15px rgba(229, 9, 20, 0.15);
    }
    div.stButton > button:hover {
        background: linear-gradient(to right, #ff6363, #e50914);
        transform: scale(1.05);
        box-shadow: 0 6px 20px rgba(229, 9, 20, 0.25);
    }
    </style>
""", unsafe_allow_html=True)

# Header Section
col1, col2 = st.columns([1, 2])
with col1:
    st.image("https://m.media-amazon.com/images/I/31JfJ6dXD9L.png", width=200)

with col2:
    st.markdown('<div class="title-style">🍿 Netflix Dashboard</div>', unsafe_allow_html=True)
    st.markdown("""
        Welcome to the Netflix Dashboard!  
        Explore insights and visualizations about Netflix content.
    """)



# Load Data
@st.cache_data
def load_data():
    df = pd.read_csv("netflix_titles.csv")
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("Filters")
if "date_added" in df.columns:
    df['year_added'] = pd.to_datetime(df['date_added'], errors='coerce').dt.year
    year_options = sorted(df['year_added'].dropna().unique(), reverse=True)
    year = st.sidebar.selectbox("Select Year", options=year_options)
    filtered_df = df[df['year_added'] == year]
else:
    filtered_df = df

# Metrics Section
st.markdown("### 📊 Key Metrics")
col3, col4, col5 = st.columns(3)
with col3:
    st.markdown('<div class="metric-style">🎞️<br>' + f"<h4>Total Titles</h4><h2>{len(filtered_df)}</h2></div>", unsafe_allow_html=True)
with col4:
    st.markdown('<div class="metric-style">🎬<br>' + f"<h4>Movies</h4><h2>{filtered_df[filtered_df['type'] == 'Movie'].shape[0]}</h2></div>", unsafe_allow_html=True)
with col5:
    st.markdown('<div class="metric-style">📺<br>' + f"<h4>TV Shows</h4><h2>{filtered_df[filtered_df['type'] == 'TV Show'].shape[0]}</h2></div>", unsafe_allow_html=True)


# Sample Data
st.subheader("🎬 Sample of Netflix Data")
st.dataframe(filtered_df.head().style.set_properties(**{
    'background-color': '#f9f9f9',
    'color': '#333',
    'font-family': 'Trebuchet MS',
    'border': '1px solid #ddd'
}))

# Visualization: Titles Added Per Year
if "year_added" in df.columns:
    year_counts = df['year_added'].value_counts().sort_index()
    fig = px.bar(
        x=year_counts.index,
        y=year_counts.values,
        labels={'x': 'Year Added', 'y': 'Number of Titles'},
        title="📈 Titles Added Per Year",
        color_discrete_sequence=["#94761c"]
    )
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', family='Trebuchet MS'),
        title_font=dict(size=24)
    )
    st.plotly_chart(fig, use_container_width=True)



if st.button("Dashboard"):
    st.switch_page("pages/Dashboard.py")


    
st.markdown("<hr><center>Created by Riddhi ", unsafe_allow_html=True)
