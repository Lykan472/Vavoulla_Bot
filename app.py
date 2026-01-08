import os
import litellm
import streamlit as st
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import BaseTool
from duckduckgo_search import DDGS

# --- 1. SYSTEM CONFIGURATION ---
st.set_page_config(page_title="Vavoulla Elite Production", page_icon="💎", layout="wide")

# Force LiteLLM to use the OpenRouter key for all calls
if "OPENROUTER_API_KEY" in st.secrets:
    # .strip() prevents accidental spaces which cause 401 errors
    OR_KEY = st.secrets["OPENROUTER_API_KEY"].strip()
    os.environ["OPENROUTER_API_KEY"] = OR_KEY
    # CrewAI sometimes looks for OPENAI_API_KEY even for other providers
    os.environ["OPENAI_API_KEY"] = OR_KEY 
else:
    st.error("⚠️ Secrets Error: Please add 'OPENROUTER_API_KEY' to your Streamlit Secrets.")
    st.stop()

# --- 2. THE PRODUCTION ENGINE ---
def run_vavoulla_crew():
    # Explicitly defining the OpenRouter LLM
    vavoulla_llm = LLM(
        model="openrouter/meta-llama/llama-3.3-70b-instruct:free",
        base_url="https://openrouter.ai/api/v1",
        api_key=OR_KEY,
        # 'extra_body' is the proven fix for OpenRouter 401 errors
        extra_body={
            "api_key": OR_KEY,
            "http_referer": "https://vavoulla.streamlit.app", # Recommended by OpenRouter
            "x-title": "Vavoulla Elite Creative"
        },
        temperature=0.2,
        max_tokens=3000
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
                return "Focusing on 2026 'Quiet Luxury' (Coquette Pink) aesthetics."

    # AGENTS
    strategist = Agent(
        role='Chief Aesthetic Strategist',
        goal='Analyze 2026 Quiet Luxury 2.0 trends and sensory hooks.',
        backstory="Trend expert for high-end fashion houses. Specializes in visual psychology.",
        llm=vavoulla_llm, tools=[LuxuryTrendTool()], verbose=True
    )

    director = Agent(
        role='Cinematic Director',
        goal='Design an impeccable 15s script with exact technical camera/light specs.',
        backstory="Award-winning filmmaker specializing in 'Faceless Luxury' content.",
        llm=vavoulla_llm, verbose=True
    )

    editor = Agent(
        role='Executive Brand Editor',
        goal='Refine output into a professional technical Director\'s Treatment.',
        backstory="Luxury editor ensures poetic prose and flawless table formatting.",
        llm=vavoulla_llm, verbose=True
    )

    # TASKS
    t1 = Task(description="Identify 2026 Pink hooks and palettes.", expected_output="Trend Brief", agent=strategist)
    t2 = Task(
        description="Write technical 15s script with 3 tables: Script, Camera Specs, and Lighting/Color.",
        expected_output="Three-table technical production guide.",
        agent=director
    )
    t3 = Task(
        description="Format into a professional Markdown 'Director's Treatment' with poetic Vavoulla language.",
        expected_output="Final Impeccable Treatment.",
        agent=editor
    )

    crew = Crew(agents=[strategist, director, editor], tasks=[t1, t2, t3], process=Process.sequential)
    return crew.kickoff()

# --- 3. UI LAYOUT ---
st.title("💎 VAVOULLA ELITE")
st.write("Professional Reels Production Engine")

if st.button("🎬 GENERATE PRODUCTION TREATMENT"):
    with st.status("💎 Orchestrating Creative Intelligence...", expanded=True) as status:
        try:
            result = run_vavoulla_crew()
            status.update(label="✅ Treatment Ready!", state="complete", expanded=False)
            st.divider()
            st.subheader("📽️ VAVOULLA: DIRECTOR'S TREATMENT")
            st.markdown(result.raw)
            st.download_button("📥 Download Script", data=str(result.raw), file_name="vavoulla_script.txt")
        except Exception as e:
            st.error(f"Execution Error: {e}")
