import streamlit as st
import seaborn as sns 
import plotly.express as px
import pandas as pd 

# Page Config
st.set_page_config(page_title="Netflix Data Analysis", layout="wide")

# Custom CSS 
st.markdown("""
    <style>
    body {
        background: linear-gradient(to right, #f9fafc, #e9ecef);
        color: #222;
        font-family: 'Trebuchet MS', sans-serif;
    }
    .title-style {
        font-size: 50px;
        font-weight: bold;
        color: #e50914;
        text-shadow: 2px 2px 5px #fff2f2;
        animation: glow 2s ease-in-out infinite alternate;
    }
    @keyframes glow {
        from { text-shadow: 0 0 10px #ffe5e5; }
        to { text-shadow: 0 0 20px #e50914, 0 0 30px #e50914; }
    }
    section[data-testid="stSidebar"] {
        background-color: #f5f6fa;
        padding: 20px;
        color: #222;
    }
    .stDataFrame {
        font-family: 'Trebuchet MS', sans-serif;
        background-color: #f9f9f9;
        color: #333;
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


# Title and Intro
st.markdown('<div class="title-style">📊 Netflix Data Analysis</div>', unsafe_allow_html=True)
st.markdown("This dashboard gives the analysis of Netflix content using interactive filters and visualizations.")



df = pd.read_csv("netflix_titles.csv")
df

# --- Sidebar Filters ---
st.sidebar.header("🎛️ Filter Options")

with st.sidebar.expander("Filter by Type"):
    type_options = df['type'].dropna().unique().tolist()
    selected_types = st.multiselect("Select Type", options=type_options, default=type_options)

with st.sidebar.expander("Filter by Country"):
    country_options = df['country'].dropna().unique().tolist()
    selected_countries = st.multiselect("Select Country", options=country_options, default=country_options[:10])

with st.sidebar.expander("Filter by Release Year"):
    min_year, max_year = int(df['release_year'].min()), int(df['release_year'].max())
    selected_years = st.slider("Select Release Year Range", min_value=min_year, max_value=max_year, value=(min_year, max_year))

# --- Place Rating and Duration in separate boxes ---
with st.sidebar.expander("Filter by Rating"):
    rating_options = df['rating'].dropna().unique().tolist()
    selected_ratings = st.multiselect("Select Rating", options=rating_options, default=rating_options)

with st.sidebar.expander("Filter by Duration (Movies Only)"):
    min_duration = int(df[df['type'] == 'Movie']['duration'].str.extract(r'(\d+)').dropna().astype(int).min())
    max_duration = int(df[df['type'] == 'Movie']['duration'].str.extract(r'(\d+)').dropna().astype(int).max())
    selected_duration = st.slider("Select Duration Range (min)", min_value=min_duration, max_value=max_duration, value=(min_duration, max_duration))


# Filter the dataframe
filtered_df = df[
    (df['type'].isin(selected_types)) &
    (df['country'].isin(selected_countries)) &
    (df['release_year'] >= selected_years[0]) &
    (df['release_year'] <= selected_years[1]) &
    (df['rating'].isin(selected_ratings))
]


# Scatter Chart: Release Year vs Duration (for Movies only)
st.markdown("### 🎥 Scatter Chart: Release Year vs Duration (Movies)")

fig1 = filtered_df[filtered_df['type'] == 'Movie'].dropna(subset=['release_year', 'duration'])
# Extract numeric duration in minutes
fig1['duration_min'] = fig1['duration'].str.extract('(\d+)').astype(float)
fig1 = px.scatter(fig1, x='release_year', y='duration_min', color='rating',
                  title='Release Year vs Duration (Movies)', labels={'duration_min': 'Duration (min)'})

fig1.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white', family='Trebuchet MS'),
    title_font=dict(size=22),
    hoverlabel=dict(bgcolor="white", font_size=12, font_family="Trebuchet MS")
)
st.plotly_chart(fig1)
st.markdown("""
<div style='font-size:16px; line-height:1.6;'>
📌 The scatter chart visualizes the relationship between <strong>release year</strong> and <strong>duration</strong> of movies on Netflix.  
Each point represents a movie, colored by its <strong>rating</strong>.  
<br>
🔍 This helps identify trends in movie lengths over time—whether movies are getting longer or shorter.  
🎨 Color coding reveals how content ratings relate to duration.  
<br>
💡 Look for clusters or outliers to spot interesting patterns in Netflix’s movie catalog.
</div>
""", unsafe_allow_html=True)


# Line Chart: Number of Titles Released per Year
st.markdown("### 📈 Line Chart: Number of Titles Released per Year")
year_count = filtered_df['release_year'].value_counts().sort_index()
fig2 = px.line(x=year_count.index, y=year_count.values, labels={'x': 'Release Year', 'y': 'Number of Titles'},
               title='Number of Titles Released per Year')
fig2.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white', family='Trebuchet MS'),
    title_font=dict(size=22),
    hoverlabel=dict(bgcolor="white", font_size=12, font_family="Trebuchet MS")
)
st.plotly_chart(fig2)

# Analysis of Line Chart
st.markdown("""
<div style='font-size:16px; line-height:1.6;'>
📊 This line chart shows how many Netflix titles were released each year.  
<br>
🔺 Peaks highlight years with a surge in content production.  
🔻 Dips may reflect strategic shifts or external disruptions (like global events).  
<br>
📈 Tracking this trend helps understand Netflix’s growth and evolving content strategy over time.
</div>
""", unsafe_allow_html=True)


# Bar Chart: Top 10 Countries by Number of Titles
st.markdown("### 🌍 Bar Chart: Top 10 Countries by Number of Titles")
country_count = filtered_df['country'].value_counts().head(10).reset_index()
country_count.columns = ['country', 'count']
fig3 = px.bar(
    country_count,
    x='country',
    y='count',
    color='country',  # Optional: gives each bar a different color
    labels={'country': 'Country', 'count': 'Number of Titles'},
    title='Top 10 Countries by Number of Titles',
    color_discrete_sequence=px.colors.qualitative.Safe
)
fig3.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    font=dict(color='white', family='Trebuchet MS'),
    title_font=dict(size=22),
    hoverlabel=dict(bgcolor="white", font_size=12, font_family="Trebuchet MS"),
    showlegend=False
)

st.plotly_chart(fig3)
# Analysis
st.markdown("""
<div style='font-size:16px; line-height:1.6;'>
📊 This bar chart highlights the <strong>top 10 countries</strong> contributing the most titles to Netflix.  
<br>
🌐 It reveals the <strong>geographic distribution</strong> of content, showing which regions dominate the platform.  
<br>
💡 Use this to understand regional content strengths and global licensing trends.
</div>
""", unsafe_allow_html=True)



st.markdown("### 🥧 Pie Chart: Distribution by Content Type")
type_count = df['type'].value_counts()
fig4 = px.pie(
    names=type_count.index,
    values=type_count.values,
    title='🥧 Distribution by Content Type',
    color_discrete_sequence=px.colors.qualitative.Pastel
)
fig4.update_layout(
    font=dict(color='white', family='Trebuchet MS'),
    paper_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig4, use_container_width=True)

# 🔵 Bubble Chart
st.markdown("### 🔵 Bubble Chart: Number of Titles by Country and Type")
top_countries = df['country'].value_counts().head(10).index
bubble_df = df[df['country'].isin(top_countries)]
bubble_data = bubble_df.groupby(['country', 'type']).size().reset_index(name='count')
fig5 = px.scatter(
    bubble_data,
    x='country',
    y='type',
    size='count',
    color='type',
    title='🔵 Number of Titles by Country and Type',
    size_max=60
)
fig5.update_layout(
    font=dict(color='white', family='Trebuchet MS'),
    paper_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig5, use_container_width=True)

# 🌞 Sunburst Chart
st.markdown("### 🌞 Sunburst Chart: Genre by Country and Type")
df_exploded = df.dropna(subset=['listed_in', 'country', 'type']).copy()
df_exploded['genre'] = df_exploded['listed_in'].str.split(', ')
df_exploded = df_exploded.explode('genre')
top_countries = df_exploded['country'].value_counts().head(10).index
sunburst_df = df_exploded[df_exploded['country'].isin(top_countries)]
fig6 = px.sunburst(
    sunburst_df,
    path=['country', 'type', 'genre'],
    title='🌞 Genres by Country and Type'
)
fig6.update_layout(
    font=dict(color='white', family='Trebuchet MS'),
    paper_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig6, use_container_width=True)

# 📦 Box Plot: Movie Duration by Rating
st.markdown("### 📦 Box Plot: Movie Duration by Rating")

# Filter and prepare data
movies_df = df[df['type'] == 'Movie'].dropna(subset=['duration', 'rating']).copy()
movies_df['duration_min'] = movies_df['duration'].str.extract(r'(\d+)').astype(float)

# Create box plot
fig7 = px.box(
    movies_df,
    x='rating',
    y='duration_min',
    color='rating',
    title='📦 Movie Duration by Rating',
    labels={'duration_min': 'Duration (min)', 'rating': 'Rating'},
    color_discrete_sequence=px.colors.qualitative.Set3
)

# Apply dark theme styling
fig7.update_layout(
    font=dict(color='white', family='Trebuchet MS'),
    paper_bgcolor='rgba(0,0,0,0)',
    plot_bgcolor='rgba(0,0,0,0)',
    title_font=dict(size=22)
)

st.plotly_chart(fig7, use_container_width=True)

# Analysis
st.markdown("""
<div style='font-size:16px; line-height:1.6;'>
📦 This box plot shows how <strong>movie durations</strong> vary across different <strong>ratings</strong>.  
<br>
Each box represents the interquartile range (IQR), with the median marked inside.  
Outliers are shown as individual points.  
<br>
🎯 Use this to explore whether certain ratings tend to have longer or shorter movies.
</div>
""", unsafe_allow_html=True)

# 📊 Histogram
st.markdown("### 📊 Histogram: Movie Duration Distribution")
fig8 = px.histogram(
    movies_df,
    x='duration_min',
    nbins=30,
    title='📊 Distribution of Movie Durations',
    labels={'duration_min': 'Duration (min)'}
)
fig8.update_layout(
    font=dict(color='white', family='Trebuchet MS'),
    paper_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig8, use_container_width=True)

# 📈 KDE + Violin Plot
st.markdown("### 📈 Distribution Plot: Movie Duration with Density Curve")
fig9 = px.histogram(
    movies_df,
    x='duration_min',
    nbins=30,
    histnorm='probability density',
    marginal='violin',
    title='📈 Movie Duration Distribution with Density Curve',
    labels={'duration_min': 'Duration (min)'}
)
fig9.update_layout(
    font=dict(color='white', family='Trebuchet MS'),
    paper_bgcolor='rgba(0,0,0,0)'
)
st.plotly_chart(fig9, use_container_width=True)

# 🎞️ Animated Bar Chart: Number of Titles by Type Over the Years
st.markdown("### 🎞️ Animated Bar Chart: Number of Titles by Type Over the Years")

# Prepare data
type_year = df.dropna(subset=['release_year', 'type'])
type_year_count = type_year.groupby(['release_year', 'type']).size().reset_index(name='count')

# Create animated bar chart
fig_anim2 = px.bar(
    type_year_count,
    x='type',
    y='count',
    color='type',
    animation_frame='release_year',
    range_y=[0, type_year_count['count'].max() + 20],
    title='📽️ Number of Titles by Type Over the Years (Animated)',
    labels={'count': 'Number of Titles', 'type': 'Type', 'release_year': 'Release Year'},
    color_discrete_sequence=px.colors.qualitative.Set2
)

# Apply light theme styling
fig_anim2.update_layout(
    plot_bgcolor='rgba(255,255,255,1)',   # White background for plot area
    paper_bgcolor='rgba(255,255,255,1)',  # White background for figure
    font=dict(color='black', family='Trebuchet MS'),
    title_font=dict(size=22, color='black'),
    transition=dict(duration=500),
    updatemenus=[
        {
            "buttons": [
                {
                    "args": [None, {"frame": {"duration": 500, "redraw": True},
                                    "fromcurrent": True, "transition": {"duration": 300}}],
                    "label": "Play",
                    "method": "animate"
                },
                {
                    "args": [[None], {"frame": {"duration": 0, "redraw": False},
                                      "mode": "immediate",
                                      "transition": {"duration": 0}}],
                    "label": "Pause",
                    "method": "animate"
                }
            ],
            "direction": "left",
            "pad": {"r": 10, "t": 87},
            "showactive": False,
            "type": "buttons",
            "x": 0.1,
            "xanchor": "right",
            "y": 0,
            "yanchor": "top",
            "bgcolor": "#e50914",      # Netflix Red for play/pause button background
            "bordercolor": "#e50914",  # Netflix Red border
            "font": {"color": "white", "family": "Trebuchet MS"}
        }
    ]
)
st.plotly_chart(fig_anim2, use_container_width=True)

# Analysis
st.markdown("""
<div style='font-size:16px; line-height:1.6;'>
🎬 This animated bar chart shows how the number of <strong>Movies</strong> and <strong>TV Shows</strong> on Netflix has evolved over time.  
<br>
📅 Each frame represents a different year, allowing you to visually track trends in content production.  
<br>
📈 Use this to spot growth patterns, shifts in strategy, or the rise of specific content types.
</div>
""", unsafe_allow_html=True)

# Add a footer 
st.markdown("Created by Riddhi ")
