import pygame
import os
import random
import neat

#Se quiser tirar a AI e jogar, manualmente, coloca False
aiJogando = True
geracao = 0


telaLargura = 500
telaAltura = 800

# pygame.transform para aumentar a escala da imagem
# os.path para identificar em que pasta a imagem está
imagemCano = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'pipe.png')))
imagemChao = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'base.png')))
imagemBackground = pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bg.png')))
imagemPassaros = [pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird1.png'))),
                  pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird2.png'))),
                  pygame.transform.scale2x(pygame.image.load(os.path.join('imgs', 'bird3.png')))]

# criar a fonte do que estará escrito na tela do jogo
pygame.font.init()
fontePontos = pygame.font.SysFont('arial', 50)


# Criando as classes
class Passaro:
    imgs = imagemPassaros
    # Criando as animações de rotação
    rotacaoMaxima = 25
    velocidadeRotacao = 20
    tempoAnimacao = 5

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 0
        self.altura = self.y
        self.tempo = 0
        self.contagemImagem = 0
        self.imagem = self.imgs[0]

    def pular(self):
        self.velocidade = -10.5
        self.tempo = 0
        self.altura = self.y

    def mover(self):
        # Vamos calcular o deslocamento
        self.tempo += 1
        deslocamento = 1.5 * (self.tempo ** 2) + self.velocidade * self.tempo

        # Vamos restringir o deslocamento para que o pássaro não saia andando loucamente
        if deslocamento > 16:
            deslocamento = 16
        elif deslocamento < 0:
            deslocamento -= 2

        self.y += deslocamento

        # o ângulo do pássaro
        # self.y é a altura máxima que ele continuará com esse ângulo para que o jogo não fique feio
        if deslocamento < 0 or self.y < (self.altura + 50):
            if self.angulo < self.rotacaoMaxima:
                self.angulo = self.rotacaoMaxima
        else:
            if self.angulo > -90:
                self.angulo -= self.velocidadeRotacao

    def desenhar(self, tela):
        # definir qual imagem do pássaro vai usar para o bater de asas
        self.contagemImagem += 1

        if self.contagemImagem < self.tempoAnimacao:
            self.imagem = self.imgs[0]
        elif self.contagemImagem < self.tempoAnimacao * 2:
            self.imagem = self.imgs[1]
        elif self.contagemImagem < self.tempoAnimacao * 3:
            self.imagem = self.imgs[2]
        elif self.contagemImagem < self.tempoAnimacao * 4:
            self.imagem = self.imgs[1]
        elif self.contagemImagem >= self.tempoAnimacao * 4 + 1:
            self.imagem = self.imgs[0]
            self.contagemImagem = 0

        # se o pássaro estiver caindo, não precisa bater asas
        # lembrando que quando ele sobe, o eixo y é negativo; quando ele desce, o eixo y é positivo
        if self.angulo <= -80:
            self.imagem = self.imgs[1]
            self.contagemImagem = self.tempoAnimacao * 2

        # vamos desenhar a imagem
        imagemRotacionada = pygame.transform.rotate(self.imagem, self.angulo)
        # posicionar a imagem ao topo esquerdo, mas no centro de um retângulo
        posCentroImagem = self.imagem.get_rect(topleft=(self.x, self.y)).center
        retangulo = imagemRotacionada.get_rect(center=posCentroImagem)
        # qualquer desenho na tela, precisa usar esse próximo comando
        # coloca o nome tela lá no "def desenhar"
        tela.blit(imagemRotacionada, retangulo.topleft)

    # criar uma máscara para que o jogo leia os pixels e não o retângulo em que a imagem está dentro
    def get_mask(self):
        return pygame.mask.from_surface(self.imagem)


class Cano:
    distancia = 200
    velocidade = 5

    def __init__(self, x):
        self.x = x
        self.altura = 0
        self.posTopo = 0
        self.posBase = 0
        self.canoTopo = pygame.transform.flip(imagemCano, False, True)
        self.canoBase = imagemCano
        self.passou = False
        self.definir_altura()

    def definir_altura(self):
        # criar um limite de range para que os canos não fiquem em posição impossível
        # se a tela tem 800 de altura (indicado no início do código), colocamos um intervalo de 50 e 450
        self.altura = random.randrange(50, 450)
        # definindo o tamanho do cano
        self.posTopo = self.altura - self.canoTopo.get_height()
        self.posBase = self.altura + self.distancia

    # como mover o cano
    def mover(self):
        self.x -= self.velocidade  # está negativo porque, no eixo x à esquerda, é negativo.

    def desenhar(self, tela):
        tela.blit(self.canoTopo, (self.x, self.posTopo))
        tela.blit(self.canoBase, (self.x, self.posBase))

    # o jogo precisa reconhecer a colisão caso haja uma
    def colidir(self, passaro):
        passaro_mask = passaro.get_mask()
        topo_mask = pygame.mask.from_surface(self.canoTopo)
        base_mask = pygame.mask.from_surface(self.canoBase)

        # calculando a distância do pássaro (que precisa ser inteiro) e a posição dos canos
        distanciaTopo = (self.x - passaro.x, self.posTopo - round(passaro.y))
        distanciaBase = (self.x - passaro.x, self.posBase - round(passaro.y))


        # ponto de colisão
        topoPonto = passaro_mask.overlap(topo_mask, distanciaTopo)
        basePonto = passaro_mask.overlap(base_mask, distanciaBase)

        # se encostar, há colisão; se não, não há colisão
        if basePonto or topoPonto:
            return True
        else:
            return False


class Chao:
    velocidade = 5
    largura = imagemChao.get_width()  # ele diz que a largura do chão é o ponto inicial mais a largura da tela.
    imagem = imagemChao

    # usando essa def para criar o chão e o segundo chão (que ficará escondido até o 1º chão terminar de rodar na tela
    def __init__(self, y):
        self.y = y
        self.x1 = 0
        self.x2 = self.largura

    def mover(self):
        self.x1 -= self.velocidade
        self.x2 -= self.velocidade

        # fazendo o chão 1 voltar ao início depois de já ter andado toda a largura da tela
        # isso faz um ciclo entre o chão 1 e 2
        if self.x1 + self.largura < 0:  # ou seja, já terminou a tela
            self.x1 = self.x2 + self.largura  # ou seja, voltou ao início da tela
        if self.x2 + self.largura < 0:
            self.x2 = self.x1 + self.largura

    def desenhar(self, tela):
        tela.blit(self.imagem, (self.x1, self.y))
        tela.blit(self.imagem, (self.x2, self.y))


def desenhar_tela(tela, passaros, canos, chao, pontos):
    tela.blit(imagemBackground, (0, 0))
    for passaro in passaros:
        passaro.desenhar(tela)  # usa esse laço porque haverá + de 1 pássaro para a IA treinar
    for cano in canos:
        cano.desenhar(tela)

    # criando o texto da pontuação na tela. O 1 é para renderizar e o 255 é a cor branca
    texto = fontePontos.render(f"Pontuação: {pontos}", 1, (255, 255, 255))
    # o texto estará na ponta direita a 10 metros do limite
    tela.blit(texto, (telaLargura - 10 - texto.get_width(), 10))

    if aiJogando:
        texto = fontePontos.render(f"Geração: {geracao}", 1, (255, 255, 255))
        tela.blit(texto, (10, 10))

    chao.desenhar(tela)
    # agora, vai finalizar o desenho de toda a tela
    pygame.display.update()


# Criar o jogo em si

# a função recebeu esses dois parâmetros por conta do NEAT
# o genoma e o config estão descritos no arquivo config
def main(genomas, config):
    global geracao
    geracao += 1

    if aiJogando:
        redes = []
        listaGenomas = []
        passaros = []
        # esse _ no for é porque você precisa pegar uma informação, mas você não precisa dela.
        for _, genoma in genomas:
            # esse neat.nn faz parte do documento da NEAT
            rede = neat.nn.FeedForwardNetwork.create(genoma, config)
            redes.append(rede)
            genoma.fitness = 0  # pontuação do pássaro pela distância que ele percorre
            listaGenomas.append(genoma)
            passaros.append(Passaro(230, 350)) # criando um novo pássaro dentro do for
    else:
        passaros = [Passaro(230, 350)]

    chao = Chao(730)  # para o chão, só precisa da posição y
    canos = [Cano(700)]  # só precisa da posição x, pois a posição y será aleatória (já designada lá em cima)
    tela = pygame.display.set_mode((telaLargura, telaAltura))
    pontos = 0
    # criar a animação do tempo (de quanto em quanto tempo)
    relogio = pygame.time.Clock()

    rodando = True
    while rodando:
        relogio.tick(30)  # quantos frames por segundo

        # como interagir com o jogo
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodando = False
                pygame.quit()
                quit()
            if not aiJogando:
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_SPACE:
                        for passaro in passaros:
                            passaro.pular()

        # aqui é para fazer o AI entender que o pássaro precisa passar pelo outro cano
        indiceCano = 0
        if len(passaros) > 0:
            if len(canos) > 1 and passaros[0].x > (canos[0].x + canos[0].canoTopo.get_width()):
                indiceCano = 1
        else:
            rodando = False
            break

        #pega o pássaro (pássaro) e a posição dele (i)
        for i, passaro in enumerate(passaros):
            passaro.mover()
            # aumentar um pouco a fitness do pássaro
            listaGenomas[i].fitness += 0.1 # vai aumentar o fitness através da posição do pássaro
            output = redes[i].activate((passaro.y,
                                       abs(passaro.y - canos[indiceCano].altura),
                                       abs(passaro.y - canos[indiceCano].posBase)))  #ativando a rede neural
            # regra criada pelo NEAT: se output for > 0,5 ele pula
            if output[0] > 0.5:
                passaro.pular()
        chao.mover()

        adicionarCano = False
        removerCanos = []
        for cano in canos:
            for i, passaro in enumerate(passaros):
                if cano.colidir(passaro):
                    passaros.pop(i)
                    if aiJogando:
                        listaGenomas[i].fitness -= 1  # tirando ponto da AI caso ela bata
                        listaGenomas.pop(i)  # retirando o pássaro que bateu
                        redes.pop(i)
                # Nesse laço, digo que, se um pássaro dessa posição colidir, ele está fora.
                # agora, se o pássaro passou do cano, precisa adicionar um novo cano
                # checa se o x do pássaro passou o x do cano, se sim, ele será maior que o x do cano
                # assim, adiciona um novo cano
                if not cano.passou and passaro.x > cano.x:
                    cano.passou = True
                    adicionarCano = True
            # removendo o cano, que já passou, da tela
            # para isso, a largura dele (x + largura) precisa ser > 0
            cano.mover()
            if cano.x + cano.canoTopo.get_width() < 0:
                removerCanos.append(cano)

        if adicionarCano:
            pontos += 1
            canos.append(Cano(600))  # se o pássaro passa do cano, adiciona outro cano (pos 600) e o jogador ganha 1 pt
            # adicionando pontos caso o pássaro da AI passe pelo cano
            for genoma in listaGenomas:
                genoma.fitness += 5

        for cano in removerCanos:
            canos.remove(cano)

        # como o pássaro morre. Se ele passar da altura limite, ele morrerá
        for i, passaro in enumerate(passaros):
            if (passaro.y + passaro.imagem.get_height()) > chao.y or passaro.y < 0:
                passaros.pop(i)
        # se o pássaro estiver acima do limite ou abaixo do limite, ele é retirado naquela posição (pop)
                if aiJogando:
                    listaGenomas.pop(i)
                    redes.pop(i)

        desenhar_tela(tela, passaros, canos, chao, pontos)

def rodar(caminhoConfig):
    # Os parâmetros são os títulos dos comandos no "config.txt" e o caminho do arquivo.
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                caminhoConfig)
    populacao = neat.Population(config)
    # Gerar as estatísticas do jogo e gerar os dados
    populacao.add_reporter(neat.StdOutReporter(True))
    populacao.add_reporter(neat.StatisticsReporter())

    if aiJogando:
        populacao.run(main, 50)  # criei 50 gerações de pássaros (pode ser o quanto quiser)
    else:
        main(None, None)  # Se não for AI, os parâmetros são vazios. Qualquer um pode jogar.


# Para executar o jogo
if __name__ == '__main__':
    caminho = os.path.dirname(__file__)  #  aqui eu garanti o endereço do arquivo NEAT
    caminhoConfig = os.path.join(caminho, 'config.txt')  # coloquei o arquivo NEAT pra garantir o AI
    rodar(caminhoConfig)
