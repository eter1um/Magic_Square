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

dark_style_sheet = """
QWidget {
    background-color: #252525;
    color: #f0f0f0;
}

QLabel {
    background: transparent;
}

QFrame#card {
    background-color: #333333;
    border: 1px solid #555555;
    border-radius: 18px;
    padding: 18px;
}

QPushButton {
    background-color: #555555;
    color: #f0f0f0;
    border: none;
    border-radius: 12px;
    padding: 10px 14px;
    font-weight: bold;
}

QPushButton:hover {
    background-color: #666666;
}

QPushButton:disabled {
    background-color: #333333;
    color: #777777;
}

QPushButton[selected="true"] {
    background-color: #2f80ed;
    color: white;
}

QPushButton[selected="true"]:hover {
    background-color: #1f6fd1;
}

QPushButton[locked="true"] {
    background-color: #3a3a3a;
    color: #9a9a9a;
}

QPushButton[locked="true"]:hover {
    background-color: #464646;
}

QLineEdit#gameCell {
    background-color: #2f2f2f;
    color: #f0f0f0;
    border: 2px solid #777777;
    border-radius: 10px;
    font-weight: bold;
}

QLineEdit#gameCell[fixed="true"] {
    background-color: #3b4658;
    color: #dbeafe;
}
"""