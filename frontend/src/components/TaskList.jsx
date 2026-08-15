import TaskCard from "./TaskCard.jsx";
import "./TaskList.css";

export default function TaskList({ tasks, loading, onEdit, onDelete, onStatusChange, hasFilters }) {
  if (loading) {
    return (
      <div className="task-list__state">
        <p>Loading tasks…</p>
      </div>
    );
  }

  if (tasks.length === 0) {
    return (
      <div className="task-list__state">
        <p className="task-list__state-title">
          {hasFilters ? "No tasks match your filters" : "No tasks yet"}
        </p>
        <p className="task-list__state-detail">
          {hasFilters
            ? "Try clearing a filter or searching for something else."
            : "Create your first task to get started."}
        </p>
      </div>
    );
  }

  return (
    <div className="task-list">
      {tasks.map((task) => (
        <TaskCard
          key={task.id}
          task={task}
          onEdit={() => onEdit(task)}
          onDelete={() => onDelete(task)}
          onStatusChange={(status) => onStatusChange(task, status)}
        />
      ))}
    </div>
  );
}
