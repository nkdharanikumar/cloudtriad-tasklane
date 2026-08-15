import { useCallback, useEffect, useState } from "react";
import { api, ApiError } from "../services/api.js";
import StatsBar from "../components/StatsBar.jsx";
import FilterBar from "../components/FilterBar.jsx";
import TaskList from "../components/TaskList.jsx";
import TaskFormModal from "../components/TaskFormModal.jsx";
import ConfirmDialog from "../components/ConfirmDialog.jsx";
import Toast from "../components/Toast.jsx";
import "./Dashboard.css";

const DEFAULT_FILTERS = { status: "", priority: "", search: "" };

export default function Dashboard() {
  const [tasks, setTasks] = useState([]);
  const [stats, setStats] = useState(null);
  const [filters, setFilters] = useState(DEFAULT_FILTERS);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [toast, setToast] = useState(null);

  const [formOpen, setFormOpen] = useState(false);
  const [editingTask, setEditingTask] = useState(null);
  const [pendingDelete, setPendingDelete] = useState(null);

  const showToast = (message, tone = "success") => {
    setToast({ message, tone, id: Date.now() });
  };

  const loadStats = useCallback(async () => {
    try {
      const data = await api.getStats();
      setStats(data);
    } catch {
      // Stats are secondary - don't block the whole dashboard on this.
    }
  }, []);

  const loadTasks = useCallback(async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await api.getTasks(filters);
      setTasks(data);
    } catch (err) {
      const message =
        err instanceof ApiError ? err.message : "Something went wrong loading tasks.";
      setError(message);
    } finally {
      setLoading(false);
    }
  }, [filters]);

  useEffect(() => {
    loadTasks();
  }, [loadTasks]);

  useEffect(() => {
    loadStats();
  }, [loadStats]);

  const refreshAll = () => {
    loadTasks();
    loadStats();
  };

  const handleCreateClick = () => {
    setEditingTask(null);
    setFormOpen(true);
  };

  const handleEditClick = (task) => {
    setEditingTask(task);
    setFormOpen(true);
  };

  const handleFormSubmit = async (payload) => {
    try {
      if (editingTask) {
        await api.updateTask(editingTask.id, payload);
        showToast("Task updated.");
      } else {
        await api.createTask(payload);
        showToast("Task created.");
      }
      setFormOpen(false);
      setEditingTask(null);
      refreshAll();
    } catch (err) {
      const message = err instanceof ApiError ? err.message : "Could not save the task.";
      showToast(message, "error");
    }
  };

  const handleStatusChange = async (task, status) => {
    try {
      await api.updateTask(task.id, { status });
      refreshAll();
    } catch (err) {
      const message = err instanceof ApiError ? err.message : "Could not update status.";
      showToast(message, "error");
    }
  };

  const handleDeleteConfirm = async () => {
    if (!pendingDelete) return;
    try {
      await api.deleteTask(pendingDelete.id);
      showToast("Task deleted.");
      setPendingDelete(null);
      refreshAll();
    } catch (err) {
      const message = err instanceof ApiError ? err.message : "Could not delete the task.";
      showToast(message, "error");
      setPendingDelete(null);
    }
  };

  return (
    <>
      <StatsBar stats={stats} />

      <FilterBar
        filters={filters}
        onFiltersChange={setFilters}
        onNewTask={handleCreateClick}
      />

      {error ? (
        <div className="dashboard-error">
          <p className="dashboard-error__title">Couldn&apos;t load tasks</p>
          <p className="dashboard-error__detail">{error}</p>
          <button className="btn btn--secondary" onClick={loadTasks}>
            Try again
          </button>
        </div>
      ) : (
        <TaskList
          tasks={tasks}
          loading={loading}
          onEdit={handleEditClick}
          onDelete={setPendingDelete}
          onStatusChange={handleStatusChange}
          hasFilters={Boolean(filters.status || filters.priority || filters.search)}
        />
      )}

      {formOpen && (
        <TaskFormModal
          task={editingTask}
          onCancel={() => {
            setFormOpen(false);
            setEditingTask(null);
          }}
          onSubmit={handleFormSubmit}
        />
      )}

      {pendingDelete && (
        <ConfirmDialog
          title="Delete task?"
          message={`This will permanently delete "${pendingDelete.title}".`}
          confirmLabel="Delete"
          tone="danger"
          onCancel={() => setPendingDelete(null)}
          onConfirm={handleDeleteConfirm}
        />
      )}

      {toast && (
        <Toast key={toast.id} message={toast.message} tone={toast.tone} onDone={() => setToast(null)} />
      )}
    </>
  );
}
