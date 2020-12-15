from csp import CSP

def main():
    var_path= "rlfap/var2-f24.txt"
    dom_path= "rlfap/dom2-f24.txt"
    ctr_path= "rlfap/ctr2-f24.txt"
    var_file = open(var_path, 'r')
    pl = int(var_file.readline())
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

    for item in var_array:
        domains_array[item] = dom_array[var_dom_array[item]]

    ctr_file = open(ctr_path, 'r')
    pl = int(ctr_file.readline())
    for i in range(0, pl):
        temp = ctr_file.readline().split()
        first_var = int(temp[0])
        second_var = int(temp[1])
        k_var = int(temp[3])

        ctr_array[first_var] = dict()
        ctr_array[first_var][second_var] = (temp[2], k_var)
    ctr_file.close()

    print(var_array)
    return

def f(A, a, B, b):
    func = abs(a-b)
    temp = ctr_array[A][B]
    if temp[0] == '>':
        if func > temp[1]:
            return True
    elif temp[0] == '=':
        if func == temp[1]:
            return True
    return False


var_array = []
domains_array = dict()
ctr_array = dict()


if __name__ == "__main__":
    main()
