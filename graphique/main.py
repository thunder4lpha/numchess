# affichage des pièces https://workshop.numworks.com/python/schraf/chess2
from math import sqrt
import graphique as graph
from time import sleep

#TODO Optimiser l'espace que prend le programme
#* Implémentation roque
#* Promotion des pions

#TODO En passant
#TODO Meilleur visibilité du surlignage

EMPTY = "  "

def coordToChess(coord):
    x = str(chr(coord[0]+97))
    y = str(coord[1]+1)
    return x+y

def chessToCoord(coord):
    x = ord(coord[0])-ord('a')
    y = ord(coord[1])-ord('1')
    return x, y

def renvCoord(coord, hoz=False):
    if hoz:
        return (abs(coord[0]-7), coord[1])
    return (coord[0], abs(coord[1]-7))

#! ############### !#
#!  GESTION PARTIE !#
#! ############### !#
class Partie():
    def __init__(s):
        # 1 : roque blanc 2 : g roque blanc 3 : roque noir 4 : g roque noir
        s.roques = [True for i in "_"*4]
        s.board = s.initBoard()
        s.joueur = 1
        s.p_coup = ((-1,-1),(-1,-1))

    def initBoard(s) -> list:
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
        board = list(reversed(board))
        return board

    # FONCTION DE VÉRIFICATIONS
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
    # FONCTION DE VÉRIFICATIONS

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
            #TODO Optimiser en utilisant un tableau des cases à échanger
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
            # Vérification du déroque
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

    def verifMat(s, board):
        for col in range(8):
            for row in range(8):
                if board[col][row][1]==str(s.joueur) and len(s.coupValide(board, board[col][row], (row, col)))!=0:
                    return False                    
        return True

    def verifEchec(s, board, x, y, joueur):
        # Vert and Hor check
        moves = [[1,0],[0,1],[-1,0],[0,-1]]
        for m in moves:
            x1, y1 = x+m[0], y+m[1]
            while s.onBoard(x1, y1):
                if board[y1][x1][1]!=joueur and (board[y1][x1][0] in ["T","D"] or (board[y1][x1][0]=="R" and int(sqrt((x1-x)**2+(y1-y)**2))<2)):
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
                if board[y1][x1][1]!=joueur and (board[y1][x1][0] in ["F","D"] or (board[y1][x1][0]=="R" and int(sqrt((x1-x)**2+(y1-y)**2))<2)):
                    return False
                if board[y1][x1] != EMPTY:
                    break;
                x1 += m[0]
                y1 += m[1]
        # Cavalier check
        moves = [[2,-1],[-2,1],[-1,2],[1,2],[1,-2],[-1,-2],[2,1],[-2,-1]]
        for m in moves:
            if s.onBoard(x+m[0], y+m[1]) and board[y+m[1]][x+m[0]][0]=="C" and board[y+m[1]][x+m[0]][1]!=joueur:
                return False
        # Pion check
        moves = [[-1,1],[1,1]]
        for m in moves:
            if s.onBoard(x+m[0], y+m[1]) and board[y+m[1]][x+m[0]][0]=="P" and board[y+m[1]][x+m[0]][1]!=joueur:
                return False
        return True

    def coupValide(s, board, piece, choix):
        # Renverser le plateau si c'est un coup des noirs
        if piece[1] == "2":
            board = list(reversed(board))
            choix = renvCoord(choix)

        valid = []
        # Pion
        if piece[0]=="P":
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
        elif piece[0]=="T":
            # Vertical
            for i in s.mVert(board, choix, True):
                valid.append(i)
            # Horizontal
            for i in s.mHorz(board, choix):
                valid.append(i)
        # Cavalier
        elif piece[0]=="C":
            moves = [[2,-1],[-2,1],[-1,2],[1,2],[1,-2],[-1,-2],[2,1],[-2,-1]]
            for m in moves:
                if s.onBoard(choix[0]+m[0], choix[1]+m[1]) and board[choix[1]+m[1]][choix[0]+m[0]][1] != piece[1]:
                    valid.append((choix[0]+m[0], choix[1]+m[1]))
        # Fou
        elif piece[0]=="F":
            # Diagonales
            for i in s.mDiag(board, choix):
                valid.append(i)
        # Dame
        elif piece[0]=="D":
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
        elif piece[0]=="R":
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
            n_board = [[case for case in col]for col in board]    # Création d'un nouveau tableau pour la simulation
            n_board = s.deplace(n_board, choix, i, False)           # Simulation du coup
            rx, ry = s.posRoi(n_board, piece[1])

            valid = False
            if i != "O-O" and i != "O-O-O" and s.verifEchec(n_board, rx, ry, piece[1]):
                valid = True
            # Vérification roque
            elif i == "O-O" and all([s.verifEchec(n_board, rx-x, ry, piece[1])for x in range(3)]):
                valid = True
            # Vérification grand roque
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
        return n_valid

    def choixCoup(s):
        # Choix du coup
        while True:
            # Choix de la pièce à déplacer
            x, y = 4, 4
            while True:
                x, y = graph.choixCase(x, y, False) # X Y pour tracking curseur
                choix_p = (renvCoord((x, y))if s.joueur==1 else renvCoord((x, y), True))
                if s.board[choix_p[1]][choix_p[0]][1] == str(s.joueur):
                    break
            graph.surligne(x, y, -1, -1, 1)

            coups = s.coupValide(s.board, s.board[choix_p[1]][choix_p[0]], choix_p)
            sleep(0.1)
            choix_c = graph.choixCase(x, y, True)
            choix_c = coordToChess((renvCoord(choix_c)if s.joueur==1 else renvCoord(choix_c, True)))

            # Roques
            choix = choix_c
            if s.joueur == 1:
                if choix == "g1" and s.roques[0]:
                    choix = "O-O"
                elif choix == "c1" and s.roques[1]:
                    choix = "O-O-O"
            elif s.joueur == 2:
                if choix == "g8" and s.roques[2]:
                    choix = "O-O"
                elif choix == "c8" and s.roques[3]:
                    choix = "O-O-O"
            if choix in coups:
                break
            graph.drawBoard(s.board, s.joueur, s.p_coup)
        s.board = s.deplace(s.board, choix_p, choix, True)

        # Vérification promotion de pion
        col = (0 if s.joueur==2 else 7)
        for row in range(8):
            if s.board[col][row] == "P"+str(s.joueur):
                n_piece = graph.promotion(s.joueur)
                s.board[col][row] = n_piece+str(s.joueur)
        # Changement de main
        s.joueur = s.joueur%2+1

        # Vérification de l'état de la partie
        rx, ry = s.posRoi(s.board, str(s.joueur))
        echec = not s.verifEchec(s.board, rx, ry, str(s.joueur))
        mat = s.verifMat(s.board)
        if echec and mat:
            text="Mat"
        elif echec:
            text="Echec"
        elif mat:
            text="Pat"
        else:
            text=""
        graph.etatPartie(text)

        if s.joueur==1:
            s.p_coup=(renvCoord(choix_p),renvCoord(chessToCoord(choix_c)))
        else:
            s.p_coup=(renvCoord(choix_p,True),renvCoord(chessToCoord(choix_c),True))

    def jouer(s):
        graph.fond()
        while True:
            graph.drawBoard(s.board, s.joueur, s.p_coup)
            s.choixCoup()
            sleep(0.5)
partie = Partie()
partie.jouer()