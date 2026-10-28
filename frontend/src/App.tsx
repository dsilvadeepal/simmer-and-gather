import { useEffect, useState } from "react";
import {
  CalendarDays,
  Clock,
  Users,
  Leaf,
  ShoppingBag,
  ChefHat,
  Star,
  Plus,
  RefreshCw,
  Utensils,
  Flame,
  ArrowRight,
} from "lucide-react";
import {
  api,
  localLogin,
  type Workspace,
  type Gathering,
  type Inputs,
  type Plan,
  type Recipe,
  type Selection,
} from "./api";
import { TaskCard } from "./TaskCard";
const categories = ["starters", "mains", "sides", "desserts", "drinks"];
function localDate(value?: string | null) {
  if (!value) return "";
  const d = new Date(value);
  return new Date(d.getTime() - d.getTimezoneOffset() * 60000)
    .toISOString()
    .slice(0, 16);
}
function iso(value: string) {
  return new Date(value).toISOString();
}
function daysBetween(start: string, end: string) {
  let days: string[] = [];
  let d = new Date(start + "T12:00:00");
  const last = new Date(end + "T12:00:00");
  while (d <= last && days.length < 21) {
    days.push(
      `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`,
    );
    d.setDate(d.getDate() + 1);
  }
  return days;
}
export default function App() {
  const [ws, setWs] = useState<Workspace | null>(null),
    [g, setG] = useState<Gathering | null>(null),
    [step, setStep] = useState(0),
    [error, setError] = useState(""),
    [notice, setNotice] = useState(""),
    [loading, setLoading] = useState(false),
    [dirty, setDirty] = useState(false),
    [plan, setPlan] = useState<Plan | null>(null),
    [source, setSource] = useState(""),
    [preview, setPreview] = useState<Recipe | null>(null),
    [reviewJson, setReviewJson] = useState(""),
    [inventory, setInventory] = useState(""),
    [approval, setApproval] = useState<string | null>(null),
    [booking, setBooking] = useState<{
      outcomes: { status: string; title?: string }[];
    } | null>(null);
  async function run(action: () => Promise<void>) {
    setLoading(true);
    setError("");
    setNotice("");
    try {
      await action();
    } catch (e) {
      setError(e instanceof Error ? e.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
  }
  async function load(id: string) {
    const data = await api<Workspace>("/workspace/" + id);
    setWs(data);
    setG(data.inputs.gathering);
    setPlan(data.plan || null);
    setDirty(false);
    setApproval(null);
  }
  useEffect(() => {
    run(async () => {
      await localLogin();
      let gs = await api<Gathering[]>("/gatherings");
      if (!gs.length) {
        const created = await api<Gathering>("/gatherings", {
          gathering: { title: "My gathering" },
        });
        gs = [created];
      }
      await load(gs[0].id!);
    });
  }, []);
  function change(values: Partial<Gathering>) {
    setG((prev) => (prev ? { ...prev, ...values } : prev));
    setDirty(true);
    setApproval(null);
  }
  async function save() {
    if (!g) return;
    const saved = await api<Gathering>("/gatherings", {
      gathering: g,
      expected_revision: g.revision,
    });
    await load(saved.id!);
    setNotice("Saved");
  }
  async function edit(changes: unknown[]) {
    if (!g) return;
    if (dirty) throw new Error("Save your gathering changes first.");
    const result = await api<Inputs>("/menu/" + g.id, {
      expected_revision: g.revision,
      changes,
    });
    await load(result.gathering.id!);
    setNotice("Saved");
  }
  const time = (value: string) =>
    new Date(value).toLocaleTimeString([], {
      hour: "numeric",
      minute: "2-digit",
    });
  if (!g || !ws)
    return (
      <main className="shell">
        <p className="brand">♧ Simmer and Gather</p>
        <h1>Your hosting plans, together.</h1>
        <p>{error || "Opening your saved gathering…"}</p>
        {error && <><a className="login-link" href="/api/google/start">Sign in with Google</a><button onClick={() => location.reload()}>Try again</button></>}
      </main>
    );
  const profile = g.profile || {
    timezone: "America/New_York",
    weekday_minutes: 60,
    weekend_minutes: 120,
    protected: [],
    equipment: {},
    helpers: [],
  };
  const selected = g.prep_days || [];
  const prepDays = daysBetween(
    g.earliest_prep || localDate(g.arrival).slice(0, 10),
    localDate(g.arrival).slice(0, 10),
  );
  const limit = (day: string) =>
    g.daily_limits?.[day] ??
    (new Date(day + "T12:00:00").getDay() % 6 === 0
      ? (g.profile?.weekend_minutes ?? 120)
      : (g.profile?.weekday_minutes ?? 60));
  const updateItem = (s: Selection, values: Partial<Selection>) =>
    run(() => edit([{ action: "update", id: s.id, values }]));
  return (
    <div className="shell">
      <header>
        <a className="brand" href="#">
          ♧{" "}
          <span>
            Simmer <i>and</i> Gather
          </span>
        </a>
        <span className="meta">A little prep. More time together.</span>
      </header>
      {ws.fixture_mode && (
        <div className="demo-banner">
          Local demo · sample recipes and calendar availability. Illustrative
          quantities and storage guidance—not instructions for cooking. No live
          calendar writes.
        </div>
      )}
      <nav aria-label="Planning steps">
        {["Gathering", "Menu", "Prep plan"].map((s, i) => (
          <button
            className={step === i ? "active" : ""}
            key={s}
            onClick={() => setStep(i)}
          >
            {i + 1} {s}
          </button>
        ))}
      </nav>
      {error && (
        <div role="alert" className="alert">
          {error}
        </div>
      )}
      {notice && (
        <div role="status" className="notice">
          {notice}
        </div>
      )}
      {loading && (
        <div role="status" className="notice">
          Working…
        </div>
      )}
      {step === 0 && (
        <>
          <div className="intro">
            <p className="eyebrow">YOUR GATHERING</p>
            <h1>Make room for the gathering.</h1>
            <p>
              Start with the people, the time you have, and the evening you
              want.
            </p>
          </div>
          <div className="grid">
            <section className="card">
              <h2>
                <Users />
                The occasion
              </h2>
              <label>
                Gathering name
                <input
                  value={g.title || ""}
                  onChange={(e) => change({ title: e.target.value })}
                />
              </label>
              <div className="fields">
                <label>
                  Occasion
                  <select
                    value={g.occasion}
                    onChange={(e) => change({ occasion: e.target.value })}
                  >
                    {[
                      "Diwali",
                      "Thanksgiving",
                      "Christmas",
                      "Birthday",
                      "Other",
                    ].map((x) => (
                      <option key={x}>{x}</option>
                    ))}
                  </select>
                </label>
                <label>
                  Guests arrive
                  <input
                    type="datetime-local"
                    value={localDate(g.arrival)}
                    onChange={(e) =>
                      e.target.value && change({ arrival: iso(e.target.value) })
                    }
                  />
                </label>
                <label>
                  Guests
                  <input
                    type="number"
                    min="1"
                    max="100"
                    value={g.guests}
                    onChange={(e) => change({ guests: +e.target.value })}
                  />
                </label>
                <label>
                  Vegetarian guests
                  <input
                    type="number"
                    min="0"
                    max={g.guests}
                    value={g.vegetarian_guests}
                    onChange={(e) =>
                      change({ vegetarian_guests: +e.target.value })
                    }
                  />
                </label>
              </div>
              <label>
                Allergies (comma separated; leave blank for none)
                <input
                  value={(g.allergies || []).join(", ")}
                  onChange={(e) =>
                    change({
                      allergies: e.target.value
                        .split(",")
                        .map((x) => x.trim())
                        .filter(Boolean),
                    })
                  }
                />
              </label>
              <label>
                Preferences
                <input
                  value={(g.preferences || []).join(", ")}
                  onChange={(e) =>
                    change({
                      preferences: e.target.value
                        .split(",")
                        .map((x) => x.trim())
                        .filter(Boolean),
                    })
                  }
                />
              </label>
            </section>
            <section className="card">
              <h2>
                <CalendarDays />
                Your prep days
              </h2>
              <label>
                I can start preparing on
                <input
                  type="date"
                  value={g.earliest_prep || ""}
                  onChange={(e) => change({ earliest_prep: e.target.value })}
                />
              </label>
              <p className="meta">
                Choose the days that work. Daily totals include cleanup and
                supervision.
              </p>
              {prepDays.map((day) => (
                <div className="day" key={day}>
                  <label className="check">
                    <input
                      type="checkbox"
                      checked={selected.includes(day)}
                      onChange={(e) =>
                        change({
                          prep_days: e.target.checked
                            ? [...selected, day]
                            : selected.filter((x) => x !== day),
                        })
                      }
                    />
                    {new Date(day + "T12:00:00").toLocaleDateString([], {
                      weekday: "short",
                      month: "short",
                      day: "numeric",
                    })}
                  </label>
                  <label className="minutes">
                    Daily minutes
                    <input
                      aria-label={"Daily minutes " + day}
                      type="number"
                      min="0"
                      max="1440"
                      value={limit(day)}
                      onChange={(e) =>
                        change({
                          daily_limits: {
                            ...g.daily_limits,
                            [day]: +e.target.value,
                          },
                        })
                      }
                    />
                  </label>
                </div>
              ))}
              <p className="total">
                {selected.reduce((a, d) => a + limit(d), 0)} minutes allowed ·
                calendar availability may be less
              </p>
            </section>
            <section className="card">
              <h2>
                <Clock />
                Make time to relax
              </h2>
              <div className="fields">
                <label>
                  Finish major cooking before arrival (minutes)
                  <input
                    type="number"
                    min="0"
                    value={g.relax_minutes}
                    onChange={(e) => change({ relax_minutes: +e.target.value })}
                  />
                </label>
                <label>
                  Small finishing tasks within that time (minutes)
                  <input
                    type="number"
                    min="0"
                    value={g.finishing_minutes}
                    onChange={(e) =>
                      change({ finishing_minutes: +e.target.value })
                    }
                  />
                </label>
              </div>
              <p className="meta">
                The remaining{" "}
                {Math.max(
                  0,
                  (g.relax_minutes || 0) - (g.finishing_minutes || 0),
                )}{" "}
                minutes stay free for you.
              </p>
              <h3>Possible prep windows</h3>
              {(g.prep_windows || []).map((w, i) => (
                <div className="fields" key={i}>
                  <label>
                    Start
                    <input
                      type="datetime-local"
                      value={localDate(w.start)}
                      onChange={(e) =>
                        e.target.value &&
                        change({
                          prep_windows: g.prep_windows!.map((v, j) =>
                            j === i ? { ...v, start: iso(e.target.value) } : v,
                          ),
                        })
                      }
                    />
                  </label>
                  <label>
                    End
                    <input
                      type="datetime-local"
                      value={localDate(w.end)}
                      onChange={(e) =>
                        e.target.value &&
                        change({
                          prep_windows: g.prep_windows!.map((v, j) =>
                            j === i ? { ...v, end: iso(e.target.value) } : v,
                          ),
                        })
                      }
                    />
                  </label>
                  <button
                    className="text-button"
                    onClick={() =>
                      change({
                        prep_windows: g.prep_windows!.filter((_, j) => j !== i),
                      })
                    }
                  >
                    Remove window
                  </button>
                </div>
              ))}
              <button
                className="secondary"
                onClick={() => {
                  const day = selected[0] || g.earliest_prep;
                  if (day)
                    change({
                      prep_windows: [
                        ...(g.prep_windows || []),
                        {
                          start: iso(day + "T18:00"),
                          end: iso(day + "T19:00"),
                        },
                      ],
                    });
                }}
              >
                <Plus size={16} />
                Add prep window
              </button>
            </section>
            <section className="card">
              <h2>
                <Flame />
                Kitchen & helpers
              </h2>
              <div className="fields">
                {["oven", "stovetop", "air fryer", "instant pot"].map(
                  (name) => (
                    <label key={name}>
                      {name} capacity
                      <input
                        type="number"
                        min="0"
                        placeholder="Needs review"
                        value={g.profile?.equipment?.[name] ?? ""}
                        onChange={(e) =>
                          change({
                            profile: {
                              ...profile,
                              equipment: {
                                ...g.profile?.equipment,
                                [name]:
                                  e.target.value === ""
                                    ? null
                                    : +e.target.value,
                              },
                            },
                          })
                        }
                      />
                    </label>
                  ),
                )}
              </div>
              <p className="meta">
                Capacity means simultaneous batches or burners. Zero means
                unavailable.
              </p>
              {(g.profile?.helpers || []).map((h, i) => (
                <div className="helper" key={h.id}>
                  <label>
                    Helper name
                    <input
                      value={h.name}
                      onChange={(e) =>
                        change({
                          profile: {
                            ...profile,
                            helpers: g.profile!.helpers!.map((x, j) =>
                              j === i ? { ...x, name: e.target.value } : x,
                            ),
                          },
                        })
                      }
                    />
                  </label>
                  <label>
                    Capabilities (comma separated)
                    <input
                      value={(h.skills || []).join(", ")}
                      onChange={(e) =>
                        change({
                          profile: {
                            ...profile,
                            helpers: g.profile!.helpers!.map((x, j) =>
                              j === i
                                ? {
                                    ...x,
                                    skills: e.target.value
                                      .split(",")
                                      .map((v) => v.trim()),
                                  }
                                : x,
                            ),
                          },
                        })
                      }
                    />
                  </label>
                  <label className="check">
                    <input
                      type="checkbox"
                      checked={h.supervision}
                      onChange={(e) =>
                        change({
                          profile: {
                            ...profile,
                            helpers: g.profile!.helpers!.map((x, j) =>
                              j === i
                                ? { ...x, supervision: e.target.checked }
                                : x,
                            ),
                          },
                        })
                      }
                    />
                    Needs supervision
                  </label>
                  <p className="meta">
                    {h.available?.length || 0} available windows
                  </p>
                  <button
                    className="secondary"
                    onClick={() => {
                      const start = prompt(
                        "Availability start (e.g. 2026-11-06T18:00)",
                      );
                      const end =
                        start &&
                        prompt("Availability end (e.g. 2026-11-06T18:30)");
                      if (start && end)
                        change({
                          profile: {
                            ...profile,
                            helpers: g.profile!.helpers!.map((x, j) =>
                              j === i
                                ? {
                                    ...x,
                                    available: [
                                      ...(x.available || []),
                                      { start: iso(start), end: iso(end) },
                                    ],
                                  }
                                : x,
                            ),
                          },
                        });
                    }}
                  >
                    Add availability
                  </button>
                  <button
                    className="text-button"
                    onClick={() =>
                      change({
                        profile: {
                          ...profile,
                          helpers: g.profile!.helpers!.map((x, j) =>
                            j === i ? { ...x, available: [] } : x,
                          ),
                        },
                      })
                    }
                  >
                    Clear availability
                  </button>
                </div>
              ))}
              <button
                className="secondary"
                onClick={() =>
                  change({
                    profile: {
                      ...profile,
                      helpers: [
                        ...(g.profile?.helpers || []),
                        {
                          id: crypto.randomUUID(),
                          name: "Helper",
                          skills: ["measure"],
                          available: [],
                          supervision: false,
                        },
                      ],
                    },
                  })
                }
              >
                <Users size={16} />
                Add helper
              </button>
            </section>
            <section className="card full">
              <h2>
                <CalendarDays />
                Calendars & protected time
              </h2>
              <label>
                Calendar IDs to check
                <input
                  placeholder="Connect Google Calendar during setup"
                  value={(g.selected_calendars || []).join(", ")}
                  onChange={(e) =>
                    change({
                      selected_calendars: e.target.value
                        .split(",")
                        .map((x) => x.trim())
                        .filter(Boolean),
                    })
                  }
                />
              </label>
              <p className="meta">
                Work, family and sleep remain protected even when a calendar
                looks free.
              </p>
              {(g.profile?.protected || []).map((w, i) => (
                <div className="row" key={i}>
                  <span>
                    {new Date(w.start).toLocaleString()} – {time(w.end)}
                  </span>
                  <button
                    className="text-button"
                    onClick={() =>
                      change({
                        profile: {
                          ...profile,
                          protected: g.profile!.protected!.filter(
                            (_, j) => j !== i,
                          ),
                        },
                      })
                    }
                  >
                    Remove
                  </button>
                </div>
              ))}
              <button
                className="secondary"
                onClick={() => {
                  const start = prompt(
                    "Protected start (e.g. 2026-11-06T09:00)",
                  );
                  const end =
                    start && prompt("Protected end (e.g. 2026-11-06T17:00)");
                  if (start && end)
                    change({
                      profile: {
                        ...profile,
                        protected: [
                          ...(g.profile?.protected || []),
                          { start: iso(start), end: iso(end) },
                        ],
                      },
                    });
                }}
              >
                Add protected time
              </button>
            </section>
          </div>
          <div className="footer-actions">
            <span className="meta">
              {dirty ? "Unsaved changes" : "Your choices are saved"}
            </span>
            <button disabled={loading} onClick={() => run(save)}>
              Save gathering
            </button>
            <button className="secondary" onClick={() => setStep(1)}>
              Review menu <ArrowRight size={16} />
            </button>
          </div>
        </>
      )}
      {step === 1 && (
        <>
          <div className="intro">
            <p className="eyebrow">A MENU WITH BREATHING ROOM</p>
            <h1>A spread that fits your week.</h1>
            <p>
              Keep your favorites. Buy a little. Let everyone bring something.
            </p>
          </div>
          <section className="card">
            <div className="row">
              <h2>
                <Utensils />
                How much variety?
              </h2>
              <div className="segmented">
                {["manageable", "generous"].map((value) => (
                  <button
                    className={g.spread === value ? "active" : "secondary"}
                    key={value}
                    onClick={() =>
                      change({
                        spread: value as Gathering["spread"],
                        category_counts: {
                          starters: value === "generous" ? 2 : 1,
                          mains: value === "generous" ? 3 : 2,
                          sides:
                            g.occasion === "Thanksgiving"
                              ? 4
                              : value === "generous"
                                ? 3
                                : 2,
                          desserts: value === "generous" ? 2 : 1,
                          drinks: 2,
                        },
                      })
                    }
                  >
                    {value === "manageable" ? "Manageable" : "More generous"}
                  </button>
                ))}
              </div>
            </div>
            <div className="counts">
              {categories.map((c) => (
                <label key={c}>
                  {c}
                  <input
                    aria-label={c + " count"}
                    type="number"
                    min="0"
                    max="12"
                    value={
                      g.category_counts?.[c] ??
                      (c === "starters" || c === "desserts" ? 1 : 2)
                    }
                    onChange={(e) =>
                      change({
                        spread: "custom",
                        category_counts: {
                          ...g.category_counts,
                          [c]: +e.target.value,
                        },
                      })
                    }
                  />
                </label>
              ))}
            </div>
            <p className="meta">
              Includes bought and guest-contributed dishes. Changing counts
              keeps your current dishes until you review additions or removals.
            </p>
            <button
              className="secondary"
              onClick={() => run(save)}
              disabled={loading}
            >
              Save menu preferences
            </button>
          </section>
          <div className="menu-grid">
            {(ws.inputs.selections || []).map((s) => (
              <article className="card recipe" key={s.id}>
                <div className="recipe-heading">
                  <div className="food-icon">
                    {s.recipe?.image_url ? (
                      <img
                        src={s.recipe.image_url}
                        alt={s.title}
                        onError={(e) => {
                          e.currentTarget.style.display = "none";
                        }}
                      />
                    ) : (
                      <Leaf size={24} />
                    )}
                  </div>
                  <div>
                    <p className="eyebrow">{s.category}</p>
                    <h3>{s.title}</h3>
                  </div>
                  <button
                    aria-label={"Must-have " + s.title}
                    className={"star " + (s.must_have ? "selected" : "")}
                    onClick={() => updateItem(s, { must_have: !s.must_have })}
                  >
                    <Star
                      size={20}
                      fill={s.must_have ? "currentColor" : "none"}
                    />
                  </button>
                </div>
                {s.recipe?.image_credit && (
                  <p className="meta">{s.recipe.image_credit}</p>
                )}
                <div className="fields">
                  <label>
                    Preparation
                    <select
                      aria-label={"Preparation " + s.title}
                      value={s.mode}
                      onChange={(e) =>
                        updateItem(s, {
                          mode: e.target.value as Selection["mode"],
                        })
                      }
                    >
                      <option value="cook">Cook</option>
                      <option value="buy">Buy prepared</option>
                      <option value="semi">Semi-prepared</option>
                      <option value="guest">Guest brings</option>
                    </select>
                  </label>
                  <label>
                    Serves
                    <input
                      aria-label={"Serves " + s.title}
                      type="number"
                      min="1"
                      value={s.servings}
                      onChange={(e) =>
                        updateItem(s, { servings: +e.target.value })
                      }
                    />
                  </label>
                </div>
                {s.mode === "guest" && (
                  <button
                    className="secondary"
                    onClick={() => {
                      const person = prompt("Who is bringing this?");
                      const serves =
                        person &&
                        prompt("How many does it serve?", String(s.servings));
                      const warm =
                        serves && prompt("Warming minutes (0 if none)", "0");
                      if (person && serves && warm !== null)
                        updateItem(s, {
                          contribution: {
                            name: s.title,
                            person,
                            servings: +serves,
                            confirmed: true,
                            warming_minutes: +warm!,
                            arrival: g.arrival,
                            equipment: +warm! ? "oven" : null,
                          },
                        });
                    }}
                  >
                    Set guest contribution
                  </button>
                )}
                {s.mode === "semi" && (
                  <p className="meta">
                    Review package instructions and preparation steps before
                    generating.
                  </p>
                )}
                <label>
                  Swap recipe
                  <select
                    aria-label={"Swap recipe " + s.title}
                    value={s.recipe?.id || ""}
                    onChange={(e) => {
                      const r = ws.recipes.find((x) => x.id === e.target.value);
                      if (r)
                        updateItem(s, {
                          recipe: r,
                          title: r.title,
                          category: r.category,
                          vegetarian: r.vegetarian,
                          mode: "cook",
                        });
                    }}
                  >
                    <option value="">Choose from collection</option>
                    {ws.recipes.map((r) => (
                      <option key={r.id} value={r.id}>
                        {r.title}
                      </option>
                    ))}
                  </select>
                </label>
                <div className="row">
                  <span className="meta">
                    {s.must_have
                      ? "Must-have"
                      : s.mode === "buy"
                        ? "No cooking tasks"
                        : "Review quantities & timing"}
                  </span>
                  <button
                    className="text-button"
                    disabled={s.must_have}
                    onClick={() =>
                      run(() => edit([{ action: "remove", id: s.id }]))
                    }
                  >
                    Remove
                  </button>
                </div>
              </article>
            ))}
          </div>
          <section className="card">
            <h2>
              <Plus />
              Add to your spread
            </h2>
            <div className="row">
              <select
                aria-label="Add saved recipe"
                defaultValue=""
                onChange={(e) => {
                  const r = ws.recipes.find((x) => x.id === e.target.value);
                  if (r)
                    run(() =>
                      edit([
                        {
                          action: "add",
                          selection: {
                            title: r.title,
                            category: r.category,
                            recipe: r,
                            mode: "cook",
                            servings: r.servings || g.guests,
                            vegetarian: r.vegetarian,
                          },
                        },
                      ]),
                    );
                  e.target.value = "";
                }}
              >
                <option value="">Choose a saved recipe…</option>
                {ws.recipes.map((r) => (
                  <option key={r.id} value={r.id}>
                    {r.title}
                  </option>
                ))}
              </select>
              <button
                className="secondary"
                onClick={() => {
                  const title = prompt("Prepared item name");
                  if (title)
                    run(() =>
                      edit([
                        {
                          action: "add",
                          selection: {
                            title,
                            mode: "buy",
                            category: "starters",
                            servings: g.guests,
                          },
                        },
                      ]),
                    );
                }}
              >
                <ShoppingBag size={16} />
                Add prepared item
              </button>
            </div>
            <details>
              <summary>Import a recipe</summary>
              <p className="meta">
                Paste a source URL or recipe text. Review missing timings and
                make-ahead support before saving.
              </p>
              <textarea
                aria-label="Recipe source"
                value={source}
                onChange={(e) => setSource(e.target.value)}
              />
              <button
                className="secondary"
                onClick={() =>
                  run(async () => {
                    const r = await api<Recipe>("/recipes/preview", { source });
                    setPreview(r);
                    setReviewJson(JSON.stringify(r, null, 2));
                  })
                }
              >
                Preview recipe
              </button>
              {preview && (
                <>
                  <p className="meta">
                    Review record: missing fields stay unknown. This first build
                    uses a structured editor; a friendlier editor is pending.
                  </p>
                  <textarea
                    aria-label="Recipe review"
                    rows={14}
                    value={reviewJson}
                    onChange={(e) => setReviewJson(e.target.value)}
                  />
                  <button
                    onClick={() =>
                      run(async () => {
                        await api("/recipes", {
                          recipe: { ...JSON.parse(reviewJson), reviewed: true },
                        });
                        await load(g.id!);
                        setPreview(null);
                        setNotice(
                          "Recipe saved locally; Notion sync requires connection.",
                        );
                      })
                    }
                  >
                    Save reviewed recipe
                  </button>
                </>
              )}
            </details>
          </section>
          <section className="card">
            <h2>
              <ShoppingBag />
              What you already have
            </h2>
            <p className="meta">
              Optional snapshot for this gathering. Enter one item per line:
              name, quantity, unit. Only confirmed amounts reduce shopping.
            </p>
            <textarea
              aria-label="Ingredients on hand"
              placeholder="Rice, 500, g"
              value={inventory}
              onChange={(e) => setInventory(e.target.value)}
            />
            <button
              className="secondary"
              onClick={() =>
                run(() =>
                  edit([
                    {
                      action: "inventory",
                      items: inventory
                        .split("\n")
                        .filter(Boolean)
                        .map((line) => {
                          const [name, quantity, unit] = line
                            .split(",")
                            .map((x) => x.trim());
                          return {
                            name,
                            quantity: quantity ? +quantity : null,
                            unit: unit || null,
                            source: "manual",
                          };
                        }),
                    },
                  ]),
                )
              }
            >
              Confirm ingredients
            </button>
            <p className="meta">
              {ws.inputs.inventory?.length || 0} confirmed items
            </p>
          </section>
          <div className="footer-actions">
            <button onClick={() => setStep(2)}>
              Review prep plan <ArrowRight size={16} />
            </button>
          </div>
        </>
      )}
      {step === 2 && (
        <>
          <div className="intro">
            <p className="eyebrow">YOUR TIME, PROTECTED</p>
            <h1>A calmer path to hosting.</h1>
            <p>
              Review the cooking sessions, then decide what goes on your
              calendar.
            </p>
          </div>
          <section className="card row">
            <span>
              <strong>{g.title}</strong>
              <br />
              <span className="meta">
                {selected.length} prep days · {g.guests} guests ·{" "}
                {g.relax_minutes} minutes before arrival
              </span>
            </span>
            <div className="actions">
              <button
                className="secondary"
                disabled={loading}
                onClick={() =>
                  run(async () => {
                    const a = await api<Inputs["availability"]>(
                      "/availability/" + g.id,
                      {},
                    );
                    setWs({ ...ws, inputs: { ...ws.inputs, availability: a } });
                    setApproval(null);
                    setNotice(
                      a?.status === "fixture"
                        ? "Sample calendar checked; no live Google connection."
                        : "Calendar rechecked. Regenerate before approval.",
                    );
                    setPlan(null);
                  })
                }
              >
                <RefreshCw size={16} />
                Recheck my plan
              </button>
              <button
                disabled={loading || dirty}
                onClick={() =>
                  run(async () => {
                    setPlan(
                      await api<Plan>("/plans/" + g.id + "/generate", {
                        expected_revision: g.revision,
                      }),
                    );
                    setApproval(null);
                    setBooking(null);
                  })
                }
              >
                Generate final plan
              </button>
            </div>
          </section>
          {dirty && (
            <p className="alert">
              Save your gathering changes before generating a plan.
            </p>
          )}
          {!plan && (
            <div className="empty">
              <ChefHat size={36} />
              <h2>Ready when you are.</h2>
              <p>
                Generate a plan from your current menu, helpers and available
                time.
              </p>
            </div>
          )}
          {plan && (
            <>
              <div
                className={
                  "plan-status " + (plan.status === "feasible" ? "good" : "")
                }
              >
                <strong>
                  {plan.status === "feasible"
                    ? "Your plan fits the entered constraints."
                    : "A few things need your attention."}
                </strong>
                <p className="meta">
                  {ws.fixture_mode
                    ? "Fixture validation only. Real calendar availability and recipe timing need verification."
                    : "Review source evidence and timings before approval."}
                </p>
              </div>
              {(plan.violations || []).length > 0 && (
                <section className="card">
                  <h2>Before we finalize</h2>
                  <ul>
                    {plan.violations?.map((v, i) => (
                      <li key={i}>{v.explanation}</li>
                    ))}
                  </ul>
                  {plan.adjustments?.map((a, i) => (
                    <div key={i} className="adjustment">
                      <p>
                        {a.day}: {a.current_minutes} → {a.proposed_minutes}{" "}
                        minutes
                      </p>
                      <p className="meta">{a.reason}</p>
                      <button
                        className="secondary"
                        onClick={() => {
                          change({
                            daily_limits: {
                              ...g.daily_limits,
                              [a.day]: a.proposed_minutes,
                            },
                          });
                          setStep(0);
                        }}
                      >
                        Use this allowance and review
                      </button>
                    </div>
                  ))}
                </section>
              )}
              <div className="grid">
                <section>
                  <h2>Cooking & prep sessions</h2>
                  {(plan.assignments || []).map((a) => (
                    <div className="session" key={a.task.id}>
                      <div className="session-meta">
                        <CalendarDays size={16} />
                        <strong>
                          {new Date(a.interval.start).toLocaleDateString([], {
                            weekday: "long",
                            month: "short",
                            day: "numeric",
                          })}{" "}
                          · {time(a.interval.start)}–{time(a.interval.end)}
                        </strong>
                        <span>
                          {a.person === "host"
                            ? "You"
                            : g.profile?.helpers?.find((h) => h.id === a.person)
                                ?.name || "Helper"}
                          {a.task.resource ? " · " + a.task.resource : ""}
                        </span>
                      </div>
                      <TaskCard task={a.task} />
                    </div>
                  ))}
                </section>
                <aside>
                  <section className="card">
                    <h2>
                      <ShoppingBag />
                      Shopping list
                    </h2>
                    {plan.shopping?.map((x, i) => (
                      <div className="ingredient" key={i}>
                        <span>{x.name}</span>
                        <strong>
                          {x.quantity == null
                            ? "Review"
                            : `${x.quantity} ${x.unit || ""}`}
                        </strong>
                      </div>
                    ))}
                  </section>
                  <section className="card">
                    <h2>Final small things</h2>
                    <ul>
                      {plan.checklist?.map((x) => (
                        <li key={x}>{x}</li>
                      ))}
                    </ul>
                  </section>
                  <section className="card">
                    <h2>
                      <CalendarDays />
                      Protect prep time
                    </h2>
                    <p>
                      Busy blocks go only to your dedicated Simmer and Gather
                      calendar.
                    </p>
                    <button
                      disabled={
                        loading ||
                        plan.status !== "feasible" ||
                        dirty ||
                        !!ws.fixture_mode
                      }
                      onClick={() =>
                        run(async () => {
                          const a = await api<{ id: string }>(
                            "/plans/" + plan.id + "/approve",
                            {
                              revision: plan.revision,
                              content_hash: plan.content_hash,
                            },
                          );
                          setApproval(a.id);
                        })
                      }
                    >
                      Approve these blocks
                    </button>
                    {approval && (
                      <button
                        onClick={() =>
                          run(async () =>
                            setBooking(
                              await api(
                                "/approvals/" + approval + "/apply",
                                {},
                              ),
                            ),
                          )
                        }
                      >
                        Add approved blocks to calendar
                      </button>
                    )}
                    {ws.fixture_mode && (
                      <p className="meta">
                        Live booking is disabled in the sample demo.
                      </p>
                    )}
                    {booking?.outcomes.map((x, i) => (
                      <p key={i}>
                        {x.title}: {x.status}
                      </p>
                    ))}
                  </section>
                </aside>
              </div>
            </>
          )}
        </>
      )}
      <footer>Simmer and Gather · made for time together</footer>
    </div>
  );
}
