import sys
import random
from game_logic import (
    load_boards, check_magic_square, numbers_in_range,
    has_duplicates, load_progress, save_progress
)
from ui_config import (
    window_width, window_height,
    title_font_size, subtitle_font_size, section_font_size,
    style_sheet, unlock_prices
)
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QLabel, QVBoxLayout,
    QStackedLayout, QGridLayout, QLineEdit, QHBoxLayout,
    QFrame, QMessageBox
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


app = QApplication(sys.argv)

# -------------------- Главное окно --------------------
window = QWidget()
window.setWindowTitle("Магический квадрат")
window.setFixedSize(window_width, window_height)

# -------------------- Шрифты --------------------
title_font = QFont()
title_font.setPointSize(title_font_size)
title_font.setBold(True)

subtitle_font = QFont()
subtitle_font.setPointSize(subtitle_font_size)

section_font = QFont()
section_font.setPointSize(section_font_size)
section_font.setBold(True)

# -------------------- Состояние игры --------------------
save_file = "save.json"
progress_data = load_progress(save_file)
coins = progress_data["coins"]
unlocked_4x4 = progress_data["unlocked_4x4"]
unlocked_5x5 = progress_data["unlocked_5x5"]

selected_size = 3
selected_difficulty = "easy"

current_board_template = []
current_solution = []
current_puzzle = []
cells = []
level_completed = False

difficulty_names = {
    "easy": "Лёгкая",
    "medium": "Средняя",
    "hard": "Сложная"
}

# -------------------- Общие функции --------------------
def update_coins_labels():
    coins_label.setText(f"Очки: {coins}")
    game_coins_label.setText(f"Очки: {coins}")


def update_size_buttons():
    if unlocked_4x4:
        size4_button.setText("4x4")
    else:
        size4_button.setText("4x4 🔒")

    if unlocked_5x5:
        size5_button.setText("5x5")
    else:
        size5_button.setText("5x5 🔒")


def save_progress_data():
    progress_data["coins"] = coins
    progress_data["unlocked_4x4"] = unlocked_4x4
    progress_data["unlocked_5x5"] = unlocked_5x5
    save_progress(save_file, progress_data)


def clear_layout(layout):
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        child_layout = item.layout()

        if widget is not None:
            widget.deleteLater()
        elif child_layout is not None:
            clear_layout(child_layout)


def set_selected_button(active_button, buttons):
    for button in buttons:
        button.setProperty("selected", False)
        button.style().unpolish(button)
        button.style().polish(button)

    active_button.setProperty("selected", True)
    active_button.style().unpolish(active_button)
    active_button.style().polish(active_button)


def select_size(size):
    global selected_size

    if size == 4 and not unlocked_4x4:
        try_buy_size(4)
        if not unlocked_4x4:
            return

    if size == 5 and not unlocked_5x5:
        try_buy_size(5)
        if not unlocked_5x5:
            return

    selected_size = size

    mapping = {
        3: size3_button,
        4: size4_button,
        5: size5_button
    }
    set_selected_button(mapping[size], [size3_button, size4_button, size5_button])


def select_difficulty(difficulty):
    global selected_difficulty
    selected_difficulty = difficulty

    mapping = {
        "easy": easy_button,
        "medium": medium_button,
        "hard": hard_button
    }
    set_selected_button(mapping[difficulty], [easy_button, medium_button, hard_button])


def try_buy_size(size):
    global coins, unlocked_4x4, unlocked_5x5

    price = unlock_prices[size]

    msg = QMessageBox(window)
    msg.setWindowTitle("Покупка")
    msg.setText(f"Купить поле {size}x{size} за {price} очков?")

    buy_button = msg.addButton("Купить", QMessageBox.ButtonRole.AcceptRole)
    msg.addButton("Отмена", QMessageBox.ButtonRole.RejectRole)

    msg.exec()

    if msg.clickedButton() != buy_button:
        return

    if coins < price:
        QMessageBox.information(window, "Недостаточно средств", "Недостаточно средств")
        return

    coins -= price

    if size == 4:
        unlocked_4x4 = True
    elif size == 5:
        unlocked_5x5 = True

    save_progress_data()
    update_coins_labels()
    update_size_buttons()

    QMessageBox.information(window, "Покупка", "Покупка успешна")


def hide_cells_by_difficulty(board, difficulty):
    puzzle = [row[:] for row in board]
    size = len(board)

    if size == 3:
        if difficulty == "easy":
            hide_count = 2
        elif difficulty == "medium":
            hide_count = 4
        else:
            hide_count = 6
    elif size == 4:
        if difficulty == "easy":
            hide_count = 4
        elif difficulty == "medium":
            hide_count = 6
        else:
            hide_count = 8
    else:
        if difficulty == "easy":
            hide_count = 6
        elif difficulty == "medium":
            hide_count = 8
        else:
            hide_count = 10

    positions = []
    for i in range(size):
        for j in range(size):
            positions.append((i, j))

    random.shuffle(positions)

    for i in range(hide_count):
        row, col = positions[i]
        puzzle[row][col] = 0

    return puzzle


def get_board_from_inputs(size):
    result = []
    k = 0

    for i in range(size):
        row = []
        for j in range(size):
            text = cells[k].text().strip()

            if text == "":
                return None

            try:
                num = int(text)
            except ValueError:
                return None

            row.append(num)
            k += 1

        result.append(row)

    return result


def build_game_board(board):
    global cells, current_board_template

    current_board_template = [row[:] for row in board]
    cells = []

    clear_layout(grid)

    size = len(board)

    board_area = 300
    cell_size = board_area // size

    if size == 3:
        font_size = 22
    elif size == 4:
        font_size = 18
    else:
        font_size = 16

    for i in range(size):
        for j in range(size):
            value = board[i][j]

            cell = QLineEdit()
            cell.setAlignment(Qt.AlignmentFlag.AlignCenter)
            cell.setFixedSize(cell_size, cell_size)
            cell.setMaxLength(2)
            cell.setObjectName("gameCell")

            cell_font = QFont()
            cell_font.setPointSize(font_size)
            cell_font.setBold(True)
            cell.setFont(cell_font)

            if value == 0:
                cell.setText("")
                cell.setReadOnly(False)
                cell.setProperty("fixed", False)
            else:
                cell.setText(str(value))
                cell.setReadOnly(True)
                cell.setProperty("fixed", True)

            cell.style().unpolish(cell)
            cell.style().polish(cell)

            cells.append(cell)
            grid.addWidget(cell, i, j)


def show_win_dialog():
    msg = QMessageBox(window)
    msg.setWindowTitle("Победа")
    msg.setText("Вы успешно решили магический квадрат!")

    repeat_button = msg.addButton("Повторить", QMessageBox.ButtonRole.AcceptRole)
    menu_button = msg.addButton("В главное меню", QMessageBox.ButtonRole.RejectRole)

    msg.exec()

    if msg.clickedButton() == repeat_button:
        start_game()
    elif msg.clickedButton() == menu_button:
        stack.setCurrentIndex(0)


def start_game():
    global current_solution, current_puzzle, level_completed

    level_completed = False

    if selected_size == 3:
        boards = load_boards("levels/3x3.json")
    elif selected_size == 4:
        boards = load_boards("levels/4x4.json")
    elif selected_size == 5:
        QMessageBox.information(
            window,
            "Скоро будет",
            "Размер 5x5 уже открыт, но уровни для него пока не добавлены."
        )
        return
    else:
        return

    current_solution = random.choice(boards)
    current_puzzle = hide_cells_by_difficulty(current_solution, selected_difficulty)

    build_game_board(current_puzzle)

    game_title.setText(f"Игра {selected_size}x{selected_size} | {difficulty_names[selected_difficulty]}")
    game_status.setText("Заполните пустые клетки")
    update_coins_labels()
    stack.setCurrentIndex(2)


def clear_board():
    if not current_board_template:
        return

    size = len(current_board_template)
    k = 0

    for i in range(size):
        for j in range(size):
            if current_board_template[i][j] == 0:
                cells[k].setText("")
            k += 1

    game_status.setText("Поле очищено")


def check_game():
    global coins, level_completed

    if not current_board_template:
        return

    if level_completed:
        game_status.setText("Этот уровень уже пройден")
        return

    size = len(current_board_template)
    current_board = get_board_from_inputs(size)

    if current_board is None:
        game_status.setText("Заполните все клетки числами")
        return

    if not numbers_in_range(current_board):
        game_status.setText(f"Числа должны быть от 1 до {size * size}")
        return

    if has_duplicates(current_board):
        game_status.setText("Числа не должны повторяться")
        return

    if check_magic_square(current_board):
        level_completed = True
        coins += 10
        save_progress_data()
        update_coins_labels()
        game_status.setText("Победа! +10 очков")
        show_win_dialog()
    else:
        game_status.setText("Неверно. Попробуйте ещё раз")


# -------------------- Страница меню --------------------
menu_page = QWidget()
menu_layout = QVBoxLayout()
menu_page.setLayout(menu_layout)

title_label = QLabel("Магический квадрат")
title_label.setFont(title_font)
title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

subtitle_label = QLabel("Логическая игра на заполнение магического квадрата")
subtitle_label.setFont(subtitle_font)
subtitle_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

play_button = QPushButton("Новая игра")
rules_button = QPushButton("Правила")
exit_button = QPushButton("Выход")

for button in [play_button, rules_button, exit_button]:
    button.setFixedSize(240, 52)

menu_layout.addStretch(1)
menu_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignCenter)
menu_layout.addSpacing(8)
menu_layout.addWidget(subtitle_label, alignment=Qt.AlignmentFlag.AlignCenter)
menu_layout.addSpacing(70)
menu_layout.addWidget(play_button, alignment=Qt.AlignmentFlag.AlignCenter)
menu_layout.addSpacing(14)
menu_layout.addWidget(rules_button, alignment=Qt.AlignmentFlag.AlignCenter)
menu_layout.addSpacing(14)
menu_layout.addWidget(exit_button, alignment=Qt.AlignmentFlag.AlignCenter)
menu_layout.addStretch(2)

# -------------------- Страница выбора игры --------------------
level_page = QWidget()
level_layout = QVBoxLayout()
level_page.setLayout(level_layout)

title_level = QLabel("Новая игра")
title_level.setFont(title_font)
title_level.setAlignment(Qt.AlignmentFlag.AlignCenter)

subtitle_level = QLabel("Выберите размер поля и сложность")
subtitle_level.setAlignment(Qt.AlignmentFlag.AlignCenter)

coins_label = QLabel("Очки: 0")
coins_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

level_back = QPushButton("<-- Назад")
level_back.setFixedSize(100, 36)

size_label = QLabel("Размер поля")
size_label.setFont(section_font)
size_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

difficulty_label = QLabel("Сложность")
difficulty_label.setFont(section_font)
difficulty_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

size3_button = QPushButton("3x3")
size4_button = QPushButton("4x4")
size5_button = QPushButton("5x5")

easy_button = QPushButton("Лёгкая")
medium_button = QPushButton("Средняя")
hard_button = QPushButton("Сложная")

start_button = QPushButton("Начать")
start_button.setFixedSize(240, 52)

for btn in [size3_button, size4_button, size5_button]:
    btn.setFixedSize(110, 46)

for btn in [easy_button, medium_button, hard_button]:
    btn.setFixedSize(110, 46)

top_layout = QHBoxLayout()
top_layout.addWidget(level_back, alignment=Qt.AlignmentFlag.AlignLeft)
top_layout.addStretch(1)
top_layout.addWidget(coins_label, alignment=Qt.AlignmentFlag.AlignRight)

settings_card = QFrame()
settings_card.setObjectName("card")
settings_layout = QVBoxLayout()
settings_card.setLayout(settings_layout)

size_buttons_layout = QHBoxLayout()
size_buttons_layout.setSpacing(12)
size_buttons_layout.addWidget(size3_button)
size_buttons_layout.addWidget(size4_button)
size_buttons_layout.addWidget(size5_button)

difficulty_buttons_layout = QHBoxLayout()
difficulty_buttons_layout.setSpacing(12)
difficulty_buttons_layout.addWidget(easy_button)
difficulty_buttons_layout.addWidget(medium_button)
difficulty_buttons_layout.addWidget(hard_button)

settings_layout.addWidget(size_label)
settings_layout.addSpacing(12)
settings_layout.addLayout(size_buttons_layout)
settings_layout.addSpacing(24)
settings_layout.addWidget(difficulty_label)
settings_layout.addSpacing(12)
settings_layout.addLayout(difficulty_buttons_layout)

level_layout.addSpacing(18)
level_layout.addLayout(top_layout)
level_layout.addSpacing(20)
level_layout.addWidget(title_level)
level_layout.addSpacing(6)
level_layout.addWidget(subtitle_level)
level_layout.addSpacing(28)
level_layout.addWidget(settings_card, alignment=Qt.AlignmentFlag.AlignCenter)
level_layout.addSpacing(30)
level_layout.addWidget(start_button, alignment=Qt.AlignmentFlag.AlignCenter)
level_layout.addStretch(1)

# -------------------- Страница игры --------------------
game_page = QWidget()
game_layout = QVBoxLayout()
game_page.setLayout(game_layout)

game_title = QLabel("Игра")
game_title.setFont(title_font)
game_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

game_status = QLabel("Заполните пустые клетки")
game_status.setAlignment(Qt.AlignmentFlag.AlignCenter)

game_coins_label = QLabel("Очки: 0")
game_coins_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

game_back_top = QPushButton("<-- Назад")
game_back_top.setFixedSize(100, 36)

game_top_layout = QHBoxLayout()
game_top_layout.addWidget(game_back_top, alignment=Qt.AlignmentFlag.AlignLeft)
game_top_layout.addStretch(1)
game_top_layout.addWidget(game_coins_label, alignment=Qt.AlignmentFlag.AlignRight)

grid_card = QFrame()
grid_card.setObjectName("card")
grid_card_layout = QVBoxLayout()
grid_card.setLayout(grid_card_layout)

grid_widget = QWidget()
grid = QGridLayout()
grid.setSpacing(10)
grid.setContentsMargins(0, 0, 0, 0)
grid_widget.setLayout(grid)

grid_card_layout.addWidget(grid_widget, alignment=Qt.AlignmentFlag.AlignCenter)

buttons_row = QHBoxLayout()
buttons_row.setSpacing(12)

check_button = QPushButton("Проверить")
clear_button = QPushButton("Очистить")
game_back = QPushButton("В меню")

for button in [check_button, clear_button, game_back]:
    button.setFixedSize(140, 48)

buttons_row.addWidget(check_button)
buttons_row.addWidget(clear_button)
buttons_row.addWidget(game_back)

game_layout.addSpacing(18)
game_layout.addLayout(game_top_layout)
game_layout.addSpacing(18)
game_layout.addWidget(game_title)
game_layout.addSpacing(8)
game_layout.addWidget(game_status)
game_layout.addSpacing(24)
game_layout.addWidget(grid_card, alignment=Qt.AlignmentFlag.AlignCenter)
game_layout.addSpacing(24)
game_layout.addLayout(buttons_row)
game_layout.addStretch(1)

# -------------------- Страница правил --------------------
rules_page = QWidget()
rules_layout = QVBoxLayout()
rules_page.setLayout(rules_layout)

title_rules = QLabel("Правила")
title_rules.setFont(title_font)
title_rules.setAlignment(Qt.AlignmentFlag.AlignCenter)

rules_subtitle = QLabel("Как играть в магический квадрат")
rules_subtitle.setFont(subtitle_font)
rules_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

rules_card = QFrame()
rules_card.setObjectName("card")
rules_card.setFixedWidth(400)

rules_card_layout = QVBoxLayout()
rules_card.setLayout(rules_card_layout)

rules_text = QLabel(
    "Цель игры:\n"
    "заполнить пустые клетки так, чтобы получился магический квадрат.\n\n"
    "Правила:\n"
    "- суммы в каждой строке должны быть одинаковыми;\n"
    "- суммы в каждом столбце должны быть одинаковыми;\n"
    "- суммы на обеих диагоналях тоже должны совпадать;\n"
    "- каждое число можно использовать только один раз.\n\n"
    "После заполнения нажмите кнопку «Проверить»."
)
rules_text.setWordWrap(True)
rules_text.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

rules_card_layout.addWidget(rules_text)

rules_back = QPushButton("Назад")
rules_back.setFixedSize(200, 50)

rules_layout.addStretch(1)
rules_layout.addWidget(title_rules, alignment=Qt.AlignmentFlag.AlignCenter)
rules_layout.addSpacing(8)
rules_layout.addWidget(rules_subtitle, alignment=Qt.AlignmentFlag.AlignCenter)
rules_layout.addSpacing(24)
rules_layout.addWidget(rules_card, alignment=Qt.AlignmentFlag.AlignCenter)
rules_layout.addSpacing(24)
rules_layout.addWidget(rules_back, alignment=Qt.AlignmentFlag.AlignCenter)
rules_layout.addStretch(2)

# -------------------- Stack --------------------
stack = QStackedLayout()
stack.addWidget(menu_page)
stack.addWidget(level_page)
stack.addWidget(game_page)
stack.addWidget(rules_page)

window.setLayout(stack)

# -------------------- Стили --------------------
window.setStyleSheet(style_sheet)

# -------------------- События --------------------
exit_button.clicked.connect(window.close)
play_button.clicked.connect(lambda: stack.setCurrentIndex(1))
rules_button.clicked.connect(lambda: stack.setCurrentIndex(3))

level_back.clicked.connect(lambda: stack.setCurrentIndex(0))
rules_back.clicked.connect(lambda: stack.setCurrentIndex(0))

game_back_top.clicked.connect(lambda: stack.setCurrentIndex(1))
game_back.clicked.connect(lambda: stack.setCurrentIndex(0))

start_button.clicked.connect(start_game)
check_button.clicked.connect(check_game)
clear_button.clicked.connect(clear_board)

size3_button.clicked.connect(lambda: select_size(3))
size4_button.clicked.connect(lambda: select_size(4))
size5_button.clicked.connect(lambda: select_size(5))

easy_button.clicked.connect(lambda: select_difficulty("easy"))
medium_button.clicked.connect(lambda: select_difficulty("medium"))
hard_button.clicked.connect(lambda: select_difficulty("hard"))

# -------------------- Начальные состояния --------------------
select_size(3)
select_difficulty("easy")
update_coins_labels()
update_size_buttons()

window.show()
sys.exit(app.exec())