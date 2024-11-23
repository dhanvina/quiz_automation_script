import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import ast  # For safely evaluating string lists

# Initialize Firebase Admin SDK
cred = credentials.Certificate(r"quizapp-36d3b-firebase-adminsdk-xierf-ff0961ee15.json")
firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()

def upload_quizzes_and_questions(quizzes_file_path):
    # Read both sheets from Excel
    quizzes_df = pd.read_excel(quizzes_file_path, sheet_name="Sheet1")
    questions_df = pd.read_excel(quizzes_file_path, sheet_name="Sheet2")

    # Process quizzes
    for _, quiz_row in quizzes_df.iterrows():
        quiz_id = quiz_row["quiz_id"]
        quiz_data = {
            "quiz_id": quiz_id,
            "title": quiz_row["title"],
            "is_Live": int(quiz_row["is_Live"]),
            "paper_type": quiz_row["paper_type"],
            "time_limit": int(quiz_row["time_limit"]),
            "questions": []  # Initialize empty questions array
        }

        # Filter questions belonging to this quiz
        quiz_questions = questions_df[questions_df["quiz_id"] == quiz_id]
        for _, question_row in quiz_questions.iterrows():
            # Build question data dynamically
            question_data = {
                "question": question_row["question"],
                "correct_option": question_row["correct_option"]
            }
            
            # Include options if available (for MCQ)
            if pd.notna(question_row["options"]):  # Check if options field is not empty
                question_data["options"] = ast.literal_eval(question_row["options"])  # Convert string to list

            # Add question to quiz
            quiz_data["questions"].append(question_data)

        # Upload to Firestore
        quiz_ref = db.collection("quizzes").document(quiz_id)
        quiz_ref.set(quiz_data)
        print(f"Uploaded quiz {quiz_id}")

if __name__ == "__main__":
    # Path to the Excel file
    excel_file_path = r"excel\quizzes.xlsx"
    upload_quizzes_and_questions(excel_file_path)
