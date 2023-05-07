# à partir du design de schraf
# https://workshop.numworks.com/python/schraf/chess2

# from kandinsky import *
# from ion import *
from math import sqrt

#TODO Optimiser l'espace que prend le programme
#TODO Dev la partie graphique

#* Déplacements cavalier
#* Système d'echec + clouage
#* Echec + roques
#TODO En passant

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

def draw(board):
    board = list(reversed(board))
    i = 8
    for row in board:
        print(i, end="   ")
        print(" ".join(row))
        i -= 1
    print("    a  b  c  d  e  f  g  h")
    pass

#! ############### !#
#!  GESTION PARTIE !#
#! ############### !#
class Partie():
    def __init__(s):
        # 1 : roque blanc 2 : g roque blanc 3 : roque noir 4 : g roque noir
        s.roques = [True for i in "_"*4]
        s.board = s.initBoard()
                #   Blancs Noirs
        s.echecs = [False, False]

    def initBoard(s) -> list:
        # board = [
        #     ["T2","C2","F2","D2","R2","F2","C2","T2"],
        #     ["P2","P2","P2","P2","P2","P2","P2","P2"],
        #     ["  ","  ","  ","  ","  ","  ","  ","  "],
        #     ["  ","  ","  ","  ","  ","  ","  ","  "],
        #     ["  ","  ","  ","  ","  ","  ","  ","  "],
        #     ["  ","  ","  ","  ","  ","  ","  ","  "],
        #     ["P1","P1","P1","P1","P1","P1","P1","P1"],
        #     ["T1","C1","F1","D1","R1","F1","C1","T1"]
        # ]
        board = [
            ["T2","C2","F2","  ","  ","F2","C2","  "],
            ["P2","P2","P2","P2","  ","  ","P2","P2"],
            ["  ","  ","  ","R2","  ","T2","  ","  "],
            ["  ","  ","  ","  ","  ","  ","  ","  "],
            ["  ","  ","  ","  ","  ","  ","  ","  "],
            ["  ","  ","  ","  ","P2","P2","  ","  "],
            ["P1","P1","P1","  ","P1","  ","P1","P1"],
            ["T1","  ","  ","  ","R1","  ","  ","T1"]
        ]
        board = list(reversed(board))
        return board

    def choixCase(s, text):
        while True:
            choix = input(text)
            if s.onBoard(ord(choix[0])-ord("a"), ord(choix[1])-ord("1")) or choix == "O-O" or choix == "O-O-O":
                break

        return choix

    # FONCTION DE VÉRIFICATIONS
    def mVert(s, board, choix, mange, dist=7, arriere=True):
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

    def mHorz(s, board, choix, dist=7):
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

    def mDiag(s, board, choix, dist=7):
        valid = []
        bas = False
        gauche = False
        for w in range(4):
            for i in range(1, dist+1):
                if gauche: a=-i; b=i
                else: a=i; b=i
                if bas: a=-a; b=-b

                if not s.onBoard(choix[0]+a, choix[1]+b):
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
    
    def onBoard(s, x, y):
        return (0 <= x < 8 and 0 <= y < 8)
    # FONCTION DE VÉRIFICATIONS

    def posRoi(s, board, nb):
        for col in range(8):
            for row in range(8):
                if board[col][row] == "R"+nb:
                    return row, col
        raise Exception("Bizarre", "Le roi a disparu")

    def deplace(s, board, choix_p, choix_c, definitif=False):
        # Petit roque
        piece = board[choix_p[1]][choix_p[0]]
        if choix_c == "O-O":
            #TODO Optimiser en utilisant un tableau des cases à échanger
            nb = (0 if piece[1]=="1" else 7)
            board[nb][6] = ("R1" if piece[1]=="1" else "R2")
            board[nb][5] = ("T1" if piece[1]=="1" else "T2")
            board[nb][4] = EMPTY
            board[nb][7] = EMPTY
            if definitif: s.roques[(int(piece[1])-1)*2], s.roques[(int(piece[1])-1)*2+1] = False, False
        # Grand roque
        elif choix_c == "O-O-O":
            nb = (0 if piece[1]=="1" else 7)
            board[nb][2] = ("R1" if piece[1]=="1" else "R2")
            board[nb][3] = ("T1" if piece[1]=="1" else "T2")

            board[nb][0] = EMPTY
            board[nb][4] = EMPTY
            if definitif: s.roques[(int(piece[1])-1)*2], s.roques[(int(piece[1])-1)*2+1] = False, False
        else:
            # Vérification du déroque
            if definitif:
                if piece=="R1":
                    s.roques[0], s.roques[1] = False, False
                elif piece=="R2":
                    s.roques[2], s.roques[3] = False, False
                if choix_p[1]==0:
                    if piece=="T1": s.roques[1] = False
                    elif piece=="T2": s.roques[3] = False
                elif choix_p[1]==7:
                    if piece=="T1": s.roques[0] = False
                    elif piece=="T2": s.roques[2] = False

            if definitif: x, y = chessToCoord(choix_c)
            else: x, y = choix_c[0], choix_c[1]
            board[y][x] = board[choix_p[1]][choix_p[0]]
            board[choix_p[1]][choix_p[0]] = EMPTY
        return board

    def verifEchec(s, board, x, y, nb):
        # Vert and Hor check
        moves = [[1,0],[0,1],[-1,0],[0,-1]]
        for m in moves:
            x1, y1 = x+m[0], y+m[1]
            while s.onBoard(x1, y1):
                if board[y1][x1][1]!=nb and (board[y1][x1][0] in ["T","D"] or (board[y1][x1][0]=="R" and int(sqrt((x1-x)**2+(y1-y)**2))<2)):
                    return False    
                if board[y1][x1] != EMPTY:
                    break;            
                x1 += m[0]
                y1 += m[1]
        # Diag check
        moves = [[1,1],[1,-1],[-1,1],[-1,-1]]
        for m in moves:
            x1, y1 = x+m[0], y+m[1]
            while s.onBoard(x1, y1):
                if board[y1][x1][1]!=nb and (board[y1][x1][0] in ["F","D"] or (board[y1][x1][0]=="R" and int(sqrt((x1-x)**2+(y1-y)**2))<2)):
                    return False
                if board[y1][x1] != EMPTY:
                    break;
                x1 += m[0]
                y1 += m[1]
        # Cavalier check
        moves = [[2,-1],[-2,1],[-1,2],[1,2],[1,-2],[-1,-2],[2,1],[-2,-1]]
        for m in moves:
            if s.onBoard(x+m[0], y+m[1]) and board[y+m[1]][x+m[0]][0]=="C" and board[y+m[1]][x+m[0]][1]!=nb:
                return False
        # Pion check
        moves = [[-1,1],[1,1]]
        for m in moves:
            if s.onBoard(x+m[0], y+m[1]) and board[y+m[1]][x+m[0]][0]=="P" and board[y+m[1]][x+m[0]][1]!=nb:
                return False
        return True


    def coupValide(s, board, piece, choix):
        # Renverser le plateau si c'est un coup des noirs
        if piece[1] == "2":
            board = list(reversed(board))
            choix = (choix[0], abs(choix[1]-7))

        valid = []
        match piece[0]:
            # Pion
            case "P":
                # Avancer
                for i in s.mVert(board, choix, False, 1, False):
                    valid.append(i)
                # Manger
                if s.onBoard(choix[0]-1, choix[1]+1) and board[choix[1]+1][choix[0]-1][1] == str(int(piece[1])%2+1):
                    valid.append((choix[0]-1, choix[1]+1))
                if s.onBoard(choix[0]+1, choix[1]+1) and board[choix[1]+1][choix[0]+1][1] == str(int(piece[1])%2+1):
                    valid.append((choix[0]+1, choix[1]+1))
                # Deux cases vers l'av
                if choix[1]==1:
                    for i in s.mVert(board, choix, False, 2, False):
                        valid.append(i)
                # En passant
            # Tour
            case "T":
                # Vertical
                for i in s.mVert(board, choix, True):
                    valid.append(i)
                # Horizontal
                for i in s.mHorz(board, choix):
                    valid.append(i)
            # Cavalier
            case "C":
                moves = [[2,-1],[-2,1],[-1,2],[1,2],[1,-2],[-1,-2],[2,1],[-2,-1]]
                for m in moves:
                    if s.onBoard(choix[0]+m[0], choix[1]+m[1]) and board[choix[1]+m[1]][choix[0]+m[0]][1] != piece[1]:
                        valid.append((choix[0]+m[0], choix[1]+m[1]))
            # Fou
            case "F":
                # Diagonales
                for i in s.mDiag(board, choix):
                    valid.append(i)
            # Dame
            case "D":
                # Vertical
                for i in s.mVert(board, choix, True):
                    valid.append(i)
                # Horizontal
                for i in s.mHorz(board, choix):
                    valid.append(i)
                # Diagonales
                for i in s.mDiag(board, choix):
                    valid.append(i)
            # Roi
            case "R":
                # Vertical
                for i in s.mVert(board, choix, True, 1):
                    valid.append(i)
                # Horizontal
                for i in s.mHorz(board, choix, 1):
                    valid.append(i)
                # Diagonales
                for i in s.mDiag(board, choix, 1):
                    valid.append(i)
                # Petit roque
                if (board[0][5] and board[0][6])==EMPTY and board[0][7]=="T"+piece[1] and s.roques[(int(piece[1])-1)*2]:
                    valid.append("O-O")
                # Grand roque
                if ("".join(board[0][1:3+1])==3*EMPTY) and board[0][0]=="T"+piece[1] and s.roques[(int(piece[1])-1)*2+1]:
                    valid.append("O-O-O")

        valid = list(set(valid))

        n_valid = []
        for i in valid:
            # Tri les coups dispo
            n_board = [[case for case in col]for col in board]    # Création d'un nouveau tableau pour la simulation
            n_board = s.deplace(n_board, choix, i, False)           # Simulation du coup
            rx, ry = s.posRoi(n_board, piece[1])
            draw(n_board)
            print("#"*10)
            valid = False
            if i != "O-O" and i != "O-O-O" and s.verifEchec(n_board, rx, ry, piece[1]):
                valid = True
            # Vérification roque
            elif i == "O-O" and all([s.verifEchec(n_board, rx-x, ry, piece[1])for x in range(3)]):
                valid = True
            # Vérification grand roque
            elif i == "O-O-O" and all([s.verifEchec(n_board, rx+x, ry, piece[1])for x in range(3)]):
                valid = True
            
            # Ajout du coup s'il est valide
            if valid:
                if type(i) == tuple:
                    # Annulation du renversement
                    if piece[1]=="2":
                        i = (i[0], abs(i[1]-7))
                    i = coordToChess(i)
                n_valid.append(i)
        n_valid = sorted(n_valid)
        print(*n_valid)
        return n_valid

    def choixCoup(s):
        while True:
            choix_p = chessToCoord(s.choixCase("Choisis une pièce: "))
            coups = s.coupValide(s.board, s.board[choix_p[1]][choix_p[0]], choix_p)
            choix_c = s.choixCase("Choisis un coup: ")
            if choix_c in coups:
                break
        s.board = s.deplace(s.board, choix_p, choix_c, True)

        for i in range(2):
            rx, ry = s.posRoi(s.board, str(i+1))
            s.echecs[i] = not s.verifEchec(s.board, rx, ry, str(i+1))

    def jouer(s):
        while True:
            draw(s.board)
            print(f"Blanc echec : {s.echecs[0]} | Noir echec : {s.echecs[1]}")
            s.choixCoup()

if __name__=="__main__":
    partie = Partie()
    partie.jouer()