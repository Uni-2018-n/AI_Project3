import csp

ctr_array = dict()

def main():
    ends = ["11.txt", "2-f24.txt", "2-f25.txt", "3-f10.txt", "3-f11.txt", "8-f10.txt", "8-f11.txt", "14-f27.txt", "14-f28.txt", "6-w2.txt", "7-w1-f4.txt"]
    for end in ends:
        var_path= "rlfap/var" + end
        dom_path= "rlfap/dom" + end
        ctr_path= "rlfap/ctr" + end


        test = Rlfap(var_path, dom_path, ctr_path)
        print(end, ": ", csp.mac(test, test.var_array[0], None, None, None))
        # print(end, ": ", csp.min_conflicts(test))
    return

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
