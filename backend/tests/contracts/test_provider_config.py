from simmer.config import validate_provider_config


def test_fixtures_need_no_credentials():
    assert validate_provider_config({'mode': 'fixtures'}) == []


def test_live_unknown_model_or_rates_denied():
    assert validate_provider_config({'mode': 'live', 'model': 'invented', 'monthly_forecast': 1})
    assert validate_provider_config({'mode': 'live', 'model': 'known', 'verified_models': ['known'], 'monthly_forecast': 1})


def test_over_budget_and_nonfinite_forecasts_denied():
    base = dict(mode='live', model='known', verified_models=['known'], input_rate=0.2, output_rate=0.6)
    for value in [5.01, float('nan'), -1]:
        assert validate_provider_config(dict(base, monthly_forecast=value))
    assert validate_provider_config(dict(base, monthly_forecast=4)) == []
