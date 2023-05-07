# à partir du design de schraf
# https://workshop.numworks.com/python/schraf/chess2

# from kandinsky import *
# from ion import *

#TODO Optimiser l'espace que prend le programme
#TODO Dev la partie graphique

#* Rework du système de coordonnées pour plus simple
#* Déplacements pions (manque prise en passant)
#* Déplacements tours
#* Déplacements fous
#* Déplacements dame
#* Déplacements roi (sans echec)

# TODO système d'echec

EMPTY = "  "

def coordToChess(coord):
    x = str(chr(coord[0]+97))
    y = str(coord[1]+1)
    return x+y

def chessToCoord(coord):
    x = ord(coord[0])-ord('a')
    y = ord(coord[1])-ord('1')
    print(x, y)
    return x, y

def initBoard() -> list:
    """Création du plateau de jeu

    Returns
    -------
    list
        plateau de jeu
    """
    board = [
        ["T2","  ","  ","  ","R2","  ","  ","T2"],
        ["P2","P2","P2","P2","P2","P2","P2","P2"],
        ["  ","  ","  ","  ","  ","  ","  ","  "],
        ["  ","  ","  ","  ","  ","  ","  ","  "],
        ["  ","  ","  ","  ","  ","  ","  ","  "],
        ["  ","  ","  ","  ","  ","  ","  ","  "],
        ["P1","P1","P1","P1","P1","P1","P1","P1"],
        ["T1","  ","  ","  ","R1","  ","  ","T1"]
    ]
    board = list(reversed(board))
    return board

def draw(board):
    """Affiche le plateau de jeu
    """
    board = list(reversed(board))
    i = 8
    for row in board:
        print(i, end="   ")
        print(" ".join(row))
        i -= 1
    print("    a  b  c  d  e  f  g  h")
    pass

def choixCase(text):
    while True:
        choix = input(text)
        if ('a' <= choix[0] <= 'h' and "1" <= choix[1] <= "8") or choix == "O-O" or choix == "O-O-O":
            break

    return choix



# FONCTION DE VÉRIFICATIONS
def mVert(board, choix, mange, dist=7, arriere=True):
    valid = []
    arr = False
    for _ in range(2):
        for i in range(1, dist+1):
            if arr:
                i = -i
            if (choix[1]+i >= 8 if not arr else choix[1]+i < 0):
                break
            if board[choix[1]+i][choix[0]]==EMPTY:
                valid.append((choix[0], choix[1]+i))
            elif mange and board[choix[1]+i][choix[0]][1] != board[choix[1]][choix[0]][1]:
                valid.append((choix[0], choix[1]+i))
                break
            else:
                break
        if not arriere:
            break
        arr = True
    return valid

def mHorz(board, choix, dist=7):
    valid = []
    gauche = False
    for _ in range(2):
        for i in range(1, dist+1):
            if gauche:
                i = -i
            if (choix[0]+i >= 8 if not gauche else choix[0]+i < 0):
                break
            if board[choix[1]][choix[0]+i]==EMPTY:
                valid.append((choix[0]+i, choix[1]))
            elif board[choix[1]][choix[0]+i][1] != board[choix[1]][choix[0]][1]:
                valid.append((choix[0]+i, choix[1]))
                break
            else:
                break
        gauche = True
    return valid

def mDiag(board, choix, dist=7):
    valid = []
    bas = False
    gauche = False
    for w in range(4):
        for i in range(1, dist+1):
            if gauche: a=-i; b=i
            else: a=i; b=i
            if bas: a=-a; b=-b

            if choix[0]+a >= 8 or choix[1]+b >= 8 or choix[0]+a < 0 or choix[1]+b < 0:
                break
            if board[choix[1]+b][choix[0]+a]==EMPTY:
                valid.append((choix[0]+a, choix[1]+b))
            elif board[choix[1]+b][choix[0]+a][1] != board[choix[1]][choix[0]][1]:
                valid.append((choix[0]+a, choix[1]+b))
                break
            else:
                break
        bas = not bas
        if w == 1:
            gauche = True
    return valid
# FONCTION DE VÉRIFICATIONS


def coupValide(board, piece, choix):
    """Renvoie les coups disponibles pour un pièce choisie

    Parameters
    ----------
    board : list
        plateau de jeu
    piece : string
        la pièce
    choix : tuple(int)
        coordonnées de la pièce

    Returns
    -------
    list
        coups valides
    """
    global roques


    # Renverser le plateau si c'est un coup des noirs
    if piece[1] == "2":
        board = list(reversed(board))
        choix = (choix[0], abs(choix[1]-7))

    print(piece, choix)
    valid = []
    match piece[0]:
        # Pion
        case "P":
            # Avancer
            for i in mVert(board, choix, False, 1, False):
                valid.append(i)
            # Manger
            if choix[0]-1 >= 0 and choix[1]+1 < 8 and board[choix[1]+1][choix[0]-1][1] == str(int(piece[1])%2+1):
                valid.append((choix[0]-1, choix[1]+1))
            if choix[0]+1 < 8 and choix[1]+1 < 8 and board[choix[1]+1][choix[0]+1][1] == str(int(piece[1])%2+1):
                valid.append((choix[0]+1, choix[1]+1))
            # Deux cases vers l'av
            if choix[1]==1:
                for i in mVert(board, choix, False, 2, False):
                    valid.append(i)
            # En passant
        # Tour
        case "T":
            # Vertical
            for i in mVert(board, choix, True):
                valid.append(i)
            # Horizontal
            for i in mHorz(board, choix):
                valid.append(i)
        # Fou
        case "F":
            # Diagonales
            for i in mDiag(board, choix):
                valid.append(i)
        # Dame
        case "D":
            # Vertical
            for i in mVert(board, choix, True):
                valid.append(i)
            # Horizontal
            for i in mHorz(board, choix):
                valid.append(i)
            # Diagonales
            for i in mDiag(board, choix):
                valid.append(i)
        # Roi
        case "R":
            # Vertical
            for i in mVert(board, choix, True, 1):
                valid.append(i)
            # Horizontal
            for i in mHorz(board, choix, 1):
                valid.append(i)
            # Diagonales
            for i in mDiag(board, choix, 1):
                valid.append(i)
            # Petit roque
            if (board[0][5] and board[0][6])==EMPTY and roques[(int(piece[1])-1)*2]:
                valid.append("O-O")
            # Grand roque
            if ("".join(board[0][1:3+1])==3*EMPTY) and roques[(int(piece[1])-1)*2+1]:
                valid.append("O-O-O")

    valid = list(set(valid))
    
    # Annule le renversement
    if piece[1] == "2":
        for i in range(len(valid)):
            if type(valid[i]) != str:
                valid[i] = (valid[i][0], abs(valid[i][1]-7))

    # Affiche les coups disponibles
    n_valid = []
    for i in valid:
        if type(i) == tuple:
            i = coordToChess(i)
        n_valid.append(i)
        print(n_valid[-1], end=" ")
    print()
    return n_valid

def choixMove(board):
    """Choix du coup à effectuer

    Parameters
    ----------
    board : list
        plateau de jeu

    Returns
    -------
    list
        plateau de jeu
    """
    global roques

    while True:
        choix_p = chessToCoord(choixCase("Choisis une pièce: "))
        coups = coupValide(board, board[choix_p[1]][choix_p[0]], choix_p)
        choix_c = choixCase("Choisis un coup: ")
        if choix_c in coups:
            break
    # Petit roque
    piece = board[choix_p[1]][choix_p[0]]
    if choix_c == "O-O":
        #TODO Optimiser en utilisant un tableau des cases à échanger
        nb = (0 if piece[1]=="1" else 7)
        board[nb][6] = ("R1" if piece[1]=="1" else "R2")
        board[nb][5] = ("T1" if piece[1]=="1" else "T2")
        board[nb][4] = EMPTY
        board[nb][7] = EMPTY
        roques[(int(piece[1])-1)*2], roques[(int(piece[1])-1)*2+1] = False, False
    # Grand roque
    elif choix_c == "O-O-O":
        nb = (0 if piece[1]=="1" else 7)
        board[nb][2] = ("R1" if piece[1]=="1" else "R2")
        board[nb][3] = ("T1" if piece[1]=="1" else "T2")
        board[nb][0] = EMPTY
        board[nb][4] = EMPTY
        roques[(int(piece[1])-1)*2], roques[(int(piece[1])-1)*2+1] = False, False
    else:
        # Vérification du déroque
        if piece=="R1":
            roques[0], roques[1] = False, False
        elif piece=="R2":
            roques[2], roques[3] = False, False
        if choix_p[1]==0:
            if piece=="T1": roques[1] = False
            elif piece=="T2": roques[3] = False
        elif choix_p[1]==7:
            if piece=="T1": roques[0] = False
            elif piece=="T2": roques[2] = False

        x, y = chessToCoord(choix_c)
        board[y][x] = board[choix_p[1]][choix_p[0]]
        board[choix_p[1]][choix_p[0]] = EMPTY

    return board

def jouer():
    board = initBoard()
    while True:
        draw(board)
        board = choixMove(board)

if __name__=="__main__":
    # 1 : roque blanc 2 : g roque blacn 3 : roque noir 4 : g roque noir
    roques = [True for i in "_"*4]

    jouer()