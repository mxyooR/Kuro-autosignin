import types
import unittest
from configparser import ConfigParser
from datetime import timezone
from typing import Optional
from unittest.mock import MagicMock, patch

import push


class DiscordPushTests(unittest.TestCase):
    def _build_config(
        self, verify_ssl: bool, http_proxy: Optional[str] = None
    ) -> ConfigParser:
        config = ConfigParser()
        config.add_section("discord")
        config.set("discord", "webhook", "https://discord.example/webhook")
        config.set("discord", "verify_ssl", str(verify_ssl).lower())
        if http_proxy:
            config.set("discord", "http_proxy", http_proxy)
        return config

    def _mock_response(self) -> MagicMock:
        response = MagicMock()
        response.status_code = 204
        return response

    @patch.dict("sys.modules", {"pytz": types.SimpleNamespace(timezone=lambda _: timezone.utc)})
    def test_discord_without_proxy_builds_session_with_verify(self):
        session = MagicMock()
        session.post.return_value = self._mock_response()

        with patch.object(push, "cfg", self._build_config(verify_ssl=False)), patch.object(
            push, "get_new_session", return_value=session
        ) as get_new_session, patch.object(
            push, "get_new_session_use_proxy"
        ) as get_new_session_use_proxy:
            push.discord("title", "message")

        get_new_session.assert_called_once_with(verify=False)
        get_new_session_use_proxy.assert_not_called()
        self.assertNotIn("verify", session.post.call_args.kwargs)
        payload = session.post.call_args.kwargs["json"]
        self.assertNotIn("username", payload)
        self.assertNotIn("avatar_url", payload)
        self.assertEqual(payload["embeds"][0]["author"]["name"], "Kuro-autosignin")

    @patch.dict("sys.modules", {"pytz": types.SimpleNamespace(timezone=lambda _: timezone.utc)})
    def test_discord_with_proxy_passes_verify_into_proxy_session(self):
        session = MagicMock()
        session.post.return_value = self._mock_response()

        with patch.object(
            push, "cfg", self._build_config(verify_ssl=False, http_proxy="127.0.0.1:1080")
        ), patch.object(push, "get_new_session") as get_new_session, patch.object(
            push, "get_new_session_use_proxy", return_value=session
        ) as get_new_session_use_proxy:
            push.discord("title", "message")

        get_new_session.assert_not_called()
        get_new_session_use_proxy.assert_called_once_with("127.0.0.1:1080", verify=False)
        self.assertNotIn("verify", session.post.call_args.kwargs)
        payload = session.post.call_args.kwargs["json"]
        self.assertNotIn("username", payload)
        self.assertNotIn("avatar_url", payload)

    @patch.dict("sys.modules", {"pytz": types.SimpleNamespace(timezone=lambda _: timezone.utc)})
    def test_discord_uses_custom_webhook_identity_when_configured(self):
        session = MagicMock()
        session.post.return_value = self._mock_response()
        config = self._build_config(verify_ssl=True)
        config.set("discord", "username", "Custom Bot")
        config.set("discord", "avatar_url", "https://cdn.example/avatar.png")

        with patch.object(push, "cfg", config), patch.object(
            push, "get_new_session", return_value=session
        ):
            push.discord("title", "message")

        payload = session.post.call_args.kwargs["json"]
        self.assertEqual(payload["username"], "Custom Bot")
        self.assertEqual(payload["avatar_url"], "https://cdn.example/avatar.png")


if __name__ == "__main__":
    unittest.main()
