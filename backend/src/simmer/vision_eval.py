"""Exact field scores on hand-labeled vision fixtures; no model judge."""
def score_items(expected, predicted):
    wanted = {x['name'].casefold(): x for x in expected}
    seen = set()
    matched = exact = unsupported = 0
    for item in predicted:
        name = item.get('name', '').casefold()
        if name in wanted and name not in seen:
            matched += 1
            target = wanted[name]
            exact += int(all(item.get(k) == target.get(k) for k in ('quantity', 'unit')))
            unsupported += int(target.get('quantity') is None and item.get('quantity') is not None)
        else:
            unsupported += 1
        seen.add(name)
    return dict(matched=matched, expected=len(expected), predicted=len(predicted), exact=exact, unsupported=unsupported)
