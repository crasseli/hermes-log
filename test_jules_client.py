import unittest
from unittest.mock import patch, MagicMock
from jules_client import JulesClient

class TestJulesClient(unittest.TestCase):
    def setUp(self):
        self.client = JulesClient(api_key="test_key")

    @patch("requests.Session.post")
    def test_create_session(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {"name": "sessions/123", "prompt": "test"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        res = self.client.create_session(
            prompt="test",
            source="repo",
            branch="main",
            title="My Session",
            automation_mode=True
        )

        mock_post.assert_called_once()
        self.assertEqual(res["name"], "sessions/123")

    @patch("requests.Session.get")
    def test_list_activities(self, mock_get):
        mock_response = MagicMock()
        mock_response.json.return_value = {"activities": [{"state": "DONE"}]}
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response

        res = self.client.list_activities("123")

        mock_get.assert_called_once()
        self.assertEqual(len(res["activities"]), 1)
        self.assertEqual(res["activities"][0]["state"], "DONE")

    @patch("requests.Session.post")
    def test_send_message(self, mock_post):
        mock_response = MagicMock()
        mock_response.json.return_value = {"status": "ok"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response

        res = self.client.send_message("123", "Hello")

        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(kwargs["json"]["message"], "Hello")

    @patch.object(JulesClient, "list_activities")
    def test_wait_for_completion(self, mock_list_activities):
        # Simulate taking a bit of time, first pending, then DONE
        mock_list_activities.side_effect = [
            {"activities": [{"state": "AGENT_TURN"}]},
            {"activities": [{"state": "DONE"}]}
        ]

        with patch("time.sleep", return_value=None):
            res = self.client.wait_for_completion("123", poll_interval=1)
            self.assertEqual(res["activities"][0]["state"], "DONE")
            self.assertEqual(mock_list_activities.call_count, 2)

if __name__ == "__main__":
    unittest.main()
