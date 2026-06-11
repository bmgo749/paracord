import re

import re

def parse_setup(content):

    prefix = re.search(r'\$prefix\("(.+?)"\)', content)
    intents = re.search(r'\$intents\("(.+?)"\)', content)
    token = re.search(r'\$run\("(.+?)"\)', content)
    status = re.search(
        r'\$status\("(.+?)"\)',
        content
    )
    activity = re.search(
        r'\$activity\(\s*(.+?)\s*;\s*"(.*?)"\s*\)',
        content,
        re.S
    )

    return {
        "prefix": prefix.group(1) if prefix else "!",
        "intents": intents.group(1) if intents else "all",
        "token": token.group(1) if token else None,

        "status":
            status.group(1)
            if status else "online",

        "activity_type":
            activity.group(1)
            if activity else None,

        "activity_name":
            activity.group(2)
            if activity else None
    }

def parse_events(content):

    events = {}

    blocks = extract_blocks(
        content,
        "event"
    )

    for block in blocks:

        event_id = re.search(
            r'\$id\("(.*?)"\)',
            block
        )

        text_content = None
        
        # Check if there's $sendModal
        send_modal = re.search(
            r'\$sendModal\("(.*?)"\)',
            block
        )
        
        # Remove $id and $sendModal from block to get text content
        block_clean = block
        
        # Remove $id
        block_clean = re.sub(r'\$id\(".*?"\)', '', block_clean, count=1)
        
        # Remove $sendModal if present
        if send_modal:
            block_clean = re.sub(r'\$sendModal\(".*?"\)', '', block_clean)
        
        # Clean up whitespace
        text_content = block_clean.strip()
        
        # If text contains ONLY $sendMessage with quoted content, extract it
        sendmsg_only = re.match(r'^\$sendMessage\("(.*?)"\)$', text_content, re.S)
        if sendmsg_only:
            text_content = sendmsg_only.group(1)

        if event_id:
            event_key = event_id.group(1)
            
            # Support multiple events with same ID - store as list
            if event_key not in events:
                events[event_key] = []
            
            events[event_key].append({
                "text": text_content if text_content else None,
                "sendModal": send_modal.group(1) if send_modal else None
            })

    return events

def parse_select_menus(content):

    select_blocks = extract_blocks(
        content,
        "newSelectMenu"
    )

    selects = {}

    for sb in select_blocks:

        custom_id = re.search(
            r'\$id\("(.*?)"\)',
            sb
        )

        placeholder = re.search(
            r'\$placeholder\("(.*?)"\)',
            sb
        )

        # Only $addSelectMenuOption format (id;label;value)
        options_raw = re.findall(
            r'\$addSelectMenuOption\("(.*?)"\)',
            sb
        )

        options = []

        for opt in options_raw:
            parts = opt.split(";")
            
            if len(parts) >= 3:
                # Format: id;label;value
                options.append({
                    "id": parts[0].strip(),
                    "label": parts[1].strip(),
                    "value": parts[2].strip()
                })

        if custom_id and options:
            selects[custom_id.group(1)] = {
                "placeholder": placeholder.group(1) if placeholder else "Select an option",
                "id": custom_id.group(1),
                "options": options
            }

    return selects

def parse_modals(content):

    modal_blocks = extract_blocks(
        content,
        "newModal"
    )

    modals = {}

    for mb in modal_blocks:

        custom_id = re.search(
            r'\$id\("(.*?)"\)',
            mb
        )

        title = re.search(
            r'\$title\("(.*?)"\)',
            mb
        )

        inputs = []

        # Only $addTextInput format: id;label;min;max;placeholder
        raw_inputs = re.findall(
            r'\$addTextInput\("(.*?)"\)',
            mb
        )

        for inp in raw_inputs:
            p = inp.split(";")

            if len(p) >= 4:
                inputs.append({
                    "id": p[0].strip(),
                    "label": p[1].strip(),
                    "min": int(p[2].strip()),
                    "max": int(p[3].strip()),
                    "placeholder": p[4].strip() if len(p) > 4 else ""
                })

        if custom_id and inputs:
            modals[custom_id.group(1)] = {
                "title": title.group(1) if title else "Modal",
                "id": custom_id.group(1),
                "inputs": inputs
            }

    return modals

def parse_buttons(content):

    button_blocks = extract_blocks(
        content,
        "newButton"
    )

    buttons = {}

    for bb in button_blocks:

        # Only $addButton format is supported now
        # Format: id;label;style;value;emoji
        add_button = re.search(
            r'\$addButton\("(.*?)"\)',
            bb
        )

        if not add_button:
            continue  # Skip if no $addButton found

        parts = add_button.group(1).split(";")
        
        if len(parts) < 3:  # Need at least id, label, style
            continue
        
        button_id = parts[0].strip()
        label = parts[1].strip() if len(parts) > 1 else "Button"
        style = parts[2].strip() if len(parts) > 2 else "primary"
        value = parts[3].strip() if len(parts) > 3 and parts[3].strip() else None
        emoji = parts[4].strip() if len(parts) > 4 and parts[4].strip() else None

        # Find event ID - now also uses $id (second occurrence)
        # First $id is in $addButton, second $id is event ID
        event_ids = re.findall(r'\$id\("(.*?)"\)', bb)
        event = event_ids[0] if len(event_ids) > 0 else None

        if button_id:
            buttons[button_id] = {
                "id": button_id,
                "label": label,
                "style": style,
                "emoji": emoji,
                "event": event,
                "value": value
            }

    return buttons

def get_event(
    event_id,
    events
):
    return events.get(event_id)

def parse_embed(block):

    def get(p):
        m = re.search(p, block)
        return m.group(1) if m else None

    embed = {
        "name": get(r'\$embedName\("(.*?)"\)'),
        "title": get(r'\$title\("(.*?)"\)'),
        "description": get(r'\$description\("([\s\S]*?)"\)'),
        "color": get(r'\$color\("(.*?)"\)'),
        "footer": get(r'\$footer\("(.*?)"\)'),
        "thumbnail": get(r'\$thumbnail\("(.*?)"\)'),
        "image": get(r'\$image\("(.*?)"\)'),
        "timestamp": "$timestamp" in block,
        "fields": [],
        "useButtons": [],
        "useSelects": []
    }

    fields = re.findall(r'\$addField\("(.*?)"\)', block)

    for f in fields:
        parts = f.split(";")
        if len(parts) == 3:
            embed["fields"].append({
                "name": parts[0],
                "value": parts[1],
                "inline": parts[2].lower() == "true"
            })

    # Parse $useButton inside embed
    use_buttons = re.findall(
        r'\$useButton\("(.*?)"\)',
        block
    )
    embed["useButtons"] = use_buttons

    # Parse $useSelectMenu inside embed
    use_selects = re.findall(
        r'\$useSelectMenu\("(.*?)"\)',
        block
    )
    embed["useSelects"] = use_selects

    return embed

def extract_blocks(content, keyword):

    blocks = []

    start = 0

    while True:

        pos = content.find(f"${keyword}(", start)

        if pos == -1:
            break

        i = pos + len(f"${keyword}(")

        depth = 1

        while i < len(content) and depth > 0:

            if content[i] == "(":
                depth += 1

            elif content[i] == ")":
                depth -= 1

            i += 1

        blocks.append(
            content[
                pos + len(f"${keyword}("):
                i - 1
            ]
        )

        start = i

    return blocks

def parse_commands(content):

    commands = {}

    # Parse regular commands ($addCommand)
    blocks = extract_blocks(
        content,
        "addCommand"
    )

    for block in blocks:

        name = re.search(r'\$name\("(.*?)"\)', block)
        embed_send = re.search(
            r'\$sendMessage\(\$(.*?)\)',
            block
        )
        text_send = re.search(
            r'\$sendMessage\("(.*?)"\)',
            block,
            re.S
            )

        embeds = {}

        embed_blocks = extract_blocks(
            block,
            "embed"
        )

        # Parse $useButton("id")
        use_buttons = re.findall(
            r'\$useButton\("(.*?)"\)',
            block
        )

        # Parse $useSelectMenu("id")
        use_selects = re.findall(
            r'\$useSelectMenu\("(.*?)"\)',
            block
        )

        # Parse $sendModal("id")
        send_modal = re.search(
            r'\$sendModal\("(.*?)"\)',
            block
        )
        
        # Parse $cooldown("time;message")
        cooldown = re.search(
            r'\$cooldown\("(.*?)"\)',
            block
        )
        
        cooldown_data = None
        if cooldown:
            parts = cooldown.group(1).split(";", 1)
            cooldown_data = {
                "time": parts[0].strip(),
                "message": parts[1].strip() if len(parts) > 1 else "Please wait before using this command again."
            }

        for eb in embed_blocks:

            embed = parse_embed(eb)

            if embed.get("name"):
                embeds[embed["name"]] = embed

        if name:
            commands[name.group(1).lower()] = {

                "text":
                    text_send.group(1)
                    if text_send else None,

                "sendEmbed":
                    embed_send.group(1)
                    if embed_send else None,

                "embeds":
                    embeds,
                
                "useButtons":
                    use_buttons,
                
                "useSelects":
                    use_selects,

                "sendModal":
                    send_modal.group(1) if send_modal else None,
                
                "cooldown":
                    cooldown_data,
                
                "type": "regular"
            }

    # Parse slash commands ($addSlashCommand)
    slash_blocks = extract_blocks(
        content,
        "addSlashCommand"
    )
    
    for block in slash_blocks:
        name = re.search(r'\$name\("(.*?)"\)', block)
        description = re.search(r'\$description\("(.*?)"\)', block)
        emoji = re.search(r'\$emoji\("(.*?)"\)', block)
        
        # Parse options: name;description;type;choices_or_value;required
        # type: "input" = user input, "choice" = predefined choices
        # choices_or_value: 
        #   - for "input": custom value when submitted
        #   - for "choice": "choice1|choice2|choice3" (choices separated by |)
        options_raw = re.findall(
            r'\$slashCommandOption\("(.*?)"\)',
            block
        )
        
        options = []
        for opt in options_raw:
            parts = opt.split(";")
            if len(parts) >= 2:
                opt_name = parts[0].strip()
                opt_desc = parts[1].strip() if len(parts) > 1 else "Option"
                opt_type = parts[2].strip().lower() if len(parts) > 2 and parts[2].strip() else "input"
                opt_data = parts[3].strip() if len(parts) > 3 and parts[3].strip() else None
                opt_required = parts[4].strip().lower() == "true" if len(parts) > 4 else False
                
                option = {
                    "name": opt_name,
                    "description": opt_desc,
                    "type": opt_type,
                    "required": opt_required
                }
                
                if opt_type == "choice" and opt_data:
                    # Parse choices: "male|female|other"
                    option["choices"] = [c.strip() for c in opt_data.split("|") if c.strip()]
                elif opt_type == "input" and opt_data:
                    # Custom value for input type
                    option["value"] = opt_data
                
                options.append(option)
        
        # Get response text (everything after options)
        block_clean = block
        # Remove all option declarations
        for opt_match in re.finditer(r'\$slashCommandOption\(".*?"\)', block):
            block_clean = block_clean.replace(opt_match.group(0), '')
        # Remove name, description, emoji
        block_clean = re.sub(r'\$name\(".*?"\)', '', block_clean)
        block_clean = re.sub(r'\$description\(".*?"\)', '', block_clean)
        block_clean = re.sub(r'\$emoji\(".*?"\)', '', block_clean)
        block_clean = re.sub(r'\$cooldown\(".*?"\)', '', block_clean)
        
        response_text = block_clean.strip()
        
        # Extract from $sendMessage if present
        sendmsg_match = re.match(r'^\$sendMessage\("(.*?)"\)$', response_text, re.S)
        if sendmsg_match:
            response_text = sendmsg_match.group(1)
        
        # Parse cooldown
        cooldown = re.search(
            r'\$cooldown\("(.*?)"\)',
            block
        )
        
        cooldown_data = None
        if cooldown:
            parts = cooldown.group(1).split(";", 1)
            cooldown_data = {
                "time": parts[0].strip(),
                "message": parts[1].strip() if len(parts) > 1 else "Please wait before using this command again."
            }
        
        if name:
            commands[name.group(1).lower()] = {
                "name": name.group(1),
                "description": description.group(1) if description else "Slash command",
                "emoji": emoji.group(1) if emoji else None,
                "options": options,
                "response": response_text,
                "cooldown": cooldown_data,
                "type": "slash"
            }

    return commands


def parse_run(content):
    run = re.search(r'\$run\("(.+?)"\)', content)
    return run.group(1) if run else None


def evaluate_conditionals(text, button_value):
    """
    Evaluate conditional blocks in text based on button value
    Supports $if, $elseif, $endif
    Format: $if[$value==("test")] ... $elseif[$value==("other")] ... $endif
    """
    if not text:
        return text
    
    # Find all conditional blocks
    # Pattern: $if[condition] content $elseif[condition] content $endif
    result = []
    i = 0
    
    while i < len(text):
        # Look for $if
        if_pos = text.find('$if[', i)
        
        if if_pos == -1:
            # No more conditionals, add rest of text
            result.append(text[i:])
            break
        
        # Add text before $if
        result.append(text[i:if_pos])
        
        # Find matching $endif
        endif_pos = text.find('$endif', if_pos)
        if endif_pos == -1:
            # No matching $endif, treat as regular text
            result.append(text[if_pos:])
            break
        
        # Extract the full conditional block
        block = text[if_pos:endif_pos + len('$endif')]
        
        # Process the conditional block
        processed = process_conditional_block(block, button_value)
        result.append(processed)
        
        i = endif_pos + len('$endif')
    
    return ''.join(result)


def process_conditional_block(block, button_value):
    """
    Process a single conditional block
    Returns the content of the first matching condition
    """
    # Split by $elseif to get all conditions
    parts = re.split(r'(\$if\[|\$elseif\[)', block)
    
    conditions = []
    current_condition = None
    
    for part in parts:
        if not part:
            continue
            
        if part == '$if[' or part == '$elseif[':
            current_condition = {'type': part.strip('$[')}
            continue
        
        if current_condition is not None:
            # Extract condition and content
            # Format: $value==("test")] content
            match = re.match(r'\$value==\("([^"]*)"\)\](.*?)(?=\$elseif\[|\$endif|$)', part, re.S)
            if match:
                expected_value = match.group(1)
                content = match.group(2).strip()
                
                # Extract text from $sendMessage if present
                sendmsg_match = re.search(r'\$sendMessage\("(.*?)"\)', content, re.S)
                if sendmsg_match:
                    content = sendmsg_match.group(1)
                
                current_condition['value'] = expected_value
                current_condition['content'] = content
                conditions.append(current_condition)
                current_condition = None
    
    # Evaluate conditions
    for cond in conditions:
        if cond['value'] == button_value:
            return cond['content']
    
    # No condition matched, return empty
    return ''