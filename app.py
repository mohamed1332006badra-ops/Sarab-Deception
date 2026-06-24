from api.auth import create_token
import os
from flask import Flask, render_template, jsonify, request
from flask_socketio import SocketIO
import threading
import subprocess
import schedule
import time
from config.settings import Config
from core.logger import DeceptionLogger
from core.reports import WeeklyReporter

app = Flask(__name__)
app.config['SECRET_KEY'] = Config.SECRET_KEY
socketio = SocketIO(app, cors_allowed_origins="*")
logger = DeceptionLogger()

@app.route('/')
def index(): return render_template('dashboard.html')

@app.route('/api/attacks')
def get_attacks(): return jsonify({'data': logger.get_recent_attacks()})

@app.route('/api/stats')
def get_stats(): return jsonify({'data': logger.get_attack_stats()})

@app.route('/api/honeypots')
def get_status(): return jsonify({'data': {'ssh': True, 'web': True, 'db': True, 'rdp': True, 'ftp': True}})

@app.route('/pricing')
def pricing():
    return """<div dir="rtl"><h1>خطط التسعير</h1><p>أساسي: $999/سنة</p><p>متقدم: $2,999/سنة</p></div>"""

def start_services():
    env = os.environ.copy(); env['PYTHONPATH'] = os.getcwd(); subprocess.Popen(['python3', 'honeypots/ssh_honeypot.py'])
    subprocess.Popen(['python3', 'honeypots/dns_honeypot.py'])
    subprocess.Popen(['python3', 'honeypots/smtp_honeypot.py'])
    subprocess.Popen(['python3', 'honeypots/snmp_honeypot.py'])
    env = os.environ.copy(); env['PYTHONPATH'] = os.getcwd(); subprocess.Popen(['python3', 'honeypots/db_honeypot.py'])
    env = os.environ.copy(); env['PYTHONPATH'] = os.getcwd(); subprocess.Popen(['python3', 'honeypots/rdp_honeypot.py'])

def schedule_weekly_report():
    reporter = WeeklyReporter()
    schedule.every().sunday.at("08:00").do(reporter.send_report)
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == '__main__':
    threading.Thread(target=start_services, daemon=True).start()
    threading.Thread(target=schedule_weekly_report, daemon=True).start()
    socketio.run(app, host='0.0.0.0', port=5000)
