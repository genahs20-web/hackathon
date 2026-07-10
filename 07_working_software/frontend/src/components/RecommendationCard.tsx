import { useState } from "react";

import type { RecommendationDto } from "../services/api";
import { RECOMMENDATION_STATUS_COLORS } from "../utils/constants";
import { formatConfidence } from "../utils/formatters";

interface RecommendationCardProps {
  recommendation: RecommendationDto;
  onApprove: (id: string) => void;
  onReject: (id: string, reason: string) => void;
}

export function RecommendationCard({ recommendation, onApprove, onReject }: RecommendationCardProps) {
  const [rejecting, setRejecting] = useState(false);
  const [reason, setReason] = useState("");

  return (
    <div className="bg-card border border-slate-200 rounded-lg p-4">
      <div className="flex justify-between items-start">
        <p className="text-sm">{recommendation.recommendation_text}</p>
        <span className={`px-2 py-1 rounded text-xs shrink-0 ml-2 ${RECOMMENDATION_STATUS_COLORS[recommendation.status]}`}>
          {recommendation.status}
        </span>
      </div>

      <div className="mt-2 h-2 bg-slate-100 rounded">
        <div
          className="h-2 bg-accent rounded"
          style={{ width: `${Math.round(recommendation.confidence_score * 100)}%` }}
        />
      </div>
      <p className="text-xs text-secondary mt-1">Confidence: {formatConfidence(recommendation.confidence_score)}</p>

      {recommendation.status === "pending" && (
        <div className="flex gap-2 mt-3">
          <button
            onClick={() => onApprove(recommendation.recommendation_id)}
            className="text-success text-sm font-medium"
          >
            Approve
          </button>
          <button onClick={() => setRejecting(true)} className="text-danger text-sm font-medium">
            Reject
          </button>
        </div>
      )}

      {rejecting && (
        <div className="mt-2">
          <textarea
            value={reason}
            onChange={(e) => setReason(e.target.value)}
            placeholder="Reason for rejection..."
            className="w-full border border-slate-300 rounded-md p-2 text-sm"
          />
          <button
            onClick={() => {
              onReject(recommendation.recommendation_id, reason);
              setRejecting(false);
            }}
            disabled={!reason.trim()}
            className="mt-1 text-sm bg-danger text-white px-3 py-1 rounded-md disabled:opacity-50"
          >
            Confirm Reject
          </button>
        </div>
      )}
    </div>
  );
}
