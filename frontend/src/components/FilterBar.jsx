import "./FilterBar.css";

export default function FilterBar({ filters, onFiltersChange, onNewTask }) {
  const update = (field) => (event) => {
    onFiltersChange({ ...filters, [field]: event.target.value });
  };

  const hasActiveFilters = filters.status || filters.priority || filters.search;

  return (
    <section className="filter-bar" aria-label="Filter tasks">
      <div className="filter-bar__search">
        <span className="filter-bar__search-icon">⌕</span>
        <input
          type="text"
          placeholder="Search tasks by title or description…"
          value={filters.search}
          onChange={update("search")}
          aria-label="Search tasks"
        />
      </div>

      <select value={filters.status} onChange={update("status")} aria-label="Filter by status">
        <option value="">All statuses</option>
        <option value="TODO">To do</option>
        <option value="IN_PROGRESS">In progress</option>
        <option value="COMPLETED">Completed</option>
      </select>

      <select value={filters.priority} onChange={update("priority")} aria-label="Filter by priority">
        <option value="">All priorities</option>
        <option value="LOW">Low</option>
        <option value="MEDIUM">Medium</option>
        <option value="HIGH">High</option>
      </select>

      {hasActiveFilters && (
        <button
          className="btn btn--ghost"
          onClick={() => onFiltersChange({ status: "", priority: "", search: "" })}
        >
          Clear
        </button>
      )}

      <button className="btn btn--primary filter-bar__new" onClick={onNewTask}>
        + New task
      </button>
    </section>
  );
}
