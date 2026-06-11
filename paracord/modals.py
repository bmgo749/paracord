import nextcord

class ParaModal(
    nextcord.ui.Modal
):

    def __init__(self, modal_data, events, uservar_manager=None):

        super().__init__(
            title=modal_data["title"]
        )

        self.custom_id = modal_data["id"]
        self.events = events
        self.modal_id = modal_data["id"]
        self.uservar_manager = uservar_manager

        for field in modal_data["inputs"]:

            self.add_item(

                nextcord.ui.TextInput(

                    label=field["label"],

                    custom_id=field["id"],

                    min_length=
                        field["min"],

                    max_length=
                        field["max"],

                    placeholder=
                        field["placeholder"]
                )
            )
    
    async def callback(self, interaction: nextcord.Interaction):
        """Handle modal submission"""
        from .runtime import replace_variables
        from .parser import evaluate_conditionals
        import asyncio
        
        # Get all input values from modal
        # For modals, $value will be a formatted string of all inputs
        input_values = []
        for component in self.children:
            if hasattr(component, 'value') and component.value:
                input_values.append(f"{component.label}: {component.value}")
        
        # Join all values with newline
        modal_value = "\n".join(input_values) if input_values else "No input provided"
        
        # Check if there's an event for this modal
        if self.modal_id in self.events:
            events_list = self.events[self.modal_id]
            
            # If not a list, convert to list for compatibility
            if not isinstance(events_list, list):
                events_list = [events_list]
            
            has_responded = False
            
            # Process all events with this ID SEQUENTIALLY
            for idx, event in enumerate(events_list):
                text = event.get("text", "")
                if text:
                    # Process conditionals if present
                    if "$if[" in text:
                        text = evaluate_conditionals(text, modal_value)
                    
                    # Replace variables
                    text = replace_variables(text, interaction, modal_value, self.uservar_manager)
                    
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
        
        # Fallback
        await interaction.response.send_message("Modal submitted successfully!", ephemeral=True)