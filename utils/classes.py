import hikari as _hikari
import lightbulb as _lightbulb
import config as _config

__all__ = (
    "BotApp",
)


class BotApp(_lightbulb.BotApp):
    version: list[int, int, int] = _config.version

    def print_banner(
        self,
        banner,
        allow_color: bool,
        force_color: bool,
        extra_args=None,
    ) -> None:
        extra_args = {
            **(extra_args or {}),
            "major": str(self.version[0]),
            "minor": (self.version[1]),
            "patch": (self.version[2])
        }
        super(_lightbulb.BotApp, self).print_banner(banner, _config.colored_banner, force_color, extra_args)

