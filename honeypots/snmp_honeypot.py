import socket
class SNMPHoneypot:
    def __init__(self, port=161): self.port = port
    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('0.0.0.0', self.port))
        print(f"[+] SNMP Honeypot active on {self.port}")
        while True:
            data, addr = s.recvfrom(1024)
            print(f"[!] SNMP Poll from {addr[0]}")
if __name__ == "__main__": SNMPHoneypot().start()
