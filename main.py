import csp

ctr_array = dict()

def main():
    ends = ["11.txt", "2-f24.txt", "2-f25.txt", "3-f10.txt", "3-f11.txt", "8-f10.txt", "8-f11.txt", "14-f27.txt", "14-f28.txt", "6-w2.txt", "7-w1-f4.txt"]
    # ends = ["2-f24.txt"]
    for end in ends:
        var_path= "rlfap/var" + end
        dom_path= "rlfap/dom" + end
        ctr_path= "rlfap/ctr" + end


        test = Rlfap(var_path, dom_path, ctr_path)
        temp = csp.backtracking_search(test, select_unassigned_variable=dom_wdeg, inference=mac)
        print(end, ": ", temp is not None)
        # temp = csp.backtracking_search(test, select_unassigned_variable=csp.mrv, inference=mac)
        # print(end, ": ", temp is not None)


        # print(temp)
    return

def dom_wdeg(assignment, rlfap):
    queue = [v for v in rlfap.variables if v not in assignment]

    sum = 1
    temp = False
    neighbors = rlfap.neighbors[queue[0]]
    for neighbor in neighbors:
        if neighbor not in assignment:
            temp = True
        sum += rlfap.weight[queue[0]][neighbor]
    if not temp:
        sum = 1

    return csp.first(csp.SortedSet(queue, key=lambda var: csp.num_legal_values(rlfap, var,assignment)/sum))


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

    if len(rlfap.curr_domains[Xi][:]) ==0:
        rlfap.weight[Xi][Xj] += 1


    return revised, checks


def mac(rlfap, var, value, assignment, removals, constraint_propagation= AC3):
    """Maintain arc consistency."""
    return constraint_propagation(rlfap, assignment, {(X, var) for X in rlfap.neighbors[var]}, removals)



class Rlfap(csp.CSP):
    def __init__(self, var_path, dom_path, ctr_path):
        var_file = open(var_path, 'r')
        pl = int(var_file.readline())
        self.var_array = []
        var_dom_array = dict()
        for i in range(0, pl):
            temp = var_file.readline().split()

            variable_temp = int(temp[0])
            dom_temp = int(temp[1])
            self.var_array.append(variable_temp)
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


        self.domains_array = dict()
        for item in self.var_array:
            self.domains_array[item] = dom_array[var_dom_array[item]]


        ctr_file = open(ctr_path, 'r')
        pl = int(ctr_file.readline())
        self.ctr_array = dict()
        self.neighbors = dict()
        for i in range(0, pl):
            temp = ctr_file.readline().split()
            first_var = int(temp[0])
            second_var = int(temp[1])
            k_var = int(temp[3])


            self.ctr_array.setdefault(first_var, {})[second_var] = (temp[2], k_var)
            self.ctr_array.setdefault(second_var, {})[first_var] = (temp[2], k_var)
            if first_var not in self.neighbors.keys():
                self.neighbors[first_var] = []
            self.neighbors[first_var].append(second_var)
            if second_var not in self.neighbors.keys():
                self.neighbors[second_var] = []
            self.neighbors[second_var].append(first_var)
        ctr_file.close()
        self.weight = dict()
        for x in self.var_array:
            for y in self.neighbors[x]:
                self.weight.setdefault(x, {})[y] = 0


        csp.CSP.__init__(self, self.var_array, self.domains_array, self.neighbors, self.f)
        return

    def f(self, A, a, B, b):
        func = abs(a-b)
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
