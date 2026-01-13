#from labyrinth_game.constants import ROOMS
from labyrinth_game import constants


def describe_current_room(game_state):
    """Описание текущей комнаты"""
    room_name = game_state['current_room']
    room = constants.ROOMS[room_name]
    
    print(f"\n== {room_name.upper()} ==")
    #print(room['description'])
    # Особое описание для темной комнаты
    if room.get('dark', False):
        print("Темно... ничего не видно.")
        print("(Может стоит осветить комнату?)")
    else:
        print(room['description'])

    # Показываем предметы (только если не темно)
    if not room.get('dark', False) and room['items']:
        print(f"\nПредметы: {', '.join(room['items'])}")

    # Показываем предметы
    #if room['items']:
    #    print(f"Предметы: {', '.join(room['items'])}")
    
    # Показываем выходы
    if room['exits']:
        directions = list(room['exits'].keys())
        print(f"Выходы: {', '.join(directions)}")
    
    # Показываем загадку
    if room['puzzle']:
        print("Есть загадка! Введите 'solve' чтобы решить.")


def show_help():
    """Показать список команд"""
    print("\nДоступные команды:")
    print("  go <direction>  - перейти в направлении (north/south/east/west)")
    print("  look            - осмотреть текущую комнату")
    print("  take <item>     - поднять предмет")
    print("  use <item>      - использовать предмет из инвентаря")
    print("  inventory       - показать инвентарь")
    print("  solve           - попытаться решить загадку в комнате")
    print("  quit            - выйти из игры")
    print("  help            - показать это сообщение")
    print("\n=== ПОДСКАЗКИ ===")
    print("- Используйте torch в темных комнатах")
    print("- Есть несколько вариантов открытия сокровища")
    print("\nПримеры:")
    print("  go north")
    print("  take torch")
    print("  look")

def solve_puzzle(game_state):
    """Решение загадки"""
    room_name = game_state['current_room']
    room = constants.ROOMS[room_name]
    
    # Проверка темноты
    if room.get('dark', False):
        print("Слишком темно, чтобы что-то разглядеть!")
        return
    
    if not room['puzzle']:
        print("Загадок здесь нет.")
        return

    question, correct_answer = room['puzzle']
    print(f"\nЗагадка: {question}")

    user_answer = input("Ваш ответ: ").strip().lower()

    if user_answer == correct_answer.lower():
        print("Правильно! Загадка решена!")
        # Убираем загадку
        #constants.ROOMS[room_name]['puzzle'] = None
        room['puzzle'] = None  # Убираем загадку
        # Можно добавить награду
        #print("Вы получаете награду!")
    else:
        print("Неверно. Попробуйте еще раз.")


def attempt_open_treasure(game_state):
    """Попытка открыть сундук с сокровищами"""
    print("\nЭта функция будет реализована на следующем этапе.")

def attempt_open_treasure(game_state):
    """Попытка открыть сундук с сокровищами"""
    room_name = game_state['current_room']
    room = constants.ROOMS[room_name]
    inventory = game_state['player_inventory']
    
    if "treasure_chest" not in room['items']:
        print("Здесь нет сундука с сокровищами.")
        return
    
    # Проверка ключа
    if 'rusty_key' in inventory:
        print("Вы применяете ключ, и замок щёлкает. Сундук открывается!")
        print("В сундуке сокровище! Вы победили!")
        game_state['game_over'] = True
        return
    
    # Предложение ввести код
    print("Сундук заперт. У вас нет ключа.")
    answer = input("Попробовать ввести код? (да/нет): ").strip().lower()
    
    if answer == 'да':
        code = input("Введите код: ").strip()
        if code == '10':  # Код из загадки treasure_room
            print("Код верный! Сундук открывается!")
            print("В сундуке сокровище! Вы победили!")
            game_state['game_over'] = True
        else:
            print("Неверный код.")
    else:
        print("Вы отступаете от сундука.")