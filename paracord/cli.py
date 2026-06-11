import sys, os, glob

from .parser import (
    parse_setup, 
    parse_commands, 
    parse_events, 
    parse_buttons, 
    parse_select_menus, 
    parse_modals
)
from .main import run_bot

def parse(content):
    return {
        "setup": parse_setup(content=content),
        "commands": parse_commands(content=content),
        "events": parse_events(content=content),
        "buttons": parse_buttons(content=content),
        "selects": parse_select_menus(content=content),
        "modals": parse_modals(content=content)
    }

def main():

    if len(sys.argv) < 3:
        print("Usage: para run <file.cord>")
        return

    command = sys.argv[1]
    file = sys.argv[2]

    if command != "run":
        print("Unknown command")
        return

    # Read main bot file
    with open(file, "r", encoding="utf8") as f:
        content = f.read()

    config = parse(content)

    # Auto-load ALL .cord files from main directory and subdirectories
    file_dir = os.path.dirname(os.path.abspath(file))
    main_file_name = os.path.basename(file)
    
    # Find all .cord files in main directory
    all_cord_files = glob.glob(os.path.join(file_dir, "*.cord"))
    
    # Find all .cord files in subdirectories (recursive)
    for root, dirs, files in os.walk(file_dir):
        for filename in files:
            if filename.endswith('.cord'):
                filepath = os.path.join(root, filename)
                if filepath not in all_cord_files:
                    all_cord_files.append(filepath)
    
    # Remove main file from the list
    other_cord_files = [f for f in all_cord_files if os.path.basename(f) != main_file_name]

    # Parse all other .cord files and merge
    for cord_file in other_cord_files:
        try:
            with open(cord_file, "r", encoding="utf8") as f:
                file_content = f.read()
            
            file_config = parse(file_content)
            
            # Merge buttons
            config["buttons"].update(file_config["buttons"])
            # Merge selects
            config["selects"].update(file_config["selects"])
            # Merge modals
            config["modals"].update(file_config["modals"])
            # Merge events (handle list merge properly)
            for event_id, event_data in file_config["events"].items():
                if event_id in config["events"]:
                    # If event already exists, append to list
                    if isinstance(config["events"][event_id], list):
                        if isinstance(event_data, list):
                            config["events"][event_id].extend(event_data)
                        else:
                            config["events"][event_id].append(event_data)
                    else:
                        # Convert to list
                        existing = config["events"][event_id]
                        if isinstance(event_data, list):
                            config["events"][event_id] = [existing] + event_data
                        else:
                            config["events"][event_id] = [existing, event_data]
                else:
                    config["events"][event_id] = event_data
            # Merge commands
            config["commands"].update(file_config["commands"])
        except Exception as e:
            # Silent fail for individual files
            continue

    run_bot(
        config["setup"],
        config["commands"],
        config["events"],
        config["buttons"],
        config["selects"],
        config["modals"]
    )