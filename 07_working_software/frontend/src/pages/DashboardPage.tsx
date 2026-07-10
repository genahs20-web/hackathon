import { useEffect, useState } from "react";
import { Link } from "react-router-dom";

import { SummaryCards } from "../components/Dashboard/SummaryCards";
import { UploadArea } from "../components/DocumentManager/UploadArea";
import { conflictsApi, recommendationsApi } from "../services/api";
import { useDocuments } from "../hooks/useDocuments";
import { useAuth } from "../hooks/useAuth";

export function DashboardPage() {
  const { documents, upload } = useDocuments();
  const { user } = useAuth();
  const [conflictCount, setConflictCount] = useState(0);
  const [pendingCount, setPendingCount] = useState(0);

  useEffect(() => {
    conflictsApi.list(undefined, false).then((res) => setConflictCount(res.data.length));
    recommendationsApi.list("pending").then((res) => setPendingCount(res.data.length));
  }, []);

  const processingCount = documents.filter((d) => d.status === "processing").length;

  return (
    <div className="p-6 space-y-6">
      {/* Welcome banner */}
      <div className="bg-gradient-brand rounded-2xl p-6 flex items-center justify-between shadow-lg shadow-primary/20">
        <div>
          <h1 className="text-xl font-bold text-white">
            Welcome back, {user?.name?.split(" ")[0] ?? "there"} 👋
          </h1>
          <p className="text-white/70 text-sm mt-1">
            Your AI knowledge workspace is ready. Upload documents or start a conversation.
          </p>
        </div>
        <div className="hidden md:flex gap-3">
          <Link
            to="/documents"
            className="bg-white/20 hover:bg-white/30 text-white text-sm font-medium px-4 py-2 rounded-xl transition backdrop-blur-sm"
          >
            Upload Docs
          </Link>
          <Link
            to="/chat"
            className="bg-white text-black text-sm font-semibold px-4 py-2 rounded-xl hover:bg-white/90 transition"
          >
            Start Chat →
          </Link>
        </div>
      </div>

      {/* Stats */}
      <SummaryCards
        documentCount={documents.length}
        processingCount={processingCount}
        conflictCount={conflictCount}
        pendingRecommendationCount={pendingCount}
      />

      {/* Quick upload + quick links */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="bg-card border border-border rounded-2xl p-5">
          <h2 className="text-sm font-semibold text-white mb-4 flex items-center gap-2">
            <svg className="w-4 h-4 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
            </svg>
            Quick Upload
          </h2>
          <UploadArea onUpload={(file) => upload(file)} />
        </div>

        <div className="bg-card border border-border rounded-2xl p-5">
          <h2 className="text-sm font-semibold text-white mb-4 flex items-center gap-2">
            <svg className="w-4 h-4 text-primary" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
              <path strokeLinecap="round" strokeLinejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" />
            </svg>
            Quick Actions
          </h2>
          <div className="space-y-2">
            {[
              { to: "/chat", label: "Ask a question", sub: "Chat with your documents", color: "text-accent" },
              { to: "/conflicts", label: "Review conflicts", sub: `${conflictCount} flagged items`, color: "text-warning" },
              { to: "/recommendations", label: "View recommendations", sub: `${pendingCount} pending`, color: "text-success" },
              { to: "/documents", label: "Manage documents", sub: `${documents.length} total`, color: "text-secondary" },
            ].map((item) => (
              <Link
                key={item.to}
                to={item.to}
                className="flex items-center justify-between p-3 rounded-xl hover:bg-surface transition group"
              >
                <div>
                  <p className={`text-sm font-medium ${item.color}`}>{item.label}</p>
                  <p className="text-xs text-muted">{item.sub}</p>
                </div>
                <svg className="w-4 h-4 text-muted group-hover:text-secondary transition" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
                  <path strokeLinecap="round" strokeLinejoin="round" d="M9 5l7 7-7 7" />
                </svg>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}
