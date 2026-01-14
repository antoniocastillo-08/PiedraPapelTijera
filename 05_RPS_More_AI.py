import random
import xml.etree.ElementTree as ET
from enum import IntEnum
from statistics import mode


class GameAction(IntEnum):
    Rock = 0
    Paper = 1
    Scissors = 2
    Lizard = 3
    Spock = 4


class GameResult(IntEnum):
    Victory = 0
    Defeat = 1
    Tie = 2


def load_victories(filename="victories.xml"):
    try:
        tree = ET.parse(filename)
        root = tree.getroot()
        rules = {}

        for victory in root.findall('victory'):
            winner_str = victory.get('choice')
            loser_str = victory.get('against')
            message = victory.text.strip()

            winner = GameAction[winner_str]
            loser = GameAction[loser_str]

            if winner not in rules:
                rules[winner] = {}
            rules[winner][loser] = message

        return rules
    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {filename}")
        return {}
    except KeyError as e:
        print(f"Error: La acción {e} en el XML no existe en GameAction")
        return {}


# Cargamos las reglas globalmente para sustituir el diccionario Victories anterior
RULES = load_victories()

NUMBER_RECENT_ACTIONS = 5


def assess_game(user_action, computer_action):
    if user_action == computer_action:
        print(f"User and computer picked {user_action.name}. Draw game!")
        return GameResult.Tie

    # Sustitución de la lógica manual por consulta al diccionario de reglas XML
    # Si la elección del usuario tiene a la de la PC como víctima:
    if computer_action in RULES.get(user_action, {}):
        print(f"{RULES[user_action][computer_action]}. You won!")
        return GameResult.Victory
    # De lo contrario, la PC gana (siempre que no sea empate)
    else:
        print(f"{RULES[computer_action][user_action]}. You lost!")
        return GameResult.Defeat


def get_computer_action(user_actions_history, game_history):
    if not user_actions_history or not game_history:
        computer_action = get_random_computer_action()
    else:
        # Predicción: buscar qué ganaría contra la acción más frecuente del usuario
        most_frequent_user_action = GameAction(mode(user_actions_history[-NUMBER_RECENT_ACTIONS:]))
        computer_action = get_winner_action(most_frequent_user_action)

    print(f"Computer picked {computer_action.name}.")
    return computer_action


def get_user_action():
    # Ahora muestra automáticamente Rock[0], Paper[1], Scissors[2], Lizard[3], Spock[4]
    game_choices = [f"{ga.name}[{ga.value}]" for ga in GameAction]
    game_choices_str = ", ".join(game_choices)
    user_selection = int(input(f"\nPick a choice ({game_choices_str}): "))
    return GameAction(user_selection)


def get_random_computer_action():
    computer_selection = random.randint(0, len(GameAction) - 1)
    return GameAction(computer_selection)


def get_winner_action(user_action):
    """
    Busca qué acciones pueden ganar a la acción del usuario basándose en las reglas XML.
    """
    possible_winners = [winner for winner, victims in RULES.items() if user_action in victims]
    return random.choice(possible_winners) if possible_winners else get_random_computer_action()


def play_another_round():
    another_round = input("\nAnother round? (y/n): ")
    return another_round.lower() == 'y'


def main():
    game_history = []
    user_actions_history = []

    while True:
        try:
            user_action = get_user_action()
            user_actions_history.append(user_action)
        except (ValueError, KeyError):
            range_str = f"[0, {len(GameAction) - 1}]"
            print(f"Invalid selection. Pick a choice in range {range_str}!")
            continue

        computer_action = get_computer_action(user_actions_history, game_history)
        game_result = assess_game(user_action, computer_action)
        game_history.append(game_result)

        if not play_another_round():
            break


if __name__ == "__main__":
    main()