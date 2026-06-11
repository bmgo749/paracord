# 🤖 Paracord v2.8 - Discord Bot Framework

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![Discord](https://img.shields.io/badge/discord-nextcord-7289DA.svg)](https://github.com/nextcord/nextcord)

**Paracord** adalah framework sederhana untuk membuat Discord bot menggunakan syntax `.cord` yang mudah dipahami. Tidak perlu coding Python - cukup tulis dalam file `.cord`!

## ✨ Features

- 🎨 **Syntax Highlighting** - VSCode extension dengan autocomplete
- 💰 **User Variables** - Sistem economy/level dengan persistent storage
- 🎮 **Components** - Buttons, Select Menus, Modals
- ⚡ **Slash Commands** - Support Discord slash commands
- ⏱️ **Cooldowns** - Built-in cooldown system
- 🛡️ **Error Handling** - Auto error reporting ke Discord
- 📝 **Embeds** - Rich embed messages
- 🔀 **Conditionals** - If/else logic untuk interactivity
- ☁️ **Replit Ready** - Deploy online gratis!

## 🚀 Quick Start

### Installation

```bash
# Clone repository
git clone https://github.com/yourusername/paracord.git
cd paracord

# Install dependencies
pip install nextcord

# Install Paracord
pip install -e .
```

### Create Your First Bot

Create `bot.cord`:

```cord
$bot(
    $prefix("!")
    $intents("all")
)

$addCommand(
    $name("ping")
    $sendMessage("🏓 Pong!")
)

$addCommand(
    $name("hello")
    $sendMessage("👋 Hello $username!")
)

$run("YOUR_BOT_TOKEN")
```

### Run Bot

```bash
para run bot.cord
```

**That's it!** 🎉

## 💰 Economy Bot Example

```cord
$bot($prefix("!") $intents("all"))

$addCommand(
    $name("balance")
    $sendMessage("💰 Balance: $getUserVar($userID;coins) coins")
)

$addCommand(
    $name("daily")
    $cooldown("24h;⏰ Come back in $time!")
    $setUserVar($userID;coins;+$random(50,150))
    $sendMessage("🎁 Daily claimed! Balance: $getUserVar($userID;coins)")
)

$addCommand(
    $name("work")
    $cooldown("1h;⏰ Rest for $time!")
    $setUserVar($userID;coins;+$random(20,80))
    $sendMessage("💼 Worked! Balance: $getUserVar($userID;coins)")
)

$run("YOUR_BOT_TOKEN")
```

## 🎨 VSCode Extension

Get syntax highlighting & autocomplete!

### Install Extension

**Method 1: Press F5 (Quick Test)**
1. Open this folder in VSCode
2. Press F5
3. New window opens with extension active
4. Open `.cord` files → See colors!

**Method 2: Permanent Install**
```bash
cd paracord-vscode
npm install
npm run compile
# Copy folder to %USERPROFILE%\.vscode\extensions\paracord-2.2.0
```

**Full guide**: [INSTALL_EXTENSION_NOW.md](INSTALL_EXTENSION_NOW.md)

## ☁️ Deploy to Replit

Deploy your bot online for free!

1. **Fork this repo** or upload files to Replit
2. **Add Secret**: `BOT_TOKEN` = your Discord bot token
3. **Run**: Click the Run button
4. **Done!** Bot is online 24/7 ☁️

**Full guide**: [REPLIT_QUICKSTART.md](REPLIT_QUICKSTART.md)

## 📚 Documentation

### Quick Start
- **[START_HERE.md](START_HERE.md)** - Get started in 2 minutes
- **[QUICKREF_v2.8.md](QUICKREF_v2.8.md)** - Complete language reference
- **[INDEX.md](INDEX.md)** - Complete documentation index

### Features
- **[USER_VARIABLES_GUIDE.md](USER_VARIABLES_GUIDE.md)** - Economy/level systems
- **[ERROR_HANDLING.md](ERROR_HANDLING.md)** - Error system
- **[REPLIT_SETUP.md](REPLIT_SETUP.md)** - Deploy to Replit

### Examples
- **[replit_bot_example.cord](replit_bot_example.cord)** - Complete bot
- **[paracord/uservars-example.cord](paracord/uservars-example.cord)** - Economy bot
- **[test.cord](test.cord)** - Simple test

## 🎯 User Variables (v2.8)

Store data per user!

```cord
// Set variables
$setUserVar($userID;coins;100)        // Direct
$setUserVar($userID;coins;+50)        // Add
$setUserVar($userID;coins;-30)        // Subtract
$setUserVar($userID;coins;*2)         // Multiply
$setUserVar($userID;coins;/2)         // Divide
$setUserVar($userID;coins;+$random(10,100))  // Random

// Get variables
Balance: $getUserVar($userID;coins) coins
```

**Features**:
- ✅ Math operations (+, -, *, /)
- ✅ Random values
- ✅ String storage
- ✅ Persistent (JSON file)
- ✅ Multi-user support

## 🎮 Components

### Buttons
```cord
$newButton(
    $addButton("btn_yes;✅ Yes;success;yes;✅")
    $id("handleChoice")
)

$addCommand(
    $name("choose")
    $sendMessage("Pick one:")
    $useButton("btn_yes")
)

$event(
    $id("handleChoice")
    $if[$value==("yes")]
        $sendMessage("You chose yes!")
    $endif
)
```

### Select Menus
```cord
$newSelectMenu(
    $id("menu_role")
    $placeholder("Choose role")
    $addSelectMenuOption("opt1;Admin;admin")
    $addSelectMenuOption("opt2;Member;member")
)
```

### Modals
```cord
$newModal(
    $id("form_feedback")
    $title("Feedback")
    $addTextInput("input1;Your message;10;500;Type here")
)
```

## 🛡️ Error Handling

Errors automatically sent to Discord!

```cord
$bot(
    $prefix("!")
    $intents("all")
    $errorChannel("1234567890")  // Optional error log channel
)
```

**Features**:
- ✅ Auto error reporting
- ✅ Clean console output
- ✅ User-friendly messages
- ✅ Stack traces for debugging

## 📊 Examples

### Simple Bot
```cord
$bot($prefix("!") $intents("all"))
$addCommand($name("ping") $sendMessage("Pong!"))
$run("TOKEN")
```

### Bot with Embed
```cord
$embed(
    $embedName("welcome")
    $title("Welcome!")
    $description("Hello $username!")
    $color("#5865F2")
)

$addCommand($name("info") $sendMessage("welcome"))
```

### Bot with Cooldown
```cord
$addCommand(
    $name("daily")
    $cooldown("24h;Wait $time!")
    $sendMessage("Daily reward!")
)
```

## 🔧 Requirements

- Python 3.8+
- nextcord library
- Discord bot token

## 📝 License

MIT License - see [LICENSE](LICENSE) file

## 🤝 Contributing

Contributions welcome! Feel free to:
- Report bugs
- Suggest features
- Submit pull requests

## 📞 Support

- **Documentation**: [INDEX.md](INDEX.md)
- **Examples**: [paracord/project-example/](paracord/project-example/)
- **Issues**: GitHub Issues

## 🎉 Credits

Built with:
- [nextcord](https://github.com/nextcord/nextcord) - Discord API wrapper
- [Python](https://python.org) - Programming language

---

**Made with ❤️ by Paracord Team**

**Star ⭐ this repo if you find it useful!**
