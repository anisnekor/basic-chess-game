import pygame
import chess
import random

pygame.init()

# Configuration de l'écran
largeur_ecran = 480
hauteur_ecran = 480
ecran = pygame.display.set_mode((largeur_ecran, hauteur_ecran))
pygame.display.set_caption("Jeu d'échecs")

# Couleurs
MARRON_CLAIR = (237, 235, 189)  # Couleur marron clair pour les cases claires
MARRON_FONCE = (168, 124, 61)   # Couleur marron foncé pour les cases sombres

# Taille des cases
taille_case = largeur_ecran // 8

# Charger les images des pièces et ajuster leur taille pour s'adapter aux cases
images_pieces = {
    "P": pygame.image.load("pieces/white_pawn.png"),
    "N": pygame.image.load("pieces/white_knight.png"),
    "B": pygame.image.load("pieces/white_bishop.png"),
    "R": pygame.image.load("pieces/white_rook.png"),
    "Q": pygame.image.load("pieces/white_queen.png"),
    "K": pygame.image.load("pieces/white_king.png"),
    "p": pygame.image.load("pieces/black_pawn.png"),
    "n": pygame.image.load("pieces/black_knight.png"),
    "b": pygame.image.load("pieces/black_bishop.png"),
    "r": pygame.image.load("pieces/black_rook.png"),
    "q": pygame.image.load("pieces/black_queen.png"),
    "k": pygame.image.load("pieces/black_king.png"),
}

for nom_piece in images_pieces:
    images_pieces[nom_piece] = pygame.transform.scale(images_pieces[nom_piece], (taille_case, taille_case))

# Générer le plateau
def dessiner_plateau():
    for rang in range(8):
        for colonne in range(8):
            couleur = MARRON_CLAIR if (rang + colonne) % 2 == 0 else MARRON_FONCE
            pygame.draw.rect(ecran, couleur, pygame.Rect(colonne * taille_case, rang * taille_case, taille_case, taille_case))

# Dessiner les pièces
def dessiner_pieces(plateau, case_selectionnee):
    for rang in range(8):
        for colonne in range(8):
            case = chess.square(colonne, 7 - rang)
            piece = plateau.piece_at(case)
            if piece is not None:
                nom_piece = piece.symbol()
                x = colonne * taille_case
                y = rang * taille_case
                img = images_pieces[nom_piece]
                ecran.blit(img, (x, y))
                if case == case_selectionnee:
                    pygame.draw.rect(ecran, (0, 255, 0), pygame.Rect(x, y, taille_case, taille_case), 4)

# Fonction pour gérer les déplacements des pièces
def gerer_deplacement(plateau, case_depart, case_arrivee):
    deplacement = chess.Move(case_depart, case_arrivee)
    if deplacement in plateau.legal_moves:
        plateau.push(deplacement)

# Fonction pour obtenir la case du plateau à partir des coordonnées de la souris
def obtenir_case_de_souris(pos):
    colonne = pos[0] // taille_case
    rang = 7 - pos[1] // taille_case
    return chess.square(colonne, rang)

# Fonction pour que l'ordinateur joue un coup aléatoire
def jouer_coup_ordinateur(plateau):
    coups_legaux = list(plateau.legal_moves)
    return random.choice(coups_legaux)

def main():
    ecran = pygame.display.set_mode((largeur_ecran, hauteur_ecran))
    pygame.display.set_caption("Jeu d'échecs")

    plateau = chess.Board()
    couleur_joueur = chess.WHITE
    couleur_ordinateur = chess.BLACK
    case_selectionnee = None
    partie_en_cours = True
    en_cours = True

    while en_cours:
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                en_cours = False

            if partie_en_cours and evenement.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                case = obtenir_case_de_souris(pos)
                piece = plateau.piece_at(case)

                if piece is not None and piece.color == couleur_joueur:
                    case_selectionnee = case
                elif case_selectionnee is not None:
                    gerer_deplacement(plateau, case_selectionnee, case)
                    case_selectionnee = None

        if partie_en_cours and plateau.turn == couleur_ordinateur:
            coup_ordinateur = jouer_coup_ordinateur(plateau)
            gerer_deplacement(plateau, coup_ordinateur.from_square, coup_ordinateur.to_square)

        ecran.fill((255, 255, 255))  # Remplir l'écran avec la couleur blanche
        dessiner_plateau()
        dessiner_pieces(plateau, case_selectionnee)
        pygame.display.update()
        pygame.time.delay(100)  # Ajouter un petit délai pour réduire l'utilisation du processeur

        if plateau.is_game_over():
            partie_en_cours = False

    pygame.quit()

if __name__ == "__main__":
    main()
