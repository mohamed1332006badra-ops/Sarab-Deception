from flask import Flask, request, render_template_string
from core.analyzer import ThreatAnalyzer
from core.logger import DeceptionLogger
from core.notifier import AlertNotifier

app = Flask(__name__)
analyzer = ThreatAnalyzer()
logger = DeceptionLogger()
notifier = AlertNotifier()

HTML = "<html><body dir='rtl'><h2>تسجيل دخول النظام</h2><form method='POST'><input name='u' placeholder='المستخدم'><input name='p' type='password'><button>دخول</button></form></body></html>"

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = {'source_ip': request.remote_addr, 'type': 'WEB', 'details': f"U: {request.form.get('u')}, P: {request.form.get('p')}"}
        analysis = analyzer.analyze_attack({'commands': data['details'], 'source_ip': request.remote_addr})
        full_data = {**data, **analysis}
        logger.log_attack(full_data)
        notifier.send_alert(full_data)
        return "خطأ في الدخول"
    return HTML

if __name__ == "__main__":
    app.run(port=8888)
