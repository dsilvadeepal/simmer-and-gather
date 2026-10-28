export function CalendarPicker({calendars, selected, onChange, error}: {
  calendars: {id:string;name:string}[]; selected:string[];
  onChange:(ids:string[])=>void; error?:string;
}) {
  return <fieldset><legend>Calendars to check</legend>
    {error && <p role="status">{error}</p>}
    {calendars.map(c=><label key={c.id} className="check"><input type="checkbox"
      checked={selected.includes(c.id)} onChange={e=>onChange(e.target.checked?[...selected,c.id]:selected.filter(id=>id!==c.id))}/>{c.name}</label>)}
    {!calendars.length && !error && <p className="meta">No calendars available.</p>}
  </fieldset>;
}
