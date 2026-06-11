import nextcord

class ParaButton(
    nextcord.ui.View
):

    def __init__(self, buttons, events, buttons_data, modals_data=None, uservar_manager=None):

        super().__init__(timeout=None)

        self.events = events
        self.buttons_data = buttons_data
        self.modals_data = modals_data or {}
        self.uservar_manager = uservar_manager

        style_map = {

            "primary":
                nextcord.ButtonStyle.primary,

            "secondary":
                nextcord.ButtonStyle.secondary,

            "success":
                nextcord.ButtonStyle.success,

            "danger":
                nextcord.ButtonStyle.danger
        }

        for button in buttons:

            btn = nextcord.ui.Button(

                label=button["label"],

                style=style_map[button["style"]],

                custom_id=button["id"],

                emoji=button["emoji"]
            )
            
            # Add callback to handle button clicks
            btn.callback = self.button_callback
            
            self.add_item(btn)
    
    async def button_callback(self, interaction: nextcord.Interaction):
        """Handle button click events"""
        from .runtime import replace_variables
        from .parser import evaluate_conditionals
        from .modals import ParaModal
        import asyncio
        
        custom_id = interaction.data.get("custom_id")
        
        if custom_id in self.buttons_data:
            button = self.buttons_data[custom_id]
            event_id = button.get("event")
            button_value = button.get("value")  # Get button value
            
            if event_id and event_id in self.events:
                events_list = self.events[event_id]
                
                # If not a list, convert to list for compatibility
                if not isinstance(events_list, list):
                    events_list = [events_list]
                
                # Track if we've responded
                has_responded = False
                
                # Process all events with this ID SEQUENTIALLY
                for idx, event in enumerate(events_list):
                    # Check if event wants to send a modal
                    if event.get("sendModal"):
                        modal_id = event["sendModal"]
                        if modal_id in self.modals_data:
                            if not has_responded:
                                modal = ParaModal(self.modals_data[modal_id], self.events, self.uservar_manager)
                                await interaction.response.send_modal(modal)
                                has_responded = True
                            continue
                    
                    # Get text
                    text = event.get("text", "")
                    if text:
                        # Process conditionals if present
                        if "$if[" in text:
                            text = evaluate_conditionals(text, button_value)
                        
                        # Replace variables including $value
                        text = replace_variables(text, interaction, button_value, self.uservar_manager)
                        
                        if text:  # Only send if text is not empty
                            if not has_responded:
                                # First response
                                await interaction.response.send_message(text)
                                has_responded = True
                            else:
                                # Subsequent responses - use followup with delay
                                await asyncio.sleep(0.5)  # Small delay between messages
                                await interaction.followup.send(text)
                
                if has_responded:
                    return
        
        # Fallback response if no event found
        await interaction.response.send_message("No event handler found for this button.", ephemeral=True)