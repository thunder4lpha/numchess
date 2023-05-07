from kandinsky import *
from ion import *
from time import sleep

TAILLE_CASE = 26
X_OFFSET = 5
Y_OFFSET = 8
B = color(255, 255, 255)
PB = color(222, 169, 82)
N = color(74, 113, 156)
PN = color(0, 0, 0)
S = [color(255, 0, 0), color(0, 255, 0)]
BG = color(49, 48, 49)
W = color(255,255,255)
SUR = color(246, 246, 105)

# 10 par 10
text = {
    "P": [0,224,496,496,496,224,224,496,496,1016,2044,2044,0],
    "T": [0,680,1016,1016,1016,496,496,496,496,1016,1016,2044,0],
    "C": [0,80,240,496,1016,952,920,960,480,224,1016,2044,0],
    "F": [0,64,64,224,496,496,1016,1016,496,224,1016,2044,0],
    "R": [0,64,224,64,744,2044,2044,1016,496,224,1016,2044,0],
    "D": [0,64,1092,1092,1772,2044,1016,1016,496,224,1016,2044,0],
}

EMPTY = "  "

def fond():
    fill_rect(0, 0, 320, 240, BG)

def etatPartie(text):    
    fill_rect(213, 0, 104, 240, BG)
    draw_string(text, 268-int(10*len(text)/2), 100, W, BG)

def drawBoard(board, joueur, p_coup=((-1,-1),(-1,-1))):
    # Plateau
    for x in range(8):
        for y in range(8):
            if x%2 == 0: c = (B if y%2==0 else N)
            else: c = (B if y%2==1 else N)
            if (x,y)==p_coup[0] or (x,y)==p_coup[1]:
                c = SUR
            fill_rect(x*TAILLE_CASE+X_OFFSET, y*TAILLE_CASE+Y_OFFSET, TAILLE_CASE, TAILLE_CASE, c)
    # Pièces
    if joueur == 2:
        board = list(reversed(board))
        n_board = []
        for col in board:
            n_board.append(list(reversed(col)))
        board = n_board[:]
    for y in range(8):
        for x in range(8):
            if board[y][x]!=EMPTY: dessinPiece(x, abs(y-7), board[y][x])

def dessinPiece(x, y, piece):
    """Dessine une pièce"""
    if piece[1]=="1": coul = PB
    else: coul = PN
    for c in range(len(text[piece[0]])):
        for l in range(len(text[piece[0]])):
            if text[piece[0]][l]>>c & 1:
                fill_rect(x*TAILLE_CASE+c*int(TAILLE_CASE/10)+X_OFFSET, y*TAILLE_CASE+l*int(TAILLE_CASE/10)+Y_OFFSET, int(TAILLE_CASE/10), int(TAILLE_CASE/10), coul)

def surligne(x, y, prev_x, prev_y, etat):
    if x != -1:
        x, y = x*TAILLE_CASE+X_OFFSET, y*TAILLE_CASE+Y_OFFSET
        # Surligne la nouvelle selection
        fill_rect(x, y, 1, TAILLE_CASE, S[etat])
        fill_rect(x, y, TAILLE_CASE, 1, S[etat])
        fill_rect(x, y+TAILLE_CASE-1, TAILLE_CASE, 1, S[etat])
        fill_rect(x+TAILLE_CASE-1, y, 1, TAILLE_CASE, S[etat])

    # Efface la précédente selection
    if prev_x != -1:
        if prev_x%2 == 0: c = (B if prev_y%2==0 else N)
        else: c = (B if prev_y%2==1 else N)
        
        prev_x, prev_y = prev_x*TAILLE_CASE+X_OFFSET, prev_y*TAILLE_CASE+Y_OFFSET
        fill_rect(prev_x, prev_y, 1, TAILLE_CASE, c)
        fill_rect(prev_x, prev_y, TAILLE_CASE, 1, c)
        fill_rect(prev_x, prev_y+TAILLE_CASE-1, TAILLE_CASE, 1, c)
        fill_rect(prev_x+TAILLE_CASE-1, prev_y, 1, TAILLE_CASE, c)

def promotion(joueur):
    joueur = str(joueur)
    # Ecran fond selection
    x_offset = 2*26
    y_offset = 3*26
    fill_rect(x_offset+X_OFFSET, y_offset+Y_OFFSET-5, 109, 62, BG)
    dessinPiece(3, 4, "C"+joueur)
    draw_string("2", x_offset+X_OFFSET+10, y_offset+Y_OFFSET+26+5, W, BG)
    dessinPiece(5, 4, "F"+joueur)
    draw_string("3", x_offset+X_OFFSET+2*26+10, y_offset+Y_OFFSET+26+5, W, BG)
    dessinPiece(3, 3, "T"+joueur)
    draw_string("0", x_offset+X_OFFSET+10, y_offset+Y_OFFSET+5, W, BG)
    dessinPiece(5, 3, "D"+joueur)
    draw_string("1", x_offset+X_OFFSET+2*26+10, y_offset+Y_OFFSET+5, W, BG)

    while True:
        if keydown(KEY_TWO):
            return "C"
        elif keydown(KEY_THREE):
            return "F"
        elif keydown(KEY_ZERO):
            return "T"
        elif keydown(KEY_ONE):
            return "D"
        sleep(0.05)


def choixCase(x, y, sur):
    f_x, f_y = (x, y)if sur else (-1,-1)
    p_x, p_y = x, y
    if not sur: surligne(x, y, -1, -1, 0)
    valid = False
    while not valid:
        if keydown(KEY_DOWN): y += 1
        elif keydown(KEY_UP): y -= 1
        elif keydown(KEY_LEFT): x -= 1
        elif keydown(KEY_RIGHT):  x += 1
        if keydown(KEY_OK): valid = True

        if y < 0: y = 7
        elif y >= 8: y = 0
        if x < 0: x = 7
        elif x >= 8: x = 0

        if (p_x, p_y) != (x, y):
            surligne((x if (x, y)!=(f_x,f_y)else -1), y, (p_x if(p_x,p_y)!=(f_x,f_y)else -1), p_y, valid)
            p_x, p_y = x, y
        sleep(0.08) #! CHANGER SUR LA CALCULATRICE A 0.08
    return x, y