import type { components } from "./schema";
export type Gathering = components["schemas"]["Gathering"];
export type Workspace = components["schemas"]["Workspace"];
export type Selection = components["schemas"]["MenuSelection"];
export type Recipe = components["schemas"]["RecipeSnapshot"];
export type Plan = components["schemas"]["PlanCandidate"];
export type Task = components["schemas"]["PrepTask"];
export type Inputs = components["schemas"]["PlanInputs"];
export async function api<T>(
  path: string,
  body?: unknown,
  method?: string,
): Promise<T> {
  const r = await fetch("/api" + path, {
    method: method || (body === undefined ? "GET" : "POST"),
    headers: {
      "Content-Type": "application/json",
      Authorization: "Bearer " + (sessionStorage.getItem("simmer-token") || ""),
    },
    ...(body === undefined ? {} : { body: JSON.stringify(body) }),
  });
  if (!r.ok) {
    const data = await r.json().catch(() => ({}));
    throw new Error(
      typeof data.detail === "string"
        ? data.detail
        : `Request failed (${r.status}). Your saved work is preserved.`,
    );
  }
  return r.json();
}
export async function localLogin() {
  const r = await fetch("/api/dev-session", { method: "POST" });
  if (!r.ok)
    throw new Error(
      "Sign in is required. Hosted authentication setup is pending.",
    );
  const d = await r.json();
  sessionStorage.setItem("simmer-token", d.token);
}
