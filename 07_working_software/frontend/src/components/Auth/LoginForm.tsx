import { useState } from "react";
import { useAuth } from "../../hooks/useAuth";
import { validateEmail } from "../../utils/validators";

export function LoginForm() {
  const { login } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    const emailError = validateEmail(email);
    if (emailError) { setError(emailError); return; }
    setSubmitting(true);
    setError(null);
    try {
      await login(email, password);
      window.location.href = "/";
    } catch {
      setError("Invalid email or password");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="w-full max-w-md">
      {/* Logo / Brand */}
      <div className="text-center mb-8">
        <div className="inline-flex items-center justify-center w-14 h-14 rounded-2xl bg-gradient-brand mb-4 shadow-lg shadow-primary/30">
          <svg className="w-7 h-7 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
            <path strokeLinecap="round" strokeLinejoin="round" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
          </svg>
        </div>
        <h1 className="text-2xl font-bold text-white">AI Knowledge Assistant</h1>
        <p className="text-muted text-sm mt-1">Sign in to your workspace</p>
      </div>

      <form onSubmit={handleSubmit} className="bg-card border border-border rounded-2xl p-8 shadow-2xl shadow-black/40">
        <div className="mb-5">
          <label className="block text-xs font-semibold text-secondary uppercase tracking-wider mb-2" htmlFor="email">
            Email Address
          </label>
          <input
            id="email"
            type="email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            onBlur={() => setError(validateEmail(email))}
            placeholder="analyst@acme.com"
            className="w-full h-11 px-4 bg-surface border border-border rounded-xl text-white placeholder-muted focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition"
          />
        </div>

        <div className="mb-6">
          <label className="block text-xs font-semibold text-secondary uppercase tracking-wider mb-2" htmlFor="password">
            Password
          </label>
          <div className="relative">
            <input
              id="password"
              type={showPassword ? "text" : "password"}
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="••••••••"
              className="w-full h-11 px-4 bg-surface border border-border rounded-xl text-white placeholder-muted focus:outline-none focus:border-primary focus:ring-1 focus:ring-primary transition"
            />
            <button
              type="button"
              onClick={() => setShowPassword((v) => !v)}
              className="absolute right-3 top-3 text-muted hover:text-secondary transition text-xs"
            >
              {showPassword ? "Hide" : "Show"}
            </button>
          </div>
        </div>

        {error && (
          <div className="flex items-center gap-2 bg-danger/10 border border-danger/30 rounded-lg px-3 py-2 mb-4">
            <svg className="w-4 h-4 text-danger flex-shrink-0" fill="currentColor" viewBox="0 0 20 20">
              <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7 4a1 1 0 11-2 0 1 1 0 012 0zm-1-9a1 1 0 00-1 1v4a1 1 0 102 0V6a1 1 0 00-1-1z" clipRule="evenodd" />
            </svg>
            <p className="text-danger text-sm">{error}</p>
          </div>
        )}

        <button
          type="submit"
          disabled={submitting}
          className="w-full h-11 bg-gradient-brand text-white rounded-xl font-semibold shadow-lg shadow-primary/30 hover:opacity-90 disabled:opacity-50 transition"
        >
          {submitting ? "Signing in..." : "Sign In →"}
        </button>

        <p className="text-center text-xs text-muted mt-4">
          Demo: <span className="text-secondary">analyst@acme.com</span> / <span className="text-secondary">Password123</span>
        </p>
      </form>
    </div>
  );
}
