# agente_treinamento.py

import os
import random
import numpy as np
import pickle

# --- Configurações do Jogo ---
LARGURA_MAPA = 40
ALTURA_MAPA = 20
PONTUACAO = 0

# --- Parâmetros do Q-Learning ---
EPSILON = 0.9
DECAY_RATE = 0.999
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.95

# Variável global para armazenar os obstáculos gerados
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
            
            # Evita gerar obstáculos em cima da cobra inicial ou de outros obstáculos
            if nova_posicao != (LARGURA_MAPA // 2, ALTURA_MAPA // 2) and nova_posicao not in OBSTACULOS:
                OBSTACULOS.append(nova_posicao)
                break

def get_estado(cobra, orb):
    """
    Retorna o estado atual do jogo, agora incluindo a posição relativa do orb e dos obstáculos.
    O estado é um vetor com 6 informações:
    1. Distância X do orb
    2. Distância Y do orb
    3. 1 se houver obstáculo/parede acima, 0 caso contrário
    4. 1 se houver obstáculo/parede abaixo, 0 caso contrário
    5. 1 se houver obstáculo/parede à esquerda, 0 caso contrário
    6. 1 se houver obstáculo/parede à direita, 0 caso contrário
    """
    dx_orb = np.sign(orb[0] - cobra[0][0])
    dy_orb = np.sign(orb[1] - cobra[0][1])
    
    x_cobra, y_cobra = cobra[0]
    
    # Verifica obstáculos e paredes nas 4 direções
    obstaculo_acima = 1 if (x_cobra, y_cobra - 1) in OBSTACULOS or y_cobra - 1 <= 0 else 0
    obstaculo_abaixo = 1 if (x_cobra, y_cobra + 1) in OBSTACULOS or y_cobra + 1 >= ALTURA_MAPA - 1 else 0
    obstaculo_esquerda = 1 if (x_cobra - 1, y_cobra) in OBSTACULOS or x_cobra - 1 <= 0 else 0
    obstaculo_direita = 1 if (x_cobra + 1, y_cobra) in OBSTACULOS or x_cobra + 1 >= LARGURA_MAPA - 1 else 0
    
    return (dx_orb, dy_orb, obstaculo_acima, obstaculo_abaixo, obstaculo_esquerda, obstaculo_direita)

def escolher_acao(estado, q_table, epsilon):
    """Escolhe uma ação com base no epsilon-greedy."""
    if random.uniform(0, 1) < epsilon:
        return random.choice(["cima", "baixo", "esquerda", "direita"])
    else:
        if estado not in q_table:
            q_table[estado] = {"cima": 0, "baixo": 0, "esquerda": 0, "direita": 0}
        return max(q_table[estado], key=q_table[estado].get)

def calcular_recompensa(colisao, comeu_orb):
    """Calcula a recompensa ou punição para a IA."""
    if colisao:
        return -100
    elif comeu_orb:
        return 10
    else:
        return -1

def aprender(estado_antigo, acao, recompensa, estado_novo, q_table):
    """Atualiza a tabela Q-Learning."""
    if estado_antigo not in q_table:
        q_table[estado_antigo] = {"cima": 0, "baixo": 0, "esquerda": 0, "direita": 0}
    if estado_novo not in q_table:
        q_table[estado_novo] = {"cima": 0, "baixo": 0, "esquerda": 0, "direita": 0}
    
    max_q_novo = max(q_table[estado_novo].values())
    
    q_table[estado_antigo][acao] += LEARNING_RATE * (
        recompensa + DISCOUNT_FACTOR * max_q_novo - q_table[estado_antigo][acao]
    )

def treinar_agente(num_episodios):
    """Função principal de treinamento para um único processo."""
    q_table = {}
    epsilon = EPSILON
    
    for episodio in range(num_episodios):
        cobra = [(LARGURA_MAPA // 2, ALTURA_MAPA // 2)]
        
        # NOVO: Gerar obstáculos aleatórios no início de cada episódio
        gerar_obstaculos()
        
        # Garante que o orb não apareça em cima da cobra ou de um obstáculo
        while True:
            orb_pos = (random.randint(1, LARGURA_MAPA - 2), random.randint(1, ALTURA_MAPA - 2))
            if orb_pos not in cobra and orb_pos not in OBSTACULOS:
                orb = orb_pos
                break
                
        game_over = False
        
        while not game_over:
            estado_antigo = get_estado(cobra, orb)
            acao = escolher_acao(estado_antigo, q_table, epsilon)
            
            x, y = cobra[0]
            if acao == "cima":
                y -= 1
            elif acao == "baixo":
                y += 1
            elif acao == "esquerda":
                x -= 1
            elif acao == "direita":
                x += 1
            
            nova_cabeca = (x, y)
            cobra.insert(0, nova_cabeca)
            
            # NOVO: A verificação de colisão agora inclui os obstáculos
            colisao = x <= 0 or x >= LARGURA_MAPA - 1 or y <= 0 or y >= ALTURA_MAPA - 1 or nova_cabeca in OBSTACULOS
            comeu = cobra[0] == orb
            
            if comeu:
                while True:
                    orb_pos = (random.randint(1, LARGURA_MAPA - 2), random.randint(1, ALTURA_MAPA - 2))
                    if orb_pos not in cobra and orb_pos not in OBSTACULOS:
                        orb = orb_pos
                        break
            else:
                cobra.pop()
            
            estado_novo = get_estado(cobra, orb)
            recompensa = calcular_recompensa(colisao, comeu)
            aprender(estado_antigo, acao, recompensa, estado_novo, q_table)
            
            if colisao:
                game_over = True
        
        epsilon *= DECAY_RATE
    
    return q_table