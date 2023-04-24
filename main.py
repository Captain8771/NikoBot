# read the env variable "DISCORD_TOKEN" from the environment variables
import os
import hikari
import lightbulb

if os.name != "nt":
    import uvloop
    uvloop.install()


DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")

# if the env variable is not set
if DISCORD_TOKEN is None:
    print("DISCORD_TOKEN is not set")
    exit(1)


# default intents
intents = hikari.Intents.ALL & ~(hikari.Intents.GUILD_MEMBERS | hikari.Intents.GUILD_PRESENCES)
bot = lightbulb.BotApp(
    token=DISCORD_TOKEN,
    prefix="niko, ",
    intents=intents,
    ignore_bots=True,
    owner_ids=[
        347366054806159360,  # main
        813770420758511636  # alt
    ]
)


@bot.command()
@lightbulb.command("ping", "Returns the bot's latency")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context):
    await ctx.respond(f"Pong! {bot.heartbeat_latency * 1000:.2f}ms")

@bot.listen(hikari.StartingEvent)
async def on_starting(event: hikari.StartingEvent):
    print("Loading extensions...")
    bot.load_extensions("extensions.Dev")

@bot.listen(hikari.StartedEvent)
async def on_started(event: hikari.StartedEvent):
    print(f"Logged in as {bot.get_me()}")


@bot.listen(lightbulb.CommandErrorEvent)
async def on_command_error(event: lightbulb.CommandErrorEvent):
    await event.context.respond(f"An error occurred while executing the command: {event.exception}")
    raise event.exception

if __name__ == "__main__":
    bot.run()
