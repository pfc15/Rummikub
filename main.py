from numpy.random import randint
from jogo import Jogo
from util import search_element
from acao import *

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
        pecas.pop(index)
    return pecas, jogador


if __name__ == "__main__":
    mesa = [Jogo("trinca", ["b1", "c1", "y1", "r1"]), Jogo("sequencia", ["r2", "r3", "r4"], "r")]
    pecas, jogador = comecaJogo()
    jogador.sort()
    resultado = get_move_mesa(mesa)
    for x in mesa:
        print(str(x))
    mesa, jogador, pecas = faz_acao("move_mesa", resultado[0], mesa, jogador, pecas)
    for x in mesa:
        print(str(x))