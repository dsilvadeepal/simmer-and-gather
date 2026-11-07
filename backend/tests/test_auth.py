from datetime import datetime, timezone, timedelta
import jwt, pytest
from simmer.auth import Authenticator, encrypt_secret, decrypt_secret
from cryptography.fernet import Fernet

def test_expired_foreign_owner_and_wrong_audience_denied():
    key='test-secret-at-least-32-characters-long'
    auth=Authenticator(key, 'allowed', issuer='simmer', audience='simmer')
    def token(**kw):
        return jwt.encode(dict(sub='allowed', iss='simmer', aud='simmer', exp=datetime.now(timezone.utc)+timedelta(minutes=2), **kw),key,algorithm='HS256')
    assert auth.require_owner(token()) == 'allowed'
    for changes in [{'sub':'other'},{'exp':0},{'aud':'other'}]:
        claims=jwt.decode(token(),key,algorithms=['HS256'],audience='simmer'); claims.update(changes)
        with pytest.raises(ValueError): auth.require_owner(jwt.encode(claims,key,algorithm='HS256'))

def test_credentials_encrypted():
    key=Fernet.generate_key().decode(); encrypted=encrypt_secret('private-value',key)
    assert 'private-value' not in encrypted
    assert decrypt_secret(encrypted,key)=='private-value'
