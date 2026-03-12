import streamlit as st
from google import genai
from pypdf import PdfReader

# 1. Page Configuration
st.set_page_config(page_title="Statecraft Matrix v15.0", layout="wide")

# 2. Sidebar: Reintroducing the Tripartite Framework Definitions
with st.sidebar:
    st.header("🏛️ Statecraft Framework")
    
    st.markdown("### ⚖️ Classical (Legalist)")
    st.info("**Focus:** State capacity, administrative tools (*Shu*), standardization (*Fa*), and strategic leverage (*Shi*). Based on Han Fei's principles of centralized control.")
    
    st.markdown("### 🚩 Leninist")
    st.error("**Focus:** Party supremacy, ideological discipline, vanguard mobilization, and safeguarding 'Political Security' (regime survival) above all else.")
    
    st.markdown("### 📈 Pragmatic")
    st.success("**Focus:** 'Seeking truth from facts.' Tangible economic targets, results-oriented problem solving, and technical constraints of the 15th Five-Year Plan.")
    
    st.markdown("---")
    api_key = st.text_input("Enter Gemini API Key:", type="password")
    st.success("🏗️ Engine: gemini-flash-latest")

# 3. App Title
st.title("🏛️ The Statecraft Matrix")
st.subheader("Geopolitical Risk & Market Opportunity Intelligence")
st.markdown("---")

# 4. Input Layout: Text Area above PDF Uploader
st.markdown("### 📥 Strategic Input")
manual_input = st.text_area("1. Paste Paragraph or Snippet for Rapid Testing:", height=200, 
                            placeholder="Paste specific chapters or editorials here...")

uploaded_file = st.file_uploader("2. Or Upload Full Policy Document (PDF):", type="pdf")

analyze_button = st.button("🚀 Execute Matrix Analysis")

# 5. The Analysis Logic
if analyze_button:
    if not api_key:
        st.error("⚠️ API Key required in sidebar.")
    else:
        try:
            client = genai.Client(api_key=api_key)
            
            # Text Aggregation
            final_text = ""
            if uploaded_file:
                with st.spinner("Processing PDF context..."):
                    reader = PdfReader(uploaded_file)
                    for page in reader.pages:
                        final_text += (page.extract_text() or "") + "\n"
            
            if manual_input:
                final_text += "\n" + manual_input

            if not final_text:
                st.error("⚠️ Please provide text or a PDF to analyze.")
                st.stop()

            # The Optimized Professional System Prompt
            sys_prompt = """
            You are a Senior Geopolitical Risk Strategist. Analyze the text using the Tripartite Statecraft Matrix.
            
            STRUCTURE:
            1. EXECUTIVE SUMMARY (TL;DR): Clinical takeaway of the document's primary strategic intent.
            2. TRIPARTITE BREAKDOWN:
               - LEGALIST: Focus on administrative tools (Shu), standardization (Fa), and state leverage (Shi).
               - LENINIST: Focus on Party leadership, ideological security, and mass mobilization.
               - PRAGMATIC: Focus on results-oriented policy and technical constraints.
            3. STRATEGIC RISK HEATMAP: A Markdown Table with columns: [Risk Category | Severity | Rationale].
            4. MARKET OPPORTUNITY INDEX: A Markdown Table identifying sectors where the state is 'Pragmatically' incentivizing investment or growth.
            5. ACTIONABLE ADVICE: 3 concrete, predictive steps for leadership.
            
            Tone: Clinical, data-driven, and focused on corporate implications. Skip all memo headers (To/From/Date).
            """

            st.markdown("---")
            st.markdown("### 📊 Strategic Analysis Output")
            
            def stream_data():
                response_stream = client.models.generate_content_stream(
                    model="gemini-flash-latest",
                    contents=f"{sys_prompt}\n\nCONTENT:\n{final_text}",
                    config={
                        "temperature": 0.1,
                        "max_output_tokens": 6000 
                    }
                )
                for chunk in response_stream:
                    if chunk.text:
                        yield chunk.text

            st.write_stream(stream_data)
                    
        except Exception as e:
            st.error(f"Analysis failed: {e}")
