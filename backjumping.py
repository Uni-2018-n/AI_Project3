import csp
def backtracking_search(rlfap, select_unassigned_variable=csp.first_unassigned_variable,
                        order_domain_values=csp.unordered_domain_values, inference=csp.no_inference):
    def backtrack(assignment):
        if len(assignment) == len(rlfap.variables):
            return assignment
        var = select_unassigned_variable(assignment, rlfap)
        rlfap.conf_set[var] = []
        print("start for, ", var)
        if(rlfap.curr_domains and rlfap.curr_domains[var]):
            # print("im here", rlfap.curr_domains[var], rlfap.domains[var])
            # rlfap.curr_domains[var] = rlfap.domains[var]
            rlfap.restore([(var, v) for v in rlfap.domains[var] if v not in rlfap.curr_domains[var]])
        for value in order_domain_values(var, assignment, rlfap):

            print("var: ", var, "value: ", value)
            print(len(assignment))
            if 0 == rlfap.nconflicts(var, value, assignment):
                rlfap.assign(var, value, assignment)
                removals = rlfap.suppose(var, value)
                if inference(rlfap, var, value, assignment, removals):
                    result = backtrack(assignment)
                    if isinstance(result, int):
                        if var != result:
                            print("going more back(im at", var, ")")
                            rlfap.unassign(var, assignment)
                            return result
                        else:
                            print("found my backjump")
                            print("backjumps domains",rlfap.curr_domains[var], value)
                    else:
                        return result
                # else:
                    # print("var: ", var, "not acceptable value", value)
                # print("var: ", var, "last domain wasnt it(", value, ") going to next")
                rlfap.restore(removals)
                # print("after restore: ", rlfap.curr_domains[var])
            # else:
                # print("error")

                # print("removals: ", removals)
        print("var:", var, "no more domains to check")
        rlfap.unassign(var, assignment)
        print("conf_set[", var, "]=", rlfap.conf_set[var])
        h= rlfap.conf_set[var][-1]
        # print("backjumping to:", h)
        # rlfap.conf_set[h] = rlfap.conf_set[h] + rlfap.conf_set[var]
        for item in rlfap.conf_set[var]:
            # print(item)
            if item not in rlfap.conf_set[h] and item < h:
                rlfap.conf_set[h].append(item)
        while(h in rlfap.conf_set[h]):
            rlfap.conf_set[h].remove(h)
        rlfap.conf_set[h].sort()
        # rlfap.curr_domains[var] = rlfap.domains[var]
        rlfap.restore([(var, v) for v in rlfap.domains[var] if v not in rlfap.curr_domains[var]])
        print("editing domain", var)
        # print(rlfap.conf_set[h])
        # flag = False
        # for item in assignment.keys():
        #     if item == h:
        #         flag = True
        #     if flag:
        #         # rlfap.unassign(assignment[item])
        #         rlfap.curr_domains[item] = rlfap.domains[item]

        return h
    # print("running")
    result = backtrack({})
    assert result is None or rlfap.goal_test(result)
    return result

def forward_checking(rlfap, var, value, assignment, removals):
    """Prune neighbor values inconsistent with var=value."""
    # print(rlfap.curr_domains)
    rlfap.support_pruning()
    add = True
    # for B in rlfap.neighbors[var]:
        # if B in assignment:
            # print("test")
            # rlfap.conf_set[var].append(B)
    # print(rlfap.conf_set[var])
    # print("neighbors: ", rlfap.neighbors[var])
    for B in rlfap.neighbors[var]:
        # if B not in assignment:
        for b in rlfap.curr_domains[B][:]:
            if not rlfap.constraints(var, value, B, b):  #seekSupport
                rlfap.prune(B, b, removals)
                # add= True
        # if add:
            # if B in assignment:
                # print("added", B)
        # print("test")
        if B in assignment:
            # print("test2")
            if B not in rlfap.conf_set[var]:
                # print("added", B)
                rlfap.conf_set[var].append(B)
        if not rlfap.curr_domains[B]:
            rlfap.weight[B][var] += 1
            rlfap.weight[var][B] += 1
            add= False
    return add
