import os.path
import time
import base64
import re  # Import the regex module
from datetime import datetime, timedelta
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

def main():
    """Shows basic usage of the Gmail API.
    Retrieves the user's plain text emails from the past day in the Primary category and saves their content to a text file,
    excluding URLs and lines containing the word 'Unsubscribe'.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "client_secret.json", SCOPES
            )
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        # Call the Gmail API
        service = build("gmail", "v1", credentials=creds)
        
        # Calculate the time 1 day ago as Unix timestamp
        one_day_ago = datetime.now() - timedelta(days=1)
        one_day_ago_unix = int(time.mktime(one_day_ago.timetuple()))

        # Query for emails received in the past 1 day in the Primary category
        query = f"after:{one_day_ago_unix} category:primary"
        results = service.users().messages().list(userId="me", q=query).execute()
        messages = results.get("messages", [])

        if not messages:
            print("No emails found.")
            return

        print("Plain text emails received in the past day in the Primary category:")
        
        # Open the file to write email content
        with open("sample_emails.txt", "w", encoding="utf-8") as file:
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

                # Write email headers to file
                file.write(f"From: {from_header}\n")
                file.write(f"Subject: {subject_header}\n")
                file.write(f"Date: {date_header}\n")

                # Extract plain text email content
                plain_text = ""
                if 'parts' in msg['payload']:
                    for part in msg['payload']['parts']:
                        if part['mimeType'] == 'text/plain':
                            plain_text = part['body']['data']
                            break  # Stop after finding the plain text part
                else:
                    if msg['payload']['mimeType'] == 'text/plain':
                        plain_text = msg['payload']['body']['data']

                # Decode the plain text content
                if plain_text:
                    decoded_plain_text = base64.urlsafe_b64decode(plain_text).decode('utf-8')

                    # Remove URLs from the decoded plain text
                    decoded_plain_text = re.sub(r'http[s]?://\S+', '', decoded_plain_text)

                    # Remove lines containing the word 'Unsubscribe' (case insensitive)
                    filtered_content = "\n".join(
                        line for line in decoded_plain_text.splitlines() if not re.search(r'unsubscribe', line, re.IGNORECASE)
                    )

                    # Write the filtered plain text content to file
                    print("Content:")
                    print(filtered_content)
                    file.write(f"Content:\n{filtered_content}\n")
                else:
                    print("No plain text content found.")
                    file.write("No plain text content found.\n")
                
                # Separate each email with a line
                file.write("\n" + "-"*50 + "\n")
                print("\n" + "-"*50 + "\n")

    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    main()



# MIAN MAIN WORKING 
# import os.path
# import time
# import base64
# from datetime import datetime, timedelta
# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError

# # If modifying these scopes, delete the file token.json.
# SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

# def main():
#     """Shows basic usage of the Gmail API.
#     Retrieves the user's plain text emails from the past day in the Primary category and saves their content to a text file.
#     """
#     creds = None
#     # The file token.json stores the user's access and refresh tokens, and is
#     # created automatically when the authorization flow completes for the first
#     # time.
#     if os.path.exists("token.json"):
#         creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
#     # If there are no (valid) credentials available, let the user log in.
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file(
#                 "client_secret.json", SCOPES
#             )
#             creds = flow.run_local_server(port=0)
#         # Save the credentials for the next run
#         with open("token.json", "w") as token:
#             token.write(creds.to_json())

#     try:
#         # Call the Gmail API
#         service = build("gmail", "v1", credentials=creds)
        
#         # Calculate the time 1 day ago as Unix timestamp
#         one_day_ago = datetime.now() - timedelta(days=1)
#         one_day_ago_unix = int(time.mktime(one_day_ago.timetuple()))

#         # Query for emails received in the past 1 day in the Primary category
#         query = f"after:{one_day_ago_unix} category:primary"
#         results = service.users().messages().list(userId="me", q=query).execute()
#         messages = results.get("messages", [])

#         if not messages:
#             print("No emails found.")
#             return

#         print("Plain text emails received in the past day in the Primary category:")
        
#         # Open the file to write email content
#         with open("sample_emails.txt", "w", encoding="utf-8") as file:
#             for msg in messages:
#                 msg_id = msg['id']
#                 msg = service.users().messages().get(userId="me", id=msg_id, format='full').execute()
#                 headers = msg['payload']['headers']
#                 from_header = next(header['value'] for header in headers if header['name'] == 'From')
#                 subject_header = next(header['value'] for header in headers if header['name'] == 'Subject')
#                 date_header = datetime.fromtimestamp(int(msg['internalDate']) / 1000).strftime('%Y-%m-%d %H:%M:%S')
                
#                 print(f"From: {from_header}")
#                 print(f"Subject: {subject_header}")
#                 print(f"Date: {date_header}")

#                 # Write email headers to file
#                 file.write(f"From: {from_header}\n")
#                 file.write(f"Subject: {subject_header}\n")
#                 file.write(f"Date: {date_header}\n")

#                 # Extract plain text email content
#                 plain_text = ""
#                 if 'parts' in msg['payload']:
#                     for part in msg['payload']['parts']:
#                         if part['mimeType'] == 'text/plain':
#                             plain_text = part['body']['data']
#                             break  # Stop after finding the plain text part
#                 else:
#                     if msg['payload']['mimeType'] == 'text/plain':
#                         plain_text = msg['payload']['body']['data']

#                 # Decode and write the plain text content to file
#                 if plain_text:
#                     decoded_plain_text = base64.urlsafe_b64decode(plain_text).decode('utf-8')
#                     print("Content:")
#                     print(decoded_plain_text)
#                     file.write(f"Content:\n{decoded_plain_text}\n")
#                 else:
#                     print("No plain text content found.")
#                     file.write("No plain text content found.\n")
                
#                 # Separate each email with a line
#                 file.write("\n" + "-"*50 + "\n")
#                 print("\n" + "-"*50 + "\n")

#     except HttpError as error:
#         print(f"An error occurred: {error}")

# if __name__ == "__main__":
#     main()