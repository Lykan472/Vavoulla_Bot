import os
import litellm
import streamlit as st
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import BaseTool
from duckduckgo_search import DDGS

# --- 1. BRAND SYSTEM CONFIGURATION ---
st.set_page_config(
    page_title="VAVOULLA: The Intentional Engine", 
    page_icon="🌿", 
    layout="wide"
)

# Secure Credential Loading
if "OPENROUTER_API_KEY" in st.secrets:
    OR_KEY = st.secrets["OPENROUTER_API_KEY"].strip()
    os.environ["OPENROUTER_API_KEY"] = OR_KEY
    os.environ["OPENAI_API_KEY"] = OR_KEY 
else:
    st.error("⚠️ Secrets Error: Please add 'OPENROUTER_API_KEY' to your Streamlit Secrets.")
    st.stop()

# --- 2. THE BRAND DNA ENGINE ---
def run_vavoulla_crew():
    # Llama 3.3 70B: High-reasoning model for intelligent, grounded prose
    vavoulla_llm = LLM(
        model="openrouter/meta-llama/llama-3.3-70b-instruct:free",
        base_url="https://openrouter.ai/api/v1",
        api_key=OR_KEY,
        extra_body={
            "api_key": OR_KEY,
            "http_referer": "https://vavoulla.streamlit.app",
            "x-title": "Vavoulla Intentional Production"
        },
        temperature=0.2 # Lower temperature for stability and calm assurance
    )

    class VavoullaInsightTool(BaseTool):
        name: str = "cultural_insight_scout"
        description: str = "Searches for real-life beauty friction and climate-aware makeup needs for Indian women."
        def _run(self, query: str) -> str:
            try:
                with DDGS() as ddgs:
                    results = [r for r in ddgs.text(query, max_results=3)]
                    return "\n".join([f"{r['title']}: {r['body']}" for r in results])
            except: 
                return "Focusing on skin-first, climate-aware beauty logic for the modern Indian woman."

    # --- AGENTS: VAVOULLA BRAIN TRUST ---
    
    anthropologist = Agent(
        role='Lead Brand Anthropologist',
        goal='Identify "Beauty Friction" and where Indian women feel overwhelmed by overconsumption.',
        backstory="""You are the guardian of the VAVOULLA ethos. You hate trend-chaos. 
        You study the daily lives of Indian women (18-32) to find where makeup feels 
        performative. You advocate for 'Calm Confidence' and 'Enough is Enough' logic.
        You ensure products align with Indian undertones and climate-aware needs.""",
        llm=vavoulla_llm, tools=[VavoullaInsightTool()], verbose=True
    )

    director = Agent(
        role='Quiet Luxury Visual Architect',
        goal='Design technical visual treatments that feel like a "reflective pause."',
        backstory="""Your visual language is 'Quiet Luxury 2.0.' You prioritize tactile surfaces 
        (stone, skin, fabric) and soft muted neutrals (dusty rose, stone grey). You focus 
        on close framing and skin-like textures. You believe in Sense over Spectacle and 
        Intention over Urgency.""",
        llm=vavoulla_llm, verbose=True
    )

    mentor = Agent(
        role='The Confident Older Sister (Voice of Vavoulla)',
        goal='Craft grounded, assured prose that values clarity and trust over aggressive persuasion.',
        backstory="""You are the 'thinking woman's' beauty guide. You never shout or use 
        FOMO-based marketing. Your tone is calm, intelligent, and grounded. You explain 
        'Why' a product exists and how it fits into a real, busy life. You value 
        resonance over reach.""",
        llm=vavoulla_llm, verbose=True
    )

    # --- TASKS: THE INTENTIONAL PIPELINE ---

    t1 = Task(
        description="""Analyze current Indian beauty friction. Identify one area where 
        'Loud' marketing is failing Indian women. Propose a Vavoulla alternative using 
        muted neutrals (Mauve, Stone, Rose) and skin-first practicality.""",
        expected_output="An Intentional Brand Brief focusing on practicality and emotional ease.",
        agent=anthropologist
    )

    t2 = Task(
        description="""Draft a 15-second Cinematic Script that feels like a pause.
        - [0-4s] THE OBSERVATION: A calm realization about daily life.
        - [4-11s] THE TACTILE ACT: Sensory, slow-motion (60fps) application of product on real skin.
        - [11-15s] THE CLARITY: An assured, grounded concluding thought.
        Visuals: Soft neutrals, natural light, stone/linen textures, close framing.""",
        expected_output="A three-table technical production guide: Script, Camera, and Lighting.",
        agent=director
    )

    t3 = Task(
        description="""Refine the script. Remove any 'salesy' or 'hype' language (viral, must-have, obsessed).
        Replace with poetic, assured, and intelligent prose. Format into a professional 
        Markdown 'Director's Treatment' for VAVOULLA.""",
        expected_output="Final Impeccable Treatment: A Production-Ready Aesthetic Guide.",
        agent=mentor
    )

    crew = Crew(agents=[anthropologist, director, mentor], tasks=[t1, t2, t3], process=Process.sequential)
    return crew.kickoff()

# --- 3. THE LUXURY INTERFACE ---
st.markdown("""
    <style>
    .stApp { background-color: #fcf8f8; color: #444; }
    .stButton>button {
        background: #D4B2B2; color: white; border: none; padding: 12px;
        border-radius: 4px; font-weight: 500; letter-spacing: 1px;
    }
    .stButton>button:hover { background: #C39F9F; border: none; color: white; }
    h1, h2, h3 { font-family: 'Georgia', serif; font-weight: 300; }
    </style>
    """, unsafe_allow_html=True)

st.title("🌿 VAVOULLA: INTENTIONAL BEAUTY")
st.write("Generating thoughtful production guides for the thinking woman.")

if st.button("📽️ GENERATE BRAND TREATMENT"):
    with st.status("🌿 Crafting intentional content...", expanded=True) as status:
        try:
            result = run_vavoulla_crew()
            status.update(label="✅ Treatment Ready", state="complete", expanded=False)
            st.divider()
            st.markdown(result.raw)
            st.download_button("📥 Export Production Sheet", data=str(result.raw), file_name="vavoulla_treatment.txt")
        except Exception as e:
            st.error(f"Execution Error: {e}")

st.caption("Aesthetic: Quiet Luxury 2.0 | Tone: The Confident Older Sister | Market: India")
