interface SummaryCardsProps {
  documentCount: number;
  processingCount: number;
  conflictCount: number;
  pendingRecommendationCount: number;
}

const CARDS = (props: SummaryCardsProps) => [
  {
    label: "Total Documents",
    value: props.documentCount,
    sub: `${props.processingCount} processing`,
    color: "from-indigo-500 to-violet-600",
    icon: (
      <svg className="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
      </svg>
    ),
  },
  {
    label: "Conflicts Flagged",
    value: props.conflictCount,
    sub: "Needs review",
    color: "from-amber-500 to-orange-600",
    icon: (
      <svg className="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
      </svg>
    ),
  },
  {
    label: "Pending Recommendations",
    value: props.pendingRecommendationCount,
    sub: "Awaiting decision",
    color: "from-emerald-500 to-teal-600",
    icon: (
      <svg className="w-5 h-5 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={2}>
        <path strokeLinecap="round" strokeLinejoin="round" d="M9.663 17h4.673M12 3v1m6.364 1.636l-.707.707M21 12h-1M4 12H3m3.343-5.657l-.707-.707m2.828 9.9a5 5 0 117.072 0l-.548.547A3.374 3.374 0 0014 18.469V19a2 2 0 11-4 0v-.531c0-.895-.356-1.754-.988-2.386l-.548-.547z" />
      </svg>
    ),
  },
];

export function SummaryCards(props: SummaryCardsProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
      {CARDS(props).map((card) => (
        <div key={card.label} className="bg-card border border-border rounded-2xl p-5 flex items-center gap-4 hover:border-primary/40 transition">
          <div className={`w-11 h-11 rounded-xl bg-gradient-to-br ${card.color} flex items-center justify-center flex-shrink-0 shadow-lg`}>
            {card.icon}
          </div>
          <div>
            <p className="text-2xl font-bold text-white">{card.value}</p>
            <p className="text-sm text-secondary">{card.label}</p>
            <p className="text-xs text-muted">{card.sub}</p>
          </div>
        </div>
      ))}
    </div>
  );
}
