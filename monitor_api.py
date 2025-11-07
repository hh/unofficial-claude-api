#!/usr/bin/env python3
"""
Real-time Claude API Monitor
Captures all API calls to claude.ai during manual interactions

Usage:
    1. Launch Chrome with: chrome --remote-debugging-port=9222
    2. Login to claude.ai
    3. Run: python3 monitor_api.py
    4. Perform actions on claude.ai
    5. Press Ctrl+C to save captured calls
"""

import asyncio
import json
from datetime import datetime
from typing import List, Dict
import sys

try:
    from pyppeteer import connect
except ImportError:
    print("⚠️  pyppeteer not installed. Installing...")
    import subprocess
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyppeteer"])
    from pyppeteer import connect


class APIMonitor:
    def __init__(self):
        self.api_calls: List[Dict] = []
        self.ws_messages: List[Dict] = []
        self.browser = None
        self.page = None

    async def connect_to_browser(self):
        """Connect to Chrome debugging session"""
        print("🔌 Connecting to Chrome on port 9222...")
        try:
            self.browser = await connect(
                browserURL='http://localhost:9222',
                slowMo=0
            )
            pages = await self.browser.pages()
            if not pages:
                print("❌ No pages found. Open claude.ai in Chrome first.")
                sys.exit(1)

            # Use the first page (or find claude.ai tab)
            self.page = pages[0]
            for p in pages:
                url = p.url
                if 'claude.ai' in url:
                    self.page = p
                    break

            print(f"✓ Connected to: {self.page.url}")
            return True
        except Exception as e:
            print(f"❌ Failed to connect: {e}")
            print("\nMake sure Chrome is running with:")
            print("  google-chrome --remote-debugging-port=9222")
            return False

    async def setup_network_monitoring(self):
        """Enable network request/response monitoring"""
        print("📡 Enabling network monitoring...\n")

        await self.page._client.send('Network.enable')

        # Monitor requests
        async def on_request(request):
            url = request['request']['url']

            # Only capture Claude API calls
            if 'claude.ai/api' not in url and 'anthropic.com/api' not in url:
                return

            call = {
                'timestamp': datetime.now().isoformat(),
                'type': 'request',
                'method': request['request']['method'],
                'url': url,
                'headers': request['request'].get('headers', {}),
                'postData': request['request'].get('postData', None),
                'requestId': request['requestId']
            }

            self.api_calls.append(call)

            # Print in real-time
            print("━" * 80)
            print(f"📤 {call['method']} {self._shorten_url(url)}")
            print(f"⏰ {call['timestamp']}")

            if call['postData']:
                try:
                    # Try to parse and pretty-print JSON
                    payload = json.loads(call['postData'])
                    print(f"📦 Payload:")
                    print(json.dumps(payload, indent=2)[:500])
                    if len(json.dumps(payload)) > 500:
                        print("    ...")
                except:
                    # Not JSON or too complex
                    print(f"📦 Payload: {call['postData'][:200]}")

        # Monitor responses
        async def on_response(response):
            url = response['response']['url']

            if 'claude.ai/api' not in url and 'anthropic.com/api' not in url:
                return

            request_id = response['requestId']
            status = response['response']['status']

            print(f"📥 Response: {status}")

            # Try to get response body
            try:
                body_data = await self.page._client.send('Network.getResponseBody', {
                    'requestId': request_id
                })
                body = body_data.get('body', '')

                # Update the corresponding request with response
                for call in self.api_calls:
                    if call.get('requestId') == request_id:
                        call['response'] = {
                            'status': status,
                            'headers': response['response'].get('headers', {}),
                            'body': body
                        }

                        # Print response preview
                        try:
                            resp_json = json.loads(body)
                            print("💾 Response body:")
                            print(json.dumps(resp_json, indent=2)[:500])
                            if len(body) > 500:
                                print("    ...")
                        except:
                            print(f"💾 Response: {body[:200]}")
                        break

            except Exception as e:
                # Some responses can't be retrieved (streaming, etc.)
                pass

            print()  # Blank line for readability

        # Monitor WebSocket frames
        async def on_ws_frame_sent(frame):
            if 'claude.ai' in frame.get('response', {}).get('url', ''):
                msg = {
                    'timestamp': datetime.now().isoformat(),
                    'type': 'ws_sent',
                    'payload': frame.get('response', {}).get('payloadData', '')
                }
                self.ws_messages.append(msg)
                print(f"🔵 WebSocket SENT: {msg['payload'][:100]}")

        async def on_ws_frame_received(frame):
            if 'claude.ai' in frame.get('response', {}).get('url', ''):
                msg = {
                    'timestamp': datetime.now().isoformat(),
                    'type': 'ws_received',
                    'payload': frame.get('response', {}).get('payloadData', '')
                }
                self.ws_messages.append(msg)
                print(f"🟢 WebSocket RECV: {msg['payload'][:100]}")

        # Attach listeners
        self.page._client.on('Network.requestWillBeSent', on_request)
        self.page._client.on('Network.responseReceived', on_response)
        # WebSocket monitoring (may not work on all setups)
        try:
            self.page._client.on('Network.webSocketFrameSent', on_ws_frame_sent)
            self.page._client.on('Network.webSocketFrameReceived', on_ws_frame_received)
        except:
            pass

    def _shorten_url(self, url: str) -> str:
        """Shorten URL for display"""
        if len(url) > 80:
            # Show just the path
            try:
                from urllib.parse import urlparse
                parsed = urlparse(url)
                return parsed.path + ('?' + parsed.query if parsed.query else '')
            except:
                return url[:80] + "..."
        return url

    async def monitor(self, duration_seconds: int = 3600):
        """Monitor for specified duration"""
        print("🔍 Monitoring Claude API calls...")
        print("=" * 80)
        print("READY! Interact with claude.ai now.")
        print("Press Ctrl+C when done to save captured data.")
        print("=" * 80)
        print()

        try:
            await asyncio.sleep(duration_seconds)
        except KeyboardInterrupt:
            print("\n\n⏹️  Stopping monitor...")

    def save_results(self):
        """Save captured API calls to files"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        # Save API calls
        api_file = f'api-calls-{timestamp}.json'
        with open(api_file, 'w') as f:
            json.dump(self.api_calls, f, indent=2)
        print(f"\n✓ Saved {len(self.api_calls)} API calls to: {api_file}")

        # Save WebSocket messages if any
        if self.ws_messages:
            ws_file = f'websocket-messages-{timestamp}.json'
            with open(ws_file, 'w') as f:
                json.dump(self.ws_messages, f, indent=2)
            print(f"✓ Saved {len(self.ws_messages)} WebSocket messages to: {ws_file}")

        # Create summary
        self._print_summary()

    def _print_summary(self):
        """Print summary of captured calls"""
        print("\n" + "=" * 80)
        print("SUMMARY")
        print("=" * 80)

        # Count by endpoint
        endpoints = {}
        for call in self.api_calls:
            method = call['method']
            url = call['url']
            # Extract endpoint pattern
            try:
                from urllib.parse import urlparse
                path = urlparse(url).path
                key = f"{method} {path}"
                endpoints[key] = endpoints.get(key, 0) + 1
            except:
                pass

        print(f"\nTotal API calls: {len(self.api_calls)}")
        print(f"Unique endpoints: {len(endpoints)}")
        print("\nEndpoint breakdown:")
        for endpoint, count in sorted(endpoints.items()):
            print(f"  {count:3d}x  {endpoint}")

        if self.ws_messages:
            print(f"\nWebSocket messages: {len(self.ws_messages)}")


async def main():
    monitor = APIMonitor()

    if not await monitor.connect_to_browser():
        sys.exit(1)

    await monitor.setup_network_monitoring()
    await monitor.monitor()
    monitor.save_results()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
