import { useEffect } from "react";
import "./Toast.css";

export default function Toast({ message, tone = "success", onDone }) {
  useEffect(() => {
    const timer = setTimeout(onDone, 3200);
    return () => clearTimeout(timer);
  }, [onDone]);

  return (
    <div className={`toast toast--${tone}`} role="status">
      {message}
    </div>
  );
}
