def update_weights_around_shot(board, x, y, ship_sizes, weights):
    max_ship_size = max(ship_sizes)

    # Define the range to update weights

    start_row = max(0, x - max_ship_size + 1)
    end_row = min(len(board), x + max_ship_size)
    
    start_col = max(0, y - max_ship_size + 1)
    end_col = min(len(board), y + max_ship_size)
    
    # Update weights within the range

    for i in range(start_row, end_row):
        for j in range(start_col, end_col):
            if board[i][j] == '.':
                weights[i][j] = 0  # Reset weight
                for ship_length in ship_sizes:
                    weights[i][j] += count_ship_placements(board, i, j, ship_length)

def count_ship_placements(board, i, j, ship_length):
    count = 0
    board_size = len(board)
    
    # Check horizontal placement to the right
    if j + ship_length <= board_size:
        if all(board[i][k] == '.' for k in range(j, j + ship_length)):
            count += 1
            
    # Check vertical placement downwards
    if i + ship_length <= board_size:
        if all(board[k][j] == '.' for k in range(i, i + ship_length)):
            count += 1

    return count