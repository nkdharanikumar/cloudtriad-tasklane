import ProgressBar from "./ProgressBar.jsx";
import "./StatsBar.css";

const CARDS = [
  { key: "total_tasks", label: "Total tasks", accent: "var(--text-primary)" },
  { key: "pending_tasks", label: "Pending", accent: "var(--status-todo)" },
  { key: "in_progress_tasks", label: "In progress", accent: "var(--status-progress)" },
  { key: "completed_tasks", label: "Completed", accent: "var(--status-completed)" },
];

export default function StatsBar({ stats }) {
  return (
    <section className="stats-bar" aria-label="Task summary">
      <div className="stats-bar__cards">
        {CARDS.map((card) => (
          <div className="stat-card" key={card.key}>
            <span className="stat-card__label">{card.label}</span>
            <span className="stat-card__value" style={{ color: card.accent }}>
              {stats ? stats[card.key] : "—"}
            </span>
          </div>
        ))}
      </div>
      <ProgressBar
        value={stats?.completion_rate ?? 0}
        label={stats ? `${stats.completion_rate}% complete` : "Loading…"}
      />
    </section>
  );
}
