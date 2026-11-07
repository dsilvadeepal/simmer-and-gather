export function CalendarPicker({calendars, selected, onChange, error}: {
  calendars: {id:string;name:string}[]; selected:string[];
  onChange:(ids:string[])=>void; error?:string;
}) {
  const matches = calendars.filter(c=>c.name.trim().toLowerCase()==='personal');
  const personal = matches.length === 1 ? matches[0] : undefined;
  const active = personal && selected.length === 1 && selected[0] === personal.id;
  return <div>
    {error ? <p role="status">{error}</p> : personal ? <>
      <p><strong>Personal</strong> · {active ? 'Selected' : 'Available'}</p>
      <p className="meta">Check this calendar for free prep time.</p>
      {!active && <button className="secondary" onClick={()=>onChange([personal.id])}>Use Personal calendar</button>}
    </> : <p role="status">{matches.length > 1 ? 'Multiple calendars are named Personal. Give your preferred calendar a unique name in Google Calendar.' : 'Personal calendar unavailable. Check your Google connection.'}</p>}
  </div>;
}
