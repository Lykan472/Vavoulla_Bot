import os
import litellm
import streamlit as st
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import BaseTool
from duckduckgo_search import DDGS

# --- 1. SYSTEM CONFIGURATION & UI ---
st.set_page_config(page_title="Vavoulla Elite Production", page_icon="💎", layout="wide")

# Force LiteLLM to use the OpenRouter key
if "OPENROUTER_API_KEY" in st.secrets:
    OR_KEY = st.secrets["OPENROUTER_API_KEY"].strip()
    # We set these to ensure LiteLLM has zero excuses for failing auth
    os.environ["OPENROUTER_API_KEY"] = OR_KEY
    os.environ["OPENAI_API_KEY"] = OR_KEY 
else:
    st.error("⚠️ Secrets Error: Please add 'OPENROUTER_API_KEY' to your Streamlit Secrets.")
    st.stop()

# --- 2. THE PRODUCTION ENGINE ---
def run_vavoulla_crew():
    # The fix for 401: We pass the key inside 'extra_body' and 'headers'
    vavoulla_llm = LLM(
        model="openrouter/meta-llama/llama-3.3-70b-instruct:free",
        base_url="https://openrouter.ai/api/v1",
        api_key=OR_KEY,
        # Mandatory OpenRouter headers for stability
        extra_body={
            "api_key": OR_KEY,
            "http_referer": "https://vavoulla.streamlit.app",
            "x-title": "Vavoulla Elite Creative"
        },
        temperature=0.2,
        max_tokens=3500
    )

    class LuxuryTrendTool(BaseTool):
        name: str = "luxury_trend_scout"
        description: str = "Searches for 2026 luxury beauty and cinematic trends."
        def _run(self, query: str) -> str:
            try:
                with DDGS() as ddgs:
                    results = [r for r in ddgs.text(query, max_results=3)]
                    return "\n".join([f"{r['title']}: {r['body']}" for r in results])
            except: 
                return "Focusing on 2026 'Quiet Luxury' (Coquette Pink) internal data."

    # --- AGENTS (The "Director" Level Brains) ---
    strategist = Agent(
        role='Chief Aesthetic Strategist',
        goal='Analyze 2026 Quiet Luxury 2.0 trends and sensory hooks.',
        backstory="Trend forecaster specializing in visual psychology and premium palettes.",
        llm=vavoulla_llm, tools=[LuxuryTrendTool()]
    )

    director = Agent(
        role='Cinematic Cinematographer',
        goal='Design an impeccable 15s script with exact technical camera/light specs.',
        backstory="Award-winning filmmaker. Expert in lens selection and lighting temperatures.",
        llm=vavoulla_llm
    )

    editor = Agent(
        role='Executive Brand Editor',
        goal='Refine output into a professional technical Director\'s Treatment.',
        backstory="Luxury editor ensures poetic prose and flawless table formatting.",
        llm=vavoulla_llm
    )

    # --- TASKS (Multi-Table Output) ---
    t1 = Task(description="Identify 2026 Pink hooks and palettes.", expected_output="Trend Brief", agent=strategist)
    
    t2 = Task(
        description="""Create a TECHNICAL 15-second production guide. 
        YOU MUST OUTPUT THREE TABLES:
        1. SCRIPT: [Time] | [Action] | [Audio] | [Text]
        2. CAMERA: [Lens] | [FPS] | [Movement]
        3. LIGHTING: [Kelvin] | [Setup Type] | [Shadow Mix]""",
        expected_output="Three-table technical production guide.",
        agent=director
    )
    
    t3 = Task(
        description="Format into a professional 'Director's Treatment' with poetic Vavoulla language.",
        expected_output="Final Impeccable Treatment with tables.",
        agent=editor
    )

    crew = Crew(agents=[strategist, director, editor], tasks=[t1, t2, t3], process=Process.sequential)
    return crew.kickoff()

# --- 3. UI LAYOUT ---
st.title("💎 VAVOULLA ELITE")
st.write("Professional Script Production via Llama 3.3 70B")

if st.button("🎬 GENERATE PRODUCTION TREATMENT"):
    with st.status("💎 Orchestrating Creative Intelligence...", expanded=True) as status:
        try:
            result = run_vavoulla_crew()
            status.update(label="✅ Treatment Ready!", state="complete", expanded=False)
            st.divider()
            st.markdown(result.raw)
            st.download_button("📥 Download Script", data=str(result.raw), file_name="vavoulla_script.txt")
        except Exception as e:
            st.error(f"Execution Error: {e}")
            if "401" in str(e):
                st.warning("Authentication failed. Ensure your OpenRouter key is fresh and account has credits.")
