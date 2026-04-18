import json


def load_boards(filename):
    with open(filename, "r", encoding="utf-8") as file:
        data = json.load(file)
        return data["boards"]


def row_sum(board, n):
    sum_row = 0
    for i in board[n]:
        sum_row += i
    return sum_row


def col_sum(board, n):
    sum_col = 0
    for i in board:
        sum_col += i[n]
    return sum_col


def main_diag_sum(board):
    sum_main_diag = 0
    for i in range(len(board)):
        sum_main_diag += board[i][i]
    return sum_main_diag


def side_diag_sum(board):
    sum_side_diag = 0
    n = len(board)
    for i in range(len(board)):
        sum_side_diag += board[i][n - 1 - i]
    return sum_side_diag


def check_magic_square(board):
    n = len(board)
    target = n * (n * n + 1) // 2

    for i in range(n):
        if row_sum(board, i) != target:
            return False

    for i in range(n):
        if col_sum(board, i) != target:
            return False

    if main_diag_sum(board) != target:
        return False

    if side_diag_sum(board) != target:
        return False

    return True


def numbers_in_range(board):
    n = len(board)

    for row in board:
        for num in row:
            if num < 1 or num > n * n:
                return False

    return True


def has_duplicates(board):
    numbers = []

    for row in board:
        for num in row:
            if num in numbers:
                return True
            numbers.append(num)

    return False

def load_progress(filename):
    try:
        with open(filename, "r", encoding="utf-8") as file:
            data = json.load(file)
        
            if "coins" not in data:
                data["coins"] = 0
            if "unlocked_4x4" not in data:
                data["unlocked_4x4"] = False
            if "unlocked_5x5" not in data:
                data["unlocked_5x5"] = False
            if "games_played" not in data:
                data["games_played"] = 0
            if "games_won" not in data:
                data["games_won"] = 0

            return data
            
    except FileNotFoundError:
        return {
            "coins": 0,
            "unlocked_4x4": False,
            "unlocked_5x5": False,
            "games_played": 0,
            "games_won": 0
        }


def save_progress(filename, data):
    with open(filename, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

