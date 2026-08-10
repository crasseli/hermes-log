import time
import requests
from requests.exceptions import RequestException
from typing import Dict, Any, Optional, List

class JulesClient:
    """
    A simple Python SDK for the Jules API.
    """

    BASE_URL = "https://jules.googleapis.com/v1alpha"

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.session = requests.Session()
        self.session.headers.update({
            "X-Goog-Api-Key": self.api_key,
            "Content-Type": "application/json"
        })

    def _normalize_session_id(self, session_id: str) -> str:
        """Helper to ensure session ID format is correct."""
        return session_id if session_id.startswith("sessions/") else f"sessions/{session_id}"

    def create_session(
        self,
        prompt: str,
        source: str,
        branch: str,
        title: Optional[str] = None,
        automation_mode: Optional[bool] = None
    ) -> Dict[str, Any]:
        """
        Creates a new Jules session.
        """
        payload = {
            "prompt": prompt,
            "sourceContext": {
                "source": source,
                "branch": branch
            }
        }
        if title is not None:
            payload["title"] = title
        if automation_mode is not None:
            payload["automationMode"] = automation_mode

        try:
            response = self.session.post(f"{self.BASE_URL}/sessions", json=payload)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            print(f"Error creating session: {e}")
            if e.response is not None:
                print(e.response.text)
            raise

    def get_session(self, session_id: str) -> Dict[str, Any]:
        """
        Gets details for a specific session.
        """
        name = self._normalize_session_id(session_id)
        try:
            response = self.session.get(f"{self.BASE_URL}/{name}")
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            print(f"Error getting session: {e}")
            if e.response is not None:
                print(e.response.text)
            raise

    def list_activities(self, session_id: str) -> Dict[str, Any]:
        """
        Lists activities for a given session.
        """
        name = self._normalize_session_id(session_id)
        try:
            response = self.session.get(f"{self.BASE_URL}/{name}/activities")
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            print(f"Error listing activities: {e}")
            if e.response is not None:
                print(e.response.text)
            raise

    def list_sessions(self) -> Dict[str, Any]:
        """
        Lists all sessions.
        """
        try:
            response = self.session.get(f"{self.BASE_URL}/sessions")
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            print(f"Error listing sessions: {e}")
            if e.response is not None:
                print(e.response.text)
            raise

    def send_message(self, session_id: str, message: str) -> Dict[str, Any]:
        """
        Sends a message to an existing session.
        """
        name = self._normalize_session_id(session_id)
        payload = {"message": message}

        try:
            response = self.session.post(f"{self.BASE_URL}/{name}:sendMessage", json=payload)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            print(f"Error sending message: {e}")
            if e.response is not None:
                print(e.response.text)
            raise

    def wait_for_completion(
        self,
        session_id: str,
        poll_interval: int = 15,
        timeout: int = 1200  # 20 minutes default
    ) -> Dict[str, Any]:
        """
        Polls the session activities until the session finishes or requires user action.
        Stops when state is DONE, FAILED, or USER_TURN.
        """
        start_time = time.time()

        while True:
            activities_resp = self.list_activities(session_id)
            activities = activities_resp.get("activities", [])

            if activities:
                # We assume the last activity is the most recent or we can iterate
                # Usually we just check the latest activity
                latest_activity = activities[-1]
                state = latest_activity.get("state")

                if state in ["DONE", "FAILED", "USER_TURN"]:
                    print(f"Session reached terminal or actionable state: {state}")
                    return activities_resp
            else:
                # If no activities yet, we can also check the session state
                session_resp = self.get_session(session_id)
                session_state = session_resp.get("sessionState", session_resp.get("state"))
                if session_state in ["DONE", "FAILED", "USER_TURN"]:
                    print(f"Session state reached: {session_state}")
                    return session_resp

            if (time.time() - start_time) > timeout:
                raise TimeoutError(f"Polling timed out after {timeout} seconds.")

            print(f"Waiting for session to complete... Sleeping for {poll_interval}s")
            time.sleep(poll_interval)


if __name__ == "__main__":
    import os
    import sys

    # Get API key from environment variable
    api_key = os.getenv("JULES_API_KEY")
    if not api_key:
        print("Please set the JULES_API_KEY environment variable.")
        sys.exit(1)

    client = JulesClient(api_key=api_key)

    # Example: List sessions
    print("--- Listing Sessions ---")
    try:
        sessions = client.list_sessions()
        print(f"Found {len(sessions.get('sessions', []))} sessions.")
    except Exception as e:
        print(f"Failed to list sessions: {e}")

    # To test creating and polling a session, uncomment the following block:
    '''
    print("\n--- Creating a new Session ---")
    session_data = client.create_session(
        prompt="Write a unit test for my python helper",
        source="https://github.com/my-org/my-repo",
        branch="main",
        title="Python Unit Test",
        automation_mode=True
    )

    session_id = session_data.get("name")
    print(f"Session created: {session_id}")

    print("\n--- Waiting for completion ---")
    try:
        final_state = client.wait_for_completion(session_id=session_id)
        print("Final State:")
        import json
        print(json.dumps(final_state, indent=2))
    except Exception as e:
        print(f"Session polling failed: {e}")
    '''
