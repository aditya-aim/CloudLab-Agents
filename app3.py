import shutil
import os

# Define paths
root_dir = r"C:\Users\AnalyticsIndiaMag\Desktop\aditya\PROJECTS\AGENTS-22\PROJECT-3 - Copy"
requirements_file = os.path.join(root_dir, "requirements.txt")

# Dictionary of project folders
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

# Copy the file to each project folder
if os.path.exists(requirements_file):
    for folder in project_mapping.keys():
        dest_folder = os.path.join(root_dir, folder)
        dest_file = os.path.join(dest_folder, "requirements.txt")

        # Ensure destination folder exists
        if os.path.exists(dest_folder):
            shutil.copy(requirements_file, dest_file)
            print(f"Copied to: {dest_file}")
        else:
            print(f"Skipping {folder}, folder does not exist.")
else:
    print("requirements.txt not found in root directory.")
