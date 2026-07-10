import { LoginForm } from "../components/Auth/LoginForm";

export function LoginPage() {
  return (
    <div className="min-h-screen flex bg-background">
      {/* Left decorative panel */}
      <div className="hidden lg:flex lg:w-1/2 bg-gradient-brand flex-col justify-between p-12 relative overflow-hidden">
        <div className="absolute inset-0 opacity-10">
          {[...Array(6)].map((_, i) => (
            <div
              key={i}
              className="absolute rounded-full border border-white"
              style={{
                width: `${(i + 1) * 120}px`,
                height: `${(i + 1) * 120}px`,
                top: "50%",
                left: "50%",
                transform: "translate(-50%, -50%)",
              }}
            />
          ))}
        </div>
        <div className="relative">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 bg-white/20 rounded-lg flex items-center justify-center">
              <svg className="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                <path strokeLinecap="round" strokeLinejoin="round" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
              </svg>
            </div>
            <span className="text-white font-bold text-lg">KnowledgeAI</span>
          </div>
        </div>
        <div className="relative">
          <h2 className="text-4xl font-bold text-white leading-tight mb-4">
            Discover insights<br />from your documents
          </h2>
          <p className="text-white/70 text-lg">
            Upload, analyze, and query enterprise documents with AI-powered semantic search and conflict detection.
          </p>
          <div className="mt-8 flex gap-6">
            {[["RAG Search", "Semantic retrieval"], ["Conflict AI", "Auto-detection"], ["Summaries", "Instant insights"]].map(([title, sub]) => (
              <div key={title} className="bg-white/10 rounded-xl p-3 backdrop-blur-sm">
                <p className="text-white font-semibold text-sm">{title}</p>
                <p className="text-white/60 text-xs">{sub}</p>
              </div>
            ))}
          </div>
        </div>
        <p className="relative text-white/40 text-xs">AI Fridays Hackathon 2026</p>
      </div>

      {/* Right login panel */}
      <div className="flex-1 flex items-center justify-center p-8">
        <LoginForm />
      </div>
    </div>
  );
}
