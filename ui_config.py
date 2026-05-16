window_width = 520
window_height = 680

title_font_size = 20
subtitle_font_size = 12
section_font_size = 14

unlock_prices = {
    4: 50,
    5: 100
}
reward_table = {
    3: {
        "easy": 10,
        "medium": 15,
        "hard": 20
    },
    4: {
        "easy": 25,
        "medium": 35,
        "hard": 50
    },
    5: {
        "easy": 45,
        "medium": 65,
        "hard": 90
    }
}

hint_prices = [10, 15, 20]

style_sheet = """
QWidget {
    background-color: #f4f1ea;
    color: #2b2b2b;
}

QLabel {
    background: transparent;
}

QFrame#card {
    background-color: #ffffff;
    border: 1px solid #d8d2c8;
    border-radius: 18px;
    padding: 18px;
}

QPushButton {
    background-color: #d9c3a3;
    border: none;
    border-radius: 12px;
    padding: 10px 14px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #cfb28c;
}

QPushButton[locked="true"] {
    background-color: #a89a87;
    color: #3f3a34;
}

QPushButton[locked="true"]:hover {
    background-color: #968773;
}

QPushButton:disabled {
    background-color: #8f877d;
    color: #4f4a44;
}

QPushButton[selected="true"] {
    background-color: #9f7b53;
    color: white;
}

QLineEdit#gameCell {
    background-color: #fbf8f2;
    border: 2px solid #ccb89a;
    border-radius: 10px;
    font-weight: bold;
}

QLineEdit#gameCell[fixed="true"] {
    background-color: #e8dccb;
    color: #5d4630;
}
"""