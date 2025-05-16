from numpy.random import randint
from jogo import Jogo
from util import search_element



def faz_acao(tipo, acao, mesa, jogador, pecas):
    print(acao)
    match tipo:
        case "add_peca":
            mesa[acao[0]].pecas.insert(acao[2], jogador[acao[1]])
            jogador.remove(acao[1])
        case "move_mesa":
            peca = mesa[acao[0]].pecas.pop(acao[2])
            mesa[acao[1]].pecas.insert(acao[3], peca)
        case "add_jogo":
            mesa.append(acao[0])
            jogador = [jogador[x] for x in range(jogador) if x not in acao[1]]
        case "compra_peca":
            for i in range(14):
                index = randint(0, len(pecas))
                jogador.append(pecas[index])
                pecas.remove(index)
    return mesa, jogador, pecas


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
        for jm_i in range(len(mesa)):
            jm = jm_i
            index = jm.can_add(pj)
            if index!=-1:
                acoes.append((jm_i, pj_i, index))
    return acoes

def get_move_mesa(mesa):
    acoes = []
    for doador_i in range(len(mesa)):
        doador = mesa[doador_i]
        if len(doador.pecas)>3:
            if doador.tipo =="trinca":
                for receptor_i in range(len(mesa)):
                    receptor = mesa[receptor_i]
                    if receptor_i != doador_i:
                        for ip in range(len(doador.pecas)):
                            index = receptor.can_add(doador.pecas[ip])
                            if index !=-1:
                                print(doador.pecas[ip], str(doador), str(receptor))
                                acoes.append((doador_i, receptor_i, ip, index))

            elif doador.tipo == "sequencia":
                for receptor_i in range(mesa):
                    receptor = mesa[receptor_i]
                    if receptor_i!=doador_i:
                        index_comeco = receptor.can_add(doador.pecas[0])
                        if index_comeco!=-1:
                            acoes.append((doador_i, receptor_i, 0, index_comeco))
                        index_final = receptor.can_add(doador.pecas[-1])
                        if index_final!=-1:
                            acoes.append((doador_i, receptor_i, len(doador.pecas)-1, index_final))
                
    return acoes

