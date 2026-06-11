#!/usr/bin/env python3
"""
Paracord Bot - Replit Entry Point
Automatically loads bot from .cord file with environment variables
"""

import os
import sys
import subprocess

print("=" * 60)
print("🚀 PARACORD BOT - REPLIT")
print("=" * 60)

# Check if bot token exists
bot_token = os.environ.get('BOT_TOKEN')

if not bot_token:
    print("\n❌ ERROR: BOT_TOKEN tidak ditemukan!")
    print("\n📝 Cara fix:")
    print("1. Klik icon 🔒 Secrets di sidebar kiri")
    print("2. Klik '+ New Secret'")
    print("3. Key: BOT_TOKEN")
    print("4. Value: (paste Discord bot token kamu)")
    print("5. Klik 'Add Secret'")
    print("6. Restart Repl\n")
    sys.exit(1)

print("✅ BOT_TOKEN found")

# Check if bot.cord exists
if not os.path.exists('bot.cord'):
    print("\n❌ ERROR: bot.cord tidak ditemukan!")
    print("\n📝 Cara fix:")
    print("1. Buat file 'bot.cord' di root folder")
    print("2. Isi dengan kode bot Paracord kamu")
    print("3. Di bagian $run(), pakai: $run(BOT_TOKEN)")
    print("4. Restart Repl\n")
    sys.exit(1)

print("✅ bot.cord found")

# Read bot.cord file
try:
    with open('bot.cord', 'r', encoding='utf-8') as f:
        cord_content = f.read()
    print("✅ bot.cord loaded")
except Exception as e:
    print(f"\n❌ ERROR reading bot.cord: {e}\n")
    sys.exit(1)

# Replace BOT_TOKEN placeholder with actual token
cord_content = cord_content.replace('BOT_TOKEN', bot_token)

# Save to temporary runtime file
try:
    with open('bot_runtime.cord', 'w', encoding='utf-8') as f:
        f.write(cord_content)
    print("✅ Runtime file created")
except Exception as e:
    print(f"\n❌ ERROR creating runtime file: {e}\n")
    sys.exit(1)

# Check if paracord is installed
try:
    import paracord
    print("✅ Paracord package installed")
except ImportError:
    print("\n❌ ERROR: Paracord tidak terinstall!")
    print("\n📝 Cara fix:")
    print("1. Di Shell, jalankan: pip install -e .")
    print("2. Restart Repl\n")
    sys.exit(1)

# Check if nextcord is installed
try:
    import nextcord
    print("✅ Nextcord installed")
except ImportError:
    print("\n⚠️  WARNING: Nextcord belum terinstall!")
    print("📦 Installing nextcord...")
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'nextcord'], check=True)
        print("✅ Nextcord installed successfully")
    except:
        print("\n❌ ERROR: Gagal install nextcord!")
        print("\n📝 Manual install:")
        print("Di Shell, jalankan: pip install nextcord\n")
        sys.exit(1)

print("\n" + "=" * 60)
print("🚀 STARTING BOT...")
print("=" * 60)
print()

# Run the bot
try:
    subprocess.run(['para', 'run', 'bot_runtime.cord'])
except FileNotFoundError:
    # If 'para' command not found, run directly
    print("⚠️  'para' command tidak ditemukan, running directly...")
    subprocess.run([sys.executable, '-m', 'paracord.cli', 'run', 'bot_runtime.cord'])
except KeyboardInterrupt:
    print("\n\n🛑 Bot stopped by user")
except Exception as e:
    print(f"\n❌ ERROR: {e}")
    sys.exit(1)
