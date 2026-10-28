from simmer.oauth import OAuthState
from simmer.db import Conflict
import pytest

def test_state_single_use_and_browser_binding(store):
    manager=OAuthState(store)
    state,binder,verifier=manager.begin()
    with pytest.raises(Conflict): manager.consume(state,'wrong')
    assert manager.consume(state,binder)==verifier
    with pytest.raises(Conflict): manager.consume(state,binder)
