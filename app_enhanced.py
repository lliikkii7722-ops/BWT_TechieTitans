"""
OrgMemory Enhanced - Enterprise Knowledge Management System
Beautiful Streamlit Version with Background Image & Enhanced Design

Run: streamlit run app_enhanced.py
"""

import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import re
import json
import base64

# Page config
st.set_page_config(
    page_title="OrgMemory Enhanced - Knowledge Management",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with Background Image
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600;700;800&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Beautiful Light Pink Background with Gradient Overlay */
    .main {
        background: linear-gradient(135deg, rgba(255, 240, 245, 0.95), rgba(255, 228, 240, 0.92)), 
                    url('https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=1920&q=80');
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }
    
    /* Glassmorphism Effect */
    .glass-effect {
        background: rgba(255, 255, 255, 0.05);
        backdrop-filter: blur(10px);
        border-radius: 16px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
    }
    
    /* Professional Tab Styling with Glassmorphism */
    .stTabs [data-baseweb="tab-list"] {
        gap: 12px;
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(20px);
        padding: 16px;
        border-radius: 16px;
        border: 1px solid rgba(236, 72, 153, 0.3);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    }
    
    .stTabs [data-baseweb="tab"] {
        background: rgba(255, 255, 255, 0.6);
        backdrop-filter: blur(10px);
        color: #475569;
        border-radius: 12px;
        padding: 14px 28px;
        font-weight: 600;
        font-size: 15px;
        border: 1px solid rgba(236, 72, 153, 0.2);
        transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: rgba(236, 72, 153, 0.2);
        color: #ec4899;
        border-color: rgba(236, 72, 153, 0.4);
        transform: translateY(-2px);
        box-shadow: 0 4px 16px rgba(236, 72, 153, 0.3);
    }
    
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        background: linear-gradient(135deg, #ec4899, #f472b6);
        color: white;
        border-color: rgba(244, 114, 182, 0.5);
        box-shadow: 0 8px 24px rgba(236, 72, 153, 0.5);
        transform: translateY(-2px);
    }
    
    /* Beautiful Headers with Glow */
    h1, h2, h3 {
        color: #1e293b !important;
        font-weight: 700 !important;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
    }
    
    /* Animated Gradient Buttons */
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6, #8b5cf6, #ec4899);
        background-size: 200% 200%;
        color: white;
        border: none;
        border-radius: 12px;
        padding: 14px 32px;
        font-weight: 700;
        font-size: 15px;
        box-shadow: 0 8px 24px rgba(59, 130, 246, 0.4);
        transition: all 0.4s ease;
        animation: gradientShift 3s ease infinite;
    }
    
    @keyframes gradientShift {
        0% { background-position: 0% 50%; }
        50% { background-position: 100% 50%; }
        100% { background-position: 0% 50%; }
    }
    
    .stButton > button:hover {
        transform: translateY(-3px) scale(1.02);
        box-shadow: 0 12px 32px rgba(59, 130, 246, 0.6);
    }
    
    /* Glass Text Areas */
    .stTextArea textarea, .stTextInput input {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border: 1px solid rgba(236, 72, 153, 0.3);
        border-radius: 12px;
        color: #1e293b;
        font-size: 15px;
        transition: all 0.3s ease;
    }
    
    .stTextArea textarea:focus, .stTextInput input:focus {
        border-color: #ec4899;
        box-shadow: 0 0 0 4px rgba(236, 72, 153, 0.2);
        background: rgba(255, 255, 255, 0.9);
    }
    
    /* Glass Expanders */
    .stExpander {
        background: rgba(255, 255, 255, 0.7);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        border-left: 4px solid #ec4899;
        border: 1px solid rgba(236, 72, 153, 0.3);
        margin-bottom: 16px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
        color: #1e293b;
    }
    
    .stExpander:hover {
        transform: translateX(4px);
        box-shadow: 0 8px 24px rgba(236, 72, 153, 0.3);
    }
    
    /* Beautiful Metrics with Glow */
    div[data-testid="metric-container"] {
        background: linear-gradient(135deg, rgba(255, 255, 255, 0.8), rgba(255, 240, 245, 0.8));
        backdrop-filter: blur(20px);
        padding: 28px;
        border-radius: 16px;
        border: 1px solid rgba(236, 72, 153, 0.3);
        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
        transition: all 0.3s ease;
    }
    
    div[data-testid="metric-container"]:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(236, 72, 153, 0.3);
    }
    
    div[data-testid="metric-container"] label {
        color: #64748b !important;
        font-size: 14px !important;
        font-weight: 600 !important;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    div[data-testid="metric-container"] [data-testid="stMetricValue"] {
        color: #ec4899 !important;
        font-size: 36px !important;
        font-weight: 800 !important;
        text-shadow: 0 2px 4px rgba(236, 72, 153, 0.3);
    }
    
    /* Glass Alert Boxes */
    .stAlert {
        background: rgba(255, 255, 255, 0.8);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        border-left: 4px solid #ec4899;
        color: #1e293b;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.1);
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: rgba(255, 240, 245, 0.5);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #ec4899, #f472b6);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #db2777, #ec4899);
    }
    
    /* Floating Animation */
    @keyframes float {
        0%, 100% { transform: translateY(0px); }
        50% { transform: translateY(-10px); }
    }
    
    .float-animation {
        animation: float 3s ease-in-out infinite;
    }
    
    /* Pulse Animation */
    @keyframes pulse {
        0%, 100% { opacity: 1; }
        50% { opacity: 0.7; }
    }
    
    /* Text with gradient */
    .gradient-text {
        background: linear-gradient(135deg, #ec4899, #f472b6, #fb7185);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }
    
    /* General text color */
    p, span, div, label {
        color: #1e293b;
    }
</style>
""", unsafe_allow_html=True)

# Database functions
def init_db():
    conn = sqlite3.connect('orgmemory.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS knowledge
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  raw_content TEXT NOT NULL,
                  summary TEXT,
                  decisions TEXT,
                  action_items TEXT,
                  risks TEXT,
                  tags TEXT,
                  people TEXT,
                  contradictions TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    conn.commit()
    conn.close()

# AI Processing
def process_knowledge(raw_content):
    content_lower = raw_content.lower()
    sentences = raw_content.split('. ')
    
    # Summary
    summary = '. '.join(sentences[:2]) + '.' if len(sentences) > 1 else raw_content
    
    # Decisions
    decision_keywords = ['decided', 'agreed', 'concluded', 'approved', 'finalized', 'chose']
    decisions = [s.strip() for s in sentences if any(k in s.lower() for k in decision_keywords)]
    decisions_text = '; '.join(decisions) if decisions else 'No explicit decisions'
    
    # Action Items
    action_keywords = ['will', 'should', 'must', 'need to', 'action', 'todo', 'task']
    actions = [s.strip() for s in sentences if any(k in s.lower() for k in action_keywords)]
    actions_text = '; '.join(actions) if actions else 'No action items'
    
    # Risks
    risk_keywords = ['risk', 'concern', 'issue', 'problem', 'blocker', 'challenge', 'warning']
    risks = [s.strip() for s in sentences if any(k in s.lower() for k in risk_keywords)]
    risks_text = '; '.join(risks) if risks else 'No risks identified'
    
    # Tags
    tags = []
    tag_map = {
        'meeting': ['meeting', 'discussion'],
        'project': ['project', 'initiative'],
        'technical': ['technical', 'code', 'api'],
        'decision': ['decided', 'approved'],
        'urgent': ['urgent', 'asap'],
    }
    for tag, keywords in tag_map.items():
        if any(k in content_lower for k in keywords):
            tags.append(tag)
    tags_text = ','.join(tags) if tags else 'general'
    
    # People
    people_pattern = r'\b[A-Z][a-z]+ [A-Z][a-z]+\b'
    people = list(set(re.findall(people_pattern, raw_content)))
    people_text = ','.join(people) if people else 'No people mentioned'
    
    # Contradictions
    contradictions = detect_contradictions(raw_content)
    
    return {
        'summary': summary,
        'decisions': decisions_text,
        'action_items': actions_text,
        'risks': risks_text,
        'tags': tags_text,
        'people': people_text,
        'contradictions': contradictions
    }

def detect_contradictions(raw_content):
    content_lower = raw_content.lower()
    contradictions = []
    
    if 'rest' in content_lower and 'graphql' in content_lower:
        contradictions.append("Potential conflict: Both REST and GraphQL mentioned")
    if 'approved' in content_lower and 'rejected' in content_lower:
        contradictions.append("Potential conflict: Both approved and rejected mentioned")
    
    return '; '.join(contradictions) if contradictions else 'No contradictions detected'

def save_knowledge(raw_content, processed):
    conn = sqlite3.connect('orgmemory.db')
    c = conn.cursor()
    c.execute('''INSERT INTO knowledge 
                 (raw_content, summary, decisions, action_items, risks, tags, people, contradictions)
                 VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
              (raw_content, processed['summary'], processed['decisions'],
               processed['action_items'], processed['risks'], 
               processed['tags'], processed['people'], processed['contradictions']))
    conn.commit()
    conn.close()

def get_all_knowledge():
    conn = sqlite3.connect('orgmemory.db')
    df = pd.read_sql_query("SELECT * FROM knowledge ORDER BY created_at DESC", conn)
    conn.close()
    return df

# Initialize database
init_db()

# Stunning Header with Animation
st.markdown("""
<div style='text-align: center; padding: 60px 20px; background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(255, 240, 245, 0.9)); backdrop-filter: blur(20px); border-radius: 24px; border: 1px solid rgba(236, 72, 153, 0.3); margin-bottom: 40px; box-shadow: 0 20px 60px rgba(0, 0, 0, 0.1);'>
    <div class='float-animation'>
        <h1 style='font-size: 4.5em; margin: 0; background: linear-gradient(135deg, #ec4899, #f472b6, #fb7185); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 800; letter-spacing: -2px;'>
            🧠 OrgMemory Enhanced
        </h1>
    </div>
    <p style='font-size: 1.5em; margin: 20px 0 12px 0; color: #1e293b; font-weight: 600;'>
        Enterprise Knowledge Management System
    </p>
    <p style='color: #475569; font-size: 1.05em; margin: 0; font-weight: 400;'>
        ✨ Capture • Process • Analyze • Discover • Innovate ✨
    </p>
</div>
""", unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📝 Capture Knowledge",
    "📚 View All",
    "🔍 Search",
    "📊 Dashboard",
    "⚠️ Risk Analysis",
    "🔗 Knowledge Graph"
])

# TAB 1: Capture Knowledge
with tab1:
    st.header("📝 Capture New Knowledge")
    st.write("Enter meeting notes, chat logs, or any organizational knowledge:")
    
    raw_content = st.text_area(
        "Knowledge Content",
        height=250,
        placeholder="Example: Meeting with John Smith and Sarah Johnson. We decided to migrate to microservices. Action item: John will prepare the architecture document by Friday. Risk: tight deadline may cause quality issues."
    )
    
    if st.button("🚀 Process & Save Knowledge", type="primary"):
        if raw_content:
            with st.spinner("🔄 Processing knowledge with AI..."):
                processed = process_knowledge(raw_content)
                save_knowledge(raw_content, processed)
            
            st.success("✅ Knowledge Captured Successfully!")
            
            col1, col2 = st.columns(2)
            with col1:
                st.info(f"**📋 Summary:** {processed['summary']}")
                st.info(f"**✅ Decisions:** {processed['decisions']}")
                st.info(f"**🎯 Action Items:** {processed['action_items']}")
            with col2:
                st.warning(f"**⚠️ Risks:** {processed['risks']}")
                st.info(f"**🏷️ Tags:** {processed['tags']}")
                st.info(f"**👥 People:** {processed['people']}")
            
            if processed['contradictions'] != 'No contradictions detected':
                st.error(f"🚨 **Contradictions:** {processed['contradictions']}")
        else:
            st.warning("⚠️ Please enter some content")

# TAB 2: View All
with tab2:
    st.header("📚 All Knowledge Entries")
    
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("🔄 Refresh", key="refresh_all"):
            st.rerun()
    
    df = get_all_knowledge()
    
    if len(df) == 0:
        st.info("📭 No knowledge entries yet. Start capturing!")
    else:
        st.success(f"✨ Found {len(df)} entries")
        
        for idx, row in df.iterrows():
            with st.expander(f"📄 Entry #{row['id']} - {row['created_at'][:10]} - {row['tags']}"):
                st.markdown(f"**📝 Raw Content:** {row['raw_content']}")
                st.markdown(f"**📋 Summary:** {row['summary']}")
                st.markdown(f"**✅ Decisions:** {row['decisions']}")
                st.markdown(f"**🎯 Action Items:** {row['action_items']}")
                st.markdown(f"**⚠️ Risks:** {row['risks']}")
                st.markdown(f"**🏷️ Tags:** {row['tags']}")
                st.markdown(f"**👥 People:** {row['people']}")
                if row['contradictions'] and row['contradictions'] != 'No contradictions detected':
                    st.error(f"**🚨 Contradictions:** {row['contradictions']}")

# TAB 3: Search
with tab3:
    st.header("🔍 Search Knowledge")
    
    search_keyword = st.text_input("🔎 Enter keyword to search:", placeholder="e.g., microservices, meeting, John")
    
    if st.button("🔍 Search Now", type="primary"):
        if search_keyword:
            with st.spinner("🔄 Searching..."):
                conn = sqlite3.connect('orgmemory.db')
                query = f"SELECT * FROM knowledge WHERE raw_content LIKE '%{search_keyword}%' OR summary LIKE '%{search_keyword}%' OR decisions LIKE '%{search_keyword}%'"
                results = pd.read_sql_query(query, conn)
                conn.close()
            
            if len(results) == 0:
                st.info("📭 No results found.")
            else:
                st.success(f"✨ Found {len(results)} result(s)")
                
                for idx, row in results.iterrows():
                    with st.expander(f"📄 Entry #{row['id']} - {row['created_at'][:10]}"):
                        st.markdown(f"**📋 Summary:** {row['summary']}")
                        st.markdown(f"**✅ Decisions:** {row['decisions']}")
                        st.markdown(f"**🏷️ Tags:** {row['tags']}")
                        st.markdown(f"**👥 People:** {row['people']}")
        else:
            st.warning("⚠️ Please enter a search keyword")

# TAB 4: Dashboard
with tab4:
    st.header("📊 Dashboard Analytics")
    
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("🔄 Refresh", key="refresh_dashboard"):
            st.rerun()
    
    df = get_all_knowledge()
    
    if len(df) > 0:
        # Metrics
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.metric("📚 Total Entries", len(df))
        
        with col2:
            decisions_count = len(df[~df['decisions'].str.contains('No explicit', na=False)])
            st.metric("✅ Decisions", decisions_count)
        
        with col3:
            actions_count = len(df[~df['action_items'].str.contains('No action', na=False)])
            st.metric("🎯 Action Items", actions_count)
        
        with col4:
            contradictions_count = len(df[~df['contradictions'].str.contains('No contradictions', na=False)])
            st.metric("🚨 Contradictions", contradictions_count)
        
        st.markdown("---")
        
        # Charts
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📌 Top Tags")
            all_tags = []
            for tags in df['tags'].dropna():
                all_tags.extend(tags.split(','))
            tag_counts = pd.Series(all_tags).value_counts().head(10)
            
            fig = px.bar(x=tag_counts.values, y=tag_counts.index, orientation='h',
                        labels={'x': 'Count', 'y': 'Tag'},
                        title="Most Common Tags",
                        color=tag_counts.values,
                        color_continuous_scale='Pinkyl')
            fig.update_layout(
                plot_bgcolor='rgba(255,255,255,0.5)',
                paper_bgcolor='rgba(255,255,255,0.8)',
                font=dict(size=14, color='#1e293b')
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader("📈 Knowledge Growth")
            df['date'] = pd.to_datetime(df['created_at']).dt.date
            growth = df.groupby('date').size().cumsum()
            
            fig = px.area(x=growth.index, y=growth.values,
                         labels={'x': 'Date', 'y': 'Total Entries'},
                         title="Cumulative Knowledge Growth")
            fig.update_traces(fill='tozeroy', fillcolor='rgba(236, 72, 153, 0.3)', 
                            line=dict(color='rgb(236, 72, 153)', width=3))
            fig.update_layout(
                plot_bgcolor='rgba(255,255,255,0.5)',
                paper_bgcolor='rgba(255,255,255,0.8)',
                font=dict(size=14, color='#1e293b')
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📭 No data yet. Start capturing knowledge!")

# TAB 5: Risk Analysis
with tab5:
    st.header("⚠️ Knowledge Risk Analysis")
    st.write("Identify employees with high knowledge concentration:")
    
    col1, col2 = st.columns([6, 1])
    with col2:
        if st.button("🔄 Refresh", key="refresh_risks"):
            st.rerun()
    
    df = get_all_knowledge()
    
    if len(df) > 0:
        person_counts = {}
        for people in df['people'].dropna():
            if people != 'No people mentioned':
                for person in people.split(','):
                    person = person.strip()
                    person_counts[person] = person_counts.get(person, 0) + 1
        
        if person_counts:
            risk_data = []
            for person, count in person_counts.items():
                risk_level = 'HIGH' if count > 10 else 'MEDIUM' if count > 5 else 'LOW'
                risk_data.append({'Person': person, 'Mentions': count, 'Risk Level': risk_level})
            
            risk_df = pd.DataFrame(risk_data).sort_values('Mentions', ascending=False)
            
            for idx, row in risk_df.iterrows():
                color = '🔴' if row['Risk Level'] == 'HIGH' else '🟡' if row['Risk Level'] == 'MEDIUM' else '🟢'
                st.markdown(f"{color} **{row['Person']}** - Mentioned {row['Mentions']} times - Risk: {row['Risk Level']}")
            
            st.markdown("---")
            
            fig = px.bar(risk_df, x='Mentions', y='Person', orientation='h',
                        color='Risk Level',
                        color_discrete_map={'HIGH': '#ef4444', 'MEDIUM': '#f59e0b', 'LOW': '#10b981'},
                        title="Knowledge Concentration by Person")
            fig.update_layout(
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(255,255,255,0.05)',
                font=dict(size=14, color='#e2e8f0')
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.info("📭 No people mentioned in knowledge base yet.")
    else:
        st.info("📭 No data yet. Start capturing knowledge!")

# TAB 6: Knowledge Graph
with tab6:
    st.header("🔗 Knowledge Graph")
    st.write("Visual network of people, projects, and decisions")
    
    df = get_all_knowledge()
    
    if len(df) > 0:
        st.info("📊 Knowledge Graph Visualization")
        st.write(f"**Total Nodes:** {len(df)} knowledge entries")
        
        all_people = []
        all_tags = []
        
        for people in df['people'].dropna():
            if people != 'No people mentioned':
                all_people.extend(people.split(','))
        
        for tags in df['tags'].dropna():
            all_tags.extend(tags.split(','))
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("👥 Unique People", len(set(all_people)))
        
        with col2:
            st.metric("🏷️ Unique Tags", len(set(all_tags)))
        
        with col3:
            st.metric("🔗 Connections", len(df))
        
        st.markdown("---")
        
        st.subheader("🕸️ Network Connections")
        
        if len(set(all_people)) > 0:
            people_counts = pd.Series(all_people).value_counts().head(10)
            
            fig = go.Figure(data=[go.Scatter(
                x=list(range(len(people_counts))),
                y=people_counts.values,
                mode='markers+lines',
                marker=dict(size=people_counts.values*5, color=people_counts.values, 
                           colorscale='Viridis', showscale=True),
                text=people_counts.index,
                hovertemplate='<b>%{text}</b><br>Connections: %{y}<extra></extra>',
                line=dict(color='rgba(96, 165, 250, 0.5)', width=2)
            )])
            
            fig.update_layout(
                title="Knowledge Network - Top Contributors",
                xaxis_title="Person Index",
                yaxis_title="Number of Connections",
                showlegend=False,
                plot_bgcolor='rgba(255,255,255,0.5)',
                paper_bgcolor='rgba(255,255,255,0.8)',
                font=dict(size=14, color='#1e293b')
            )
            
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("📭 No data yet. Start capturing knowledge to build the graph!")

# Beautiful Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; padding: 32px; background: linear-gradient(135deg, rgba(255, 255, 255, 0.9), rgba(255, 240, 245, 0.9)); backdrop-filter: blur(20px); border-radius: 16px; border: 1px solid rgba(236, 72, 153, 0.3); margin-top: 40px; box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);'>
    <p style='font-size: 1.3em; margin: 0; background: linear-gradient(135deg, #ec4899, #f472b6, #fb7185); -webkit-background-clip: text; -webkit-text-fill-color: transparent; font-weight: 700;'>
        🧠 OrgMemory Enhanced
    </p>
    <p style='color: #1e293b; font-size: 1em; margin: 12px 0 0 0; font-weight: 500;'>
        Enterprise Knowledge Management System
    </p>
    <p style='color: #475569; font-size: 0.9em; margin: 8px 0 0 0;'>
        Powered by AI | Built with Streamlit | © 2024
    </p>
</div>
""", unsafe_allow_html=True)
