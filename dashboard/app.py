"""
OMNIMIND Dashboard App

Main application for the Thought Inspector UI.
"""

import streamlit as st
import json
from typing import Dict, Any
import requests
import os
import streamlit.components.v1 as components

def main():
    """Main dashboard application."""
    st.set_page_config(
        page_title="OMNIMIND - Thought Inspector",
        page_icon="🧬",
        layout="wide"
    )
    
    st.title("🧬 OMNIMIND - Thought Inspector")
    st.markdown("### The Autonomous, Self-Evolving Cognitive Kernel")
    
    # Sidebar
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choose a page",
        ["Overview", "Thought Chain", "Knowledge Graph", "Metrics", "Settings"]
    )
    
    if page == "Overview":
        show_overview()
    elif page == "Thought Chain":
        show_thought_chain()
    elif page == "Knowledge Graph":
        show_knowledge_graph()
    elif page == "Metrics":
        show_metrics()
    elif page == "Settings":
        show_settings()

def show_overview():
    """Show overview dashboard."""
    st.header("System Overview")
    
    # System status
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Active Agents", "3")
    
    with col2:
        st.metric("Knowledge Base", "1,247 entities")
    
    with col3:
        st.metric("Vector DB", "5,892 embeddings")
    
    with col4:
        st.metric("System Health", "🟢 Healthy")
    
    # Recent activity
    st.subheader("Recent Activity")
    st.write("No recent activity to display.")

def show_thought_chain():
    """Show thought chain visualization."""
    st.header("Thought Chain Analysis")
    
    # Placeholder for thought chain visualization
    st.write("Thought chain visualization will be implemented here.")
    
    # Sample thought chain data
    thought_chain = [
        {"step": 1, "thought": "Received query about AI safety", "confidence": 0.8},
        {"step": 2, "thought": "Retrieved relevant documents", "confidence": 0.9},
        {"step": 3, "thought": "Applied fact checking", "confidence": 0.7},
        {"step": 4, "thought": "Generated response", "confidence": 0.85}
    ]
    
    st.json(thought_chain)

def show_knowledge_graph():
    """Show knowledge graph visualization."""
    st.header("Knowledge Graph Explorer")
    
    st.write("Knowledge graph visualization will be implemented here.")
    
    # Placeholder for D3.js visualization
    st.markdown("""
    <div style="border: 1px solid #ddd; padding: 20px; text-align: center;">
        <p>Knowledge Graph Visualization (D3.js)</p>
        <p>This will show entity relationships and connections</p>
    </div>
    """, unsafe_allow_html=True)

def show_metrics():
    """Show metrics and monitoring, including Evidently drift report upload/viewer."""
    st.header("📊 Monitoring & Drift Detection")
    st.markdown("Upload reference and current data to generate an Evidently drift report.")
    ref_file = st.file_uploader("Reference Data (CSV)", type=["csv"], key="ref")
    cur_file = st.file_uploader("Current Data (CSV)", type=["csv"], key="cur")
    if st.button("Run Drift Report") and ref_file and cur_file:
        files = {"reference": ref_file, "current": cur_file}
        response = requests.post("http://localhost:8000/monitor/drift", files=files)
        if response.ok:
            report_path = response.json().get("report_path")
            st.success(f"Drift report generated: {report_path}")
            if os.path.exists(report_path):
                with open(report_path, "r") as f:
                    html = f.read()
                components.html(html, height=800, scrolling=True)
            else:
                st.info("Report file not found on this machine. Download from server if remote.")
        else:
            st.error("Failed to generate drift report.")

def show_settings():
    """Show system settings."""
    st.header("System Settings")
    
    # Configuration options
    st.subheader("Agent Configuration")
    
    agent_count = st.slider("Number of Agents", 1, 10, 3)
    confidence_threshold = st.slider("Confidence Threshold", 0.0, 1.0, 0.7)
    
    st.subheader("Model Settings")
    model_name = st.selectbox("Embedding Model", ["text-embedding-ada-002", "BGE", "Custom"])
    
    if st.button("Save Settings"):
        st.success("Settings saved successfully!")

if __name__ == "__main__":
    main() 