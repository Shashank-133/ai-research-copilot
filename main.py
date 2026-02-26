"""
AI Research Co-Pilot Pro - Main Application
Multi-agent research assistant with web search and document analysis
"""

import streamlit as st
from openai import OpenAI
import time
from datetime import datetime
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Import our modules
from src.config import (
    OPENAI_API_KEY, OPENAI_API_BASE, MODEL_OPTIONS, 
    DEFAULT_TEMPERATURE, DEFAULT_MAX_TOKENS, MAX_SEARCH_RESULTS, 
    SEARCH_KEYWORDS
)
from src.search import web_search, format_search_context, needs_web_search
from src.document import process_uploaded_doc
from src.export import export_to_docx, export_to_pdf
from src.agents import MultiAgentSystem

# Page config
st.set_page_config(
    page_title="AI Research Co-Pilot Pro",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        text-align: center;
        padding: 1rem;
    }
    .stButton>button {
        width: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        padding: 0.5rem;
        font-weight: bold;
        border: none;
        transition: transform 0.2s;
    }
    .stButton>button:hover {
        transform: scale(1.05);
    }
    .chat-message {
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1rem;
        background: transparent;
        border-left: 4px solid;
    }
    .user-message {
        border-left-color: #667eea;
    }
    .user-message strong {
        color: #667eea;
        font-size: 1.1rem;
    }
    .assistant-message {
        border-left-color: #764ba2;
    }
    .assistant-message strong {
        color: #764ba2;
        font-size: 1.1rem;
    }
    .agent-working {
        padding: 1rem;
        background: linear-gradient(90deg, #667eea15 0%, #764ba215 100%);
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #667eea;
    }
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    }
    .success-box {
        background: #d4edda;
        border: 1px solid #c3e6cb;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize OpenAI client
@st.cache_resource
def get_openai_client():
    return OpenAI(
        api_key=OPENAI_API_KEY,
        base_url=OPENAI_API_BASE
    )

client = get_openai_client()

# Initialize session state
if 'messages' not in st.session_state:
    st.session_state.messages = []

if 'search_enabled' not in st.session_state:
    st.session_state.search_enabled = True

if 'multi_agent_enabled' not in st.session_state:
    st.session_state.multi_agent_enabled = False

if 'uploaded_doc_text' not in st.session_state:
    st.session_state.uploaded_doc_text = None

if 'stats' not in st.session_state:
    st.session_state.stats = {
        'total_queries': 0,
        'web_searches': 0,
        'documents_uploaded': 0,
        'exports': 0
    }

# Sidebar
with st.sidebar:
    st.markdown("## ⚙️ Settings")
    
    # Model selection
    selected_model_name = st.selectbox(
        "🤖 Select AI Model",
        options=list(MODEL_OPTIONS.keys()),
        index=0
    )
    
    selected_model = MODEL_OPTIONS[selected_model_name]
    
    # Features
    st.markdown("### 🎯 Features")
    
    st.session_state.search_enabled = st.checkbox(
        "🔍 Web Search",
        value=True,
        help="Search the web for current information"
    )
    
    st.session_state.multi_agent_enabled = st.checkbox(
        "🤖 Multi-Agent Mode",
        value=False,
        help="Use 3 AI agents: Researcher → Analyst → Writer"
    )
    
    st.markdown("---")
    
    # Document Upload
    st.markdown("### 📄 Document Upload")
    uploaded_file = st.file_uploader(
        "Upload a document to analyze",
        type=['pdf', 'docx', 'txt'],
        help="Upload PDF, DOCX, or TXT files"
    )
    
    if uploaded_file:
        with st.spinner("📖 Reading document..."):
            doc_text = process_uploaded_doc(uploaded_file)
            if doc_text:
                st.session_state.uploaded_doc_text = doc_text
                st.session_state.stats['documents_uploaded'] += 1
                st.success(f"✅ Loaded: {uploaded_file.name}")
                st.info(f"📊 {len(doc_text.split())} words")
            else:
                st.error("❌ Could not read document")
    
    st.markdown("---")
    
    # Statistics
    st.markdown("### 📊 Analytics")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Queries", st.session_state.stats['total_queries'])
        st.metric("Searches", st.session_state.stats['web_searches'])
    with col2:
        st.metric("Docs", st.session_state.stats['documents_uploaded'])
        st.metric("Exports", st.session_state.stats['exports'])
    
    st.markdown("---")
    
    # Clear chat
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.session_state.uploaded_doc_text = None
        st.rerun()
    
    st.markdown("---")
    
    # Info
    st.markdown("### ℹ️ About")
    st.markdown("""
    **V3.0 Features:**
    - 🤖 Multi-Agent System
    - 🔍 Real-time Web Search
    - 📄 Document Analysis
    - 📊 Export Reports (PDF/DOCX)
    - 📈 Analytics Dashboard
    
    Built with Python & Streamlit 🚀
    """)

# Main content
tab1, tab2 = st.tabs(["💬 Chat Interface", "📊 Analytics Dashboard"])

with tab1:
    st.markdown('<h1 class="main-header">🤖 AI Research Co-Pilot Pro</h1>', unsafe_allow_html=True)
    
    st.markdown("""
    <div style='text-align: center; padding: 1rem; background: linear-gradient(90deg, #667eea15 0%, #764ba215 100%); border-radius: 10px; margin-bottom: 2rem;'>
        <p style='font-size: 1.2rem; margin: 0;'>
            Advanced AI Research Assistant with Multi-Agent System, Web Search & Document Analysis
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Display chat messages
    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]
        
        if role == "user":
            st.markdown(f"""
            <div class="chat-message user-message">
                <strong>👤 You:</strong><br>
                {content}
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
            <div class="chat-message assistant-message">
                <strong>🤖 AI Co-Pilot:</strong><br>
                {content}
            </div>
            """, unsafe_allow_html=True)
            
            # Show sources
            if "sources" in message and message["sources"]:
                with st.expander("📚 View Sources"):
                    for i, source in enumerate(message["sources"], 1):
                        st.markdown(f"""
                        **{i}. [{source['title']}]({source['url']})**
                        
                        {source['snippet']}
                        """)
            
            # Show agent breakdown
            if "agents_output" in message and message["agents_output"]:
                with st.expander("🤖 View Multi-Agent Breakdown"):
                    agents = message["agents_output"]
                    
                    if 'research' in agents:
                        st.markdown("### 1️⃣ Research Agent")
                        st.write(agents['research'])
                    
                    if 'analysis' in agents:
                        st.markdown("### 2️⃣ Analysis Agent")
                        st.write(agents['analysis'])
                    
                    if 'final' in agents:
                        st.markdown("### 3️⃣ Writer Agent")
                        st.write(agents['final'])
            
            # Export buttons
            if "exportable" in message and message["exportable"]:
                col1, col2 = st.columns(2)
                
                with col1:
                    docx_file = export_to_docx(
                        message.get("query", ""),
                        content,
                        message.get("sources", []),
                        message.get("agents_output", {})
                    )
                    st.download_button(
                        label="📄 Download as DOCX",
                        data=docx_file,
                        file_name=f"research_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        key=f"docx_{message.get('timestamp', '')}"
                    )
                
                with col2:
                    pdf_file = export_to_pdf(
                        message.get("query", ""),
                        content,
                        message.get("sources", [])
                    )
                    st.download_button(
                        label="📕 Download as PDF",
                        data=pdf_file,
                        file_name=f"research_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf",
                        mime="application/pdf",
                        key=f"pdf_{message.get('timestamp', '')}"
                    )
    
    # Chat input
    user_question = st.chat_input("Ask me anything... (e.g., 'Latest AI trends in 2026')")
    
    if user_question:
        # Add document context if available
        if st.session_state.uploaded_doc_text:
            user_question_with_doc = f"{user_question}\n\nDocument Context:\n{st.session_state.uploaded_doc_text[:3000]}"
        else:
            user_question_with_doc = user_question
        
        # Add user message
        st.session_state.messages.append({"role": "user", "content": user_question})
        st.session_state.stats['total_queries'] += 1
        
        # Get AI response
        try:
            sources = []
            agents_output = {}
            
            # Multi-Agent Mode
            if st.session_state.multi_agent_enabled:
                multi_agent = MultiAgentSystem(client, selected_model)
                
                # Step 1: Web Search
                if st.session_state.search_enabled and needs_web_search(user_question, SEARCH_KEYWORDS):
                    st.session_state.stats['web_searches'] += 1
                    progress_placeholder = st.empty()
                    progress_placeholder.markdown("""
                    <div class="agent-working">
                        🔍 <strong>Searching the web...</strong>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    sources = web_search(user_question, MAX_SEARCH_RESULTS)
                    time.sleep(0.5)
                    progress_placeholder.empty()
                
                # Step 2: Research Agent
                progress_placeholder = st.empty()
                progress_placeholder.markdown("""
                <div class="agent-working">
                    🤖 <strong>Agent 1: Researcher</strong> - Gathering information...
                </div>
                """, unsafe_allow_html=True)
                
                research_output = multi_agent.researcher_agent(user_question_with_doc, sources)
                agents_output['research'] = research_output
                time.sleep(0.5)
                progress_placeholder.empty()
                
                # Step 3: Analyst Agent
                progress_placeholder = st.empty()
                progress_placeholder.markdown("""
                <div class="agent-working">
                    🧠 <strong>Agent 2: Analyst</strong> - Analyzing findings...
                </div>
                """, unsafe_allow_html=True)
                
                analysis_output = multi_agent.analyst_agent(user_question, research_output)
                agents_output['analysis'] = analysis_output
                time.sleep(0.5)
                progress_placeholder.empty()
                
                # Step 4: Writer Agent
                progress_placeholder = st.empty()
                progress_placeholder.markdown("""
                <div class="agent-working">
                    ✍️ <strong>Agent 3: Writer</strong> - Creating response...
                </div>
                """, unsafe_allow_html=True)
                
                final_output = multi_agent.writer_agent(user_question, research_output, analysis_output)
                agents_output['final'] = final_output
                time.sleep(0.5)
                progress_placeholder.empty()
                
                ai_response = final_output
                
            else:
                # Single Agent Mode
                current_time = datetime.now().strftime("%A, %B %d, %Y at %I:%M %p")
                
                search_context = ""
                if st.session_state.search_enabled and needs_web_search(user_question, SEARCH_KEYWORDS):
                    st.session_state.stats['web_searches'] += 1
                    with st.spinner("🔍 Searching the web..."):
                        sources = web_search(user_question, MAX_SEARCH_RESULTS)
                    
                    if sources:
                        search_context = format_search_context(sources)
                
                system_prompt = f"""You are an advanced AI Research Co-Pilot with expertise in technology, AI, and research.
You provide detailed, accurate, and insightful answers.

CURRENT INFORMATION:
- Current Date/Time: {current_time}

When web search results are provided, use them to give accurate, up-to-date information.
Always cite sources when using web search data.
Provide comprehensive answers with clear structure."""

                user_message = user_question_with_doc
                if search_context:
                    user_message = f"{user_question_with_doc}\n{search_context}"

                with st.spinner(f"🤖 {selected_model_name.split('(')[0]} is thinking..."):
                    response = client.chat.completions.create(
                        model=selected_model,
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_message}
                        ],
                        temperature=DEFAULT_TEMPERATURE,
                        max_tokens=DEFAULT_MAX_TOKENS
                    )
                
                ai_response = response.choices[0].message.content
            
            # Add assistant message
            st.session_state.messages.append({
                "role": "assistant",
                "content": ai_response,
                "sources": sources,
                "agents_output": agents_output if st.session_state.multi_agent_enabled else {},
                "exportable": True,
                "query": user_question,
                "timestamp": datetime.now().isoformat()
            })
            
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Error: {e}")
    
    # Quick action buttons
    st.markdown("---")
    st.markdown("### 💡 Quick Actions")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        if st.button("📰 Latest AI News"):
            st.session_state.messages.append({"role": "user", "content": "What are the latest AI news and developments in 2026?"})
            st.rerun()
    
    with col2:
        if st.button("🎓 Study Helper"):
            st.session_state.messages.append({"role": "user", "content": "Help me understand Generative AI, RAG, and Multi-Agent systems"})
            st.rerun()
    
    with col3:
        if st.button("💼 Business Ideas"):
            st.session_state.messages.append({"role": "user", "content": "Give me 5 innovative AI business ideas for startups in 2026"})
            st.rerun()
    
    with col4:
        if st.button("🔬 Research Topics"):
            st.session_state.messages.append({"role": "user", "content": "Suggest interesting AI research topics with implementation details"})
            st.rerun()

with tab2:
    st.markdown('<h1 class="main-header">📊 Analytics Dashboard</h1>', unsafe_allow_html=True)
    
    # Metrics overview
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h2 style='margin:0; font-size: 2.5rem;'>{st.session_state.stats['total_queries']}</h2>
            <p style='margin:0.5rem 0 0 0;'>Total Queries</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card">
            <h2 style='margin:0; font-size: 2.5rem;'>{st.session_state.stats['web_searches']}</h2>
            <p style='margin:0.5rem 0 0 0;'>Web Searches</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card">
            <h2 style='margin:0; font-size: 2.5rem;'>{st.session_state.stats['documents_uploaded']}</h2>
            <p style='margin:0.5rem 0 0 0;'>Documents</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h2 style='margin:0; font-size: 2.5rem;'>{st.session_state.stats['exports']}</h2>
            <p style='margin:0.5rem 0 0 0;'>Reports Exported</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    if st.session_state.messages:
        st.markdown("### 📈 Usage Over Time")
        
        message_times = []
        for msg in st.session_state.messages:
            if msg['role'] == 'user':
                message_times.append({'time': datetime.now(), 'type': 'Query'})
        
        if message_times:
            df = pd.DataFrame(message_times)
            
            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=list(range(len(message_times))),
                y=[1] * len(message_times),
                mode='markers',
                marker=dict(size=15, color='#667eea'),
                name='Queries'
            ))
            
            fig.update_layout(
                title="Query Timeline",
                xaxis_title="Query Number",
                yaxis_title="Activity",
                height=300,
                showlegend=False
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### 🎯 Feature Usage")
        
        col1, col2 = st.columns(2)
        
        with col1:
            feature_data = pd.DataFrame({
                'Feature': ['Web Search', 'Multi-Agent', 'Document Upload', 'Export'],
                'Usage': [
                    st.session_state.stats['web_searches'],
                    sum(1 for msg in st.session_state.messages if msg.get('agents_output')),
                    st.session_state.stats['documents_uploaded'],
                    st.session_state.stats['exports']
                ]
            })
            
            fig = px.bar(feature_data, x='Feature', y='Usage',
                        color='Usage',
                        color_continuous_scale='Purples',
                        title='Feature Usage Statistics')
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = px.pie(feature_data, values='Usage', names='Feature',
                        title='Feature Distribution',
                        color_discrete_sequence=px.colors.sequential.Purples_r)
            fig.update_layout(height=350)
            st.plotly_chart(fig, use_container_width=True)
        
        st.markdown("### 📝 Recent Queries")
        
        recent_queries = [msg['content'] for msg in st.session_state.messages if msg['role'] == 'user'][-5:]
        for i, query in enumerate(reversed(recent_queries), 1):
            st.markdown(f"""
            <div class="success-box">
                <strong>{i}.</strong> {query[:200]}{'...' if len(query) > 200 else ''}
            </div>
            """, unsafe_allow_html=True)
    
    else:
        st.info("📊 Start chatting to see analytics!")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p><strong>AI Research Co-Pilot Pro V3.0</strong></p>
    <p>Built by [Your Name] | Personal Project 2026</p>
    <p>Multi-Agent System • Web Search • Document Analysis • Export Reports</p>
    <p>Powered by Nebius AI</p>
</div>
""", unsafe_allow_html=True)