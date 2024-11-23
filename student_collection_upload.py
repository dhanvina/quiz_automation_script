import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd

# Initialize Firebase Admin SDK
cred = credentials.Certificate(r"quizapp-36d3b-firebase-adminsdk-xierf-ff0961ee15.json")
firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()

# Function to upload students from Excel
def upload_students_from_excel(file_path):
    # Read Excel file
    df = pd.read_excel(file_path)

    # Iterate over rows and upload each student's data
    for _, row in df.iterrows():
        student_id = row['id']  # Ensure the Excel file has an 'id' column
        student_data = {
            "name": row['name'],
            "school": row['school'],  # School name
            "roll_number": row['roll_number'],
            "quiz_results": [],  # Initially empty
            "has_attempted_live_quiz": False,  # Initially False
            "class": row.get('class', ''),  # Optional field if present in the Excel
            "password": row['school_code'],  # Using school_code as the password
            "school_code": row['school_code']  # Storing school_code separately
        }

        # Add document to Firestore
        student_ref = db.collection('students').document(student_id)
        student_ref.set(student_data)
        print(f"Added student {student_id}")

if __name__ == "__main__":
    # Path to your Excel file
    excel_file_path = r"excel\students.xlsx"
    upload_students_from_excel(excel_file_path)
