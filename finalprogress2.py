import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import math
import os
import base64
import io
from PIL import Image

# ==================================================
# 1. PAGE CONFIG & ADVANCED UI/UX STYLING
# ==================================================
st.set_page_config(
    page_title="Discrete Math Graph Project",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🕸️"
)

# --- FUTURISTIC ACADEMIC / DARK GLASSMORPHISM CSS ---
st.markdown("""
<style>
    /* 1. GOOGLE FONTS IMPORT */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;800&family=JetBrains+Mono:wght@400;700&display=swap');

    /* 2. ROOT VARIABLES (Color Palette) */
    :root {
        --bg-dark: #050505;
        --bg-gradient: radial-gradient(circle at top left, #1a1f2c 0%, #050505 100%);
        --glass-bg: rgba(255, 255, 255, 0.03);
        --glass-border: rgba(255, 255, 255, 0.08);
        --glass-shadow: 0 8px 32px 0 rgba(0, 0, 0, 0.37);
        
        --accent-gold: #FFD700;
        --accent-cyan: #4ea8de;
        --accent-purple: #bb86fc;
        
        --text-main: #ECECF1;
        --text-muted: #9ca3af;
        
        --font-ui: 'Inter', sans-serif;
        --font-mono: 'JetBrains Mono', monospace;
    }

    /* 3. GLOBAL RESET & BODY */
    .stApp {
        background: var(--bg-gradient);
        color: var(--text-main);
        font-family: var(--font-ui);
    }
    
    /* Hide Default Header & Hamburger (Optional cleaner look) */
    header[data-testid="stHeader"] {
        background: transparent;
    }
    .stDeployButton {display:none;}
    
    /* 4. TYPOGRAPHY */
    h1, h2, h3 {
        font-weight: 800;
        letter-spacing: -0.5px;
        color: white;
    }
    
    h1 {
        background: linear-gradient(120deg, #ffffff 0%, var(--accent-gold) 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }

    /* 5. SIDEBAR STYLING */
    section[data-testid="stSidebar"] {
        background-color: #0a0a0a;
        border-right: 1px solid var(--glass-border);
    }
    
    /* Custom Navigation Pills (Hacking Streamlit Radios) */
    div[data-testid="stRadio"] > label {
        display: none; /* Hide default label if present */
    }
    div[role="radiogroup"] {
        gap: 8px;
    }
    div[role="radiogroup"] label {
        background: transparent;
        border: 1px solid transparent;
        border-radius: 8px;
        padding: 10px 15px;
        transition: all 0.3s ease;
        color: var(--text-muted);
        font-weight: 500;
        cursor: pointer;
    }
    div[role="radiogroup"] label:hover {
        background: rgba(255, 255, 255, 0.05);
        color: white;
        transform: translateX(5px);
    }
    /* Active State for Radio */
    div[role="radiogroup"] label[data-checked="true"] {
        background: linear-gradient(90deg, rgba(78, 168, 222, 0.15), transparent);
        border-left: 3px solid var(--accent-cyan);
        color: var(--accent-cyan);
        font-weight: 700;
    }

    /* 6. GLASSMORPHISM CARDS (The "Vibe") */
    .glass-card {
        background: var(--glass-bg);
        backdrop-filter: blur(16px);
        -webkit-backdrop-filter: blur(16px);
        border: 1px solid var(--glass-border);
        box-shadow: var(--glass-shadow);
        border-radius: 16px;
        padding: 24px;
        margin-bottom: 20px;
        transition: transform 0.3s ease, border-color 0.3s ease;
        animation: fadeInUp 0.8s ease-out forwards;
    }
    
    .glass-card:hover {
        border-color: rgba(255, 215, 0, 0.3); /* Gold glow on hover */
        transform: translateY(-4px);
    }

    /* 7. INPUTS & WIDGETS */
    /* Selectbox & Number Input */
    .stSelectbox > div > div, .stNumberInput > div > div {
        background-color: rgba(255,255,255,0.03);
        border: 1px solid var(--glass-border);
        color: white;
        border-radius: 8px;
    }
    .stSelectbox > div > div:hover {
        border-color: var(--accent-cyan);
    }

    /* 8. BUTTONS (Gradient & Animation) */
    .stButton > button {
        background: linear-gradient(135deg, #1e293b 0%, #0f172a 100%);
        border: 1px solid var(--glass-border);
        color: var(--accent-cyan);
        font-weight: 600;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 0.85rem;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .stButton > button:hover {
        background: linear-gradient(135deg, var(--accent-cyan) 0%, #2563eb 100%);
        color: white;
        border-color: transparent;
        transform: scale(1.02);
        box-shadow: 0 0 15px rgba(78, 168, 222, 0.4);
    }

    /* 9. TABS */
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
        border-bottom: 1px solid var(--glass-border);
    }
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-radius: 4px;
        color: var(--text-muted);
        font-size: 1rem;
    }
    .stTabs [aria-selected="true"] {
        color: var(--accent-gold) !important;
        font-weight: bold;
        border-bottom: 2px solid var(--accent-gold);
    }

    /* 10. ANIMATIONS */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translate3d(0, 30px, 0);
        }
        to {
            opacity: 1;
            transform: translate3d(0, 0, 0);
        }
    }
    
    /* Utils */
    .highlight-text { color: var(--accent-gold); font-weight: bold; }
    .mono-text { font-family: var(--font-mono); font-size: 0.9em; opacity: 0.8; }
    
    /* Result Box Specifics */
    .result-box {
        border-left: 4px solid var(--accent-gold);
        background: linear-gradient(90deg, rgba(255, 215, 0, 0.05), transparent);
    }

</style>
""", unsafe_allow_html=True)

# ==================================================
# 2. TRANSLATION DICTIONARY
# ==================================================
translations = {
    "en": {
        "sidebar_title": "NAVIGATION",
        "lang_label": "Language / Bahasa",
        "nav_overview": "Overview",
        "nav_profiles": "Developers",
        "nav_matrix": "Matrix Lab",
        "nav_routing": "Routing Tool",
        "nav_goto": "MENU",
        
        # Overview
        "ov_title": "Discrete Mathematics",
        "ov_subtitle": "Graph Theory • Adjacency Matrices • Pathfinding Algorithms",
        "tab_about": "System Overview",
        "tab_theory": "Core Concepts",
        "tab_matrix": "Matrix Logic",
        "tab_algo": "Algorithm",
        "ov_welcome_title": "Project Scope",
        "ov_welcome_text": "A computational interface designed to simulate and visualize complex Discrete Structures. Explore the correlation between numerical matrices and visual graph topology.",
        "ov_find_1": "Team Profiles: Engineering & Research roles.",
        "ov_find_2": "Matrix Lab: Real-time Erdős-Rényi graph generation.",
        "ov_find_3": "Routing Tool: Geospatial Dijkstra implementation.",
        "ov_goal": "Objective: Visualizing Abstract Math.",
        "ov_stack": "Tech Stack: Python, NetworkX, Folium.",
        "theory_what": "Graph Fundamentals",
        "theory_def_v": "Vertices (V): The fundamental units (Nodes/Cities).",
        "theory_def_e": "Edges (E): The relational connections (Roads/Links).",
        "matrix_desc": "The Adjacency Matrix is a square matrix used to represent a finite graph. The elements indicate whether pairs of vertices are adjacent.",
        "algo_title": "Dijkstra's Algorithm",
        "algo_desc": "An iterative algorithm that determines the shortest path tree from a source node to a destination node by minimizing edge weights.",

        # Profiles
        "prof_title": "Team",
        "prof_subtitle": "Design • Research • Development",
        "prof_role_leader": "LEAD ENGINEER",
        "prof_role_research": "RESEARCHER",
        "prof_role_dev": "DEVELOPER",
        
        # Matrix App
        "mat_title": "Matrix Visualization",
        "mat_ctrl": "Simulation Parameters",
        "mat_vert": "Node Count (n)",
        "mat_prob": "Edge Probability (p)",
        "mat_seed": "Random Seed",
        "mat_tab_view": "Graph Topology",
        "mat_tab_data": "Adjacency Matrix",

        # Routing Tool
        "route_title": "Intelligent Routing",
        "route_set": "Path Configuration",
        "route_start": "Origin Node",
        "route_end": "Destination Node",
        "route_btn": "Compute Optimal Path",
        "route_err": "Routing Failed: No viable path found within the defined constraints.",
        "route_res_dist": "Total Distance",
        "route_res_path": "Optimized Route",
        "route_start_mark": "START",
        "route_dest_mark": "END",
        "route_on_route": "Waypoint"
    },
    "id": {
        "sidebar_title": "NAVIGASI",
        "lang_label": "Language / Bahasa",
        "nav_overview": "Ringkasan",
        "nav_profiles": "Pengembang",
        "nav_matrix": "Lab Matriks",
        "nav_routing": "Alat Rute",
        "nav_goto": "MENU",

        # Overview
        "ov_title": "Matematika Diskrit",
        "ov_subtitle": "Teori Graf • Matriks • Algoritma Pencarian Jalur",
        "tab_about": "Ikhtisar Sistem",
        "tab_theory": "Konsep Inti",
        "tab_matrix": "Logika Matriks",
        "tab_algo": "Algoritma",
        "ov_welcome_title": "Lingkup Proyek",
        "ov_welcome_text": "Antarmuka komputasi yang dirancang untuk mensimulasikan dan memvisualisasikan Struktur Diskrit. Eksplorasi korelasi antara matriks numerik dan topologi graf visual.",
        "ov_find_1": "Profil Tim: Peran Teknik & Riset.",
        "ov_find_2": "Lab Matriks: Generasi graf Erdős-Rényi real-time.",
        "ov_find_3": "Alat Rute: Implementasi Geospasial Dijkstra.",
        "ov_goal": "Tujuan: Visualisasi Matematika Abstrak.",
        "ov_stack": "Teknologi: Python, NetworkX, Folium.",
        "theory_what": "Dasar Teori Graf",
        "theory_def_v": "Simpul (V): Unit dasar (Node/Kota).",
        "theory_def_e": "Sisi (E): Koneksi relasional (Jalan/Link).",
        "matrix_desc": "Matriks Adjasensi adalah matriks persegi yang merepresentasikan graf terbatas. Elemen menunjukkan apakah pasangan simpul terhubung.",
        "algo_title": "Algoritma Dijkstra",
        "algo_desc": "Algoritma iteratif yang menentukan pohon jalur terpendek dari node sumber ke tujuan dengan meminimalkan bobot sisi.",

        # Profiles
        "prof_title": "Tim Teknik",
        "prof_subtitle": "Desain • Riset • Pengembangan",
        "prof_role_leader": "KETUA TEKNIK",
        "prof_role_research": "PENELITI",
        "prof_role_dev": "PENGEMBANG",

        # Matrix App
        "mat_title": "Visualisasi Matriks",
        "mat_ctrl": "Parameter Simulasi",
        "mat_vert": "Jumlah Node (n)",
        "mat_prob": "Probabilitas Sisi (p)",
        "mat_seed": "Random Seed",
        "mat_tab_view": "Topologi Graf",
        "mat_tab_data": "Matriks Adjasensi",

        # Routing Tool
        "route_title": "Routing Cerdas",
        "route_set": "Konfigurasi Jalur",
        "route_start": "Node Asal",
        "route_end": "Node Tujuan",
        "route_btn": "Hitung Jalur Optimal",
        "route_err": "Gagal: Tidak ada jalur yang ditemukan dalam batasan yang ditentukan.",
        "route_res_dist": "Jarak Total",
        "route_res_path": "Rute Optimal",
        "route_start_mark": "MULAI",
        "route_dest_mark": "AKHIR",
        "route_on_route": "Titik Lewat"
    }
}

# ==================================================
# 3. GLOBAL CONFIG & DATA
# ==================================================

# --- LANGUAGE SELECTOR ---
st.sidebar.markdown(f"<h3 style='margin-bottom:10px; font-size:1.2rem;'>🌐 Language</h3>", unsafe_allow_html=True)
lang_choice = st.sidebar.selectbox("Select Language", ["English", "Bahasa Indonesia"], label_visibility="collapsed")
lang_code = "en" if lang_choice == "English" else "id"
t = translations[lang_code]

current_dir = os.path.dirname(os.path.abspath(__file__))

# Data Structures (Same as before)
java_data = {
    "DKI Jakarta": {
        "Central Jakarta": (-6.1805, 106.8283),
        "South Jakarta": (-6.2615, 106.8106),
        "West Jakarta": (-6.1674, 106.7637),
        "East Jakarta": (-6.2250, 106.9004),
        "North Jakarta": (-6.1214, 106.8827)
    },
    "Banten": {
        "Serang": (-6.1104, 106.1636),
        "Tangerang": (-6.1702, 106.6403),
        "Cilegon": (-6.0174, 106.0538)
    },
    "West Java": {
        "Bandung": (-6.9175, 107.6191),
        "Bogor": (-6.5971, 106.8060),
        "Depok": (-6.4025, 106.7942),
        "Bekasi": (-6.2383, 106.9756),
        "Cirebon": (-6.7320, 108.5523),
        "Sukabumi": (-6.9277, 106.9300),
        "Tasikmalaya": (-7.3274, 108.2207)
    },
    "Central Java": {
        "Semarang": (-6.9667, 110.4167),
        "Surakarta": (-7.5755, 110.8243),
        "Magelang": (-7.4797, 110.2177),
        "Tegal": (-6.8694, 109.1402),
        "Purwokerto": (-7.4243, 109.2391),
    },
    "East Java": {
        "Surabaya": (-7.2575, 112.7521),
        "Malang": (-7.9666, 112.6326),
        "Kediri": (-7.8485, 112.0178),
        "Banyuwangi": (-8.2192, 114.3691),
        "Madiun": (-7.6298, 111.5239)
    }
}

@st.cache_data
def get_all_cities():
    cities = {}
    for prov, data in java_data.items():
        for city, coord in data.items():
            cities[city] = coord
    return cities

@st.cache_data
def haversine(coord1, coord2):
    R = 6371
    lat1, lon1 = math.radians(coord1[0]), math.radians(coord1[1])
    lat2, lon2 = math.radians(coord2[0]), math.radians(coord2[1])
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = math.sin(dlat/2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    return R * c

@st.cache_resource
def build_graph():
    G = nx.Graph()
    cities = get_all_cities()
    city_names = list(cities.keys())
    for city, coord in cities.items():
        G.add_node(city, pos=coord)
    for i in range(len(city_names)):
        for j in range(i + 1, len(city_names)):
            c1, c2 = city_names[i], city_names[j]
            dist = haversine(cities[c1], cities[c2])
            if dist < 250:
                G.add_edge(c1, c2, weight=dist)
    return G

# ==================================================
# 4. NAVIGATION
# ==================================================
st.sidebar.markdown(f"<h2 style='padding-top:20px;'>{t['sidebar_title']}</h2>", unsafe_allow_html=True)
nav_options = [t["nav_overview"], t["nav_profiles"], t["nav_matrix"], t["nav_routing"]]
page_selection = st.sidebar.radio(t["nav_goto"], nav_options)

# ==================================================
# PAGE: PROJECT OVERVIEW
# ==================================================
if page_selection == t["nav_overview"]:
    st.markdown(f"<h1 style='text-align:center;'>{t['ov_title']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<p style='text-align:center; font-family:JetBrains Mono; color:#4ea8de; margin-bottom:40px;'>{t['ov_subtitle']}</p>", unsafe_allow_html=True)

    tab1, tab2, tab3, tab4 = st.tabs([t["tab_about"], t["tab_theory"], t["tab_matrix"], t["tab_algo"]])

    with tab1:
        st.markdown(f"""
        <div class="glass-card">
            <h3 class="highlight-text">{t['ov_welcome_title']}</h3>
            <p>{t['ov_welcome_text']}</p>
            <ul>
                <li>{t['ov_find_1']}</li>
                <li>{t['ov_find_2']}</li>
                <li>{t['ov_find_3']}</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        c1, c2 = st.columns(2)
        with c1:
            st.markdown(f'<div class="glass-card" style="border-left:3px solid #FFD700">{t["ov_goal"]}</div>', unsafe_allow_html=True)
        with c2:
            st.markdown(f'<div class="glass-card" style="border-left:3px solid #4ea8de">{t["ov_stack"]}</div>', unsafe_allow_html=True)

    with tab2:
        col_text, col_viz = st.columns([1.5, 1])
        with col_text:
            st.markdown(f"""
            <div class="glass-card">
                <h3>{t['theory_what']}</h3>
                <p>A <b>Graph</b> $G = (V, E)$ consists of:</p>
                <ul style="margin-left:20px;">
                    <li style="margin-bottom:10px;">{t['theory_def_v']}</li>
                    <li>{t['theory_def_e']}</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col_viz:
            fig_demo, ax_demo = plt.subplots(figsize=(4, 3))
            fig_demo.patch.set_alpha(0) # Transparent fig
            ax_demo.set_facecolor("#00000000") # Transparent ax
            
            G_demo = nx.Graph()
            G_demo.add_edges_from([(1, 2), (1, 3), (2, 3), (3, 4)])
            pos_demo = nx.spring_layout(G_demo, seed=42)
            nx.draw(G_demo, pos_demo, ax=ax_demo, with_labels=True, node_color="#4ea8de", edge_color="white", font_color="black", font_weight="bold")
            st.pyplot(fig_demo)

    with tab3:
        st.markdown(f"""
        <div class="glass-card">
            <h3 style="color:#bb86fc">{t['tab_matrix']}</h3>
            <p>{t['matrix_desc']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        df_example = pd.DataFrame(
            [[0, 1, 1], [1, 0, 0], [1, 0, 0]],
            columns=["A", "B", "C"],
            index=["A", "B", "C"]
        )
        st.dataframe(df_example, use_container_width=True)

    with tab4:
        st.markdown(f"""
        <div class="glass-card result-box">
            <h3>{t['algo_title']}</h3>
            <p>{t['algo_desc']}</p>
            <p class="mono-text">Algorithm Complexity: O(|E| + |V|log|V|)</p>
        </div>
        """, unsafe_allow_html=True)

# ==================================================
# PAGE: TEAM PROFILES
# ==================================================
elif page_selection == t["nav_profiles"]:
    
    # Define tasks
    krisna_tasks = ["Led Project planning", "Analytical calculations", "UI/UX Architecture"] if lang_code == "en" else ["Perencanaan proyek", "Perhitungan analitis", "Arsitektur UI/UX"]
    zahra_tasks = ["Visual Methodology", "Documentation Lead", "Presentation Data"] if lang_code == "en" else ["Metodologi Visual", "Dokumentasi", "Data Presentasi"]
    naia_tasks = ["Fullstack Dev", "Mapping Algorithms", "Asset Management"] if lang_code == "en" else ["Fullstack Dev", "Algoritma Pemetaan", "Manajemen Aset"]

    st.markdown(f"<h1 style='text-align:center;'>{t['prof_title']}</h1>", unsafe_allow_html=True)
    st.markdown(f"<div style='text-align:center; color:#9ca3af; margin-bottom:50px;'>{t['prof_subtitle']}</div>", unsafe_allow_html=True)

    # Image Helper
    def get_safe_base64_image(filename_base):
        possible_names = [f"{filename_base}.jpeg", f"{filename_base}.jpg", f"{filename_base}.png"]
        possible_folders = [current_dir, os.path.join(current_dir, "images"), os.path.join(current_dir, "assets")]
        for folder in possible_folders:
            for fname in possible_names:
                full_path = os.path.join(folder, fname)
                if os.path.exists(full_path):
                    try:
                        with Image.open(full_path) as img:
                            img = img.convert("RGB")
                            img.thumbnail((400, 400))
                            buffered = io.BytesIO()
                            img.save(buffered, format="JPEG", quality=90)
                            return base64.b64encode(buffered.getvalue()).decode()
                    except: pass
        return None

    team_data = [
        {"name": "I Putu Gede Krisna Ananta Putra Suryawan", "id": "021202500012", "role": t["prof_role_leader"], "file": "krisna", "tasks": krisna_tasks},
        {"name": "Azzahra Yundilla Rabbani ", "id": "021202500014", "role": t["prof_role_research"], "file": "zahra", "tasks": zahra_tasks},
        {"name": "Naia Aulia Syuroatmodjo", "id": "021202500016", "role": t["prof_role_dev"], "file": "naia", "tasks": naia_tasks}
    ]

    cols = st.columns(3)
    for i, member in enumerate(team_data):
        img_b64 = get_safe_base64_image(member['file'])
        img_src = f"data:image/jpeg;base64,{img_b64}" if img_b64 else f"https://ui-avatars.com/api/?name={member['name'].replace(' ', '+')}&background=050505&color=4ea8de&size=256"
        
        task_list = "".join([f"<li style='color:#9ca3af; font-size:0.85rem; margin-bottom:4px;'>▹ {task}</li>" for task in member['tasks']])

        with cols[i]:
            st.markdown(f"""
            <div class="glass-card" style="text-align:center; padding:30px 20px;">
                <div style="width:120px; height:120px; margin:0 auto 20px; border-radius:50%; overflow:hidden; border:2px solid #4ea8de; box-shadow:0 0 20px rgba(78,168,222,0.3);">
                    <img src="{img_src}" style="width:100%; height:100%; object-fit:cover;">
                </div>
                <h3 style="margin:0; font-size:1.2rem; color:white;">{member['name']}</h3>
                <div class="mono-text" style="color:#FFD700; font-size:0.8rem; margin-bottom:10px;">ID: {member['id']}</div>
                <div style="background:rgba(78,168,222,0.1); color:#4ea8de; padding:4px 12px; border-radius:20px; display:inline-block; font-size:0.75rem; font-weight:bold; margin-bottom:20px;">
                    {member['role']}
                </div>
                <ul style="text-align:left; list-style:none; padding:0;">
                    {task_list}
                </ul>
            </div>
            """, unsafe_allow_html=True)

# ==================================================
# PAGE: MATRIX -> GRAPH
# ==================================================
elif page_selection == t["nav_matrix"]:
    st.markdown(f"<h1 style='text-align:center;'>{t['mat_title']}</h1>", unsafe_allow_html=True)
    
    col_ctrl, col_main = st.columns([1, 3])
    with col_ctrl:
        st.markdown(f"<div class='glass-card'><h4>{t['mat_ctrl']}</h4>", unsafe_allow_html=True)
        n = st.number_input(t["mat_vert"], 3, 20, 6)
        prob = st.slider(t["mat_prob"], 0.0, 1.0, 0.4)
        seed = st.number_input(t["mat_seed"], 1, 100, 42)
        st.markdown("</div>", unsafe_allow_html=True)
    
    with col_main:
        G = nx.erdos_renyi_graph(n, prob, seed=seed)
        pos = nx.spring_layout(G, seed=seed)
        adj_matrix = nx.to_pandas_adjacency(G, dtype=int)
        
        tab1, tab2 = st.tabs([t["mat_tab_view"], t["mat_tab_data"]])
        with tab1:
            # Custom styled plot
            fig, ax = plt.subplots(figsize=(8, 5))
            fig.patch.set_alpha(0)
            ax.set_facecolor("#00000000")
            
            # Nodes
            nx.draw_networkx_nodes(G, pos, ax=ax, node_color="#050505", edgecolors="#4ea8de", node_size=600, linewidths=2)
            # Edges
            nx.draw_networkx_edges(G, pos, ax=ax, edge_color="white", alpha=0.3, width=1.5)
            # Labels
            nx.draw_networkx_labels(G, pos, ax=ax, font_color="white", font_weight="bold", font_family="sans-serif")
            
            ax.axis('off')
            st.pyplot(fig)
        with tab2:
            st.dataframe(adj_matrix, use_container_width=True)

# ==================================================
# PAGE: CITY ROUTING TOOL
# ==================================================
elif page_selection == t["nav_routing"]:
    st.markdown(f"<h1 style='text-align:center;'>{t['route_title']}</h1>", unsafe_allow_html=True)
    
    all_cities_dict = get_all_cities()
    all_cities_list = list(all_cities_dict.keys())
    G = build_graph()

    # Session
    if 'route_path' not in st.session_state: st.session_state['route_path'] = []
    if 'route_dist' not in st.session_state: st.session_state['route_dist'] = 0

    with st.sidebar:
        st.markdown("---")
        st.markdown(f"### ⚙️ {t['route_set']}")
        start_city = st.selectbox(t["route_start"], all_cities_list, index=0)
        end_city = st.selectbox(t["route_end"], all_cities_list, index=len(all_cities_list)-1)
        
        if st.button(t["route_btn"]):
            try:
                path = nx.shortest_path(G, source=start_city, target=end_city, weight='weight')
                dist = nx.shortest_path_length(G, source=start_city, target=end_city, weight='weight')
                st.session_state['route_path'] = path
                st.session_state['route_dist'] = dist
            except nx.NetworkXNoPath:
                st.session_state['route_path'] = []
                st.error(f"{t['route_err']}")

    # METRICS UI
    if st.session_state['route_path']:
        path_nodes = st.session_state['route_path']
        total_dist = st.session_state['route_dist']
        
        c1, c2 = st.columns([1, 2])
        with c1:
             st.markdown(f"""
            <div class="glass-card result-box" style="text-align:center;">
                <div class="mono-text" style="color:#9ca3af;">{t['route_res_dist']}</div>
                <div style="color:#FFD700; font-size:2.5rem; font-weight:800; text-shadow:0 0 15px rgba(255,215,0,0.5);">{total_dist:.0f} km</div>
            </div>
            """, unsafe_allow_html=True)
        with c2:
            path_str = ' <span style="color:#4ea8de">➝</span> '.join(path_nodes)
            st.markdown(f"""
            <div class="glass-card" style="height:100%; display:flex; align-items:center;">
                <div>
                    <div class="mono-text" style="color:#9ca3af; margin-bottom:5px;">{t['route_res_path']}</div>
                    <div style="color:white; font-size:1.1rem; line-height:1.6;">{path_str}</div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # MAP
    all_coords = list(all_cities_dict.values())
    center_lat = np.mean([c[0] for c in all_coords])
    center_lon = np.mean([c[1] for c in all_coords])

    # Dark Map Tiles
    m = folium.Map(location=[center_lat, center_lon], zoom_start=7, tiles="CartoDB dark_matter")
    
    # Edges
    for u, v, data in G.edges(data=True):
        folium.PolyLine(
            [all_cities_dict[u], all_cities_dict[v]],
            color="#2d3748",
            weight=1,
            opacity=0.3
        ).add_to(m)

    # Active Route
    if st.session_state['route_path']:
        route_coords = [all_cities_dict[node] for node in st.session_state['route_path']]
        folium.PolyLine(route_coords, color="#4ea8de", weight=8, opacity=0.4).add_to(m) # Glow
        folium.PolyLine(route_coords, color="#FFD700", weight=3, opacity=1).add_to(m) # Core

    # Markers
    for city, coord in all_cities_dict.items():
        is_start = st.session_state['route_path'] and city == st.session_state['route_path'][0]
        is_end = st.session_state['route_path'] and city == st.session_state['route_path'][-1]
        
        if is_start:
            folium.CircleMarker(coord, radius=8, color="#FFD700", fill=True, fill_color="black", fill_opacity=1, popup="START").add_to(m)
        elif is_end:
            folium.CircleMarker(coord, radius=8, color="#FF4444", fill=True, fill_color="black", fill_opacity=1, popup="END").add_to(m)
        else:
            folium.CircleMarker(coord, radius=3, color="#555", fill=True, fill_color="#222").add_to(m)

    st_folium(m, width=1200, height=550)