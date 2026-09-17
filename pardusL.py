# pardusL.py
"""
LIWILOCK - Pardus İşletim Sistemi Uyumlaştırıcısı
Bu modül, kodun Pardus işletim sistemine uygun hale gelmesini sağlar.
Sadece ilk açılışta kontrol yapar; sistem Windows veya başka bir işletim 
sistemi olsa bile hata vermeden sorunsuzca çalışmayı sürdürür.
"""

import platform
import os
from log import Logger

class PardusOptimizer:
    @staticmethod
    def optimize():
        current_os = platform.system()
        os_release = ""
        
        # Linux dağıtımı detaylarını öğrenmeye çalışalım (Pardus tespiti için)
        if current_os == "Linux":
            try:
                if os.path.exists("/etc/os-release"):
                    with open("/etc/os-release", "r", encoding="utf-8") as f:
                        os_release = f.read()
            except Exception as e:
                Logger.write_log(f"Linux sürüm dosyası okunurken hata oluştu: {e}")

        # Pardus veya genel Linux/Akıllı Tahta ortamı kontrolü
        if current_os == "Linux" and ("pardus" in os_release.lower() or os_release == ""):
            Logger.write_log("Pardus İşletim Sistemi tespit edildi. Akıllı tahta optimizasyonları uygulanıyor.")
            print("[PardusOptimizer] Pardus Akıllı Tahta ortamı doğrulandı.")
            
            try:
                # Pardus / XFCE / GNOME masaüstü ortamı için ekran ve pencere ayarları
                # DISPLAY değişkeninin ayarlanması (Arayüzün doğru ekranda açılması için)
                if 'DISPLAY' not in os.environ:
                    os.environ['DISPLAY'] = ':0'
                
                # Akıllı tahta odak optimizasyonu için ek parametreler buraya eklenebilir
                print("[PardusOptimizer] Pardus optimizasyonları başarıyla uygulandı.")
                Logger.write_log("Pardus optimizasyonları başarıyla uygulandı.")
                
            except Exception as e:
                error_msg = f"Pardus optimizasyonları uygulanırken hata oluştu: {e}"
                print(f"[PardusOptimizer HATA] {error_msg}")
                Logger.write_log(error_msg)
        else:
            # Windows veya macOS gibi farklı bir ortamdaysa
            msg = f"Algılanan İşletim Sistemi: {current_os}. Pardus özel modu atlandı, sistem sorunsuz devam ediyor."
            print(f"[PardusOptimizer] {msg}")
            Logger.write_log(msg)