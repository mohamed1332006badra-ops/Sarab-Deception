import socket
import threading
from datetime import datetime
import time
from core.analyzer import ThreatAnalyzer
from core.logger import DeceptionLogger
from core.notifier import AlertNotifier

class SSHHoneypot:
    def __init__(self, host='0.0.0.0', port=2222):
        self.host = host
        self.port = port
        self.analyzer = ThreatAnalyzer()
        self.logger = DeceptionLogger()
        self.notifier = AlertNotifier()
        self.fake_commands = {'ls': 'Desktop Documents Downloads\n', 'pwd': '/home/root\n', 'whoami': 'root\n'}
    
    def start(self):
        server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind((self.host, self.port))
        server.listen(5)
        while True:
            client, addr = server.accept()
            threading.Thread(target=self._handle_client, args=(client, addr), daemon=True).start()
    
    def _handle_client(self, client_socket, addr):
        attack_data = {'source_ip': addr[0], 'type': 'SSH', 'commands': []}
        try:
            client_socket.send(b"SSH-2.0-OpenSSH_8.9p1 Ubuntu\r\n")
            client_socket.send(b"login: ")
            user = client_socket.recv(1024).decode().strip()
            client_socket.send(b"Password: ")
            password = client_socket.recv(1024).decode().strip()
            attack_data['details'] = f"User: {user}, Pass: {password}"
            client_socket.send(b"\r\nLogin incorrect\r\nroot@ubuntu:~$ ")
            cmd = client_socket.recv(1024).decode().strip()
            attack_data['commands'].append(cmd)
            client_socket.send(self.fake_commands.get(cmd, "bash: command not found\n").encode())
        finally:
            client_socket.close()
            analysis = self.analyzer.analyze_attack({'commands': ' '.join(attack_data['commands']), 'source_ip': addr[0]})
            full_data = {**attack_data, **analysis}
            self.logger.log_attack(full_data)
            self.notifier.send_alert(full_data)

if __name__ == "__main__":
    SSHHoneypot().start()
