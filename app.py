# app.py - main interface

import streamlit as st
from analyzer import analyze_article
from utils import extract_from_url

#  set_page_config MUST be first 

st.set_page_config(
    page_title="AI Fake News Detector",
    page_icon="🔍",
    layout="centered"
)

#  Load CSS

with open("style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

#  Card function 

def show_analysis_cards(score, explanation, red_flags):
    if score >= 70:
        color = "#2ecc71"
        icon = "✅"
        label = "CREDIBLE"
    elif score >= 40:
        color = "#f39c12"
        icon = "⚠️"
        label = "NEEDS VERIFICATION"
    else:
        color = "#e94560"
        icon = "❌"
        label = "MISLEADING"

    # Main result card
    
    st.markdown(f"""
        <div class="result-card" style="border-color: {color};">
            <div class="result-icon">{icon}</div>
            <div class="result-label" style="color: {color};">{label}</div>
            <div class="result-subtitle">Analysis Complete</div>
        </div>
    """, unsafe_allow_html=True)

    # Metric cards row
    
    st.markdown(f"""
        <div class="cards-row">
            <div class="metric-card">
                <div class="metric-icon">🎯</div>
                <div class="metric-title">Trust Score</div>
                <div class="metric-value" style="color:{color};">{score}/100</div>
            </div>
            <div class="metric-card">
                <div class="metric-icon">🚩</div>
                <div class="metric-title">Red Flags</div>
                <div class="metric-value" style="color:#e94560;">{len(red_flags)}</div>
            </div>
            <div class="metric-card">
                <div class="metric-icon">📋</div>
                <div class="metric-title">Status</div>
                <div class="metric-value" style="color:{color}; font-size:16px;">{label}</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Explanation card
    
    st.markdown(f"""
        <div class="result-card" style="border-color:#1e4d7b; text-align:left; padding:25px;">
            <div class="metric-title">📝 WHY?</div>
            <p style="color:white; font-size:15px; margin-top:10px;">{explanation}</p>
        </div>
    """, unsafe_allow_html=True)

    # Red flags card
    
    if red_flags:
        flags_html = "".join([f'<p style="color:#e94560; font-size:15px;">🚩 {flag}</p>' for flag in red_flags])
        st.markdown(f"""
            <div class="result-card" style="border-color:#e94560; text-align:left; padding:25px;">
                <div class="metric-title">🚩 RED FLAGS FOUND</div>
                <div style="margin-top:10px;">{flags_html}</div>
            </div>
        """, unsafe_allow_html=True)

# MAIN CODE

st.title("🔍 AI Fake News Detector")
st.markdown("<p style='text-align:center; color:#aaaaaa; font-size:13px;'>| Created by Souvik Naskar | Powered by Gemini | </p>", unsafe_allow_html=True)
st.subheader("Paste an article or enter a URL")

input_type = st.radio("Input type", ["Paste text", "Enter URL"])

if input_type == "Paste text":
    article_text = st.text_area("Paste article here", height=200)
else:
    url = st.text_input("Enter article URL")
    article_text = extract_from_url(url) if url else ""

result = None
if st.button("Analyse Article") and article_text:
    with st.spinner("Analysing..."):
        result = analyze_article(article_text)

# ── STEP 4: Replace old result block with cards ────────
if result:
    show_analysis_cards(
        score=result.get("trust_score", 0),
        explanation=result.get("explanation", ""),
        red_flags=result.get("red_flags", [])
    )