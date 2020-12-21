# def cbj(rlfap, current):
#     h, i, jump = 0
#     if current > len(rlfap.variables):
#         # solution()
#         return len(rlfap.variables)
#     rlfap.conf_set[current] = []
#     for i in range(0, len(rlfap.curr_domains[rlfap.variables[current]])):
#         # assign to current domain i
#         if consistent(rlfap, current):
#             jump = cbj(rlfap, current+1)
#             if jump != current:
#                 return jump
#     h = max(rlfap.conf_set[current])
#     rlfap.conf_set[h] = rlfap.conf_set[h] + rlfap.conf_set[current]
#     return h


def fc_cbj(rlfap, z):
    def check(i, j):
        if rlfap.constraints(rlfap.variables[i], rlfap.assignments[rlfap.variables[i]], rlfap.variables[j], rlfap.assignments[rlfap.variables[j]]):
            return 1
        return 0


    def consistent(current):
        old= 0
        dell = 0
        for j in range(current+1, len(rlfap.variables)):
            if(rlfap.variables[j] not in rlfap.neighbors[rlfap.variables[current]]):
                continue
            for a in range(0, len(rlfap.domains[rlfap.variables[j]])):
                if rlfap.fc_obj_domains[j][a] ==0:
                    old += 1
                    rlfap.assign(rlfap.variables[j], rlfap.domains[rlfap.variables[j]][a], rlfap.assignments)
                    if check(current, j) == 0:
                        rlfap.fc_obj_domains[j][a] = current
                        dell += 1
            if dell:
                rlfap.fc_checking[current][j] = 1
            if old-dell == 0:
                return j
        return 0

    def restore(i):
        for j in range(i+1, len(rlfap.variables)):
            if rlfap.variables[j] not in rlfap.neighbors[rlfap.variables[i]]:
                continue
            if rlfap.fc_checking[i][j]:
                rlfap.fc_checking[i][j]=0
                for a in range(0, len(rlfap.domains[rlfap.variables[j]])):
                    if rlfap.fc_obj_domains[j][a] > 0:
                        rlfap.fc_obj_domains[j][a]= 0
                        # rlfap.prune(rlfap.variables[j], rlfap.domains[j][a], [])


    if z >= len(rlfap.variables):
        # solution()
        return len(rlfap.variables)
    rlfap.conf_set[z] = []
    for i in range(0, len(rlfap.domains[rlfap.variables[z]])):
        if rlfap.fc_obj_domains[z][i] > 0:
            continue
        rlfap.assign(rlfap.variables[z], rlfap.domains[rlfap.variables[z]][i], rlfap.assignments)
        fail = consistent(z)
        if fail ==0:
            jump = fc_cbj(rlfap, z+1)
            if jump != z:
                return jump
        restore(z)
        if fail:
            for j in range(1, z):
                if rlfap.fc_checking[z][fail]:
                    rlfap.conf_set[z].append(j)
    for j in range(1, z):
        if rlfap.fc_checking[j][z]:
            rlfap.conf_set[z].append(j)
    h = max(rlfap.conf_set[z])
    rlfap.conf_set[h] = rlfap.conf_set[h] + rlfap.conf_set[z]
    for j in range(z, h+1, -1):
        restore(i)
    return h
