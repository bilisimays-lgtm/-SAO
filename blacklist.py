# blacklist.py
"""
LIWILOCK - Kara Liste ve Etkileşim Takipçisi
Kara listedeki siteleri (örn. youtube.com, instagram.com vb.) denetler.
Etkileşim yakalandığında log.py'a aktarır ve kilit ekranına haber verir.
"""

import time
import threading
from log import Logger

class BlacklistManager:
    def __init__(self):
        # Kara listede tutulan örnek siteler
        self.blacklisted_sites = [
            "youtube.com", 
            "instagram.com", 
            "facebook.com", 
            "twitter.com", 
            "tiktok.com",
            "poki.com",
            "crazygames.com"
            
        ]
        
        # Uyarı gecikmesi (Siteler etkileşime girince log.py'a aktarılmadan önceki süre - saniye cinsinden)
        self.warning_delay_seconds = 3

    def add_to_blacklist(self, site_name):
        """Kara listeye yeni bir site ekler."""
        if site_name not in self.blacklisted_sites:
            self.blacklisted_sites.append(site_name.lower())
            Logger.write_log(f"Yeni site kara listeye eklendi: {site_name}")

    def remove_from_blacklist(self, site_name):
        """Kara listeden site çıkarır."""
        if site_name.lower() in self.blacklisted_sites:
            self.blacklisted_sites.remove(site_name.lower())
            Logger.write_log(f"Site kara listeden çıkarıldı: {site_name}")

    def check_interaction(self, active_target_string, lock_callback=None):
        """
        Aktif pencere başlığını veya URL metnini kara liste ile kıyaslar.
        Eşleşme bulursa uyarı süreci başlatır ve loglar.
        """
        target_lower = active_target_string.lower()
        
        for site in self.blacklisted_sites:
            if site in target_lower:
                Logger.write_log(f"UYARI: Kara listedeki site ile etkileşim tespit edildi -> {site}")
                
                # Belirtilen süre (uyarıcı gecikmesi) sonrasında log.py ve kilit tetiklemesi
                def delayed_trigger():
                    time.sleep(self.warning_delay_seconds)
                    Logger.write_log(f"Kara liste ihlali onaylandı ve loglandı: {site}")
                    if lock_callback:
                        lock_callback() # Kilit ekranını (lock.py) çağırır

                # Arka planda gecikmeli tetikleme başlat
                threading.Thread(target=delayed_trigger, daemon=True).start()
                return True
                
        return False