def replace_variables(template, ctx, custom_value=None, uservar_manager=None):

    if template is None:
        return ""

    result = template

    user = None
    user_id = None

    if hasattr(ctx, "author"):
        user = ctx.author
        user_id = ctx.author.id

    elif hasattr(ctx, "user"):
        user = ctx.user
        user_id = ctx.user.id
    
    # Process $setUserVar and $getUserVar FIRST (before replacing $userID)
    import re
    import random
    
    if uservar_manager and user_id:
        # Process $setUserVar($userID;var_name;value)
        # Manual parsing to handle nested parentheses from $random
        def process_all_setuservars(text):
            while '$setUserVar(' in text:
                start_idx = text.find('$setUserVar(')
                if start_idx == -1:
                    break
                
                # Find matching closing parenthesis
                paren_count = 0
                idx = start_idx + len('$setUserVar')
                end_idx = -1
                
                for i in range(idx, len(text)):
                    if text[i] == '(':
                        paren_count += 1
                    elif text[i] == ')':
                        paren_count -= 1
                        if paren_count == 0:
                            end_idx = i
                            break
                
                if end_idx == -1:
                    break
                
                # Extract content between parentheses
                content = text[start_idx + len('$setUserVar('):end_idx]
                
                # Split by semicolon to get parts
                parts = content.split(';', 2)
                if len(parts) != 3:
                    break
                
                first_part = parts[0].strip()
                var_name = parts[1].strip()
                var_value = parts[2].strip()
                
                # Validate first part is $userID
                if first_part != '$userID':
                    break
                
                # Process $random in value
                def random_replacer(m):
                    min_val = int(m.group(1))
                    max_val = int(m.group(2))
                    return str(random.randint(min_val, max_val))
                
                var_value = re.sub(r'\$random\((-?\d+)\s*,\s*(-?\d+)\)', random_replacer, var_value)
                
                # Process other variables in value ($username, etc)
                if user:
                    var_value = var_value.replace("$username", user.name)
                    var_value = var_value.replace("$mention", user.mention)
                if custom_value is not None:
                    var_value = var_value.replace("$value", str(custom_value))
                
                # Set the variable
                uservar_manager.set_var(user_id, var_name, var_value)
                
                # Remove the $setUserVar call from text
                text = text[:start_idx] + text[end_idx + 1:]
            
            return text
        
        result = process_all_setuservars(result)
        
        # Process $getUserVar($userID;var_name)
        def process_getuservar(match):
            var_name = match.group(1).strip()
            return uservar_manager.get_var(user_id, var_name, "0")
        
        result = re.sub(r'\$getUserVar\(\s*\$userID\s*;\s*([^)]+)\s*\)', process_getuservar, result)

    # Now process regular variables
    if user:

        result = result.replace(
            "$username",
            user.name
        )

        result = result.replace(
            "$mention",
            user.mention
        )

        result = result.replace(
            "$userID",
            str(user.id)
        )

        result = result.replace(
            "$userAvatar",
            str(user.display_avatar.url)
        )

    if hasattr(ctx, "content"):

        parts = ctx.content.split(" ", 1)

        args = (
            parts[1]
            if len(parts) > 1
            else ""
        )

        result = result.replace(
            "$args",
            args
        )

    else:

        result = result.replace(
            "$args",
            ""
        )

    # Replace $value with custom value (from button, select, or modal)
    if custom_value is not None:
        result = result.replace(
            "$value",
            str(custom_value)
        )
    else:
        result = result.replace(
            "$value",
            ""
        )
    
    # Replace $random(min,max)
    def random_replacer(match):
        min_val = int(match.group(1))
        max_val = int(match.group(2))
        return str(random.randint(min_val, max_val))
    
    result = re.sub(r'\$random\((-?\d+)\s*,\s*(-?\d+)\)', random_replacer, result)

    return result