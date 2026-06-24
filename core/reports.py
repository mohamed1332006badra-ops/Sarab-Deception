import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from core.logger import DeceptionLogger
from config.settings import Config

class WeeklyReporter:
    def __init__(self):
        self.logger = DeceptionLogger()
        self.smtp_config = {
            'server': Config.SMTP_SERVER,
            'port': Config.SMTP_PORT,
            'email': Config.SMTP_EMAIL,
            'password': Config.SMTP_PASSWORD
        }
    
    def generate_report(self):
        attacks = self.logger.get_recent_attacks(1000)
        week_ago = datetime.now() - timedelta(days=7)
        weekly_attacks = [a for a in attacks if datetime.fromisoformat(a['timestamp']) > week_ago]
        
        stats = {'total': len(weekly_attacks), 'by_type': {}, 'by_severity': {}, 'top_attackers': {}}
        for attack in weekly_attacks:
            t = attack.get('threat_type', 'Unknown'); s = attack.get('severity', 'LOW'); src = attack.get('source_ip', 'Unknown')
            stats['by_type'][t] = stats['by_type'].get(t, 0) + 1
            stats['by_severity'][s] = stats['by_severity'].get(s, 0) + 1
            stats['top_attackers'][src] = stats['top_attackers'].get(src, 0) + 1
        
        stats['top_attackers'] = dict(sorted(stats['top_attackers'].items(), key=lambda x: x[1], reverse=True)[:5])
        return stats
    
    def generate_html_report(self, stats):
        html = f"""<div dir="rtl"><h1>تقرير الأمن الأسبوعي - سراب</h1><p>{datetime.now().strftime('%Y-%m-%d')}</p><p>إجمالي الهجمات: {stats['total']}</p></div>"""
        return html
    
    def send_report(self):
        stats = self.generate_report()
        html = self.generate_html_report(stats)
        msg = MIMEMultipart(); msg['From'] = self.smtp_config['email']; msg['To'] = self.smtp_config['email']; msg['Subject'] = "Weekly Security Report"
        msg.attach(MIMEText(html, 'html'))
        try:
            server = smtplib.SMTP(self.smtp_config['server'], self.smtp_config['port'])
            server.starttls(); server.login(self.smtp_config['email'], self.smtp_config['password'])
            server.send_message(msg); server.quit()
            return True
        except: return False
