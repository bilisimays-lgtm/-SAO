# repetitiveness.py
"""
LIWILOCK - Süreklilik ve Sistem Servisi Yöneticisi
Sistemi arka planda sürekli olarak ("Sistem Servisi" mantığıyla) çalıştırır.
Hiç kapanmadan döngü halinde çalışarak kara liste ve güvenlik kontrollerini yürütür.
"""

import time
import threading
from blacklist import BlacklistManager
from log import Logger

class SystemService:
    def __init__(self):
        self.blacklist_manager = BlacklistManager()
        self.is_running = False
        self.service_thread = None
        Logger.write_log("SystemService (repetitiveness.py) başlatıldı ve servise hazır.")

    def background_loop(self):
        """
        Arka planda sürekli dönen ana servis döngüsü.
        Akıllı tahta açık olduğu sürece aktif kalır ve denetimleri yapar.
        """
        Logger.write_log("Arka plan denetim döngüsü aktif hale geldi.")
        
        while self.is_running:
            try:
                # Burada akıllı tahta üzerindeki açık tarayıcı pencereleri, 
                # aktif sekmeler veya URL denetimleri gerçekleştirilebilir.
                # Örnek periyodik kontrol döngüsü (Her 5 saniyede bir):
                
                # Örnek simülasyon testi için aktif hedef kontrolü:
                # (Gerçek sistemde aktif pencere başlığı alma kütüphaneleri [pygetwindow vb.] entegre edilebilir)
                
                time.sleep(5) # İşlemciyi yormamak için periyodik bekleme süresi
                
            except Exception as e:
                Logger.write_log(f"Arka plan döngüsü çalışırken hata oluştu: {e}")
                time.sleep(5)

    def start_background_check(self):
        """Servisi ayrı bir arka plan iş parçacığında (Thread) başlatır."""
        if not self.is_running:
            self.is_running = True
            self.service_thread = threading.Thread(target=self.background_loop, daemon=True)
            self.service_thread.start()
            Logger.write_log("Sistem Servisi arka planda çalışmaya başladı (Daemon Thread).")

    def stop_background_check(self):
        """Çalışmakta olan servisi güvenli bir şekilde durdurur."""
        if self.is_running:
            self.is_running = False
            Logger.write_log("Sistem Servisi durduruldu.")