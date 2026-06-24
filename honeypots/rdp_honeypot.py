import socket
import threading
from datetime import datetime
from core.analyzer import ThreatAnalyzer
from core.logger import DeceptionLogger
from core.notifier import AlertNotifier

class RDPHoneypot:
    def __init__(self, host='0.0.0.0', port=3389):
        self.host = host; self.port = port
        self.analyzer = ThreatAnalyzer(); self.logger = DeceptionLogger(); self.notifier = AlertNotifier()
    
    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port)); server.listen(5)
        while True:
            c, addr = server.accept()
            threading.Thread(target=self._handle, args=(c, addr), daemon=True).start()
    
    def _handle(self, c, addr):
        try:
            c.send(b"\x03\x00\x00\x13\x0e\xe0\x00\x00\x00\x00\x00\x01\x00\x08\x00\x03\x00\x00\x00")
            data = {'source_ip': addr[0], 'type': 'RDP_ATTACK', 'severity': 'HIGH', 'details': 'RDP Connection Attempt'}
            self.logger.log_attack(data); self.notifier.send_alert(data)
        finally: c.close()

if __name__ == "__main__":
    RDPHoneypot().start()
