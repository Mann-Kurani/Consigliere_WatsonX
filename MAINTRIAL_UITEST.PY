import streamlit as st
import os
from ibm_watsonx_ai.foundation_models import Model

# Function to get credentials
def get_credentials():
    return {
        "url": "https://us-south.ml.cloud.ibm.com",
        "apikey": st.text_input("Please enter your API key", type="password")
    }

# Define model parameters and other variables
model_id = "meta-llama/llama-3-70b-instruct"
parameters = {
    "decoding_method": "sample",
    "max_new_tokens": 500,
    "stop_sequences": ["Thank You"],
    "temperature": 0.3,
    "top_k": 88,
    "top_p": 0.5,
    "repetition_penalty": 1
}

# Get environment variables
project_id = os.getenv("PROJECT_ID")
space_id = os.getenv("SPACE_ID")

# Streamlit app
st.title("Email Summarization App")

st.write("This app summarizes and ranks emails based on their content.")

# Input for user
prompt_example = """Rank the emails with importance of the given profile.
Make sure to add adequete details while summarizing them like names and dates

Input: Emails with a profile These are a CEO's emails:

From: Sarah Lewis sarah.lewis@company.com
Subject: Upcoming Board Meeting Agenda
Date: 2024-08-24 16:10:00
Plain Text Content:
Dear [CEO's Name],

This is to confirm the agenda for our upcoming board meeting scheduled for August 30th. Please review the attached document for a detailed breakdown of topics to be discussed.

Agenda Highlights:

Q2 Financial Overview
Strategic Plan Review
New Project Proposals
If there are additional items you wish to include or changes needed, please let me know by August 27th.

Thank you,

Sarah Lewis
Executive Assistant

... (rest of the prompt_example as provided) ...

Give me important emails with ranks and make sure to highlight important deadlines from the given input email only. DO NOT give replies to these emails after summarizing. Dont take any input from the examples. Summarize them with some details Top Important Mails:
1. Agenda for board meeting on August 30th.
2. New compliance regulations summary.
3. Marketing campaign proposal due for feedback by August 30th.
4. Results of the employee engagement survey.

Deadlines and Action Required Mails:
1. IT maintenance scheduled with expected downtime.
2. Add missing elective by Friday 5:00 PM.
3. Revise and resubmit paper with missing references by tomorrow 5:00 PM.

Invitations to Events:
No Invitation

Thank You

Input: Emails with a profile These are a Student's emails:

From: Professor Adams professor.adams@college.edu
Subject: Midterm Exam Schedule
Date: 2024-08-24 10:00:00
Plain Text Content:
Dear [Student's Name],

This is to inform you about the midterm exam schedule for this semester. Please find the details below:

Math 101: September 5th, 10:00 AM - 12:00 PM
History 202: September 7th, 2:00 PM - 4:00 PM
Biology 303: September 10th, 9:00 AM - 11:00 AM
Ensure you are prepared and review the topics listed in the syllabus.

Best regards,
Professor Adams

... (rest of the prompt_example as provided) ...

Give me important emails with ranks and make sure to highlight important deadlines from the given input email only. DO NOT give replies to these emails after summarizing. Dont take any input from the examples. Summarize them with some details Top Important Mails:
1. Midterm exam schedule.
2. Advising appointment confirmation.
3. New study rooms reservation system.
4. Internet outage notification.

Deadlines and Action Required Mails:
1. Flu shot clinic dates.
2. Group project meeting on August 28th.
3. Review of campus safety tips.

Invitations to Events:
1. Welcome Back BBQ on August 30th.
2. Yoga class schedule.

Thank You

Input: Emails with a profile These are a doctor's emails:

From: Dr. Alice Roberts alice.roberts@clinic.com
Subject: Urgent: Critical Patient Report for Review
Date: 2024-08-24 16:15:00
Plain Text Content:
Dear Dr. [Doctor's Name],

Please review the attached critical patient report for immediate attention. The report concerns Patient John Doe, who has shown severe symptoms that require urgent intervention.

Key Details:

Patient Name: John Doe
Symptoms: Severe abdominal pain, high fever
Recommended Action: Immediate diagnostic tests and treatment
Best regards,
Alice Roberts
Chief Medical Officer

... (rest of the prompt_example as provided) ...

"""

user_input = st.text_area("Input: These are a Student's emails:", height=200)

if st.button("Submit"):
    if user_input:
        # Combine the prompt example with user input
        prompt_input = prompt_example + user_input

        # Create model instance
        model = Model(
            model_id=model_id,
            params=parameters,
            credentials=get_credentials(),
            project_id=project_id,
            space_id=space_id
        )

        st.write("Submitting generation request...")

        # Generate text
        generated_response = model.generate_text(prompt=prompt_input, guardrails=True)

        # Display the response
        st.subheader("Generated Response")
        st.text_area("Response", value=generated_response, height=400)
    else:
        st.error("Please enter the email text in the input area.")

