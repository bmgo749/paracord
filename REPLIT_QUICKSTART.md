# ⚡ Paracord - Replit Quick Start

## 🚀 Install dalam 5 Menit!

### 1. Buat Replit Project
- Buka [Replit.com](https://replit.com)
- Klik **"+ Create Repl"**
- Pilih **"Python"**
- Nama: **"Paracord-Bot"**

### 2. Upload Files
Upload file-file ini ke Replit:

**📁 Required Files:**
```
📦 Your Replit Project
├── 📁 paracord/          (upload seluruh folder)
│   ├── __init__.py
│   ├── main.py
│   ├── runtime.py
│   ├── parser.py
│   ├── cli.py
│   ├── buttons.py
│   ├── selects.py
│   ├── modals.py
│   ├── uservars.py
│   └── cooldowns.py
├── 📄 setup.py           (untuk install command 'para')
├── 📄 replit_main.py     (entry point - rename jadi main.py)
├── 📄 bot.cord           (atau pakai replit_bot_example.cord)
└── 📄 requirements.txt   (auto-install dependencies)
```

### 3. Setup Token
1. Klik **🔒 Secrets** (icon gembok)
2. **Key**: `BOT_TOKEN`
3. **Value**: (Discord bot token)
4. **Add Secret**

### 4. Install Paracord
Di **Shell** tab, jalankan:
```bash
pip install -e .
```

### 5. Run Bot
Klik tombol **▶️ Run** - Done! 🎉

---

## 📝 File Contents

### `main.py` (rename dari replit_main.py)
```python
#!/usr/bin/env python3
import os
import sys
import subprocess

bot_token = os.environ.get('BOT_TOKEN')

if not bot_token:
    print("❌ Add BOT_TOKEN to Secrets!")
    sys.exit(1)

with open('bot.cord', 'r') as f:
    content = f.read().replace('BOT_TOKEN', bot_token)

with open('bot_runtime.cord', 'w') as f:
    f.write(content)

subprocess.run(['para', 'run', 'bot_runtime.cord'])
```

### `bot.cord` (simple example)
```cord
$bot(
    $prefix("!")
    $intents("all")
)

$addCommand(
    $name("ping")
    $sendMessage("🏓 Pong! Online on Replit!")
)

$addCommand(
    $name("balance")
    $sendMessage("💰 Balance: $getUserVar($userID;coins) coins")
)

$addCommand(
    $name("daily")
    $cooldown("24h;Come back in $time!")
    $setUserVar($userID;coins;+$random(50,150))
    $sendMessage("🎁 Daily claimed! Balance: $getUserVar($userID;coins)")
)

$run(BOT_TOKEN)
```

### `requirements.txt`
```
nextcord>=2.6.0
```

---

## 🌐 Keep Bot Online 24/7

### Option 1: UptimeRobot (FREE)

1. **Add Keep-Alive Server** - Modify `main.py`:
```python
from replit_keep_alive import keep_alive
keep_alive()  # Add this before running bot
```

2. **Install Flask**:
```bash
pip install flask
```

3. **Setup UptimeRobot**:
   - Daftar di [uptimerobot.com](https://uptimerobot.com)
   - Add Monitor
   - Type: HTTP(s)
   - URL: (your Replit URL)
   - Interval: 5 minutes

### Option 2: Replit Always On (PAID)
Upgrade ke Hacker plan - $7/month

---

## 🧪 Test Bot

Setelah bot online, test commands:

```
!ping          → Check bot status
!hello         → Test basic command
!balance       → Check coins (economy)
!daily         → Claim daily reward
!work          → Work for coins
!help          → Show all commands
```

---

## ❌ Troubleshooting

### "para: command not found"
```bash
pip install -e .
```
atau run manual:
```bash
python -m paracord.cli run bot.cord
```

### "No module named 'nextcord'"
```bash
pip install nextcord
```

### Bot tidak online
1. Check token di Secrets
2. Aktifkan **all intents** di [Discord Developer Portal](https://discord.com/developers/applications)
   - Bot → Privileged Gateway Intents
   - ✅ Message Content Intent
   - ✅ Server Members Intent
   - ✅ Presence Intent

---

## 📚 Full Documentation

- **Complete Guide**: `REPLIT_SETUP.md`
- **User Variables**: `USER_VARIABLES_GUIDE.md`
- **Language Reference**: `QUICKREF_v2.8.md`
- **Example Bot**: `replit_bot_example.cord`

---

## ✅ Success Checklist

- [ ] Replit project created
- [ ] Folder `paracord` uploaded
- [ ] `setup.py` uploaded
- [ ] `main.py` created (from replit_main.py)
- [ ] `bot.cord` created
- [ ] BOT_TOKEN added to Secrets
- [ ] `pip install -e .` completed
- [ ] Bot intents enabled in Discord
- [ ] Click Run button
- [ ] Bot online! 🎉

---

**Happy Botting!** 🚀

Need help? Read `REPLIT_SETUP.md` for detailed guide.
