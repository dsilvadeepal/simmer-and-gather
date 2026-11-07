from simmer.scheduler import validate_schedule
from simmer.menu import validate_menu

def evaluate_case(inputs,result):
    violations=validate_schedule(inputs,result)+validate_menu(inputs)
    return {'hard_constraints_pass':not violations,'violation_codes':sorted(set(v.code for v in violations)),'human_rating':None}
