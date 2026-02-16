import os
import datetime
from langchain.tools import Tool
from youtube_search import YoutubeSearch
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# --- Tool 1: YouTube Search (Free, no API key needed) ---
def search_youtube(query: str) -> str:
    """Searches YouTube for videos related to the study topic."""
    try:
        results = YoutubeSearch(query, max_results=3).to_dict()
        response = "Here are some relevant videos:\n"
        for video in results:
            link = f"https://www.youtube.com/watch?v={video['id']}"
            response += f"- [{video['title']}]({link}) (Channel: {video['channel']})\n"
        return response
    except Exception as e:
        return f"Error searching YouTube: {e}"

# --- Tool 2: Google Calendar (Real + Mock Fallback) ---
SCOPES = ['https://www.googleapis.com/auth/calendar']

class CalendarManager:
    def __init__(self):
        self.service = None
        self.authenticate()

    def authenticate(self):
        """Attempts to authenticate with Google Calendar."""
        creds = None
        # Check if token.json exists (saved session)
        if os.path.exists('token.json'):
            try:
                creds = Credentials.from_authorized_user_file('token.json', SCOPES)
            except:
                pass
        
        # If no valid creds, let user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except:
                    creds = None
            
            # Only run interactive login if credentials.json exists
            if not creds and os.path.exists('credentials.json'):
                try:
                    flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
                    creds = flow.run_local_server(port=0)
                    # Save the credentials for the next run
                    with open('token.json', 'w') as token:
                        token.write(creds.to_json())
                except Exception as e:
                    print(f"Calendar Auth Failed: {e}")

        if creds:
            self.service = build('calendar', 'v3', credentials=creds)

    def schedule_event(self, event_details: str) -> str:
        """
        Parses string to schedule event. 
        Format expected: "Title | YYYY-MM-DDTHH:MM:SS | Duration_Minutes"
        Example: "Study Python | 2025-10-20T14:00:00 | 60"
        """
        if not self.service:
            return "[Mock Mode] Calendar event created: " + event_details + " (Real API unavailable - missing credentials.json)"

        try:
            parts = [p.strip() for p in event_details.split('|')]
            if len(parts) < 3:
                return "Error: Invalid format. Use 'Title | ISO_Date | Duration_Minutes'"
            
            summary, start_str, duration = parts
            start_time = datetime.datetime.fromisoformat(start_str)
            end_time = start_time + datetime.timedelta(minutes=int(duration))

            event = {
                'summary': summary,
                'start': {'dateTime': start_time.isoformat(), 'timeZone': 'UTC'},
                'end': {'dateTime': end_time.isoformat(), 'timeZone': 'UTC'},
            }

            event_result = self.service.events().insert(calendarId='primary', body=event).execute()
            return f"Event created: {event_result.get('htmlLink')}"
        except Exception as e:
            return f"Failed to create event: {e}"

# Instantiate the manager
calendar_manager = CalendarManager()

# Define LangChain Tools
def get_tools():
    return [
        Tool(
            name="YouTube_Search",
            func=search_youtube,
            description="Useful for finding video tutorials and lectures. Input should be a search topic."
        ),
        Tool(
            name="Schedule_Study_Session",
            func=calendar_manager.schedule_event,
            description="Schedules a study session on the calendar. Input MUST be in format: 'Topic | YYYY-MM-DDTHH:MM:SS | Duration(mins)'. Example: 'Math Review | 2023-12-01T10:00:00 | 60'"
        )
    ]