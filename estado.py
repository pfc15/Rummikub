from numpy.random import randint

class Estado():
    def __init__(self, mesa,jogador, pecas, vez=0,movimento=0, acao=0, comeco=False):
        self.mesa = mesa
        self.jogador = jogador
        self.pecas = pecas
        self.vez = vez
        self.movimento = movimento
        self.acao = acao
        if comeco:
            self.comeca_jogo()
        
    def comeca_jogo(self):
        self.pecas = self.cria_pecas()
        self.jogador = []
        for i in range(14):
            index = randint(0, len(self.pecas))
            self.jogador.append(self.pecas[index])
            self.jogador.sort()
            self.pecas.pop(index)
    
    def cria_pecas(self):
        cores = ['c','o', 'p', 'e']
        pecas = []
        for e in range(2):
            for cor in cores:
                for i in range(1, 14):
                    pecas.append(f'{cor}{i}')
        # pecas.append('j0')
        # pecas.append('j0')
        return pecas

    def get_fitness(self):
        return (len(self.jogador), self.vez)
    
    def mesa_to_string(self):
        s = ""
        for j in self.mesa:
            s += str(j)+"/"
        return s

    def to_string(self):
        a = f"mesa:{self.mesa_to_string()};\n jogador: {self.jogador};\n vez: {self.vez};\npecas:{len(self.pecas)} quant_acoes:{self.acao}"
        return a

