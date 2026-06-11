import nextcord
from nextcord.ext import commands
from nextcord import SlashOption
from .runtime import replace_variables
from .buttons import ParaButton
from .selects import ParaSelectMenu
from .modals import ParaModal
from .cooldowns import CooldownManager
from .uservars import UserVarManager
from .parser import evaluate_conditionals

def run_bot(setup, commands_data, events, buttons_data, selects_data, modals_data):

    prefix = setup["prefix"]
    token = setup["token"]

    intents = nextcord.Intents.all()

    bot = commands.Bot(
        command_prefix=prefix,
        intents=intents
    )
    
    # Initialize cooldown manager
    cooldown_manager = CooldownManager()
    
    # Initialize user variable manager
    uservar_manager = UserVarManager()
    
    # Error channel for logging (optional - set via $errorChannel in setup)
    error_channel_id = setup.get("error_channel")
    
    # Register slash commands
    for cmd_name, cmd_data in commands_data.items():
        if cmd_data.get("type") == "slash":
            register_slash_command(bot, cmd_name, cmd_data, cooldown_manager, events, uservar_manager)

    @bot.event
    async def on_ready():
        print(f"✅ Logged in as {bot.user}")

        activity = None

        activity_type = setup.get(
            "activity_type"
        )

        activity_name = setup.get(
            "activity_name"
        )

        if activity_type and activity_name:

            activity_type = activity_type.lower()

            if activity_type == "playing":
                activity = nextcord.Game(
                    name=activity_name
                )

            elif activity_type == "watching":
                activity = nextcord.Activity(
                    type=nextcord.ActivityType.watching,
                    name=activity_name
                )

            elif activity_type == "listening":
                activity = nextcord.Activity(
                    type=nextcord.ActivityType.listening,
                    name=activity_name
                )

            elif activity_type == "streaming":
                activity = nextcord.Streaming(
                    name=activity_name,
                    url="https://twitch.tv/paracord"
                )

            elif activity_type == "competing":
                activity = nextcord.Activity(
                    type=nextcord.ActivityType.competing,
                    name=activity_name
                )

        status_map = {

            "online":
                nextcord.Status.online,

            "idle":
                nextcord.Status.idle,

            "dnd":
                nextcord.Status.dnd,

            "offline":
                nextcord.Status.invisible
        }

        await bot.change_presence(

            status=status_map.get(
                setup.get("status", "online"),
                nextcord.Status.online
            ),

            activity=activity
        )
    
    @bot.event
    async def on_command_error(ctx, error):
        """Send errors to Discord channel"""
        error_msg = f"❌ **Error in command `{ctx.command}`:**\n```\n{str(error)}\n```"
        
        # Try to send to error channel if configured
        if error_channel_id:
            try:
                channel = bot.get_channel(int(error_channel_id))
                if channel:
                    await channel.send(error_msg)
                else:
                    # Fallback to command channel
                    await ctx.send(error_msg)
            except:
                # Fallback to command channel
                await ctx.send(error_msg)
        else:
            # Send to command channel
            await ctx.send(error_msg)
    
    @bot.event
    async def on_application_command_error(interaction: nextcord.Interaction, error):
        """Send slash command errors to Discord"""
        error_msg = f"❌ **Error in slash command:**\n```\n{str(error)}\n```"
        
        # Try to respond to interaction
        try:
            if interaction.response.is_done():
                await interaction.followup.send(error_msg, ephemeral=True)
            else:
                await interaction.response.send_message(error_msg, ephemeral=True)
        except:
            pass
        
        # Also log to error channel if configured
        if error_channel_id:
            try:
                channel = bot.get_channel(int(error_channel_id))
                if channel:
                    await channel.send(f"{error_msg}\nUser: {interaction.user.mention}\nCommand: {interaction.application_command.name}")
            except:
                pass

    # Interaction handling is now done in the View/Modal classes themselves
    # No need for a global on_interaction handler

    @bot.event
    async def on_message(message):

        if message.author.bot:
            return

        content = message.content.strip()

        if not content.startswith(prefix):
            return

        parts = content[len(prefix):].strip().split(" ", 1)
        cmd = parts[0].strip().lower()

        if cmd in commands_data:

            data = commands_data[cmd]
            
            # Skip if this is a slash command
            if data.get("type") == "slash":
                return
            
            # Check cooldown for regular commands
            if data.get("cooldown"):
                cooldown_data = data["cooldown"]
                cooldown_seconds = cooldown_manager.parse_time(cooldown_data["time"])
                on_cooldown, remaining = cooldown_manager.check_cooldown(cmd, message.author.id, cooldown_seconds)
                
                if on_cooldown:
                    cooldown_msg = cooldown_data["message"].replace(
                        "$time", cooldown_manager.format_time(remaining)
                    )
                    await message.channel.send(cooldown_msg)
                    return
                
                # Set cooldown
                cooldown_manager.set_cooldown(cmd, message.author.id)

            data = commands_data[cmd]

            embed_name = data.get("sendEmbed")

            # Build view with buttons and select menus
            view = None
            has_components = False

            # Collect all buttons (from command and from embeds)
            all_buttons = list(data.get("useButtons", []))
            
            # Check for buttons in embeds
            if embed_name and embed_name in data["embeds"]:
                e = data["embeds"][embed_name]
                if e.get("useButtons"):
                    all_buttons.extend(e["useButtons"])

            # Remove duplicates while preserving order
            seen_buttons = set()
            unique_buttons = []
            for btn_id in all_buttons:
                if btn_id not in seen_buttons:
                    seen_buttons.add(btn_id)
                    unique_buttons.append(btn_id)

            # Collect all selects (from command and from embeds)
            all_selects = list(data.get("useSelects", []))
            
            # Check for selects in embeds
            if embed_name and embed_name in data["embeds"]:
                e = data["embeds"][embed_name]
                if e.get("useSelects"):
                    all_selects.extend(e["useSelects"])

            # Remove duplicates for selects
            seen_selects = set()
            unique_selects = []
            for sel_id in all_selects:
                if sel_id not in seen_selects:
                    seen_selects.add(sel_id)
                    unique_selects.append(sel_id)

            # Build buttons
            if unique_buttons:
                button_list = []
                for btn_id in unique_buttons:
                    if btn_id in buttons_data:
                        button_list.append(buttons_data[btn_id])
                
                if button_list:
                    view = ParaButton(button_list, events, buttons_data, modals_data, uservar_manager)
                    has_components = True

            # Build select menus
            if unique_selects:
                select_list = []
                for sel_id in unique_selects:
                    if sel_id in selects_data:
                        select_list.append(selects_data[sel_id])
                
                if select_list:
                    if view is None:
                        view = ParaSelectMenu(select_list, events, selects_data, modals_data, uservar_manager)
                    else:
                        # Combine button view with select menus
                        for select in select_list:
                            sel = nextcord.ui.Select(
                                placeholder=select["placeholder"],
                                custom_id=select["id"],
                                options=[
                                    nextcord.SelectOption(
                                        label=o["label"],
                                        value=o["value"]
                                    )
                                    for o in select["options"]
                                ]
                            )
                            # Add callback for select menu
                            async def select_callback(interaction: nextcord.Interaction):
                                from .runtime import replace_variables
                                from .parser import evaluate_conditionals
                                from .modals import ParaModal
                                
                                custom_id = interaction.data.get("custom_id")
                                selected_values = interaction.data.get("values", [])
                                selected_value = selected_values[0] if selected_values else None
                                
                                if custom_id in selects_data:
                                    event_id = custom_id
                                    if event_id in events:
                                        events_list = events[event_id]
                                        
                                        if not isinstance(events_list, list):
                                            events_list = [events_list]
                                        
                                        has_responded = False
                                        responses = []
                                        
                                        for event in events_list:
                                            if event.get("sendModal"):
                                                modal_id = event["sendModal"]
                                                if modal_id in modals_data:
                                                    if not has_responded:
                                                        modal = ParaModal(modals_data[modal_id], events, uservar_manager)
                                                        await interaction.response.send_modal(modal)
                                                        has_responded = True
                                                    continue
                                            
                                            text = event.get("text", "")
                                            if text:
                                                if "$if[" in text:
                                                    text = evaluate_conditionals(text, selected_value)
                                                text = replace_variables(text, interaction, selected_value, uservar_manager)
                                                if text:
                                                    responses.append(text)
                                        
                                        if responses:
                                            full_response = "\n\n".join(responses)
                                            if not has_responded:
                                                await interaction.response.send_message(full_response)
                                            else:
                                                await interaction.followup.send(full_response)
                            
                            sel.callback = select_callback
                            view.add_item(sel)
                    has_components = True

            # Handle modal
            if data.get("sendModal"):
                modal_id = data["sendModal"]
                if modal_id in modals_data:
                    # For modal, we can't send it directly in on_message
                    # User needs to use a button or slash command to trigger modal
                    await message.channel.send("Modal can only be sent through interactions (buttons/slash commands)")
                    return

            if embed_name and embed_name in data["embeds"]:

                e = data["embeds"][embed_name]

                color = e.get("color")

                if color:
                    color_value = int(
                        color.replace("#", ""),
                        16
                    )
                else:
                    color_value = 0x5865F2

                embed = nextcord.Embed(
                    title=replace_variables(e.get("title"), message, None, uservar_manager),
                    description=replace_variables(e.get("description"), message, None, uservar_manager),
                    color=color_value
                )

                if e.get("footer"):
                    embed.set_footer(text=replace_variables(e["footer"], message, None, uservar_manager))

                if e.get("thumbnail"):
                    embed.set_thumbnail(url=replace_variables(e["thumbnail"], message, None, uservar_manager))

                if e.get("image"):
                    embed.set_image(url=e["image"])

                if e.get("timestamp"):
                    embed.timestamp = message.created_at

                for f in e.get("fields", []):
                    embed.add_field(
                        name=replace_variables(
                            f["name"],
                            message,
                            None,
                            uservar_manager
                        ),
                        value=replace_variables(
                            f["value"],
                            message,
                            None,
                            uservar_manager
                        ),
                        inline=f["inline"]
                    )

                await message.channel.send(embed=embed, view=view)
                return

            if data.get("text"):

                response = replace_variables(
                    data["text"],
                    message,
                    None,
                    uservar_manager
                )

                await message.channel.send(
                    response, 
                    view=view
                )

        await bot.process_commands(message)

    bot.run(token)


def register_slash_command(bot, cmd_name, cmd_data, cooldown_manager, events, uservar_manager):
    """Register a slash command dynamically"""
    
    options_list = cmd_data.get("options", [])
    
    # Create the handler
    async def handler(interaction: nextcord.Interaction, **kwargs):
        # Check cooldown
        if cmd_data.get("cooldown"):
            cooldown_data = cmd_data["cooldown"]
            cooldown_seconds = cooldown_manager.parse_time(cooldown_data["time"])
            on_cooldown, remaining = cooldown_manager.check_cooldown(
                cmd_name, interaction.user.id, cooldown_seconds
            )
            
            if on_cooldown:
                cooldown_msg = cooldown_data["message"].replace(
                    "$time", cooldown_manager.format_time(remaining)
                )
                await interaction.response.send_message(cooldown_msg, ephemeral=True)
                return
            
            cooldown_manager.set_cooldown(cmd_name, interaction.user.id)
        
        # Get selected value from kwargs
        selected_value = None
        for opt in options_list:
            opt_name = opt["name"]
            if opt_name in kwargs and kwargs[opt_name] is not None:
                user_input = str(kwargs[opt_name])
                
                # If option type is "input" and has custom value, use custom value
                # Otherwise use the user's input/choice
                if opt["type"] == "input" and opt.get("value"):
                    selected_value = opt["value"]
                else:
                    selected_value = user_input
                break
        
        # Get response
        response_text = cmd_data.get("response", "Command executed")
        
        # Process conditionals
        if selected_value and "$if[" in response_text:
            response_text = evaluate_conditionals(response_text, selected_value)
        
        # Replace variables
        response_text = replace_variables(response_text, interaction, selected_value, uservar_manager)
        
        await interaction.response.send_message(response_text)
    
    # Register based on number of options
    if len(options_list) == 0:
        # No options
        async def cmd_no_opt(interaction: nextcord.Interaction):
            await handler(interaction)
        
        bot.slash_command(
            name=cmd_name,
            description=cmd_data.get("description", "Slash command")
        )(cmd_no_opt)
        
    elif len(options_list) == 1:
        # One option
        opt = options_list[0]
        
        # Build SlashOption with or without choices
        if opt["type"] == "choice" and opt.get("choices"):
            slash_opt = SlashOption(
                name=opt["name"],
                description=opt["description"],
                required=opt["required"],
                choices=opt["choices"]
            )
        else:
            slash_opt = SlashOption(
                name=opt["name"],
                description=opt["description"],
                required=opt["required"]
            )
        
        async def cmd_1_opt(
            interaction: nextcord.Interaction,
            option1: str = slash_opt
        ):
            await handler(interaction, **{opt["name"]: option1})
        
        bot.slash_command(
            name=cmd_name,
            description=cmd_data.get("description", "Slash command")
        )(cmd_1_opt)
        
    elif len(options_list) == 2:
        # Two options
        opt1, opt2 = options_list[0], options_list[1]
        
        # Build SlashOptions
        if opt1["type"] == "choice" and opt1.get("choices"):
            slash_opt1 = SlashOption(
                name=opt1["name"],
                description=opt1["description"],
                required=opt1["required"],
                choices=opt1["choices"]
            )
        else:
            slash_opt1 = SlashOption(
                name=opt1["name"],
                description=opt1["description"],
                required=opt1["required"]
            )
        
        if opt2["type"] == "choice" and opt2.get("choices"):
            slash_opt2 = SlashOption(
                name=opt2["name"],
                description=opt2["description"],
                required=opt2["required"],
                choices=opt2["choices"]
            )
        else:
            slash_opt2 = SlashOption(
                name=opt2["name"],
                description=opt2["description"],
                required=opt2["required"]
            )
        
        async def cmd_2_opt(
            interaction: nextcord.Interaction,
            option1: str = slash_opt1,
            option2: str = slash_opt2
        ):
            await handler(interaction, **{opt1["name"]: option1, opt2["name"]: option2})
        
        bot.slash_command(
            name=cmd_name,
            description=cmd_data.get("description", "Slash command")
        )(cmd_2_opt)
        
    elif len(options_list) == 3:
        # Three options
        opt1, opt2, opt3 = options_list[0], options_list[1], options_list[2]
        
        # Build SlashOptions
        if opt1["type"] == "choice" and opt1.get("choices"):
            slash_opt1 = SlashOption(
                name=opt1["name"],
                description=opt1["description"],
                required=opt1["required"],
                choices=opt1["choices"]
            )
        else:
            slash_opt1 = SlashOption(
                name=opt1["name"],
                description=opt1["description"],
                required=opt1["required"]
            )
        
        if opt2["type"] == "choice" and opt2.get("choices"):
            slash_opt2 = SlashOption(
                name=opt2["name"],
                description=opt2["description"],
                required=opt2["required"],
                choices=opt2["choices"]
            )
        else:
            slash_opt2 = SlashOption(
                name=opt2["name"],
                description=opt2["description"],
                required=opt2["required"]
            )
        
        if opt3["type"] == "choice" and opt3.get("choices"):
            slash_opt3 = SlashOption(
                name=opt3["name"],
                description=opt3["description"],
                required=opt3["required"],
                choices=opt3["choices"]
            )
        else:
            slash_opt3 = SlashOption(
                name=opt3["name"],
                description=opt3["description"],
                required=opt3["required"]
            )
        
        async def cmd_3_opt(
            interaction: nextcord.Interaction,
            option1: str = slash_opt1,
            option2: str = slash_opt2,
            option3: str = slash_opt3
        ):
            await handler(interaction, **{
                opt1["name"]: option1,
                opt2["name"]: option2,
                opt3["name"]: option3
            })
        
        bot.slash_command(
            name=cmd_name,
            description=cmd_data.get("description", "Slash command")
        )(cmd_3_opt)
    else:
        print(f"Warning: Slash command '{cmd_name}' has {len(options_list)} options. Maximum 3 supported.")