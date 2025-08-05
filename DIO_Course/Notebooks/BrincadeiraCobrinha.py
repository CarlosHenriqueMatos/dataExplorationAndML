# jogar.py

import os
import random
import time
import pickle
import numpy as np

# --- Carregar Tabela Q-Learning Treinada ---
try:
    with open("q_table_paralela.pkl", "rb") as f:
        q_table = pickle.load(f)
    print("Tabela Q-Learning carregada com sucesso.")
except FileNotFoundError:
    print("Erro: 'q_table_paralela.pkl' não encontrado. Por favor, execute o treinamento primeiro.")
    exit()

# --- Configurações do Jogo ---
LARGURA_MAPA = 40
ALTURA_MAPA = 20
PONTUACAO = 0

# --- Variável para os obstáculos ---
OBSTACULOS = []

def gerar_obstaculos():
    """Gera obstáculos aleatoriamente no mapa."""
    global OBSTACULOS
    OBSTACULOS = []
    
    # Define o número de obstáculos a serem gerados
    num_obstaculos = 15
    
    for _ in range(num_obstaculos):
        while True:
            posicao_x = random.randint(1, LARGURA_MAPA - 2)
            posicao_y = random.randint(1, ALTURA_MAPA - 2)
            nova_posicao = (posicao_x, posicao_y)
            
            if nova_posicao != (LARGURA_MAPA // 2, ALTURA_MAPA // 2) and nova_posicao not in OBSTACULOS:
                OBSTACULOS.append(nova_posicao)
                break

# --- Posição inicial da cobra e do orb ---
cobra = [(LARGURA_MAPA // 2, ALTURA_MAPA // 2)]

# Gerar obstáculos e orb inicial
gerar_obstaculos()

while True:
    orb_pos = (random.randint(1, LARGURA_MAPA - 2), random.randint(1, ALTURA_MAPA - 2))
    if orb_pos not in cobra and orb_pos not in OBSTACULOS:
        orb = orb_pos
        break

# --- Estado inicial do jogo ---
direcao = "direita"
game_over = False

def limpar_tela():
    os.system("cls" if os.name == "nt" else "clear")

def desenhar_mapa():
    limpar_tela()
    print("SLITHER.IO - AGENTE JOGANDO")
    print(f"Pontuação: {PONTUACAO}\n")
    
    print("#" * LARGURA_MAPA)
    for y in range(ALTURA_MAPA):
        for x in range(LARGURA_MAPA):
            posicao = (x, y)
            if x == 0 or x == LARGURA_MAPA - 1 or y == 0 or y == ALTURA_MAPA - 1:
                print("#", end="")
            elif posicao in OBSTACULOS:
                print("X", end="")
            elif posicao == cobra[0]:
                print("O", end="")
            elif posicao in cobra[1:]:
                print("o", end="")
            elif posicao == orb:
                print("*", end="")
            else:
                print(" ", end="")
        print()
    print("#" * LARGURA_MAPA)

def mover_cobra():
    global direcao
    x, y = cobra[0]
    if direcao == "cima":
        y -= 1
    elif direcao == "baixo":
        y += 1
    elif direcao == "esquerda":
        x -= 1
    elif direcao == "direita":
        x += 1
    
    nova_cabeca = (x, y)
    cobra.insert(0, nova_cabeca)

def verificar_colisao():
    global game_over
    x, y = cobra[0]
    if x <= 0 or x >= LARGURA_MAPA - 1 or y <= 0 or y >= ALTURA_MAPA - 1 or (x, y) in OBSTACULOS:
        game_over = True
    
def verificar_comida():
    global PONTUACAO, orb
    if cobra[0] == orb:
        PONTUACAO += 10
        while True:
            orb_pos = (random.randint(1, LARGURA_MAPA - 2), random.randint(1, ALTURA_MAPA - 2))
            if orb_pos not in cobra and orb_pos not in OBSTACULOS:
                orb = orb_pos
                break
    else:
        cobra.pop()

def get_estado(cobra, orb):
    dx_orb = np.sign(orb[0] - cobra[0][0])
    dy_orb = np.sign(orb[1] - cobra[0][1])
    
    x_cobra, y_cobra = cobra[0]
    
    obstaculo_acima = 1 if (x_cobra, y_cobra - 1) in OBSTACULOS or y_cobra - 1 <= 0 else 0
    obstaculo_abaixo = 1 if (x_cobra, y_cobra + 1) in OBSTACULOS or y_cobra + 1 >= ALTURA_MAPA - 1 else 0
    obstaculo_esquerda = 1 if (x_cobra - 1, y_cobra) in OBSTACULOS or x_cobra - 1 <= 0 else 0
    obstaculo_direita = 1 if (x_cobra + 1, y_cobra) in OBSTACULOS or x_cobra + 1 >= LARGURA_MAPA - 1 else 0
    
    return (dx_orb, dy_orb, obstaculo_acima, obstaculo_abaixo, obstaculo_esquerda, obstaculo_direita)

def tomar_decisao_treinada():
    global direcao
    estado_atual = get_estado(cobra, orb)
    
    if estado_atual in q_table:
        direcao = max(q_table[estado_atual], key=q_table[estado_atual].get)
    else:
        direcao = random.choice(["cima", "baixo", "esquerda", "direita"])

# --- Loop Principal do Jogo ---
while not game_over:
    desenhar_mapa()
    tomar_decisao_treinada()
    mover_cobra()
    verificar_colisao()
    verificar_comida()
    
    velocidade = 0.1 - (len(cobra) * 0.001)
    if velocidade < 0.05:
        velocidade = 0.05
    time.sleep(velocidade)

# --- Fim do Jogo ---
limpar_tela()
print("Fim de jogo!")
print(f"Sua pontuação final é: {PONTUACAO}")