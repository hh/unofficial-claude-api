# Quick Start: API Discovery Session

**Goal:** Capture all Claude Projects and Code API endpoints in 2-3 hours

---

## Prerequisites

- Chrome browser installed
- Python 3.10+ installed
- Active Claude.ai account (logged in)
- ~3 hours of time

---

## Step 1: Install Dependencies (5 minutes)

```bash
# Install Python monitoring tools
pip install pyppeteer

# Or if you prefer manual monitoring, just use Chrome DevTools
# No installation needed
```

---

## Step 2: Launch Chrome with Debugging (2 minutes)

**Close all Chrome windows first**, then:

```bash
# macOS
/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=/tmp/chrome-debug-claude

# Linux
google-chrome \
  --remote-debugging-port=9222 \
  --user-data-dir=/tmp/chrome-debug-claude

# Windows (PowerShell)
& "C:\Program Files\Google\Chrome\Application\chrome.exe" `
  --remote-debugging-port=9222 `
  --user-data-dir=C:\temp\chrome-debug-claude
```

This will:
- Open a new Chrome window
- Enable remote debugging on port 9222
- Use a temporary profile (you'll need to login to claude.ai)

**Login to claude.ai before proceeding!**

---

## Step 3: Start Monitoring (1 minute)

### Option A: Automated Python Monitor (Recommended)

```bash
cd /home/user/unofficial-claude-api
python3 monitor_api.py
```

You should see:
```
🔌 Connecting to Chrome on port 9222...
✓ Connected to: https://claude.ai/...
📡 Enabling network monitoring...

🔍 Monitoring Claude API calls...
================================================================================
READY! Interact with claude.ai now.
Press Ctrl+C when done to save captured data.
================================================================================
```

### Option B: Manual DevTools

1. In Chrome, press **F12** to open DevTools
2. Go to **Network** tab
3. Filter by: `api/`
4. Check **Preserve log**
5. Ready! Perform actions and right-click requests to copy

---

## Step 4: Projects Discovery (30 minutes)

Follow these steps **in order**, watching the terminal for API calls:

### ✅ Action 1: Create Project
1. Go to https://claude.ai
2. Click "Projects" tab
3. Click "New Project" or "+ Create Project"
4. Enter:
   - Name: "API Discovery Test"
   - Description: "Testing endpoint discovery"
5. Click "Create"

**Expected capture:**
- `POST /api/organizations/{org_id}/projects`

---

### ✅ Action 2: Upload File to Project
1. In the project, find "Add knowledge" or "Upload files"
2. Create a test file:
   ```bash
   echo "This is a test file for API discovery" > test-file.txt
   ```
3. Upload `test-file.txt`
4. Wait for upload to complete

**Expected capture:**
- `POST /api/organizations/{org_id}/upload` or
- `POST /api/organizations/{org_id}/projects/{project_id}/files`

---

### ✅ Action 3: Update Custom Instructions
1. In project, find "Custom instructions" or "Settings"
2. Add text: "You are a helpful API documentation assistant."
3. Save/Update

**Expected capture:**
- `PATCH /api/organizations/{org_id}/projects/{project_id}` or
- `PUT /api/organizations/{org_id}/projects/{project_id}/instructions`

---

### ✅ Action 4: Create Chat in Project
1. In the project, start a new conversation
2. May happen automatically when you try to send a message

**Expected capture:**
- `POST /api/organizations/{org_id}/projects/{project_id}/chat_conversations`

---

### ✅ Action 5: Send Message in Project
1. Type: "What files are available in this project?"
2. Send message
3. Wait for response

**Expected capture:**
- `POST /api/organizations/{org_id}/projects/{project_id}/chat_conversations/{chat_id}/completion`
- Streaming response (Server-Sent Events)

---

### ✅ Action 6: View Project Details
1. Go back to project overview
2. View files list
3. View chats list

**Expected capture:**
- `GET /api/organizations/{org_id}/projects/{project_id}`
- `GET /api/organizations/{org_id}/projects/{project_id}/files`

---

### ✅ Action 7: Delete File
1. In project files, find the uploaded file
2. Delete it (hover → click delete icon)
3. Confirm

**Expected capture:**
- `DELETE /api/organizations/{org_id}/projects/{project_id}/files/{file_id}`

---

### ✅ Action 8: Delete Project
1. Go to project settings or list
2. Delete the test project
3. Confirm

**Expected capture:**
- `DELETE /api/organizations/{org_id}/projects/{project_id}`

---

## Step 5: Code Discovery (45 minutes)

### ⚠️ Note: Claude Code may require Pro/Team subscription

### ✅ Action 9: Create Workspace
1. Navigate to https://claude.ai/code
2. Click "New Workspace" or "Connect Repository"
3. Enter GitHub repo: `octocat/Hello-World` (public repo)
4. Select branch: `main`
5. Click "Create" or "Continue"

**Expected capture:**
- `POST /api/code/workspaces`
- Possibly WebSocket connection to `wss://claude.ai/api/code/workspaces/{id}/stream`

---

### ✅ Action 10: Monitor Workspace Setup
1. Watch the progress indicators
2. Note each status change
3. Wait until "Ready" status

**Expected capture:**
- `GET /api/code/workspaces/{workspace_id}` (polling)
- WebSocket messages with status updates

---

### ✅ Action 11: Browse Files
1. Once ready, expand the file tree
2. Click on a file to view contents
3. Navigate to different directories

**Expected capture:**
- `GET /api/code/workspaces/{workspace_id}/files?path=/`
- `GET /api/code/workspaces/{workspace_id}/files/{file_path}`

---

### ✅ Action 12: Send Code Task
1. In the workspace, send: "Add a comment at the top of README.md"
2. Watch Claude's response
3. View the code changes

**Expected capture:**
- `POST /api/code/workspaces/{workspace_id}/messages` or
- `POST /api/code/workspaces/{workspace_id}/completion`
- Streaming response

---

### ✅ Action 13: Edit File
1. Click "Edit" on a file (if available)
2. Make a small change
3. Save

**Expected capture:**
- `PUT /api/code/workspaces/{workspace_id}/files/{file_path}` or
- `PATCH /api/code/workspaces/{workspace_id}/files/{file_path}`

---

### ✅ Action 14: Execute Code (if available)
1. Look for "Run" or "Terminal" button
2. Execute a simple command like `ls` or `cat README.md`

**Expected capture:**
- `POST /api/code/workspaces/{workspace_id}/execute`

---

### ✅ Action 15: Terminate Workspace
1. Go to workspace settings
2. Click "Terminate" or "Delete workspace"
3. Confirm

**Expected capture:**
- `DELETE /api/code/workspaces/{workspace_id}`

---

## Step 6: Stop Monitoring & Save (1 minute)

### If using Python monitor:

Press **Ctrl+C** in the terminal

You'll see:
```
⏹️  Stopping monitor...

✓ Saved 25 API calls to: api-calls-20251107_123456.json
✓ Saved 15 WebSocket messages to: websocket-messages-20251107_123456.json

================================================================================
SUMMARY
================================================================================

Total API calls: 25
Unique endpoints: 15

Endpoint breakdown:
    2x  POST /api/organizations/{org_id}/projects
    1x  POST /api/organizations/{org_id}/upload
    ...
```

### If using manual DevTools:

1. In Network tab, right-click each API call
2. Select "Copy" → "Copy as cURL"
3. Paste into a text file
4. Or right-click → "Save all as HAR"

---

## Step 7: Document Findings (30 minutes)

Open `api-endpoints-template.md` and fill in:

1. For each captured endpoint:
   - Copy request URL, method, headers
   - Copy request payload (if any)
   - Copy response body
   - Note status code
   - Add observations

2. Look for patterns:
   - URL structure
   - Authentication method
   - Response formats
   - Error handling

3. Note surprises:
   - Unexpected endpoints
   - Different payload structures
   - WebSocket usage
   - Streaming responses

---

## Step 8: Validate (15 minutes)

Test a few endpoints with cURL:

```bash
# Example: List projects
curl 'https://claude.ai/api/organizations/{your_org_id}/projects' \
  -H 'Cookie: sessionKey=your_session_key' \
  -H 'User-Agent: Mozilla/5.0...'

# Example: Get project details
curl 'https://claude.ai/api/organizations/{org_id}/projects/{project_id}' \
  -H 'Cookie: sessionKey=your_session_key'
```

Verify responses match what was captured.

---

## Expected Results

After completing all steps, you should have:

- ✅ **~15-20 documented endpoints** for Projects
- ✅ **~10-15 documented endpoints** for Code
- ✅ **Request/response examples** for each
- ✅ **WebSocket message formats** (if applicable)
- ✅ **Error response patterns**
- ✅ **Complete API specification**

Files created:
- `api-calls-TIMESTAMP.json` - All captured API calls
- `websocket-messages-TIMESTAMP.json` - WebSocket messages
- `api-endpoints-template.md` - Filled in with real data

---

## Troubleshooting

### Chrome won't connect
```bash
# Kill all Chrome processes
pkill -9 chrome  # Linux/Mac
taskkill /F /IM chrome.exe  # Windows

# Remove temp directory
rm -rf /tmp/chrome-debug-claude

# Try again
```

### Python monitor fails to connect
```bash
# Check if Chrome is running with debugging
curl http://localhost:9222/json

# Should return JSON with open tabs
# If not, Chrome debugging is not enabled
```

### No API calls showing up
- Make sure filter is correct (looking for 'claude.ai/api')
- Check you're logged into claude.ai
- Try refreshing the page and repeating action

### WebSocket not captured
- WebSocket monitoring may not work in all setups
- Fallback: Use Chrome DevTools → Network → WS filter
- Manually copy WebSocket frames

### Project features not available
- Projects may require Pro subscription
- Check if feature is visible in UI
- Document what you can access

### Code workspace won't create
- Claude Code may require Team/Enterprise
- Try with public GitHub repos first
- Note any error messages

---

## Next Steps

Once you have the API documentation:

1. ✅ Review findings with implementation team
2. ✅ Update `analysis-report.md` with real endpoints
3. ✅ Adjust implementation estimates
4. ✅ Start coding `ClaudeProjectClient`
5. ✅ Write tests with captured responses

---

## Tips

- **Take your time** - Rushing leads to missed captures
- **One action at a time** - Let each request complete before next
- **Watch the terminal** - Verify each capture happens
- **Take notes** - Document anything unexpected
- **Save frequently** - Copy important captures immediately
- **Test assumptions** - If unsure, try the action twice

---

## Questions?

Refer to:
- `api-discovery-plan.md` - Full detailed plan
- `monitor_api.py` - Monitoring script source
- `api-endpoints-template.md` - Documentation template

Good luck! 🚀
