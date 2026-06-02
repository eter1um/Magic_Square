import random

from paths import resource_path, save_path

from localization import get_text

from audio import (
    setup_audio, play_music,
    set_music_volume, set_sound_volume,
    play_click, play_win, play_error
)

from game_logic import (
    load_boards, check_magic_square, numbers_in_range,
    has_duplicates, load_progress, save_progress,
    get_magic_constant
)

from dialogs import (
    show_info_dialog as create_info_dialog,
    show_choice_dialog as create_choice_dialog
)

from board_ui import (
    build_game_board as create_game_board,
    get_board_from_inputs
)

from pages import (
    create_menu_page, create_level_page, create_game_page,
    create_rules_page, create_stats_page, create_settings_page
)

from ui_config import (
    window_width, window_height,
    title_font_size, subtitle_font_size, section_font_size,
    style_sheet, dark_style_sheet, unlock_prices, hint_prices, reward_table
)

from PyQt6.QtWidgets import QWidget, QStackedLayout, QLabel

from PyQt6.QtCore import QTimer, Qt
from PyQt6.QtGui import QFont

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
save_file = save_path("save.json")

progress_data = load_progress(save_file)
coins = progress_data["coins"]
unlocked_4x4 = progress_data["unlocked_4x4"]
unlocked_5x5 = progress_data["unlocked_5x5"]
games_played = progress_data["games_played"]
games_won = progress_data["games_won"]

selected_size = 3
selected_difficulty = "easy"
current_theme = progress_data["theme"]
current_language = progress_data["language"]
music_volume = progress_data["music_volume"]
sound_volume = progress_data["sound_volume"]
show_sums = progress_data["show_sums"]

setup_audio()
set_music_volume(music_volume)
set_sound_volume(sound_volume)
play_music()

current_board_template = []
current_solution = []
current_puzzle = []
cells = []
row_sum_labels = []
col_sum_labels = []
diag_sum_labels = []
level_completed = False
game_seconds = 0
timer = QTimer()
hints_used = 0


def tr(key, **kwargs):
    return get_text(current_language, key, **kwargs)


def get_difficulty_name(difficulty):
    return tr(difficulty)

def get_time_bonus(seconds):
    if seconds <= 10:
        return 10
    elif seconds <= 15:
        return 5
    elif seconds <= 20:
        return 3
    return 0


# -------------------- Таймер --------------------
def update_timer_label():
    minutes = game_seconds // 60
    seconds = game_seconds % 60
    game_timer_label.setText(tr("time", minutes=minutes, seconds=seconds))


def tick_timer():
    global game_seconds
    game_seconds += 1
    update_timer_label()


def reset_timer():
    global game_seconds
    game_seconds = 0
    update_timer_label()


timer.timeout.connect(tick_timer)


# -------------------- Диалоговые окна --------------------
def get_current_style():
    if current_theme == "dark":
        return dark_style_sheet
    return style_sheet


def show_info_dialog(title, text):
    create_info_dialog(
        window,
        title,
        text,
        tr("ok"),
        get_current_style()
    )


def show_choice_dialog(title, text, left_text, right_text):
    return create_choice_dialog(
        window,
        title,
        text,
        left_text,
        right_text,
        get_current_style()
    )


# -------------------- Общие функции --------------------
def update_coins_labels():
    coins_label.setText(tr("coins", coins=coins))
    game_coins_label.setText(tr("coins", coins=coins))

def get_current_board_values():
    if not current_board_template:
        return []

    size = len(current_board_template)
    board = []
    k = 0

    for i in range(size):
        row = []

        for j in range(size):
            text = cells[k].text().strip()

            if text == "":
                row.append(0)
            else:
                try:
                    row.append(int(text))
                except ValueError:
                    row.append(0)

            k += 1

        board.append(row)

    return board


def clear_sum_labels():
    global row_sum_labels, col_sum_labels, diag_sum_labels

    for label in row_sum_labels + col_sum_labels + diag_sum_labels:
        label.deleteLater()

    row_sum_labels = []
    col_sum_labels = []
    diag_sum_labels = []


def create_sum_label():
    label = QLabel(grid_card)
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setFixedSize(34, 20)
    label.raise_()
    label.setVisible(show_sums)
    return label


def create_sum_labels(size):
    global row_sum_labels, col_sum_labels, diag_sum_labels

    clear_sum_labels()

    for i in range(size):
        row_sum_labels.append(create_sum_label())

    for j in range(size):
        col_sum_labels.append(create_sum_label())

    for i in range(2):
        diag_sum_labels.append(create_sum_label())


def update_sum_labels_position():
    if not cells:
        return

    size = len(current_board_template)
    grid_widget = grid.parentWidget()

    base_x = grid_widget.x()
    base_y = grid_widget.y()

    for i in range(size):
        right_cell = cells[i * size + (size - 1)]

        row_sum_labels[i].move(
            base_x + right_cell.x() + right_cell.width() - 4,
            base_y + right_cell.y() + right_cell.height() // 2 - 10
        )

    for j in range(size):
        bottom_cell = cells[(size - 1) * size + j]

        col_sum_labels[j].move(
            base_x + bottom_cell.x() + bottom_cell.width() // 2 - 17,
            base_y + bottom_cell.y() + bottom_cell.height() + 2
        )

    bottom_left_cell = cells[(size - 1) * size]
    bottom_right_cell = cells[size * size - 1]

    diag_sum_labels[0].move(
        base_x + bottom_right_cell.x() + bottom_right_cell.width() - 4,
        base_y + bottom_right_cell.y() + bottom_right_cell.height() + 2
    )

    diag_sum_labels[1].move(
        base_x + bottom_left_cell.x() - 30,
        base_y + bottom_left_cell.y() + bottom_left_cell.height() + 2
    )


def update_sum_hints():
    if not current_board_template:
        return

    if not row_sum_labels or not col_sum_labels or not diag_sum_labels:
        return
    
    if not show_sums:
        return

    size = len(current_board_template)
    board = get_current_board_values()

    for i in range(size):
        row_sum_labels[i].setText(str(sum(board[i])))

    for j in range(size):
        total = 0
        for i in range(size):
            total += board[i][j]
        col_sum_labels[j].setText(str(total))

    main_diag = 0
    side_diag = 0

    for i in range(size):
        main_diag += board[i][i]
        side_diag += board[i][size - 1 - i]

    diag_sum_labels[0].setText(str(main_diag))
    diag_sum_labels[1].setText(str(side_diag))

    update_sum_labels_position()

def update_stats_labels():
    stats_played_value.setText(str(games_played))
    stats_won_value.setText(str(games_won))
    stats_coins_value.setText(str(coins))


def update_size_buttons():
    if unlocked_4x4:
        size4_button.setText("4x4")
        size4_button.setProperty("locked", False)
    else:
        size4_button.setText(tr("buy_4x4"))
        size4_button.setProperty("locked", True)

    if unlocked_5x5:
        size5_button.setText("5x5")
        size5_button.setProperty("locked", False)
    else:
        size5_button.setText(tr("buy_5x5"))
        size5_button.setProperty("locked", True)

    for button in [size4_button, size5_button]:
        button.style().unpolish(button)
        button.style().polish(button)


def save_progress_data():
    progress_data["coins"] = coins
    progress_data["unlocked_4x4"] = unlocked_4x4
    progress_data["unlocked_5x5"] = unlocked_5x5
    progress_data["games_played"] = games_played
    progress_data["games_won"] = games_won
    progress_data["theme"] = current_theme
    progress_data["language"] = current_language
    progress_data["music_volume"] = music_volume
    progress_data["sound_volume"] = sound_volume
    progress_data["show_sums"] = show_sums
    save_progress(save_file, progress_data)


def set_selected_button(active_button, buttons):
    for button in buttons:
        button.setProperty("selected", False)
        button.style().unpolish(button)
        button.style().polish(button)

    active_button.setProperty("selected", True)
    active_button.style().unpolish(active_button)
    active_button.style().polish(active_button)


def apply_theme(theme):
    global current_theme

    current_theme = theme

    if theme == "light":
        window.setStyleSheet(style_sheet)
        set_selected_button(light_theme_button, [light_theme_button, dark_theme_button])
    elif theme == "dark":
        window.setStyleSheet(dark_style_sheet)
        set_selected_button(dark_theme_button, [light_theme_button, dark_theme_button])

    save_progress_data()


def change_language(language_index):
    global current_language

    if language_index == 0:
        current_language = "ru"
    else:
        current_language = "en"

    update_language_texts()
    save_progress_data()


def update_volume_labels():
    music_volume_value.setText(f"{music_volume}%")
    sound_volume_value.setText(f"{sound_volume}%")


def change_music_volume(value):
    global music_volume

    music_volume = value
    set_music_volume(value)
    update_volume_labels()
    save_progress_data()


def change_sound_volume(value):
    global sound_volume

    sound_volume = value
    set_sound_volume(value)
    update_volume_labels()
    save_progress_data()

def set_sum_labels_visible(visible):
    for label in row_sum_labels + col_sum_labels + diag_sum_labels:
        label.setVisible(visible)


def update_show_sums_buttons():
    if show_sums:
        set_selected_button(show_sums_on_button, [show_sums_on_button, show_sums_off_button])
    else:
        set_selected_button(show_sums_off_button, [show_sums_on_button, show_sums_off_button])


def change_show_sums(value):
    global show_sums

    show_sums = value
    set_sum_labels_visible(show_sums)
    update_show_sums_buttons()
    save_progress_data()

    if show_sums:
        update_sum_hints()

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

    choice = show_choice_dialog(
        tr("purchase"),
        tr("buy_field", size=size, price=price),
        tr("cancel"),
        tr("buy")
    )

    if choice != "right":
        return

    if coins < price:
        play_error()
        show_info_dialog(tr("not_enough_money"), tr("not_enough_money"))
        return

    coins -= price

    if size == 4:
        unlocked_4x4 = True
    elif size == 5:
        unlocked_5x5 = True

    save_progress_data()
    update_coins_labels()
    update_size_buttons()

    show_info_dialog(tr("purchase"), tr("purchase_success"))


def hide_cells_by_difficulty(board, difficulty):
    puzzle = [row[:] for row in board]
    size = len(board)

    total_cells = size * size

    if difficulty == "easy":
        hide_percent = 0.2
    elif difficulty == "medium":
        hide_percent = 0.35
    else:
        hide_percent = 0.5

    hide_count = max(1, round(total_cells * hide_percent))

    positions = []
    for i in range(size):
        for j in range(size):
            positions.append((i, j))

    random.shuffle(positions)

    for i in range(hide_count):
        row, col = positions[i]
        puzzle[row][col] = 0

    return puzzle


def build_game_board(board):
    global cells, current_board_template

    current_board_template = [row[:] for row in board]
    cells = create_game_board(grid, board)

    size = len(board)
    create_sum_labels(size)

    for cell in cells:
        if not cell.isReadOnly():
            cell.textChanged.connect(update_sum_hints)


def show_win_dialog():
    choice = show_choice_dialog(
        tr("win"),
        tr("win_text"),
        tr("main_menu"),
        tr("repeat")
    )

    if choice == "right":
        start_game()
    elif choice == "left":
        stack.setCurrentIndex(0)


def start_game():
    global current_solution, current_puzzle, level_completed, games_played, hints_used

    level_completed = False
    games_played += 1
    save_progress_data()
    hints_used = 0
    update_hint_button()

    timer.stop()
    reset_timer()
    timer.start(1000)

    if selected_size == 3:
        boards = load_boards(resource_path("levels/3x3.json"))
    elif selected_size == 4:
        boards = load_boards(resource_path("levels/4x4.json"))
    elif selected_size == 5:
        boards = load_boards(resource_path("levels/5x5.json"))
    else:
        return

    current_solution = random.choice(boards)
    current_puzzle = hide_cells_by_difficulty(current_solution, selected_difficulty)

    build_game_board(current_puzzle)

    game_title.setText(
        tr("game_title", size=selected_size, difficulty=get_difficulty_name(selected_difficulty))
    )

    game_magic_label.setText(
        tr("magic_constant", value=get_magic_constant(selected_size))
    )

    game_status.setText(tr("fill_empty_cells"))
    update_coins_labels()
    stack.setCurrentIndex(2)
    QTimer.singleShot(0, update_sum_hints)

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

    game_status.setText(tr("board_cleared"))
    update_sum_hints()


def update_hint_button():
    hint_button.setText(tr("hint"))

    if hints_used >= len(hint_prices):
        hint_button.setEnabled(False)
    else:
        hint_button.setEnabled(True)


def buy_hint():
    global coins, hints_used

    if not current_board_template:
        return

    if level_completed:
        play_error()
        game_status.setText(tr("level_completed"))
        return

    if hints_used >= len(hint_prices):
        play_error()
        game_status.setText(tr("hints_finished"))
        update_hint_button()
        return

    current_hint_price = hint_prices[hints_used]

    choice = show_choice_dialog(
        tr("hint"),
        tr("buy_hint_text", price=current_hint_price),
        tr("cancel"),
        tr("buy")
    )

    if choice != "right":
        return

    if coins < current_hint_price:
        play_error()
        show_info_dialog(tr("not_enough_money"), tr("not_enough_money"))
        return

    empty_positions = []
    size = len(current_board_template)

    for i in range(size):
        for j in range(size):
            cell_index = i * size + j

            if current_board_template[i][j] == 0 and cells[cell_index].text().strip() == "":
                empty_positions.append((i, j))

    if not empty_positions:
        play_error()
        show_info_dialog(tr("hint"), tr("no_empty_cells"))
        return

    row, col = random.choice(empty_positions)
    correct_value = current_solution[row][col]

    cell_index = row * size + col
    cell = cells[cell_index]

    cell.setText(str(correct_value))
    cell.setReadOnly(True)
    cell.setProperty("fixed", True)
    cell.style().unpolish(cell)
    cell.style().polish(cell)

    current_board_template[row][col] = correct_value
    update_sum_hints()

    coins -= current_hint_price
    hints_used += 1
    play_click()

    save_progress_data()
    update_coins_labels()
    update_stats_labels()
    update_hint_button()

    game_status.setText(tr("hint_bought", price=current_hint_price))


def check_game():
    global coins, level_completed, games_won

    if not current_board_template:
        return

    if level_completed:
        game_status.setText(tr("already_completed"))
        return

    size = len(current_board_template)
    current_board = get_board_from_inputs(cells, size)

    if current_board is None:
        play_error()
        game_status.setText(tr("fill_all_cells"))
        return

    if not numbers_in_range(current_board):
        play_error()
        game_status.setText(tr("numbers_range", max_number=size * size))
        return

    if has_duplicates(current_board):
        play_error()
        game_status.setText(tr("no_duplicates"))
        return

    if check_magic_square(current_board):
        play_win()
        level_completed = True
        timer.stop()
        games_won += 1

        reward = reward_table[selected_size][selected_difficulty]
        time_bonus = get_time_bonus(game_seconds)
        total_reward = reward + time_bonus

        coins += total_reward

        save_progress_data()
        update_coins_labels()
        update_stats_labels()

        if time_bonus > 0:
            game_status.setText(
                tr("victory_reward_time", reward=reward, bonus=time_bonus, total=total_reward)
            )
        else:
            game_status.setText(tr("victory_reward", reward=reward))

        show_win_dialog()

    else:
        play_error()
        game_status.setText(tr("wrong_try_again"))


# -------------------- Страница меню --------------------
menu_page, menu_widgets = create_menu_page(title_font, subtitle_font)

title_label = menu_widgets["title_label"]
subtitle_label = menu_widgets["subtitle_label"]
play_button = menu_widgets["play_button"]
rules_button = menu_widgets["rules_button"]
stats_button = menu_widgets["stats_button"]
settings_button = menu_widgets["settings_button"]
exit_button = menu_widgets["exit_button"]

# -------------------- Страница выбора игры --------------------
level_page, level_widgets = create_level_page(title_font, section_font)

title_level = level_widgets["title_level"]
subtitle_level = level_widgets["subtitle_level"]
coins_label = level_widgets["coins_label"]
level_back = level_widgets["level_back"]
size_label = level_widgets["size_label"]
difficulty_label = level_widgets["difficulty_label"]
size3_button = level_widgets["size3_button"]
size4_button = level_widgets["size4_button"]
size5_button = level_widgets["size5_button"]
easy_button = level_widgets["easy_button"]
medium_button = level_widgets["medium_button"]
hard_button = level_widgets["hard_button"]
start_button = level_widgets["start_button"]

# -------------------- Страница игры --------------------
game_page, game_widgets = create_game_page(title_font)

game_title = game_widgets["game_title"]
game_status = game_widgets["game_status"]
game_timer_label = game_widgets["game_timer_label"]
game_coins_label = game_widgets["game_coins_label"]
game_magic_label = game_widgets["game_magic_label"]
game_back_top = game_widgets["game_back_top"]
grid_card = game_widgets["grid_card"]
grid = game_widgets["grid"]
check_button = game_widgets["check_button"]
clear_button = game_widgets["clear_button"]
hint_button = game_widgets["hint_button"]

# -------------------- Страница правил --------------------
rules_page, rules_widgets = create_rules_page(title_font, subtitle_font)

title_rules = rules_widgets["title_rules"]
rules_subtitle = rules_widgets["rules_subtitle"]
rules_text = rules_widgets["rules_text"]
rules_back = rules_widgets["rules_back"]

# -------------------- Страница статистики --------------------
stats_page, stats_widgets = create_stats_page(title_font, subtitle_font, section_font)

title_stats = stats_widgets["title_stats"]
stats_subtitle = stats_widgets["stats_subtitle"]
stats_played_label = stats_widgets["stats_played_label"]
stats_played_value = stats_widgets["stats_played_value"]
stats_won_label = stats_widgets["stats_won_label"]
stats_won_value = stats_widgets["stats_won_value"]
stats_coins_label = stats_widgets["stats_coins_label"]
stats_coins_value = stats_widgets["stats_coins_value"]
stats_back = stats_widgets["stats_back"]

# -------------------- Страница настроек --------------------
settings_page, settings_widgets = create_settings_page(
    title_font, subtitle_font, section_font,
    music_volume, sound_volume
)

title_settings = settings_widgets["title_settings"]
settings_subtitle = settings_widgets["settings_subtitle"]
theme_label = settings_widgets["theme_label"]
light_theme_button = settings_widgets["light_theme_button"]
dark_theme_button = settings_widgets["dark_theme_button"]
language_label = settings_widgets["language_label"]
language_combo = settings_widgets["language_combo"]
music_volume_label = settings_widgets["music_volume_label"]
music_volume_value = settings_widgets["music_volume_value"]
music_volume_slider = settings_widgets["music_volume_slider"]
sound_volume_label = settings_widgets["sound_volume_label"]
sound_volume_value = settings_widgets["sound_volume_value"]
sound_volume_slider = settings_widgets["sound_volume_slider"]
show_sums_label = settings_widgets["show_sums_label"]
show_sums_on_button = settings_widgets["show_sums_on_button"]
show_sums_off_button = settings_widgets["show_sums_off_button"]
settings_back = settings_widgets["settings_back"]

# -------------------- Stack --------------------
stack = QStackedLayout()
stack.addWidget(menu_page)
stack.addWidget(level_page)
stack.addWidget(game_page)
stack.addWidget(rules_page)
stack.addWidget(stats_page)
stack.addWidget(settings_page)

window.setLayout(stack)

# -------------------- Обновление языка --------------------
def update_language_texts():
    window.setWindowTitle(tr("window_title"))

    title_label.setText(tr("title"))
    subtitle_label.setText(tr("subtitle"))
    play_button.setText(tr("new_game"))
    rules_button.setText(tr("rules"))
    stats_button.setText(tr("statistics"))
    settings_button.setText(tr("settings"))
    exit_button.setText(tr("exit"))

    title_level.setText(tr("choose_game"))
    subtitle_level.setText(tr("choose_size_difficulty"))
    level_back.setText(tr("back_arrow"))
    size_label.setText(tr("field_size"))
    difficulty_label.setText(tr("difficulty"))
    easy_button.setText(tr("easy"))
    medium_button.setText(tr("medium"))
    hard_button.setText(tr("hard"))
    start_button.setText(tr("start"))

    if current_board_template:
        game_title.setText(
            tr("game_title", size=selected_size, difficulty=get_difficulty_name(selected_difficulty))
        )
    else:
        game_title.setText(tr("game"))

    game_magic_label.setText(
        tr("magic_constant", value=get_magic_constant(selected_size))
    )

    game_back_top.setText(tr("back_arrow"))
    check_button.setText(tr("check"))
    clear_button.setText(tr("clear"))
    hint_button.setText(tr("hint"))

    title_rules.setText(tr("rules"))
    rules_subtitle.setText(tr("rules_subtitle"))
    rules_text.setText(tr("rules_text"))
    rules_back.setText(tr("back"))

    title_stats.setText(tr("statistics"))
    stats_subtitle.setText(tr("stats_subtitle"))
    stats_played_label.setText(tr("played_games"))
    stats_won_label.setText(tr("won_games"))
    stats_coins_label.setText(tr("total_coins"))
    stats_back.setText(tr("back"))

    title_settings.setText(tr("settings"))
    settings_subtitle.setText(tr("settings_subtitle"))
    theme_label.setText(tr("interface_theme"))
    light_theme_button.setText(tr("light_theme"))
    dark_theme_button.setText(tr("dark_theme"))
    language_label.setText(tr("interface_language"))
    music_volume_label.setText(tr("music_volume"))
    sound_volume_label.setText(tr("sound_volume"))
    show_sums_label.setText(tr("show_sums"))
    show_sums_on_button.setText(tr("show_sums_on"))
    show_sums_off_button.setText(tr("show_sums_off"))
    settings_back.setText(tr("back"))

    update_coins_labels()
    update_size_buttons()
    update_timer_label()
    update_volume_labels()


# -------------------- Стили --------------------
window.setStyleSheet(style_sheet)

# -------------------- События --------------------
click_buttons = [
    play_button, rules_button, stats_button, settings_button, exit_button,
    level_back, start_button,
    rules_back, stats_back, settings_back,
    game_back_top,
    size3_button, size4_button, size5_button,
    easy_button, medium_button, hard_button,
    check_button, clear_button, hint_button,
    light_theme_button, dark_theme_button,
    show_sums_on_button, show_sums_off_button
]

for button in click_buttons:
    button.clicked.connect(play_click)

exit_button.clicked.connect(window.close)
play_button.clicked.connect(lambda: stack.setCurrentIndex(1))
rules_button.clicked.connect(lambda: stack.setCurrentIndex(3))

level_back.clicked.connect(lambda: stack.setCurrentIndex(0))
rules_back.clicked.connect(lambda: stack.setCurrentIndex(0))

stats_button.clicked.connect(lambda: (update_stats_labels(), stack.setCurrentIndex(4)))
stats_back.clicked.connect(lambda: stack.setCurrentIndex(0))

game_back_top.clicked.connect(lambda: (timer.stop(), stack.setCurrentIndex(1)))

start_button.clicked.connect(start_game)
check_button.clicked.connect(check_game)
clear_button.clicked.connect(clear_board)
hint_button.clicked.connect(buy_hint)

size3_button.clicked.connect(lambda: select_size(3))
size4_button.clicked.connect(lambda: select_size(4))
size5_button.clicked.connect(lambda: select_size(5))

easy_button.clicked.connect(lambda: select_difficulty("easy"))
medium_button.clicked.connect(lambda: select_difficulty("medium"))
hard_button.clicked.connect(lambda: select_difficulty("hard"))

settings_button.clicked.connect(lambda: stack.setCurrentIndex(5))
settings_back.clicked.connect(lambda: stack.setCurrentIndex(0))

light_theme_button.clicked.connect(lambda: apply_theme("light"))
dark_theme_button.clicked.connect(lambda: apply_theme("dark"))

language_combo.currentIndexChanged.connect(change_language)
music_volume_slider.valueChanged.connect(change_music_volume)
sound_volume_slider.valueChanged.connect(change_sound_volume)

show_sums_on_button.clicked.connect(lambda: change_show_sums(True))
show_sums_off_button.clicked.connect(lambda: change_show_sums(False))

# -------------------- Начальные состояния --------------------
def start_app():
    select_size(3)
    select_difficulty("easy")
    update_coins_labels()
    update_size_buttons()
    update_stats_labels()
    update_hint_button()
    reset_timer()

    if current_language == "ru":
        language_combo.setCurrentIndex(0)
    else:
        language_combo.setCurrentIndex(1)

    music_volume_slider.setValue(music_volume)
    sound_volume_slider.setValue(sound_volume)
    update_volume_labels()
    update_show_sums_buttons()

    update_language_texts()
    apply_theme(current_theme)