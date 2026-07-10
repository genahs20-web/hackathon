import { useEffect, useState } from "react";
import { chatApi, type ConversationDto } from "../services/api";

interface ConversationSidebarProps {
  activeConversationId: string | null;
  onSelect: (conversationId: string) => void;
  onCreate: () => void;
}

export function ConversationSidebar({ activeConversationId, onSelect, onCreate }: ConversationSidebarProps) {
  const [conversations, setConversations] = useState<ConversationDto[]>([]);
  const [search, setSearch] = useState("");

  useEffect(() => {
    chatApi.listConversations().then((res) => setConversations(res.data));
  }, []);

  const filtered = conversations.filter((c) => c.title.toLowerCase().includes(search.toLowerCase()));

  return (
    <div className="w-56 bg-surface border-r border-border flex flex-col">
      <div className="p-3 border-b border-border">
        <button
          onClick={onCreate}
          className="w-full h-9 bg-gradient-brand text-white rounded-xl text-sm font-semibold hover:opacity-90 transition shadow-md shadow-primary/20"
        >
          + New Chat
        </button>
      </div>
      <div className="px-3 py-2">
        <input
          value={search}
          onChange={(e) => setSearch(e.target.value)}
          placeholder="Search chats..."
          className="w-full h-8 px-3 bg-card border border-border rounded-lg text-xs text-white placeholder-muted focus:outline-none focus:border-primary transition"
        />
      </div>
      <p className="px-3 pb-1 text-xs font-semibold text-muted uppercase tracking-wider">Recent</p>
      <ul className="overflow-y-auto flex-1 px-2 pb-2 space-y-0.5">
        {filtered.length === 0 && (
          <li className="text-xs text-muted text-center py-4">No conversations yet</li>
        )}
        {filtered.map((c) => (
          <li key={c.conversation_id}>
            <button
              onClick={() => onSelect(c.conversation_id)}
              className={`w-full text-left px-3 py-2 text-xs rounded-xl truncate transition ${
                c.conversation_id === activeConversationId
                  ? "bg-primary/20 text-accent border border-primary/30 font-medium"
                  : "text-secondary hover:bg-card hover:text-white"
              }`}
            >
              <svg className="w-3 h-3 inline mr-1.5 opacity-60" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
              {c.title}
            </button>
          </li>
        ))}
      </ul>
    </div>
  );
}
