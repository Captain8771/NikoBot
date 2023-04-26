# read the env variable "DISCORD_TOKEN" from the environment variables
import os
import hikari
import lightbulb
from logging import getLogger, Logger
from utils import BotApp
import config

if config.supress_hikari_and_lightbulb_logs:
    import sys
    import re
    original_stdout = sys.stdout.write
    original_stderr = sys.stderr.write

    f = open(".hidden-logs.log", "w")

    def write(text: str, type: str = "stdout"):
        regex = re.compile(r"[a-z] \d{4}(?:-\d{2}){2} (?:\d{2}:){2}\d{2},\d{3} ((?:hikari|lightbulb)(?:\.[a-z]+\b)?)",
                           re.IGNORECASE | re.MULTILINE)
        # get matches from the text
        # but first, escape the ansii escape codes
        escaped = re.sub(r"\x1b\[[0-9;]*m", "", text)
        matches = regex.findall(escaped)
        if matches:
            f.write(f"Hidden log from {matches[0]}: {escaped}")
            f.flush()
            return
        if type == "stdout":

            original_stdout(text)
        elif type == "stderr":
            original_stderr(text)

    sys.stdout.write = lambda text: write(text, "stdout")
    sys.stderr.write = lambda text: write(text, "stderr")


logger = getLogger("NikoBot")

if os.name != "nt":
    try:
        import uvloop
        uvloop.install()
    except:
        logger.warning("Installing uvloop is recommended on Linux, for better performance.")


DISCORD_TOKEN = os.environ.get("DISCORD_TOKEN")

# if the env variable is not set
if DISCORD_TOKEN is None:
    print("DISCORD_TOKEN is not set")
    exit(1)


def get_prefix(bot: lightbulb.BotApp, message: hikari.Message):
    return ["niko, ", "solstice "]


# default intents
intents = hikari.Intents.ALL & ~(hikari.Intents.GUILD_MEMBERS | hikari.Intents.GUILD_PRESENCES)
bot = BotApp(
    token=DISCORD_TOKEN,
    prefix=get_prefix,
    intents=intents,
    ignore_bots=True,
    owner_ids=[
        347366054806159360,  # main
        813770420758511636  # alt
    ],
    case_insensitive_prefix_commands=True,
    banner="assets"
)


@bot.command()
@lightbulb.command("ping", "Returns the bot's latency")
@lightbulb.implements(lightbulb.PrefixCommand, lightbulb.SlashCommand)
async def ping(ctx: lightbulb.Context):
    await ctx.respond(f"Pong! {bot.heartbeat_latency * 1000:.2f}ms")


@bot.listen(hikari.StartingEvent)
async def on_starting(event: hikari.StartingEvent):
    logger.info("Loading extensions...")
    bot.load_extensions_from("extensions")
    logger.info("Extensions loaded.")


if __name__ == "__main__":
    # bot.run()
    logger.warning("Bot stopped. Exiting...")
    exit(0)
