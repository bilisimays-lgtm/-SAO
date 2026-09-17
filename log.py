# log.py
"""
LIWILOCK - Loglama ve Kayıt Sistemi
Sistemdeki tüm işlemleri, kara liste yakalamalarını, şifre denemelerini 
ve uyarıları zaman damgasıyla birlikte log dosyasına yazar.
"""

import datetime
import os

class Logger:
    LOG_FILE = "liwlock_system.log"

    @staticmethod
    def write_log(message):
        """
        Belirtilen mesajı güncel tarih ve saat bilgisiyle birlikte 
        hem konsola yazdırır hem de log dosyasına kaydeder.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] {message}\n"
        
        # Konsola bilgi çıktısı ver
        print(f"[LIWILOCK LOG] {log_entry.strip()}")
        
        try:
            # Log dosyasına güvenli bir şekilde ekleme yap
            with open(Logger.LOG_FILE, "a", encoding="utf-8") as f:
                f.write(log_entry)
        except Exception as e:
            print(f"[LIWILOCK LOG HATASI] Log dosyasına yazılamadı: {e}")

    @staticmethod
    def read_logs(line_count=50):
        """
        Log dosyasındaki son kayıtları okur ve döndürür.
        Arayüz veya hata ayıklama için kullanılabilir.
        """
        if not os.path.exists(Logger.LOG_FILE):
            return ["Henüz log kaydı bulunmuyor."]
            
        try:
            with open(Logger.LOG_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()
                return lines[-line_count:] # Son N satırı döndür
        except Exception as e:
            return [f"Loglar okunurken hata oluştu: {e}"]