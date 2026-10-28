"""Fail closed for unverified paid configurations."""
from decimal import Decimal, InvalidOperation


def validate_provider_config(config: dict) -> list[str]:
    if config.get('mode') == 'fixtures':
        return []
    errors = []
    if config.get('mode') != 'live':
        errors.append('Choose fixtures or live mode')
    if not config.get('model') or config['model'] not in config.get('verified_models', []):
        errors.append('Model is not verified')
    for key in ('input_rate', 'output_rate', 'monthly_forecast'):
        try:
            value = Decimal(str(config[key]))
            if not value.is_finite() or value < 0 or (key == 'monthly_forecast' and value > 5):
                raise ValueError()
        except (KeyError, InvalidOperation, ValueError):
            errors.append(f'{key} must be verified, finite and within budget')
    return errors
