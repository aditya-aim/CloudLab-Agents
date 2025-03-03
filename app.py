import openai
import os
import time

# Set your OpenAI API key
api_key = "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"

# Root directory containing all project folders
root_dir = r"C:\Users\AnalyticsIndiaMag\Desktop\aditya\PROJECTS\AGENTS-22\PROJECT-3"

# Mapping folder names to their corresponding project titles
project_mapping = {
    "01_resume_gen": "AI Resume & Cover Letter Generator",
    "02_interview_coach": "AI Interview Coach",
    "03_study_planner": "AI Study Planner",
    "04_code_debugger": "AI Code Debugger & Optimizer",
    "05_story_writer": "AI Story & Novel Writer",
    "06_social_media_ai": "AI Social Media Post Generator",
    "07_productivity_ai": "AI Productivity Assistant",
    "08_journal_tracker": "AI Personal Journal & Mood Tracker",
    "09_investment_ai": "AI Investment Portfolio Analyzer",
    "10_cooking_ai": "AI Cooking Assistant",
    "11_language_buddy": "AI Language Learning Buddy",
    "12_email_assist": "AI Email Composer & Summarizer",
    "13_workout_ai": "AI Workout & Yoga Instructor",
    "14_legal_docs": "AI Legal Document Assistant",
    "15_meditation_ai": "AI Meditation & Mindfulness Coach",
    "16_parenting_ai": "AI Parenting Assistant",
    "17_art_gen": "AI Digital Art Generator",
    "18_budget_planner": "AI Home Budget Planner",
    "19_expense_tracker": "AI Shopping & Expense Tracker",
    "20_task_gamifier": "AI Productivity Gamifier"
}

def generate_readme(api_key, project_name, project_code):
    """Generates a README.md file content using OpenAI API."""
    prompt = f"""
        You are an expert in software documentation. Given the project name and its source code, generate a detailed and professional README.md file.

        ### **Project Name:**  
        {project_name}

        ### **Project Code:**  
        {project_code}

        ### **README Structure:**  
        1. **Project Title & Description**  
        - Start with an eye-catching title and a concise summary of what the project does.  

        2. **Project Overview**  
        - Explain the purpose of the project and who it is for.  
        - Highlight how it improves user experience or solves a problem.  

        3. **Key Features**  
        - List at least 4-5 main features with clear bullet points.  

        4. **Installation & Setup Guide**  
        - Provide step-by-step instructions for setting up the project locally.  
        - Include virtual environment setup (if applicable).  
        - Mention dependencies and provide a `pip install -r requirements.txt` command if necessary.  

        5. **Usage Instructions**  
        - Explain how to interact with the project after setup.  
        - If the project is a Streamlit app, include the command to run it (`streamlit run app.py`).  
        - Provide a walkthrough of major functionalities.  

        6. **Technology Stack**  
        - List the primary languages, frameworks, and APIs used.  

        7. **Additional Notes**  
        - Mention any extra configuration, limitations, or future improvements.  

        **Formatting Notes:**  
        - Use proper Markdown syntax.  
        - Ensure the README is well-structured and easy to read.  
    """

    response = openai.ChatCompletion.create(
        model="gpt-4o",
        messages=[{"role": "system", "content": "You are a professional software documentation writer."},
                  {"role": "user", "content": prompt}]
    )

    

    return response["choices"][0]["message"]["content"]

# Iterate over project folders one by one
for folder_name, project_name in project_mapping.items():
    project_path = os.path.join(root_dir, folder_name)
    readme_path = os.path.join(project_path, "README.md")

    # Check if project folder exists
    if os.path.exists(project_path):
        print(f"\nProcessing: {project_name} ({folder_name})")

        # Find the main project file (assuming app.py exists)
        main_file = os.path.join(project_path, "app.py")

        if os.path.exists(main_file):
            with open(main_file, "r", encoding="utf-8") as file:
                project_code = file.read()
        else:
            print(f"Warning: 'app.py' not found in {project_name}. Proceeding with an empty code block.")
            project_code = "No source code available."

        # Generate README content
        readme_content = generate_readme(api_key, project_name, project_code)

        # Save the README file in the project directory
        with open(readme_path, "w", encoding="utf-8") as readme_file:
            readme_file.write(readme_content)

        print(f"✅ README.md generated for {project_name}")

        # Wait a few seconds before moving to the next project (to avoid rate limits)
        time.sleep(2)

print("\n🎉 All README files have been successfully generated!")
