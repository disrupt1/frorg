import discord
from discord import app_commands
from typing import Optional
from discord.ext import commands

class Ticket(commands.Cog):
    def __init__(self, client) -> None:
        self.client = client
    
    global Openticket
    class Openticket(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)
                    
        @discord.ui.button(label="Create a ticket", style=discord.ButtonStyle.blurple, emoji="📩", custom_id="openticket")
        async def ticketcallback(self, interaction: discord.Interaction, button: discord.ui.Button):
            guild = interaction.guild
            global user
            user = interaction.user
            overwritess = {
                guild.default_role: discord.PermissionOverwrite(view_channel=False, send_messages=False),
                interaction.user: discord.PermissionOverwrite(view_channel=True, send_messages=True)
            }
            await interaction.response.defer(thinking=True, ephemeral=True)
            categorye = discord.utils.get(guild.categories, name="Tickets")
            if not categorye:
                categorye = await guild.create_category(name="Tickets")
            global CHANNELE
            CHANNELE = await guild.create_text_channel(name=f"ticket-{interaction.user.display_name}", category=categorye, overwrites=overwritess)
            emb3 = discord.Embed(title="Staff will be with you shortly.")
            emb3.set_footer(text="frorg bot", icon_url="https://cdn.discordapp.com/avatars/899277495247966279/57324dd1cddc5ecc6298ad4b2752fe20.png?size=1024")
            await CHANNELE.send(f"Welcome {interaction.user.mention}", embed=emb3, view=Closeticket())
            await interaction.followup.send(f"Created ticket in {CHANNELE.mention}", ephemeral=True)
        
    global Closeticket
    class Closeticket(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)
                    
        @discord.ui.button(label="Close ticket", style=discord.ButtonStyle.red, emoji="❌", custom_id="closeticket")
        async def closebuttoncall(self, interaction: discord.Interaction, button: discord.ui.Button):
            guild = interaction.guild
            overwritesd = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False, send_messages=False)
        }
            await interaction.response.send_message("Closing this ticket...")
            close_category = discord.utils.get(guild.categories, name="Closed tickets")
            if not close_category:
                close_category = await guild.create_category(name="Closed tickets")
            close_channel = await CHANNELE.edit(name=f"closed-{interaction.user.display_name}" ,category=close_category, overwrites=overwritesd)
            await close_channel.send("This ticket has been closed.", view=Viewe())
            
    global Viewe
    class Viewe(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)
            
        @discord.ui.button(label="Delete ticket", custom_id="deleteticket", style=discord.ButtonStyle.red, emoji="🗑️")
        async def deletecallback(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message("Are you sure you want to delete this ticket?", view=Deleteticket())
            
    global Deleteticket
    class Deleteticket(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=20)
            
        @discord.ui.button(label="Yes", style=discord.ButtonStyle.green)
        async def yescall(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message("Deleting ticket...")
            await interaction.channel.delete()
            
    global deleteall
    class deleteall(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=100)
            
        @discord.ui.button(label="Yes", style=discord.ButtonStyle.red)
        async def yesbutton(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message("Deleting all ticket channels...")
            for channel in interaction.guild.channels:
                if channel.name.startswith("ticket-"):
                    await channel.delete(reason=None)
                if channel.name.startswith("closed-"):
                    await channel.delete(reason=None)
            await interaction.followup.send("All ticket channels have been deleted.")
            
        @discord.ui.button(label="No", style=discord.ButtonStyle.green)
        async def nobutton(self, interaction: discord.Interaction, button: discord.ui.Button):
            await interaction.response.send_message("Operation cancelled.")
    
    @app_commands.command()
    @app_commands.describe(channel="Select the channel you want to send this ticket panel. (optional)")
    async def setupticket(self, interaction: discord.Interaction, channel: Optional[discord.TextChannel]):
        """Sends a message to the current channel with a button that opens a ticket."""
        if interaction.user.guild_permissions.manage_guild == False:
            await interaction.response.send_message("You dont have permission to run this command", ephemeral=True)
        elif interaction.user.guild_permissions.manage_guild:
            emb = discord.Embed(title="Create a ticket!", description="Click the button below to create a ticket")
            if not channel:
                await interaction.response.send_message("Sent ticket panel to current channel.", ephemeral=True)
                await interaction.channel.send(embed=emb, view=Openticket())
            else:
                await interaction.response.send_message(f"Sent ticket panel to {channel.mention}.", ephemeral=True)
                await channel.send(embed=emb, view=Openticket())
                
    @app_commands.command()
    @app_commands.describe(member="Select the member you want to add to this ticket.")
    async def addmember(self, interaction: discord.Interaction, member: discord.Member):
        """Adds a member to a ticket channel."""
        if interaction.user.guild_permissions.manage_channels:
            if interaction.channel.name.startswith('ticket-') or interaction.channel.name.startswith("closed-"):
                overwritess = discord.PermissionOverwrite(view_channel=True, send_messages=True)
                await interaction.channel.set_permissions(member, overwrite=overwritess)
                await interaction.response.send_message(f"Added {member.mention} to the ticket.")
            else:
                await interaction.response.send_message("This is not a ticket channel", ephemeral=True)
        else:
            await interaction.response.send_message("You don't have manage channels permission to run this command.")
            
    @app_commands.command()
    @app_commands.describe(member="Select the member you want to add to this ticket.")
    async def removemember(self, interaction: discord.Interaction, member: discord.Member):
        """Removes a member from a ticket channel."""
        if interaction.user.guild_permissions.manage_channels:
            if interaction.channel.name.startswith('ticket-') or interaction.channel.name.startswith("closed-"):
                overwritess = discord.PermissionOverwrite(view_channel=False, send_messages=False)
                await interaction.channel.set_permissions(member, overwrite=overwritess)
                await interaction.response.send_message(f"Removed {member.mention} from the ticket.")
            else:
                await interaction.response.send_message("This is not a ticket channel", ephemeral=True)
        else:
            await interaction.response.send_message("You don't have manage channels permission to run this command.")
            
    @app_commands.command(name="delete-all-tickets")
    async def delete_all_tickets(self, interaction: discord.Interaction):
        """Deletes all ticket channels including closed ones."""
        if interaction.user.guild_permissions.manage_channels:
            await interaction.response.send_message("You do not have Manage Channels permission to run this command.", ephemeral=True)
        else:
            await interaction.response.send_message("Are you sure you want to delete all ticket channels?", view=deleteall())
    
async def setup(client):
    await client.add_cog(Ticket(client))