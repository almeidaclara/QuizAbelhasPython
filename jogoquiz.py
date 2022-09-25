import random
from operator import itemgetter
import pygame


def adicionar():
    f = open('perguntasabelhas.txt', 'r', encoding='utf8')
    texto = f.readlines()
    global perguntas
    perguntas = []
    f.close()
    for x in texto:
        pergunta = texto[0:6]
        for i in range(0, 6):
            texto.pop(0)
        perguntas.append(pergunta)
    # essa parte acima transforma o arquivo em uma lista de listas
    return perguntas


def buscar():
    for x in range(0, len(perguntas)):
        print('-' * 50)
        print('Pergunta {}:' .format(x))
        for y in perguntas[x]:
            print(y, end='')
    return perguntas


def remover():
    print('Remoção de perguntas: ')
    buscar()
    pergunta_remover = input('Digite o número da pergunta a ser removida: ')
    while pergunta_remover.isdigit() is False or int(pergunta_remover) > len(perguntas):
        pergunta_remover = input('Valor inválido. Digite uma das opções acima ')
        # assim não serão permitidos valores não numericos ou fora do range
    perguntas.remove(perguntas[int(pergunta_remover)])
    print('Pergunta {} removida com sucesso.'.format(pergunta_remover))
    return perguntas


def alterar():
    buscar()
    pergunta_alterar = input('Escolha a questão que você deseja modificar: ')
    while pergunta_alterar.isdigit() is False or int(pergunta_alterar) > len(perguntas):
        pergunta_alterar = input('Valor inválido. Digite uma das opções acima ')
    print('Pergunta escolhida:', pergunta_alterar)
    pergunta_alterar = int(pergunta_alterar)
    for x in perguntas[pergunta_alterar]:
        print(x, end='')
    print('-'*100, '\nO que você deseja alterar na questão {}?' .format(pergunta_alterar))
    print('0-O texto do enunciado\n1-O texto da alternativa a)\n2-O texto da alternativa b)\n'
          '3-O texto da alternativa c)\n4-A resposta')
    opcao = input('Qual a opção desejada?')
    while opcao not in '01234':
        opcao = input('Valor inválido. Digite uma das opções acima ')
    opcao = int(opcao)
    print('- '*50, '\nTexto original:', perguntas[pergunta_alterar][opcao], end='')
    texto_novo = input('Digite novo texto: ')
    perguntas[pergunta_alterar][opcao] = texto_novo + '\n'
    print('Pergunta {} modificada com sucesso para:' .format(pergunta_alterar))
    for x in perguntas[pergunta_alterar]:
        print(x, end='')
    print('~'*50)
    print('0-Voltar ao menu anterior\n1-Modificar outra pergunta')
    continua = input('Digite a opção desejada')
    while continua not in '01':
        continua = input('Valor inválido. Digite uma das opções descritas')
    if continua in '1':
        alterar()


def jogar():
    # o jogo em si
    perguntas_jogo = perguntas.copy()
    # criei essa cópia para poder reutilizar a lista inicial caso o usuario queira repetir as perguntas do 0
    perguntas_ja_feitas = []
    placar = []
    while True:
        print('=-' * 50)
        pontos = 0
        jogador = input('Digite o nome do jogador: ')
        pontuacao = [jogador]
        for c in range(0, 5):
            questao = random.choice(perguntas_jogo)
            print(questao[0], questao[1], questao[2], questao[3], questao[4], end='')
            resposta = input('Qual a alternativa correta?')
            if resposta not in 'AaBbCc':
                print('Valor inválido. Serão aceitas apenas a, b ou c como respostas.')
            else:
                if resposta in questao[5]:
                    print('Correto!')
                    pygame.mixer.music.load('success-chime.mp3')
                    pygame.mixer.music.play()
                    if 'FÁCIL' in questao[0]:
                        pontos += 1
                    elif 'MÉDIO' in questao[0]:
                        pontos += 2
                    elif 'DIFÍCIL' in questao[0]:
                        pontos += 3
                    # essa parte dá pontuação diferente para o nível das perguntas
                else:
                    print('Incorreto. A resposta correta é', questao[5])
                    pygame.mixer.music.load('sound-fail-fallo.mp3')
                    pygame.mixer.music.play(start=2.8)
            print("-" * 100)
            perguntas_ja_feitas.append(questao)
            perguntas_jogo.remove(questao)
        pontuacao.append(pontos)
        placar.append(pontuacao)
        # abaixo, criando o arquivo que armazena a pontuacao de cada jogador
        g = open('ranking.txt', 'a')
        g.write('{}\n'.format(jogador))
        g.write(str('{}\n'.format(pontos)))
        g.close()
        print('{}, sua pontuação foi {}'.format(pontuacao[0], pontuacao[1]))
        if len(perguntas_jogo) < 5:
            print('Não há perguntas suficientes para continuar. Jogo encerrado')
            break
        continuar = '0'
        while continuar not in 'NnSs':
            continuar = input('Próximo jogador? (s/n)')
        if continuar in 'Nn':
            print('Jogo encerrado. Voltando ao menu inicial')
            break
    placar_ordenado = sorted(placar, key=itemgetter(1), reverse=True)
    print('RANKING DOS JOGADORES')
    for x in placar_ordenado[:10]:
        print(x)
    # essa parte acima imprime o ranking dos 10 melhores jogadores(se tiver) com pontuação em ordem decrescente


# programa principal
adicionar()
while True:
    print('-' * 100, '\nQUIZ DAS ABELHAS\nMENU INICIAL\nO que você deseja fazer?\n0-Encerrar o programa\n1-Jogar\n'
                     '2-Editar perguntas')
    pygame.init()
    pygame.mixer.music.load('abelha.mp3')
    pygame.mixer.music.play()
    escolha_menu = input('Digite a opção escolhida: ')
    if escolha_menu in '0':
        break
    while escolha_menu not in '12':
        escolha_menu = input('Você digitou um valor inválido. Digite uma das opções descritas acima')
    if escolha_menu in '1':
        jogar()
    elif escolha_menu in '2':
        print('-'*100, '\nMENU DE EDIÇÃO\n0-Voltar ao menu inicial\n3-Ver as perguntas\n4-Remover pergunta\n'
              '5-Alterar pergunta')
        escolha_menu = input('Digite a opção desejada: ')
        while escolha_menu not in '03456':
            escolha_menu = input('Você digitou um valor inválido. Digite uma das opções descritas acima')
        if escolha_menu in '3':
            print('Visualização de perguntas: ')
            buscar()
            escolha_menu = '2'
        elif escolha_menu in '4':
            remover()
            escolha_menu = '2'
        elif escolha_menu in '5':
            alterar()
            escolha_menu = '2'
print('Programa encerrado. Obrigada por jogar!!', '\U0001F41D'*5, '\nInformação é poder.'
      ' Sem abelhas não há biodiversidade.')
