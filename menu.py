# menu.py
"""
LIWILOCK - Menü ve Arayüz Yöneticisi
Tüm menüleri, butonları, görsel öğeleri ve kullanıcı arayüzü etkileşimlerini yönetir.
reader.py entegrasyonu ile arka plandaki web girişimlerini anlık dinler.
"""

import tkinter as tk
from tkinter import messagebox

# Diğer modüllerin içe aktarılması
from pardusL import PardusOptimizer
from lock import LockScreen
from log import Logger
from reader import ReaderService

class MenuManager:
    def __init__(self):
        Logger.write_log("MenuManager başlatılıyor...")
        
        # Pardus işletim sistemi optimizasyonlarını ilk açılışta uygula
        PardusOptimizer.optimize()
        
        # Ana Tkinter penceresini oluştur
        self.root = tk.Tk()
        self.root.title("LIWILOCK - Akıllı Tahta Güvenlik Paneli")
        self.root.geometry("450x550")
        self.root.configure(bg="#1e1e2e") # Modern koyu tema arka planı
        self.root.resizable(False, False)
        
        # Arayüz elemanlarını yerleştir
        self.create_widgets()
        
        # reader.py servisini başlat ve kilit tetikleyicisini güvenli bağla
        self.init_reader_service()
        
        Logger.write_log("MenuManager arayüzü ve tarama servisi başarıyla oluşturuldu.")

    def create_widgets(self):
        # Üst Başlık Çerçevesi
        header_frame = tk.Frame(self.root, bg="#1e1e2e")
        header_frame.pack(pady=30)

        title_label = tk.Label(
            header_frame, 
            text="LIWILOCK KONTROL", 
            font=("Arial", 18, "bold"), 
            bg="#1e1e2e", 
            fg="#cdd6f4"
        )
        title_label.pack()

        subtitle_label = tk.Label(
            header_frame, 
            text="Pardus Akıllı Tahta Güvenlik Katmanı", 
            font=("Arial", 10, "italic"), 
            bg="#1e1e2e", 
            fg="#a6adc8"
        )
        subtitle_label.pack(pady=5)

        # Bilgilendirme Kartı / Alanı
        info_frame = tk.Frame(self.root, bg="#313244", relief="flat", bd=0)
        info_frame.pack(pady=10, padx=30, fill="x")

        info_text = (
            "• Sistem arkaplanda web trafiğini tarar.\n"
            "• Kara listedeki sitelerle etkileşimi anında engeller.\n"
            "• Şifre: [9032] (Açık kalma süresi: 40 dk)"
        )
        info_label = tk.Label(
            info_frame, 
            text=info_text, 
            font=("Arial", 11), 
            bg="#313244", 
            fg="#bac2de", 
            justify="left"
        )
        info_label.pack(padx=15, pady=15)

        # Butonlar Alanı
        button_frame = tk.Frame(self.root, bg="#1e1e2e")
        button_frame.pack(pady=20)

        # Manuel Kilit Test Butonu
        btn_test_lock = tk.Button(
            button_frame, 
            text="🔒 Kilit Ekranını Test Et", 
            font=("Arial", 12, "bold"), 
            bg="#f38ba8", 
            fg="#11111b",
            activebackground="#eba0ac", 
            activeforeground="#11111b",
            relief="flat", 
            cursor="hand2",
            width=22, 
            height=2,
            command=self.trigger_lock_screen
        )
        btn_test_lock.pack(pady=10)

        # Logları Görüntüle Butonu
        btn_logs = tk.Button(
            button_frame, 
            text="📄 Log Kayıtlarını Göster", 
            font=("Arial", 11), 
            bg="#45475a", 
            fg="#cdd6f4",
            activebackground="#585b70", 
            activeforeground="#ffffff",
            relief="flat", 
            cursor="hand2",
            width=22, 
            height=2,
            command=self.show_logs_info
        )
        btn_logs.pack(pady=5)

        # Durum Çubuğu (Status Bar)
        self.status_label = tk.Label(
            self.root, 
            text="Durum: Web Tarama ve Koruma Aktif ✅", 
            font=("Arial", 10, "bold"), 
            bg="#1e1e2e", 
            fg="#a6e3a1"
        )
        self.status_label.pack(side="bottom", pady=20)

    def init_reader_service(self):
        """Web girişimlerini tarayacak reader.py servisini arayüze entegre eder."""
        try:
            def trigger_system_lock():
                # Tkinter arayüz iş parçacığı güvenliği (Thread-safe) için after kullanıyoruz
                self.root.after(0, lambda: LockScreen(self.root))

            self.reader_service = ReaderService(lock_callback=trigger_system_lock)
            self.reader_service.start_reading()
            Logger.write_log("ReaderService arayüze başarıyla bağlandı ve tarama döngüsü başlatıldı.")
        except Exception as e:
            Logger.write_log(f"ReaderService başlatılırken hata oluştu: {e}")

    def trigger_lock_screen(self):
        Logger.write_log("Kullanıcı arayüz üzerinden manuel kilit testi başlattı.")
        LockScreen(self.root)

    def show_logs_info(self):
        Logger.write_log("Kullanıcı log bilgi ekranını açtı.")
        messagebox.showinfo(
            "Log Bilgisi", 
            "Tüm işlemler 'liwlock_system.log' dosyasına kaydedilmektedir.\nKara liste ve şifre denemeleri buradan takip edilebilir."
        )

    def run(self):
        # Tkinter ana döngüsünü başlat
        self.root.mainloop()