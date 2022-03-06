from discord import User
from discord.commands import Option, slash_command
from discord.ext import commands
from discord import ui, Interaction, ButtonStyle
from vars import GUILD_ID


class Confirm(ui.View):
    def __init__(self):
        super().__init__()
        self.value = None

    # When the confirm button is pressed, set the inner value to `True` and
    # stop the View from listening to more input.
    # We also send the user an ephemeral message that we're confirming their choice.
    @ui.button(label='Confirm', style=ButtonStyle.green)
    async def confirm(self, button: ui.Button, interaction: Interaction):
        await interaction.response.send_message('Sesh is on! (^_^)', ephemeral=False)
        self.value = True
        self.stop()

    # This one is similar to the confirmation button except sets the inner value to `False`
    @ui.button(label='Decline', style=ButtonStyle.red)
    async def cancel(self, button: ui.Button, interaction: Interaction):
        await interaction.response.send_message('No sesh :(', ephemeral=False)
        self.value = False
        self.stop()


class Sesh(commands.Cog):

    def __init__(self, client):
        self.client = client

    @slash_command(name='sesh',
                   description='Invite someone to sesh',
                   guild_ids=[GUILD_ID])
    async def sesh(self, ctx, arg: Option(User, 'The person to invite', required=True)):
        view = Confirm()
        await ctx.respond(f'<@{ctx.author.id}> has invited you to a sesh <@{arg.id}>', view=view)
        # Wait for the View to stop listening for input...
        await view.wait()


def setup(client):
    client.add_cog(Sesh(client))
