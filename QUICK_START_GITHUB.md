# 🚀 Quick Start - Upload Paracord v2.8 ke GitHub

## ⚡ 3 Langkah Mudah:

### 1. Ganti README (WAJIB!)

```cmd
del README.md
ren README_GITHUB.md README.md
```

**Kenapa?** README_GITHUB.md dibuat khusus untuk GitHub dengan badges, features, dan installation guide lengkap.

---

### 2. Upload ke GitHub

**Buat Repository Baru di GitHub:**
- Nama: `paracord`
- Description: `Discord bot framework with .cord syntax`
- Public
- **JANGAN** centang "Add README" (kita sudah punya!)

**Upload Files:**

```cmd
git init
git add .
git commit -m "Initial commit - Paracord v2.8"
git remote add origin https://github.com/USERNAME_KAMU/paracord.git
git branch -M main
git push -u origin main
```

**Ganti `USERNAME_KAMU` dengan username GitHub kamu!**

---

### 3. Verify

Cek di GitHub:
- ✅ README.md tampil di homepage repository
- ✅ File structure lengkap (paracord/, paracord-vscode/, docs/)
- ✅ .gitignore bekerja (tidak ada __pycache__, node_modules, dll)

**SELESAI!** 🎉

---

## 📝 Yang Akan User Lakukan (Setelah Clone):

```bash
# Clone
git clone https://github.com/USERNAME_KAMU/paracord.git
cd paracord

# Install
pip install nextcord
pip install -e .

# Test
para --help

# Create bot
echo $bot($prefix("!") $intents("all")) > mybot.cord
echo $addCommand($name("ping") $sendMessage("Pong!")) >> mybot.cord
echo $run("TOKEN") >> mybot.cord

# Run
para run mybot.cord
```

**Bot online!** ✅

---

## 🎨 VSCode Extension (Optional untuk User):

**Method 1: Quick Test (F5)**
1. Buka folder `paracord` di VSCode
2. Press **F5**
3. New window → .cord files colored!

**Method 2: Permanent Install**
```bash
cd paracord-vscode
npm install
npm run compile
xcopy /E /I . "%USERPROFILE%\.vscode\extensions\paracord-2.2.0"
```

Reload VSCode → Done!

---

## ✅ Apa Yang Sudah Siap?

### Core Features:
- ✅ Slash commands
- ✅ User variables (economy system)
- ✅ Cooldowns
- ✅ Buttons, Select Menus, Modals
- ✅ Conditionals (if/else)
- ✅ Embeds
- ✅ Error handling auto ke Discord
- ✅ Clean console output

### Documentation:
- ✅ README_GITHUB.md → Jadi README.md
- ✅ INSTALLATION.md → Installation guide
- ✅ REPLIT_SETUP.md → Deploy ke Replit
- ✅ LICENSE → MIT License

### VSCode Extension:
- ✅ Syntax highlighting (.vscode/settings.json)
- ✅ 50+ hover documentation
- ✅ Autocomplete
- ✅ TypeScript compiled (paracord-vscode/out/)

### Examples:
- ✅ test.cord → Simple test
- ✅ paracord/project-example/ → Full project

---

## ⚠️ Penting!

### JANGAN upload ini ke GitHub:
- ❌ `__pycache__/` (sudah di .gitignore)
- ❌ `node_modules/` (sudah di .gitignore)
- ❌ `uservars.json` (user data)
- ❌ Bot tokens
- ❌ `.env` files

### HARUS upload:
- ✅ `paracord/` (source code)
- ✅ `paracord-vscode/` (VSCode extension)
- ✅ `.vscode/settings.json` (syntax highlighting)
- ✅ `paracord/project-example/` (examples)
- ✅ All documentation (*.md)
- ✅ `setup.py`, `requirements.txt`
- ✅ LICENSE, .gitignore

---

## 🔗 Setelah Upload

### Update Placeholders:
Di documentation, ganti `yourusername` dengan username GitHub kamu:
- `README.md` (line 27)
- `INSTALLATION.md` (line 8)
- `REPLIT_SETUP.md` (line 34)
- `paracord-vscode/package.json` (line 8)

**Atau biarkan users ganti sendiri!**

### Add Topics (GitHub):
Settings → Topics → Add:
- `discord`
- `discord-bot`
- `bot-framework`
- `nextcord`
- `python`
- `discord-py`

---

## 🧪 Test Installation

Setelah upload, test dengan clone fresh:

```bash
# Clone dari GitHub
git clone https://github.com/USERNAME_KAMU/paracord.git
cd paracord

# Install
pip install -e .

# Verify
para --help
```

Harusnya muncul help menu! ✅

---

## 💡 Tips

### Replit Deployment:
Users bisa deploy gratis ke Replit:
1. Import from GitHub → URL repo kamu
2. Add Secret: `BOT_TOKEN`
3. Run → Bot online 24/7!

**Guide lengkap:** `REPLIT_QUICKSTART.md`

### Syntax Highlighting:
Langsung kerja setelah clone! File `.vscode/settings.json` sudah configured.

Users tinggal:
1. Open folder di VSCode
2. Open `.cord` file
3. Colors muncul! 🎨

### Extension (optional):
Untuk hover documentation & autocomplete:
- Press F5 (quick test)
- OR install permanent (guide di `INSTALLATION.md`)

---

## 📊 Stats untuk README Badge (Optional):

Add ke README.md:
```markdown
![GitHub stars](https://img.shields.io/github/stars/USERNAME/paracord)
![GitHub forks](https://img.shields.io/github/forks/USERNAME/paracord)
![GitHub issues](https://img.shields.io/github/issues/USERNAME/paracord)
```

---

## ✅ Final Checklist:

- [ ] README.md replaced dengan README_GITHUB.md
- [ ] Git initialized
- [ ] Repository created di GitHub
- [ ] Files pushed
- [ ] README tampil di GitHub homepage
- [ ] Clone test berhasil
- [ ] Installation guide tested
- [ ] Extension works (F5 test)
- [ ] Topics added di GitHub
- [ ] Repository description updated

**READY TO SHARE!** 🎉

---

**Made with ❤️ by Paracord Team**

**Star ⭐ the repo if you find it useful!**
