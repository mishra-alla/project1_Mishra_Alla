#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from labyrinth_game import constants
from labyrinth_game import player_actions
from labyrinth_game import utils


def main():
    """Основная функция игры"""
    game_state = {
        'player_inventory': [],
        'current_room': 'entrance',
        'game_over': False,
        'steps_taken': 0
    }
    
    print("Добро пожаловать в Лабиринт сокровищ!")
    print("=" * 40)
    print("Введите 'help' для списка команд.")
    print("=" * 40)
    
    # Показываем стартовую комнату
    utils.describe_current_room(game_state)
    
    # Основной игровой цикл
    while not game_state['game_over']:
        command = player_actions.get_input("\n> ")
        process_command(game_state, command)


def process_command(game_state, command_line):
    """Обработка команд игрока"""
    # Убираем лишние пробелы и переводим в нижний регистр
    command_line = command_line.strip().lower()
    
    if not command_line:  # Пустая строка
        return
    
    # Разделяем команду на части
    parts = command_line.split()
    command = parts[0]
    
    # Обработка команд
    if command == "look":
        utils.describe_current_room(game_state)
        
    elif command == "go" and len(parts) > 1:
        direction = parts[1]
        player_actions.move_player(game_state, direction)
        
    elif command == "take" and len(parts) > 1:
        item_name = parts[1]
        player_actions.take_item(game_state, item_name)
        
    elif command == "inventory":
        player_actions.show_inventory(game_state)
        
    elif command == "help":
        utils.show_help()
        
    elif command == "solve":
        utils.solve_puzzle(game_state)
        
    elif command in ["quit", "exit"]:
        print("Спасибо за игру! До свидания!")
        game_state['game_over'] = True
        
    else:
        print(f"Неизвестная команда: {command}")
        print("Введите 'help' для списка команд.")


if __name__ == "__main__":
    main()