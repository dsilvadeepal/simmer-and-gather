"""Validate task graphs before attempting a schedule, without rewriting recipes."""
def task_contract_errors(tasks):
    errors=[]
    by_id={t.id:t for t in tasks}
    if len(by_id)!=len(tasks):
        errors.append('Preparation steps have duplicate identifiers.')
    for task in tasks:
        missing=[d for d in task.dependencies if d not in by_id]
        if missing:
            errors.append(f'{task.title}: prerequisite steps are missing: {", ".join(missing)}.')
        if task.minutes is not None:
            if task.active_minutes is not None and task.active_minutes>task.minutes:
                errors.append(f'{task.title}: hands-on time exceeds elapsed time.')
            if task.presence_minutes is not None and task.presence_minutes>task.minutes:
                errors.append(f'{task.title}: required presence exceeds elapsed time.')
            if any(s.offset_minutes+s.minutes>task.minutes for s in task.attention_segments):
                errors.append(f'{task.title}: an attention segment ends after the step.')
    # Iterative traversal avoids recursion failure on malformed imported graphs.
    pending={t.id:set(t.dependencies) for t in tasks}
    while pending:
        ready={key for key,deps in pending.items() if not deps}
        if not ready:
            if not any(d not in by_id for deps in pending.values() for d in deps):
                errors.append('Preparation steps contain a dependency cycle.')
            break
        pending={key:deps-ready for key,deps in pending.items() if key not in ready}
    return errors
