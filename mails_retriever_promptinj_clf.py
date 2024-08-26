import os.path
import time
import base64
import re
import json
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import torch

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def extract_specific_html_content(content):
    """
    Extracts specific HTML content based on a pattern.
    This function targets specific tags in the email content.
    """
    # Define a regex pattern to match the specific HTML content
    pattern = re.compile(r'<p>Dear all,.*?<p>See you there!</p>', re.DOTALL)

    # Search for the pattern in the content
    match = pattern.search(content)
    if match:
        return match.group(0)  # Return the matched HTML content
    return ""

def fetch_emails():
    """Fetches the last 10 emails in the Primary category and saves their content to a JSON file."""
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("gmail", "v1", credentials=creds)
        
        # Calculate the time 1 day ago as Unix timestamp
        one_day_ago = datetime.now() - timedelta(days=1)
        one_day_ago_unix = int(time.mktime(one_day_ago.timetuple()))

        # Query for emails received in the past 1 day in the Primary category and limit to the last 15 emails
        query = f"after:{one_day_ago_unix} category:primary"
        results = service.users().messages().list(userId="me", q=query, maxResults=10).execute()
        messages = results.get("messages", [])

        if not messages:
            print("No emails found.")
            return

        print("Last 10 emails received in the past day in the Primary category:")

        # Initialize an empty list to store all email contents
        k = []
        
        for msg in messages:
            msg_id = msg['id']
            msg = service.users().messages().get(userId="me", id=msg_id, format='full').execute()
            headers = msg['payload']['headers']
            from_header = next(header['value'] for header in headers if header['name'] == 'From')
            subject_header = next(header['value'] for header in headers if header['name'] == 'Subject')
            date_header = datetime.fromtimestamp(int(msg['internalDate']) / 1000).strftime('%Y-%m-%d %H:%M:%S')
            
            print(f"From: {from_header}")
            print(f"Subject: {subject_header}")
            print(f"Date: {date_header}")

            # Initialize variables for plain text and HTML content
            plain_text = ""
            html_content = ""

            # Extract email content
            if 'parts' in msg['payload']:
                for part in msg['payload']['parts']:
                    if part['mimeType'] == 'text/plain':
                        plain_text = part['body']['data']
                    elif part['mimeType'] == 'text/html':
                        html_content = part['body']['data']
            else:
                if msg['payload']['mimeType'] == 'text/plain':
                    plain_text = msg['payload']['body']['data']
                elif msg['payload']['mimeType'] == 'text/html':
                    html_content = msg['payload']['body']['data']

            # Decode and process the plain text content
            if plain_text:
                decoded_plain_text = base64.urlsafe_b64decode(plain_text).decode('utf-8')

                # Remove URLs from the decoded plain text
                decoded_plain_text = re.sub(r'http[s]?://\S+', '', decoded_plain_text)

                # Remove lines containing the word 'Unsubscribe' (case insensitive)
                filtered_plain_text = "\n".join(
                    line for line in decoded_plain_text.splitlines() if not re.search(r'unsubscribe', line, re.IGNORECASE)
                )
            else:
                filtered_plain_text = "No plain text content found."

            # Decode and process the HTML content
            if html_content:
                decoded_html_content = base64.urlsafe_b64decode(html_content).decode('utf-8')

                # Extract specific HTML content
                specific_content = extract_specific_html_content(decoded_html_content)
                if not specific_content:
                    specific_content = "No specific HTML content found."
            else:
                specific_content = "No HTML content found."

            # Append email details as a dictionary to the list `k`
            email_details = {
                "From": from_header,
                "Subject": subject_header,
                "Date": date_header,
                "Plain_Text_Content": filtered_plain_text,
                "HTML_Content": specific_content
            }
            k.append(email_details)

            print("\n" + "-"*50 + "\n")

        # Write the list `k` to a JSON file
        with open("sample_emails.json", "w", encoding="utf-8") as file:
            json.dump(k, file, indent=4)

    except HttpError as error:
        print(f"An error occurred: {error}")

def classify_emails():
    """Classifies emails as safe or unsafe and updates the JSON file accordingly."""
    
    # Load emails from JSON file
    with open("sample_emails.json", "r", encoding="utf-8") as file:
        emails = json.load(file)
    
    # Load the classification model and tokenizer
    tokenizer = AutoTokenizer.from_pretrained("ProtectAI/deberta-v3-base-prompt-injection")
    model = AutoModelForSequenceClassification.from_pretrained("ProtectAI/deberta-v3-base-prompt-injection")
    
    classifier = pipeline(
        "text-classification",
        model=model,
        tokenizer=tokenizer,
        truncation=True,
        max_length=512,
        device=torch.device("cuda" if torch.cuda.is_available() else "cpu"),
    )
    
    # Initialize an empty list for safe emails
    safe_emails = []

    for email in emails:
        email_content = email['Plain_Text_Content']
        # Classify the email content
        result = classifier(email_content)

        # If email is classified as safe, add to safe_emails list
        if result[0]['label'] == 'SAFE':
            safe_emails.append(email)
    
    # Write the safe emails back to the JSON file
    with open("sample_emails.json", "w", encoding="utf-8") as file:
        json.dump(safe_emails, file, indent=4)

    print(f"Updated {len(safe_emails)} safe emails in sample_emails.json")

if __name__ == "__main__":
    fetch_emails()  # Fetch and save emails to JSON
    classify_emails()  # Classify and filter emails, then update JSON files
    