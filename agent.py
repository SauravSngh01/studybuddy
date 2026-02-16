import time
import random
import os

# --- 1. MOCK AGENT (For Testing/No Internet) ---
class MockStudyBuddy:
    """
    A fake agent that simulates AI responses without needing Ollama or Internet.
    """
    def __init__(self):
        print("--- MODE: MOCK AGENT (No Real AI) ---")

    def run(self, query: str) -> str:
        query = query.lower()
        time.sleep(1)  # Fake "thinking" delay

        if "plan" in query or "schedule" in query:
            return (
                "📅 **Mock Study Plan Created!**\n\n"
                "**Topic:** " + query.replace('plan', '').strip() + "\n"
                "- 10:00 AM: Basics & Introduction\n"
                "- 11:30 AM: Deep Dive into Concepts\n"
                "- 01:00 PM: Lunch Break\n"
                "- 02:00 PM: Practice & Quiz\n\n"
                "*(I can add this to your Google Calendar if you connect the API!)*"
            )
        
        elif "youtube" in query or "video" in query:
            return (
                "📺 **Mock Video Recommendations:**\n\n"
                "1. [Complete Guide to Topic (15:00)](https://www.youtube.com/watch?v=dQw4w9WgXcQ)\n"
                "2. [Crash Course: Exam Prep (12:45)](https://www.youtube.com/watch?v=dQw4w9WgXcQ)\n"
                "3. [Advanced Tips & Tricks (20:10)](https://www.youtube.com/watch?v=dQw4w9WgXcQ)"
            )

        elif "quiz" in query:
            return (
                "📝 **Mock Quiz Time!**\n\n"
                "**Q1:** What is the capital of France?\n(A) Berlin  (B) Madrid  (C) Paris\n\n"
                "**Q2:** What is 5 + 7?\n(A) 10  (B) 12  (C) 15"
            )
        
        else:
            return "I am in **Dummy Mode**. I can help you 'plan', find 'videos', or take a 'quiz'. Try asking one of those!"

# --- 2. REAL AGENT (Requires Ollama & LangChain) ---
class RealStudyBuddy:
    """
    The real AI Agent connecting to Ollama and Tools.
    """
    def __init__(self, model_name="llama3"):
        print(f"--- MODE: REAL AGENT ({model_name}) ---")
        try:
            from langchain_ollama import OllamaLLM
            from langchain.agents import initialize_agent, AgentType
            from langchain.tools import Tool
            # Import your actual tools here if you have them defined
            # from src.tools import get_youtube_videos, add_calendar_event
            
            self.llm = OllamaLLM(model=model_name)
            
            # Placeholder for tools - You will add real tools later
            self.tools = [] 
            
            self.agent = initialize_agent(
                self.tools, 
                self.llm, 
                agent=AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
                verbose=True,
                handle_parsing_errors=True
            )
        except ImportError:
            print("CRITICAL ERROR: LangChain or Ollama not installed correctly.")
            raise

    def run(self, query: str) -> str:
        try:
            # If you haven't set up the agent tools yet, we just use the raw LLM
            # return self.agent.run(query) 
            return self.llm.invoke(query)
        except Exception as e:
            return f"Error connecting to Ollama: {str(e)}. Is 'ollama serve' running?"

# --- 3. SWITCHER FUNCTION ---
def get_agent(use_dummy_llm: bool = True):
    """
    Returns either the Mock agent or the Real agent based on the flag.
    """
    if use_dummy_llm:
        return MockStudyBuddy()
    else:
        # You can change "llama3" to "mistral" if you downloaded that instead
        return RealStudyBuddy(model_name="llama3")