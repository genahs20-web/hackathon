import { useEffect, useState } from "react";

import { RecommendationCard } from "../components/RecommendationCard";
import { recommendationsApi, type RecommendationDto } from "../services/api";

const STATUS_FILTERS = ["all", "pending", "approved", "rejected"] as const;

export function RecommendationsPage() {
  const [recommendations, setRecommendations] = useState<RecommendationDto[]>([]);
  const [filter, setFilter] = useState<(typeof STATUS_FILTERS)[number]>("all");

  async function refresh() {
    const statusFilter = filter === "all" ? undefined : filter;
    const response = await recommendationsApi.list(statusFilter);
    setRecommendations(response.data);
  }

  useEffect(() => {
    refresh();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [filter]);

  async function handleApprove(id: string) {
    await recommendationsApi.patch(id, "approved");
    await refresh();
  }

  async function handleReject(id: string, reason: string) {
    await recommendationsApi.patch(id, "rejected", reason);
    await refresh();
  }

  return (
    <div className="p-6 space-y-4">
      <h1 className="text-2xl font-bold text-primary">AI Recommendations</h1>
      <div className="flex gap-2">
        {STATUS_FILTERS.map((s) => (
          <button
            key={s}
            onClick={() => setFilter(s)}
            className={`px-3 py-1.5 rounded-md text-sm ${
              filter === s ? "bg-primary text-white" : "bg-card border border-slate-200 text-secondary"
            }`}
          >
            {s === "all" ? "All" : s.charAt(0).toUpperCase() + s.slice(1)}
          </button>
        ))}
      </div>
      <div className="space-y-3">
        {recommendations.map((rec) => (
          <RecommendationCard
            key={rec.recommendation_id}
            recommendation={rec}
            onApprove={handleApprove}
            onReject={handleReject}
          />
        ))}
        {recommendations.length === 0 && <p className="text-secondary text-sm">No recommendations found.</p>}
      </div>
    </div>
  );
}
