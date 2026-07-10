import { useState } from "react";
import { MAX_MESSAGE_LENGTH } from "../../utils/constants";
import { validateMessage } from "../../utils/validators";

interface MessageInputProps {
  onSend: (text: string) => void;
  disabled: boolean;
}

export function MessageInput({ onSend, disabled }: MessageInputProps) {
  const [text, setText] = useState("");
  const [error, setError] = useState<string | null>(null);

  function handleSubmit() {
    const validationError = validateMessage(text);
    if (validationError) { setError(validationError); return; }
    setError(null);
    onSend(text);
    setText("");
  }

  return (
    <div className="border-t border-border bg-surface p-4">
      {error && (
        <p className="text-danger text-xs mb-2">{error}</p>
      )}
      <div className="flex gap-2 items-end">
        <textarea
          value={text}
          onChange={(e) => { setText(e.target.value); setError(null); }}
          onKeyDown={(e) => { if (e.key === "Enter" && e.ctrlKey) handleSubmit(); }}
          maxLength={MAX_MESSAGE_LENGTH}
          placeholder="Ask a question about your documents... (Ctrl+Enter to send)"
          className="flex-1 bg-card border border-border rounded-xl px-4 py-3 text-sm text-white placeholder-muted resize-none h-16 focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition"
        />
        <button
          onClick={handleSubmit}
          disabled={disabled || !text.trim()}
          className="h-16 w-12 bg-gradient-brand text-white rounded-xl flex items-center justify-center disabled:opacity-40 hover:opacity-90 transition flex-shrink-0 shadow-lg shadow-primary/20"
        >
          <svg className="w-5 h-5" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M12 19l9 2-9-18-9 18 9-2zm0 0v-8" />
          </svg>
        </button>
      </div>
      <p className="text-xs text-muted mt-1.5 text-right">{text.length}/{MAX_MESSAGE_LENGTH}</p>
    </div>
  );
}
