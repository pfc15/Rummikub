from util import get_n_comeco, get_n_final 

class Jogo():
    def __init__(self, tipo, pecas, cor=''):
        self.tipo = tipo
        self.cor = cor
        self.pecas = pecas[:]
    
    def is_legal(self):
        if len(self.pecas)<3:
            return False
        elif self.tipo =='trinca':
            cores = []
            peca_num = str(get_n_comeco(self.pecas, True))
            for p in self.pecas:
                if p[0]!='j' and (p[1]!=peca_num or p[0] in cores):
                    return False
                cores.append(p[1])
        elif self.tipo == 'sequencia':
            i = self.pecas[0]
            cont = 0
            while i[1] == '0':
                cont +=1
                i=self.pecas[cont]
            n = int(self.pecas[cont][1])-cont-1
            for p in self.pecas:
                if p[0]!='j'and (int(p[1])!=n+1 or self.cor != p[0]):
                    return False
                n+=1
        return True

    def __str__(self):
        s = self.pecas[0]
        for p in self.pecas[1:]:
            s += "/"+p
        
        return  f'tipo: {self.tipo}; jogo: {s}'

    def can_add(self, peca):
        if 'j0' in self.pecas:
            pass
        if self.tipo == 'sequencia':
            if peca[0] == self.cor:
                n_comeco = int(self.pecas[0][1:])
                n_final = int(self.pecas[-1][1:])
                # n_comeco = get_n_comeco(self.pecas)
                # n_final = get_n_final(self.pecas)
                if int(peca[1:]) == n_comeco-1:
                    return 0
                if int(peca[1:]) == n_final+1:
                    return len(self.pecas)
        elif self.tipo == 'trinca':
            # peca_num = get_n_comeco(self.pecas, True)
            peca_num = self.pecas[0][1:]
            if int(peca[1:]) == int(peca_num):
                cor_repetida = False
                for p in self.pecas:
                    if p[0] == peca[0]:
                        cor_repetida = True
                        break
                if not cor_repetida:
                    return len(self.pecas)
        return -1


        
            
if __name__ == "__main__":
    j1 = Jogo('trinca', ['b1', 'y1', 'j0'])
    print(j1.is_legal())
