

# app/data_fetcher.py
import requests
import logging
from typing import List, Dict, Any

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DataFetcher:
    """
    Fetch member messages from API or use mock data if API fails.
    """

    def __init__(self, base_url: str = "https://november7-730026606190.europe-west1.run.app"):
        self.base_url = base_url
        self.messages_endpoint = f"{base_url}/messages/"

    def fetch_all_messages(self) -> List[Dict[str, Any]]:
        try:
            logger.info("Fetching messages from API")
            response = requests.get(self.messages_endpoint, timeout=5)
            response.raise_for_status()
            data = response.json()
            return data.get("items", [])
        except Exception as e:
            logger.warning(f"API fetch failed ({e}), using mock data")
            # fallback mock messages
            return [
                {"user_name": "Layla", "message": "Planning my London trip for June 20th", "timestamp": "2025-06-01", "user_id": "1"},
                {"user_name": "Vikram Desai", "message": "I have 2 cars", "timestamp": "2025-06-02", "user_id": "2"},
                {"user_name": "Amira", "message": "I love Italian and Japanese food", "timestamp": "2025-06-03", "user_id": "3"},
                {"user_name": "Marcus", "message": "I enjoy hiking and swimming", "timestamp": "2025-06-04", "user_id": "4"},
            ]

    def format_messages_for_context(self, messages: List[Dict[str, Any]]) -> str:
        context_parts = []
        for msg in messages:
            context_parts.append(
                f"User: {msg.get('user_name','Unknown')} (ID: {msg.get('user_id','')})\n"
                f"Message: {msg.get('message','')}\n"
                f"Timestamp: {msg.get('timestamp','')}\n---"
            )
        return "\n".join(context_parts)

    def get_message_stats(self, messages: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not messages:
            return {}
        unique_users = {msg.get("user_name","Unknown") for msg in messages}
        return {
            "total_messages": len(messages),
            "unique_users": len(unique_users)
        }
