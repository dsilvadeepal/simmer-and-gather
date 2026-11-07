from simmer.vision_eval import score_items


def test_hallucinated_quantity_fails_even_when_name_correct():
    result = score_items([{'name': 'rice', 'quantity': None, 'unit': None}], [{'name': 'rice', 'quantity': 2, 'unit': 'kg'}])
    assert result == {'matched': 1, 'expected': 1, 'predicted': 1, 'exact': 0, 'unsupported': 1}


def test_missing_and_extra_items_count_separately():
    assert score_items([{'name': 'rice', 'quantity': 1, 'unit': 'kg'}], [{'name': 'milk', 'quantity': 1, 'unit': 'l'}])['matched'] == 0
