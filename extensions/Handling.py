import logging

import hikari
import lightbulb

plugin = lightbulb.Plugin("Handling")
logger = logging.getLogger("NikoBot").getChild("HandlingExtension")


@plugin.listener(hikari.StartedEvent)
async def on_started(event: hikari.StartedEvent):
    logger.info(f"Logged in as {plugin.bot.get_me()}")


@plugin.listener(lightbulb.CommandErrorEvent)
async def on_command_error(event: lightbulb.CommandErrorEvent):
    exception = event.exception
    exception = getattr(exception, "original", exception)
    if isinstance(exception, lightbulb.errors.CommandNotFound):
        if exception.invoked_with == "we":
            # we need to cook?
            if event.context.event.message.content.lower().startswith(f"niko, we need to cook"):
                await event.context.respond("waltuh, we need to cook")
                return

        embed = hikari.Embed(
            title="Command not found",
            description=f"The command `{exception.invoked_with}` was not found.",
            color=0xFF0000
        )
        await event.context.respond(embed=embed)

    elif isinstance(exception, lightbulb.errors.NotOwner):
        await event.context.respond("Never gonna give you up, never gonna let you down, "
                                    "never gonna run around and desert you.")

    else:
        # unknown exception
        await event.context.respond(f"An unknown error occurred: `{exception}`")
        raise exception


def load(bot: lightbulb.BotApp):
    bot.add_plugin(plugin)


def unload(bot: lightbulb.BotApp):
    bot.remove_plugin(plugin)
