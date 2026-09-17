# lock.py
"""
LIWILOCK - Kilit Ekranı Yöneticisi
Yasaklı site algılandığında tam ekran açılır, arka plandaki yasaklı tarayıcıyı (örneğin YouTube) 
kapatır ve doğru şifre girilene kadar sistemi kilitli tutar.
"""

import tkinter as tk
from tkinter import messagebox
import subprocess
import platform
from log import Logger

class LockScreen:
    def __init__(self, parent_root=None):
        Logger.write_log("Kilit ekranı tetiklendi ve açılıyor.")
        
        # Üst üste birden fazla kilit açılmasını önle
        if hasattr(LockScreen, "is_locked") and LockScreen.is_locked:
            return
        LockScreen.is_locked = True

        # 1. Adım: Yasaklı sekmeyi/pencereyi arkaplandan hemen kapat (Kill/Close)
        self.close_forbidden_browser_window()

        # 2. Adım: Tam ekran kilit penceresini oluştur
        self.top = tk.Toplevel(parent_root) if parent_root else tk.Tk()
        self.top.title("LIWILOCK - GÜVENLİK KİLİDİ")
        
        # Tam ekran ve pencereler üstünde kalma (Overrideredirect ile görev çubuğu ve butonları gizle)
        self.top.attributes("-fullscreen", True)
        self.top.attributes("-topmost", True)
        self.top.configure(bg="#11111b")
        
        # Odak sorununu çözmek için pencereyi öne getir ve odakla
        self.top.focus_force()
        self.top.grab_set()

        # İçerik Çerçevesi (Ortalanmış)
        main_frame = tk.Frame(self.top, bg="#11111b")
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        # Uyarı İkonu / Başlık
        lbl_title = tk.Label(
            main_frame, 
            text="🔒 SİSTEM GÜVENLİK KİLİDİ", 
            font=("Arial", 28, "bold"), 
            bg="#11111b", 
            fg="#f38ba8"
        )
        lbl_title.pack(pady=10)

        lbl_desc = tk.Label(
            main_frame, 
            text="Yasaklı bir web sayfasına erişim tespit edildi ve engellendi.\nKilidi açmak için lütfen yetkili şifresini giriniz.", 
            font=("Arial", 14), 
            bg="#11111b", 
            fg="#cdd6f4",
            justify="center"
        )
        lbl_desc.pack(pady=15)

        # Şifre Giriş Kutusu
        self.entry_pass = tk.Entry(
            main_frame, 
            font=("Arial", 20), 
            show="*", 
            justify="center", 
            bg="#313244", 
            fg="#cdd6f4",
            insertbackground="white",
            relief="flat",
            width=15
        )
        self.entry_pass.pack(pady=20)
        self.entry_pass.focus_set() # Doğrudan şifre kutusuna odaklan

        # Enter tuşuna basıldığında kilidi açmayı tetikle
        self.entry_pass.bind("<Return>", lambda event: self.verify_password())

        # Kilidi Aç Butonu
        btn_unlock = tk.Button(
            main_frame, 
            text="Kilidi Aç", 
            font=("Arial", 14, "bold"), 
            bg="#a6e3a1", 
            fg="#11111b",
            activebackground="#94e2d5",
            relief="flat",
            cursor="hand2",
            width=15,
            height=2,
            command=self.verify_password
        )
        btn_unlock.pack(pady=10)

        # Durum/Bilgi Etiketi
        self.lbl_status = tk.Label(
            main_frame, 
            text="LIWILOCK", 
            font=("Arial", 10, "italic"), 
            bg="#11111b", 
            fg="#6c7086"
        )
        self.lbl_status.pack(pady=10)

    def close_forbidden_browser_window(self):
        """Aktif olan yasaklı tarayıcı penceresini/sekmesini kapatır."""
        try:
            is_windows = platform.system() == "Windows"
            if is_windows:
                # Windows test ortamı için aktif pencereyi kapatma (Alt+F4 simülasyonu veya taskkill)
                import ctypes
                hwnd = ctypes.windll.user32.GetForegroundWindow()
                ctypes.windll.user32.PostMessageW(hwnd, 0x0010, 0, 0) # WM_CLOSE
            else:
                # Pardus / Linux (X11) ortamı için aktif pencereyi kapatma komutu
                # wmctrl veya xdotool kullanarak aktif pencerenin kapatılması sağlanır
                subprocess.run(["wmctrl", "-c", ":ACTIVE:"], stderr=subprocess.DEVNULL)
                # Alternatif xdotool tuş kombinasyonu (Ctrl+W sekme kapatma veya Alt+F4 pencere kapatma)
                subprocess.run(["xdotool", "key", "ctrl+w"], stderr=subprocess.DEVNULL)
                
            Logger.write_log("Yasaklı tarayıcı sekmesi/penceresi kapatıldı.")
        except Exception as e:
            Logger.write_log(f"Tarayıcı sekmesi kapatılırken hata oluştu: {e}")

    def verify_password(self):
        entered_pass = self.entry_pass.get().strip()
        CORRECT_PASS = "9032" # Belirttiğiniz şifre

        if entered_pass == CORRECT_PASS:
            Logger.write_log("Doğru şifre girildi, kilit kaldırılıyor.")
            LockScreen.is_locked = False
            self.top.destroy()
        else:
            Logger.write_log("Hatalı şifre denemesi.")
            self.lbl_status.config(text="❌ Hatalı Şifre! Tekrar deneyiniz.", fg="#f38ba8")
            self.entry_pass.delete(0, tk.END)