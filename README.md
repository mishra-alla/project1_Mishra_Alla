# Project1_Mishra_Alla_nod - Лабиринт сокровищ
Текстовая adventure игра "Лабиринт сокровищ".

## Описание
- Игрок блуждает по комнатам, собирает артефакты, разгадывает ребусы и загадки в комнатах - ищет `treasure_key`, подсказки с кодом для замка.
### Цель игры:  
 Получить главный приз - открыть сундук с сокровищами!
 (с помощью `treasure_key`, подсказки с кодом для замка).

- Игра завершается, когда игрок успешно открывает `treasure_chest` или вводит команду `quit`/`exit`.


## Установка
```bash
# Клонирование репозитория
git clone <your-repo-url>
cd project1_Mishra_Alla

# Установка зависимостей
poetry install
# Или через Makefile
poetry run project

## Использование
poetry run project
# или через Makefile
make project
```
> Убедитесь, что у вас установлены: Python 3.12 Poetry и/или make

## Структура проекта
```bash
project1_Ovsyannikov_Sergey_M25-555/
├── labyrinth_game/        # исходный код игры
│   ├── __init__.py
│   ├── main.py            # главный исполняемый файл
│   ├── constants.py       # константы (комнаты, help)
│   ├── player_actions.py  # действия игрока (перемещение, действия с предметами и т.д.)
│   └── utils.py           # вспомогательные функции
├── pyproject.toml.        # конфигурация проекта и зависимости
├── poetry.lock            # фиксированные версии зависимостей
├── Makefile               #команды для сборки и запуска
├── .gitignore
└── README.md
```


## Зависимости
- `Python >= 3.12`
- `Poetry`   # для управления зависимостями
- `Ruff`     # для проверки кода

## Автор
mishra-alla Email: [allasr22@gmail.com]
