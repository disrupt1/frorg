import discord
import os
from cogs.ticket import *
from discord.ext import commands

class Client(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        intents.moderation = True
        super().__init__(command_prefix=commands.when_mentioned_or('>'), intents=intents, chunk_guilds_at_startup=False)
        
    async def setup_hook(self):
        self.add_view(Openticket())
        self.add_view(Viewe())
        self.add_view(Closeticket())
        for extension in os.listdir('./cogs'):
            if extension.endswith('.py'):
                await client.load_extension(f'cogs.{extension[:-3]}')
                print(f"{extension} has been loaded.")
        
    async def on_ready(self):
        synced = await client.tree.sync()
        print(f"Synced {len(synced)} tree commands")
        await client.change_presence(activity=discord.Streaming(name="noobistan hunger games", url="https://www.twitch.tv/anomaly"))
        print (f"({client.user}) with id ({client.application_id}) is online.")

client = Client()
OWNER_ID = 609911897671860245

@client.command()
async def sync(ctx: commands.Context):
    """(This command can only be used by the owner)"""
    if ctx.author.id == OWNER_ID:
        await client.tree.sync()
        await ctx.reply("slash commands synced")
    else:
        await ctx.send("only the owner of the bot can access this command")
        
@client.tree.context_menu(name="Mute member")
async def mute(interaction: discord.Interaction, member: discord.Member):
    if interaction.user.guild_permissions.manage_roles == False:
        await interaction.response.send_message("You don't have Manage Roles permission to run this command.")
    else:
        muterole = discord.utils.get(interaction.guild.roles, name='Muted.')
        guild = interaction.guild
        if not muterole:
            await interaction.response.send_message("Mute role not detected. Creating mute role...", ephemeral=True)
            muterole = await guild.create_role(name='Muted.')
            for channel in guild.channels:
                await channel.set_permissions(muterole, send_messages=False, send_messages_in_threads=False, create_public_threads=False, create_private_threads=False)
            await interaction.edit_original_response(content="Mute role has been created, run the command again.")
        else:
            await member.add_roles(muterole)
            await interaction.response.send_message(f"{member.mention} has been muted.")
            
@client.tree.context_menu(name="Unmute member")
async def unmute(interaction: discord.Interaction, member: discord.Member):
    if interaction.user.guild_permissions.manage_roles == False:
        await interaction.response.send_message("You don't have Manage Roles permission to run this command.")
    else:
        muterole = discord.utils.get(interaction.guild.roles, name='Muted.')
        if not muterole or muterole not in member.roles:
            await interaction.response.send_message("Member is not muted", ephemeral=True)
        else:
            await member.remove_roles(muterole)
            await interaction.response.send_message(f"{member.mention} has been unmuted.")
            
@client.tree.context_menu(name="Delete message")
async def useless(interaction: discord.Interaction, message: discord.Message):
    await interaction.response.defer(thinking=True, ephemeral=True)
    await message.delete()
    await interaction.followup.send("Deleted message.", ephemeral=True)

@client.command()
async def embor(ctx: commands.Context):
    emb3 = discord.Embed(title="Test", url="https://r.mtdv.me/", description="test man", color=discord.Colour.random())
    emb3.set_author(name=ctx.author.display_name)
    emb3.add_field(name="test field", value="yes")
    emb3.set_thumbnail(url=ctx.author.display_avatar)
    emb3.set_footer(text=ctx.author.display_name)
    await ctx.send(content=ctx.guild.categories ,embed=emb3)

@client.tree.command()
async def testor(interaction: discord.Interaction):
    """ test for slash commands """
    print(f">{interaction.user} used the command.")
    await interaction.response.send_message("> sup homie", ephemeral=True)


client.run('ODk5Mjc3NDk1MjQ3OTY2Mjc5.GQCFev.RF8BIiGLtCz9_IItpOdVV_fN6aWf-SdjGljRTE')
