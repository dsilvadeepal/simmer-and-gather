import { useState } from "react";
import { Clock, ChevronDown } from "lucide-react";
import type { Task } from "./api";
export function TaskCard({
  task,
}: {
  task: Pick<
    Task,
    "title" | "minutes" | "ingredients" | "phase" | "guidance" | "evidence"
  >;
}) {
  const [open, setOpen] = useState(false);
  return (
    <article className={"task " + (task.phase === "cleanup" ? "compact" : "")}>
      <div className="row">
        <h3>{task.title.replace(/\s+and measure (?:sauce )?(?:ingredients|spices|milk\/sugar)/gi, '')}</h3>
        <span className="meta">
          <Clock size={14} />
          {task.minutes ?? "Review"} min
        </span>
      </div>
      {task.phase !== "cleanup" && (
        <>
          {(task.ingredients || []).map((x, i) => (
            <div className="ingredient" key={i}>
              <span>{x.name}</span>
              <strong>
                {x.quantity == null
                  ? "Needs review"
                  : `${x.quantity} ${x.unit || ""}`}
              </strong>
            </div>
          ))}
          {task.guidance && <details><summary>Preparation and storage notes</summary><p className="guidance">{task.guidance.replace(/CHEF PROPOSAL — untested; not a publisher storage instruction\.\s*/gi, '')}</p></details>}
          <button
            className="text-button"
            aria-expanded={open}
            onClick={() => setOpen(!open)}
          >
            Recipe details <ChevronDown size={14} />
          </button>
          {open && (
            <p className="meta">
              {task.evidence || "Source evidence needs review."}
            </p>
          )}
        </>
      )}
    </article>
  );
}
