# traceability_core.py
import os, re
from collections import defaultdict, deque
from pdfminer.high_level import extract_text
import networkx as nx
import numpy as np

STOP=set("the and is are was on for to of in student record system module etc data info".split())
AMBIG={"fast","user-friendly","etc","flexible","tbd","optimize","robust"}

def clean(t):
    return re.sub(r"\s+"," ",t).strip() if isinstance(t,str) else ""

def section_gap(a,b):
    A=[int(x) for x in re.findall(r"\d+",a)]
    B=[int(x) for x in re.findall(r"\d+",b)]
    L=max(len(A),len(B)); A+=[0]*(L-len(A)); B+=[0]*(L-len(B))
    return sum(abs(x-y) for x,y in zip(A,B))/(L or 1)

def ambiguity(s):
    if not isinstance(s,str): return 0
    toks = re.findall(r"[a-zA-Z']+", s.lower())
    vag = sum(w in s.lower() for w in AMBIG)
    return min(1, vag / (len(toks) / 12 + 1))

def volatility(s):
    t=s.lower()
    cue=sum(x in t for x in ["policy","as per","guideline","ugc","may"])
    return min(1, cue/3)

def kterms(s,k=6):
    toks=[t.lower() for t in re.findall(r"[A-Za-z']+",s) if len(t)>2 and t.lower() not in STOP]
    freq=defaultdict(int)
    for t in toks: freq[t]+=1
    return [w for w,_ in sorted(freq.items(), key=lambda x:-x[1])[:k]]

def parse_pdf_to_nodes(pdf_path):
    text = extract_text(pdf_path)
    nodes = []
    if not text: return nodes

    sections=[clean(s) for s in re.split(r"\n(?=\d+(\.\d+)*)",text) if clean(s)]
    req=[]
    for s in sections:
        m=re.match(r"(\d+(\.\d+)*)\s+(.*)",s)
        sec=m.group(1) if m else "0"
        lines=re.split(r"(?<=[.;])\s+|[\n•\-]\s+",s)
        for l in lines:
            if re.search(r"\b(shall|should|must|will)\b",l,re.I) and len(l)>25:
                req.append((sec,clean(l)))

    uniq=set()
    for s,t in req:
        if (s,t.lower()) not in uniq:
            uniq.add((s,t.lower()))
            nodes.append({
                "id":f"REQ-{len(uniq):03d}",
                "section":s,
                "text":t,
                "ambiguity":ambiguity(t),
                "volatility":volatility(t)
            })
    return nodes

def build_graph(nodes):
    G = nx.DiGraph()
    for r in nodes: G.add_node(r["id"],**r)
    idx=defaultdict(list)
    for r in nodes:
        for t in kterms(r["text"]): idx[t].append(r["id"])

    for r in nodes:
        cur=r["id"]
        for t in kterms(r["text"]):
            for o in idx[t]:
                if o!=cur and section_gap(r["section"],G.nodes[o]["section"])<=3:
                    ru,rv=G.nodes[cur],G.nodes[o]
                    sg=min(1, section_gap(ru["section"],rv["section"])/5)
                    cost = 0.5*((ru["ambiguity"]+rv["ambiguity"])/2) + \
                           0.3*((ru["volatility"]+rv["volatility"])/2) + \
                           0.15*sg + 0.05
                    G.add_edge(cur,o,cost=float(cost))
    return G

def keys(G,n): return set(kterms(G.nodes[n]["text"]))

def h(G,u,g):
    ku,kg = keys(G,u),keys(G,g)
    j = 1-(len(ku&kg)/max(len(ku|kg),1))
    s = section_gap(G.nodes[u]["section"],G.nodes[g]["section"])/10
    return 0.3*j + 0.2*s

def a_star(G,start,goal):
    import heapq
    pq=[(0,start)]; gc={start:0}; par={start:None}; seen=set(); pops=0
    while pq:
        _,u = heapq.heappop(pq)
        if u in seen: continue
        seen.add(u); pops+=1
        if u==goal:
            p=[u]
            while par[u] is not None: u=par[u]; p.append(u)
            return p[::-1], gc[p[-1]], pops
        for v in G.successors(u):
            nc = gc[u] + G[u][v]["cost"]
            if nc < gc.get(v,1e9):
                gc[v] = nc; par[v]=u
                heapq.heappush(pq,(nc+h(G,v,goal),v))
    return None,999,pops

def bfs(G,start,goal):
    q=deque([start]); par={start:None}; seen={start}; pops=0
    while q:
        u=q.popleft(); pops+=1
        if u==goal:
            p=[u]
            while par[u] is not None: u=par[u]; p.append(u)
            p=p[::-1]
            cost=sum(G[x][y]["cost"] for x,y in zip(p,p[1:]))
            return p,cost,pops
        for v in G.successors(u):
            if v not in seen:
                seen.add(v); par[v]=u; q.append(v)
    return None,999,pops
