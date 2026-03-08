import sqlite3

def db_hazirla():
    baglanti = sqlite3.connect("rehber_tel_pk.db")
    kursor = baglanti.cursor()
    # tel1 ana anahtar (PRIMARY KEY), isim ise UNIQUE (aynı isimden iki tane olamaz)
    kursor.execute("""
        CREATE TABLE IF NOT EXISTS rehber (
            tel1 TEXT PRIMARY KEY,
            isim TEXT NOT NULL UNIQUE,
            soyisim TEXT NOT NULL,
            tel2 TEXT,
            eposta TEXT,
            is_adresi TEXT,
            ev_adresi TEXT
        )
    """)
    baglanti.commit()
    baglanti.close()

def kayit_getir(arama_metni):
    """Kullanıcının girdiği HERHANGİ bir veriyle (isim, tel, adres vb.) arama yapar."""
    baglanti = sqlite3.connect("rehber_tel_pk.db")
    baglanti.row_factory = sqlite3.Row 
    kursor = baglanti.cursor()
    
    # Tüm sütunlarda 'OR' (VEYA) mantığıyla arama
    sorgu = """
        SELECT * FROM rehber 
        WHERE tel1 = ? OR isim = ? OR soyisim = ? OR 
              tel2 = ? OR eposta = ? OR is_adresi = ? OR ev_adresi = ?
    """
    # Parametreyi 7 sütun için de uyguluyoruz
    kursor.execute(sorgu, (arama_metni,) * 7)
    row = kursor.fetchone()
    baglanti.close()
    
    return dict(row) if row else None

def kisi_ekle():
    print("\n--- 🆕 YENİ KAYIT EKLE ---")
    isim = input("İsim*: ")
    soyisim = input("Soyisim*: ")
    tel1 = input("Telefon 1 (Anahtar)*: ")
    
    tel2 = input("Telefon 2 (İsteğe bağlı): ") or None
    eposta = input("E-posta (İsteğe bağlı): ") or None
    is_adres = input("İş Adresi (İsteğe bağlı): ") or None
    ev_adres = input("Ev Adresi (İsteğe bağlı): ") or None

    if not isim or not tel1:
        print("❌ Hata: İsim ve Telefon 1 alanları zorunludur!")
        return

    try:
        baglanti = sqlite3.connect("rehber_tel_pk.db")
        kursor = baglanti.cursor()
        kursor.execute("INSERT INTO rehber VALUES (?,?,?,?,?,?,?)", 
                       (tel1, isim, soyisim, tel2, eposta, is_adres, ev_adres))
        baglanti.commit()
        baglanti.close()
        print(f"✅ {isim} {soyisim} başarıyla rehbere kaydedildi.")
    except sqlite3.IntegrityError:
        print("❌ Hata: Bu telefon numarası veya isim rehberde zaten var!")

def duzenleme_modu():
    print("\n" + "═"*50)
    print(f"{'🔍 KAYIT BUL VE DÜZENLE (ESNEK ARAMA)':^50}")
    print("═"*50)
    
    hedef = input("Kişiyi bulmak için HERHANGİ bir bilgisini girin (İsim, Tel, E-posta vb.): ")
    kayit = kayit_getir(hedef)

    if not kayit:
        print(f"❌ Hata: '{hedef}' ile eşleşen bir kayıt bulunamadı!")
        return

    # Orijinal benzersiz alanı (tel1) hafızada tutuyoruz (UPDATE işlemi için)
    eski_tel1 = kayit['tel1']
    taslak = kayit.copy()
    
    while True:
        print("\n" + "─"*30)
        print("TASLAK ÜZERİNDEKİ GÜNCEL BİLGİLER:")
        for anahtar, deger in taslak.items():
            etiket = " [ANAHTAR]" if anahtar == "tel1" else ""
            print(f"👉 {anahtar.upper()}{etiket}: {deger if deger else '(Boş)'}")
        print("─"*30)
        
        print("\nKomutlar: [isim, soyisim, tel1, tel2, eposta, is_adresi, ev_adresi]")
        print("Kaydetmek için: 'S' | İptal edip çıkmak için: 'Q'")
        
        secim = input("\nDeğiştirmek istediğiniz alan adını yazın: ").lower()

        if secim == 's':
            onay = input("⚠️ Değişiklikler kaydedilsin mi? (E/H): ").lower()
            if onay == 'e':
                try:
                    baglanti = sqlite3.connect("rehber_tel_pk.db")
                    kursor = baglanti.cursor()
                    sorgu = """
                        UPDATE rehber SET 
                        tel1 = ?, isim = ?, soyisim = ?, tel2 = ?, 
                        eposta = ?, is_adresi = ?, ev_adresi = ?
                        WHERE tel1 = ?
                    """
                    kursor.execute(sorgu, (
                        taslak['tel1'], taslak['isim'], taslak['soyisim'],
                        taslak['tel2'], taslak['eposta'], taslak['is_adresi'],
                        taslak['ev_adresi'], eski_tel1
                    ))
                    baglanti.commit()
                    baglanti.close()
                    print("✅ BAŞARILI: Veritabanı güncellendi.")
                    break
                except sqlite3.IntegrityError:
                    print("❌ HATA: Yeni telefon veya isim başka bir kayıtta zaten var!")
            else:
                print("İşlem tamamlanmadı, taslak hala aktif.")

        elif secim == 'q':
            print("❌ İşlem iptal edildi.")
            break
        
        elif secim in taslak:
            yeni_deger = input(f"Yeni {secim} değerini girin: ")
            taslak[secim] = yeni_deger if yeni_deger else None
        else:
            print("⚠️ Geçersiz alan adı! Lütfen listedeki isimlerden birini yazın.")

def listele():
    baglanti = sqlite3.connect("rehber_tel_pk.db")
    kursor = baglanti.cursor()
    kursor.execute("SELECT * FROM rehber")
    veriler = kursor.fetchall()
    baglanti.close()
    
    print("\n" + "═"*50)
    print(f"{'📋 TÜM REHBER':^50}")
    print("═"*50)

    if not veriler:
        print("Rehber şu an boş.")
    else:
        for v in veriler:
            print(f"👤 AD SOYAD     : {v[1]} {v[2]}")
            print(f"📞 ANA TELEFON  : {v[0]}")
            print(f"📱 YEDEK TELEFON: {v[3] if v[3] else '---'}")
            print(f"📧 E-POSTA      : {v[4] if v[4] else '---'}")
            print(f"🏢 İŞ ADRESİ    : {v[5] if v[5] else '---'}")
            print(f"🏠 EV ADRESİ    : {v[6] if v[6] else '---'}")
            print("─"*60) # Her kişi arasına ince ayraç
        
        print(f"📊 Toplam Kayıt Sayısı: {len(veriler)}")
        print("─"*50)

    
def calistir():
    db_hazirla()
    while True:
        print("-"*30)
        print("╔═══════════════════════╗")
        print("║  TELEFON REHBERİ      ║")
        print("║                       ║")
        print("║  1-Kişi Ekle          ║")
        print("║  2-Listele            ║")
        print("║  3-Düzenle            ║")
        print("║                       ║")
        print("║                       ║")
        print("║  0-Çıkış              ║")
        print("║                       ║")
        print("║    Seçiminiz nedir?   ║")
        print("╚═══════════════════════╝")

        try:
            secim = int(input("Lütfen ne yapmak istediğinizi seçiniz:\t"))
            if secim == 1:
                print("Kişi eklemeyi seçtiniz.\n\n")
                kisi_ekle()
            elif secim == 2:
                print("Rehberi listelemeyi seçtiniz.\n\n")
                listele()
            elif secim == 3:
                print("Kişileri düzenlemeyi seçtiniz.\n\n")
                duzenleme_modu()
            elif secim == 0:
                print('Ana menüye dönülüyor...')
                break
            else:
                print("Lütfen telefon rehberi menüsünde belirtilen seçeneklerden birini seçiniz!")
        except ValueError:
            print("Hata: Lütfen sayı giriniz!")
if __name__ == "__main__":
    calistir()    
