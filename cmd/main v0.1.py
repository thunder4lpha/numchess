# à partir du code de  schraf
# https://workshop.numworks.com/python/schraf/chess2

# from kandinsky import *
# from ion import *
from time import sleep

#TODO Optimiser l'espace que prend le programme
#TODO Dev la partie graphique

EMPTY = "  "

def coordToChess(coord):
    x = str(chr(coord[0]+97))
    y = str(abs(coord[1]-8))
    return x+y

def initBoard() -> list:
    """Création du plateau de jeu

    Returns
    -------
    list
        plateau de jeu
    """
    board = [
        ["T2","C2","F2","D2","R2","F2","C2","T2"],
        ["P2","P2","P2","P2","P2","P2","P2","P2"],
        ["  ","  ","  ","  ","  ","  ","  ","  "],
        ["  ","  ","  ","  ","  ","  ","  ","  "],
        ["  ","  ","  ","  ","  ","  ","  ","  "],
        ["  ","  ","  ","  ","  ","  ","  ","  "],
        ["P1","P1","P1","P1","P1","P1","P1","P1"],
        ["T1","C1","F1","D1","R1","F1","C1","T1"]
    ]
    return board

def draw(board):
    """Affiche le plateau de jeu
    """
    for row in board:
        print(" ".join(row))
    pass


def coupValid(board, piece, choix):
    # Renverser le plateau si c'est un coup des noirs
    if piece[1] == "2":
        board = list(reversed(board))
        choix = (choix[0], abs(choix[1]-7))
        draw(board)

    print(piece, choix)

    valid = []

    # Lambdas
    m_vert = lambda dist : [(choix[0], choix[1]-i) for i in range(1,dist+1)if board[choix[1]-i][choix[0]]==EMPTY]

    match piece[0]:
        # Pion
        case "P":
            # Une case vers l'av
            if choix[1]-1 >= 0 and board[choix[1]-1][choix[0]]==EMPTY:
                valid.append((choix[0], choix[1]-1))
            # Manger
            if board[choix[1]-1][choix[0]-1][1] != (piece[1] and " ") and choix[0]-1 >= 0 and choix[1]-1 >= 0:
                valid.append((choix[0]-1, choix[1]-1))
            if board[choix[1]-1][choix[0]+1][1] != (piece[1] and " ") and choix[0]+1 < 8 and choix[1]-1 >= 0:
                valid.append((choix[0]+1, choix[1]-1))
            # Deux cases vers l'av
            if choix[1]==6:
                for i in m_vert(2):
                    valid.append(i)
            # En passant

        case "T":
            # Mouvement avant
            dist = abs((choix[1]-7) - 8)
            print(dist)
            for i in m_vert(dist):
                valid.append(i)
                

    valid = list(set(valid))
    
    # Annule le renversement
    if piece[1] == "2":
        for i in range(len(valid)):
            valid[i] = (valid[i][0], abs(valid[i][1]-7))

    # Affiche les coups disponibles
    for i in valid:
        print(coordToChess(i))
    return valid

def choixCase(text):
    while True:
        choix = input(text)
        x, y = (ord(choix[0])-97), abs(int(choix[1])-8)
        if 0 <= x < 8 and 0 <= y < 8:
            break

    return x, y

def choixMove(board):
    """Choix du coup à faire

    Parameters
    ----------
    board : _type_
        plateau de jeu
    """
    while True:
        choix_p = choixCase("Choisis une pièce: ")
        coups = coupValid(board, board[choix_p[1]][choix_p[0]], choix_p)
        choix_c = choixCase("Choisis un coup: ")
        if choix_c in coups:
            break

    board[choix_c[1]][choix_c[0]] = board[choix_p[1]][choix_p[0]]
    board[choix_p[1]][choix_p[0]] = EMPTY

    return board

def jouer():
    board = initBoard()
    while True:
        draw(board)
        board = choixMove(board)

if __name__ == "__main__":
    jouer()