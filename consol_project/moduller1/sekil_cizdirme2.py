#design_menu
import turtle
import time

def calistir():
    
    try:
        uzunluk = int(input("Lütfen bir uzunluk giriniz:\t"))
        aci = int(input("Lütfen açı değerini giriniz:\t"))
        
        k1=turtle.Turtle()
        k1.pensize(5)
        k1.pencolor("black")
        k2=turtle.Turtle()
        k2.pensize(7)
        k2.pencolor("blue")
        k1.speed(10)
        k2.speed(10)    
        for i in range(8):
            for a in range (4):
                k2.forward(uzunluk)
                k2.right(aci)
            k2.right(45)  
        
        for j in range (11):
            for b in range (4):
                k1.forward (50)
                k1.right (90)
            k1.right (30)     
        print("Şekil çizildi, işlemler menüsüne geri dönülüyor...")
        time.sleep(6)  
        turtle.clearscreen()   
    except ValueError:
        print("Hata: Lütfen sayı giriniz!")
  