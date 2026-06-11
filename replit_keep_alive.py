"""
Keep Alive Server for Replit
Keeps your bot online 24/7 with UptimeRobot
"""

from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return """
    <html>
    <head>
        <title>Paracord Bot - Online</title>
        <style>
            body {
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }
            .container {
                text-align: center;
                background: rgba(255, 255, 255, 0.1);
                padding: 40px;
                border-radius: 20px;
                box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
                backdrop-filter: blur(4px);
                border: 1px solid rgba(255, 255, 255, 0.18);
            }
            h1 {
                font-size: 3em;
                margin: 0;
                animation: pulse 2s infinite;
            }
            p {
                font-size: 1.5em;
                margin: 20px 0;
            }
            .status {
                display: inline-block;
                width: 20px;
                height: 20px;
                background: #00ff00;
                border-radius: 50%;
                animation: blink 1s infinite;
                margin-right: 10px;
            }
            @keyframes pulse {
                0%, 100% { transform: scale(1); }
                50% { transform: scale(1.05); }
            }
            @keyframes blink {
                0%, 50%, 100% { opacity: 1; }
                25%, 75% { opacity: 0.5; }
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 Paracord Bot</h1>
            <p><span class="status"></span>Bot is online and running!</p>
            <p style="font-size: 1em; opacity: 0.8;">Powered by Replit & Paracord v2.8</p>
        </div>
    </body>
    </html>
    """

@app.route('/ping')
def ping():
    return {'status': 'alive', 'bot': 'paracord', 'version': '2.8'}

@app.route('/health')
def health():
    return {'status': 'ok', 'message': 'Bot is running'}

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    """Start the keep-alive server in a separate thread"""
    t = Thread(target=run)
    t.daemon = True
    t.start()
    print("✅ Keep-alive server started on port 8080")
    print("📡 Add this URL to UptimeRobot to keep bot online 24/7")
