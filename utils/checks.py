from disnake import ApplicationCommandInteraction


def discord_admins(inter: ApplicationCommandInteraction):
    return inter.user.id in [324922480642752512, 377383169420427264]
