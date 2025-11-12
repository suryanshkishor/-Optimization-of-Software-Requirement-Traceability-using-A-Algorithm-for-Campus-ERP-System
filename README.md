# -Optimization-of-Software-Requirement-Traceability-using-A-Algorithm-for-Campus-ERP-System

# 🤖 Optimization of Software Requirement Traceability using A* Algorithm for Campus ERP System  

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/Framework-Streamlit-red)
![AI](https://img.shields.io/badge/Field-Artificial%20Intelligence-purple)
![License](https://img.shields.io/badge/License-MIT-green)

---

## 🎓 Project Overview  

This project demonstrates the application of the **A\* (A-Star) Search Algorithm** in optimizing **Software Requirement Traceability (SRT)** within a **Campus ERP System**.  
It integrates **AI search techniques** with real-world software engineering processes, helping developers trace, link, and manage requirements efficiently.

This system is designed for academic and real-life ERP use cases — making requirement tracking intelligent, visual, and data-driven.

---

## 🧩 Objectives  

- Automate requirement traceability using the A\* algorithm  
- Visualize dependency graphs between requirements  
- Compare A\* with traditional BFS in terms of efficiency  
- Provide a Streamlit-based interactive dashboard for demonstration  
- Build a scalable model applicable to real ERP systems (like CGU ERP)  

---

## ⚙️ Tech Stack  

| Component | Technology Used |
|------------|----------------|
| Programming Language | Python 🐍 |
| Framework | Streamlit |
| Graph Engine | NetworkX |
| Visualization | Matplotlib |
| PDF Parsing | pdfminer.six |
| IDE | Visual Studio Code |

---

## 🧠 Algorithmic Model  

### A* Search Formula:
\[
f(n) = g(n) + h(n)
\]

Where:  
- `g(n)` → actual cost from start node to current node  
- `h(n)` → heuristic (predicted cost to goal node)  

The algorithm finds **optimal paths** between requirements, minimizing complexity in large software documentation.

---

## 🧮 System Architecture  

📁 **Input:** SRS (Software Requirement Specification) PDF  
🔄 **Processing:**  
1. Extract requirements (via NLP + PDF parser)  
2. Build a requirement graph (NetworkX)  
3. Run A\* and BFS algorithms  
4. Compare and visualize traceability  
📊 **Output:** Interactive Streamlit dashboard with graphs, tables, and stats  

---

## 🧰 Installation  

### Step 1: Clone the Repository  
```bash
git clone https://github.com/<your-username>/Campus-ERP-Traceability-AStar.git
cd Campus-ERP-Traceability-AStar

Step 2: Install Required Libraries
pip install streamlit networkx matplotlib pdfminer.six

Step 3: Run the Application
streamlit run app.py

💻 User Instructions
Launch the Streamlit app.
Upload your SRS.pdf file.
Choose A* or BFS mode.
View the requirement traceability graph and path comparisons.
Download analysis reports from the output section.

