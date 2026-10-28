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
  const fragment = new URLSearchParams(location.hash.slice(1));
  if (fragment.get('session')) {
    sessionStorage.setItem('simmer-token', fragment.get('session')!);
    history.replaceState(null, '', location.pathname);
  }
  if (sessionStorage.getItem('simmer-token')) {
    try { await api('/profile'); return; } catch { sessionStorage.removeItem('simmer-token'); }
  }
  const r = await fetch('/api/dev-session', {method:'POST'});
  if (!r.ok) throw new Error('Sign in with Google to open your private hosting plans.');
  const data = await r.json(); sessionStorage.setItem('simmer-token', data.token);
}
