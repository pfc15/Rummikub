from numpy.random import randint
from jogo import Jogo
from util import search_element
from acao import *
from estado import Estado
import time 
# comeco de jogo

def melhorar(estado):
    cria_jogo = get_criar_jogo_jogador(estado)
    if len(cria_jogo)>0:
        index = randint(0, len(cria_jogo))
        return faz_acao("add_jogo", cria_jogo[index], estado)

    cria_jogo_dupla = get_completa_dupla_jogador(estado)
    if len(cria_jogo_dupla)>0:
        index =randint(0,len(cria_jogo_dupla))
        return faz_acao("dupla_mesa", cria_jogo_dupla[index], estado)
    add_peca = get_add_peca_mesa(estado)
    if len(add_peca)>0:
        index = randint(0, len(add_peca))
        return faz_acao("add_peca", add_peca[index], estado)
    movimento = get_move_mesa(estado)
    if len(movimento)>0:
        index=randint(0,len(movimento))
        return faz_acao("move_mesa", movimento[index], estado)
    return faz_acao("compra_peca", [], estado)


if __name__ == "__main__":
    jogos = []
    start_time = time.time()
    estado_inicial = Estado([],[],[], comeco=True)
    estado_atual = Estado(estado_inicial.mesa[:], estado_inicial.jogador[:], estado_inicial.pecas[:])
    
    geracao =0
    restart = 0
    while len(estado_atual.jogador)>0:
        geracao+=1
        melhorar(estado_atual)
        # print(f'geracao: {geracao}: estado: {estado_atual.to_string()} restart: {restart}')
        if geracao== 10000:
            estado_atual = Estado(estado_inicial.mesa[:], estado_inicial.jogador[:], estado_inicial.pecas[:])
            restart +=1
            geracao = 0
    print('-=-'*20)
    print(f'geracao: {geracao+(restart*10000)}: estado: {estado_atual.to_string()} restart: {restart}')
    print("--- %s seconds ---" % (time.time() - start_time))

