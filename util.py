def search_element(lst, target):
    if target in lst:
        return lst.index(target)
    else:
        return -1

def get_n_comeco(pecas, trinca=False):
    cont = 0
    i = pecas[0]
    while i[1] == '0':
        cont +=1
        i=pecas[cont]
    n = int(pecas[cont][1])-cont

    return n if not trinca else int(pecas[cont][1])

def get_n_final(pecas, trinca=False):
    cont = len(pecas)-1
    i = pecas[-1]
    while i[1] == '0':
        cont -=1
        i=pecas[cont]
    n = int(pecas[len(pecas)-cont][1])+cont
    return n if not trinca else int(pecas[cont][1])


