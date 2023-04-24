# read the env variable "DISCORD_TOKEN" from the environment variables
import os
import hikari
import lightbulb

if os.name != "nt":
    try:
        import uvloop
        uvloop.install()
    except:
        print("Installing uvloop is recommended on Linux, for better performance.")


DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")

# if the env variable is not set
if DISCORD_TOKEN is None:
    print("DISCORD_TOKEN is not set")
    exit(1)

def get_prefix(bot: lightbulb.BotApp, message: hikari.Message):
    return ["niko, ", "solstice "]


# default intents
intents = hikari.Intents.ALL & ~(hikari.Intents.GUILD_MEMBERS | hikari.Intents.GUILD_PRESENCES)
bot = lightbulb.BotApp(
    token=DISCORD_TOKEN,
    prefix=get_prefix,
    intents=intents,
    ignore_bots=True,
    owner_ids=[
        347366054806159360,  # main
        813770420758511636  # alt
    ],
    case_insensitive_prefix_commands=True
)


@bot.command()
@lightbulb.command("ping", "Returns the bot's latency")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context):
    await ctx.respond(f"Pong! {bot.heartbeat_latency * 1000:.2f}ms")


@bot.listen(hikari.StartingEvent)
async def on_starting(event: hikari.StartingEvent):
    print("Loading extensions...")
    bot.load_extensions_from("extensions")
    print("Extensions loaded.")


if __name__ == "__main__":
    bot.run()
