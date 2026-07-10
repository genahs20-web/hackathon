import ReactMarkdown from "react-markdown";
import type { ChatMessageView } from "../../hooks/useChat";
import { formatConfidence } from "../../utils/formatters";

interface MessageListProps {
  messages: ChatMessageView[];
  sending: boolean;
}

export function MessageList({ messages, sending }: MessageListProps) {
  return (
    <div className="flex-1 overflow-y-auto p-4 space-y-4">
      {messages.map((message) => (
        <div key={message.id} className={`flex gap-3 ${message.sender === "user" ? "flex-row-reverse" : "flex-row"}`}>
          {/* Avatar */}
          <div className={`w-7 h-7 rounded-full flex-shrink-0 flex items-center justify-center text-xs font-bold ${
            message.sender === "user"
              ? "bg-gradient-brand text-white"
              : "bg-surface border border-border text-accent"
          }`}>
            {message.sender === "user" ? "U" : "AI"}
          </div>

          {/* Bubble */}
          <div className={`max-w-xl rounded-2xl px-4 py-3 text-sm ${
            message.sender === "user"
              ? "bg-primary/20 border border-primary/30 text-white rounded-tr-sm"
              : "bg-card border border-border text-slate-200 rounded-tl-sm"
          }`}>
            <div className="prose prose-invert prose-sm max-w-none">
              <ReactMarkdown>{message.text}</ReactMarkdown>
            </div>

            {message.sources && message.sources.length > 0 && (
              <details className="mt-3 text-xs">
                <summary className="cursor-pointer text-muted hover:text-secondary transition select-none">
                  📎 {message.sources.length} source{message.sources.length > 1 ? "s" : ""}
                  {message.confidence !== undefined && (
                    <span className="ml-2 bg-success/20 text-success px-1.5 py-0.5 rounded-full">
                      {formatConfidence(message.confidence)} confidence
                    </span>
                  )}
                </summary>
                <ul className="mt-2 space-y-1.5 pl-2 border-l border-border">
                  {message.sources.map((source, i) => (
                    <li key={i} className="text-muted">
                      <span className="text-secondary font-medium">{source.document_name}</span>
                      {" — "}
                      {source.snippet.slice(0, 100)}…
                    </li>
                  ))}
                </ul>
              </details>
            )}
          </div>
        </div>
      ))}

      {sending && (
        <div className="flex gap-3">
          <div className="w-7 h-7 rounded-full bg-surface border border-border flex items-center justify-center text-xs text-accent">AI</div>
          <div className="bg-card border border-border rounded-2xl rounded-tl-sm px-4 py-3 flex items-center gap-1.5">
            {[0, 1, 2].map((i) => (
              <span
                key={i}
                className="w-1.5 h-1.5 bg-muted rounded-full animate-bounce"
                style={{ animationDelay: `${i * 0.15}s` }}
              />
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
