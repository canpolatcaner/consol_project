import turtle
import random
import time

# --- TETRİS OYUNU ---
def tetris_oyunu():
    # Temel Ayarlar
    genislik = 10
    yukseklik = 20
    hucre_boyutu = 20

    window = turtle.Screen()
    window.title("Mini Tetris")
    window.bgcolor("black")
    window.setup(width=400, height=600)
    window.tracer(0)

    # Parça Şekilleri (L, S, Z, T, O, I, J)
    sekiller = [
        [[1, 1, 1], [0, 1, 0]], # T
        [[0, 2, 2], [2, 2, 0]], # S
        [[3, 3, 0], [0, 3, 3]], # Z
        [[4, 0, 0], [4, 4, 4]], # J
        [[0, 0, 5], [5, 5, 5]], # L
        [[6, 6, 6, 6]],         # I
        [[7, 7], [7, 7]]        # O
    ]

    renkler = ["black", "purple", "green", "red", "blue", "orange", "cyan", "yellow"]

    # Oyun Alanı (Grid) Oluşturma
    grid = [[0 for _ in range(genislik)] for _ in range(yukseklik)]

    # Çizim kalemi
    pen = turtle.Turtle()
    pen.penup()
    pen.speed(0)
    pen.hideturtle()

    def hucre_ciz(x, y, renk_indeksi):
        x_pos = -100 + (x * hucre_boyutu)
        y_pos = 200 - (y * hucre_boyutu)
        pen.goto(x_pos, y_pos)
        pen.color("white", renkler[renk_indeksi])
        pen.begin_fill()
        for _ in range(4):
            pen.forward(hucre_boyutu - 1)
            pen.right(90)
        pen.end_fill()

    def ekrani_guncelle(grid, parca, px, py):
        pen.clear()
        # Izgarayı ve yerleşmiş parçaları çiz
        for y in range(yukseklik):
            for x in range(genislik):
                hucre_ciz(x, y, grid[y][x])
        
        # Hareket eden parçayı çiz
        if parca:
            for y, satir in enumerate(parca):
                for x, deger in enumerate(satir):
                    if deger:
                        hucre_ciz(px + x, py + y, deger)
        window.update()

    
    # Tetris mantığı (Çarpışma Kontrolü)
    def carpisma_var_mi(grid, parca, px, py):
        for y, satir in enumerate(parca):
            for x, deger in enumerate(satir):
                if deger:
                    if (px + x < 0 or px + x >= genislik or 
                        py + y >= yukseklik or grid[py + y][px + x]):
                        return True
        return False

    # Başlangıç değişkenleri
    gecerli_parca = random.choice(sekiller)
    px, py = 3, 0
    oyun_devam = True

    # Kontroller
    def sola(): nonlocal px; px -= 1 if not carpisma_var_mi(grid, gecerli_parca, px - 1, py) else 0
    def saga(): nonlocal px; px += 1 if not carpisma_var_mi(grid, gecerli_parca, px + 1, py) else 0
    def dondur():
        nonlocal gecerli_parca
        yeni_parca = list(zip(*gecerli_parca[::-1]))
        if not carpisma_var_mi(grid, yeni_parca, px, py): gecerli_parca = yeni_parca
    def hizlandir():
        nonlocal py
        # Aşağıda engel yoksa bir adım aşağı indir
        if not carpisma_var_mi(grid, gecerli_parca, px, py + 1):
            py += 1
    def tam_asagi():
        nonlocal py
        # Çarpışma olana kadar py değerini artır
        while not carpisma_var_mi(grid, gecerli_parca, px, py + 1):
            py += 1
    window.listen()
    window.onkeypress(sola, "Left")
    window.onkeypress(saga, "Right")
    window.onkeypress(dondur, "Up")
    window.onkeypress(hizlandir, "Down") 
    window.onkeypress(tam_asagi, "space")

    # Ana Döngü
    sayac = 0
    while oyun_devam:
        try:
            ekrani_guncelle(grid, gecerli_parca, px, py)
            sayac += 1
            if sayac % 10 == 0: # Düşme hızı
                if not carpisma_var_mi(grid, gecerli_parca, px, py + 1):
                    py += 1
                else:
                    # Parçayı sabitle
                    for y, satir in enumerate(gecerli_parca):
                        for x, deger in enumerate(satir):
                            if deger: grid[py + y][px + x] = deger
                    
                    # Satır temizleme (basit)
                    grid = [s for s in grid if 0 in s]
                    while len(grid) < yukseklik: grid.insert(0, [0]*genislik)
                    
                    # Yeni parça
                    gecerli_parca = random.choice(sekiller)
                    px, py = 3, 0
                    if carpisma_var_mi(grid, gecerli_parca, px, py):
                        oyun_devam = False
            
            time.sleep(0.05)
        except:
            break

    print("Oyun bitti!")
    window.clear()


# --- YILAN OYUNU ---
def yilan_oyunu():
    s_score = 0
    delay = 0.1

    window = turtle.Screen()
    window.title("Yılan Oyunu")
    window.bgcolor("black")
    window.setup(width=600, height=600)
    window.tracer(0)

    # Yılan kafası
    head = turtle.Turtle()
    head.speed(0)
    head.shape("square")
    head.color("white")
    head.penup()
    head.goto(0,0)
    head.direction = "stop"

    # Yiyecek
    food = turtle.Turtle()
    food.speed(0)
    food.shape("circle")
    food.color("red")
    food.penup()
    food.goto(0,100)

    segments = []

    def go_up():
        if head.direction != "down": head.direction = "up"
    def go_down():
        if head.direction != "up": head.direction = "down"
    def go_left():
        if head.direction != "right": head.direction = "left"
    def go_right():
        if head.direction != "left": head.direction = "right"

    def move():
        if head.direction == "up": head.sety(head.ycor() + 20)
        if head.direction == "down": head.sety(head.ycor() - 20)
        if head.direction == "left": head.setx(head.xcor() - 20)
        if head.direction == "right": head.setx(head.xcor() + 20)

    window.listen()
    window.onkeypress(go_up, "w")
    window.onkeypress(go_down, "s")
    window.onkeypress(go_left, "a")
    window.onkeypress(go_right, "d")

    # Oyun Döngüsü
    for _ in range(1000): # Belirli bir süre sonra kapanması için veya while True
        window.update()
        
        # Kenar çarpışması
        if head.xcor()>290 or head.xcor()<-290 or head.ycor()>290 or head.ycor()<-290:
            time.sleep(1)
            break

        # Yiyecek yeme
        if head.distance(food) < 20:
            food.goto(random.randint(-290, 290), random.randint(-290, 290))
            new_segment = turtle.Turtle()
            new_segment.speed(0)
            new_segment.shape("square")
            new_segment.color("grey")
            new_segment.penup()
            segments.append(new_segment)

        for index in range(len(segments)-1, 0, -1):
            segments[index].goto(segments[index-1].xcor(), segments[index-1].ycor())
        if len(segments) > 0:
            segments[0].goto(head.xcor(), head.ycor())

        move()
        time.sleep(delay)
    
    print("Oyun bitti!")
    window.clearscreen()
    window.bye()



# --- UÇAK OYUNU ---
def ucak_oyunu():
    turtle.resetscreen()
    win = turtle.Screen()
    win.title("Klasik Uçak Savaşı")
    win.bgcolor("navy") # Gökyüzü rengi
    win.setup(width=600, height=800)
    win.tracer(0)

    # 1. BİZİM UÇAĞIMIZ
    player = turtle.Turtle()
    player.shape("triangle") # Basit uçak şekli
    player.color("white")
    player.penup()
    player.setheading(90) # Yukarı baksın
    player.goto(0, -350)

    # 2. ATEŞ SİSTEMİ (Mermiler)
    bullets = []
    def ates_et():
        bullet = turtle.Turtle()
        bullet.shape("square")
        bullet.color("yellow")
        bullet.shapesize(0.5, 0.2)
        bullet.penup()
        bullet.speed(0)
        bullet.goto(player.xcor(), player.ycor() + 20)
        bullets.append(bullet)

    # 3. DÜŞMAN UÇAKLARI
    enemies = []
    for _ in range(5): # Ekranda aynı anda 5 düşman olsun
        enemy = turtle.Turtle()
        enemy.shape("triangle")
        enemy.color("red")
        enemy.penup()
        enemy.setheading(270) # Aşağı baksın
        enemy.goto(random.randint(-280, 280), random.randint(200, 400))
        enemies.append(enemy)

    # Hareketler
    def sola(): 
        if player.xcor() > -280: player.setx(player.xcor() - 20)
    def saga(): 
        if player.xcor() < 280: player.setx(player.xcor() + 20)

    win.listen()
    win.onkeypress(sola, "Left")
    win.onkeypress(saga, "Right")
    win.onkeypress(ates_et, "space") # Boşlukla ateş et

    # OYUN DÖNGÜSÜ
    score = 0
    running = True
    while running:
        try:
            win.update()
            time.sleep(0.10)

            # Mermileri hareket ettir
            for bullet in bullets[:]:
                bullet.sety(bullet.ycor() + 15)
                if bullet.ycor() > 400: # Ekrandan çıktıysa sil
                    bullet.hideturtle()
                    bullets.remove(bullet)

            # Düşmanları hareket ettir ve Çarpışma Kontrolü
            for enemy in enemies:
                enemy.sety(enemy.ycor() - 5) # Düşman hızı
                
                # Düşman en alta indiyse başa dönsün
                if enemy.ycor() < -400:
                    enemy.goto(random.randint(-280, 280), random.randint(200, 400))

                # Mermi düşmanı vurdu mu?
                for bullet in bullets[:]:
                    if bullet.distance(enemy) < 25:
                        score += 10
                        enemy.goto(random.randint(-280, 280), random.randint(200, 400))
                        bullet.hideturtle()
                        if bullet in bullets: bullets.remove(bullet)
                        print(f"Puan: {score}")

                # Düşman bize çarptı mı?
                if enemy.distance(player) < 30:
                    print("EYVAH! VURULDUN!")
                    running = False

        except:
            break

    print(f"Oyun Bitti! Toplam Puanın: {score}")
    win.clear()


def calistir():
    while True:
        print("-"*30)
        print("╔═══════════════════════╗")
        print("║    Oyunlar            ║")
        print("║                       ║")
        print("║  1-Tetris             ║")
        print("║  2-Yılan              ║")
        print("║  3-Savaş Uçağı        ║")
        print("║                       ║")
        print("║                       ║")
        print("║  0-Çıkış              ║")
        print("║                       ║")
        print("║    Seçiminiz nedir?   ║")
        print("╚═══════════════════════╝")

        try:
            secim = int(input("Lütfen bir oyun seçiniz:\t"))
            if secim == 1:
                print("Tetris oyununu seçtiniz.\n\n")
                tetris_oyunu()
            elif secim == 2:
                print("Yılan oyununu seçtiniz.\n\n")
                yilan_oyunu()
            elif secim == 3:
                print("Savaş uçağı seçtiniz.\n\n")
                ucak_oyunu()
            elif secim == 0:
                print('Ana menüye dönülüyor...')
                break
            else:
                print("Lütfen oyun menüsünde belirtilen oyunlardan birini seçiniz!")
        except ValueError:
            print("Hata: Lütfen sayı giriniz!")
if __name__ == "__main__":
    calistir()    