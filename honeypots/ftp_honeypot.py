import socket
import threading
from datetime import datetime
from core.analyzer import ThreatAnalyzer
from core.logger import DeceptionLogger
from core.notifier import AlertNotifier

class FTPHoneypot:
    def __init__(self, host='0.0.0.0', port=21):
        self.host = host
        self.port = port
        self.analyzer = ThreatAnalyzer()
        self.logger = DeceptionLogger()
        self.notifier = AlertNotifier()
    
    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(5)
        print(f"[+] فخ FTP يعمل على المنفذ {self.port}")
        
        while True:
            client, addr = server.accept()
            threading.Thread(target=self._handle_client, args=(client, addr)).start()
    
    def _handle_client(self, client, addr):
        try:
            client.send(b"220 FTP Server (vsftpd 3.0.5) ready\r\n")
            attack_data = {
                'source_ip': addr[0],
                'type': 'FTP_ATTACK',
                'timestamp': datetime.now().isoformat(),
                'severity': 'MEDIUM',
                'details': 'محاولة اتصال FTP وهمي'
            }
            self.logger.log_attack(attack_data)
            client.close()
        except:
            pass

if __name__ == '__main__':
    honeypot = FTPHoneypot()
    honeypot.start()
