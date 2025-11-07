# Claude API Discovery Plan
## Real-time Endpoint Monitoring with Chrome DevTools Protocol

**Goal:** Capture and document all API endpoints for Claude Projects and Claude Code by monitoring network traffic during manual interactions.

---

## 1. SETUP OPTIONS

### Option A: Chrome DevTools Protocol (CDP) Direct
**Best for:** Quick setup, built-in Chrome functionality

**Setup:**
```bash
# Launch Chrome with remote debugging enabled
google-chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=/tmp/chrome-debug \
  https://claude.ai
```

**Monitor with Python:**
```python
# monitor_api.py
import asyncio
from pyppeteer import connect
import json
from datetime import datetime

async def monitor_network():
    browser = await connect(browserURL='http://localhost:9222')
    pages = await browser.pages()
    page = pages[0]

    # Enable network tracking
    await page._client.send('Network.enable')

    # Storage for API calls
    api_calls = []

    async def on_request(request):
        if 'claude.ai/api' in request['request']['url']:
            call = {
                'timestamp': datetime.now().isoformat(),
                'method': request['request']['method'],
                'url': request['request']['url'],
                'headers': request['request'].get('headers', {}),
                'postData': request['request'].get('postData', None)
            }
            api_calls.append(call)
            print(f"\n{'='*60}")
            print(f"📤 {call['method']} {call['url']}")
            if call['postData']:
                print(f"📦 Payload: {call['postData'][:200]}...")

    async def on_response(response):
        if 'claude.ai/api' in response['response']['url']:
            # Get response body
            try:
                body = await page._client.send('Network.getResponseBody', {
                    'requestId': response['requestId']
                })
                print(f"📥 Response: {body.get('body', '')[:200]}...")
            except:
                pass

    page._client.on('Network.requestWillBeSent', on_request)
    page._client.on('Network.responseReceived', on_response)

    print("🔍 Monitoring network traffic...")
    print("Interact with Claude.ai now. Press Ctrl+C to stop and save.\n")

    try:
        await asyncio.sleep(3600)  # Monitor for 1 hour
    except KeyboardInterrupt:
        # Save all captured calls
        with open('api-calls.json', 'w') as f:
            json.dump(api_calls, f, indent=2)
        print(f"\n✓ Saved {len(api_calls)} API calls to api-calls.json")

if __name__ == '__main__':
    asyncio.run(monitor_network())
```

**Install dependencies:**
```bash
pip install pyppeteer pychrome
```

---

### Option B: Chrome DevTools MCP Server
**Best for:** Integration with Claude or other MCP clients

**Check if available:**
```bash
# List available MCP servers
ls ~/.config/claude/mcp-servers/ 2>/dev/null || echo "No MCP servers configured"
```

**If chrome-devtools-mcp is available, it will be listed as `mcp__chrome*` tools.**

---

### Option C: Manual DevTools + Copy as cURL
**Best for:** No coding required, manual process

**Steps:**
1. Open Chrome DevTools (F12)
2. Go to Network tab
3. Filter: `api/`
4. Perform action (create project, etc.)
5. Right-click request → Copy → Copy as cURL
6. Paste into documentation

**Pros:** Simple, no setup
**Cons:** Manual, tedious for many requests

---

## 2. API DISCOVERY WORKFLOW

### Phase 1: Projects API Discovery (30-45 minutes)

#### Scenario 1: Create Project
**Actions to perform:**
1. Navigate to https://claude.ai
2. Click "Projects" (or navigate to projects page)
3. Click "New Project"
4. Fill in:
   - Name: "Test API Discovery"
   - Description: "Testing project creation"
5. Click "Create"

**Expected endpoints:**
- `POST /api/organizations/{org_id}/projects`
- `GET /api/organizations/{org_id}/projects` (list projects)

**Data to capture:**
```json
{
  "request": {
    "method": "POST",
    "url": "...",
    "headers": { ... },
    "payload": {
      "name": "...",
      "description": "...",
      "uuid": "..."
    }
  },
  "response": {
    "status": 201,
    "body": {
      "uuid": "...",
      "name": "...",
      "created_at": "..."
    }
  }
}
```

---

#### Scenario 2: Upload Project File
**Actions to perform:**
1. Open the project created above
2. Click "Add files" or "Upload knowledge"
3. Select a test file (e.g., `test-document.txt`)
4. Wait for upload to complete

**Expected endpoints:**
- `POST /api/organizations/{org_id}/projects/{project_id}/files`
- OR `POST /api/{org_id}/upload` (with project context)
- `GET /api/organizations/{org_id}/projects/{project_id}/files` (list files)

**Data to capture:**
- Multipart form data structure
- File UUID returned
- How file is referenced in project

---

#### Scenario 3: Update Custom Instructions
**Actions to perform:**
1. In the project, find "Custom Instructions" or "Project Settings"
2. Add custom instructions: "You are a helpful assistant focused on API documentation."
3. Save/Update

**Expected endpoints:**
- `PATCH /api/organizations/{org_id}/projects/{project_id}`
- OR `PUT /api/organizations/{org_id}/projects/{project_id}/instructions`

**Data to capture:**
```json
{
  "payload": {
    "custom_instructions": "..."
  }
}
```

---

#### Scenario 4: Create Project Chat
**Actions to perform:**
1. In the project, start a new conversation
2. Note the chat creation (might be automatic)
3. Send a test message: "Hello, this is a test message"

**Expected endpoints:**
- `POST /api/organizations/{org_id}/projects/{project_id}/chat_conversations`
- `POST /api/organizations/{org_id}/projects/{project_id}/chat_conversations/{chat_id}/completion`

**Data to capture:**
- How chat is scoped to project
- If project files are auto-included
- Custom instructions in context

---

#### Scenario 5: List Project Contents
**Actions to perform:**
1. Navigate back to project overview
2. View files list
3. View conversations list

**Expected endpoints:**
- `GET /api/organizations/{org_id}/projects/{project_id}`
- `GET /api/organizations/{org_id}/projects/{project_id}/files`
- `GET /api/organizations/{org_id}/projects/{project_id}/chat_conversations`

---

#### Scenario 6: Delete Project File
**Actions to perform:**
1. In project files, delete the uploaded test file
2. Confirm deletion

**Expected endpoints:**
- `DELETE /api/organizations/{org_id}/projects/{project_id}/files/{file_id}`

---

#### Scenario 7: Delete Project
**Actions to perform:**
1. Go to project settings or project list
2. Delete the test project
3. Confirm deletion

**Expected endpoints:**
- `DELETE /api/organizations/{org_id}/projects/{project_id}`

---

### Phase 2: Claude Code API Discovery (45-60 minutes)

#### Scenario 8: Create Code Workspace
**Actions to perform:**
1. Navigate to https://claude.ai/code
2. Click "New Workspace" or "Connect Repository"
3. Enter GitHub repo: `octocat/Hello-World` (public test repo)
4. Select branch: `main`
5. Select environment (if prompted)
6. Click "Create Workspace"

**Expected endpoints:**
- `POST /api/code/workspaces`
- `GET /api/code/workspaces/{workspace_id}/status`
- WebSocket: `wss://claude.ai/api/code/workspaces/{workspace_id}/stream`

**Data to capture:**
- Workspace creation payload
- Status polling frequency
- WebSocket messages during setup
- When status transitions: pending → initializing → cloning → ready

---

#### Scenario 9: Monitor Workspace Setup Progress
**Actions to perform:**
1. Watch the workspace initialization
2. Note all status messages
3. Capture WebSocket traffic if possible

**Expected WebSocket messages:**
```json
{
  "type": "status_update",
  "status": "cloning_repo",
  "message": "Cloning repository...",
  "progress": 25
}
```

**Data to capture:**
- All status states
- Progress indicators
- Error handling
- Final "ready" message

---

#### Scenario 10: Browse Workspace Files
**Actions to perform:**
1. Once workspace is ready, browse the file tree
2. Expand directories
3. Open a file to view contents

**Expected endpoints:**
- `GET /api/code/workspaces/{workspace_id}/files?path=/`
- `GET /api/code/workspaces/{workspace_id}/files/{file_path}`

**Data to capture:**
- File tree structure
- How files are represented
- File content encoding

---

#### Scenario 11: Send Code Task
**Actions to perform:**
1. In the workspace, send a prompt: "Add a comment to README.md explaining what this repo does"
2. Watch Claude's response and code changes

**Expected endpoints:**
- `POST /api/code/workspaces/{workspace_id}/messages`
- OR `POST /api/code/workspaces/{workspace_id}/completion`
- Possibly streaming: `text/event-stream`

**Data to capture:**
- Message payload structure
- How file context is included
- Response streaming format
- Code diff format

---

#### Scenario 12: Execute Code
**Actions to perform:**
1. If there's a "Run" or "Execute" button, click it
2. OR use terminal if available
3. Run a simple command like `ls` or `cat README.md`

**Expected endpoints:**
- `POST /api/code/workspaces/{workspace_id}/execute`
- `GET /api/code/workspaces/{workspace_id}/terminal/{session_id}`

**Data to capture:**
- Command execution payload
- stdout/stderr response
- Exit codes
- Streaming output

---

#### Scenario 13: Edit File Directly
**Actions to perform:**
1. Click "Edit" on a file
2. Make a change (add a line)
3. Save the file

**Expected endpoints:**
- `PUT /api/code/workspaces/{workspace_id}/files/{file_path}`
- OR `PATCH /api/code/workspaces/{workspace_id}/files/{file_path}`

**Data to capture:**
- Update payload (full content vs. diff)
- Response confirmation
- File versioning

---

#### Scenario 14: View Workspace Sessions/Chats
**Actions to perform:**
1. Navigate to workspace chat history
2. View previous conversations
3. Start a new session/chat within workspace

**Expected endpoints:**
- `GET /api/code/workspaces/{workspace_id}/sessions`
- `POST /api/code/workspaces/{workspace_id}/sessions`

---

#### Scenario 15: Terminate Workspace
**Actions to perform:**
1. Go to workspace settings or list
2. Click "Terminate" or "Delete"
3. Confirm deletion

**Expected endpoints:**
- `DELETE /api/code/workspaces/{workspace_id}`
- OR `POST /api/code/workspaces/{workspace_id}/terminate`

**Data to capture:**
- Termination process
- Cleanup confirmation
- If data is preserved

---

## 3. MONITORING COMMANDS

### Start Monitoring Session

**Terminal 1: Launch Chrome with debugging**
```bash
# Close all Chrome instances first
pkill chrome

# Launch with remote debugging
google-chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=/tmp/chrome-debug-claude \
  --auto-open-devtools-for-tabs \
  https://claude.ai

# Login to your Claude account before starting capture
```

**Terminal 2: Run monitoring script**
```bash
# Start the Python monitor
python3 monitor_api.py

# Output will show real-time API calls
```

**Terminal 3: Optional - WebSocket monitor**
```bash
# Monitor WebSocket traffic separately
npm install -g wscat

# Connect to workspace WebSocket (get URL from captured traffic)
wscat -c "wss://claude.ai/api/code/workspaces/{workspace_id}/stream" \
  -H "Cookie: <your-session-cookie>"
```

---

## 4. DATA CAPTURE TEMPLATE

For each API call, document:

```markdown
### Endpoint: Create Project

**Request:**
- Method: `POST`
- URL: `/api/organizations/{org_id}/projects`
- Headers:
  ```json
  {
    "Content-Type": "application/json",
    "Cookie": "sessionKey=...",
    "User-Agent": "...",
    ...
  }
  ```
- Payload:
  ```json
  {
    "name": "Test API Discovery",
    "description": "Testing project creation",
    "uuid": "a1b2c3d4-...",
    "custom_instructions": ""
  }
  ```

**Response:**
- Status: `201 Created`
- Body:
  ```json
  {
    "uuid": "a1b2c3d4-...",
    "name": "Test API Discovery",
    "description": "Testing project creation",
    "created_at": "2025-11-07T12:34:56.789Z",
    "updated_at": "2025-11-07T12:34:56.789Z",
    "organization_id": "org-123",
    "file_ids": [],
    "chat_conversation_ids": []
  }
  ```

**Notes:**
- UUID is client-generated (same pattern as chat creation)
- Response includes empty file_ids and chat_conversation_ids arrays
- Organization ID is embedded in URL and response
```

---

## 5. DOCUMENTATION OUTPUT

### Create these files:

1. **`api-endpoints-projects.md`**
   - All Projects-related endpoints
   - Request/response examples
   - Error cases

2. **`api-endpoints-code.md`**
   - All Code workspace endpoints
   - WebSocket message formats
   - Streaming responses

3. **`api-calls-raw.json`**
   - Raw captured data
   - Full headers and payloads
   - For reference

4. **`websocket-messages.json`**
   - All WebSocket message types
   - Status updates
   - Code execution streams

---

## 6. REAL-TIME MONITORING WORKFLOW

### Step-by-Step Process:

**Preparation (5 min):**
1. Close all Chrome instances
2. Launch Chrome with debugging on port 9222
3. Login to claude.ai
4. Start Python monitoring script
5. Open API documentation template

**Projects Discovery (30 min):**
1. ✅ Create project → Capture
2. ✅ Upload file → Capture
3. ✅ Update instructions → Capture
4. ✅ Create chat → Capture
5. ✅ Send message → Capture
6. ✅ List project contents → Capture
7. ✅ Delete file → Capture
8. ✅ Delete project → Capture

**Code Discovery (45 min):**
1. ✅ Create workspace → Capture
2. ✅ Monitor setup progress → Capture WebSocket
3. ✅ Browse files → Capture
4. ✅ Send code task → Capture
5. ✅ Execute command → Capture
6. ✅ Edit file → Capture
7. ✅ View sessions → Capture
8. ✅ Terminate workspace → Capture

**Documentation (30 min):**
1. Review all captured calls
2. Fill in endpoint documentation
3. Note any surprises or unknowns
4. Create implementation notes

---

## 7. TROUBLESHOOTING

### Issue: Chrome won't connect to debugger
**Solution:**
```bash
# Kill all Chrome processes
pkill -9 chrome
# Remove lock files
rm -rf /tmp/chrome-debug-claude
# Try again
```

### Issue: WebSocket messages not captured
**Solution:**
- Use browser DevTools WS tab
- Or use browser extension like "WebSocket Monitor"
- Chrome DevTools → Network → WS filter

### Issue: Can't see request payloads
**Solution:**
```javascript
// Inject into page console to log all fetch calls
(function() {
  const originalFetch = window.fetch;
  window.fetch = function(...args) {
    console.log('🔵 FETCH:', args[0], args[1]);
    return originalFetch.apply(this, args);
  };
})();
```

### Issue: Responses are compressed
**Solution:**
- Chrome DevTools automatically decompresses
- Python script should handle with zlib
- Check `Content-Encoding` header

---

## 8. EXPECTED TIMELINE

| Phase | Duration | Output |
|-------|----------|--------|
| Setup monitoring | 10 min | Chrome + Python running |
| Projects discovery | 30 min | 8-10 endpoints documented |
| Code discovery | 45 min | 10-12 endpoints documented |
| WebSocket capture | 15 min | Message formats documented |
| Documentation | 30 min | Complete API reference |
| **TOTAL** | **2.5 hours** | **Full API specification** |

---

## 9. SUCCESS CRITERIA

By the end, you should have:

- ✅ Complete endpoint list for Projects
- ✅ Complete endpoint list for Code
- ✅ Request/response examples for each
- ✅ WebSocket message formats
- ✅ Error response patterns
- ✅ Authentication/header requirements
- ✅ Rate limiting behavior
- ✅ File upload mechanisms
- ✅ Streaming response formats

---

## 10. NEXT STEPS AFTER DISCOVERY

Once we have the API documentation:

1. **Validate findings** (30 min)
   - Test captured cURL commands
   - Verify responses match expectations

2. **Update implementation plan** (1 hour)
   - Adjust `ClaudeProjectClient` design
   - Adjust `ClaudeCodeClient` design
   - Update time estimates

3. **Start implementation** (Week 1-2)
   - Code Projects extension
   - Write tests
   - Document usage

4. **Continue with Code** (Week 3-4)
   - Code workspace extension
   - WebSocket integration
   - Testing

---

## READY TO START?

When you're ready to begin:

1. I'll help you set up the monitoring (choose Option A, B, or C)
2. You perform the actions on claude.ai
3. I'll help document the captured API calls in real-time
4. We'll create the complete API specification together

**Which monitoring option do you prefer?**
- **Option A:** Python script with CDP (most automated)
- **Option B:** MCP chrome-devtools server (if available)
- **Option C:** Manual DevTools + copy/paste (simplest)

Let me know and we'll get started! 🚀
