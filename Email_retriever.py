from simplegmail import Gmail
from simplegmail.query import construct_query
from datetime import datetime, timedelta

# Initialize Gmail client
gmail = Gmail()

# Calculate the date and time for 24 hours ago
yesterday = datetime.now() - timedelta(days=1)

# Define query parameters for emails received in the last 24 hours
query_params = {
    "newer_than": (1, "day")
      # Query for emails newer than 1 day
}

# # Fetch messages from the inbox received in the last 24 hours
messages = gmail.get_unread_messages(query=construct_query(query_params))

# # Iterate over each message and print details
# for message in messages:
#     print("From: " + message.sender)
#     print("Subject: " + message.subject)
#     print("Date: " + message.date)
#     print("Preview: " + message.snippet)
    
#     # Save the email body to a file if it's in plain text format
#     with open("sample_emails.txt", "a") as f:
#         if message.plain:
#             f.write("From: " + message.sender + "\n" )
#             f.write("Subject: " + message.subject + "\n")
#             f.write("Date: " + message.date + "\n")
#             f.write("Preview: " + message.snippet + "\n")
#             f.write("Content: " + message.plain + "\n\n")



# from simplegmail im
# from simplegmail.query import construct_query

# gmail = Gmail()


# # Calculate the date and time for 24 hours ago
# yesterday = datetime.now() - timedelta(days=1)

# # Define query parameters for emails received in the last 24 hours
# query_params = {
#     "newer_than": (1, "day")  # Query for emails newer than 1 day
# }

# messages = gmail.get_sent_messages(query=construct_query(query_params))

# for message in messages:
#     print("To: " + message.recipient)
#     print("From: " + message.sender)
#     print("Subject: " + message.subject)
#     print("Date: " + message.date)
#     print("Preview: " + message.snippet)
    
#     with open("email_samples.txt", "a") as f:
#         if message.plain:
#             if len(message.plain) < 1000:
#                 f.write(message.plain)




























# from google.oauth2.credentials import Credentials
# from google_auth_oauthlib.flow import InstalledAppFlow
# from google.auth.transport.requests import Request
# from googleapiclient.discovery import build
# import os
# import datetime

# # If modifying these SCOPES, delete the file token.json.
# SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

# def get_service():
#     creds = None
#     # Load credentials from token.json if it exists
#     if os.path.exists('token.json'):
#         creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    
#     # If credentials are not available or are invalid, perform login flow
#     if not creds or not creds.valid:
#         if creds and creds.expired and creds.refresh_token:
#             creds.refresh(Request())
#         else:
#             flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
#             creds = flow.run_local_server(port=0)
#         # Save the credentials for the next run
#         with open('token.json', 'w') as token:
#             token.write(creds.to_json())

#     try:
#         service = build('gmail', 'v1', credentials=creds)
#     except Exception as e:
#         print(f"Error initializing Gmail API service: {e}")
#         service = None

#     return service

# def get_emails(service):
#     today = datetime.date.today().isoformat()
#     query = f"after:{today}"
    
#     try:
#         # Fetch messages with query
#         results = service.users().messages().list(userId='me', q=query).execute()
#         messages = results.get('messages', [])
#     except Exception as e:
#         print(f"Error fetching emails: {e}")
#         return
    
#     if not messages:
#         print('No emails found.')
#     else:
#         print('Emails found:')
#         for message in messages:
#             # Fetch additional details for each email
#             try:
#                 msg = service.users().messages().get(userId='me', id=message['id']).execute()
#                 print(f"ID: {message['id']} - Snippet: {msg['snippet']}")
#             except Exception as e:
#                 print(f"Error fetching details for email ID {message['id']}: {e}")

# def main():
#     service = get_service()
#     if service:
#         get_emails(service)

# if __name__ == '__main__':
#     main()