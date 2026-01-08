import os
import litellm
import streamlit as st
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import BaseTool
from duckduckgo_search import DDGS

# --- 1. SECURE CREDENTIAL LOADING ---
# This looks for the secret you saved in the Streamlit Cloud Settings
if "OPENROUTER_API_KEY" in st.secrets:
    OPENROUTER_KEY = st.secrets["OPENROUTER_API_KEY"]
else:
    st.error("⚠️ API Key not found in Streamlit Secrets. Please add 'OPENROUTER_API_KEY' to your app settings.")
    st.stop()

# Bypass internal CrewAI checks
os.environ["OPENAI_API_KEY"] = "sk-dummy-key"

# --- 2. THE PRODUCTION ENGINE ---
def run_vavoulla_crew():
    # Elite Brain: Llama 3.3 70B
    vavoulla_llm = LLM(
        model="openrouter/meta-llama/llama-3.3-70b-instruct:free",
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_KEY,
        extra_body={"api_key": OPENROUTER_KEY}, # Crucial fix for 401/404 errors
        temperature=0.2, # Lower for extreme technical detail
        max_tokens=3000
    )

    class LuxuryTrendTool(BaseTool):
        name: str = "luxury_trend_scout"
        description: str = "Searches for 2026 luxury beauty aesthetics."
        def _run(self, query: str) -> str:
            try:
                with DDGS() as ddgs:
                    results = [r for r in ddgs.text(query, max_results=3)]
                    return "\n".join([f"{r['title']}: {r['body']}" for r in results])
            except: 
                return "Utilizing internal Vavoulla 'Quiet Luxury' database for 2026."

    # --- AGENTS (Ultra-Detailed Roles) ---
    strategist = Agent(
        role='Chief Aesthetic Strategist',
        goal='Analyze 2026 trends for "Quiet Luxury 2.0" and psychological pattern-interrupts.',
        backstory="""You are the lead trend forecaster for Vavoulla. You specialize in 
        sensory synergy—how lighting, textures, and specific 2026 pink hues (like 'Amber Flare') 
        evoke immediate desire in high-net-worth demographics.""",
        llm=vavoulla_llm, tools=[LuxuryTrendTool()]
    )

    director = Agent(
        role='Cinematic Cinematographer & Director',
        goal='Design a 15-second "Faceless" production script with exact technical specs.',
        backstory="""You are an award-winning commercial filmmaker. You speak in 
        technical lens data (85mm, 35mm Macro), lighting setups (Rembrandt, Golden Hour), 
        and camera movements (Parallax, Slow Tracking). Your goal is to defeat traditional 
        agencies with sheer visual precision.""",
        llm=vavoulla_llm
    )

    editor = Agent(
        role='Executive Brand Editor',
        goal='Package the output into an impeccable Director\'s Treatment.',
        backstory="""You refine all content into poetic luxury prose. You format data 
        into highly organized, professional Markdown tables. You are the gatekeeper of 
        the Vavoulla 'Soft Power' brand voice.""",
        llm=vavoulla_llm
    )

    # --- TASKS (Forcing Extreme Detail) ---
    t1 = Task(
        description="""Identify the 2026 'Quiet Luxury' color palette and one specific 
        'Pattern Interrupt' hook for a faceless beauty reel. Focus on 'Pink Flare' tones.""",
        expected_output="A luxury trend brief with hex codes and psychological triggers.",
        agent=strategist
    )

    t2 = Task(
        description="""Create a TECHNICAL 15-second production guide. 
        YOU MUST OUTPUT THREE DETAILED TABLES:
        1. THE SCRIPT TABLE: [Scene #] | [Time] | [Technical Visual] | [Audio/SFX] | [Text Overlay]
        2. CAMERA SPECS: Define Focal Length (e.g. 100mm Macro), FPS (60fps), and specific Camera Movement.
        3. LIGHTING/COLOR: Define Color Temp (Kelvin), Shadow Softness, and Vavoulla Pink LUT settings.""",
        expected_output="A comprehensive three-table technical breakdown.",
        agent=director
    )

    t3 = Task(
        description="""Format the response as a professional 'Director's Treatment'. 
        Remove all marketing fluff. Ensure the tables are impeccable and the language is poetic.""",
        expected_output="Final Impeccable Director's Treatment with three technical tables.",
        agent=editor
    )

    crew = Crew(agents=[strategist, director, editor], tasks=[t1, t2, t3], process=Process.sequential)
    return crew.kickoff()

# --- 3. THE LUXURY INTERFACE ---
st.title("💎 VAVOULLA ELITE PRODUCTION")
st.write("Generating technical, impeccable cinematic treatments for Instagram Reels.")

if st.button("🎬 INITIATE PRODUCTION TREATMENT"):
    with st.status("🔮 Orchestrating Creative Intelligence...", expanded=True) as status:
        try:
            result = run_vavoulla_crew()
            status.update(label="✅ Treatment Ready!", state="complete", expanded=False)
            
            st.divider()
            st.subheader("📽️ VAVOULLA: DIRECTOR'S TREATMENT")
            st.markdown(result.raw) # Displays the impeccable tables
            
            st.download_button(
                label="📥 Download Production Sheet",
                data=str(result.raw),
                file_name="vavoulla_elite_treatment.txt"
            )
        except Exception as e:
            st.error(f"Execution Error: {e}")
            st.info("Ensure your OpenRouter key has credits and the model 'llama-3.3-70b-instruct:free' is active.")

st.caption("Engine: Vavoulla v2.0-Elite | Aesthetic: Quiet Luxury 2.0")
