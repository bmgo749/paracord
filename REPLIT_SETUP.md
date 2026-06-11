# 🚀 Cara Install & Run Paracord di Replit

## 📋 Langkah-langkah Instalasi

### 1️⃣ Setup Replit Project

1. **Buka Replit.com** dan login
2. **Klik "+ Create Repl"**
3. **Pilih Template**: Python
4. **Nama Repl**: Paracord-Bot (atau nama lain sesukamu)
5. **Klik "Create Repl"**

---

### 2️⃣ Install Paracord

Di **Shell/Console** Replit, jalankan command ini:

```bash
pip install nextcord
```

Tunggu sampai selesai install. Nextcord adalah library Discord yang dipakai Paracord.

---

### 3️⃣ Upload File Paracord

Ada 2 cara:

#### **Cara A: Clone dari GitHub (Recommended)**
Di Shell Replit:
```bash
git clone https://github.com/yourusername/paracord.git
cd paracord
```

#### **Cara B: Upload Manual**
1. Upload folder `paracord` (yang berisi main.py, runtime.py, dll)
2. Upload file `setup.py`
3. Upload file `bot.cord` (bot kamu)

Struktur folder harus seperti ini:
```
/home/runner/YourReplName/
├── paracord/
│   ├── __init__.py
│   ├── main.py
│   ├── runtime.py
│   ├── parser.py
│   ├── cli.py
│   ├── buttons.py
│   ├── selects.py
│   ├── modals.py
│   ├── uservars.py
│   ├── cooldowns.py
│   └── project-example/
│       └── (example files)
├── setup.py
└── bot.cord (file bot kamu)
```

---

### 4️⃣ Install Paracord Package

Di Shell Replit, jalankan:

```bash
pip install -e .
```

atau

```bash
python setup.py install
```

Ini akan menginstall command `para` yang bisa dipakai untuk run bot.

---

### 5️⃣ Setup Environment Variables (BOT TOKEN)

⚠️ **JANGAN taruh token langsung di code!**

1. Di Replit, klik **🔒 Secrets** (icon gembok di sidebar kiri)
2. Klik **+ New Secret**
3. **Key**: `BOT_TOKEN`
4. **Value**: (paste Discord bot token kamu)
5. **Klik "Add Secret"**

---

### 6️⃣ Buat File Bot

Buat file `bot.cord` di root folder:

```cord
$bot(
    $prefix("!")
    $intents("all")
    $activity(playing;"Paracord on Replit")
)

$addCommand(
    $name("ping")
    $sendMessage("🏓 Pong! Bot is running on Replit!")
)

$addCommand(
    $name("hello")
    $sendMessage("👋 Hello $username! Welcome!")
)

$run(BOT_TOKEN)
```

⚠️ **Perhatikan**: `$run(BOT_TOKEN)` **TANPA $** - ini akan otomatis ambil dari environment variable!

---

### 7️⃣ Buat File `main.py` (untuk Replit)

Replit butuh file `main.py` sebagai entry point:

```python
import os
import subprocess

# Get bot token from environment
bot_token = os.environ.get('BOT_TOKEN')

if not bot_token:
    print("❌ ERROR: BOT_TOKEN tidak ditemukan!")
    print("Tambahkan BOT_TOKEN di Secrets (🔒 icon)")
    exit(1)

# Replace BOT_TOKEN in .cord file
with open('bot.cord', 'r') as f:
    cord_content = f.read()

# Replace BOT_TOKEN with actual token
cord_content = cord_content.replace('BOT_TOKEN', bot_token)

# Save to temporary file
with open('bot_runtime.cord', 'w') as f:
    f.write(cord_content)

# Run the bot
print("🚀 Starting Paracord bot...")
subprocess.run(['para', 'run', 'bot_runtime.cord'])
```

---

### 8️⃣ Run Bot!

Ada 2 cara run bot:

#### **Cara A: Pakai Replit Run Button (Recommended)**
1. Klik tombol **▶️ Run** di atas
2. Bot akan otomatis jalan!

#### **Cara B: Manual via Shell**
```bash
para run bot.cord
```

atau

```bash
python main.py
```

---

## 🔧 Troubleshooting

### ❌ Error: `para: command not found`

**Solusi**:
```bash
pip install -e .
```

atau run langsung:
```bash
python -m paracord.cli run bot.cord
```

---

### ❌ Error: `No module named 'nextcord'`

**Solusi**:
```bash
pip install nextcord
```

---

### ❌ Error: `BOT_TOKEN tidak ditemukan`

**Solusi**:
1. Buka **Secrets** (🔒)
2. Tambahkan `BOT_TOKEN` dengan value token Discord bot kamu
3. Restart Repl

---

### ❌ Bot jalan tapi tidak online

**Kemungkinan**:
1. Token salah - cek lagi di Discord Developer Portal
2. Intents tidak aktif - aktifkan **all intents** di Discord Developer Portal:
   - Bot → Privileged Gateway Intents
   - ✅ Message Content Intent
   - ✅ Server Members Intent
   - ✅ Presence Intent

---

## 🌐 Keep Bot Always Online

Replit gratis akan sleep setelah tidak ada aktivitas. Untuk keep alive:

### **Cara 1: UptimeRobot (Recommended)**

1. Buat file `keep_alive.py`:

```python
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
```

2. Modify `main.py`:

```python
import os
import subprocess
from keep_alive import keep_alive

# Start web server
keep_alive()

# Get bot token
bot_token = os.environ.get('BOT_TOKEN')

if not bot_token:
    print("❌ ERROR: BOT_TOKEN tidak ditemukan!")
    exit(1)

# Replace BOT_TOKEN in .cord file
with open('bot.cord', 'r') as f:
    cord_content = f.read()

cord_content = cord_content.replace('BOT_TOKEN', bot_token)

with open('bot_runtime.cord', 'w') as f:
    f.write(cord_content)

# Run bot
print("🚀 Starting Paracord bot...")
subprocess.run(['para', 'run', 'bot_runtime.cord'])
```

3. Install Flask:
```bash
pip install flask
```

4. Daftar di **UptimeRobot.com**
5. Add Monitor:
   - Type: HTTP(s)
   - URL: (copy dari Replit webview URL)
   - Interval: 5 minutes
6. Bot akan tetap online 24/7!

---

### **Cara 2: Replit Always On (Paid)**

Upgrade ke Replit Hacker plan ($7/month) untuk fitur "Always On".

---

## 📦 Install Requirements Otomatis

Buat file `requirements.txt`:

```
nextcord>=2.0.0
```

Replit akan otomatis install packages dari file ini.

---

## 🎯 Example: Economy Bot di Replit

Buat file `economy_bot.cord`:

```cord
$bot(
    $prefix("!")
    $intents("all")
    $activity(playing;"Economy Bot on Replit")
)

// Balance
$addCommand(
    $name("balance")
    $sendMessage("💰 Balance: $getUserVar($userID;coins) coins")
)

// Daily reward
$addCommand(
    $name("daily")
    $cooldown("24h;⏰ Come back in $time!")
    $setUserVar($userID;coins;+$random(50,150))
    $sendMessage("🎁 Daily claimed! You got coins! Balance: $getUserVar($userID;coins)")
)

// Work
$addCommand(
    $name("work")
    $cooldown("1h;⏰ You're tired! Rest for $time")
    $setUserVar($userID;coins;+$random(20,80))
    $sendMessage("💼 You worked! Earned coins! Balance: $getUserVar($userID;coins)")
)

$run(BOT_TOKEN)
```

Run dengan:
```bash
python main.py
```

---

## 📝 Tips Replit

1. **Always save**: Replit auto-save, tapi pastikan file kesave sebelum run
2. **Use Secrets**: JANGAN taruh token di code langsung
3. **Check logs**: Lihat console untuk error messages
4. **Restart clean**: Stop bot (Ctrl+C), clear console, run lagi
5. **Storage limit**: Replit free punya limit 500MB
6. **User variables**: File `uservars.json` akan tersimpan otomatis di Replit

---

## 🆘 Butuh Bantuan?

### Check Logs
Lihat output di console untuk error messages.

### Test Command Installation
```bash
para --help
```

Seharusnya muncul help menu Paracord.

### Manual Run (Debug Mode)
```bash
python -m paracord.cli run bot.cord --debug
```

---

## ✅ Checklist Setup

- [ ] Python Repl dibuat
- [ ] `pip install nextcord` berhasil
- [ ] Folder `paracord` ter-upload
- [ ] `pip install -e .` berhasil
- [ ] BOT_TOKEN ditambahkan di Secrets
- [ ] File `bot.cord` dibuat
- [ ] File `main.py` dibuat
- [ ] Intents aktif di Discord Developer Portal
- [ ] Bot invite ke server dengan permission yang cukup
- [ ] Klik Run button
- [ ] Bot online di Discord! 🎉

---

## 🎉 Selesai!

Bot Paracord kamu sekarang running di Replit!

Test dengan command:
- `!ping` - Check if bot alive
- `!hello` - Test basic command
- `!balance` - Check economy features

**Happy botting!** 🚀
