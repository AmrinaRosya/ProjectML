# netflix_dashboard_netflix_style.py
import streamlit as st
import pandas as pd
import plotly.express as px

# --- CONFIG
st.set_page_config(page_title="Netflix-style Dashboard", layout="wide")

# --- CUSTOM CSS Netflix Color Palette
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;700&display=swap');

    html, body, [class*="css"]  {
        font-family: 'Roboto', sans-serif;
        background-color: #000000 !important;
        color: #FFFFFF !important;
        font-size: 18px !important;
        font-weight: 700 !important;
    }

    .stApp, .main, .block-container, .css-18e3th9, .css-1d391kg, .css-1outpf7 {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }

    .stMetric {
        background-color: #666666;
        border-radius: 12px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        box-shadow: 0 4px 10px rgba(255, 255, 255, 0.05);
        text-align: center;
        color: white;
    }

    .stMetricLabel {
        color: #ffffff !important;
        font-weight: 900 !important;
        font-size: 20px !important;
    }

    h1, h2, h3, h5, .stText, .stMarkdown, .stDataFrame, .stPlotlyChart {
        color: #FFFFFF !important;
        font-weight: 700 !important;
    }

    .sidebar .sidebar-content {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }

    .css-1v0mbdj, .css-1d391kg, .css-1outpf7, .css-ffhzg2 {
        background-color: #000000 !important;
        color: #FFFFFF !important;
    }
    </style>
""", unsafe_allow_html=True)

# --- LOAD DATA ---
df = pd.read_csv("netflix_titles.csv")
df['date_added'] = pd.to_datetime(df['date_added'], errors='coerce')
df['year_added'] = df['date_added'].dt.year
df['main_genre'] = df['listed_in'].str.split(',').str[0]

# --- TITLE ---
st.image("https://raw.githubusercontent.com/rosyada/netflix-dashboard/main/Netflix.jpg", width=250)
st.title("Netflix Content Dashboard")

# --- YEAR FILTER (in main page) ---
st.subheader("Pilih Rentang Tahun Ditambahkan")
year_range = st.slider("", 
                       int(df['year_added'].min()), 
                       int(df['year_added'].max()), 
                       (2015, 2021))
df_filtered = df[(df['year_added'] >= year_range[0]) & (df['year_added'] <= year_range[1])]

# --- KPIs ---
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown('<p class="stMetricLabel">Total Konten</p>', unsafe_allow_html=True)
    st.metric(label="", value=f"{df_filtered.shape[0]:,}")
with col2:
    st.markdown('<p class="stMetricLabel">Jumlah Film</p>', unsafe_allow_html=True)
    st.metric(label="", value=f"{df_filtered[df_filtered['type']=='Movie'].shape[0]:,}")
with col3:
    st.markdown('<p class="stMetricLabel">Jumlah TV Show</p>', unsafe_allow_html=True)
    st.metric(label="", value=f"{df_filtered[df_filtered['type']=='TV Show'].shape[0]:,}")

# --- VISUAL 1: Pie Chart Type ---
type_count = df_filtered['type'].value_counts().reset_index()
type_count.columns = ['type', 'count']
fig1 = px.pie(type_count, names='type', values='count', title="Distribusi Tipe Konten",
              color_discrete_sequence=['#FF1717', '#666666'])
fig1.update_layout(paper_bgcolor='#000000', font_color='white', title_font_color='white', legend_font_color='white')
st.plotly_chart(fig1, use_container_width=True)

# --- VISUAL 2: Konten Ditambahkan per Tahun ---
yearly = df.groupby('year_added').size().reset_index(name='count')
fig2 = px.line(yearly, x='year_added', y='count', title="Jumlah Konten Ditambahkan per Tahun", markers=True,
               line_shape='linear')
fig2.update_traces(line=dict(color='#E50914'))
fig2.update_layout(paper_bgcolor='#000000', plot_bgcolor='#1a1a1a', font_color='white', title_font_color='white')

# --- VISUAL 3: Negara Asal Terbanyak ---
top_countries = df_filtered['country'].value_counts().nlargest(10).reset_index()
top_countries.columns = ['country', 'count']
fig3 = px.bar(top_countries, x='country', y='count', title="Top 10 Negara Asal Konten",
              color_discrete_sequence=['#FF1717'])
fig3.update_layout(paper_bgcolor='#000000', plot_bgcolor='#1a1a1a', font_color='white', title_font_color='white')

# --- VISUAL 4: Genre Populer ---
top_genres = df_filtered['main_genre'].value_counts().nlargest(10).reset_index()
top_genres.columns = ['genre', 'count']
fig4 = px.bar(top_genres, x='genre', y='count', title="Top Genre di Netflix",
              color_discrete_sequence=['#FF1717'])
fig4.update_layout(paper_bgcolor='#000000', plot_bgcolor='#1a1a1a', font_color='white', title_font_color='white')

# --- VISUAL 5: Rating ---
top_ratings = df_filtered['rating'].value_counts().nlargest(10).reset_index()
top_ratings.columns = ['rating', 'count']
fig5 = px.bar(top_ratings, x='rating', y='count', title="Distribusi Rating",
              color_discrete_sequence=['#FF1717'])
fig5.update_layout(paper_bgcolor='#000000', plot_bgcolor='#1a1a1a', font_color='white', title_font_color='white')

# --- VISUAL 6: Tahun Rilis ---
release_year = df_filtered['release_year'].value_counts().sort_index().reset_index()
release_year.columns = ['release_year', 'count']
fig6 = px.area(release_year, x='release_year', y='count', title="Distribusi Tahun Rilis",
              color_discrete_sequence=['#FF1717'])
fig6.update_layout(paper_bgcolor='#000000', plot_bgcolor='#1a1a1a', font_color='white', title_font_color='white')

# --- LAYOUT VISUALS ---
col4, col5 = st.columns(2)
col4.plotly_chart(fig2, use_container_width=True)
col5.plotly_chart(fig3, use_container_width=True)

col6, col7 = st.columns(2)
col6.plotly_chart(fig4, use_container_width=True)
col7.plotly_chart(fig5, use_container_width=True)

st.plotly_chart(fig6, use_container_width=True)

# --- ABOUT ---
with st.expander("Tentang Dashboard"):
    st.markdown("""
        Dashboard ini dibuat dari dataset Netflix Titles dari Kaggle.
        Anda dapat menganalisis tren konten berdasarkan jenis, negara, genre, tahun rilis, dan rating.
    """)

