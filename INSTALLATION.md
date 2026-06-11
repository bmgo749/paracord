# 📦 Paracord Installation Guide

## 🚀 For Users (Clone from GitHub)

### Step 1: Clone Repository

```bash
git clone https://github.com/yourusername/paracord.git
cd paracord
```

### Step 2: Install Dependencies

```bash
# Install nextcord
pip install nextcord

# Or use requirements.txt
pip install -r requirements.txt
```

### Step 3: Install Paracord

```bash
# Install as package
pip install -e .
```

This installs the `para` command globally.

### Step 4: Verify Installation

```bash
para --help
```

Should show Paracord help menu.

### Step 5: Get Discord Bot Token

1. Go to [Discord Developer Portal](https://discord.com/developers/applications)
2. Create New Application
3. Go to "Bot" section
4. Click "Reset Token" → Copy token
5. Enable all **Privileged Gateway Intents**:
   - ✅ Presence Intent
   - ✅ Server Members Intent
   - ✅ Message Content Intent

### Step 6: Create Your Bot

Create `mybot.cord`:

```cord
$bot(
    $prefix("!")
    $intents("all")
)

$addCommand(
    $name("ping")
    $sendMessage("Pong!")
)

$run("YOUR_BOT_TOKEN_HERE")
```

### Step 7: Run Bot

```bash
para run mybot.cord
```

**Output**:
```
✅ Logged in as YourBot#1234
```

### Step 8: Test Bot

In Discord, type: `!ping`

Bot responds: `Pong!`

**Success!** 🎉

---

## 🎨 Install VSCode Extension (Optional)

Get syntax highlighting & autocomplete!

### Method 1: Press F5 (Quick)

1. Open `paracord` folder in VSCode
2. Press **F5** (Run & Debug)
3. New window opens
4. Open `.cord` files → Colors working!

### Method 2: Install Permanent

**Windows:**
```bash
cd paracord-vscode
npm install
npm run compile

# Copy to extensions folder
xcopy /E /I . "%USERPROFILE%\.vscode\extensions\paracord-2.2.0"
```

**Mac/Linux:**
```bash
cd paracord-vscode
npm install
npm run compile

# Copy to extensions folder
cp -r . ~/.vscode/extensions/paracord-2.2.0
```

Then reload VSCode: `Ctrl+Shift+P` → "Reload Window"

**Full guide**: [INSTALL_EXTENSION_NOW.md](INSTALL_EXTENSION_NOW.md)

---

## ☁️ Deploy to Replit (Optional)

### Step 1: Upload to Replit

1. Go to [Replit.com](https://replit.com)
2. Create New Repl → Python
3. Upload all files from `paracord` folder

**Or fork from GitHub:**
- Import from GitHub → Your repo URL

### Step 2: Add Bot Token

1. Click **🔒 Secrets** (lock icon)
2. Add Secret:
   - Key: `BOT_TOKEN`
   - Value: Your Discord bot token

### Step 3: Setup Files

Rename `replit_main.py` to `main.py`

Or create `main.py`:
```python
import os
import subprocess

bot_token = os.environ.get('BOT_TOKEN')
if not bot_token:
    print("❌ Add BOT_TOKEN to Secrets!")
    exit(1)

# Replace token in bot file
with open('bot.cord', 'r') as f:
    content = f.read().replace('BOT_TOKEN', bot_token)

with open('bot_runtime.cord', 'w') as f:
    f.write(content)

subprocess.run(['para', 'run', 'bot_runtime.cord'])
```

Update `bot.cord`:
```cord
$run(BOT_TOKEN)  // No quotes - will be replaced
```

### Step 4: Run Bot

Click **▶️ Run** button

Bot online! ☁️

**Full guide**: [REPLIT_SETUP.md](REPLIT_SETUP.md)

---

## 🧪 Test Installation

### Test 1: Command Available

```bash
para --help
```

Should show help menu.

### Test 2: Run Example

```bash
para run test.cord
```

Should start bot (with valid token).

### Test 3: Python Import

```bash
python -c "import paracord; print('OK')"
```

Should print `OK`.

---

## ❌ Troubleshooting

### `para: command not found`

**Solution 1**: Reinstall
```bash
pip install -e .
```

**Solution 2**: Run directly
```bash
python -m paracord.cli run bot.cord
```

### `No module named 'nextcord'`

**Solution**:
```bash
pip install nextcord
```

### `Permission denied`

**Windows**: Run as Administrator

**Mac/Linux**: Use `sudo`
```bash
sudo pip install -e .
```

### Bot not responding

**Check**:
1. Bot token correct?
2. Intents enabled in Developer Portal?
3. Bot invited to server with permissions?
4. Prefix correct? (default: `!`)

---

## 📋 Requirements

- **Python**: 3.8 or higher
- **pip**: Latest version
- **nextcord**: 2.0.0 or higher
- **Discord bot token**: From Developer Portal

### Optional:
- **Node.js**: For VSCode extension development
- **VSCode**: For syntax highlighting
- **Replit**: For cloud hosting

---

## 🔄 Updating

```bash
# Pull latest changes
git pull origin main

# Reinstall
pip install -e . --upgrade
```

---

## 🆘 Getting Help

1. **Check documentation**: [INDEX.md](INDEX.md)
2. **Read examples**: [paracord/project-example/](paracord/project-example/)
3. **Quick reference**: [QUICKREF_v2.8.md](QUICKREF_v2.8.md)
4. **GitHub Issues**: Report bugs

---

## ✅ Installation Checklist

- [ ] Repository cloned
- [ ] Dependencies installed (`pip install nextcord`)
- [ ] Paracord installed (`pip install -e .`)
- [ ] Command works (`para --help`)
- [ ] Bot token obtained
- [ ] Intents enabled in Discord
- [ ] Test bot created
- [ ] Bot runs successfully
- [ ] Bot responds in Discord
- [ ] Ready to build! 🎉

---

## 🎓 Next Steps

1. **Learn syntax**: [QUICKREF_v2.8.md](QUICKREF_v2.8.md)
2. **Try examples**: [replit_bot_example.cord](replit_bot_example.cord)
3. **Build economy**: [USER_VARIABLES_GUIDE.md](USER_VARIABLES_GUIDE.md)
4. **Deploy online**: [REPLIT_SETUP.md](REPLIT_SETUP.md)

**Happy botting!** 🚀
