def main():
    var_path= "rlfap/var2-f24.txt"
    dom_path= "rlfap/dom2-f24.txt"
    ctr_path= "rlfap/ctr2-f24.txt"
    var_file = open(var_path, 'r')
    var_array = dict()
    pl = int(var_file.readline())
    for i in range(0, pl):
        temp = var_file.readline()
        variable_temp = ''
        index =0
        for index in range(len(temp)):
            if temp[index] == ' ':
                break
            else:
                variable_temp += temp[index]

        dom_temp = ''
        for t in range(index, len(temp)):
            if t == len(temp):
                break
            else:
                dom_temp += temp[t]

        variable_temp = int(variable_temp)
        dom_temp = int(dom_temp)
        var_array[variable_temp] = dom_temp
    var_file.close()


    dom_file = open(dom_path, 'r')
    dom_array = dict()
    pl = int(dom_file.readline())
    for i in range(0, pl):
        temp = dom_file.readline()
        id_temp = ''
        for j in range(len(temp)):
            if temp[j] == ' ':
                break
            else:
                id_temp += temp[j]
        id_temp = int(id_temp)

        pl_temp = ''
        for k in range(j+1, len(temp)):
            if temp[k] == ' ':
                break
            else:
                pl_temp += temp[k]
        pl_temp = int(pl_temp)


        num_list = []
        for m in range(pl_temp):
            k += 1
            num_temp = ''
            while True:
                if temp[k] == ' ' or temp[k] == '\n':
                    break
                else:
                    num_temp += temp[k]
                k += 1

            num_list.append(int(num_temp))

        dom_array[id_temp] = num_list
    dom_file.close()



    ctr_file = open(ctr_path, 'r')
    pl = int(ctr_file.readline())
    ctr_array = dict()
    for i in range(0, pl):
        temp = ctr_file.readline()
        k=0
        first_var = ''
        while True:
            if temp[k] == ' ':
                k += 1
                break
            else:
                first_var += temp[k]
            k += 1

        second_var = ''
        while True:
            if temp[k] == ' ':
                k += 1
                break
            else:
                second_var += temp[k]
            k += 1

        op = temp[k]
        k += 1

        k_var = ''
        while True:
            if temp[k] == '\n':
                break
            else:
                k_var += temp[k]
            k += 1

        first_var = int(first_var)
        second_var = int(second_var)
        k_var = int(k_var)

        ctr_array[first_var] = dict()
        ctr_array[first_var][second_var] = (op, k_var)
    ctr_file.close()
    return












if __name__ == "__main__":
    main()
