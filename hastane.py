import tkinter as tk
from tkinter import messagebox, ttk

# sınıflar
class Hasta:
    def __init__(self, ad, tc):
        self.ad = ad
        self.tc = tc
        self.rlist = []

class Doktor:
    def __init__(self, ad, bolum, saatler):
        self.ad = ad
        self.bolum = bolum
        self.saatler = saatler

class Randevu:
    def __init__(self, saat, dr, hasta):
        self.saat = saat
        self.dr = dr
        self.hasta = hasta

    def __str__(self):
        return self.saat + " - " + self.dr.ad

class App:
    def __init__(self, pencere):
        self.win = pencere
        self.win.title("Randevu Sistemi")

        self.hlist = []
        self.dlist = []
        self.rlist = []
        self.giris_yapan = None

        # doktorlar
        self.doktor_ekle("Dr. Berkay", "Kardiyoloji", ["2025-05-01 10:00", "2025-05-01 14:00"])
        self.doktor_ekle("Dr. Eren", "Ağız ve Diş Sağlığı", ["2025-05-02 09:00", "2025-05-02 13:00"])

        self.login_ekrani()

    def doktor_ekle(self, ad, bolum, saatler):
        self.dlist.append(Doktor(ad, bolum, saatler))

    def login_ekrani(self):
        self.temizle()
        tk.Label(self.win, text="Giriş", font=("Arial", 14)).pack(pady=10)
        tk.Label(self.win, text="Adınız:").pack()
        self.ent_ad = tk.Entry(self.win)
        self.ent_ad.pack()
        tk.Label(self.win, text="TC Kimlik:").pack()
        self.ent_tc = tk.Entry(self.win)
        self.ent_tc.pack()
        tk.Button(self.win, text="Giriş Yap", command=self.giris_yap).pack(pady=10)

    def giris_yap(self):
        ad = self.ent_ad.get()
        tc = self.ent_tc.get()
        if not ad or not tc:
            messagebox.showerror("Hata", "Boş bırakmayınız")
            return

        varmi = None
        for h in self.hlist:
            if h.tc == tc:
                varmi = h
                break

        if varmi:
            self.giris_yapan = varmi
        else:
            yeni = Hasta(ad, tc)
            self.hlist.append(yeni)
            self.giris_yapan = yeni

        self.menu_ekrani()

    def menu_ekrani(self):
        self.temizle()
        tk.Label(self.win, text=f"Merhabalar {self.giris_yapan.ad}", font=("Arial", 12)).pack(pady=5)

        tk.Label(self.win, text="Doktor Seçiniz:").pack()
        self.cmb_doktor = ttk.Combobox(self.win, values=[d.ad for d in self.dlist])
        self.cmb_doktor.pack()

        tk.Label(self.win, text="Saat Seçiniz:").pack()
        self.cmb_saat = ttk.Combobox(self.win)
        self.cmb_saat.pack()

        self.cmb_doktor.bind("<<ComboboxSelected>>", self.saat_guncelle)

        tk.Button(self.win, text="Randevu Al", command=self.r_al).pack(pady=5)
        tk.Button(self.win, text="Randevu Sil", command=self.r_sil).pack(pady=5)
        tk.Button(self.win, text="Randevularım", command=self.r_goster).pack(pady=5)
        tk.Button(self.win, text="Çıkış", command=self.login_ekrani).pack(pady=5)

    def saat_guncelle(self, e):
        secilen = self.cmb_doktor.get()
        dr = next((d for d in self.dlist if d.ad == secilen), None)
        if dr:
            self.cmb_saat['values'] = dr.saatler

    def r_al(self):
        d_ismi = self.cmb_doktor.get()
        saat = self.cmb_saat.get()
        dr = next((d for d in self.dlist if d.ad == d_ismi), None)
        if dr and saat in dr.saatler:
            r = Randevu(saat, dr, self.giris_yapan)
            self.rlist.append(r)
            self.giris_yapan.rlist.append(r)
            dr.saatler.remove(saat)
            self.saat_guncelle(None)
            messagebox.showinfo("Tamam", "Randevu alındı")
        else:
            messagebox.showerror("Hata", "Alınamadı")

    def r_sil(self):
        saat = self.cmb_saat.get()
        r = next((r for r in self.rlist if r.hasta.tc == self.giris_yapan.tc and r.saat == saat), None)
        if r:
            self.rlist.remove(r)
            self.giris_yapan.rlist.remove(r)
            r.dr.saatler.append(saat)
            self.saat_guncelle(None)
            messagebox.showinfo("Tamam", "Silindi")
        else:
            messagebox.showerror("Yok", "Randevu yok")

    def r_goster(self):
        metin = "\n".join(str(r) for r in self.giris_yapan.rlist)
        if not metin:
            metin = "Randevu yok"
        messagebox.showinfo("Randevular", metin)

    def temizle(self):
        for i in self.win.winfo_children():
            i.destroy()

root = tk.Tk()
app = App(root)
root.mainloop()