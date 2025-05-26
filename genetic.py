from numpy.random import randint, choice
from jogo import Jogo
from util import bubble_sort
from acao import *
from estado import Estado
import time 
from queue import Queue
import copy
import threading

def mutacao(pai):
    filho = copy.deepcopy(pai)
    for i in range(3):
        tipo_acao = ""
        index = randint(0,5)
        acoes = []
        while len(acoes)==0:
            if len(filho.mesa)<=2:
                index = (index+1)%6
                tipo_acao = ["add_jogo", "add_jogo", "add_jogo", "dupla_mesa", "add_peca", "compra_peca"][index]
            else:
                index = (index+1)%4
                tipo_acao = ["add_jogo", "dupla_mesa", "add_peca", "move_mesa"][index]
                if tipo_acao=='move_mesa':
                    acoes = get_move_mesa(filho)
                    if len(acoes)==0:
                        filho.movimento+=1
                        if filho.movimento>(2*len(filho.mesa))+5:
                            faz_acao("compra_peca", [], filho)
            match tipo_acao:
                case "add_jogo":
                    acoes = get_criar_jogo_jogador(filho)
                case "dupla_mesa":
                    acoes = get_completa_dupla_jogador(filho)
                case "add_peca":
                    acoes = get_add_peca_mesa(filho)
                case "move_mesa":
                    # print('move')
                    acoes = get_move_mesa(filho)
                case "compra_peca":
                    acoes = [[]]
        if len(acoes)>=2:
            acoes = acoes[randint(0,1)]
        elif len(acoes)==1:
            acoes = acoes[0]
            
        faz_acao(tipo_acao, acoes[:], filho)
        # print(acoes)
    return filho


def nova_geracao(pai, fila):
    
    for i in range(3):
        atual = copy.deepcopy(pai)
        nova_gercao = mutacao(atual)
        fila.put(nova_gercao)
    


if __name__ == "__main__":
    start_time = time.time()
    pai = Estado([], [], [],comeco=True)
    quant_geracao = 0
    geracao = [mutacao(pai) for i in range(10)]
    acabou = False
    while True:
        quant_geracao+=1
        melhor_geracao = bubble_sort(geracao)[:5]
        
        geracao = []
        threads = []
        q = Queue()
        print(f'-='*25)
        print(f'geracao: {quant_geracao}')
        for g in melhor_geracao:
            print(f"fitness: ", g.get_fitness())
            thread = threading.Thread(target=nova_geracao, args=[g, q])
            thread.start()
            threads.append(thread)

        
        for t in threads:
            t.join()
        resultados = []
    
        while not q.empty():
            geracao.append(q.get())
        
        if len(melhor_geracao[0].jogador)==0: 
            break

    print(f'{quant_geracao}: {melhor_geracao[0].to_string()}; tempo: {time.time()-start_time}')

    
    
    

