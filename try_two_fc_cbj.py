import csp

def fc_cbj(rlfap, select_unassigned_variable=csp.first_unassigned_variable, order_domain_values=csp.unordered_domain_values):
    i = 1
    var = select_unassigned_variable(rlfap.assignments, rlfap)
    rlfap.support_pruning()
    rlfap.conf_set[var] = []  #this must have (i, neighbor_var)
    while i >= 1 and i <= len(rlfap.variables):
        value = csp.first(order_domain_values(var, rlfap.assignments, rlfap))
        if not value:
            # iprev = i
            i = float('-Inf')
            temp = var
            for item in rlfap.conf_set[var]:
                if item[0] > i:
                    i = item[0]
                    temp = item[1]
            # conf_Set[i] = conf_Set[i] + conf_Set[iprev] - {xi}
            rlfap.conf_set[temp] = rlfap.conf_set[temp] + rlfap.conf_set[var]  # - {xi} but xi is null
            # reseat each curr_domain[k] where k > i to its value before xi was last instantiated
            var = temp
        else:
            rlfap.assign(var, value, rlfap.assignments)
            i += 1
            var = select_unassigned_variable(rlfap.assignments, rlfap)
            rlfap.curr_domains[var] = list(rlfap.domains[var])
            rlfap.conf_set[var] = []
    if i ==0:
        return {}
    else:
        return rlfap.assignments
