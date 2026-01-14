# from labyrinth_game.constants import ROOMS
from labyrinth_game import constants
import math


def pseudo_random(seed, modulo):
    """Псевдослучайный генератор по sin())"""
    x = math.sin(seed * constants.SIN_MULTIPLIER) * constants.RANDOM_MULTIPLIER
    fractional = x - math.floor(x)
    return int(fractional * modulo)


def trigger_trap(game_state):
    """Активация ловушки"""
    print("\nЛовушка активирована! Пол стал дрожать...")

    inventory = game_state["player_inventory"]
    if inventory:
        # Выбираем случайный предмет
        idx = pseudo_random(game_state["steps_taken"], len(inventory))
        lost_item = inventory.pop(idx)
        print(f"Вы потеряли предмет: {lost_item}!")
    else:
        # Игрок получает урон
        chance = pseudo_random(game_state["steps_taken"], constants.EVENT_PROB)
        if chance < constants.TRAP_THRESHOLD:
            print("Вы попали в смертельную ловушку! Игра окончена!")
            game_state["game_over"] = True
        else:
            print("Вам повезло! Вы чудом избежали опасности!")


def random_event(game_state):
    """Случайное событие при перемещении"""
    # 30% шанс события (rand_num <= 2 из 10)
    rand_num = pseudo_random(game_state["steps_taken"], constants.EVENT_PROB)
    
    # Событие происходит если число <= порога
    if rand_num <= constants.RANDOM_THRESHOLD:
        # Выбираем событие
        event_type = pseudo_random(game_state["steps_taken"] + 1, constants.EVENT_TYPES)
        current_room = game_state["current_room"]
        room = constants.ROOMS[current_room]
        inventory = game_state["player_inventory"]

        #print("\nСлучайное событие!")       
        if event_type == 0:
            print("Вы нашли на полу монетку!")
            if "coin" not in room["items"]:
                room["items"].append("coin")
        
        elif event_type == 1:
            print("Вы слышите странный шорох из темного угла...")
            if "sword" in inventory:
                print("Вы хватаете меч, и звук мгновенно прекращается!")
        
        elif event_type == 2:
            if current_room == "trap_room" and "torch" not in inventory:
                print("Опасность! Кажется, вы активировали ловушку!")
                trigger_trap(game_state)
        
        elif event_type == 3:
            print("Вам сегодня везёт!")
            if inventory:
                print("Ваши предметы кажутся особенно ценными.")
        
        elif event_type == 4:
            smells = ["запах плесени", "аромат старых книг", "запах сырости", "сладкий аромат"]
            smell = smells[pseudo_random(game_state["steps_taken"], len(smells))]
            print(f"Вы чувствуете {smell}...")
        else:
            return


def describe_current_room(game_state):
    """Описание текущей комнаты"""
    room_name = game_state["current_room"]
    room = constants.ROOMS[room_name]

    print(f"\n== {room_name.upper()} ==")
    # print(room['description'])
    # Особое описание для темной комнаты
    if room.get("dark", False):
        print("Темно... ничего не видно.")
        print("(Может стоит осветить комнату?)")
    else:
        print(room["description"])

    # Показываем предметы (только если не темно)
    if not room.get("dark", False) and room["items"]:
        print(f"\nПредметы: {', '.join(room['items'])}")

    # Показываем предметы
    # if room['items']:
    #    print(f"Предметы: {', '.join(room['items'])}")

    # Показываем выходы
    if room["exits"]:
        directions = list(room["exits"].keys())
        print(f"Выходы: {', '.join(directions)}")

    # Показываем загадку
    if room["puzzle"]:
        print("Есть загадка! Введите 'solve' чтобы решить.")


def solve_puzzle(game_state):
    """Решение загадки"""
    room_name = game_state["current_room"]
    room = constants.ROOMS[room_name]
    # Проверка темноты
    if room.get("dark", False):
        print("Слишком темно, чтобы что-то разглядеть!")
        return
    # Если игрок в hall и хочет открыть дверь
    if room_name == "hall":
        print("1. Решить загадку на пьедестале")
        print("2. Попробовать открыть дверь на север(north)")
        choice = input("Выберите (1/2): ").strip()

        if choice == "2":
            # Загадка двери
            print(f"\nЗагадка двери: {room['door_puzzle'][0]}")
            answer = input("Код: ").strip()

            # ALTERNATIVE_ANSWERS
            correct_answers = ["9"]
            if "9" in constants.ALTERNATIVE_ANSWERS:
                correct_answers.extend(constants.ALTERNATIVE_ANSWERS["9"])
                print("Дверь открывается!")
                constants.ROOMS["treasure_room"]["locked"] = False
            else:
                print("Неверный код.")
            return

    if not room["puzzle"]:
        print("Загадок здесь нет.")
        return

    question, correct = room["puzzle"]
    print(f"\nЗагадка: {question}")

    answer = input("Ваш ответ: ").strip().lower()

    # Используем ALTERNATIVE_ANSWERS
    correct_answers = [correct.lower()]
    if correct in constants.ALTERNATIVE_ANSWERS:
        correct_answers.extend(constants.ALTERNATIVE_ANSWERS[correct])

    if answer in correct_answers:
        print("Правильно!")
        room["puzzle"] = None
        if room_name == "hall":
            print("Пьедестал опускается...")

    else:
        print("Неверно. Попробуйте еще раз.")
        # В trap_room - активируем ловушку
        if room_name == "trap_room":
            trigger_trap(game_state)


def attempt_open_treasure(game_state):
    """Попытка открыть сундук с сокровищами"""
    room_name = game_state["current_room"]
    room = constants.ROOMS[room_name]
    inventory = game_state["player_inventory"]

    if "treasure_chest" not in room["items"]:
        print("Здесь нет сундука с сокровищами.")
        return
    # Проверка ключа
    if "rusty_key" in inventory:
        print("Вы применяете ключ, и замок щёлкает. Сундук открывается!")
        print("В сундуке сокровище! Вы победили!")
        game_state["game_over"] = True
        return

    # Предложение ввести код
    print("Сундук заперт. У вас нет ключа.")
    answer = input("Попробовать ввести код? (да/нет): ").strip().lower()

    if answer == "да":
        code = input("Введите код: ").strip()
        if code == "10":  # Код из загадки treasure_room
            print("Код верный! Сундук открывается!")
            print("В сундуке сокровище! Вы победили!")
            game_state["game_over"] = True
        else:
            print("Неверный код.")
    else:
        print("Вы отступаете от сундука.")


def show_help():
    """Показать список команд"""
    print("КОМАНДЫ:")
    print("-" * 40)
    for cmd, desc in constants.COMMANDS.items():
        print(f"  {cmd:<16} - {desc}")
    print("\nПОДСКАЗКИ:")
    print("-" * 40)
    print("- Можно использовать north/south/east/west без 'go'")
    print("- Используйте torch в темных комнатах")
    print("- В trap_room будьте осторожны с неверными ответами")
    print("- Случайные события происходят при перемещении")
    print("\nПРИМЕРЫ:")
    print("" + "-" * 40)
    print("  north  / или go north")
    print("  take torch")
    print("  look")
