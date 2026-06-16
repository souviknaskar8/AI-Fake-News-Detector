import streamlit as st

def show_header():
    st.title("🔍 AI Fake News Detector")
    st.markdown("<p style='text-align:center; color:#aaa;'>Powered by Google Gemini AI</p>", unsafe_allow_html=True)
    st.markdown("---")