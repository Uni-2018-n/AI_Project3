import csp
import time
import random
import backjumping as cbj

def main():
    ends = ["2-f24.txt", "2-f25.txt", "3-f10.txt", "3-f11.txt", "6-w2.txt", "7-w1-f4.txt", "7-w1-f5.txt", "8-f10.txt", "8-f11.txt", "11.txt", "14-f27.txt", "14-f28.txt"]
    # ends = ["3-f10.txt", "11.txt"]
    # ends = ["11.txt"]
    # ends = ["2-f24.txt"]
    # ends= ["6-w2.txt"]

    print("FOR MAC:")
    for end in ends:
        var_path= "rlfap/var" + end
        dom_path= "rlfap/dom" + end
        ctr_path= "rlfap/ctr" + end

        mo_cc = 0
        mo_ac = 0
        mo_rt = 0
        for t in range(0,5):
            test = Rlfap(var_path, dom_path, ctr_path)
            start_time = time.time()
            temp = csp.backtracking_search(test, select_unassigned_variable=dom_wdeg,order_domain_values=csp.lcv, inference=mac)
            mo_rt += (time.time()-start_time)
            mo_cc += test.nconstraints
            mo_ac += test.nassigns
        print(end, ":", temp is not None)
        print("\trun time mo: %f" % (mo_rt/5))
        print("\tassign count mo: %.2f" % (mo_ac/5))
        print("\tconstraints count mo: %.2f" % (mo_cc/5))

    print("FOR FC:")
    for end in ends:
        var_path= "rlfap/var" + end
        dom_path= "rlfap/dom" + end
        ctr_path= "rlfap/ctr" + end

        mo_cc = 0
        mo_ac = 0
        mo_rt = 0
        for t in range(0,5):
            test = Rlfap(var_path, dom_path, ctr_path)
            start_time = time.time()
            temp = csp.backtracking_search(test, select_unassigned_variable=dom_wdeg,order_domain_values=csp.lcv, inference=forward_checking)
            mo_rt += (time.time()-start_time)
            mo_cc += test.nconstraints
            mo_ac += test.nassigns
        print(end, ":", temp is not None)
        print("\trun time mo: %f" % (mo_rt/5))
        print("\tassign count mo: %.2f" % (mo_ac/5))
        print("\tconstraints count mo: %.2f" % (mo_cc/5))
    return

def dom_wdeg(assignment, rlfap):
    queue = [v for v in rlfap.variables if v not in assignment]
    minimum = float('+Inf')
    output = queue[0]
    tt= []
    for x in queue:
        temp = [v for v in rlfap.neighbors[x] if v not in assignment]
        if temp:
            sum = 1
            for y in rlfap.neighbors[x]:
                sum += rlfap.weight[x][y]
                sum += rlfap.weight[y][x]
            if rlfap.curr_domains:
                t = len(rlfap.curr_domains[x])
            else:
                t = csp.count(rlfap.nconflicts(x, val, assignment) == 0 for val in rlfap.domains[x])
            sum = t/(sum * len(rlfap.neighbors[x]))
            if sum < minimum:
                tt = []
                tt.append(x)
                minimum = sum
                output = x
            elif sum == minimum:
                tt.append(x)
    if tt:
        # print(tt)
        return random.choice(tt)
    else:
        return csp.argmin_random_tie(queue, key= lambda var: csp.num_legal_values(rlfap, var, assignment))
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
                rlfap.weight[Xj][Xi] += 1
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
                rlfap.weight[var][B] += 1
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

            # print(first_var, second_var)
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

        self.fc_obj_domains = []
        for i in range(0, len(self.variables)):
            temp = []
            for j in range(0, len(self.domains[self.variables[i]])):
                temp.append(0)
            self.fc_obj_domains.append(temp)

        self.fc_checking = []
        for i in range(0, len(self.variables)):
            temp = []
            for j in range(0, len(self.variables)):
                temp.append(0)
            self.fc_checking.append(temp)

        self.conf_set = dict()

        self.assignments = dict()
        self.nconstraints = 0
        return

    def f(self, A, a, B, b):
        self.nconstraints += 1
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
