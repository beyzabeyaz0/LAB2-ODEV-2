# AYBÜKE TÜRİDİ 220502005 ELİF BEYZA BEYAZ 220502033
# -*- coding: utf-8 -*-
import sqlite3
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

# Aşama 1: Sql server üzerinden gemi,sefer,personel ve liman için table oluşturma

def veritabani_olustur():
    baglanti_gemiler = sqlite3.connect('GEMILER.db')
    imlec_gemiler = baglanti_gemiler.cursor()
    baglanti_seferler = sqlite3.connect('SEFERLER.db')
    cursor_seferler = baglanti_seferler.cursor()
    baglanti_personel = sqlite3.connect('PERSONEL.db')
    imlec_personel = baglanti_personel.cursor()
    baglanti_liman = sqlite3.connect('LIMAN.db')
    imlec_liman = baglanti_liman.cursor()

    # GEMILER tablosu
    imlec_gemiler.execute('''
        CREATE TABLE IF NOT EXISTS GEMILER (
            SERI_NO INTEGER PRIMARY KEY,
            GEMI_ADI TEXT,
            AGIRLIK REAL,
            YAPIM_YILI INTEGER,
            TUR TEXT
        )
    ''')

    # Yolcu gemileri için
    imlec_gemiler.execute('''
        CREATE TABLE IF NOT EXISTS YOLCU_GEMILERI (
            SERI_NO INTEGER,
            YOLCU_KAPASITESI INTEGER,
            FOREIGN KEY(SERI_NO) REFERENCES GEMILER(SERI_NO)
        )
    ''')

    # Petrol gemileri için
    imlec_gemiler.execute('''
        CREATE TABLE IF NOT EXISTS PETROL_TANKERLERI (
            SERI_NO INTEGER,
            PETROL_KAPASITESI REAL,
            FOREIGN KEY(SERI_NO) REFERENCES GEMILER(SERI_NO)
        )
    ''')

    # Konteyner gemileri için
    imlec_gemiler.execute('''
        CREATE TABLE IF NOT EXISTS KONTEYNER_GEMILERI (
            SERI_NO INTEGER,
            KONTEYNER_SAYISI INTEGER,
            MAKS_AGIRLIK REAL,
            FOREIGN KEY(SERI_NO) REFERENCES GEMILER(SERI_NO)
        )
    ''')

    # SEFERLER tablosu
    cursor_seferler.execute('''
            CREATE TABLE IF NOT EXISTS SEFERLER (
                S_ID INTEGER PRIMARY KEY,
                S_CIKIS TEXT,
                S_DONUS TEXT,
                S_LİMAN TEXT,
                SERI_NO INTEGER,
                FOREIGN KEY(SERI_NO) REFERENCES GEMILER(SERI_NO)
            )
        ''')

    # PERSONEL tablosu
    imlec_personel.execute('''
            CREATE TABLE IF NOT EXISTS PERSONEL (
                PERSONEL_ID INTEGER PRIMARY KEY,
                PERSONEL_AD TEXT,
                PERSONEL_SOYAD TEXT,
                PERSONEL_VATANDASLIK TEXT,
                PERSONEL_DOGUM_TARIHI TEXT,
                PERSONEL_MESLEGI, PERSONEL_ISE_GIRIS TEXT,
                PERSONEL_ADRESI TEXT,
                PERSONEL_DURUM TEXT
            )
        ''')

    # LİMAN tablosu
    imlec_liman.execute('''
            CREATE TABLE IF NOT EXISTS LIMAN (
            LIMAN_ADI TEXT,
            ULKE TEXT,
            PASAPORT_ISTEGI TEXT CHECK(PASAPORT_ISTEGI IN ('E', 'H')), -- E: Evet, H: Hayır,
            DEMIRLEME_UCRETI REAL,
            PRIMARY KEY (LIMAN_ADI, ULKE) 
            )
        ''')
    baglanti_gemiler.commit()
    baglanti_seferler.commit()
    baglanti_personel.commit()
    baglanti_liman.commit()

# Aşama 2: Oluşturulan tablolar için metotlar(ekleme,çıkarma vs.)

# GEMİ İÇİN

# 3 gemi türü için de aynı gemi ekleme metodu kullanırız. Duruma göre sütunlar None olur ya da değer alır.
def gemi_ekle(seri_no, gemi_adi, agirlik, yapim_yili, tur, yolcu_kapasitesi=None, petrol_kapasitesi=None,
              konteyner_sayisi=None, maks_agirlik=None):
    baglanti_gemi2 = sqlite3.connect('GEMILER.db')
    imlec_gemi2 = baglanti_gemi2.cursor()
    imlec_gemi2.execute('''
        INSERT INTO GEMILER (SERI_NO, GEMI_ADI, AGIRLIK, YAPIM_YILI, TUR)
        VALUES (?, ?, ?, ?, ?)
    ''', (seri_no, gemi_adi, agirlik, yapim_yili, tur))

    if tur == "YOLCU" and yolcu_kapasitesi is not None:
        imlec_gemi2.execute('''
            INSERT INTO YOLCU_GEMILERI (SERI_NO, YOLCU_KAPASITESI)
            VALUES (?, ?)
        ''', (seri_no, yolcu_kapasitesi))
    elif tur == "PETROL_TANKERI" and petrol_kapasitesi is not None:
        imlec_gemi2.execute('''
            INSERT INTO PETROL_TANKERLERI (SERI_NO, PETROL_KAPASITESI)
            VALUES (?, ?)
        ''', (seri_no, petrol_kapasitesi))
    elif tur == "KONTEYNER" and konteyner_sayisi is not None and maks_agirlik is not None:
        imlec_gemi2.execute('''
            INSERT INTO KONTEYNER_GEMILERI (SERI_NO, KONTEYNER_SAYISI, MAKS_AGIRLIK)
            VALUES (?, ?, ?)
        ''', (seri_no, konteyner_sayisi, maks_agirlik))

    baglanti_gemi2.commit()
    baglanti_gemi2.close()

def gemi_sil(seri_no):
    baglanti_gemi3 = sqlite3.connect('GEMILER.db')
    imlec_gemi3 = baglanti_gemi3.cursor()
    imlec_gemi3.execute('''
        DELETE FROM GEMILER WHERE SERI_NO=?
    ''', (seri_no,))
    baglanti_gemi3.commit()
    baglanti_gemi3.close()

def gemileri_al():
    baglanti_gemi4 = sqlite3.connect('GEMILER.db')
    imlec_gemi4 = baglanti_gemi4.cursor()
    imlec_gemi4.execute('SELECT * FROM GEMILER')
    gemiler = imlec_gemi4.fetchall()
    baglanti_gemi4.close()
    return gemiler

def gemi_turu_bilgilerini_al(seri_no, tur):
    baglanti_gemi5 = sqlite3.connect('GEMILER.db')
    imlec_gemi5 = baglanti_gemi5.cursor()
    if tur == "YOLCU":
        imlec_gemi5.execute('SELECT YOLCU_KAPASITESI FROM YOLCU_GEMILERI WHERE SERI_NO = ?', (seri_no,))
    elif tur == "PETROL_TANKERI":
        imlec_gemi5.execute('SELECT PETROL_KAPASITESI FROM PETROL_TANKERLERI WHERE SERI_NO = ?', (seri_no,))
    elif tur == "KONTEYNER":
        imlec_gemi5.execute('SELECT KONTEYNER_SAYISI, MAKS_AGIRLIK FROM KONTEYNER_GEMILERI WHERE SERI_NO = ?', (seri_no,))

    bilgi = imlec_gemi5.fetchone()
    baglanti_gemi5.close()
    return bilgi

# SEFER İÇİN

def sefer_ekle(s_ID, s_CIKIS, s_DONUS, s_LIMAN, seri_no):
    baglanti_sefer2 = sqlite3.connect('SEFERLER.db')
    imlec_sefer2 = baglanti_sefer2.cursor()
    imlec_sefer2.execute('''
            INSERT INTO SEFERLER (S_ID,S_CIKIS,S_DONUS,S_LİMAN,SERI_NO)
            VALUES (?, ?, ?, ?, ?)
        ''', (s_ID, s_CIKIS, s_DONUS, s_LIMAN, seri_no))
    baglanti_sefer2.commit()
    baglanti_sefer2.close()

def sefer_sil(s_ID):
    baglanti = sqlite3.connect('SEFERLER.db')
    imlec = baglanti.cursor()
    imlec.execute('SELECT * FROM SEFERLER WHERE S_ID = ?', (s_ID,))
    sefer = imlec.fetchone()  # Girilen s_ID'de sefer olup olmadığını kontrol edip buna göre if-else yapısı ile silme işlemi gerçekleşir
    if sefer:
        imlec.execute('DELETE FROM SEFERLER WHERE S_ID = ?', (s_ID,))
        baglanti.commit()
        silindi = True
    else:
        silindi = False
    baglanti.close()
    return silindi

def sefer_belirle():
    baglanti_sefer4 = sqlite3.connect('SEFERLER.db')
    imlec_sefer4 = baglanti_sefer4.cursor()
    imlec_sefer4.execute('SELECT * FROM SEFERLER')
    seferler = imlec_sefer4.fetchall()
    baglanti_sefer4.close()
    return seferler

# PERSONEL için

def personel_ekle(personel_id, ad, soyad, vatandaslik, dogum_tarihi, meslek, ise_giris, adres,durum):
    baglanti = sqlite3.connect('PERSONEL.db')
    imlec = baglanti.cursor()
    imlec.execute('''
        INSERT INTO PERSONEL (PERSONEL_ID, PERSONEL_AD, PERSONEL_SOYAD, PERSONEL_VATANDASLIK,
                             PERSONEL_DOGUM_TARIHI, PERSONEL_MESLEGI, PERSONEL_ISE_GIRIS, PERSONEL_ADRESI,PERSONEL_DURUM)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?,?)
    ''', (personel_id, ad, soyad, vatandaslik, dogum_tarihi, meslek, ise_giris, adres,durum))
    baglanti.commit()
    baglanti.close()

def personel_sil(personel_id):
    baglanti = sqlite3.connect('PERSONEL.db')
    imlec = baglanti.cursor()
    imlec.execute('''
        DELETE FROM PERSONEL WHERE PERSONEL_ID=?
    ''', (personel_id,))
    baglanti.commit()
    baglanti.close()

def personelleri_al():
    baglanti = sqlite3.connect('PERSONEL.db')
    imlec = baglanti.cursor()
    imlec.execute('SELECT * FROM PERSONEL')
    personeller = imlec.fetchall()
    baglanti.close()
    return personeller

# LİMAN için

def liman_ekle(liman_adi, ulke, pasaport_istegi, demirleme_ucreti):
    baglanti_liman = sqlite3.connect('LIMAN.db')
    imlec_liman = baglanti_liman.cursor()
    try:
        imlec_liman.execute('''
            INSERT INTO LIMAN (LIMAN_ADI, ULKE, PASAPORT_ISTEGI, DEMIRLEME_UCRETI)
            VALUES (?, ?, ?, ?)
        ''', (liman_adi, ulke, pasaport_istegi, demirleme_ucreti))
        baglanti_liman.commit()
    except sqlite3.IntegrityError:
        messagebox.showerror("Hata", "Bu liman adı ve ülke kombinasyonu zaten mevcut.")
    finally:
        baglanti_liman.close()

def liman_sil(liman_adi, ulke):
    baglanti_liman = sqlite3.connect('LIMAN.db')
    imlec_liman = baglanti_liman.cursor()
    imlec_liman.execute('''
        DELETE FROM LIMAN WHERE LIMAN_ADI = ? AND ULKE = ?
    ''', (liman_adi, ulke))
    baglanti_liman.commit()
    silinen_sayisi = imlec_liman.rowcount
    baglanti_liman.close()
    return silinen_sayisi > 0

def limanlari_al():
    baglanti_liman = sqlite3.connect('LIMAN.db')
    imlec_liman = baglanti_liman.cursor()
    imlec_liman.execute('SELECT * FROM LIMAN')
    limanlar = imlec_liman.fetchall()
    baglanti_liman.close()
    return limanlar


# Aşama 3: Veritabanındaki değerleri kullanıcıdan form üzerinden almak için tkinter kütüphanesiyle yapılmış form ekranı

# Her bir sınıfın kendine uygun ekleme,silme,listeleme metotu bulunmaktadır. Bunu ekrana girilen değerler aracılığıyla yapar.

# GEMİ için

class GemiTablosu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Gemi Yönetim Sistemi")

        self.label_seri_no = tk.Label(self, text="Seri No:")
        self.entry_seri_no = tk.Entry(self)

        self.label_gemi_adi = tk.Label(self, text="Gemi Adı:")
        self.entry_gemi_adi = tk.Entry(self)

        self.label_agirlik = tk.Label(self, text="Ağırlık:")
        self.entry_agirlik = tk.Entry(self)

        self.label_yapim_yili = tk.Label(self, text="Yapım Yılı:")
        self.entry_yapim_yili = tk.Entry(self)

        self.label_tur = tk.Label(self, text="Gemi Türü:")

        self.label_silinecek_seri_no = tk.Label(self, text="Silinecek Seri No:")
        self.label_silinecek_seri_no.grid(row=6, column=0)

        self.entry_silinecek_seri_no = tk.Entry(self)
        self.entry_silinecek_seri_no.grid(row=6, column=1)

        self.sil_button = tk.Button(self, text="Gemi Sil", command=self.gemi_sil_tk)
        self.sil_button.grid(row=7, column=0, columnspan=2)

        self.liste_button = tk.Button(self, text="Gemi Listesi", command=self.gemileri_goster)
        self.liste_button.grid(row=8, column=0, columnspan=2)

        self.gemi_turu_var = tk.StringVar(value="YOLCU")  # varsayılan tür
        self.radio_yolcu = tk.Radiobutton(self, text="Yolcu Gemisi", variable=self.gemi_turu_var, value="YOLCU",
                                          command=self.gemi_turu_secildi)
        self.radio_petrol = tk.Radiobutton(self, text="Petrol Tankeri", variable=self.gemi_turu_var,
                                           value="PETROL_TANKERI", command=self.gemi_turu_secildi)
        self.radio_konteyner = tk.Radiobutton(self, text="Konteyner Gemisi", variable=self.gemi_turu_var,
                                              value="KONTEYNER", command=self.gemi_turu_secildi)

        self.label_yolcu_kapasitesi = tk.Label(self, text="Yolcu Kapasitesi:")
        self.entry_yolcu_kapasitesi = tk.Entry(self)

        self.label_petrol_kapasitesi = tk.Label(self, text="Petrol Kapasitesi (litre):")
        self.entry_petrol_kapasitesi = tk.Entry(self)

        self.label_konteyner_sayisi = tk.Label(self, text="Konteyner Sayısı:")
        self.entry_konteyner_sayisi = tk.Entry(self)

        self.label_maks_agirlik = tk.Label(self, text="Maksimum Ağırlık:")
        self.entry_maks_agirlik = tk.Entry(self)

        self.ekle_button = tk.Button(self, text="Gemi Ekle", command=self.gemi_ekle_tk)

        self.label_seri_no.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.entry_seri_no.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        self.label_gemi_adi.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.entry_gemi_adi.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        self.label_agirlik.grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.entry_agirlik.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        self.label_yapim_yili.grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.entry_yapim_yili.grid(row=3, column=1, padx=5, pady=5, sticky='w')

        self.label_tur.grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.radio_yolcu.grid(row=4, column=1, padx=5, pady=5, sticky='w')
        self.radio_petrol.grid(row=4, column=2, padx=5, pady=5, sticky='w')
        self.radio_konteyner.grid(row=4, column=3, padx=5, pady=5, sticky='w')

        self.label_yolcu_kapasitesi.grid(row=5, column=0, padx=5, pady=5, sticky='w')
        self.entry_yolcu_kapasitesi.grid(row=5, column=1, padx=5, pady=5, sticky='w')

        self.label_petrol_kapasitesi.grid(row=6, column=0, padx=5, pady=5, sticky='w')
        self.entry_petrol_kapasitesi.grid(row=6, column=1, padx=5, pady=5, sticky='w')

        self.label_konteyner_sayisi.grid(row=7, column=0, padx=5, pady=5, sticky='w')
        self.entry_konteyner_sayisi.grid(row=7, column=1, padx=5, pady=5, sticky='w')

        self.label_maks_agirlik.grid(row=8, column=0, padx=5, pady=5, sticky='w')
        self.entry_maks_agirlik.grid(row=8, column=1, padx=5, pady=5, sticky='w')

        self.ekle_button.grid(row=9, column=0, columnspan=2, padx=5, pady=10, sticky='we')
        self.label_silinecek_seri_no.grid(row=10, column=0, padx=5, pady=5, sticky='w')
        self.entry_silinecek_seri_no.grid(row=10, column=1, padx=5, pady=5, sticky='w')

        self.sil_button.grid(row=11, column=0, columnspan=2, padx=5, pady=10, sticky='we')
        self.liste_button.grid(row=12, column=0, columnspan=2, padx=5, pady=10, sticky='we')

        self.gemi_turu_secildi()

        self.ekle_button.grid(row=9, column=0, columnspan=2)

    def gemi_turu_secildi(self):
        gemi_turu = self.gemi_turu_var.get()

        if gemi_turu == "YOLCU":
            self.label_yolcu_kapasitesi.grid(row=5, column=0)
            self.entry_yolcu_kapasitesi.grid(row=5, column=1)
        # Gemi türleri için seçilen türe göre girilecek değerler farklılık gösterir.
            self.label_petrol_kapasitesi.grid_forget()
            self.entry_petrol_kapasitesi.grid_forget()
            self.label_konteyner_sayisi.grid_forget()
            self.entry_konteyner_sayisi.grid_forget()
            self.label_maks_agirlik.grid_forget()
            self.entry_maks_agirlik.grid_forget()

        elif gemi_turu == "PETROL_TANKERI":
            self.label_petrol_kapasitesi.grid(row=5, column=0)
            self.entry_petrol_kapasitesi.grid(row=5, column=1)

            self.label_yolcu_kapasitesi.grid_forget()
            self.entry_yolcu_kapasitesi.grid_forget()
            self.label_konteyner_sayisi.grid_forget()
            self.entry_konteyner_sayisi.grid_forget()
            self.label_maks_agirlik.grid_forget()
            self.entry_maks_agirlik.grid_forget()

        elif gemi_turu == "KONTEYNER":
            self.label_konteyner_sayisi.grid(row=5, column=0)
            self.entry_konteyner_sayisi.grid(row=5, column=1)

            self.label_maks_agirlik.grid(row=6, column=0)
            self.entry_maks_agirlik.grid(row=6, column=1)

            self.label_yolcu_kapasitesi.grid_forget()
            self.entry_yolcu_kapasitesi.grid_forget()
            self.label_petrol_kapasitesi.grid_forget()
            self.entry_petrol_kapasitesi.grid_forget()

    def gemi_ekle_tk(self):
        try:
            seri_no = int(self.entry_seri_no.get())
            gemi_adi = self.entry_gemi_adi.get()
            agirlik = float(self.entry_agirlik.get())
            yapim_yili = int(self.entry_yapim_yili.get())
            tur = self.gemi_turu_var.get()

            # Gemi türüne göre ek bilgileri alın
            if tur == "YOLCU":
                yolcu_kapasitesi = int(self.entry_yolcu_kapasitesi.get())
                gemi_ekle(seri_no, gemi_adi, agirlik, yapim_yili, tur, yolcu_kapasitesi=yolcu_kapasitesi)
            elif tur == "PETROL_TANKERI":
                petrol_kapasitesi = float(self.entry_petrol_kapasitesi.get())
                gemi_ekle(seri_no, gemi_adi, agirlik, yapim_yili, tur, petrol_kapasitesi=petrol_kapasitesi)
            elif tur == "KONTEYNER":
                konteyner_sayisi = int(self.entry_konteyner_sayisi.get())
                maks_agirlik = float(self.entry_maks_agirlik.get())
                gemi_ekle(seri_no, gemi_adi, agirlik, yapim_yili, tur, konteyner_sayisi=konteyner_sayisi,
                          maks_agirlik=maks_agirlik)

            messagebox.showinfo("Başarılı", "Gemi başarıyla eklendi.")

            self.entry_seri_no.delete(0, tk.END)
            self.entry_gemi_adi.delete(0, tk.END)
            self.entry_agirlik.delete(0, tk.END)
            self.entry_yapim_yili.delete(0, tk.END)
            self.gemi_turu_secildi()  # Güncelleme

        except ValueError:
            messagebox.showerror("Hata", "Geçerli değerler giriniz.")

    def gemi_sil_tk(self):
        silinecek_seri_no = self.entry_silinecek_seri_no.get()

        if silinecek_seri_no:
            try:
                silinecek_seri_no = int(silinecek_seri_no)
                gemi_sil(silinecek_seri_no)
                messagebox.showinfo("Başarılı", "Gemi başarıyla silindi.")
                self.entry_silinecek_seri_no.delete(0, tk.END)
            except ValueError:
                messagebox.showerror("Hata", "Geçerli bir seri no giriniz.")
        else:
            messagebox.showerror("Hata", "Lütfen silinecek seri no'yu giriniz.")

    def gemileri_goster(self):
        yeni_pencere = tk.Toplevel(self)
        yeni_pencere.title("Gemi Listesi")
        yeni_pencere.geometry("600x400")  # Pencere boyutunu

        gemi_treeview = ttk.Treeview(
            yeni_pencere,
            columns=("serino", "gemiadi", "agirlik", "yapimyili", "tur", "ozel_bilgi"),
            show='headings'
        )

        gemi_treeview.heading("serino", text="Seri No")
        gemi_treeview.heading("gemiadi", text="Gemi Adı")
        gemi_treeview.heading("agirlik", text="Ağırlık")
        gemi_treeview.heading("yapimyili", text="Yapım Yılı")
        gemi_treeview.heading("tur", text="Tür")
        gemi_treeview.heading("ozel_bilgi", text="Özel Bilgi")

        # Treeview sütun genişliklerini ayarla
        gemi_treeview.column("serino", width=50)
        gemi_treeview.column("gemiadi", width=50)
        gemi_treeview.column("agirlik", width=50)
        gemi_treeview.column("yapimyili", width=50)
        gemi_treeview.column("tur", width=50)
        gemi_treeview.column("ozel_bilgi", width=150)

        gemi_treeview.pack(fill='both', expand=True)

        gemiler = gemileri_al()

        if gemiler:
            for gemi in gemiler:
                seri_no = gemi[0]
                tur = gemi[4]
                ozel_bilgi = ""

                # Gemi türüne göre özel bilgiyi alın
                bilgi = gemi_turu_bilgilerini_al(seri_no, tur)

                if tur == "YOLCU" and bilgi:
                    ozel_bilgi = f"Yolcu Kapasitesi: {bilgi[0]}"
                elif tur == "PETROL_TANKERI" and bilgi:
                    ozel_bilgi = f"Petrol Kapasitesi: {bilgi[0]} Litre"
                elif tur == "KONTEYNER" and bilgi:
                    ozel_bilgi = f"Konteyner Sayısı: {bilgi[0]}, Maksimum Ağırlık: {bilgi[1]} Ton"

                gemi_treeview.insert("", "end", values=(seri_no, gemi[1], gemi[2], gemi[3], tur, ozel_bilgi))
        else:
            messagebox.showinfo("Bilgi", "Veritabanında hiç gemi bulunamadı.")

# SEFER için

class SeferTablosu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Sefer Yönetim Sistemi")
        self.geometry("500x500")

        self.entry_s_ID = tk.Entry(self)
        self.entry_s_CIKIS = tk.Entry(self)
        self.entry_s_DONUS = tk.Entry(self)
        self.entry_s_LIMAN = tk.Entry(self)
        self.entry_seri_no = tk.Entry(self)

        self.label_sefer_id = tk.Label(self, text="Sefer ID:")
        self.label_sefer_id.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.entry_s_ID.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        self.label_sefer_cikis = tk.Label(self, text="Çıkış Tarihi:")
        self.label_sefer_cikis.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.entry_s_CIKIS.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        self.label_sefer_donus = tk.Label(self, text="Dönüş Tarihi:")
        self.label_sefer_donus.grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.entry_s_DONUS.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        self.label_sefer_liman = tk.Label(self, text="Çıkış Limanı:")
        self.label_sefer_liman.grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.entry_s_LIMAN.grid(row=3, column=1, padx=5, pady=5, sticky='w')

        self.label_seri_no = tk.Label(self, text="Gemi Seri No:")
        self.label_seri_no.grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.entry_seri_no.grid(row=4, column=1, padx=5, pady=5, sticky='w')

        self.ekle_button = tk.Button(self, text="Sefer Ekle", command=self.sefer_ekle_tk)
        self.ekle_button.grid(row=5, column=0, columnspan=2, padx=5, pady=10, sticky='we')

        self.label_silinecek_sefer_id = tk.Label(self, text="Silinecek Sefer ID:")
        self.label_silinecek_sefer_id.grid(row=6, column=0, padx=5, pady=5, sticky='w')
        self.entry_silinecek_sefer_id = tk.Entry(self)
        self.entry_silinecek_sefer_id.grid(row=6, column=1, padx=5, pady=5, sticky='w')

        self.sil_button = tk.Button(self, text="Sefer Sil", command=self.sefer_sil_tk)
        self.sil_button.grid(row=7, column=0, columnspan=2, padx=5, pady=10, sticky='we')

        self.liste_button = tk.Button(self, text="Sefer Listesi", command=self.sefer_goster)
        self.liste_button.grid(row=8, column=0, columnspan=2, padx=5, pady=10, sticky='we')

    def sefer_ekle_tk(self):
        try:
            s_ID = int(self.entry_s_ID.get())
            s_CIKIS = self.entry_s_CIKIS.get()
            s_DONUS = self.entry_s_DONUS.get()
            s_LIMAN = self.entry_s_LIMAN.get()
            seri_no = int(self.entry_seri_no.get())

            if all([s_ID, s_CIKIS, s_DONUS, s_LIMAN, seri_no]):
                sefer_ekle(s_ID, s_CIKIS, s_DONUS, s_LIMAN, seri_no)
                messagebox.showinfo("Başarılı", "Sefer başarıyla eklendi.")

                self.entry_s_ID.delete(0, tk.END)
                self.entry_s_CIKIS.delete(0, tk.END)
                self.entry_s_DONUS.delete(0, tk.END)
                self.entry_s_LIMAN.delete(0, tk.END)
                self.entry_seri_no.delete(0, tk.END)
            else:
                raise ValueError("Eksik bilgiler")
        except ValueError:
            messagebox.showerror("Hata", "Tüm alanları doldurun ve geçerli değerler girin.")

    def sefer_sil_tk(self):
        try:
            silinecek_s_ID = int(self.entry_silinecek_sefer_id.get())
            sefer_sil(silinecek_s_ID)
            messagebox.showinfo("Başarılı", "Sefer başarıyla silindi.")

            self.entry_silinecek_sefer_id.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Hata", "Geçerli bir Sefer ID girin.")

    def sefer_goster(self):
        seferler = sefer_belirle()

        yeni_pencere = tk.Toplevel(self)
        yeni_pencere.title("Sefer Listesi")
        yeni_pencere.geometry("400x400")

        sefer_treeview = ttk.Treeview(
            yeni_pencere,
            columns=("s_id", "s_cikis", "s_donus", "s_liman", "seri_no"),
            show='headings'
        )

        sefer_treeview.heading("s_id", text="Sefer ID")
        sefer_treeview.heading("s_cikis", text="Çıkış Tarihi")
        sefer_treeview.heading("s_donus", text="Dönüş Tarihi")
        sefer_treeview.heading("s_liman", text="Liman")
        sefer_treeview.heading("seri_no", text="Gemi Seri No")

        sefer_treeview.column("s_id", width=70)
        sefer_treeview.column("s_cikis", width=100)
        sefer_treeview.column("s_donus", width=100)
        sefer_treeview.column("s_liman", width=100)
        sefer_treeview.column("seri_no", width=100)

        sefer_treeview.pack(fill='both', expand=True)

        if seferler:
            for sefer in seferler:
                sefer_treeview.insert("", "end", values=(
                    sefer[0], sefer[1], sefer[2], sefer[3], sefer[4]
                ))
        else:
            messagebox.showinfo("Bilgi", "Hiç sefer bulunamadı.")

# PERSONEL için

class PersonelTablosu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Personel Yönetim Sistemi")
        self.geometry("500x500")

        self.label_personel_id = tk.Label(self, text="Personel ID:")
        self.entry_personel_id = tk.Entry(self)

        self.label_personel_ad = tk.Label(self, text="Ad:")
        self.entry_personel_ad = tk.Entry(self)

        self.label_personel_soyad = tk.Label(self, text="Soyad:")
        self.entry_personel_soyad = tk.Entry(self)

        self.label_personel_vatandaslik = tk.Label(self, text="Vatandaşlık:")
        self.entry_personel_vatandaslik = tk.Entry(self)

        self.label_personel_dogum_tarihi = tk.Label(self, text="Doğum Tarihi:")
        self.entry_personel_dogum_tarihi = tk.Entry(self)

        self.label_personel_meslek = tk.Label(self, text="Meslek:")
        self.entry_personel_meslek = tk.Entry(self)

        self.label_personel_ise_giris = tk.Label(self, text="İşe Giriş Tarihi:")
        self.entry_personel_ise_giris = tk.Entry(self)

        self.label_personel_adresi = tk.Label(self, text="Adres:")
        self.entry_personel_adresi = tk.Entry(self)

        self.label_personel_durum = tk.Label(self, text="Lisans veya Görev:")
        self.entry_personel_durum = tk.Entry(self)

        self.ekle_button = tk.Button(self, text="Personel Ekle", command=self.personel_ekle_tk)
        self.ekle_button.grid(row=9, column=0, columnspan=2, padx=5, pady=10, sticky='we')

        self.label_silinecek_personel_id = tk.Label(self, text="Silinecek Personel ID:")
        self.entry_silinecek_personel_id = tk.Entry(self)
        self.sil_button = tk.Button(self, text="Personel Sil", command=self.personel_sil_tk)

        self.liste_button = tk.Button(self, text="Personelleri Göster", command=self.personelleri_goster)

        self.label_personel_id.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.entry_personel_id.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        self.label_personel_ad.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.entry_personel_ad.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        self.label_personel_soyad.grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.entry_personel_soyad.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        self.label_personel_vatandaslik.grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.entry_personel_vatandaslik.grid(row=3, column=1, padx=5, pady=5, sticky='w')

        self.label_personel_dogum_tarihi.grid(row=4, column=0, padx=5, pady=5, sticky='w')
        self.entry_personel_dogum_tarihi.grid(row=4, column=1, padx=5, pady=5, sticky='w')

        self.label_personel_meslek.grid(row=5, column=0, padx=5, pady=5, sticky='w')
        self.entry_personel_meslek.grid(row=5, column=1, padx=5, pady=5, sticky='w')

        self.label_personel_ise_giris.grid(row=6, column=0, padx=5, pady=5, sticky='w')
        self.entry_personel_ise_giris.grid(row=6, column=1, padx=5, pady=5, sticky='w')

        self.label_personel_adresi.grid(row=7, column=0, padx=5, pady=5, sticky='w')
        self.entry_personel_adresi.grid(row=7, column=1, padx=5, pady=5, sticky='w')

        self.label_personel_durum.grid(row=8, column=0, padx=5, pady=5, sticky='w')
        self.entry_personel_durum.grid(row=8, column=1, padx=5, pady=5, sticky='w')

        self.ekle_button.grid(row=9, column=0, columnspan=2, padx=5, pady=10, sticky='we')


        self.label_silinecek_personel_id.grid(row=10, column=0, padx=5, pady=5, sticky='w')
        self.entry_silinecek_personel_id.grid(row=10, column=1, padx=5, pady=5, sticky='w')
        self.sil_button.grid(row=11, column=0, columnspan=2, padx=5, pady=10, sticky='we')

        self.liste_button.grid(row=12, column=0, columnspan=2, padx=5, pady=10, sticky='we')

    def personel_ekle_tk(self):
        try:
            personel_id = int(self.entry_personel_id.get())
            ad = self.entry_personel_ad.get()
            soyad = self.entry_personel_soyad.get()
            vatandaslik = self.entry_personel_vatandaslik.get()
            dogum_tarihi = self.entry_personel_dogum_tarihi.get()
            meslek = self.entry_personel_meslek.get()
            ise_giris = self.entry_personel_ise_giris.get()
            adres = self.entry_personel_adresi.get()
            durum = self.entry_personel_durum.get()

            personel_ekle(personel_id, ad, soyad, vatandaslik, dogum_tarihi, meslek, ise_giris, adres,durum)

            messagebox.showinfo("Başarılı", "Personel başarıyla eklendi.")

            self.entry_personel_id.delete(0, tk.END)
            self.entry_personel_ad.delete(0, tk.END)
            self.entry_personel_soyad.delete(0, tk.END)
            self.entry_personel_vatandaslik.delete(0, tk.END)
            self.entry_personel_dogum_tarihi.delete(0, tk.END)
            self.entry_personel_meslek.delete(0, tk.END)
            self.entry_personel_ise_giris.delete(0, tk.END)
            self.entry_personel_adresi.delete(0, tk.END)
            self.entry_personel_durum.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Hata", "Geçerli değerler giriniz.")

    def personel_sil_tk(self):
        try:
            personel_id = int(self.entry_silinecek_personel_id.get())
            personel_sil(personel_id)

            messagebox.showinfo("Başarılı", "Personel başarıyla silindi.")
            self.entry_silinecek_personel_id.delete(0, tk.END)
        except ValueError:
            messagebox.showerror("Hata", "Geçerli bir Personel ID giriniz.")

    def personelleri_goster(self):
        personeller = personelleri_al()

        yeni_pencere = tk.Toplevel(self)
        yeni_pencere.title("Personel Listesi")
        yeni_pencere.geometry("400x400")

        personel_treeview = ttk.Treeview(
            yeni_pencere,
            columns=("personel_id", "ad", "soyad", "vatandaslik", "dogum_tarihi", "meslek", "ise_giris", "adres","durum"),
            show='headings'
        )

        personel_treeview.heading("personel_id", text="Personel ID")
        personel_treeview.heading("ad", text="Ad")
        personel_treeview.heading("soyad", text="Soyad")
        personel_treeview.heading("vatandaslik", text="Vatandaşlık")
        personel_treeview.heading("dogum_tarihi", text="Doğum Tarihi")
        personel_treeview.heading("meslek", text="Meslek")
        personel_treeview.heading("ise_giris", text="İşe Giriş Tarihi")
        personel_treeview.heading("adres", text="Adres")
        personel_treeview.heading("durum", text="Lisans veya Görev")

        personel_treeview.column("personel_id", width=70)
        personel_treeview.column("ad", width=100)
        personel_treeview.column("soyad", width=100)
        personel_treeview.column("vatandaslik", width=100)
        personel_treeview.column("dogum_tarihi", width=100)
        personel_treeview.column("meslek", width=100)
        personel_treeview.column("ise_giris", width=100)
        personel_treeview.column("adres", width=150)
        personel_treeview.column("durum", width=100)

        personel_treeview.pack(fill='both', expand=True)

        if personeller:
            for personel in personeller:
                personel_treeview.insert("", "end", values=(
                    personel[0], personel[1], personel[2], personel[3], personel[4], personel[5], personel[6], personel[7],personel[8]
                ))
        else:
            messagebox.showerror("Hata", "Hiç personel bulunamadı.")

# LİMAN için

class LimanTablosu(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Liman Yönetim Sistemi")
        self.geometry("400x400")

        self.label_liman_adi = tk.Label(self, text="Liman Adı:")
        self.entry_liman_adi = tk.Entry(self)

        self.label_ulke = tk.Label(self, text="Ülke:")
        self.entry_ulke = tk.Entry(self)

        self.label_pasaport_istegi = tk.Label(self, text="Pasaport Gereksinimi (E/H):")
        self.entry_pasaport_istegi = tk.Entry(self)

        self.label_demirleme_ucreti = tk.Label(self, text="Demirleme Ücreti:")
        self.entry_demirleme_ucreti = tk.Entry(self)

        self.ekle_button = tk.Button(self, text="Liman Ekle", command=self.liman_ekle_tk)

        self.label_silinecek_liman_adi = tk.Label(self, text="Silinecek Liman Adı:")
        self.entry_silinecek_liman_adi = tk.Entry(self)

        self.label_silinecek_ulke = tk.Label(self, text="Silinecek Ülke:")
        self.entry_silinecek_ulke = tk.Entry(self)

        self.sil_button = tk.Button(self, text="Liman Sil", command=self.liman_sil_tk)

        self.liste_button = tk.Button(self, text="Liman Listesi", command=self.limanlari_goster_tk)

        self.label_liman_adi.grid(row=0, column=0, padx=5, pady=5, sticky='w')
        self.entry_liman_adi.grid(row=0, column=1, padx=5, pady=5, sticky='w')

        self.label_ulke.grid(row=1, column=0, padx=5, pady=5, sticky='w')
        self.entry_ulke.grid(row=1, column=1, padx=5, pady=5, sticky='w')

        self.label_pasaport_istegi.grid(row=2, column=0, padx=5, pady=5, sticky='w')
        self.entry_pasaport_istegi.grid(row=2, column=1, padx=5, pady=5, sticky='w')

        self.label_demirleme_ucreti.grid(row=3, column=0, padx=5, pady=5, sticky='w')
        self.entry_demirleme_ucreti.grid(row=3, column=1, padx=5, pady=5, sticky='w')

        self.ekle_button.grid(row=4, column=0, columnspan=2, padx=5, pady=10, sticky='we')

        self.label_silinecek_liman_adi.grid(row=5, column=0, padx=5, pady=5, sticky='w')
        self.entry_silinecek_liman_adi.grid(row=5, column=1, padx=5, pady=5, sticky='w')

        self.label_silinecek_ulke.grid(row=6, column=0, padx=5, pady=5, sticky='w')
        self.entry_silinecek_ulke.grid(row=6, column=1, padx=5, pady=5, sticky='w')

        self.sil_button.grid(row=7, column=0, columnspan=2, padx=5, pady=10, sticky='we')

        self.liste_button.grid(row=8, column=0, columnspan=2, padx=5, pady=10, sticky='we')

    def liman_ekle_tk(self):
        try:
            liman_adi = self.entry_liman_adi.get()
            ulke = self.entry_ulke.get()
            pasaport_istegi = self.entry_pasaport_istegi.get().upper()
            demirleme_ucreti = float(self.entry_demirleme_ucreti.get())

            if pasaport_istegi not in ['E', 'H']:
                raise ValueError("Pasaport gereksinimi yalnızca 'E' veya 'H' olmalıdır.")

            if all([liman_adi, ulke, pasaport_istegi, demirleme_ucreti]):
                liman_ekle(liman_adi, ulke, pasaport_istegi, demirleme_ucreti)
                messagebox.showinfo("Başarılı", "Liman başarıyla eklendi.")

                self.entry_liman_adi.delete(0, tk.END)
                self.entry_ulke.delete(0, tk.END)
                self.entry_pasaport_istegi.delete(0, tk.END)
                self.entry_demirleme_ucreti.delete(0, tk.END)

            else:
                raise ValueError("Eksik bilgiler.")

        except ValueError:
            messagebox.showerror("Hata", "Geçerli ve eksiksiz bilgiler girin.")

    def liman_sil_tk(self):
        try:
            liman_adi = self.entry_silinecek_liman_adi.get()
            ulke = self.entry_silinecek_ulke.get()

            if all([liman_adi, ulke]):
                silindi = liman_sil(liman_adi, ulke)
                if silindi:
                    messagebox.showinfo("Başarılı", "Liman başarıyla silindi.")
                    self.entry_silinecek_liman_adi.delete(0, tk.END)
                    self.entry_silinecek_ulke.delete(0, tk.END)
                else:
                    messagebox.showerror("Hata", "Liman adı ve ülke kombinasyonu bulunamadı.")
            else:
                raise ValueError("Eksik bilgiler.")

        except ValueError:
            messagebox.showerror("Hata", "Geçerli Liman Adı ve Ülke girin.")

    def limanlari_goster_tk(self):
        limanlar = limanlari_al()

        yeni_pencere = tk.Toplevel(self)
        yeni_pencere.title("Liman Listesi")
        yeni_pencere.geometry("400x400")

        liman_treeview = ttk.Treeview(
            yeni_pencere,
            columns=("liman_adi", "ulke", "pasaport_istegi", "demirleme_ucreti"),
            show='headings'
        )

        liman_treeview.heading("liman_adi", text="Liman Adı")
        liman_treeview.heading("ulke", text="Ülke")
        liman_treeview.heading("pasaport_istegi", text="Pasaport Gereksinimi (Y/N)")
        liman_treeview.heading("demirleme_ucreti", text="Demirleme Ücreti")

        liman_treeview.column("liman_adi", width=100)
        liman_treeview.column("ulke", width=100)
        liman_treeview.column("pasaport_istegi", width=80)
        liman_treeview.column("demirleme_ucreti", width=100)

        liman_treeview.pack(fill='both', expand=True)

        if limanlar:
            for liman in limanlar:
                liman_treeview.insert("", "end", values=(
                    liman[0], liman[1], liman[2], liman[3]
                ))
        else:
            messagebox.showinfo("Bilgi", "Veritabanında hiç liman bulunamadı.")

# AŞAMA 4: Veritabanı fonksiyonunu çalıştırarak giriş yapmak için form ekranlarını da çalıştırıyoruz.
# Kullanıcı terminalden hangi veritabanında veri işlemi yapmak istediğini seçer.

veritabani_olustur()

secim = input("HANGİ TABLO İÇİN VERİ İŞLEMİ YAPMAK İSTERSİNİZ?\n A: GEMİ  B: SEFER  C: PERSONEL  D: LİMAN\n Seçiniz:")

if secim.upper() == "A":
    uygulama = GemiTablosu()
    uygulama.mainloop()
elif secim.upper() == "B":
    uygulama = SeferTablosu()
    uygulama.mainloop()
elif secim.upper() == "C":
    uygulama = PersonelTablosu()
    uygulama.mainloop()
elif secim.upper() == "D":
    uygulama = LimanTablosu()
    uygulama.mainloop()
else:
    print("şıklardan seçim yapınız")
