import streamlit as st
import os
import json
import pickle
import numpy as np
from memory.episodic_manager import EpisodicManager
from memory.semantic_manager import SemanticManager
from memory.procedural_manager import ProceduralManager

st.set_page_config(page_title="OMNIMIND Memory Inspector", layout="wide")

# Sidebar navigation
st.sidebar.title("Memory Inspector")
view = st.sidebar.radio("Select Memory Type", ["Episodic Timeline", "Semantic Cluster Map", "Procedural Chain Graph"])

# Instantiate managers
episodic_manager = EpisodicManager()
semantic_manager = SemanticManager()
procedural_manager = ProceduralManager()

if view == "Episodic Timeline":
    st.header("Episodic Memory Timeline")
    episodes = episodic_manager.retrieve_sessions(limit=200)
    if not episodes:
        st.info("No episodic memory found.")
    else:
        # Timeline visualization
        for ep in episodes:
            st.markdown(f"**{ep['timestamp']}** | Session: `{ep['session_id']}`")
            st.write(f"- **User Query:** {ep['user_query']}")
            st.write(f"- **Agent Thoughts:** {ep['agent_thoughts']}")
            if ep.get('feedback'):
                st.write(f"- **Feedback:** {ep['feedback']}")
            if ep.get('extra'):
                st.write(f"- **Extra:** {ep['extra']}")
            st.markdown("---")

elif view == "Semantic Cluster Map":
    st.header("Semantic Memory Cluster Map")
    # Cluster and visualize
    labels = semantic_manager.cluster_vectors()
    vectors = semantic_manager._get_embeddings()
    if not vectors or not labels:
        st.info("No semantic clusters found.")
    else:
        # Reduce to 2D for visualization
        from sklearn.decomposition import PCA
        X = np.array(vectors)
        pca = PCA(n_components=2)
        X_2d = pca.fit_transform(X)
        import matplotlib.pyplot as plt
        import seaborn as sns
        fig, ax = plt.subplots(figsize=(8, 6))
        palette = sns.color_palette("hsv", len(set(labels)))
        for cluster_id in set(labels):
            idx = [i for i, l in enumerate(labels) if l == cluster_id]
            ax.scatter(X_2d[idx, 0], X_2d[idx, 1], label=f"Cluster {cluster_id}", s=30, color=palette[cluster_id % len(palette)])
        ax.set_title("Semantic Clusters (PCA)")
        ax.legend()
        st.pyplot(fig)

elif view == "Procedural Chain Graph":
    st.header("Procedural Memory Chain Graph")
    workflows = procedural_manager._load_workflows()
    if not workflows:
        st.info("No procedural workflows found.")
    else:
        import networkx as nx
        import matplotlib.pyplot as plt
        for wf in workflows:
            st.subheader(f"Workflow: {wf['workflow_id']}")
            G = nx.DiGraph()
            steps = wf.get('steps', [])
            for i, step in enumerate(steps):
                label = step.get('name', f"Step {i+1}")
                G.add_node(label)
                if i > 0:
                    prev_label = steps[i-1].get('name', f"Step {i}")
                    G.add_edge(prev_label, label)
            fig, ax = plt.subplots(figsize=(6, 3))
            nx.draw(G, with_labels=True, node_color='lightblue', ax=ax, node_size=1200, font_size=10, arrows=True)
            st.pyplot(fig)
            st.write(f"**Description:** {wf.get('description', '')}")
            st.write(f"**Tags:** {wf.get('tags', [])}")
            st.markdown("---") 