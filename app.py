import os
import streamlit as st
from crewai import Agent, Task, Crew, Process, LLM
from crewai.tools import BaseTool
from duckduckgo_search import DDGS

# --- 1. SYSTEM CONFIGURATION ---
st.set_page_config(page_title="Vavoulla Director's Suite", page_icon="🎬", layout="wide")

# This works for both local and online deployment
if "OPENROUTER_API_KEY" in st.secrets:
    OPENROUTER_KEY = st.secrets["OPENROUTER_API_KEY"]
else:
    st.error("Missing OpenRouter API Key. Please add it to your secrets.")
    st.stop()

os.environ["OPENAI_API_KEY"] = "sk-dummy-key" 

def run_vavoulla_crew():
    # Using Llama 3.3 70B for high-precision formatting
    vavoulla_llm = LLM(
        model="openrouter/meta-llama/llama-3.3-70b-instruct:free",
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_KEY,
        temperature=0.2, # Ultra-focused on structure
        max_tokens=3000
    )

    # --- AGENTS ---
    strategist = Agent(
        role='Luxury Brand Strategist',
        goal='Define the "Vavoulla" 2026 aesthetic and psychological hook points.',
        backstory="Expert in high-end consumer behavior. You provide the 'why' behind the visual.",
        llm=vavoulla_llm
    )

    director = Agent(
        role='Cinematic Director & Cinematographer',
        goal='Create a technical 15s script with exact camera movements, focal lengths, and lighting.',
        backstory="""You speak in technical film language. You don't say 'show the product'; 
        you say 'Slow 60fps tracking shot, 85mm lens, f/1.8 for shallow depth of field.'""",
        llm=vavoulla_llm
    )

    editor = Agent(
        role='Executive Producer',
        goal='Package the output into a professional Director\'s Treatment.',
        backstory="You organize chaos into world-class documents. You ensure every detail is impeccably presented.",
        llm=vavoulla_llm
    )

    # --- TASKS (THE FIX FOR STRUCTURE) ---
    t1 = Task(
        description="Identify the 2026 'Quiet Luxury' color story for Vavoulla (Hex: #FFC5C5 and variants). Define the 'Pattern Interrupt' hook.",
        expected_output="A brand strategy brief.",
        agent=strategist
    )

    t2 = Task(
        description="""Create a TECHNICAL 15-second production script. 
        YOU MUST PROVIDE THREE TABLES:
        
        1. THE SCRIPT TABLE: [Scene #] | [Time] | [Technical Visual] | [Audio/SFX] | [Text Overlay]
        2. CAMERA SPECS: Define lens type (Macro/Wide), Frame Rate (60fps/24fps), and Camera Movement for each beat.
        3. LIGHTING & COLOR: Define Color Temperature (Kelvin), Shadow Depth, and 'Vavoulla Pink' LUT settings.""",
        expected_output="A three-table technical production breakdown.",
        agent=director
    )

    t3 = Task(
        description="""Review the technical tables. Ensure the language is high-end. 
        Format the entire response as a professional 'Director's Treatment' with clear headings, bold text, and perfectly aligned tables.""",
        expected_output="The final impeccable Director's Treatment.",
        agent=editor
    )

    crew = Crew(agents=[strategist, director, editor], tasks=[t1, t2, t3], process=Process.sequential)
    return crew.kickoff()

# --- 2. LUXURY FRONTEND ---
st.title("🎬 Vavoulla Director's Treatment Engine")
st.write("Generate professional-grade cinematic production guides for 2026.")

if st.button("🌟 INITIATE PRODUCTION"):
    with st.status("💎 Architecting Visual Narrative...", expanded=True) as status:
        try:
            result = run_vavoulla_crew()
            status.update(label="✅ Treatment Ready!", state="complete", expanded=False)
            
            st.divider()
            st.markdown(result.raw) # This will now display the detailed tables
            
            st.download_button("📥 Download PDF/Text Treatment", data=str(result.raw), file_name="vavoulla_director_treatment.txt")
        except Exception as e:
            st.error(f"Error: {e}")

st.caption("Technical Mode: On | Aesthetic: Quiet Luxury 2.0")