# Gemini-Powered Homework Agent System

This project demonstrates a multi-agent orchestration system using the `openai-agents` SDK. It features a Triage Agent that routes queries to specialized Math and History tutors, but only after passing through a custom Homework Guardrail.

## 🛠 Features
- **Gemini 2.0 Flash Integration**: Uses the OpenAI-compatible endpoint for Google Gemini.
- **Agentic Triage**: Automatically routes user queries to the correct specialist.
- **Input Guardrails**: Prevents the agents from answering non-homework related questions.
- **Modular Design**: Clean separation between connection logic and agent logic.

## 📂 Project Structure
- `connection.py`: Handles API authentication and `RunConfig` setup.
- `main.py`: Defines agents, tools, and the guardrail logic.
- `.env`: (Hidden) Stores your `GEMINI_API_KEY`.

## 🚀 Getting Started

### 1. Install Dependencies
```bash
pip install openai-agents python-dotenv
```

### 2. Setup Environment Variables

Create a `.env` file in the root directory:

```text
GEMINI_API_KEY=your_gemini_api_key_here

```

### 3. Run the Application

```bash
python main.py

```

## 🤖 How it Works

1. **Guardrail Agent**: Analyzes the input to see if it qualifies as "homework."
2. **Triage Agent**: If valid, it "hands off" the conversation to either the Math Tutor or History Tutor.
3. **Execution**: The `Runner` handles the state and ensures the correct model configuration is used across all agents.

```

---
### 4. Summary of commands for GitHub

If you are initializing this via terminal:

```bash
# Initialize repo
git init

# Add files
git add .

# Commit
git commit -m "Initial commit: Homework Agent with Gemini Guardrails"
