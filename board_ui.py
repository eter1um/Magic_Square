from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont


def clear_layout(layout):
    while layout.count():
        item = layout.takeAt(0)
        widget = item.widget()
        child_layout = item.layout()

        if widget is not None:
            widget.deleteLater()
        elif child_layout is not None:
            clear_layout(child_layout)


def build_game_board(grid, board):
    clear_layout(grid)

    cells = []
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

    return cells


def get_board_from_inputs(cells, size):
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