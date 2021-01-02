import csp
def backjumping_search(rlfap, select_unassigned_variable=csp.first_unassigned_variable,
                        order_domain_values=csp.unordered_domain_values, inference=csp.no_inference):
    """[Figure 6.5]"""

    def backjump(assignment):
        if len(assignment) == len(rlfap.variables):
            return assignment
        var = select_unassigned_variable(assignment, rlfap)
        rlfap.conf_set[var] = []
        for value in order_domain_values(var, assignment, rlfap):
            if 0 == rlfap.nconflicts(var, value, assignment):
                rlfap.assign(var, value, assignment)
                removals = rlfap.suppose(var, value)
                if inference(rlfap, var, value, assignment, removals):
                    result = backjump(assignment)
                    if isinstance(result, int): #incase of backjump
                        if result != var: #check if we need to backjump here
                            rlfap.unassign(var, assignment) #if not unassign the variable that was assigned
                            rlfap.restore(removals) #and restore its domain
                            return result
                    elif result is not None:
                        return result
                rlfap.restore(removals) #if its the var we need to backjump it restores it by it shelf and changes the assigned value so we dont need to do anything
        rlfap.unassign(var, assignment)
        for item in reversed(list(assignment.keys())): #used this logic to find the latest assigned value inside the conf_set[var]
            if item in rlfap.conf_set[var]:
                h= item
                break
        for item in rlfap.conf_set[var]: #used this logic to murge the two conf_sets and skip the already added items or the item h
            if item not in rlfap.conf_set[h] and item != h:
                rlfap.conf_set[h].append(item)
        return h

    result = backjump({})
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
                    rlfap.conf_set[B].append(var)
            if not rlfap.curr_domains[B]:
                for item in rlfap.conf_set[B]:
                    if item not in rlfap.conf_set[var] and item != var:
                        rlfap.conf_set[var].append(item)
                return False
    return True
