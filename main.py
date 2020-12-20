import csp
import time
ctr_array = dict()

def main():
    ends = ["2-f24.txt", "2-f25.txt", "3-f10.txt", "3-f11.txt", "6-w2.txt", "7-w1-f4.txt", "7-w1-f5.txt", "8-f10.txt", "8-f11.txt", "11.txt", "14-f27.txt", "14-f28.txt"]
    # ends = ["3-f10.txt", "11.txt"]
    # ends = ["2-f24.txt"]
    # ends= ["14-f27.txt"]

    print("FOR MAC:")
    for end in ends:
        var_path= "rlfap/var" + end
        dom_path= "rlfap/dom" + end
        ctr_path= "rlfap/ctr" + end


        test = Rlfap(var_path, dom_path, ctr_path)
        start_time = time.time()
        temp = csp.backtracking_search(test, select_unassigned_variable=dom_wdeg, order_domain_values=csp.lcv, inference=mac)
        print(end, ":", temp is not None, "\n\trun time: %.2f" % (time.time()-start_time), "\n\tassign count:", test.nassigns)

    print("FOR FC:")
    for end in ends:
        var_path= "rlfap/var" + end
        dom_path= "rlfap/dom" + end
        ctr_path= "rlfap/ctr" + end


        test = Rlfap(var_path, dom_path, ctr_path)
        start_time = time.time()
        temp = csp.backtracking_search(test, select_unassigned_variable=dom_wdeg, order_domain_values=csp.lcv, inference=forward_checking)
        print(end, ":", temp is not None, "\n\trun time: %.2f" % (time.time()-start_time), "\n\tassign count:", test.nassigns)

    print("FOR MIN-CONF:")
    for end in ends:
        var_path= "rlfap/var" + end
        dom_path= "rlfap/dom" + end
        ctr_path= "rlfap/ctr" + end


        test = Rlfap(var_path, dom_path, ctr_path)
        start_time = time.time()
        temp = csp.min_conflicts(test)
        print(end, ":", temp is not None, "\n\trun time: %.2f" % (time.time()-start_time), "\n\tassign count:", test.nassigns)

    return


def FC_CBJ(rlfap):
    def main_FC_CBJ(assignment, z, conf_set):
        def consistent(current):
            j, a=0
            old, dell = 0
            for j in range(current+1, len(rlfap.variables)):
                for a in range(0, rlfap.curr_domains[j]):
                    if rlfap.curr_domains[j][a]:
                        old += 1
                        rlfap.assign(rlfap.variables[j], rlfap.curr_domains[a], assignment)
                        # if


        if z > len(rlfap.variables):
            return (len(rlfap.variables), assignment)

        rlfap.support_pruning()
        for i in range(0, len(rlfap.curr_domains[z])):
            conf_set[i] = []
            if not rlfap.curr_domains[z][i]:
                continue
            rlfap.assign(rlfap.variables[z], rlfap.curr_domains[i], assignment)
            fail = csp.consistency
        return

    conf_set = dict()
    result = main_FC_CBJ({}, 0, conf_set)
    assert result is None or rlfap.goal_test(result)
    return result

def dom_wdeg(assignment, rlfap):
    queue = [v for v in rlfap.variables if v not in assignment]
    minimum = float('+Inf')
    output = queue[0]
    for x in queue:
        flag = False
        sum = 1
        for y in rlfap.neighbors[x]:
            if y not in assignment:
                flag = True
            sum += rlfap.weight[x][y]
        if not flag:
            sum = float('+Inf')
        if rlfap.curr_domains:
            sum = len(rlfap.curr_domains[x])/sum
        else:
            sum = csp.count(rlfap.nconflicts(x, val, assignment) == 0 for val in rlfap.domains[x])
        if sum < minimum:
            minimum = sum
            output = x
    return output

def AC3(rlfap, assignment, queue=None, removals=None, arc_heuristic=csp.dom_j_up):
    """[Figure 6.3]"""
    if queue is None:
        queue = {(Xi, Xk) for Xi in rlfap.variables for Xk in rlfap.neighbors[Xi]}
    rlfap.support_pruning()
    queue = arc_heuristic(rlfap, queue)
    checks = 0
    while queue:
        (Xi, Xj) = queue.pop()
        revised, checks = revise(rlfap, Xi, Xj, removals, checks)
        if revised:
            if not rlfap.curr_domains[Xi]:
                rlfap.weight[Xi][Xj] += 1
                return False, checks  # rlfap is inconsistent
            for Xk in rlfap.neighbors[Xi]:
                if Xk != Xj:
                    queue.add((Xk, Xi))
    return True, checks  # CSP is satisfiable


def revise(rlfap, Xi, Xj, removals, checks=0):
    """Return true if we remove a value."""
    revised = False
    for x in rlfap.curr_domains[Xi][:]:
        conflict = True
        for y in rlfap.curr_domains[Xj]:
            if rlfap.constraints(Xi, x, Xj, y):
                conflict = False
            checks += 1
            if not conflict:
                break
        if conflict:
            rlfap.prune(Xi, x, removals)
            revised = True
    # if not rlfap.curr_domains[Xi]:
    #     # print(rlfap.curr_domains[Xi])
    #     rlfap.weight[Xi][Xj] += 1


    return revised, checks


def mac(rlfap, var, value, assignment, removals, constraint_propagation=AC3):
    """Maintain arc consistency."""
    return constraint_propagation(rlfap, assignment, {(X, var) for X in rlfap.neighbors[var]}, removals)


def forward_checking(rlfap, var, value, assignment, removals):
    """Prune neighbor values inconsistent with var=value."""
    rlfap.support_pruning()
    for B in rlfap.neighbors[var]:
        if B not in assignment:
            for b in rlfap.curr_domains[B][:]:
                if not rlfap.constraints(var, value, B, b):  #seekSupport
                    rlfap.prune(B, b, removals)
            if not rlfap.curr_domains[B]:
                rlfap.weight[B][var] += 1
                return False
    return True



class Rlfap(csp.CSP):
    def __init__(self, var_path, dom_path, ctr_path):
        var_file = open(var_path, 'r')
        pl = int(var_file.readline())
        var_array = []
        var_dom_array = dict()
        for i in range(0, pl):
            temp = var_file.readline().split()

            variable_temp = int(temp[0])
            dom_temp = int(temp[1])
            var_array.append(variable_temp)
            var_dom_array[variable_temp] = dom_temp
        var_file.close()


        dom_file = open(dom_path, 'r')
        dom_array = dict()
        pl = int(dom_file.readline())
        for i in range(0, pl):
            temp = dom_file.readline().split()
            id_temp = int(temp[0])
            pl_temp = int(temp[1])
            num_list = []
            for j in range(2, pl_temp+2):
                num_list.append(int(temp[j]))
            dom_array[id_temp] = num_list
        dom_file.close()


        domains_array = dict()
        for item in var_array:
            domains_array[item] = dom_array[var_dom_array[item]]


        ctr_file = open(ctr_path, 'r')
        pl = int(ctr_file.readline())
        self.ctr_array = dict()
        neighbors = dict()
        for i in range(0, pl):
            temp = ctr_file.readline().split()
            first_var = int(temp[0])
            second_var = int(temp[1])
            k_var = int(temp[3])


            self.ctr_array.setdefault(first_var, {})[second_var] = (temp[2], k_var)
            self.ctr_array.setdefault(second_var, {})[first_var] = (temp[2], k_var)
            if first_var not in neighbors.keys():
                neighbors[first_var] = []
            neighbors[first_var].append(second_var)
            if second_var not in neighbors.keys():
                neighbors[second_var] = []
            neighbors[second_var].append(first_var)
        ctr_file.close()
        self.weight = dict()
        for x in var_array:
            for y in neighbors[x]:
                self.weight.setdefault(x, {})[y] = 0


        csp.CSP.__init__(self, var_array, domains_array, neighbors, self.f)
        return

    def f(self, A, a, B, b):
        if a > b:
            func = a-b
        else:
            func = b-a
        temp = self.ctr_array[A][B]
        if temp[0] == '>':
            if func > temp[1]:
                return True
        elif temp[0] == '=':
            if func == temp[1]:
                return True
        return False


if __name__ == "__main__":
    main()
