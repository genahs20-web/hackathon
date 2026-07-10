import { Link } from "react-router-dom";

export function NotFoundPage() {
  return (
    <div className="min-h-screen flex flex-col items-center justify-center gap-4">
      <h1 className="text-3xl font-bold text-primary">404 — Page Not Found</h1>
      <Link to="/" className="text-accent">
        Return to Dashboard
      </Link>
    </div>
  );
}
