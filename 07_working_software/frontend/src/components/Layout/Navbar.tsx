import { useAuth } from "../../hooks/useAuth";

export function Navbar() {
  const { user, logout } = useAuth();

  return (
    <header className="h-14 bg-surface border-b border-border flex items-center justify-between px-6 z-10">
      <div className="flex items-center gap-3">
        <div className="w-7 h-7 rounded-lg bg-gradient-brand flex items-center justify-center shadow-md shadow-primary/30">
          <svg className="w-4 h-4 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
        </div>
        <span className="font-bold text-white text-sm">KnowledgeAI</span>
        <span className="hidden md:block text-border text-xs">|</span>
        <span className="hidden md:block text-muted text-xs">Decision Assistant</span>
      </div>
      <div className="flex items-center gap-3">
        {user && (
          <div className="flex items-center gap-2">
            <div className="w-7 h-7 rounded-full bg-gradient-brand flex items-center justify-center text-white text-xs font-bold">
              {user.name?.charAt(0).toUpperCase()}
            </div>
            <span className="text-sm text-secondary hidden sm:block">{user.name}</span>
          </div>
        )}
        <button
          onClick={logout}
          className="text-xs text-muted hover:text-danger border border-border hover:border-danger/50 rounded-lg px-3 py-1.5 transition"
        >
          Sign out
        </button>
      </div>
    </header>
  );
}
