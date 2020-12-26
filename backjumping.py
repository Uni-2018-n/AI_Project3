import csp
def backtracking_search(rlfap, select_unassigned_variable=csp.first_unassigned_variable,
                        order_domain_values=csp.unordered_domain_values, inference=csp.no_inference):
    """[Figure 6.5]"""

    def backtrack(assignment):
        # print(len(assignment))
        if len(assignment) == len(rlfap.variables):
            return assignment
        var = select_unassigned_variable(assignment, rlfap)
        rlfap.conf_set[var] = []
        for value in order_domain_values(var, assignment, rlfap):
            if 0 == rlfap.nconflicts(var, value, assignment):
                rlfap.assign(var, value, assignment)
                removals = rlfap.suppose(var, value)
                if inference(rlfap, var, value, assignment, removals):
                    result = backtrack(assignment)
                    if result is not None:
                        return result
                rlfap.restore(removals)
        rlfap.unassign(var, assignment)
        if not rlfap.conf_set[var]:
            return None
        # print(rlfap.conf_set[var])
        h = rlfap.conf_set[var][-1]
        if h not in rlfap.conf_set.keys():
            rlfap.conf_set[h] = []
        rlfap.conf_set[h] += rlfap.conf_set[var]
        rlfap.unassign(var, assignment)
        return None

    result = backtrack({})
    assert result is None or rlfap.goal_test(result)
    return result

def forward_checking(rlfap, var, value, assignment, removals):
    """Prune neighbor values inconsistent with var=value."""
    rlfap.support_pruning()
    for B in rlfap.neighbors[var]:
        if B not in assignment:
            for b in rlfap.curr_domains[B][:]:
                if not rlfap.constraints(var, value, B, b):
                    rlfap.prune(B, b, removals)
            if not rlfap.curr_domains[B]:
                return False
            rlfap.conf_set[var].append(B)
    return True
