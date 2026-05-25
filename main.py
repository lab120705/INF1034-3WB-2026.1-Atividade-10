import pygame
import random

pygame.init()
largura, altura = 1000, 700
tela = pygame.display.set_mode((largura, altura))

# fontes
fonte_titulo = pygame.font.SysFont("Arial", 40, bold=True)
fonte_peq = pygame.font.SysFont("Arial", 18)
fonte_input = pygame.font.SysFont("Courier", 25)

# estado do menu
estado = 0

# lista 1
lista1_bruta = []
for i in range(65):
    lista1_bruta.append(random.randint(0, 100))

# lista 2
faixas_h2 = ["0-10", "11-20", "21-30", "31-40", "41-50", "51-60"]
contagem_h2 = []
soma_maxima = 100
soma_atual = 0
for i in range(len(faixas_h2)):
    if soma_atual < soma_maxima:
        valor = random.randint(0, (soma_maxima - soma_atual) // 2 + 5)
        contagem_h2.append(valor)
        soma_atual += valor
    else:
        contagem_h2.append(0)

# lista 3
texto_input = ""
lista3_processada = []


# funcoes
def desenha_eixos(titulo, x_labels, y_max):
    
    if y_max <= 0:
        y_max = 1
        
    pygame.draw.line(tela, (0, 0, 0), (100, 150), (100, 600), 3)
    pygame.draw.line(tela, (0, 0, 0), (100, 600), (900, 600), 3)

    # titulo grafico
    img_tit = fonte_titulo.render(titulo, True, (0, 0, 0))
    tela.blit(img_tit, (largura // 2 - img_tit.get_width() // 2, 50))

    passo_y = 450 / 5
    for i in range(6):
        valor_y = int((y_max / 5) * i)
        pos_y = 600 - (i * passo_y)
        pygame.draw.line(tela, (200, 200, 200), (95, pos_y), (900, pos_y), 1)
        txt = fonte_peq.render(str(valor_y), True, (50, 50, 50))
        tela.blit(txt, (60, pos_y - 10))


def processar_input_usuario(texto):
    
    numeros = []
    partes = texto.split(",")
    for p in partes:
        if p.strip().isdigit():
            numeros.append(int(p.strip()))
    return numeros


# loop principal
rodando = True
while rodando:
    tela.fill((255, 255, 255))

    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            rodando = False

        if ev.type == pygame.KEYDOWN:
            # meu interativo extra
            if ev.key == pygame.K_RIGHT:
                estado = (estado + 1) % 4
            if ev.key == pygame.K_LEFT:
                estado = (estado - 1) % 4

            # logica de digitacao extra
            if estado == 0:
                if ev.key == pygame.K_BACKSPACE:
                    texto_input = texto_input[:-1]
                elif ev.key == pygame.K_RETURN:
                    lista3_processada = processar_input_usuario(texto_input)
                    estado = 3
                else:
                    if ev.unicode in "0123456789,":
                        texto_input += ev.unicode

    # tela 0 input
    if estado == 0:
        msg = fonte_titulo.render("ENTRADA DE DADOS (H3)", True, (0, 0, 0))
        instrucao = fonte_peq.render("Digite numeros separados por virgula e aperte ENTER:", True, (50, 50, 50))
        tela.blit(msg, (largura // 2 - msg.get_width() // 2, 200))
        tela.blit(instrucao, (largura // 2 - instrucao.get_width() // 2, 260))

        # caixa de texto
        pygame.draw.rect(tela, (240, 240, 240), (200, 300, 600, 50))
        pygame.draw.rect(tela, (0, 0, 0), (200, 300, 600, 50), 2)
        txt_surf = fonte_input.render(texto_input, True, (0, 0, 255))
        tela.blit(txt_surf, (210, 310))

        aviso = fonte_peq.render("Use as SETAS do teclado para navegar entre os graficos", True, (150, 0, 0))
        tela.blit(aviso, (largura // 2 - aviso.get_width() // 2, 600))

    # tela 1 histograma
    elif estado == 1:
        contagem = [0, 0, 0, 0, 0]
        for n in lista1_bruta:
            if n <= 20: contagem[0] += 1
            elif n <= 40: contagem[1] += 1
            elif n <= 60: contagem[2] += 1
            elif n <= 80: contagem[3] += 1
            else: contagem[4] += 1

        desenha_eixos("H1: Numeros Aleatorios (0-100)", ["0-20", "21-40", "41-60", "61-80", "81-100"], 30)

        # barras desenho
        for i in range(5):
            largura_barra = 120
            altura_barra = (contagem[i] / 30) * 450
            cor = ((i * 50) % 255, (i * 100) % 255, 200)
            x_pos = 150 + (i * 150)
            pygame.draw.rect(tela, cor, (x_pos, 600 - altura_barra, largura_barra, altura_barra))
            lbl = fonte_peq.render(f"F{i+1}", True, (0, 0, 0))
            tela.blit(lbl, (x_pos + 45, 610))

    # tela 2 histograma 2
    elif estado == 2:
        desenha_eixos("H2: Frequencias Aleatorias (Soma < 100)", faixas_h2, 50)
        for i in range(len(contagem_h2)):
            largura_barra = 80
            altura_barra = (contagem_h2[i] / 50) * 450
            x_pos = 120 + (i * 110)
            pygame.draw.rect(tela, (255, i * 30, 50), (x_pos, 600 - altura_barra, largura_barra, altura_barra))
            lbl = fonte_peq.render(faixas_h2[i], True, (0, 0, 0))
            tela.blit(lbl, (x_pos + 5, 610))

    # tela 3 histograma 3
    elif estado == 3:
        contagem = [0, 0, 0, 0]
        for n in lista3_processada:
            if n < 10: contagem[0] += 1
            elif n < 20: contagem[1] += 1
            elif n < 30: contagem[2] += 1
            else: contagem[3] += 1

        maior_valor = max(contagem) if len(contagem) > 0 and max(contagem) > 0 else 10
        desenha_eixos("H3: Dados do Usuario", ["<10", "<20", "<30", "30+"], maior_valor)

        for i in range(4):
            largura_barra = 150
            altura_barra = (contagem[i] / maior_valor) * 450
            x_pos = 180 + (i * 180)
            pygame.draw.rect(tela, (0, 150, i * 40 + 50), (x_pos, 600 - altura_barra, largura_barra, altura_barra))
            lbl = fonte_peq.render(["<10", "<20", "<30", "30+"][i], True, (0, 0, 0))
            tela.blit(lbl, (x_pos + 50, 610))

    pygame.display.update()

pygame.quit()