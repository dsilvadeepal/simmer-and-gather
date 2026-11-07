from unittest.mock import patch
from simmer.agent import buy_prepared_suggestions
from simmer.domain import PlanInputs, Gathering, MenuSelection, PlanCandidate, ConstraintViolation

def test_only_validated_optional_buy_is_suggested_without_changing_menu():
    inputs=PlanInputs(gathering=Gathering(),selections=[MenuSelection(id='must',title='Must',must_have=True),MenuSelection(id='dish',title='Turkey')])
    plan=PlanCandidate(gathering_id=inputs.gathering.id,revision=1,input_hash='test',status='conflict',violations=[ConstraintViolation(code='unscheduled',explanation='No slot')])
    def candidate(trial):
        assert trial.selections[0].mode=='cook'
        assert trial.selections[1].mode=='buy'
        return plan.model_copy(update={'status':'feasible'})
    with patch('simmer.scheduler.schedule',side_effect=candidate),patch('simmer.agent.validate_menu',return_value=[]):
        suggestions=buy_prepared_suggestions(inputs,plan)
    assert suggestions[0].affected_ids==['dish']
    assert all(x.mode=='cook' for x in inputs.selections)

def test_no_fallback_for_other_conflicts():
    inputs=PlanInputs(gathering=Gathering(),selections=[MenuSelection(title='Turkey')])
    plan=PlanCandidate(gathering_id=inputs.gathering.id,revision=1,input_hash='test',status='conflict',violations=[ConstraintViolation(code='allergy',explanation='Check allergy')])
    assert buy_prepared_suggestions(inputs,plan)==[]

def test_offers_more_than_one_tested_alternative():
    inputs=PlanInputs(gathering=Gathering(),selections=[MenuSelection(id='one',title='Turkey'),MenuSelection(id='two',title='Dessert')])
    plan=PlanCandidate(gathering_id=inputs.gathering.id,revision=1,input_hash='test',status='conflict',violations=[ConstraintViolation(code='unscheduled',explanation='No slot')])
    with patch('simmer.scheduler.schedule',return_value=plan.model_copy(update={'status':'feasible'})),patch('simmer.agent.validate_menu',return_value=[]):
        result=buy_prepared_suggestions(inputs,plan)
    assert [x.affected_ids for x in result]==[['one'],['two']]
    assert all(x.mode=='cook' for x in inputs.selections)
