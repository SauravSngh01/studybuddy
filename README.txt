🎓 StudyBuddy: Agentic AI Study Planner
StudyBuddy is an intelligent, Agentic AI-powered assistant designed to help students manage their studies. Unlike a simple chatbot, StudyBuddy can take action: it creates personalized study schedules, integrates with Google Calendar, curates relevant YouTube tutorials, and generates quizzes to test your knowledge.

It is built using Python, LangChain, and Streamlit, and it runs locally using Ollama (Llama 3 / Mistral), ensuring privacy and zero API costs.

🚀 Features
📅 Autonomous Scheduling: Creates study plans and (optionally) adds them to your Google Calendar.

📺 Content Curation: Automatically searches and suggests the best YouTube videos for your topics.

🤖 Local AI Brain: Runs entirely on your machine using Ollama (no OpenAI API keys needed).

📝 Active Recall: Generates instant quizzes to test your understanding of a topic.

⚡ Dual Mode: Works in "Dummy Mode" (for testing without high-end hardware) and "Real Mode" (for full AI capabilities).

🛠️ Tech Stack
Frontend: Streamlit

AI Framework: LangChain & LangChain-Ollama

LLM Engine: Ollama (Llama 3 or Mistral)

Tools: Google Calendar API, YouTube Search

Language: Python 3.10+

📋 Prerequisites
Before you begin, ensure you have the following installed on your Windows machine:

Python (3.10 or later): Download Here

Important: Check the box "Add Python to PATH" during installation.

Ollama (for Real AI mode): Download Here

⚙️ Installation Guide (Windows)
Follow these steps to set up the project from scratch.

1. Download the Project
Download the project zip file or clone it using git:

PowerShell
git clone https://github.com/yourusername/studybuddy.git
cd studybuddy
2. Create a Virtual Environment
This keeps your project dependencies separate from your system. Open your Command Prompt (cmd) or PowerShell in the project folder and run:

PowerShell
python -m venv venv
3. Activate the Environment
Command Prompt (cmd):

DOS
venv\Scripts\activate.bat
PowerShell:

PowerShell
venv\Scripts\Activate.ps1
(If you get a permission error in PowerShell, run Set-ExecutionPolicy Unrestricted -Scope Process first).

You should see (venv) appear at the start of your command line.

4. Install Dependencies
Run the following command to install all required libraries:

PowerShell
pip install -r requirements.txt
🧠 Setting Up the AI (Ollama)
If you want to use the Real AI capabilities, you need to download the brain model.

Install Ollama from the link in Prerequisites.

Open a new terminal window and run:

PowerShell
ollama run llama3
(You can also use ollama run mistral if you prefer).

Once it loads and you see a chat prompt (>>>), you can type /bye to exit, but keep the Ollama app running in the system tray.

🎮 How to Run the App
1. Configure the Mode
Open main.py in a text editor (like Notepad or VS Code). Look for this line at the top:

Python
# Set this to False when you want to use the Real AI (Ollama)
USE_DUMMY_LLM = True 
For Testing/Demo: Set it to True. The app will work instantly with fake data (no heavy AI needed).

For Real Usage: Set it to False. Ensure Ollama is running.

2. Start the Application
In your terminal (make sure (venv) is active), run:

PowerShell
streamlit run main.py
3. Usage
The app will open in your browser at http://localhost:8501.

Ask for a Plan: "Create a study schedule for Python loops."

Ask for Videos: "Find me tutorials on Matrix Multiplication."

Take a Quiz: "Give me a quiz on Biology."

📅 Google Calendar Integration (Optional)
To enable real calendar events (instead of just text plans):

Go to the Google Cloud Console.

Create a project and enable the Google Calendar API.

Download the OAuth 2.0 Client credentials and save the file as credentials.json in the main project folder.

The first time you ask the AI to "Schedule" something, a browser window will pop up asking you to log in to Google.

🐛 Troubleshooting
'streamlit' is not recognized...:

Make sure you activated the virtual environment (venv\Scripts\activate).

Try running: python -m streamlit run main.py

ConnectionRefusedError (in Real Mode):

Ollama is not running. Open a separate terminal and type ollama serve.

Model not found:

You might have downloaded a different model (e.g., Mistral) but the code expects Llama 3. Update model="llama3" in src/agent.py to match what you have.