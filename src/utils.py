from discord import Color
from discord import OptionChoice


class Colors:

    color_options = [
        OptionChoice(name="Red", value=Color.red().value),
        OptionChoice(name="Green", value=Color.green().value),
        OptionChoice(name="Blue", value=Color.blue().value),
        OptionChoice(name="Yellow", value=Color.yellow().value),
        OptionChoice(name="Purple", value=Color.purple().value),
        OptionChoice(name="Orange", value=Color.orange().value),
        OptionChoice(name="Gray", value=Color.dark_gray().value),
        OptionChoice(name="Pink", value=Color.nitro_pink().value),
        OptionChoice(name="Random", value=Color.random().value)
    ]
