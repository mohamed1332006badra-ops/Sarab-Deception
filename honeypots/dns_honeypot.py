import socket, threading, struct
class DNSHoneypot:
    def __init__(self, port=53): self.port = port
    def start(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.bind(('0.0.0.0', self.port))
        print(f"[+] DNS Honeypot active on {self.port}")
        while True:
            data, addr = s.recvfrom(512)
            print(f"[!] DNS Query from {addr[0]}")
if __name__ == "__main__": DNSHoneypot().start()
