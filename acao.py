from numpy.random import randint
from jogo import Jogo
from util import search_element



def faz_acao(tipo, acao, estado):
    estado.acao+=1
    match tipo:
        case "add_peca": # acao = [index_jogo_mesa (qual jogo colocar), index_peca_jogador (qual peca colocar), index_peca_jogo (onde colocar no jogo)]
            estado.mesa[acao[0]].pecas.insert(acao[2], estado.jogador[acao[1]])
            estado.jogador.pop(acao[1])
        case "move_mesa": # acao = [index_jogo_mesa_remetente, index_jogo_mesa_destino, index_peca_remetente, index_peca_destino]
            peca = estado.mesa[acao[0]].pecas.pop(acao[2])
            estado.mesa[acao[1]].pecas.insert(acao[3], peca)
            estado.movimento+=1
            if estado.movimento>(5*len(estado.mesa))+5:
                faz_acao("compra_peca", [], estado)
            
        case "add_jogo": # acao = [lista_index_pecas_jogador]
            estado.mesa.append(acao[0])
            estado.jogador = [estado.jogador[x] for x in range(len(estado.jogador)) if x not in acao[1]]
        case "compra_peca": # acao = []
            estado.vez +=1
            if len(estado.pecas)>0:
                estado.movimento =0
                index = randint(0, len(estado.pecas))
                estado.jogador.append(estado.pecas[index])
                estado.jogador.sort()
                estado.pecas.pop(index)
        case "dupla_mesa": #acoes = [(index_jogo_mesa, index_peca_mesa), lista_index_peca_jogador, obj_jogo]
            estado.mesa[acao[0][0]].pecas.pop(acao[0][1])
            estado.jogador = [estado.jogador[x] for x in range(len(estado.jogador)) if x not in acao[1]]
            estado.mesa.append(acao[2])
    
    return estado


# get movimentos
def get_criar_jogo_jogador(estado):
    if len(estado.jogador) <3:
        return []
    acoes = []
    em_uso = []
    # trinca
    for i in range(len(estado.jogador)-2):
        if i not in em_uso:
            p = estado.jogador[i]
            cores = [p[0] if p[0]!='j' else None]
            jogo_potencial = [p]
            jogo_index = [i]
            for c in range(i+1,len(estado.jogador)):
                if c not in em_uso:
                    copia = estado.jogador[c]
                    if copia[0] not in cores and int(copia[1:])==int(p[1:]):
                        jogo_potencial.append(copia)
                        jogo_index.append(int(c))
                        cores.append(copia[0])
                    if copia == 'j0':
                        jogo_index.append(int(c))
                        jogo_potencial.append(copia)
            if len(jogo_potencial)>=3:
                acoes.append((Jogo('trinca', jogo_potencial), jogo_index))
                em_uso += jogo_index



                
    
    em_uso = []
    index_j = search_element(estado.jogador, 'j0')
    # sequencia
    for i in range(len(estado.jogador)-2):
        if i not in em_uso:
            p = estado.jogador[i]
            jogo_potencial = [p]
            jogo_index = [i]
            p_aux = p
            cont = 0
            while p_aux[1] == '0':
                cont +=1
                p_aux = estado.jogador[cont]
            n = int(estado.jogador[cont+i][1:])-cont
            
            for c in range(1, len(estado.jogador)):
                if c not in em_uso:
                    copia = estado.jogador[c]
                    if int(copia[1]) == n+1 and copia[0]==p[0]:
                        jogo_potencial.append(copia)
                        jogo_index.append(c)
                        n+=1
                    
                    if index_j!=-1:
                        if (int(copia[1])==n+2 and copia[0]==p[0]) and index_j not in jogo_index:
                            jogo_index.append(index_j)
                            jogo_potencial.append(estado.jogador[index_j])
                            jogo_potencial.append(copia)
                            jogo_index.append(c)
                            n+=2

                            
            if len(jogo_potencial)>=3:
                acoes.append((Jogo('sequencia', jogo_potencial), jogo_index))
                em_uso += jogo_index
    return acoes

def get_add_peca_mesa(estado):
    acoes = []
    for pj_i in range(len(estado.jogador)):
        pj = estado.jogador[pj_i]
        for jm_i in range(len(estado.mesa)):
            jm = estado.mesa[jm_i]
            index = jm.can_add(pj)
            if index!=-1:
                acoes.append((jm_i, pj_i, index))
    return acoes

def get_move_mesa(estado):
    acoes = []
    for doador_i in range(len(estado.mesa)):
        doador = estado.mesa[doador_i]
        if len(doador.pecas)>3:
            if doador.tipo =="trinca":
                for receptor_i in range(len(estado.mesa)):
                    receptor = estado.mesa[receptor_i]
                    if receptor_i != doador_i:
                        for ip in range(len(doador.pecas)):
                            index = receptor.can_add(doador.pecas[ip])
                            if index !=-1:
                                acoes.append((doador_i, receptor_i, ip, index))

            elif doador.tipo == "sequencia":
                for receptor_i in range(len(estado.mesa)):
                    receptor = estado.mesa[receptor_i]
                    if receptor_i!=doador_i:
                        index_comeco = receptor.can_add(doador.pecas[0])
                        if index_comeco!=-1:
                            acoes.append((doador_i, receptor_i, 0, index_comeco))
                        index_final = receptor.can_add(doador.pecas[-1])
                        if index_final!=-1:
                            acoes.append((doador_i, receptor_i, len(doador.pecas)-1, index_final))
                
    return acoes

def get_completa_dupla_jogador(estado):
    if len(estado.jogador) <2:
        return []
    duplas_trica = []
    duplas_sequencia = []
    em_uso = []
    # trinca
    for i in range(len(estado.jogador)-1):
        if i not in em_uso:
            p = estado.jogador[i]
            cores = [p[0] if p[0]!='j' else None]
            jogo_potencial = [p]
            jogo_index = [i]
            for c in range(i+1,len(estado.jogador)):
                if c not in em_uso:
                    copia = estado.jogador[c]
                    if copia[0] not in cores and int(copia[1:])==int(p[1:]):
                        jogo_potencial.append(copia)
                        jogo_index.append(int(c))
                        cores.append(copia[0])
                    if copia == 'j0':
                        jogo_index.append(int(c))
                        jogo_potencial.append(copia)
            if len(jogo_potencial)>=2:
                duplas_trica.append(jogo_index)
                em_uso += jogo_index
    
    em_uso = []
    index_j = search_element(estado.jogador, 'j0')
    # sequencia
    for i in range(len(estado.jogador)-1):
        if i not in em_uso:
            p = estado.jogador[i]
            jogo_potencial = [p]
            jogo_index = [i]
            p_aux = p
            cont = 0
            while p_aux[1] == '0':
                cont +=1
                p_aux = estado.jogador[cont]
            n = int(estado.jogador[cont+i][1:])-cont
            
            for c in range(1, len(estado.jogador)):
                if c not in em_uso:
                    copia = estado.jogador[c]
                    if int(copia[1]) == n+1 and copia[0]==p[0]:
                        jogo_potencial.append(copia)
                        jogo_index.append(c)
                        n+=1
                    
                    if index_j!=-1:
                        if (int(copia[1])==n+2 and copia[0]==p[0]) and index_j not in jogo_index:
                            jogo_index.append(index_j)
                            jogo_potencial.append(estado.jogador[index_j])
                            jogo_potencial.append(copia)
                            jogo_index.append(c)
                            n+=2

                            
            if len(jogo_potencial)>=2:
                duplas_sequencia.append(jogo_index)
                em_uso += jogo_index
    
    acoes = []
    for i_mesa in range(len(estado.mesa)):
        jogo_mesa = estado.mesa[i_mesa]
        if len(jogo_mesa.pecas)>3:
            if jogo_mesa.tipo == "trinca":
                for i_peca in range(len(jogo_mesa.pecas)):
                    peca = jogo_mesa.pecas[i_peca]
                    for jogo_pecas in duplas_trica:
                        pecas = [estado.jogador[x] for x in jogo_pecas]
                        jogo = Jogo("trinca", pecas[:])
                        index = jogo.can_add(peca)
                        if index !=-1:
                            jogo.pecas.insert(index, peca)
                            acoes.append([(i_mesa, i_peca), jogo_pecas, jogo])
                    
                    for jogo_pecas in duplas_sequencia:
                        pecas = [estado.jogador[x] for x in jogo_pecas]
                        jogo = Jogo("sequencia", pecas[:], cor=pecas[0][0])
                        index = jogo.can_add(jogo_mesa.pecas[i_peca])
                        if index != -1:
                            jogo.pecas.insert(index, peca)
                            acoes.append([(i_mesa, i_peca), jogo_pecas, jogo])
            elif jogo_mesa.tipo == "sequencia":
                for jogo_pecas in duplas_sequencia:
                    pecas = [estado.jogador[x] for x in jogo_pecas]
                    jogo = Jogo("sequencia", pecas[:], cor=pecas[0][0])
                    index = jogo.can_add(jogo_mesa.pecas[0])
                    if index != -1:
                        jogo.pecas.insert(index, jogo_mesa.pecas[0])
                        acoes.append([(i_mesa, 0), jogo_pecas, jogo])
                    index = jogo.can_add(jogo_mesa.pecas[-1])
                    if index != -1:
                        jogo.pecas.insert(index, jogo_mesa.pecas[-1])
                        acoes.append([(i_mesa, len(jogo_mesa.pecas)-1), jogo_pecas, jogo])
                
                for jogo_pecas in duplas_trica:
                    pecas = [estado.jogador[x] for x in jogo_pecas]
                    jogo = Jogo("trinca", pecas[:])
                    index = jogo.can_add(jogo_mesa.pecas[0])
                    if index != -1:
                        jogo.pecas.insert(index, jogo_mesa.pecas[0])
                        acoes.append([(i_mesa, 0), jogo_pecas, jogo])
                    index = jogo.can_add(jogo_mesa.pecas[-1])
                    if index != -1:
                        jogo.pecas.insert(index, jogo_mesa.pecas[-1])
                        acoes.append([(i_mesa, len(jogo_mesa.pecas)-1), jogo_pecas, jogo])
    
    return acoes
