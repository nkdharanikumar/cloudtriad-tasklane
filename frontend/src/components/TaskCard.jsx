import "./TaskCard.css";

const PRIORITY_LABEL = {
  LOW: "Low",
  MEDIUM: "Medium",
  HIGH: "High",
};

function formatDate(dateStr) {
  if (!dateStr) return null;
  const d = new Date(dateStr);
  if (Number.isNaN(d.getTime())) return dateStr;
  return d.toLocaleDateString(undefined, { month: "short", day: "numeric", year: "numeric" });
}

export default function TaskCard({ task, onEdit, onDelete, onStatusChange }) {
  const isOverdue =
    task.due_date && task.status !== "COMPLETED" && new Date(task.due_date) < new Date(new Date().toDateString());

  return (
    <article className={`task-card priority-${task.priority.toLowerCase()}`}>
      <div className="task-card__edge" />
      <div className="task-card__body">
        <div className="task-card__top">
          <h3 className="task-card__title">{task.title}</h3>
          <div className="task-card__actions">
            <button className="icon-btn" onClick={onEdit} aria-label={`Edit ${task.title}`} title="Edit">
              ✎
            </button>
            <button className="icon-btn icon-btn--danger" onClick={onDelete} aria-label={`Delete ${task.title}`} title="Delete">
              ✕
            </button>
          </div>
        </div>

        {task.description && <p className="task-card__description">{task.description}</p>}

        <div className="task-card__meta">
          <span className={`badge badge--priority-${task.priority.toLowerCase()}`}>
            {PRIORITY_LABEL[task.priority]}
          </span>
          {task.due_date && (
            <span className={`task-card__due ${isOverdue ? "task-card__due--overdue" : ""}`}>
              due {formatDate(task.due_date)}
            </span>
          )}
        </div>

        <div className="task-card__footer">
          <span className={`status-dot status-dot--${task.status.toLowerCase()}`} aria-hidden="true" />
          <select
            className="task-card__status-select"
            value={task.status}
            onChange={(e) => onStatusChange(e.target.value)}
            aria-label={`Change status for ${task.title}`}
          >
            <option value="TODO">TODO</option>
            <option value="IN_PROGRESS">IN_PROGRESS</option>
            <option value="COMPLETED">COMPLETED</option>
          </select>
        </div>
      </div>
    </article>
  );
}
