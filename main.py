import pygame
import random
import sys

# Inisialisasi Pygame dan mixer
pygame.init()
pygame.mixer.init()

# Memuat dan memutar musik
pygame.mixer.music.load("assets/music.mp3")  # file music.mp3
pygame.mixer.music.play(-1)  # -1 untuk memutar musik secara berulang-ulang
buah_sound = pygame.mixer.Sound("assets/buah.mp3")  # file buah.mp3
gameover_sound = pygame.mixer.Sound("assets/gameover.mp3")  # file gameover.mp3
bom_sound = pygame.mixer.Sound("assets/bom.mp3")  # file bom.mp3
level_up_sound = pygame.mixer.Sound("assets/level.mp3")  # file level.mp3
select_sound = pygame.mixer.Sound("assets/select.mp3")  # file select.mp3
play_sound = pygame.mixer.Sound("assets/play.mp3")  # file play.mp3
quit_sound = pygame.mixer.Sound("assets/quit.mp3")  # file quit.mp3


# Ukuran layar
SCREEN_WIDTH, SCREEN_HEIGHT = 1280, 720
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tangkap Buah Jatuh")

# Memuat gambar latar belakang
background_image = pygame.image.load("assets/bg.png")  # Pastikan file bg.png ada di folder assets
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Warna
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)

# Clock untuk mengatur FPS
clock = pygame.time.Clock()

# Player
player_width, player_height = 100, 20
player_x = SCREEN_WIDTH // 2 - player_width // 2
player_y = SCREEN_HEIGHT - 50
player_speed = 10
player_boost_speed = 10  # Kecepatan player dengan boost

# Skor dan level
score = 0
level = 1
font = pygame.font.Font(None, 36)
large_font = pygame.font.Font(None, 72)  # Font besar untuk "Game Over"

# Objek jatuh
objects = []  # List untuk menyimpan objek jatuh
num_objects = 1  # Jumlah objek yang jatuh
object_speed = 3  # Kecepatan objek jatuh

# Fungsi untuk menampilkan home screen
def show_home_screen():
    screen.blit(background_image, (0, 0))

    title_text = large_font.render("TANGKAP BUAH JATUH", True, WHITE)
    play_text = font.render("PLAY", True, GREEN)
    quit_text = font.render("QUIT", True, RED)

    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3))
    play_rect = play_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    quit_rect = quit_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50))

    screen.blit(title_text, title_rect)
    screen.blit(play_text, play_rect)
    screen.blit(quit_text, quit_rect)
    pygame.display.flip()

    selected = 0  # 0 untuk Play, 1 untuk Quit

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:  # Tombol panah atas
                    selected = 0  # Pilih Play
                    select_sound.play()  # Mainkan suara select
                elif event.key == pygame.K_DOWN:  # Tombol panah bawah
                    selected = 1  # Pilih Quit
                    select_sound.play()  # Mainkan suara select
                elif event.key == pygame.K_RETURN:  # Tombol Enter
                    if selected == 0:
                        play_sound.play()  # Mainkan suara play
                        return  # Mulai permainan jika Play dipilih
                    elif selected == 1:
                        quit_sound.play()  # Mainkan suara quit
                        pygame.quit()  # Keluar jika Quit dipilih
                        sys.exit()

        # Mengubah warna teks berdasarkan pilihan yang dipilih
        if selected == 0:
            play_text = font.render("PLAY", True, GREEN)
            quit_text = font.render("QUIT", True, RED)
        elif selected == 1:
            play_text = font.render("PLAY", True, RED)
            quit_text = font.render("QUIT", True, GREEN)

        # Menggambar ulang layar dengan pilihan yang diperbarui
        screen.fill(BLACK)
        screen.blit(title_text, title_rect)
        screen.blit(play_text, play_rect)
        screen.blit(quit_text, quit_rect)
        pygame.display.flip()

# Fungsi untuk memuat gambar aset buah secara acak
def load_fruit_images():
    # Memuat gambar buah dari buah1.png hingga buah17.png
    return [pygame.image.load(f"assets/buah{i}.png") for i in range(1, 18)]  # Buah1.png hingga Buah17.png

def load_bomb_image():
    return pygame.image.load("assets/bom.png")  # Pastikan file bom.png ada di folder assets

# Menginisialisasi gambar buah dan bom
fruit_images = load_fruit_images()
bomb_image = load_bomb_image()

# Fungsi untuk menggambar player (keranjang)
def draw_player(x, y):
    keranjang_image = pygame.image.load("assets/keranjang.png")  # Memuat gambar keranjang
    keranjang_width, keranjang_height = keranjang_image.get_size()  # Mendapatkan ukuran gambar
    keranjang_image = pygame.transform.scale(keranjang_image, (player_width, player_height))  # Menyesuaikan ukuran gambar dengan player
    screen.blit(keranjang_image, (x, y))  # Menggambar gambar keranjang di posisi pemain

# Fungsi untuk menggambar objek jatuh dengan gambar
def draw_objects(objects):
    for obj in objects:
        if 'image' in obj:
            # Resize gambar agar sesuai dengan ukuran objek
            image = pygame.transform.scale(obj['image'], (obj['width'], obj['height']))
            screen.blit(image, (obj['x'], obj['y']))

# Fungsi untuk menampilkan skor
def show_score(x, y, score):
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (x, y))

# Fungsi untuk menampilkan level
def show_level(x, y, level):
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(level_text, (x, y))

def show_game_over(score, level):
    while True:
        screen.blit(background_image, (0, 0))
        game_over_text = large_font.render("GAME OVER", True, RED)
        score_text = font.render(f"Final Score: {score}", True, WHITE)
        level_text = font.render(f"Final Level: {level}", True, WHITE)
        retry_text = font.render("Press Space to Retry or Esc to Quit", True, GREEN)

        screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))
        screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, SCREEN_HEIGHT // 2))
        screen.blit(level_text, (SCREEN_WIDTH // 2 - level_text.get_width() // 2, SCREEN_HEIGHT // 2 + 50))
        screen.blit(retry_text, (SCREEN_WIDTH // 2 - retry_text.get_width() // 2, SCREEN_HEIGHT // 2 + 100))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    game_loop()  # Memulai ulang game loop
                    return  # Keluar dari fungsi show_game_over
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

# Fungsi untuk menginisialisasi objek dengan gambar buah secara acak
def init_objects(level):
    # Pilih gambar buah acak untuk setiap objek
    return [{
        'x': random.randint(0, SCREEN_WIDTH - 30),  # Posisi X acak
        'y': -50,  # Posisi Y mulai di atas layar
        'width': 50,  # Ukuran objek
        'height': 50,
        'speed': object_speed,  # Kecepatan objek jatuh
        'image': random.choice(fruit_images)  # Pilih gambar acak dari buah yang tersedia
    } for _ in range(num_objects + level)]  # Jumlah objek bertambah dengan level

# Fungsi untuk membuat kotak hijau (bom) dengan gambar
def create_green_boxes(level):
    green_boxes = []
    for _ in range(level):
        # Membuat posisi X acak dengan memastikan kotak hijau tidak terlalu berdekatan
        while True:
            x_position = random.randint(0, SCREEN_WIDTH - 50)
            y_position = random.randint(-SCREEN_HEIGHT, -50)  # Posisi Y juga acak dari atas

            # Pastikan kotak hijau tidak terlalu dekat dengan kotak lainnya
            too_close = False
            for box in green_boxes:
                if abs(x_position - box['x']) < 50 and abs(y_position - box['y']) < 50:
                    too_close = True
                    break

            # Jika posisi X dan Y cukup jauh dari kotak lainnya, keluar dari while
            if not too_close:
                break

        # Menambahkan kotak hijau (bom) ke dalam list green_boxes
        green_boxes.append({
            'x': x_position,
            'y': y_position,  # Menetapkan posisi Y acak
            'width': 50,
            'height': 50,
            'type': 'bomb',
            'image': bomb_image  # Ganti kotak hijau dengan gambar bom
        })
    return green_boxes

# Game Loop
running = True

# Di dalam game loop, perbarui logika untuk meningkatkan jumlah objek setiap naik level
def game_loop():
    global running
    # Variabel game
    player_width, player_height = 100, 20
    player_x = SCREEN_WIDTH // 2 - player_width // 2
    player_y = SCREEN_HEIGHT - 50
    player_speed = 10

    score = 0
    level = 1

    objects = init_objects(level)  # Menginisialisasi objek dengan jumlah yang sesuai dengan level
    special_boxes = create_green_boxes(level)

    game_over = False
    last_score = 0

    pygame.mixer.music.play(-1)  # Putar musik lagi saat game dimulai

    while running:
        screen.blit(background_image, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if game_over:
            pygame.mixer.music.stop()  # Hentikan musik saat game over
            gameover_sound.play()
            show_game_over(score, level)
            break  # Setelah game over, keluar dari game loop

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player_x > 0:
            player_x -= player_speed
        if keys[pygame.K_RIGHT] and player_x < SCREEN_WIDTH - player_width:
            player_x += player_speed

        for obj in objects:
            obj['y'] += obj['speed']

            # Jika objek jatuh keluar dari layar, atur posisinya ulang dan pilih gambar baru secara acak
            if obj['y'] > SCREEN_HEIGHT:
                obj['y'] = -50
                obj['x'] = random.randint(0, SCREEN_WIDTH - obj['width'])
                obj['image'] = random.choice(fruit_images)  # Pilih gambar baru setiap kali objek muncul ulang

            if (
                    player_x < obj['x'] + obj['width'] and
                    player_x + player_width > obj['x'] and
                    player_y < obj['y'] + obj['height'] and
                    player_y + player_height > obj['y']
            ):
                if obj['image'] in fruit_images:
                    score += 1
                    obj['y'] = -50
                    obj['x'] = random.randint(0, SCREEN_WIDTH - obj['width'])
                    obj['image'] = random.choice(fruit_images)  # Pilih gambar baru setelah menangkap buah
                    buah_sound.play()

        for box in special_boxes:
            box['y'] += object_speed
            if box['y'] > SCREEN_HEIGHT:
                box['y'] = -50
                box['x'] = random.randint(0, SCREEN_WIDTH - box['width'])

            if (
                player_x < box['x'] + box['width'] and
                player_x + player_width > box['x'] and
                player_y < box['y'] + box['height'] and
                player_y + player_height > box['y']
            ):
                game_over = True
                bom_sound.play()

        # Jika skor mencapai kelipatan 10, tingkatkan level
        if score // 10 > last_score // 10:
            last_score = score
            level += 1
            level_up_sound.play()

            # Setelah level naik, tambahkan objek buah lebih banyak
            objects = init_objects(level)
            special_boxes = create_green_boxes(level)

        draw_player(player_x, player_y)
        draw_objects(objects + special_boxes)

        show_score(10, 10, score)
        show_level(10, 40, level)

        pygame.display.flip()
        clock.tick(60)

# Tampilkan home screen
show_home_screen()

# Mulai game loop
if running:
    game_loop()

pygame.quit()
sys.exit()
