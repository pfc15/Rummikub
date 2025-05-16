from numpy.random import randint
from jogo import Jogo
from util import search_element

# get movimentos
def get_criar_jogo_jogador(jogador):
    if len(jogador) <3:
        return []
    acoes = []
    em_uso = []
    # trinca
    for i in range(len(jogador)-2):
        if i not in em_uso:
            p = jogador[i]
            cores = [p[0] if p[0]!='j' else None]
            jogo_potencial = [p]
            jogo_index = [i]
            for c in range(i+1,len(jogador)):
                if c not in em_uso:
                    copia = jogador[c]
                    if copia[0] not in cores and copia[1]==p[1]:
                        jogo_potencial.append(copia)
                        jogo_index.append(c)
                    if copia == 'j0':
                        jogo_index.append(c)
                        jogo_potencial.append(copia)
            if len(jogo_potencial)>=3:
                acoes.append((Jogo('trinca', jogo_potencial), jogo_index))
                em_uso += jogo_index
    
    em_uso = []
    index_j = search_element(jogador, 'j0')
    # sequencia
    for i in range(len(jogador)-2):
        if i not in em_uso:
            p = jogador[i]
            jogo_potencial = [p]
            jogo_index = [i]
            p_aux = p
            cont = 0
            while p_aux[1] == '0':
                cont +=1
                p_aux = jogador[cont]
            n = int(jogador[cont][1])-cont
            
            for c in range(1, len(jogador)):
                if c not in em_uso:
                    copia = jogador[c]
                    if int(copia[1]) == n+1 and copia[0]==p[0]:
                        jogo_potencial.append(copia)
                        jogo_index.append(c)
                        n+=1
                    
                    if index_j!=-1:
                        if (int(copia[1])==n+2 and copia[0]==p[0]) and index_j not in jogo_index:
                            jogo_index.append(index_j)
                            jogo_potencial.append(jogador[index_j])
                            jogo_potencial.append(copia)
                            jogo_index.append(c)
                            n+=2

                            
            if len(jogo_potencial)>=3:
                acoes.append((Jogo('sequencia', jogo_potencial), jogo_index))
                em_uso += jogo_index
    return acoes

def get_add_peca_mesa(mesa, jogador):
    acoes = []
    for pj_i in range(len(jogador)):
        pj = jogador[pj_i]
        for jm in mesa:
            if jm.can_add(pj):
                acoes.append((jm, pj_i))
    return acoes

def get_move_mesa(mesa):
    



# ação de jogo
def comprar_peca(pecas, jogador):
    for i in range(14):
        index = randint(0, len(pecas))
        jogador.append(pecas[index])
        pecas.remove(index)
    return pecas, jogador


# comeco de jogo
def cria_pecas():
    cores = ['c','r', 'y', 'b']
    pecas = []
    for e in range(2):
        for cor in cores:
            for i in range(1, 14):
                pecas.append(f'{cor}{i}')
    pecas.append('j0')
    pecas.append('j0')
    return pecas

def comecaJogo():
    pecas = cria_pecas()
    jogador = []
    for i in range(14):
        index = randint(0, len(pecas))
        jogador.append(pecas[index])
        pecas.remove(index)
    return pecas, jogador


if __name__ == "__main__":
    mesa = []
    pecas, jogador = comecaJogo()
    jogador.sort()
    resultado = get_add_peca_mesa(mesa, jogador)
    print(jogador)
    for r in resultado:
        print(str(r[0]), r[1])



        
        

        







