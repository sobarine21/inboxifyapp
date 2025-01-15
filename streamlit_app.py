import subprocess
from fastapi import FastAPI
from pydantic import BaseModel
from email_validator import validate_email, EmailNotValidError
import dns.resolver
import smtplib
import streamlit as st
import threading

# FastAPI App
app = FastAPI()

class EmailRequest(BaseModel):
    email: str
    blacklist: list

@app.post("/validate_email")
def validate_email_address(request: EmailRequest):
    email = request.email
    blacklist = request.blacklist

    try:
        validate_email(email)
    except EmailNotValidError as e:
        return {"email": email, "status": "Invalid", "message": str(e)}

    # Add DNS and SMTP checks here...
    return {"email": email, "status": "Valid", "message": "Email is valid"}

# Streamlit App
def run_streamlit():
    # Streamlit app logic
    st.title("Email Validator - Streamlit")
    email = st.text_input("Enter your email:")
    blacklist = st.text_area("Enter blacklist domains (comma-separated):")

    if st.button("Validate"):
        import requests

        # Call FastAPI
        response = requests.post(
            "http://127.0.0.1:8000/validate_email",
            json={"email": email, "blacklist": blacklist.split(",")},
        )

        if response.status_code == 200:
            result = response.json()
            st.write(f"Status: {result['status']}")
            st.write(f"Message: {result['message']}")
        else:
            st.write("Error in API response")

# Run FastAPI and Streamlit concurrently
def run_both():
    threading.Thread(target=lambda: subprocess.run(["uvicorn", "main:app", "--reload"])).start()
    run_streamlit()

if __name__ == "__main__":
    run_both()
