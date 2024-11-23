import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
from werkzeug.security import generate_password_hash

# Initialize Firebase Admin SDK
cred = credentials.Certificate(r"quizapp-36d3b-firebase-adminsdk-xierf-ff0961ee15.json")
firebase_admin.initialize_app(cred)

# Get Firestore client
db = firestore.client()

# Function to upload admins from Excel
def upload_admins(file_path):
    # Read Excel file
    df = pd.read_excel(file_path)

    # Iterate over rows and upload each admin's data
    for _, row in df.iterrows():
        admin_id = row['id']  # Ensure 'id' column is in the Excel file
        admin_data = {
            "name": row['name'],
            "email": row['email'],
            "password": generate_password_hash(row['password']),  # Securely hash password
            "school_id": row['school_id'],  # Link to school
            "role": row['role'],
            "created_at": firestore.SERVER_TIMESTAMP
        }

        # Add document to Firestore
        admin_ref = db.collection('admins').document(admin_id)
        admin_ref.set(admin_data)
        print(f"Added admin {admin_id}")

if __name__ == "__main__":
    # Path to your admins Excel file
    admins_file_path = r"excel\admins.xlsx"
    upload_admins(admins_file_path)
