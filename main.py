import nextcord
from nextcord.ui import Button, View

TOKEN = "MTA5MTg0NTM4MjAyNTI0ODgwOA.Gb8-eO.ruAmrGVbOabKYBGErM4n6o-wjZ0lOFd3zorHdw"

botName = "Birdsupply#4154"

client = nextcord.Client()
verificationPassword = "Birdsupply"
verificationChannelID = 1074835768339607572
loggingChannelID = 1091846403464102050
verificationRoleID = 1033507950418997262
linksPermittedRoles = ["Member"]


@client.event
async def on_ready():
  print(f'{client.user} has connected to Discord!')
  verificationChannel = client.get_channel(verificationChannelID)

  messages = await verificationChannel.history(limit=200).flatten()
  for message in messages:
    if str(message.author) == botName:
      await message.delete()

  button = Button(label="Verify")
  view = View(timeout=None)
  view.add_item(button)
  button.callback = send  # 'send' of 'button_callback'
  embed = nextcord.Embed(
    title="Verification Discord Supply",
    description=
    "By clicking the verify button down below you agree that:\n\n- You will not use your account to harm, harass, or negatively affect other users.\n- You read <#1054496495937794149> to be informed\n- When trying to mislead us, we will ban you.\n- You follow the rules of discord ToS.\n\nPassword to enter is: **__Birdsupply__**",
    color=0xe73020)
  await verificationChannel.send(embed=embed, view=view)


async def button_callback(interaction):
  role = nextcord.utils.get(interaction.user.guild.roles, name="Member")
  await interaction.user.add_roles(role)

  embed = nextcord.Embed(title="Verification successful",
                         description="You have successfully been verified!",
                         color=0xe73020)
  await interaction.response.send_message(embed=embed, ephemeral=True)


@client.event
async def on_message(message):
  if str(message.author) == botName:
    return

  messageContent = message.content.lower()
  if "https://" in messageContent or ".com" in messageContent:
    roleAccepted = 0
    for x in range(len(linksPermittedRoles)):
      role = nextcord.utils.get(message.author.guild.roles,
                                name=linksPermittedRoles[x])
      if role in message.author.roles:
        roleAccepted = 1
        break
    if roleAccepted == 0:
      await message.delete()


class PasswordModal(nextcord.ui.Modal):

  def __init__(self):
    super().__init__("Verification")  # Modal title

    # Create a text input and add it to the modal
    self.name = nextcord.ui.TextInput(
      label="What is the key to verify?",
      min_length=5,
      max_length=25,
    )
    self.add_item(self.name)

  async def callback(self, interaction: nextcord.Interaction) -> None:
    # This is the function that gets called when the submit button is pressed
    loggingChannel = client.get_channel(loggingChannelID)
    response = f"{interaction.user.mention} gave:  {self.name.value}"
    if self.name.value == verificationPassword:
      response += ", correct password."
      role = nextcord.utils.get(interaction.user.guild.roles, name="Member")
      await interaction.user.add_roles(role)

      embed = nextcord.Embed(title="Verification Successful",
                             description="Correct password, welcome!",
                             color=0x2ec27e)
      await interaction.send(embed=embed, ephemeral=True)

      embed = nextcord.Embed(title="Verification Successful",
                             description=f"{interaction.user.mention} "
                             f"Has verified themself with: "
                             f"{self.name.value}",
                             color=0x2ec27e)
      await loggingChannel.send(embed=embed)
    else:
      embed = nextcord.Embed(title="Verification Failed",
                             description="Incorrect password, try again!",
                             color=0xe01b24)
      await interaction.send(embed=embed, ephemeral=True)

      embed = nextcord.Embed(title="Verification Failed",
                             description=f"{interaction.user.mention} "
                             f"Has attempted to gain access with: "
                             f"{self.name.value}",
                             color=0xe01b24)
      await loggingChannel.send(embed=embed)


async def send(interaction: nextcord.Interaction):
  modal = PasswordModal()
  await interaction.response.send_modal(modal)

client.run(TOKEN)
