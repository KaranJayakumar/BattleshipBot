import random
def ShipLogic(round, yourMap, yourHp, enemyHp, p1ShotSeq, p1PrevHit, storage):
    x = random.randint(1,10)
    y = random.randint(1,10)

    curEnemyBoard = updateBoard(p1ShotSeq, p1PrevHit) 
    getShot(curEnemyBoard)
    return [x,y], storage

def updateBoard(p1ShotSeq, p1PrevHit):
    board = [["." for _ in range(10)] for _ in range(10)]
    p1Missed = []
    for coord in p1ShotSeq:
        if coord not in p1PrevHit:
            p1Missed.append(coord)

    for coord in p1PrevHit:
        board[coord[0]][coord[1]] = "H"

    for coord in p1Missed:
        board[coord[0]][coord[1]] = "M"

    return board 

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
    updateWeights(weights, board)
    return weights

def choose_shot(weights):
    max_weight = max(max(row) for row in weights)
    candidates = [(x, y) for x in range(10) for y in range(10) if weights[x][y] == max_weight]
    return random.choice(candidates)

def updateWeights(weights, board):
    for rowNo in range(0, 10, 1):
        for colNo in range(10):
            if(board[rowNo][colNo] == 'H'):
                if(isLoneHit(rowNo, colNo, board)):
                    updateLoneHit()
                else: 
                    updateConnectedHits(weights, board, rowNo, colNo)

def updateConnectedHits(weights, board, rowNo, colNo):
    # Define the directions (up, down, left, right)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for dx, dy in directions:
        x, y = rowNo + dx, colNo + dy
        connected_hits = 0  # Count of consecutive hits in line

        # Check if the adjacent square is within bounds and contains a hit
        while (0 <= x < 10) and (0 <= y < 10) and (board[x][y] == 'H'):
            connected_hits += 1
            x, y = x + dx, y + dy

        # If there are at least two consecutive hits in line
        if connected_hits >= 2:
            x, y = rowNo + dx, colNo + dy
            while (0 <= x < 10) and (0 <= y < 10) and (board[x][y] == 'H'):
                x, y = x + dx, y + dy

            # Update the weight of the next empty square in line
            if (0 <= x < 10) and (0 <= y < 10) and (board[x][y] == '.'):
                weights[x][y] += 1

def isLoneHit(rowNo, colNo, board):
    # Check if the hit is at the top-left corner
    if rowNo == 0 and colNo == 0:
        return (
            board[rowNo + 1][colNo] == '.' and
            board[rowNo][colNo + 1] == '.'
        )
    
    # Check if the hit is at the top-right corner
    if rowNo == 0 and colNo == 9:
        return (
            board[rowNo + 1][colNo] == '.' and
            board[rowNo][colNo - 1] == '.'
        )
    
    # Check if the hit is at the bottom-left corner
    if rowNo == 9 and colNo == 0:
        return (
            board[rowNo - 1][colNo] == '.' and
            board[rowNo][colNo + 1] == '.'
        )

    # Check if the hit is at the bottom-right corner
    if rowNo == 9 and colNo == 9:
        return (
            board[rowNo - 1][colNo] == '.' and
            board[rowNo][colNo - 1] == '.'
        )

    # Check if the hit is on the top edge (excluding corners)
    if rowNo == 0:
        return (
            board[rowNo + 1][colNo] == '.' and
            board[rowNo][colNo + 1] == '.' and
            board[rowNo][colNo - 1] == '.'
        )

    # Check if the hit is on the bottom edge (excluding corners)
    if rowNo == 9:
        return (
            board[rowNo - 1][colNo] == '.' and
            board[rowNo][colNo + 1] == '.' and
            board[rowNo][colNo - 1] == '.'
        )

    # Check if the hit is on the left edge (excluding corners)
    if colNo == 0:
        return (
            board[rowNo + 1][colNo] == '.' and
            board[rowNo - 1][colNo] == '.' and
            board[rowNo][colNo + 1] == '.'
        )

    # Check if the hit is on the right edge (excluding corners)
    if colNo == 9:
        return (
            board[rowNo + 1][colNo] == '.' and
            board[rowNo - 1][colNo] == '.' and
            board[rowNo][colNo - 1] == '.'
        )

    # Check if the hit is in the interior of the board
    return (
        board[rowNo + 1][colNo] == '.' and
        board[rowNo - 1][colNo] == '.' and
        board[rowNo][colNo + 1] == '.' and
        board[rowNo][colNo - 1] == '.'
    )

def updateLoneHit(weights, rowNo, colNo):
    # Define the directions (up, down, left, right)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for dx, dy in directions:
        x, y = rowNo + dx, colNo + dy

        # Check if the adjacent square is within bounds
        if 0 <= x < 10 and 0 <= y < 10:
            weights[x][y] +=  10  # Increase the weight for adjacent squares

def getShot(enemyBoard):
    ship_sizes = [2,2,3,3,5] 
    return choose_shot(calculate_weights(enemyBoard, ship_sizes))