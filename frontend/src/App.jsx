import Dashboard from "./pages/Dashboard.jsx";
import "./App.css";

export default function App() {
  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="app-header__brand">
          <span className="app-header__mark">▲</span>
          <div>
            <h1 className="app-header__title">Tasklane</h1>
            <p className="app-header__tagline">// task tracking, before it ships to k8s</p>
          </div>
        </div>
      </header>
      <main className="app-main">
        <Dashboard />
      </main>
    </div>
  );
}
