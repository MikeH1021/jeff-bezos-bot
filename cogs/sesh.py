from discord.ext import commands
from discord import ui, Interaction, ButtonStyle
import asyncio

# Define a simple View that gives us a confirmation menu


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

    @commands.command()
    async def sesh(self, ctx, arg):
        """Invite someone to sesh"""
        view = Confirm()
        await ctx.message.delete()
        await ctx.send(f'<@{ctx.author.id}> has invited you to a sesh {arg}', view=view)
        # Wait for the View to stop listening for input...
        await view.wait()
        if view.value is None:
            print('Timed out...')
        elif view.value:
            print('Sesh confirmed! (^_^)')
        else:
            print('Cancelled...')


def setup(client):
    client.add_cog(Sesh(client))
