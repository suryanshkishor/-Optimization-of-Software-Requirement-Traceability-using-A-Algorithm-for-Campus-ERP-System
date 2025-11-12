#pip install streamlit networkx matplotlib pdfminer.six
#streamlit run app.py
import os
import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt
from traceability_core import parse_pdf_to_nodes, build_graph, a_star, bfs

st.set_page_config(page_title="Campus ERP Traceability", layout="wide")
st.title("📘 Campus ERP – Requirement Traceability using A* Algorithm")

mode = st.radio("PDF Source:", ["Use SRS.pdf", "Upload PDF"])

# ✅ Load PDF
if mode == "Upload PDF":
    uploaded = st.file_uploader("Upload SRS PDF", type=["pdf"])
    if not uploaded:
        st.stop()
    pdf_path = "uploaded_srs.pdf"
    with open(pdf_path, "wb") as f:
        f.write(uploaded.read())
else:
    pdf_path = "SRS.pdf"
    if not os.path.exists(pdf_path):
        st.error("⚠️ Place `SRS.pdf` in this folder.")
        st.stop()

st.info("⏳ Reading SRS & extracting requirements...")
nodes = parse_pdf_to_nodes(pdf_path)
G = build_graph(nodes)

st.success(f"✅ Extracted {len(nodes)} requirements and {G.number_of_edges()} links")

# ✅ Requirement Mapping Table
st.subheader("📄 Requirement Table (ID → Text)")
mapping_df = [{"ID": n["id"], "Section": n["section"], "Requirement Text": n["text"]} for n in nodes]
st.dataframe(mapping_df, use_container_width=True, height=300)

# ✅ Selection Boxes
ids = [n["id"] for n in nodes]
start = st.selectbox("Start Requirement", ids, index=0)
goal = st.selectbox("Goal Requirement", ids, index=min(1, len(ids)-1))

# ✅ Run Search and Plot Graph
if st.button("Run A* vs BFS Search"):
    ap,ac,ax = a_star(G,start,goal)
    bp,bc,bx = bfs(G,start,goal)

    # Results
    st.subheader("🔎 Algorithm Results")
    st.write(f"**A\\*** Path: `{ap}` | Cost: `{ac:.3f}` | Steps: `{ax}`")
    st.write(f"**BFS** Path: `{bp}` | Cost: `{bc:.3f}` | Steps: `{bx}`")

    gain = (bx-ax)/bx*100 if bx > 0 else 0
    st.success(f"🚀 A* is **{gain:.2f}% faster** than BFS")

    # ✅ Build simple fixed graph
    st.subheader("📌 Requirement Traceability Graph (Static View)")

    H = G.copy()
    
    # Convert REQ-001 → R1, REQ-002 → R2, ...
    label_mapping = {n: n.replace("REQ-", "R") for n in H.nodes()}
    H = nx.relabel_nodes(H, label_mapping)

    # Node positions fixed for consistent look
    pos = nx.spring_layout(H, seed=7)

    plt.figure(figsize=(10, 8))

    # Draw nodes
    nx.draw_networkx_nodes(H, pos, node_size=800, node_color="skyblue")

    # Draw plain black edges
    nx.draw_networkx_edges(H, pos, edge_color="black", arrows=False)

    # Label nodes
    nx.draw_networkx_labels(H, pos, font_size=10, font_weight="bold")

    plt.axis("off")
    st.pyplot(plt)
