import os
import sys
import json
import subprocess
import tempfile
import logging
import urllib.request
import re
from typing import Dict, Any, Optional, List

logger = logging.getLogger("webcmd.client")
logging.basicConfig(level=logging.INFO)

# Auto-configure Chrome path for Webcmd 0.7.4 if not already set
if not os.environ.get("CLOAKBROWSER_BINARY_PATH"):
    possible_chrome_paths = [
        r"C:\Program Files\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
        r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"
    ]
    for p in possible_chrome_paths:
        if os.path.exists(p):
            os.environ["CLOAKBROWSER_BINARY_PATH"] = p
            logger.info(f"Configured CLOAKBROWSER_BINARY_PATH -> {p}")
            break

class WebcmdClient:
    def __init__(self, profile: Optional[str] = None):
        self.profile = profile
        self.active_sessions: List[str] = []

    def _run_cmd(self, args: List[str], timeout: int = 35) -> Dict[str, Any]:
        cmd = ["webcmd"] + args
        try:
            use_shell = sys.platform == "win32"
            env = os.environ.copy()
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                shell=use_shell,
                env=env
            )
            stdout = result.stdout.strip()
            stderr = result.stderr.strip()

            if result.returncode != 0:
                logger.warning(f"webcmd command returned code {result.returncode}: {cmd[:4]}\nStderr: {stderr[:300]}")
                return {
                    "ok": False,
                    "returncode": result.returncode,
                    "stdout": stdout,
                    "stderr": stderr,
                    "error": stderr or stdout
                }
            return {
                "ok": True,
                "returncode": 0,
                "stdout": stdout,
                "stderr": stderr
            }
        except subprocess.TimeoutExpired:
            logger.error(f"webcmd command timed out after {timeout}s: {cmd[:4]}")
            return {
                "ok": False,
                "returncode": -1,
                "stdout": "",
                "stderr": f"Command timed out after {timeout} seconds",
                "error": "TIMEOUT"
            }
        except Exception as e:
            logger.error(f"webcmd command error: {e}")
            return {
                "ok": False,
                "returncode": -1,
                "stdout": "",
                "stderr": str(e),
                "error": str(e)
            }

    def _direct_fetch(self, url: str, timeout: int = 15) -> Dict[str, Any]:
        """Direct HTTP fetch for local development or loopback mock portals."""
        try:
            req = urllib.request.Request(
                url,
                headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Webcmd/0.7.4"}
            )
            with urllib.request.urlopen(req, timeout=timeout) as response:
                html_content = response.read().decode("utf-8", errors="ignore")
                clean_text = re.sub(r"<script.*?</script>", "", html_content, flags=re.DOTALL | re.IGNORECASE)
                clean_text = re.sub(r"<style.*?</style>", "", clean_text, flags=re.DOTALL | re.IGNORECASE)
                clean_text = re.sub(r"<[^>]+>", " ", clean_text)
                clean_text = re.sub(r"\s+", " ", clean_text).strip()
                
                title_match = re.search(r"<title>(.*?)</title>", html_content, re.IGNORECASE)
                title = title_match.group(1).strip() if title_match else "Opportunity Details"
                
                return {
                    "ok": True,
                    "status": 200,
                    "title": title,
                    "content": clean_text,
                    "url": url,
                    "source": "direct_http_fetch"
                }
        except Exception as err:
            return {
                "ok": False,
                "status": 500,
                "error": f"Direct fetch error: {err}",
                "url": url
            }

    def fetch_url(self, url: str, timeout: int = 25) -> Dict[str, Any]:
        """
        Fetches and extracts clean readability content from a URL
        using official 'webcmd web fetch --url <url> --allow-private true -f json'.
        """
        if "localhost" in url or "127.0.0.1" in url or url.startswith("http://0.0.0.0"):
            return self._direct_fetch(url, timeout=timeout)

        args = ["web", "fetch", "--url", url, "--allow-private", "true", "-f", "json"]
        res = self._run_cmd(args, timeout=timeout)
        if res["ok"] and res["stdout"]:
            try:
                data = json.loads(res["stdout"])
                return {
                    "ok": True,
                    "status": data.get("status", 200),
                    "title": data.get("title", ""),
                    "content": data.get("content", ""),
                    "url": data.get("finalUrl", url),
                    "source": "webcmd_web_fetch",
                    "raw": data
                }
            except json.JSONDecodeError:
                return {
                    "ok": True,
                    "status": 200,
                    "title": "",
                    "content": res["stdout"],
                    "url": url,
                    "source": "webcmd_web_fetch_raw"
                }
        else:
            return self._direct_fetch(url, timeout=timeout)

    def create_session(self) -> Optional[str]:
        """Creates a browser workspace session via 'webcmd session create -f json'."""
        args = []
        if self.profile:
            args.extend(["--profile", self.profile])
        args.extend(["session", "create", "-f", "json"])
        res = self._run_cmd(args, timeout=20)
        if res["ok"] and res["stdout"]:
            try:
                data = json.loads(res["stdout"])
                session_id = data.get("id")
                if session_id:
                    self.active_sessions.append(session_id)
                    logger.info(f"Created Webcmd session: {session_id}")
                    return session_id
            except json.JSONDecodeError:
                pass
        return None

    def close_session(self, session_id: str) -> bool:
        """Closes browser session via 'webcmd session close <session_id>'."""
        args = ["session", "close", session_id]
        res = self._run_cmd(args, timeout=15)
        if session_id in self.active_sessions:
            self.active_sessions.remove(session_id)
        return res["ok"]

    def snapshot(self, session_id: str, mode: str = "act") -> Dict[str, Any]:
        """Takes an accessibility snapshot of current page."""
        args = ["--session", session_id, "browser", "snapshot", "--snapshot-mode", mode]
        res = self._run_cmd(args, timeout=25)
        return {
            "ok": res["ok"],
            "output": res["stdout"] if res["ok"] else res.get("stderr", ""),
            "error": res.get("error")
        }

    def run_script(self, session_id: str, js_code: str, timeout: int = 30, no_diff: bool = True) -> Dict[str, Any]:
        """Runs a Playwright JS script via 'webcmd browser run --file <tmp>'."""
        temp_file = None
        try:
            with tempfile.NamedTemporaryFile(mode="w", suffix=".js", delete=False, encoding="utf-8") as f:
                f.write(js_code)
                temp_file = f.name

            args = ["--session", session_id, "browser", "run", "--file", temp_file, "--timeout", str(timeout)]
            if no_diff:
                args.append("--no-snapshot-diff")

            res = self._run_cmd(args, timeout=timeout + 10)
            if res["ok"]:
                try:
                    data = json.loads(res["stdout"])
                    result_payload = data.get("result", data)
                    return {"ok": True, "data": result_payload, "raw": res["stdout"]}
                except Exception:
                    return {"ok": True, "data": res["stdout"], "raw": res["stdout"]}
            else:
                return {"ok": False, "error": res.get("error", "Browser script execution failed"), "stderr": res.get("stderr")}
        finally:
            if temp_file and os.path.exists(temp_file):
                try:
                    os.remove(temp_file)
                except Exception:
                    pass

    def cleanup(self):
        for s in list(self.active_sessions):
            try:
                self.close_session(s)
            except Exception:
                pass