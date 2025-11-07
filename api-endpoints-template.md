# Claude API Endpoints Documentation
## Discovered through real-time monitoring

**Discovery Date:** [Fill in]
**Claude Account Type:** [Free/Pro/Team]
**Browser:** Chrome + CDP

---

## PROJECTS API

### 1. List Projects

**Request:**
```http
GET /api/organizations/{org_id}/projects HTTP/1.1
Host: claude.ai
Cookie: sessionKey=...
User-Agent: ...
```

**Response:**
```json
{
  "projects": [
    {
      "uuid": "...",
      "name": "...",
      "description": "...",
      "created_at": "...",
      "file_count": 0
    }
  ]
}
```

**Status Code:** `200 OK`

**Notes:**
- [Add observations]

---

### 2. Create Project

**Request:**
```http
POST /api/organizations/{org_id}/projects HTTP/1.1
Host: claude.ai
Content-Type: application/json
Cookie: sessionKey=...

{
  "name": "Test Project",
  "description": "Test description",
  "uuid": "generated-uuid",
  "custom_instructions": ""
}
```

**Response:**
```json
{
  "uuid": "...",
  "name": "...",
  "description": "...",
  "created_at": "...",
  "updated_at": "...",
  "organization_id": "...",
  "custom_instructions": "",
  "file_ids": [],
  "chat_conversation_ids": []
}
```

**Status Code:** `201 Created`

**Notes:**
- UUID is client-generated (like chat creation)
- [Other observations]

---

### 3. Get Project Details

**Request:**
```http
GET /api/organizations/{org_id}/projects/{project_id} HTTP/1.1
Host: claude.ai
Cookie: sessionKey=...
```

**Response:**
```json
{
  "uuid": "...",
  "name": "...",
  "description": "...",
  "custom_instructions": "...",
  "files": [...],
  "chat_conversations": [...]
}
```

**Status Code:** `200 OK`

---

### 4. Update Project (Custom Instructions)

**Request:**
```http
PATCH /api/organizations/{org_id}/projects/{project_id} HTTP/1.1
Host: claude.ai
Content-Type: application/json

{
  "custom_instructions": "You are a helpful assistant..."
}
```

**Response:**
```json
{
  "uuid": "...",
  "custom_instructions": "..."
}
```

**Status Code:** `200 OK`

---

### 5. Upload Project File

**Request:**
```http
POST /api/organizations/{org_id}/projects/{project_id}/files HTTP/1.1
Host: claude.ai
Content-Type: multipart/form-data; boundary=...

--boundary
Content-Disposition: form-data; name="file"; filename="test.txt"
Content-Type: text/plain

[file content]
--boundary
Content-Disposition: form-data; name="projectId"

{project_id}
--boundary--
```

**Response:**
```json
{
  "file_uuid": "...",
  "file_name": "test.txt",
  "file_size": 1234,
  "created_at": "..."
}
```

**Status Code:** `200 OK`

**Notes:**
- Similar to regular file upload but scoped to project
- [Other observations]

---

### 6. List Project Files

**Request:**
```http
GET /api/organizations/{org_id}/projects/{project_id}/files HTTP/1.1
```

**Response:**
```json
{
  "files": [
    {
      "uuid": "...",
      "file_name": "...",
      "file_size": 1234,
      "file_type": "text/plain",
      "created_at": "..."
    }
  ]
}
```

---

### 7. Delete Project File

**Request:**
```http
DELETE /api/organizations/{org_id}/projects/{project_id}/files/{file_id} HTTP/1.1
```

**Response:**
```
(empty body)
```

**Status Code:** `204 No Content`

---

### 8. Create Project Chat

**Request:**
```http
POST /api/organizations/{org_id}/projects/{project_id}/chat_conversations HTTP/1.1
Content-Type: application/json

{
  "uuid": "generated-uuid",
  "name": "Chat name",
  "project_id": "{project_id}"
}
```

**Response:**
```json
{
  "uuid": "...",
  "name": "...",
  "project_id": "...",
  "created_at": "..."
}
```

**Status Code:** `201 Created`

---

### 9. Send Project Message

**Request:**
```http
POST /api/organizations/{org_id}/projects/{project_id}/chat_conversations/{chat_id}/completion HTTP/1.1
Content-Type: application/json
Accept: text/event-stream

{
  "prompt": "Hello",
  "timezone": "America/New_York",
  "attachments": [],
  "files": [],
  "project_id": "{project_id}"
}
```

**Response:** (Server-Sent Events)
```
data: {"completion": "Hello", ...}
data: {"completion": " there", ...}
...
```

**Status Code:** `200 OK`

**Notes:**
- Streaming response
- Project files auto-included in context
- Custom instructions applied
- [Other observations]

---

### 10. Delete Project

**Request:**
```http
DELETE /api/organizations/{org_id}/projects/{project_id} HTTP/1.1
```

**Response:**
```
(empty body)
```

**Status Code:** `204 No Content`

---

## CODE API

### 1. Create Workspace

**Request:**
```http
POST /api/code/workspaces HTTP/1.1
Content-Type: application/json

{
  "github_repo": "octocat/Hello-World",
  "branch": "main",
  "environment": "auto",
  "organization_id": "{org_id}"
}
```

**Response:**
```json
{
  "workspace_id": "...",
  "status": "pending",
  "github_repo": "...",
  "created_at": "..."
}
```

**Status Code:** `201 Created`

---

### 2. Get Workspace Status

**Request:**
```http
GET /api/code/workspaces/{workspace_id} HTTP/1.1
```

**Response:**
```json
{
  "workspace_id": "...",
  "status": "ready",
  "github_repo": "...",
  "branch": "...",
  "environment": "python",
  "url": "https://...",
  "created_at": "...",
  "ready_at": "..."
}
```

**Possible status values:**
- `pending`
- `initializing`
- `cloning_repo`
- `installing_deps`
- `ready`
- `error`
- `terminated`

---

### 3. WebSocket: Workspace Progress Stream

**Connection:**
```
wss://claude.ai/api/code/workspaces/{workspace_id}/stream
```

**Authentication:**
- Cookie header: sessionKey=...

**Message Format:**
```json
{
  "type": "status_update",
  "status": "cloning_repo",
  "message": "Cloning repository from GitHub...",
  "progress": 25,
  "timestamp": "..."
}
```

**Message Types:**
- `status_update` - Status change
- `log` - Console output
- `error` - Error occurred
- `complete` - Setup finished

---

### 4. List Workspace Files

**Request:**
```http
GET /api/code/workspaces/{workspace_id}/files?path=/ HTTP/1.1
```

**Response:**
```json
{
  "files": [
    {
      "name": "README.md",
      "path": "/README.md",
      "type": "file",
      "size": 1234
    },
    {
      "name": "src",
      "path": "/src",
      "type": "directory"
    }
  ]
}
```

---

### 5. Read Workspace File

**Request:**
```http
GET /api/code/workspaces/{workspace_id}/files/{file_path} HTTP/1.1
```

**Response:**
```json
{
  "path": "/README.md",
  "content": "# Hello World...",
  "encoding": "utf-8",
  "size": 1234
}
```

---

### 6. Write/Update Workspace File

**Request:**
```http
PUT /api/code/workspaces/{workspace_id}/files/{file_path} HTTP/1.1
Content-Type: application/json

{
  "content": "# Updated content...",
  "encoding": "utf-8"
}
```

**Response:**
```json
{
  "path": "/README.md",
  "updated_at": "...",
  "size": 1234
}
```

**Status Code:** `200 OK`

---

### 7. Send Code Message

**Request:**
```http
POST /api/code/workspaces/{workspace_id}/messages HTTP/1.1
Content-Type: application/json
Accept: text/event-stream

{
  "prompt": "Add a comment to README.md",
  "context_files": ["/README.md"],
  "timezone": "America/New_York"
}
```

**Response:** (Streaming)
```
data: {"type": "message", "content": "I'll add"}
data: {"type": "message", "content": " a comment"}
data: {"type": "code_change", "file": "/README.md", "diff": "..."}
...
```

---

### 8. Execute Code

**Request:**
```http
POST /api/code/workspaces/{workspace_id}/execute HTTP/1.1
Content-Type: application/json

{
  "command": "python test.py",
  "timeout": 30
}
```

**Response:**
```json
{
  "stdout": "Test output...",
  "stderr": "",
  "exit_code": 0,
  "execution_time": 1.23
}
```

**Status Code:** `200 OK`

---

### 9. Terminate Workspace

**Request:**
```http
DELETE /api/code/workspaces/{workspace_id} HTTP/1.1
```

**Response:**
```
(empty body)
```

**Status Code:** `204 No Content`

---

## COMMON PATTERNS

### Authentication
All requests require:
```http
Cookie: sessionKey=...; __cf_bm=...; ...
```

### Headers
Standard headers:
```http
User-Agent: Mozilla/5.0 ...
Accept: application/json (or text/event-stream for streaming)
Content-Type: application/json
Origin: https://claude.ai
Referer: https://claude.ai/...
DNT: 1
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
```

### Error Responses

**Rate Limit:**
```json
{
  "error": {
    "type": "rate_limit_error",
    "message": "...",
    "resets_at": 1699123456
  }
}
```

**Overload:**
```json
{
  "error": {
    "type": "overloaded_error",
    "message": "..."
  }
}
```

**Not Found:**
```json
{
  "error": {
    "type": "not_found",
    "message": "Resource not found"
  }
}
```

---

## OBSERVATIONS

### Projects
- [Add key observations]
- Files are uploaded separately then referenced
- Custom instructions apply to all chats in project
- Project context auto-included (no need to re-attach files)

### Code
- [Add key observations]
- Workspace creation is async (requires polling or WebSocket)
- File operations are synchronous
- Code execution has timeout limits

### Rate Limiting
- [Observed limits]
- Appears to share limits with regular chats
- Reset times provided in error responses

---

## NEXT STEPS

After completing this documentation:

1. ✅ Validate all endpoints with test requests
2. ✅ Update `ClaudeProjectClient` implementation
3. ✅ Update `ClaudeCodeClient` implementation
4. ✅ Write integration tests
5. ✅ Document usage examples

---

**Last Updated:** [Date]
**Verified Against:** Claude.ai production environment
