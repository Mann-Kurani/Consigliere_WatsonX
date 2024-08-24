# MAIN WORKING CODE 2
import os.path
import time
import base64  # Import the base64 module
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
    Retrieves the user's plain text emails from the past day in the Primary category and prints their content.
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
        for msg in messages:
            msg_id = msg['id']
            msg = service.users().messages().get(userId="me", id=msg_id, format='full').execute()
            headers = msg['payload']['headers']
            from_header = next(header['value'] for header in headers if header['name'] == 'From')
            subject_header = next(header['value'] for header in headers if header['name'] == 'Subject')
            print(f"From: {from_header}")
            print(f"Subject: {subject_header}")
            # Convert internalDate to readable date format
            date_header = datetime.fromtimestamp(int(msg['internalDate']) / 1000).strftime('%Y-%m-%d %H:%M:%S')
            print(f"Date: {date_header}")

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

            # Decode and print the plain text content
            if plain_text:
                decoded_plain_text = base64.urlsafe_b64decode(plain_text).decode('utf-8')
                print("Content:")
                print(decoded_plain_text)
            else:
                print("No plain text content found.")
            print("\n" + "-"*50 + "\n")

    except HttpError as error:
        print(f"An error occurred: {error}")

if __name__ == "__main__":
    main()













# BEST WORKING CODE 
# import os.path
# import time
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
#     Retrieves the user's emails from the past week.
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
        
#         # Calculate the time 7 days ago as Unix timestamp
#         one_day_ago = datetime.now() - timedelta(days=1)
#         one_day_ago_unix = int(time.mktime(one_day_ago.timetuple()))

#         # Query for emails received in the past 1 day using Unix timestamp
#         results = service.users().messages().list(userId="me", q=f"after:{one_day_ago_unix}").execute()
#         messages = results.get("messages", [])

#         if not messages:
#             print("No emails found.")
#             return

#         print("Emails received in the past day:")
#         for msg in messages:
#             msg_id = msg['id']
#             msg = service.users().messages().get(userId="me", id=msg_id).execute()
#             headers = msg['payload']['headers']
#             from_header = next(header['value'] for header in headers if header['name'] == 'From')
#             subject_header = next(header['value'] for header in headers if header['name'] == 'Subject')
#             print(f"From: {from_header}")
#             print(f"Subject: {subject_header}")
#             # Convert internalDate to readable date format
#             date_header = datetime.fromtimestamp(int(msg['internalDate']) / 1000).strftime('%Y-%m-%d %H:%M:%S')
#             print(f"Date: {date_header}")
#             print()

#     except HttpError as error:
#         print(f"An error occurred: {error}")

# if __name__ == "__main__":
#     main()



# PAST WORKING KINDA

# import os.path

# from google.auth.transport.requests import Request
# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from googleapiclient.discovery import build
# from googleapiclient.errors import HttpError

# # If modifying these scopes, delete the file token.json.
# SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]


# def main():
#   """Shows basic usage of the Gmail API.
#   Lists the user's Gmail labels.
#   """
#   creds = None
#   # The file token.json stores the user's access and refresh tokens, and is
#   # created automatically when the authorization flow completes for the first
#   # time.
#   if os.path.exists("token.json"):
#     creds = Credentials.from_authorized_user_file("gmail_token.json", SCOPES)
#   # If there are no (valid) credentials available, let the user log in.
#   if not creds or not creds.valid:
#     if creds and creds.expired and creds.refresh_token:
#       creds.refresh(Request())
#     else:
#       flow = InstalledAppFlow.from_client_secrets_file(
#           "client_secret.json", SCOPES
#       )
#       creds = flow.run_local_server(port=0)
#     # Save the credentials for the next run
#     with open("token.json", "w") as token:
#       token.write(creds.to_json())

#   try:
#     # Call the Gmail API
#     service = build("gmail", "v1", credentials=creds)
#     results = service.users().labels().list(userId="me").execute()
#     labels = results.get("labels", [])

#     if not labels:
#       print("No labels found.")
#       return
#     print("Labels:")
#     for label in labels:
#       print(label["name"])

#   except HttpError as error:
#     # TODO(developer) - Handle errors from gmail API.
#     print(f"An error occurred: {error}")


# if __name__ == "__main__":
#   main()



