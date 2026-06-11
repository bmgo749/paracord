import nextcord

class ParaSelectMenu(
    nextcord.ui.View
):

    def __init__(self, selects, events, selects_data, modals_data=None, uservar_manager=None):

        super().__init__(timeout=None)

        self.events = events
        self.selects_data = selects_data
        self.modals_data = modals_data or {}
        self.uservar_manager = uservar_manager

        for select in selects:

            sel = nextcord.ui.Select(

                placeholder=
                    select["placeholder"],

                custom_id=
                    select["id"],

                options=[

                    nextcord.SelectOption(

                        label=o["label"],
                        value=o["value"]

                    )

                    for o in select["options"]
                ]
            )
            
            # Add callback to handle select menu interactions
            sel.callback = self.select_callback
            
            self.add_item(sel)
    
    async def select_callback(self, interaction: nextcord.Interaction):
        """Handle select menu interactions"""
        from .runtime import replace_variables
        from .parser import evaluate_conditionals
        from .modals import ParaModal
        import asyncio
        
        custom_id = interaction.data.get("custom_id")
        selected_values = interaction.data.get("values", [])
        selected_value = selected_values[0] if selected_values else None
        
        if custom_id in self.selects_data:
            # Trigger event based on select menu id
            event_id = custom_id
            if event_id in self.events:
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
                            text = evaluate_conditionals(text, selected_value)
                        
                        # Replace variables including $value
                        text = replace_variables(text, interaction, selected_value, self.uservar_manager)
                        
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
        await interaction.response.send_message("No event handler found for this select menu.", ephemeral=True)