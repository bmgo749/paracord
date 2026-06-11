# 🎮 Paracord v2.8 - Example Project

Complete example demonstrating all Paracord v2.8 features.

## 🚀 Quick Start

1. **Edit token in `setup-v2.8.cord`:**
   ```cord
   $run("YOUR_BOT_TOKEN_HERE")
   ```

2. **Run bot:**
   ```bash
   para run setup-v2.8.cord
   ```

3. **Test commands:**
   ```
   !ping
   !quiz
   !report
   /greet name:"John"
   /mathquiz answer:"25"
   ```

## 📁 Files

- **`setup-v2.8.cord`** - Bot configuration (START HERE)
- **`commands-v2.8.cord`** - Regular commands (!ping, !quiz, etc.)
- **`slash-v2.8.cord`** - Slash commands (/greet, /quiz, etc.)
- **`components-v2.8.cord`** - Buttons, select menus, modals
- **`events-v2.8.cord`** - Event handlers with conditionals

## 🎯 Features Demonstrated

- ✅ Regular commands with cooldowns
- ✅ Slash commands with options (input/choice)
- ✅ Buttons with values
- ✅ Select menus
- ✅ Modals (report, feedback)
- ✅ Conditionals ($if/$elseif/$endif)
- ✅ $random function
- ✅ $value variable
- ✅ Multiple events

## 💬 Available Commands

### Regular Commands
- `!ping` - Simple ping
- `!daily` - Daily reward (24h cooldown, random coins)
- `!roll` - Roll dice (5s cooldown)
- `!quiz` - Math quiz with buttons
- `!report` - Report user (opens modal)
- `!feedback` - Send feedback (opens modal)
- `!colortest` - Color picker (select menu)
- `!confirm` - Yes/No confirmation

### Slash Commands
- `/greet name:"John"` - Greet someone
- `/gender gender:"Male"` - Select gender (choice)
- `/dailyslash` - Daily reward (10s cooldown)
- `/mathquiz answer:"25"` - Math quiz (15s cooldown)
- `/register` - Register with 3 options
- `/color color:"Red"` - Pick color

## 📚 Documentation

See [`../../QUICKREF_v2.8.md`](../../QUICKREF_v2.8.md) for syntax reference.

---

**Paracord v2.8** - Making Discord bots simple! 🚀
