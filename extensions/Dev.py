import hikari
import traceback
import lightbulb
import contextlib
import textwrap
from io import StringIO
import asyncio
import import_expression

plugin = lightbulb.Plugin("Dev")


@plugin.command()
@lightbulb.option("code", "The code to evaluate", modifier=lightbulb.OptionModifier.CONSUME_REST)
@lightbulb.add_checks(lightbulb.owner_only)
@lightbulb.command("eval", "Evaluates Python code", hidden=True)
@lightbulb.implements(lightbulb.PrefixCommand)
async def _eval(ctx: lightbulb.Context):
    vars = {
        "egg": "🥚",
    }
    code = ctx.options.code
    io = StringIO()
    auto_return = True
    dbg = False
    if "`" in code:
        flags = code[: code.find("`")].strip().split(" ")
        if flags:
            if "-r" in flags:
                auto_return = False

            if "-dbg" in flags:
                dbg = True

            code = code[code.find("`"):]

    if code.startswith("```") and code.endswith("```"):
        code = code[3:-3]
        if code.startswith("py"):
            code = code[2:]

    with contextlib.redirect_stdout(io):
        if ctx.event.message.referenced_message and ctx.event.message.referenced_message.type == hikari.MessageType.REPLY:
            reply = ctx.event.message.referenced_message
        else:
            reply = None
        vars = {
            **vars,
            "ctx": ctx,
            "message": ctx.event.message,
            "author": ctx.author,
            "channel": ctx.bot.cache.get_guild_channel(ctx.channel_id),
            "guild": ctx.bot.cache.get_guild(ctx.guild_id),
            "reference": reply,
            "bot": plugin.bot,
            "discord": hikari,
            "hikari": hikari,
            "lightbulb": lightbulb,
            "code": code
        }
        tb = None
        isstatement = False
        try:
            try:
                comp = import_expression.compile(code.split("\n")[-1], "<eval command>", "eval")
            except SyntaxError:  # its a statement
                isstatement = True
                try:
                    comp = import_expression.compile(code.split("\n")[-1], "<eval comomand>", "exec")
                except:
                    isstatement = "what the...?"

            if not auto_return:
                isstatement = True

            if not isstatement:
                _c = code.split("\n")
                _c[-1] = f"return {_c[-1]}"
                code = "\n".join(_c)

            c = f"async def func():\n    \"Function to evaluate code in discord.\"\n{textwrap.indent(code, prefix='    ')}"

            if not dbg:
                import_expression.exec(c, vars)
                returned = await vars["func"]()
            else:
                print(c)
                returned = "DBugger"
            if asyncio.iscoroutine(returned):
                returned = await returned
            output = io.getvalue()
            result = f"{output}\u200b```\n\n```diff\n+>>> {returned}"
        except Exception as e:
            tb = traceback.format_exception(type(e), e, e.__traceback__)
            result = "".join(tb)
        result = str(result)  # .replace(get_config().pc_name, "<PC NAME>")
        n = 1990
        chunks = [result[i: i + n] for i in range(0, len(result), n)]
        success = True if not tb else False
        if len(chunks) > 1:
            for i, chunk in enumerate(chunks):
                await ctx.respond(f"```py\n{chunk}```")
        else:
            await ctx.respond(f"```py\n{chunks[0]}```")


def load(bot):
    bot.add_plugin(plugin)

def unload(bot):
    bot.remove_plugin(plugin)