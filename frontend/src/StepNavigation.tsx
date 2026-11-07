export function StepNavigation({step,onSelect}:{step:number;onSelect:(step:number)=>void}) {
 return <nav aria-label="Planning steps" className="step-navigation">
  {['Gathering','Menu','Prep plan'].map((label,index)=><button key={label} type="button" className={index===step?'active':''} aria-current={index===step?'step':undefined} onClick={()=>onSelect(index)}><span className="step-number">{index+1}</span><span>{label}</span></button>)}
 </nav>;
}
