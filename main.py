# main.py
"""
LIWILOCK - Ana Yönetim ve Başlatıcı Scripti
Bu script, tüm sistemin kalbidir. Diğer tüm modüllerin (menu, pardusL, lock, 
blacklist, log, repetitiveness, reader) koordinasyonunu ve ayağa kaldırılmasını sağlar.
"""

import sys
import os

def check_dependencies():
    """Gerekli modüllerin varlığını ve dosya bütünlüğünü kontrol eder."""
    required_files = [
        "menu.py", 
        "pardusL.py", 
        "lock.py", 
        "blacklist.py", 
        "log.py", 
        "repetitiveness.py",
        "reader.py"
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
            
    if missing_files:
        print(f"[LIWILOCK HATA] Eksik modül dosyaları tespit edildi: {missing_files}")
        print("[LIWILOCK] Lütfen tüm scriptlerin aynı dizinde olduğundan emin olun.")
        sys.exit(1)
    else:
        print("[LIWILOCK] Tüm modül dosyaları tam ve eksiksiz.")

def main():
    print("=" * 60)
    print("      LIWILOCK - AKILLI TAHTA GÜVENLİK VE KONTROL SİSTEMİ")
    print("=" * 60)
    
    # 1. Dosya bütünlük kontrolü
    check_dependencies()
    
    # 2. Log modülünü içe aktar ve başlangıç kaydı düş
    try:
        from log import Logger
        Logger.write_log("main.py çalıştırıldı. Sistem başlatma süreci başladı.")
    except Exception as e:
        print(f"[Kritik Hata] Log modülü yüklenemedi: {e}")
        sys.exit(1)

    # 3. Arkaplan servis modülünü (repetitiveness.py) başlat
    try:
        from repetitiveness import SystemService
        service = SystemService()
        service.start_background_check()
        Logger.write_log("Arka plan sistem servisi başarıyla tetiklendi.")
    except Exception as e:
        Logger.write_log(f"Arka plan servisi başlatılamadı: {e}")

    # 4. Arayüz ve Menü yöneticisini (menu.py) yükle ve çalıştır
    try:
        from menu import MenuManager
        Logger.write_log("MenuManager yükleniyor, arayüz başlatılıyor...")
        
        app = MenuManager()
        app.run()
        
    except Exception as e:
        Logger.write_log(f"Arayüz çalışırken kritik hata oluştu: {e}")
        print(f"[HATA] Arayüz başlatılamadı: {e}")
    finally:
        Logger.write_log("LIWILOCK sistemi kapatılıyor.")
        print("[LIWILOCK] Sistem güvenli bir şekilde sonlandırıldı.")

if __name__ == "__main__":
    main()