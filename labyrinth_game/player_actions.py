from labyrinth_game import constants
#from labyrinth_game.constants import ROOMS
import labyrinth_game.utils as utils

def get_input(prompt="> "):
    """Получение ввода от пользователя с обработкой ошибок"""
    try:
        return input(prompt).strip()
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit"

def show_inventory(game_state):
    """Показать инвентарь игрока"""
    inventory = game_state['player_inventory']
    
    if inventory:
        print(f"\nВаш инвентарь: {', '.join(inventory)}")
    else:
        print("\nВаш инвентарь пуст.")

def move_player(game_state, direction):
    """Перемещение игрока"""
    room_name = game_state['current_room']
    room = constants.ROOMS[room_name]
    
    if direction in room['exits']:
        new_room = room['exits'][direction]
        game_state['current_room'] = new_room
        game_state['steps_taken'] += 1
        
        print(f"\nВы перешли {direction} в {new_room}.")
        utils.describe_current_room(game_state)
    else:
        print(f"Нельзя пойти в направлении {direction}.")

def take_item(game_state, item_name):
    """Взять предмет"""
    room_name = game_state['current_room']
    room = constants.ROOMS[room_name]

    # Проверка на тяжелый сундук (требование задания)
    if item_name == "treasure_chest":
        print("Вы не можете поднять сундук, он слишком тяжелый.")
        return
    
    if item_name in room['items']:
        # Берем предмет
        game_state['player_inventory'].append(item_name)
        room['items'].remove(item_name) # Убираем из комнаты
        print(f"Вы взяли: {item_name}")
    else:
        print(f"Предмет '{item_name}' не найден.")

def use_item(game_state, item_name):
    """Использовать предмет из инвентаря"""
    print("\nЭта функция будет реализована на следующем этапе.")

def use_item(game_state, item_name):
    """Использовать предмет"""
    inventory = game_state['player_inventory']
    current_room = game_state['current_room']
    
    # ПОЛУЧАЕМ ДАННЫЕ КОМНАТЫ
    room = constants.ROOMS[current_room] 

    if item_name not in inventory:
        print(f"У вас нет предмета '{item_name}'.")
        return
    
    # 1. ФАКЕЛ в темной комнате
    if item_name == "torch" and current_room == "dark_room" and room.get('dark', False):
        print("\nВы зажигаете факел. Комната освещается!")
        print("Теперь вы видите маленький ключик (small_key) среди игрушек! Можете его взять!")
        room['items'].append('small_key')  # Добавляем ключ
        room['dark'] = False  # Комната больше не темная
        return
    
    # 2. МАЛЕНЬКИЙ КЛЮЧ на запечатанный сундук в HALL
    #if item_name == "small_key" and current_room == "hall":
    #    if "sealed_chest" in room['items']:
    #        print("\nВы используете маленький ключ на запечатанном сундуке...")
    #        print("Сундук открывается! Внутри вы находите ржавый ключ!")
    #        inventory.append('rusty_key')
    #        room['items'].remove('sealed_chest')
    #        inventory.remove('small_key')
    #        print("Теперь у вас есть rusty_key!")
    #    else:
    #        print("Здесь нет запечатанного сундука для этого ключа.")
    #    return
    
    # 2. МАЛЕНЬКИЙ КЛЮЧ для bronze_box
    if item_name == "small_key":
        # Проверяем есть ли bronze_box в комнате
        if "bronze_box" in room['items']:
            print("\nВы используете маленький ключ на бронзовой шкатулке...")
            print("Шкатулка открывается! Внутри вы находите ржавый ключ!")
            # Добавляем rusty_key в инвентарь
            inventory.append('rusty_key')       
            # Убираем bronze_box из комнаты
            room['items'].remove('bronze_box')
            # Убираем small_key из инвентаря (использован)
            if 'small_key' in inventory:
                inventory.remove('small_key')
            print("Теперь у вас есть rusty_key!")
        else:
            print("Здесь нет бронзовой шкатулки для этого ключа.")
        return
    
    # 3. КНИГА в комнате телепортации
    if item_name == "ancient_book" and current_room == "teleport_room":
        print("\nВы поставили книгу на подставку - древняя книга открылась")
        print("Символы на стенах начинают светиться ярче!")
        
        if "rusty_key" in inventory:
            print("Книга телепортирует вас прямо к сокровищам!")
            game_state['current_room'] = "treasure_room"
            utils.describe_current_room(game_state)
        else:
            print("Книга телепортирует вас в ловушку!")
            game_state['current_room'] = "trap_room"
            utils.describe_current_room(game_state)
        return

    # Проверяем предметы
    if item_name == "torch":
        print("\nВы зажгли факел. Стало светлее!")
        
    elif item_name == "sword":
        print("\nВы взмахнули мечом. Чувствуете уверенность!")
        
    elif item_name == "bronze_box":
        print("\nШкатулка заперта маленьким ключом. \n" \
                    "Найдите small_key чтобы открыть её.")
            
    elif item_name == "rusty_key":
        # Проверяем если мы в комнате с сокровищами
        if current_room == "treasure_room":
            print("\nВы используете ржавый ключ на сундуке...")
            print("Ключ подходит! Сундук открывается!")
            print("🎉 ПОЗДРАВЛЯЕМ! ВЫ НАШЛИ СОКРОВИЩА! 🎉")
            game_state['game_over'] = True
        else:
            print("Здесь нечего открывать этим ключом.")
            
    else:
        print(f"Вы не знаете, как использовать {item_name}.")