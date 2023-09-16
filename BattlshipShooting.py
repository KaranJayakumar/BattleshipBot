def count_ship_placements(board, x, y, ship_length):
    # Count for horizontal and vertical placements
    horizontal_count, vertical_count = 0, 0

    # Check horizontal placement to the right
    if y + ship_length - 1 < len(board):
        horizontal_count = all(cell != 'M' for cell in board[x][y:y+ship_length])

    # Check vertical placement downwards
    if x + ship_length - 1 < len(board):
        vertical_count = all(board[i][y] != 'M' for i in range(x, x + ship_length))

    return horizontal_count + vertical_count

def calculate_weights(board, ship_sizes):
    weights = [[0 for _ in range(10)] for _ in range(10)]
    for x in range(10):
        for y in range(10):
            if board[x][y] == '.':
                for ship_length in ship_sizes:
                    weights[x][y] += count_ship_placements(board, x, y, ship_length)
    return weights

def choose_shot(weights):
    max_weight = max(max(row) for row in weights)
    candidates = [(x, y) for x in range(10) for y in range(10) if weights[x][y] == max_weight]
    return random.choice(candidates)

board = [['.' for _ in range(10)] for _ in range(10)]

# This is just a test to simulate some shots

# board[5][5] = 'M'
# board[5][6] = 'H'
# board[5][7] = 'H'
# ship_sizes = [2, 3, 3, 4, 5]  # Standard Battleship sizes

# weights = calculate_weights(board, ship_sizes)
# x, y = choose_shot(weights)
# print(f"Bot should shoot at ({x}, {y}) based on the calculated weights.")

