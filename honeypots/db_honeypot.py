import socket
import threading
from core.analyzer import ThreatAnalyzer
from core.logger import DeceptionLogger
from core.notifier import AlertNotifier

class DBHoneypot:
    def __init__(self, port=5432):
        self.port = port
        self.analyzer = ThreatAnalyzer()
        self.logger = DeceptionLogger()
        self.notifier = AlertNotifier()
    
    def start(self):
        s = socket.socket()
        s.bind(('0.0.0.0', self.port))
        s.listen(5)
        while True:
            c, addr = s.accept()
            threading.Thread(target=self._handle, args=(c, addr), daemon=True).start()
    
    def _handle(self, c, addr):
        try:
            c.send(b"PostgreSQL 14.5\n")
            data = c.recv(1024).decode()
            attack = {'source_ip': addr[0], 'type': 'DB', 'commands': [data]}
            analysis = self.analyzer.analyze_attack({'commands': data, 'source_ip': addr[0]})
            full = {**attack, **analysis}
            self.logger.log_attack(full)
            self.notifier.send_alert(full)
        finally: c.close()

if __name__ == "__main__":
    DBHoneypot().start()
