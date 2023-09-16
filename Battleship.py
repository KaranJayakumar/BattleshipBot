import random
def ShipLogic(round, yourMap, yourHp, enemyHp, p1ShotSeq, p1PrevHit, storage):
    x = random.randint(1,10)
    y = random.randint(1,10)

    curEnemyBoard = updateBoard(p1ShotSeq, p1PrevHit) 

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
