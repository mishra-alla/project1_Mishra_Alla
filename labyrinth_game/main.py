#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from labyrinth_game import player_actions
from labyrinth_game import utils


def main():
    # print("Первая попытка запустить проект!")

    game_state = {
        "player_inventory": [],  # Инвентарь игрока
        "current_room": "entrance",  # Текущая комната
        "game_over": False,  # Значения окончания игры
        "steps_taken": 0,  # Количество шагов
    }
    print("Добро пожаловать в Лабиринт сокровищ!")
    print("=" * 40)

    # Описание стартовой комнаты
    utils.describe_current_room(game_state)

    # Основной игровой цикл
    while not game_state["game_over"]:
        command = player_actions.get_input("> ")
        process_command(game_state, command)


def process_command(game_state, command_line):
    """Обработка команд игрока"""
    command_line = command_line.strip().lower()
    if not command_line:
        return

    # Разделяем команду на части
    parts = command_line.split()
    command = parts[0]

    match command:
        # Односложные команды движения
        case "north" | "south" | "east" | "west" as direction:
            player_actions.move_player(game_state, direction)

        # Команды с направлением и предметом
        case "go" if len(parts) > 1:
            direction = parts[1]
            player_actions.move_player(game_state, direction)
        case "take" if len(parts) > 1:
            item_name = parts[1]
            player_actions.take_item(game_state, item_name)
        case "use" if len(parts) > 1:
            item_name = parts[1]
            player_actions.use_item(game_state, item_name)

        # Простые команды без аргументов
        case "look":
            utils.describe_current_room(game_state)
        case "inventory":
            player_actions.show_inventory(game_state)
        case "solve":
            # Если в treasure_room - пробуем открыть сундук
            if game_state["current_room"] == "treasure_room":
                utils.attempt_open_treasure(game_state)
            else:
                utils.solve_puzzle(game_state)
        case "help":
            utils.show_help()
        case "quit" | "exit":
            print("Спасибо за игру! До свидания!")
            game_state["game_over"] = True
        case _:
            print(f"Неизвестная команда: {command}")
            print("Введите 'help' для списка команд.")


if __name__ == "__main__":
    main()
