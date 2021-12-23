from __future__ import print_function
import datetime
import os.path
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from datetime import datetime, timedelta

# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/calendar']


def insert(access_token, refresh_token, summary, descripion, start):
#def main():
    try:
        with open('token.json', 'w') as token:
            token.write(
                """{"token": \"""" + access_token+  """\", "refresh_token": \"""" + refresh_token+"""\", "token_uri": "https://oauth2.googleapis.com/token", "client_id": "565907076275-dfcr2jb40hlgoentonn8avj4ql1mn915.apps.googleusercontent.com", "client_secret": "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", "scopes": ["https://www.googleapis.com/auth/calendar"], "expiry": "2021-12-23T18:50:10.284801Z"}""")

        creds = None
        if os.path.exists('token.json'):
            creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            # else:
            #     flow = InstalledAppFlow.from_client_secrets_file(
            #         'credentials.json', SCOPES)
            #     creds = flow.run_local_server(port=0)
            # Save the credentials for the next run
            with open('token.json', 'w') as token:
                token.write(creds.to_json())

    
        
        service = build('calendar', 'v3', credentials=creds)
        result = service.calendarList().list().execute()
        #print(result['items'])#[0])
        #[print("\n******", x) for x in result['items']]
        for calender in result['items']:
            if "gmail.com" in calender['id']:
                print(calender['id'])
                calendar_id = calender['id']

        #calendar_id = result['items'][0]['id']
        #print(calendar_id)
        """events results"""
        # result = service.events().list(calendarId=calendar_id, timeZone="Asia/Tehran").execute()
        # print(result['items'][0])

        s2 = start.split('_')
        datearr = s2[0].split('-')
        timearr = s2[1].split(':')

        start_time = datetime(int(datearr[0]), int(datearr[1]), int(datearr[2]), int(timearr[0]), int(timearr[1]), 0)
        end_time = start_time + timedelta(hours=1)
        timezone = 'Asia/Tehran'
        event = {
        'summary': summary,
        #'location': 'Tehran',
        'description': descripion,
        'start': {
            'dateTime': start_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': timezone,
        },
        'end': {
            'dateTime': end_time.strftime("%Y-%m-%dT%H:%M:%S"),
            'timeZone': timezone,
        },
        'reminders': {
            'useDefault': False,
            'overrides': [
            #{'method': 'email', 'minutes': 24 * 60},
            # {'method': 'popup', 'minutes': 10},
            ],
        },
        }
        service.events().insert(calendarId=calendar_id, body=event).execute()        


    except HttpError as error:
        print('An error occurred: %s' % error)


# if __name__ == '__main__':
#     #main()
#     insert("ya29.a0ARrdaM8I0H8T_midGeC7234JZKt3MpSjcYxdr6zLug5RwmadLssuIOe2MjVyh7BRSnoFmcglsIhmZkcrQ5ql7ku_ug5k01-PoIdQo0KXigegBj8T6d4Y0-rMspyp3en3lcpHIy6jKYJfTwkf-D1VlHWHPZLz"
#     , "1//03io3X5oViF-FCgYIARAAGAMSNwF-L9Ir0dKF9179O0UPhZwLy9EeyEmijuQVYbF_s1fsMLeaiMk-dMeD3ec4V09Jl5_jFdYOdLQ"
#     , "test1", "This is a test", "2021-12-24_00:45")