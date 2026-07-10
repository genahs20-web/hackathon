# Screen Behavior Specifications

## Screen: ChatInterface
**Purpose:** Real-time conversation with the AI assistant.

### Component: MessageInput
- Type: textarea, placeholder "Ask a question...", max length 2000
- Behaviors:
  - `keydown (Ctrl+Enter)` → `submit_message()`
  - `focus` → `clear_error_message()`
  - `input` → `update_character_count()`
- Validation: `message.trim().length > 0`, `message.length <= 2000`
- Error display: below input, red `#DC2626`

### Component: MessageDisplay
- User messages: right-aligned, light blue background
- Assistant messages: left-aligned, white background with border
- Timestamp shown below each message
- Sources shown as a collapsible list under assistant messages
- Markdown rendering supported for assistant messages
- Hover reveals copy / delete / edit buttons
- Loading state: skeleton placeholder for incoming message
- Streaming: text appended token-by-token with a blinking cursor

### Component: ConversationSidebar
- Lists 10 most recent conversations
- `click` → `load_conversation(id)`
- "New Conversation" button always visible at top
- Hover reveals Archive / Delete actions
- Current conversation highlighted
- Search box filters by title (client-side substring match)

---

## Screen: DocumentManager

### Component: UploadArea
- Accepts drag-and-drop or click-to-browse
- Accepted MIME types: `application/pdf`, `application/vnd.openxmlformats-officedocument.wordprocessingml.document`, `application/vnd.openxmlformats-officedocument.presentationml.presentation`, `application/vnd.openxmlformats-officedocument.spreadsheetml.sheet`, `message/rfc822`
- On drop/select: client-side validates extension + size before upload begins
- Shows per-file progress bar during upload
- On success: adds row to DocumentTable with status `processing`; polls document status every 3s until `indexed` or `failed`

### Component: DocumentTable
- Columns: Name, Format, Status (badge, color-coded), Size, Upload Date, Actions
- Status badge colors: `uploaded`=slate, `processing`=amber, `indexed`=green, `failed`=red
- Row actions: View, Delete (confirm modal), Reindex (only enabled when status is `indexed` or `failed`)
- Sortable columns: Name, Upload Date, Size
- Pagination: 20 rows/page

---

## Screen: ConflictDetection

### Component: ConflictCard
- Severity badge color-coded (low=slate, medium=amber, high=red)
- Shows involved documents as clickable badges
- `click "View Details"` → opens modal with side-by-side source excerpts
- Modal includes resolution notes textarea + "Mark as Resolved" button
- On resolve: `PATCH` conflict, card moves out of "unresolved" filter view

---

## Screen: Recommendations

### Component: RecommendationCard
- Confidence score rendered as a horizontal progress bar (0-100%)
- Status badge: pending=slate, approved=green, rejected=red
- Actions: Approve, Reject (opens reason textarea), View Details
- Approving/rejecting is optimistic in the UI, rolled back on API error with toast notification

---

## Global Behaviors
- All API errors surface as a dismissible toast with the `user_message` from the matching `ErrorCode` (see `error_handling.md`).
- All authenticated routes redirect to `/login` on a 401 response and clear the local JWT.
- Global loading indicator (top progress bar) shown during any in-flight request > 300ms.
