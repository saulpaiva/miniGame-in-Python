import pgzrun
import random
import math

# Configuração da tela
WIDTH = 800
HEIGHT = 600

# Variáveis de controle
game_started = False
music_on = True
sounds_on = True

# Carregar o background
background = "background_image"  # Nome do arquivo da imagem de fundo

# Classes para o herói e os inimigos
class Character:
    def __init__(self, image_prefix, pos, speed):
        self.image_prefix = image_prefix
        self.actor = Actor(f"{image_prefix}_idle_0", pos)
        self.speed = speed
        self.frame = 0
        self.moving = False
        self.animation_timer = 0  # Controla a velocidade da animação

    def move(self, direction):
        if direction == "left":
            self.actor.x -= self.speed
        elif direction == "right":
            self.actor.x += self.speed
        elif direction == "up":
            self.actor.y -= self.speed
        elif direction == "down":
            self.actor.y += self.speed
        self.moving = True

    def update_animation(self):
        # Atualiza o frame de animação a cada 0.1 segundo
        self.animation_timer += 1
        if self.animation_timer >= 10:  # Controla a velocidade da animação
            if self.moving:
                self.frame = (self.frame + 1) % 4  # Assumindo 4 frames de animação
                self.actor.image = f"{self.image_prefix}_walk_{self.frame}"
            else:
                self.frame = (self.frame + 1) % 4
                self.actor.image = f"{self.image_prefix}_idle_{self.frame}"
            self.animation_timer = 0

    def update(self):
        # Atualiza a animação, independentemente de estar se movendo
        self.update_animation()
        self.moving = False  # Reseta para não mover se nenhuma tecla for pressionada

    def draw(self):
        self.actor.draw()


class Enemy(Character):
    def patrol(self):
        # Lógica simples de patrulha aleatória
        self.move(random.choice(["left", "right", "up", "down"]))
        self.update_animation()


# Inicialização do herói e inimigos
hero = Character("hero", (WIDTH // 2, HEIGHT // 2), speed=3)
enemies = [Enemy("enemy", (random.randint(50, WIDTH-50), random.randint(50, HEIGHT-50)), speed=2) for _ in range(3)]

# Função para desenhar a tela do menu
def draw_menu():
    screen.clear()
    screen.draw.text("My Game", center=(WIDTH // 2, HEIGHT // 3), fontsize=60, color="white")
    screen.draw.text("Start Game", center=(WIDTH // 2, HEIGHT // 2), fontsize=40, color="green")
    screen.draw.text("Music: On" if music_on else "Music: Off", center=(WIDTH // 2, HEIGHT // 2 + 60), fontsize=40, color="yellow")
    screen.draw.text("Exit", center=(WIDTH // 2, HEIGHT // 2 + 120), fontsize=40, color="red")

# Função para desenhar o jogo
def draw():
    if not game_started:
        draw_menu()
    else:
        screen.clear()
        screen.blit(background, (0, 0))  # Desenha o background
        hero.draw()
        for enemy in enemies:
            enemy.draw()

# Função para verificar as teclas de controle
def update():
    global game_started
    if game_started:
        if keyboard.left:
            hero.move("left")
        elif keyboard.right:
            hero.move("right")
        elif keyboard.up:
            hero.move("up")
        elif keyboard.down:
            hero.move("down")
        else:
            hero.moving = False  # Garante que a animação de idle seja usada quando parar de se mover

        # Atualiza a animação e posição do herói
        hero.update()

        # Movimento dos inimigos
        for enemy in enemies:
            enemy.patrol()

# Controle de música
def toggle_music():
    if music_on:
        music.play("background_music")
    else:
        music.stop()

# Função para controle de clique no menu
def on_mouse_down(pos):
    global game_started, music_on, sounds_on
    if not game_started:
        # Detecta cliques nos botões do menu
        if WIDTH // 2 - 100 < pos[0] < WIDTH // 2 + 100 and HEIGHT // 2 - 20 < pos[1] < HEIGHT // 2 + 20:
            game_started = True
        elif WIDTH // 2 - 100 < pos[0] < WIDTH // 2 + 100 and HEIGHT // 2 + 40 < pos[1] < HEIGHT // 2 + 80:
            music_on = not music_on
            toggle_music()
        elif WIDTH // 2 - 100 < pos[0] < WIDTH // 2 + 100 and HEIGHT // 2 + 100 < pos[1] < HEIGHT // 2 + 140:
            exit()

# Inicializa o jogo
pgzrun.go()
