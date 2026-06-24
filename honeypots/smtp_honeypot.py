import socket, threading
class SMTPHoneypot:
    def __init__(self, port=25): self.port = port
    def start(self):
        s = socket.socket()
        s.bind(('0.0.0.0', self.port))
        s.listen(5)
        print(f"[+] SMTP Honeypot active on {self.port}")
        while True:
            c, addr = s.accept()
            c.send(b"220 mail.company.com ESMTP\r\n")
            c.close()
if __name__ == "__main__": SMTPHoneypot().start()
