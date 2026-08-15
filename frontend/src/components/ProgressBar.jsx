import "./ProgressBar.css";

export default function ProgressBar({ value, label }) {
  const clamped = Math.min(100, Math.max(0, value));

  return (
    <div className="progress" role="progressbar" aria-valuenow={clamped} aria-valuemin={0} aria-valuemax={100}>
      <div className="progress__track">
        <div className="progress__fill" style={{ width: `${clamped}%` }} />
      </div>
      <span className="progress__label">{label}</span>
    </div>
  );
}
