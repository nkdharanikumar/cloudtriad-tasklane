import { useState } from "react";
import "./Modal.css";

const emptyForm = {
  title: "",
  description: "",
  status: "TODO",
  priority: "MEDIUM",
  due_date: "",
};

export default function TaskFormModal({ task, onCancel, onSubmit }) {
  const [form, setForm] = useState(
    task
      ? {
          title: task.title || "",
          description: task.description || "",
          status: task.status || "TODO",
          priority: task.priority || "MEDIUM",
          due_date: task.due_date ? task.due_date.slice(0, 10) : "",
        }
      : emptyForm
  );
  const [formError, setFormError] = useState(null);
  const [submitting, setSubmitting] = useState(false);

  const update = (field) => (e) => setForm({ ...form, [field]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!form.title.trim()) {
      setFormError("Title is required.");
      return;
    }
    setFormError(null);
    setSubmitting(true);
    try {
      await onSubmit({ ...form, due_date: form.due_date || null });
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="modal-overlay" onMouseDown={onCancel}>
      <div
        className="modal"
        role="dialog"
        aria-modal="true"
        aria-labelledby="task-form-title"
        onMouseDown={(e) => e.stopPropagation()}
      >
        <h2 className="modal__title" id="task-form-title">
          {task ? "Edit task" : "New task"}
        </h2>

        <form onSubmit={handleSubmit} className="task-form">
          <label className="task-form__field">
            <span>Title</span>
            <input
              type="text"
              value={form.title}
              onChange={update("title")}
              placeholder="e.g. Set up Kubernetes cluster"
              autoFocus
            />
          </label>

          <label className="task-form__field">
            <span>Description</span>
            <textarea
              value={form.description}
              onChange={update("description")}
              placeholder="Optional details…"
              rows={3}
            />
          </label>

          <div className="task-form__row">
            <label className="task-form__field">
              <span>Status</span>
              <select value={form.status} onChange={update("status")}>
                <option value="TODO">To do</option>
                <option value="IN_PROGRESS">In progress</option>
                <option value="COMPLETED">Completed</option>
              </select>
            </label>

            <label className="task-form__field">
              <span>Priority</span>
              <select value={form.priority} onChange={update("priority")}>
                <option value="LOW">Low</option>
                <option value="MEDIUM">Medium</option>
                <option value="HIGH">High</option>
              </select>
            </label>
          </div>

          <label className="task-form__field">
            <span>Due date</span>
            <input type="date" value={form.due_date} onChange={update("due_date")} />
          </label>

          {formError && <p className="task-form__error">{formError}</p>}

          <div className="modal__actions">
            <button type="button" className="btn btn--secondary" onClick={onCancel}>
              Cancel
            </button>
            <button type="submit" className="btn btn--primary" disabled={submitting}>
              {submitting ? "Saving…" : task ? "Save changes" : "Create task"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
