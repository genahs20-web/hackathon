import { useCallback, useState } from "react";

import { chatApi, type SourceCitation } from "../services/api";
import { validateMessage } from "../utils/validators";

export interface ChatMessageView {
  id: string;
  sender: "user" | "assistant";
  text: string;
  sources?: SourceCitation[];
  confidence?: number;
}

export function useChat(conversationId: string) {
  const [messages, setMessages] = useState<ChatMessageView[]>([]);
  const [sending, setSending] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const sendMessage = useCallback(
    async (text: string) => {
      const validationError = validateMessage(text);
      if (validationError) {
        setError(validationError);
        return;
      }
      setError(null);
      setSending(true);
      setMessages((prev) => [...prev, { id: `local-${Date.now()}`, sender: "user", text }]);

      try {
        const response = await chatApi.sendMessage(conversationId, text);
        setMessages((prev) => [
          ...prev,
          {
            id: response.data.message_id,
            sender: "assistant",
            text: response.data.response,
            sources: response.data.sources,
            confidence: response.data.confidence,
          },
        ]);
      } catch {
        setError("Failed to send message. Please try again.");
      } finally {
        setSending(false);
      }
    },
    [conversationId]
  );

  return { messages, sending, error, sendMessage };
}
