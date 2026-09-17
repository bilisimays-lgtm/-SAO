# reader.py
"""
LIWILOCK - Tarayıcı ve Etkileşim Okuyucu
"""

import time
import subprocess
import platform
import re
from blacklist import BlacklistManager
from log import Logger

class ReaderService:
    def __init__(self, lock_callback=None):
        self.blacklist_mgr = BlacklistManager()
        self.lock_callback = lock_callback
        self.is_active = False
        Logger.write_log("ReaderService başlatıldı.")

    def get_active_window_title_linux(self):
        try:
            output = subprocess.check_output(["xdotool", "getactivewindow", "getwindowname"], stderr=subprocess.DEVNULL)
            return output.decode("utf-8", errors='ignore').strip().lower()
        except Exception:
            try:
                root = subprocess.Popen(['xprop', '-root', '_NET_ACTIVE_WINDOW'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                stdout, _ = root.communicate()
                m = re.search(b'^_NET_ACTIVE_WINDOW.* ([\\w]+)$', stdout)
                if m:
                    window_id = m.group(1)
                    window = subprocess.Popen(['xprop', '-id', window_id.decode(), 'WM_NAME'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                    stdout_w, _ = window.communicate()
                    wmatch = re.search(b'WM_NAME\\(\\w+\\)\\s*=\\s*(?P<name>.+)$', stdout_w)
                    if wmatch:
                        return wmatch.group('name').decode('utf-8', errors='ignore').strip('"').lower()
            except Exception:
                pass
        return ""

    def get_active_window_title_windows(self):
        try:
            import ctypes
            hWnd = ctypes.windll.user32.GetForegroundWindow()
            length = ctypes.windll.user32.GetWindowTextLengthW(hWnd)
            buf = ctypes.create_unicode_buffer(length + 1)
            ctypes.windll.user32.GetWindowTextW(hWnd, buf, length + 1)
            return buf.value.lower()
        except Exception:
            return ""

    def scan_loop(self):
        is_windows = platform.system() == "Windows"
        while self.is_active:
            try:
                title = self.get_active_window_title_windows() if is_windows else self.get_active_window_title_linux()
                if title:
                    for site in self.blacklist_mgr.blacklisted_sites:
                        keyword = site.split('.')[0].lower()
                        if keyword in title:
                            Logger.write_log(f"Yasaklı site yakalandı: {site} ({title})")
                            if self.lock_callback:
                                self.lock_callback()
                            time.sleep(5) # Üst üste tetiklenmeyi önle
                            break
            except Exception as e:
                Logger.write_log(f"Reader döngü hatası: {e}")
            time.sleep(0.4)

    def start_reading(self):
        if not self.is_active:
            self.is_active = True
            import threading
            threading.Thread(target=self.scan_loop, daemon=True).start()

    def stop_reading(self):
        self.is_active = False