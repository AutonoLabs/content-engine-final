#!/usr/bin/env python3
"""
Blotato API client wrapper.

Usage:
    from blotato_client import BlotatoClient
    client = BlotatoClient()
    accounts = client.list_accounts()
"""

import os
import requests
from typing import Optional, List, Dict, Any
from dotenv import load_dotenv

load_dotenv()


class BlotatoClient:
    BASE_URL = "https://api.blotato.com/v1"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("BLOTATO_API_KEY")
        if not self.api_key:
            raise ValueError("BLOTATO_API_KEY not found in .env")
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        })

    def _request(self, method: str, endpoint: str, **kwargs) -> Dict[str, Any]:
        url = f"{self.BASE_URL}/{endpoint}"
        response = self.session.request(method, url, **kwargs)
        response.raise_for_status()
        return response.json()

    def list_accounts(self, platform: Optional[str] = None) -> List[Dict[str, Any]]:
        """List connected accounts."""
        params = {"platform": platform} if platform else {}
        result = self._request("GET", "accounts", params=params)
        if isinstance(result, list):
            return result
        return result.get("accounts", []) if isinstance(result, dict) else []

    def get_account(self, account_id: str) -> Dict[str, Any]:
        """Get single account details."""
        result = self._request("GET", f"accounts/{account_id}")
        return result if isinstance(result, dict) else {}

    def create_post(
        self,
        account_id: str,
        platform: str,
        text: str,
        media_urls: Optional[List[str]] = None,
        **platform_kwargs
    ) -> Dict[str, Any]:
        """Create a post (publish immediately)."""
        payload = {
            "accountId": account_id,
            "platform": platform,
            "text": text,
            "mediaUrls": media_urls or [],
            **platform_kwargs
        }
        return self._request("POST", "posts", json=payload)

    def schedule_post(
        self,
        account_id: str,
        platform: str,
        text: str,
        scheduled_time: str,  # ISO 8601
        media_urls: Optional[List[str]] = None,
        **platform_kwargs
    ) -> Dict[str, Any]:
        """Schedule a post for future publishing."""
        payload = {
            "accountId": account_id,
            "platform": platform,
            "text": text,
            "scheduledTime": scheduled_time,
            "mediaUrls": media_urls or [],
            **platform_kwargs
        }
        return self._request("POST", "schedules", json=payload)

    def get_post_status(self, submission_id: str) -> Dict[str, Any]:
        """Get publish status."""
        return self._request("GET", f"posts/{submission_id}/status")

    def list_schedules(self) -> List[Dict[str, Any]]:
        """List all scheduled posts."""
        result = self._request("GET", "schedules")
        if isinstance(result, list):
            return result
        return result.get("schedules", []) if isinstance(result, dict) else []

    def update_schedule(self, schedule_id: str, **updates) -> Dict[str, Any]:
        """Update a scheduled post."""
        return self._request("PATCH", f"schedules/{schedule_id}", json=updates)

    def delete_schedule(self, schedule_id: str) -> Dict[str, Any]:
        """Delete a scheduled post."""
        return self._request("DELETE", f"schedules/{schedule_id}")

    def create_presigned_upload(self, filename: str) -> Dict[str, Any]:
        """Get presigned URL for local file upload."""
        return self._request("POST", "uploads/presigned", json={"filename": filename})


if __name__ == "__main__":
    # Quick CLI test
    client = BlotatoClient()
    accounts = client.list_accounts()
    print(f"Found {len(accounts)} accounts")
    for acc in accounts[:5]:
        print(f"  {acc.get('platform')}: {acc.get('username', acc.get('displayName'))} (id={acc.get('id')})")