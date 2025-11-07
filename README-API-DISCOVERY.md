# API Discovery Toolkit - Ready to Use! 🚀

This toolkit enables you to reverse-engineer Claude's Projects and Code APIs by monitoring real browser interactions.

---

## What We've Built

### 📋 Complete Documentation
1. **analysis-report.md** (2,119 lines)
   - Full codebase analysis
   - Extension designs with code samples
   - Pros/cons and recommendations
   - Implementation roadmap

2. **api-discovery-plan.md** (detailed guide)
   - 3 monitoring options (CDP, MCP, Manual)
   - 15 capture scenarios
   - Data capture templates
   - Expected timeline: 2.5 hours

3. **QUICKSTART-API-DISCOVERY.md** (quick reference)
   - Step-by-step instructions
   - Copy-paste commands
   - Troubleshooting tips
   - Estimated time: 2-3 hours

4. **api-endpoints-template.md** (structured template)
   - Pre-formatted endpoint sections
   - Request/response examples
   - Common patterns
   - Observations checklist

### 🔧 Tools

**monitor_api.py** - Real-time API Monitor
- Connects to Chrome via DevTools Protocol
- Captures all claude.ai API calls automatically
- Monitors WebSocket messages
- Saves to timestamped JSON files
- Prints endpoint summary

```bash
# One-command start:
python3 monitor_api.py

# Output: api-calls-TIMESTAMP.json
#         websocket-messages-TIMESTAMP.json
```

---

## Quick Start (5 Minutes)

### Option 1: Automated Monitoring (Recommended)

```bash
# 1. Install dependency
pip install pyppeteer

# 2. Launch Chrome with debugging
google-chrome --remote-debugging-port=9222 \
  --user-data-dir=/tmp/chrome-debug-claude

# 3. Login to claude.ai in the Chrome window

# 4. In a new terminal, start monitor
cd /home/user/unofficial-claude-api
python3 monitor_api.py

# 5. Perform actions in Claude UI
# - Create project
# - Upload file
# - Send message
# etc.

# 6. Press Ctrl+C when done
# API calls saved to api-calls-TIMESTAMP.json ✓
```

### Option 2: Manual DevTools

```bash
# 1. Open Chrome normally
# 2. Navigate to claude.ai
# 3. Press F12 → Network tab → Filter: "api/"
# 4. Perform actions
# 5. Right-click requests → Copy as cURL
```

---

## Discovery Workflow

### Phase 1: Projects API (30 min)

Execute these actions in Claude UI:

1. ✅ Create project
2. ✅ Upload file to project
3. ✅ Update custom instructions
4. ✅ Create chat in project
5. ✅ Send message (with project context)
6. ✅ View project details
7. ✅ Delete file
8. ✅ Delete project

**Expected Output:** 8-10 Projects endpoints captured

---

### Phase 2: Code API (45 min)

Execute these actions:

1. ✅ Create workspace from GitHub repo
2. ✅ Monitor workspace setup progress
3. ✅ Browse workspace files
4. ✅ Send code task to Claude
5. ✅ Edit file directly
6. ✅ Execute command (if available)
7. ✅ Terminate workspace

**Expected Output:** 10-12 Code endpoints captured + WebSocket messages

---

## Output Files

After running `monitor_api.py` and pressing Ctrl+C:

```
api-calls-20251107_123456.json
websocket-messages-20251107_123456.json
```

Example `api-calls-TIMESTAMP.json`:
```json
[
  {
    "timestamp": "2025-11-07T12:34:56.789",
    "type": "request",
    "method": "POST",
    "url": "https://claude.ai/api/organizations/org-123/projects",
    "headers": { ... },
    "postData": "{\"name\":\"Test\",\"uuid\":\"...\"}",
    "response": {
      "status": 201,
      "body": "{\"uuid\":\"...\",\"name\":\"Test\"}"
    }
  },
  ...
]
```

---

## Next Steps After Discovery

1. **Review Captures** (15 min)
   - Open `api-calls-TIMESTAMP.json`
   - Verify all expected endpoints captured
   - Note any surprises

2. **Fill Template** (30 min)
   - Open `api-endpoints-template.md`
   - Copy real data from captured JSON
   - Document each endpoint
   - Add observations

3. **Validate** (15 min)
   - Test a few endpoints with cURL
   - Verify responses match
   - Confirm authentication works

4. **Update Implementation** (1 hour)
   - Adjust `ClaudeProjectClient` design in analysis-report.md
   - Adjust `ClaudeCodeClient` design
   - Update time estimates
   - Refine implementation plan

5. **Start Coding** (Week 1)
   - Create `claude_api/projects.py`
   - Implement based on real API
   - Write tests
   - Document usage

---

## Troubleshooting

### Chrome won't start with debugging
```bash
# Kill all Chrome instances
pkill -9 chrome

# Remove temp directory
rm -rf /tmp/chrome-debug-claude

# Try again
```

### Python script can't connect
```bash
# Verify Chrome debugging is running
curl http://localhost:9222/json

# Should return JSON list of tabs
# If not, Chrome debugging port not open
```

### No API calls appearing
- Make sure you're logged into claude.ai
- Check Network filter is set to "api/"
- Verify actions are actually completing
- Try refreshing page and repeating

### Missing pyppeteer
```bash
pip install pyppeteer
# Or
pip3 install pyppeteer
```

---

## Files Overview

```
unofficial-claude-api/
├── analysis-report.md              # Full analysis (READ FIRST)
├── api-discovery-plan.md           # Detailed discovery plan
├── QUICKSTART-API-DISCOVERY.md     # Quick reference guide
├── api-endpoints-template.md       # Documentation template
├── monitor_api.py                  # Automated monitoring tool
└── README-API-DISCOVERY.md         # This file

Generated after discovery:
├── api-calls-TIMESTAMP.json        # Captured API calls
└── websocket-messages-TIMESTAMP.json  # Captured WS messages
```

---

## What Each File Does

| File | Purpose | When to Use |
|------|---------|-------------|
| `analysis-report.md` | Understand the codebase and extension strategy | Read before starting |
| `api-discovery-plan.md` | Detailed reference for all scenarios | During discovery session |
| `QUICKSTART-API-DISCOVERY.md` | Step-by-step quick guide | During discovery session |
| `api-endpoints-template.md` | Structure for documenting findings | After capturing calls |
| `monitor_api.py` | Automated API call capture | During discovery session |
| `README-API-DISCOVERY.md` | Overview and quick start | Start here! |

---

## Monitoring Options Comparison

| Option | Setup Time | Ease of Use | Completeness | Best For |
|--------|------------|-------------|--------------|----------|
| **Python CDP** | 5 min | Easy | 95% | Most users |
| **Manual DevTools** | 1 min | Manual | 90% | Quick tests |
| **MCP Server** | 10 min | Medium | 95% | MCP integration |

**Recommendation:** Start with **Python CDP** (monitor_api.py)

---

## Expected Results

After 2-3 hours of discovery:

✅ **Projects API:**
- `POST /api/organizations/{org}/projects` - Create
- `GET /api/organizations/{org}/projects` - List
- `GET /api/organizations/{org}/projects/{id}` - Get
- `PATCH /api/organizations/{org}/projects/{id}` - Update
- `DELETE /api/organizations/{org}/projects/{id}` - Delete
- `POST /api/organizations/{org}/projects/{id}/files` - Upload file
- `DELETE /api/organizations/{org}/projects/{id}/files/{file_id}` - Delete file
- `POST /api/organizations/{org}/projects/{id}/chat_conversations` - Create chat
- `POST /api/organizations/{org}/projects/{id}/chat_conversations/{chat_id}/completion` - Send message

✅ **Code API:**
- `POST /api/code/workspaces` - Create
- `GET /api/code/workspaces/{id}` - Status
- `DELETE /api/code/workspaces/{id}` - Terminate
- `GET /api/code/workspaces/{id}/files` - List files
- `GET /api/code/workspaces/{id}/files/{path}` - Read file
- `PUT /api/code/workspaces/{id}/files/{path}` - Update file
- `POST /api/code/workspaces/{id}/messages` - Send task
- `POST /api/code/workspaces/{id}/execute` - Run command
- `wss://.../workspaces/{id}/stream` - Progress WebSocket

✅ **Documentation:**
- Complete endpoint list
- Request/response examples
- Authentication requirements
- Error patterns
- WebSocket message formats

---

## Success Checklist

Before moving to implementation:

- [ ] Captured all 15+ Projects endpoints
- [ ] Captured all 10+ Code endpoints
- [ ] Documented request formats
- [ ] Documented response formats
- [ ] Captured WebSocket messages (Code)
- [ ] Noted error responses
- [ ] Tested 2-3 endpoints with cURL
- [ ] Filled in api-endpoints-template.md
- [ ] Identified any unknowns/surprises
- [ ] Updated analysis-report.md with findings

---

## Timeline Summary

| Phase | Time | Activity |
|-------|------|----------|
| **Setup** | 5 min | Install tools, launch Chrome |
| **Projects** | 30 min | Execute 8 scenarios, capture endpoints |
| **Code** | 45 min | Execute 7 scenarios, capture endpoints |
| **Document** | 30 min | Fill template with captured data |
| **Validate** | 15 min | Test with cURL, verify responses |
| **Review** | 15 min | Check completeness, note surprises |
| **TOTAL** | **2.5 hours** | Complete API specification |

---

## Ready to Begin?

### Pre-flight Checklist:

- [ ] Chrome installed
- [ ] Python 3.10+ installed
- [ ] Claude.ai account ready
- [ ] 3 hours available
- [ ] Read QUICKSTART-API-DISCOVERY.md

### Launch Sequence:

```bash
# 1. Install
pip install pyppeteer

# 2. Launch Chrome
google-chrome --remote-debugging-port=9222 \
  --user-data-dir=/tmp/chrome-debug-claude

# 3. Login to claude.ai

# 4. Start monitor (new terminal)
python3 monitor_api.py

# 5. Follow QUICKSTART guide to perform actions

# 6. Ctrl+C to save

# 7. Review captured data

# 8. Fill in template

# 9. Start implementation!
```

---

## Questions?

**During setup:**
- See troubleshooting section above
- Check QUICKSTART-API-DISCOVERY.md

**During discovery:**
- Follow api-discovery-plan.md scenarios
- Watch terminal for real-time captures

**After discovery:**
- Fill api-endpoints-template.md
- Validate with cURL
- Update analysis-report.md

---

## Support & Contributing

Found an issue or have suggestions?
- Document in api-endpoints-template.md "Observations" section
- Note in implementation plan
- Update analysis-report.md with new findings

---

**Ready when you are!** 🎯

The toolkit is complete and ready to use. Just say the word and we can start the discovery session together, or you can run it independently following the QUICKSTART guide.

Good luck! 🚀
