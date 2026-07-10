import { useState } from "react";

import { ConversationSidebar } from "../components/ConversationSidebar";
import { MessageInput } from "../components/ChatInterface/MessageInput";
import { MessageList } from "../components/ChatInterface/MessageList";
import { useChat } from "../hooks/useChat";
import { chatApi } from "../services/api";

export function ChatPage() {
  const [conversationId, setConversationId] = useState<string | null>(null);
  const { messages, sending, error, sendMessage } = useChat(conversationId ?? "");

  async function handleCreate() {
    const response = await chatApi.createConversation();
    setConversationId(response.data.conversation_id);
  }

  return (
    <div className="flex h-[calc(100vh-3.5rem)]">
      <ConversationSidebar
        activeConversationId={conversationId}
        onSelect={setConversationId}
        onCreate={handleCreate}
      />
      <div className="flex-1 flex flex-col bg-background">
        {conversationId ? (
          <>
            <div className="px-4 py-3 border-b border-border bg-surface flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-success animate-pulse" />
              <span className="text-xs text-secondary">AI Assistant ready</span>
            </div>
            <MessageList messages={messages} sending={sending} />
            {error && (
              <div className="mx-4 mb-2 bg-danger/10 border border-danger/30 text-danger text-xs rounded-lg px-3 py-2">
                {error}
              </div>
            )}
            <MessageInput onSend={sendMessage} disabled={sending} />
          </>
        ) : (
          <div className="flex-1 flex flex-col items-center justify-center gap-4 text-center p-8">
            <div className="w-16 h-16 rounded-2xl bg-gradient-brand flex items-center justify-center shadow-lg shadow-primary/30">
              <svg className="w-8 h-8 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z" />
              </svg>
            </div>
            <div>
              <h2 className="text-lg font-bold text-white">Start a conversation</h2>
              <p className="text-sm text-muted mt-1 max-w-xs">
                Select an existing conversation or create a new one to query your documents.
              </p>
            </div>
            <button
              onClick={handleCreate}
              className="bg-gradient-brand text-white text-sm font-semibold px-5 py-2.5 rounded-xl shadow-lg shadow-primary/30 hover:opacity-90 transition"
            >
              New Conversation →
            </button>
          </div>
        )}
      </div>
    </div>
  );
}
