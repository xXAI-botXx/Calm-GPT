import sys
sys.path.insert(0, './RIS_bot')

from ris_bot import RIS_Bot
import numpy as np

scenarios = [
    "japanese garden",
    "express",
    "mountain",
    "forest clearing",
    "cave",
    "meadow",
    "outer-space",
    "hot-air-balloon",
    "christmas",
    "home",
    "ocean",
    "beach"
    "lake",
    "castle",
    "stream",
    "magic",
    "garden",
    "shopping mall",
    "medieval",
    "dinosaurs",
    "church",
    "adventure park",
    "zoo",
    "north pole",
    "other planet",
    "past",
    "timetravel",
    "flying",
    "clouds",
    "underwater world",
    "city in the sky",
    "atlantis",
    "heaven",
    "valhalla",
    "super mario world",
    "pokemon world",
    "chinese tempel",
    "travel around the world",
    "timeless bubble",
    "magic castle",
    "treehouse",
    "stone age",
    "whirlpool",
    "walking on the sun",
    "living on moon",
    "desert",
    "ice Storm",
    "in glacier",
    "vulcano",
    "chocolate factory",
    "super powers",
    "cave full of shiny jewels",
    "rainforest",
    "carnival",
    "haunted house",
    "art gallery",
    "amusement park",
    "aquarium",
    "planetarium",
    "rainbow",
    "circus",
    "futuristic city",
    "waterfall",
    "mountain lake",
    "coral reef",
    "safari",
    "starry sky",
    "enchanted forest",
    "cathedral",
    "fairy tale forest",
    "giants castle",
    "haunted mansion",
    "ice palace",
    "jungle temple",
    "fireplace",
    "gold cave",
    "mermaid lagoon",
    "rainbow bridge",
    "balcony with city view",
    "volcano island",
    "dinosaur island",
    "candy island",
    "space station",
    "zen garden",
    "xanadu city",
    "mythical creature",
    "mythical tempel",
    "witch cottage",
    "underwater cave"
]

start_sentence = "Create me a unique interactive story to calm with the topic:"

# # command methods
# def exit():
#     pass

# COMMANDS = {
#         	"exit": lambda x: x.exit(),
#             "restart": lambda x: x.restart()
# }


def run():
    bot = RIS_Bot('./RIS_bot/weights/model_weights_V3_6.pth')

    loop = 0
    while True:
        if loop == 0:
            input_sentence = "Write a scenario, you want to visit (or write nothing): "
        else:
            input_sentence = "Your Answer: "
        user_input = input(input_sentence)
        if user_input.lower() in ["q", "quit", "e", "exit", "x"]:
            print("See you later! I hope you had fun ^^")
            break
        elif user_input in ["restart", "new"]:
            loop = 0
            bot.reload()

        if loop == 0 and user_input in ["", "\n"]:
            user_input = np.random.choice(scenarios, 1)[0]
        
        if loop == 0:
            user_input = f"{start_sentence} {user_input}"

        print("Bot:", bot.inference(user_input))
        loop += 1

if __name__ == '__main__':
    run()