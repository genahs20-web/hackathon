# Deliverable 5: Wireframes & User Interface Design
## AI Knowledge Discovery & Decision Assistant

---

## Design System

**Color Palette**

| Token | Hex | Usage |
|---|---|---|
| Background | `#F8FAFC` | Page background |
| Card | `#FFFFFF` | Card/panel surfaces |
| Primary | `#1E3A8A` | Headings, primary buttons |
| Secondary | `#475569` | Secondary text |
| Accent | `#2563EB` | Links, active states |
| Success | `#16A34A` | Success states, "indexed" badge |
| Warning | `#CA8A04` | "processing" badge, medium severity |
| Danger | `#DC2626` | Errors, "failed" badge, high severity |
| Neutral text | `#1F2937` | Body text |

**Typography:** H1 32px/bold, H2 24px/bold, Body 16px, Small 14px, Labels 14px/medium — all in `#1E3A8A`/`#4B5563` as appropriate.

**Spacing scale:** 8 / 16 / 24 / 32 / 48 px.

**Components:** Buttons 40px height, rounded 6px · Inputs 40px height, 1px border `#E5E7EB` · Cards 1px border + subtle shadow · Tables striped with `#F3F4F6` header · Modals centered with dark overlay.

---

## Screen 1: Login

```
┌─────────────────────────────────────────┐
│                                           │
│         ┌───────────────────────┐        │
│         │   AI Knowledge Assist  │       │
│         │                        │       │
│         │  Email                 │       │
│         │  [_____________________]│      │
│         │  Password        [👁]  │       │
│         │  [_____________________]│      │
│         │  [ ] Remember me       │       │
│         │           Forgot pw?   │       │
│         │  [      Sign In       ]│       │
│         │  Don't have an account?│       │
│         │        Sign up         │       │
│         └───────────────────────┘        │
└─────────────────────────────────────────┘
```
**Interactions:** Email validated on blur · password visibility toggle · submit disabled while pending · inline error text below the offending field.

---

## Screen 2: Dashboard

```
┌──────────────────────────────────────────────────────────┐
│ Logo        AI Knowledge Discovery      [user ▾] [Logout] │
├───────────┬────────────────────────────────────────────────┤
│ Dashboard │ ┌─Quick Upload──┐┌─Documents──┐┌─Recent Q's──┐ │
│ Documents │ │ drag & drop   ││   24 total  ││ "renewal.." │ │
│ Chat      │ │ pdf/docx/...  ││ 2 processing││ "vendor.."  │ │
│ Conflicts │ └───────────────┘└────────────┘└─────────────┘ │
│ Recs.     │ ┌─Recommendations┐┌─Conflicts──┐┌─Renewals───┐ │
│ Admin     │ │ 5 pending      ││ 2 flagged  ││   87%      │ │
│           │ └───────────────┘└────────────┘└─────────────┘ │
│           │ ┌─ Recent Conversations ──────────────────────┐ │
│           │ │ Table: Title | Updated | # msgs             │ │
│           │ └──────────────────────────────────────────────┘│
└───────────┴────────────────────────────────────────────────┘
```
**Interactions:** Cards hover-highlight and navigate on click; quick-upload accepts drag-drop directly from dashboard.

---

## Screen 3: Document Management

```
┌──────────────────────────────────────────────────────────┐
│ Your Documents                       [+ Upload Document] │
│ [Search...........] [Status ▾] [Format ▾]                │
├──────────────────────────────────────────────────────────┤
│ Name              | Format | Status    | Size  | Actions │
│ remote_policy.pdf | PDF    | Indexed   | 200KB | 👁 🗑 ↻  │
│ vendor_q2.xlsx    | XLSX   | Processing| 1.2MB | 👁 🗑    │
│ board_notes.eml   | EML    | Failed    | 40KB  | 🗑 ↻     │
├──────────────────────────────────────────────────────────┤
│                     ‹ 1 2 3 ›                             │
└──────────────────────────────────────────────────────────┘
```
**Details:** Failed rows show error tooltip on hover; progress bar replaces status text while `processing`.

---

## Screen 4: Query & Search

```
┌──────────────────────────────────────────────────────────┐
│ [ Search: "policy renewal deadlines"           ] [Search] │
├───────────┬──────────────────────────────────────────────┤
│ Filters   │ Result 1 — remote_policy_2025.pdf   (0.91)   │
│ Date ▾    │ "...renewal deadline is 90 days prior..."    │
│ Doc ▾     │ Page 4              [View in context]        │
│ Conf. ▾   │ Result 2 — vendor_contract.docx     (0.84)   │
│           │ "...auto-renews annually unless..."          │
│           │ Page 2              [View in context]        │
└───────────┴──────────────────────────────────────────────┘
```
**Interactions:** Auto-complete suggestions; matching terms highlighted; click opens preview modal with surrounding context.

---

## Screen 5: Chat / Conversation

```
┌──────────────────────────────────────────────────────────┐
│ Conversations│ Q2 Vendor Risk Review                      │
│ + New        │ ┌────────────────────────────────────────┐│
│ • Q2 Vendor..│ │           What's our vendor risk?  [You]││
│ • Remote wk..│ │[Assistant] 2 vendors flagged high-risk  ││
│ • Onboarding │ │  in Q2 report. Sources: vendor_q2.xlsx  ││
│              │ │  (Row 14), board_notes.eml               ││
│              │ │  [Copy][Save as recommendation]          ││
│              │ └────────────────────────────────────────┘│
│              │ [ Type a message...           ] [📎][Send]│
└──────────────────────────────────────────────────────────┘
```
**Interactions:** Streaming assistant text; typing indicator; sources collapsible; markdown rendering; copy/edit/delete on hover.

---

## Screen 6: Conflict Detection

```
┌──────────────────────────────────────────────────────────┐
│ Identified Conflicts     [All] [Low] [Medium] [High]      │
├──────────────────────────────────────────────────────────┤
│ ⚠ MEDIUM  Remote work days: 2024 policy says 2, 2025      │
│           says 3 days/week          [Resolved: No]        │
│           Docs: [remote_2024.pdf] [remote_2025.pdf]        │
│                                     [View Details]         │
├──────────────────────────────────────────────────────────┤
│ Details Modal:                                             │
│  Side-by-side excerpts | Suggested resolution              │
│  [Resolution notes.....................] [Mark Resolved]   │
└──────────────────────────────────────────────────────────┘
```

---

## Screen 7: Recommendations

```
┌──────────────────────────────────────────────────────────┐
│ AI Recommendations         [Pending][Approved][Rejected]  │
├──────────────────────────────────────────────────────────┤
│ Schedule review with Procurement — 2 vendors high-risk    │
│ Confidence: [████████░░] 87%                              │
│ Supporting: vendor_q2.xlsx, board_notes.eml                │
│ [Approve] [Reject] [View Details]                          │
└──────────────────────────────────────────────────────────┘
```

---

## Screen 8: Admin Dashboard

```
┌──────────────────────────────────────────────────────────┐
│ Users            | Documents         | Audit Logs         │
│ [+ Add User]     | Total: 340        | [Search logs...]   │
│ Table: name/email| [Reindex All]     | Table: action/user │
│ /role/actions    |                   | /entity/time        │
├──────────────────────────────────────────────────────────┤
│ System Health: API ● Up | DB ● Up | ChromaDB ● Up          │
└──────────────────────────────────────────────────────────┘
```

---

*End of Deliverable 5.*
