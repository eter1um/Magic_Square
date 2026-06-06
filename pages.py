from PyQt6.QtWidgets import (
    QWidget, QPushButton, QLabel, QVBoxLayout,
    QHBoxLayout, QFrame, QGridLayout,
    QComboBox, QSlider
)
from PyQt6.QtCore import Qt

def create_menu_page(title_font, subtitle_font):
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
    stats_button = QPushButton("Статистика")
    settings_button = QPushButton("Настройки")
    exit_button = QPushButton("Выход")

    for button in [play_button, rules_button, stats_button, settings_button, exit_button]:
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
    menu_layout.addWidget(stats_button, alignment=Qt.AlignmentFlag.AlignCenter)
    menu_layout.addSpacing(14)
    menu_layout.addWidget(settings_button, alignment=Qt.AlignmentFlag.AlignCenter)
    menu_layout.addSpacing(14)
    menu_layout.addWidget(exit_button, alignment=Qt.AlignmentFlag.AlignCenter)
    menu_layout.addStretch(2)

    widgets = {
        "title_label": title_label,
        "subtitle_label": subtitle_label,
        "play_button": play_button,
        "rules_button": rules_button,
        "stats_button": stats_button,
        "settings_button": settings_button,
        "exit_button": exit_button
    }

    return menu_page, widgets


def create_level_page(title_font, section_font):
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
        btn.setFixedSize(125, 46)

    for btn in [easy_button, medium_button, hard_button]:
        btn.setFixedSize(125, 46)

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

    level_layout.addSpacing(14)
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

    widgets = {
        "title_level": title_level,
        "subtitle_level": subtitle_level,
        "coins_label": coins_label,
        "level_back": level_back,
        "size_label": size_label,
        "difficulty_label": difficulty_label,
        "size3_button": size3_button,
        "size4_button": size4_button,
        "size5_button": size5_button,
        "easy_button": easy_button,
        "medium_button": medium_button,
        "hard_button": hard_button,
        "start_button": start_button
    }

    return level_page, widgets


def create_game_page(title_font):
    game_page = QWidget()
    game_layout = QVBoxLayout()
    game_page.setLayout(game_layout)

    game_title = QLabel("Игра")
    game_title.setFont(title_font)
    game_title.setAlignment(Qt.AlignmentFlag.AlignCenter)

    game_status = QLabel("Заполните пустые клетки")
    game_status.setAlignment(Qt.AlignmentFlag.AlignCenter)

    game_timer_label = QLabel("Время: 00:00")
    game_timer_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

    game_coins_label = QLabel("Очки: 0")
    game_coins_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

    game_magic_label = QLabel("Магическая сумма: 15")
    game_magic_label.setAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

    game_back_top = QPushButton("<-- Назад")
    game_back_top.setFixedSize(100, 36)

    game_top_layout = QHBoxLayout()
    game_top_layout.addWidget(game_back_top, alignment=Qt.AlignmentFlag.AlignLeft)
    game_top_layout.addStretch(1)

    game_info_layout = QVBoxLayout()
    game_info_layout.setSpacing(4)
    game_info_layout.addWidget(game_timer_label, alignment=Qt.AlignmentFlag.AlignRight)
    game_info_layout.addWidget(game_coins_label, alignment=Qt.AlignmentFlag.AlignRight)
    game_info_layout.addWidget(game_magic_label, alignment=Qt.AlignmentFlag.AlignRight)

    game_top_layout.addLayout(game_info_layout)

    grid_card = QFrame()
    grid_card.setObjectName("card")
    grid_card_layout = QVBoxLayout()
    grid_card.setLayout(grid_card_layout)

    grid_widget = QWidget()
    grid = QGridLayout()
    grid.setSpacing(8)
    grid.setContentsMargins(0, 0, 0, 0)
    grid_widget.setLayout(grid)

    grid_card_layout.addWidget(grid_widget, alignment=Qt.AlignmentFlag.AlignCenter)

    buttons_row = QHBoxLayout()
    buttons_row.setSpacing(12)

    check_button = QPushButton("Проверить")
    clear_button = QPushButton("Очистить")
    hint_button = QPushButton("Подсказка")

    for button in [check_button, clear_button, hint_button]:
        button.setFixedSize(130, 48)

    buttons_row.addStretch(1)
    buttons_row.addWidget(check_button)
    buttons_row.addWidget(clear_button)
    buttons_row.addWidget(hint_button)
    buttons_row.addStretch(1)

    game_layout.addSpacing(0)
    game_layout.addLayout(game_top_layout)
    game_layout.addSpacing(14)
    game_layout.addWidget(game_title, alignment=Qt.AlignmentFlag.AlignCenter)
    game_layout.addSpacing(8)
    game_layout.addWidget(game_status, alignment=Qt.AlignmentFlag.AlignCenter)
    board_area = QWidget()
    board_area.setFixedHeight(390)

    board_area_layout = QVBoxLayout()
    board_area_layout.setContentsMargins(0, 0, 0, 0)
    board_area_layout.setSpacing(0)
    board_area.setLayout(board_area_layout)

    board_area_layout.addStretch(1)
    board_area_layout.addWidget(grid_card, alignment=Qt.AlignmentFlag.AlignCenter)
    board_area_layout.addStretch(1)

    game_layout.addSpacing(16)
    game_layout.addWidget(board_area)
    game_layout.addSpacing(14)
    game_layout.addLayout(buttons_row)
    game_layout.addStretch(1)

    widgets = {
        "game_title": game_title,
        "game_status": game_status,
        "game_timer_label": game_timer_label,
        "game_coins_label": game_coins_label,
        "game_magic_label": game_magic_label,
        "game_back_top": game_back_top,
        "grid_card": grid_card,
        "grid": grid,
        "check_button": check_button,
        "clear_button": clear_button,
        "hint_button": hint_button
    }

    return game_page, widgets


def create_rules_page(title_font, subtitle_font):
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
    rules_card.setFixedSize(400, 330)

    rules_card_layout = QVBoxLayout()
    rules_card.setLayout(rules_card_layout)

    rules_text = QLabel()
    rules_text.setWordWrap(True)
    rules_text.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)
    rules_text.setFont(subtitle_font)

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

    widgets = {
        "title_rules": title_rules,
        "rules_subtitle": rules_subtitle,
        "rules_text": rules_text,
        "rules_back": rules_back
    }

    return rules_page, widgets


def create_stats_page(title_font, subtitle_font, section_font):
    stats_page = QWidget()
    stats_layout = QVBoxLayout()
    stats_page.setLayout(stats_layout)

    title_stats = QLabel("Статистика")
    title_stats.setFont(title_font)
    title_stats.setAlignment(Qt.AlignmentFlag.AlignCenter)

    stats_subtitle = QLabel("Общий прогресс игрока")
    stats_subtitle.setFont(subtitle_font)
    stats_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

    stats_card = QFrame()
    stats_card.setObjectName("card")
    stats_card.setFixedWidth(380)

    stats_card_layout = QVBoxLayout()
    stats_card.setLayout(stats_card_layout)

    stats_played_label = QLabel("Сыгранные игры:")
    stats_played_value = QLabel("0")

    stats_won_label = QLabel("Успешные игры:")
    stats_won_value = QLabel("0")

    stats_coins_label = QLabel("Общее число очков:")
    stats_coins_value = QLabel("0")

    for label in [stats_played_label, stats_won_label, stats_coins_label]:
        label.setFont(section_font)

    stats_card_layout.addWidget(stats_played_label)
    stats_card_layout.addWidget(stats_played_value)
    stats_card_layout.addSpacing(12)

    stats_card_layout.addWidget(stats_won_label)
    stats_card_layout.addWidget(stats_won_value)
    stats_card_layout.addSpacing(12)

    stats_card_layout.addWidget(stats_coins_label)
    stats_card_layout.addWidget(stats_coins_value)

    stats_back = QPushButton("Назад")
    stats_back.setFixedSize(200, 50)

    stats_layout.addStretch(1)
    stats_layout.addWidget(title_stats, alignment=Qt.AlignmentFlag.AlignCenter)
    stats_layout.addSpacing(8)
    stats_layout.addWidget(stats_subtitle, alignment=Qt.AlignmentFlag.AlignCenter)
    stats_layout.addSpacing(24)
    stats_layout.addWidget(stats_card, alignment=Qt.AlignmentFlag.AlignCenter)
    stats_layout.addSpacing(24)
    stats_layout.addWidget(stats_back, alignment=Qt.AlignmentFlag.AlignCenter)
    stats_layout.addStretch(2)

    widgets = {
        "title_stats": title_stats,
        "stats_subtitle": stats_subtitle,
        "stats_played_label": stats_played_label,
        "stats_played_value": stats_played_value,
        "stats_won_label": stats_won_label,
        "stats_won_value": stats_won_value,
        "stats_coins_label": stats_coins_label,
        "stats_coins_value": stats_coins_value,
        "stats_back": stats_back
    }

    return stats_page, widgets


def create_settings_page(title_font, subtitle_font, section_font, music_volume, sound_volume):
    settings_page = QWidget()
    settings_page_layout = QVBoxLayout()
    settings_page.setLayout(settings_page_layout)

    title_settings = QLabel("Настройки")
    title_settings.setFont(title_font)
    title_settings.setAlignment(Qt.AlignmentFlag.AlignCenter)

    settings_subtitle = QLabel("Параметры интерфейса")
    settings_subtitle.setFont(subtitle_font)
    settings_subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)

    settings_card_page = QFrame()
    settings_card_page.setObjectName("card")
    settings_card_page.setFixedSize(380, 500)

    settings_card_page_layout = QVBoxLayout()
    settings_card_page.setLayout(settings_card_page_layout)

    theme_label = QLabel("Тема интерфейса")
    theme_label.setFont(section_font)
    theme_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    light_theme_button = QPushButton("Светлая")
    dark_theme_button = QPushButton("Тёмная")

    light_theme_button.setFixedSize(140, 46)
    dark_theme_button.setFixedSize(140, 46)

    theme_buttons_layout = QHBoxLayout()
    theme_buttons_layout.setSpacing(12)
    theme_buttons_layout.addWidget(light_theme_button)
    theme_buttons_layout.addWidget(dark_theme_button)

    settings_card_page_layout.addWidget(theme_label)
    settings_card_page_layout.addSpacing(12)
    settings_card_page_layout.addLayout(theme_buttons_layout)
    settings_card_page_layout.addSpacing(24)

    language_label = QLabel("Язык интерфейса")
    language_label.setFont(section_font)
    language_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    language_combo = QComboBox()
    language_combo.addItem("Русский")
    language_combo.addItem("English")
    language_combo.setFixedHeight(42)

    settings_card_page_layout.addWidget(language_label)
    settings_card_page_layout.addSpacing(10)
    settings_card_page_layout.addWidget(language_combo)
    settings_card_page_layout.addSpacing(24)

    music_volume_label = QLabel("Громкость музыки")
    music_volume_label.setFont(section_font)
    music_volume_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    music_volume_value = QLabel("50%")
    music_volume_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

    music_volume_slider = QSlider(Qt.Orientation.Horizontal)
    music_volume_slider.setMinimum(0)
    music_volume_slider.setMaximum(100)
    music_volume_slider.setValue(music_volume)

    settings_card_page_layout.addWidget(music_volume_label)
    settings_card_page_layout.addSpacing(6)
    settings_card_page_layout.addWidget(music_volume_value)
    settings_card_page_layout.addWidget(music_volume_slider)
    settings_card_page_layout.addSpacing(18)

    sound_volume_label = QLabel("Громкость звуков")
    sound_volume_label.setFont(section_font)
    sound_volume_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    sound_volume_value = QLabel("50%")
    sound_volume_value.setAlignment(Qt.AlignmentFlag.AlignCenter)

    sound_volume_slider = QSlider(Qt.Orientation.Horizontal)
    sound_volume_slider.setMinimum(0)
    sound_volume_slider.setMaximum(100)
    sound_volume_slider.setValue(sound_volume)

    settings_card_page_layout.addWidget(sound_volume_label)
    settings_card_page_layout.addSpacing(6)
    settings_card_page_layout.addWidget(sound_volume_value)
    settings_card_page_layout.addWidget(sound_volume_slider)
    settings_card_page_layout.addSpacing(18)

    show_sums_label = QLabel("Показывать суммы")
    show_sums_label.setFont(section_font)
    show_sums_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    show_sums_on_button = QPushButton("Да")
    show_sums_off_button = QPushButton("Нет")

    show_sums_on_button.setFixedSize(140, 46)
    show_sums_off_button.setFixedSize(140, 46)

    show_sums_buttons_layout = QHBoxLayout()
    show_sums_buttons_layout.setSpacing(12)
    show_sums_buttons_layout.addWidget(show_sums_on_button)
    show_sums_buttons_layout.addWidget(show_sums_off_button)

    settings_card_page_layout.addWidget(show_sums_label)
    settings_card_page_layout.addSpacing(10)
    settings_card_page_layout.addLayout(show_sums_buttons_layout)
    settings_card_page_layout.addSpacing(15)


    settings_back = QPushButton("Назад")
    settings_back.setFixedSize(200, 50)

    settings_page_layout.addStretch(1)
    settings_page_layout.addWidget(title_settings, alignment=Qt.AlignmentFlag.AlignCenter)
    settings_page_layout.addSpacing(8)
    settings_page_layout.addWidget(settings_subtitle, alignment=Qt.AlignmentFlag.AlignCenter)
    settings_page_layout.addSpacing(24)
    settings_page_layout.addWidget(settings_card_page, alignment=Qt.AlignmentFlag.AlignCenter)
    settings_page_layout.addSpacing(24)
    settings_page_layout.addWidget(settings_back, alignment=Qt.AlignmentFlag.AlignCenter)
    settings_page_layout.addStretch(2)

    widgets = {
        "title_settings": title_settings,
        "settings_subtitle": settings_subtitle,
        "theme_label": theme_label,
        "light_theme_button": light_theme_button,
        "dark_theme_button": dark_theme_button,
        "language_label": language_label,
        "language_combo": language_combo,
        "music_volume_label": music_volume_label,
        "music_volume_value": music_volume_value,
        "music_volume_slider": music_volume_slider,
        "sound_volume_label": sound_volume_label,
        "sound_volume_value": sound_volume_value,
        "sound_volume_slider": sound_volume_slider,
        "show_sums_label": show_sums_label,
        "show_sums_on_button": show_sums_on_button,
        "show_sums_off_button": show_sums_off_button,
        "settings_back": settings_back
    }

    return settings_page, widgets