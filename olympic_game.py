import pygame
import random
import sqlite3
import emoji
import time
from colorama import Fore, Back, Style
import numpy as np

print(Fore.RED)

PLAYER_2_GAMEMODE = False
affichage_drapeau1, affichage_drapeau2 = False, False
nom1, nom2 = "", ""
nation1, nation2 = "", ""
nation_ai = ""
ordre_gagnant_nom = []
ordre_gagnant_pays = []

def accueil():
    global PLAYER_2_GAMEMODE, affichage_drapeau1, affichage_drapeau2, nom1, nom2, nation1, nation2, nation_ai

    # Reset les noms et pays choisis pour reset les choix à *RIEN* quand on recommence la boucle du jeu
    affichage_drapeau1, affichage_drapeau2 = False, False
    nom1, nom2 = "", ""
    nation1, nation2 = "", ""

    '''PLUGIN POUR METTRE DES EMOJIS DANS L'INTERPRÉTEUR'''
    medail1 = emoji.emojize(':1st_place_medal:')
    medail2 = emoji.emojize(':2nd_place_medal:')
    medail3 = emoji.emojize(':3rd_place_medal:')


    # création base de donnée
    connexion = sqlite3.connect("basetp.db")
    # Les données seront stockées dans basetp.db
    cursor = connexion.cursor()  # Création d'un curseur
    # requête de création d'une table participants
    requete = """CREATE TABLE IF NOT EXISTS participants(
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    nation TEXT NOT NULL, 
    nom TEXT NOT NULL,
    temps float)"""

    cursor.execute(requete)  # exécuter la requête
    connexion.commit()# Valider l'exécution de la requête

    cursor.execute("select*from participants")
    nb_participants = len(cursor.fetchall())
    connexion.commit()

    pygame.init()  # initialisation de tous les composants de pygame
    ecran = pygame.display.set_mode((550, 500))
    pygame.display.set_caption("Accueil")  # changer le texte de l'onglet

    coord_record = pygame.Rect(150, 230, 250, 50)
    coord_solo = pygame.Rect(150, 320, 250, 50)
    coord_qualification = pygame.Rect(150, 410, 250, 50)

    image_logo = pygame.image.load("logo1.png")  # methode pour charger une image
    image_logo = pygame.transform.scale(image_logo, (400, 250))

    lancement = True

    while lancement:
        ecran.fill((200, 250, 255))

        font = pygame.font.SysFont("Impact", 25, bold=False)

        # texte des trois boutons
        texte_r = font.render("record mondial", 10, (40, 40, 40))
        texte_s = font.render("solo", 10, (40, 40, 40))
        texte_q = font.render("qualifications", 10, (40, 40, 40))

        # rectangle qui sont les boutons
        pygame.draw.rect(ecran, (255, 85, 85), coord_record)
        pygame.draw.rect(ecran, (250, 200, 55), coord_solo)
        pygame.draw.rect(ecran, (85, 150, 80), coord_qualification)

        # placement du texte sur les boutons
        ecran.blit(texte_r, (198, 240))
        ecran.blit(texte_s, (250, 330))
        ecran.blit(texte_q, (203, 420))
        # place logo
        ecran.blit(image_logo, (80, 20))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # constante QUIT
                lancement = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if coord_record.collidepoint(pygame.mouse.get_pos()): # si on clique sur le bouton records
                    if nb_participants != 0:
                        '''PLUGIN POUR RENDRE LE TEXT DANS L'INTERPRÉTEUR BLEU POUR LE LEADERBOARD'''
                        print(Fore.BLUE)
                        print('records')
                        contenu = cursor.execute("SELECT id, nation, nom, temps from PARTICIPANTS ORDER BY temps DESC")
                        n = 0
                        for row in contenu:
                            if n == 0:
                                print(medail1 + ' temps: '+ str(row[3]) + ' secondes  nation: '+ row[1][:-4] + '  nom: '+ row[2])
                            elif n == 1:
                                print(medail2 + ' temps: '+ str(row[3]) + ' secondes  nation: '+ row[1][:-4] + '  nom: '+ row[2])
                            elif n == 2:
                                print(medail3 + ' temps: '+ str(row[3]) + ' secondes  nation: '+ row[1][:-4] + '  nom: '+ row[2])
                            else:
                                print(' temps: '+ str(row[3]) + ' secondes  nation: ' + row[1][:-4] + '  nom: ' +row[2])
                            n += 1
                        '''PLUGIN POUR RENDRE LE TEXT DANS L'INTERPRÉTEUR ROUGE POUR LES MESSAGES DE GESTION D'ERREURS'''
                        print(Fore.RED)
                if coord_solo.collidepoint(pygame.mouse.get_pos()): # si on clique sur le bouton solo
                    lancement = False
                    PLAYER_2_GAMEMODE = False
                    nations()


                elif coord_qualification.collidepoint(pygame.mouse.get_pos()): # si on clique sur le bouton qualification
                    lancement = False
                    PLAYER_2_GAMEMODE = True
                    nations()

    connexion.close()
    pygame.quit()  # desinitailiser les composants de pygame

def nations():
    global PLAYER_2_GAMEMODE, affichage_drapeau1, affichage_drapeau2, nom1, nom2, nation1, nation2, nation_ai

    pygame.init()  # initialisation de tous les composants de pygame
    ecran = pygame.display.set_mode((550, 500))
    pygame.display.set_caption("Nations")  # changer le texte de l'onglet

    drapeau_etats_unis = pygame.image.load("etats_unis.png")
    drapeau_canada = pygame.image.load("canada.png")
    drapeau_fidji = pygame.image.load("fidji.png")
    drapeau_vietnam = pygame.image.load("vietnam.png")
    drapeau_kirghizistan = pygame.image.load("kirghizistan.png")
    drapeau_zimbabwe = pygame.image.load("zimbabwe.png")
    drapeau_togo = pygame.image.load("togo.png")
    drapeau_bielorussie = pygame.image.load("bielorussie.png")
    drapeau_liechtenstein = pygame.image.load("liechtenstein.png")

    drapeau_canada = pygame.transform.scale(drapeau_canada, (125, 65))
    drapeau_etats_unis = pygame.transform.scale(drapeau_etats_unis, (125, 65))
    drapeau_fidji = pygame.transform.scale(drapeau_fidji, (125, 65))
    drapeau_vietnam = pygame.transform.scale(drapeau_vietnam, (125, 65))
    drapeau_kirghizistan = pygame.transform.scale(drapeau_kirghizistan, (125, 65))
    drapeau_liechtenstein = pygame.transform.scale(drapeau_liechtenstein, (125, 65))
    drapeau_zimbabwe = pygame.transform.scale(drapeau_zimbabwe, (125, 65))
    drapeau_togo = pygame.transform.scale(drapeau_togo, (125, 65))
    drapeau_bielorussie = pygame.transform.scale(drapeau_bielorussie, (125, 65))

    # Visualisation drapeau choisi
    drapeau_canada_petit = pygame.transform.scale(drapeau_canada, (80, 42))
    drapeau_etats_unis_petit = pygame.transform.scale(drapeau_etats_unis, (80, 42))
    drapeau_fidji_petit = pygame.transform.scale(drapeau_fidji, (80, 42))
    drapeau_vietnam_petit = pygame.transform.scale(drapeau_vietnam, (80, 42))
    drapeau_kirghizistan_petit = pygame.transform.scale(drapeau_kirghizistan, (80, 42))
    drapeau_liechtenstein_petit = pygame.transform.scale(drapeau_liechtenstein, (80, 42))
    drapeau_zimbabwe_petit = pygame.transform.scale(drapeau_zimbabwe, (80, 42))
    drapeau_togo_petit = pygame.transform.scale(drapeau_togo, (80, 42))
    drapeau_bielorussie_petit = pygame.transform.scale(drapeau_bielorussie, (80, 42))

    surface_drapeau_canada = pygame.Rect(47, 80, 125, 65)
    surface_drapeau_etats_unis = pygame.Rect(213, 80, 125, 65)
    surface_drapeau_fidji = pygame.Rect(378, 80, 125, 65)
    surface_drapeau_vietnam = pygame.Rect(47, 180, 125, 65)
    surface_drapeau_kirghizistan = pygame.Rect(213, 180, 125, 65)
    surface_drapeau_liechtenstein = pygame.Rect(378, 180, 125, 65)
    surface_drapeau_zimbabwe = pygame.Rect(47, 280, 125, 65)
    surface_drapeau_togo = pygame.Rect(213, 280, 125, 65)
    surface_drapeau_bielorussie = pygame.Rect(378, 280, 125, 65)


    font = pygame.font.SysFont("Futura", 30, bold=True)
    font2 = pygame.font.SysFont("Futura", 16, bold=False)
    font3 = pygame.font.SysFont("Futura", 12, bold=True)

    titre_nation = font.render("CHOIX DE LA NATION", 10, (40, 40, 40))

    canada = font3.render("CANADA", 10, (40, 40, 40))
    etats_unis = font3.render("ÉTATS-UNIS", 10, (40, 40, 40))
    fidji = font3.render("FIDJI", 10, (40, 40, 40))
    vietnam = font3.render("VIETNAM", 10, (40, 40, 40))
    kirghizistan = font3.render("KIRGHIZISTAN", 10, (40, 40, 40))
    liechtenstein = font3.render("LIECHTENSTEIN", 10, (40, 40, 40))
    zimbabwe = font3.render("ZIMBABWE", 10, (40, 40, 40))
    togo = font3.render("TOGO", 10, (40, 40, 40))
    bielorussie = font3.render("BIÉLORUSSIE", 10, (40, 40, 40))

    rectangle_bouton_commencer = pygame.Rect(215, 470, 120, 25)
    texte_bouton_commencer = font2.render("COMMENCER", 10, (40, 40, 40))
    joueur1 = font3.render("JOUEUR 1", 10, (40, 40, 40))
    joueur2 = font3.render("JOUEUR 2", 10, (40, 40, 40))

    lancement = True
    active1, active2 = False, False

    surface_texte1 = font2.render(nom1, 10, (0,0,0))



    while lancement:
        pygame.display.flip()

        surface_texte1 = font2.render(nom1, 10, (0, 0, 0))
        surface_texte2 = font2.render(nom2, 10, (0, 0, 0))


        # affichage de tous les éléments constants sur l'écran
        ecran.fill((200, 250, 255))
        ecran.blit(titre_nation, (100, 28))
        ecran.blit(drapeau_canada, (47, 80))
        ecran.blit(canada, (83, 150))
        ecran.blit(drapeau_etats_unis, (213, 80))
        ecran.blit(etats_unis, (238, 150))
        ecran.blit(drapeau_fidji, (378, 80))
        ecran.blit(fidji, (425, 150))
        ecran.blit(drapeau_vietnam, (47, 180))
        ecran.blit(vietnam, (83, 250))
        ecran.blit(drapeau_kirghizistan, (213, 180))
        ecran.blit(kirghizistan, (232, 250))
        ecran.blit(drapeau_liechtenstein, (378, 180))
        ecran.blit(liechtenstein, (393, 250))
        ecran.blit(drapeau_zimbabwe, (47, 280))
        ecran.blit(zimbabwe, (80, 350))
        ecran.blit(drapeau_togo, (213, 280))
        ecran.blit(togo, (258, 350))
        ecran.blit(drapeau_bielorussie, (378, 280))
        ecran.blit(bielorussie, (403, 350))
        pygame.draw.rect(ecran, (200, 200, 200), rectangle_bouton_commencer, 0)
        ecran.blit(texte_bouton_commencer, (225, 473))

        # s'il n'y a qu'un seul joueur
        if PLAYER_2_GAMEMODE == False:
            coords_entree1 = pygame.Rect(80, 400, 170, 25)
            pygame.draw.rect(ecran, (255, 255, 255), coords_entree1, 0)
            selection_nation = font2.render("NATION SÉLÉCTIONNÉE :", 10, (0,0,0))
            nom_joueur1 = font2.render("NOM DU JOUEUR :", 10, (0,0,0))
            ecran.blit(selection_nation, (310, 375))
            ecran.blit(nom_joueur1, (97, 375))
            ecran.blit(surface_texte1, (84, 403))

        if PLAYER_2_GAMEMODE == True:
            clics_possible = font3.render("(CLIC GAUCHE POUR JOUEUR 1, CLIC DROIT POUR JOUEUR 2)", 10, (40, 40, 40))
            coords_entree1 = pygame.Rect(70, 387, 170, 25)
            coords_entree2 = pygame.Rect(70, 437, 170, 25)
            pygame.draw.rect(ecran, (255, 255, 255), coords_entree1, 0)
            pygame.draw.rect(ecran, (255, 255, 255), coords_entree2, 0)
            nom_joueur1 = font2.render("NOM DU JOUEUR 1 :", 10, (0, 0, 0))
            nom_joueur2 = font2.render("NOM DU JOUEUR 2 :", 10, (0, 0, 0))
            selection_nation = font2.render("NATIONS SÉLÉCTIONNÉES :", 10, (0,0,0))
            ecran.blit(clics_possible, (83, 58))
            ecran.blit(nom_joueur1, (80, 367))
            ecran.blit(nom_joueur2, (80, 417))
            ecran.blit(selection_nation, (310, 375))
            ecran.blit(surface_texte1, (74, 390))
            ecran.blit(surface_texte2, (74, 440))


        if affichage_drapeau1 == True and PLAYER_2_GAMEMODE == False:
            ecran.blit(affichage1, (360, 405))

        if affichage_drapeau1 == True and PLAYER_2_GAMEMODE == True:
            ecran.blit(affichage1, (315, 405))
            ecran.blit(joueur1, (325, 455))

        if affichage_drapeau2 == True and PLAYER_2_GAMEMODE == True:
            ecran.blit(affichage2, (415, 405))
            ecran.blit(joueur2, (425, 455))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                lancement = False

            if event.type == pygame.KEYDOWN:
                if active1 == True:
                    if surface_texte1.get_width() <= 155:
                        if event.key == pygame.K_BACKSPACE:
                            nom1 = nom1[0:-1]
                        else:
                            nom1 += event.unicode
                    if surface_texte1.get_width() >= 155:
                        if event.key == pygame.K_BACKSPACE:
                            nom1 = nom1[0:-1]

                if active2 == True:
                    if surface_texte2.get_width() <= 155:
                        if event.key == pygame.K_BACKSPACE:
                            nom2 = nom2[0:-1]
                        else:
                            nom2 += event.unicode
                    if surface_texte2.get_width() >= 155:
                        if event.key == pygame.K_BACKSPACE:
                            nom2 = nom2[0:-1]

            if event.type == pygame.MOUSEBUTTONDOWN:
                if coords_entree1.collidepoint(event.pos):
                    active1 = True
                    active2 = False
                else:
                    active1 = False

                if PLAYER_2_GAMEMODE == True:
                    if coords_entree2.collidepoint(event.pos):
                        active2 = True
                        active1 = False
                    else:
                        active2 = False

                if event.button == 1:
                    if surface_drapeau_canada.collidepoint(event.pos):
                        affichage_drapeau1 = True
                        affichage1 = drapeau_canada_petit
                        nation1 = "canada.png"

                    if surface_drapeau_etats_unis.collidepoint(event.pos):
                        affichage_drapeau1 = True
                        affichage1 = drapeau_etats_unis_petit
                        nation1 = "etats_unis.png"

                    if surface_drapeau_fidji.collidepoint(event.pos):
                        affichage_drapeau1 = True
                        affichage1 = drapeau_fidji_petit
                        nation1 = "fidji.png"

                    if surface_drapeau_vietnam.collidepoint(event.pos):
                        affichage_drapeau1 = True
                        affichage1 = drapeau_vietnam_petit
                        nation1 = "vietnam.png"

                    if surface_drapeau_kirghizistan.collidepoint(event.pos):
                        affichage_drapeau1 = True
                        affichage1 = drapeau_kirghizistan_petit
                        nation1 = "kirghizistan.png"

                    if surface_drapeau_liechtenstein.collidepoint(event.pos):
                        affichage_drapeau1 = True
                        affichage1 = drapeau_liechtenstein_petit
                        nation1 = "liechtenstein.png"

                    if surface_drapeau_zimbabwe.collidepoint(event.pos):
                        affichage_drapeau1 = True
                        affichage1 = drapeau_zimbabwe_petit
                        nation1 = "zimbabwe.png"

                    if surface_drapeau_togo.collidepoint(event.pos):
                        affichage_drapeau1 = True
                        affichage1 = drapeau_togo_petit
                        nation1 = "togo.png"

                    if surface_drapeau_bielorussie.collidepoint(event.pos):
                        affichage_drapeau1 = True
                        affichage1 = drapeau_bielorussie_petit
                        nation1 = "bielorussie.png"

                if event.button == 3:
                    if surface_drapeau_canada.collidepoint(event.pos):
                        affichage_drapeau2 = True
                        affichage2 = drapeau_canada_petit
                        nation2 = "canada.png"

                    if surface_drapeau_etats_unis.collidepoint(event.pos):
                        affichage_drapeau2 = True
                        affichage2 = drapeau_etats_unis_petit
                        nation2 = "etats_unis.png"

                    if surface_drapeau_fidji.collidepoint(event.pos):
                        affichage_drapeau2 = True
                        affichage2 = drapeau_fidji_petit
                        nation2 = "fidji.png"

                    if surface_drapeau_vietnam.collidepoint(event.pos):
                        affichage_drapeau2 = True
                        affichage2 = drapeau_vietnam_petit
                        nation2 = "vietnam.png"

                    if surface_drapeau_kirghizistan.collidepoint(event.pos):
                        affichage_drapeau2 = True
                        affichage2 = drapeau_kirghizistan_petit
                        nation2 = "kirghizistan.png"

                    if surface_drapeau_liechtenstein.collidepoint(event.pos):
                        affichage_drapeau2 = True
                        affichage2 = drapeau_liechtenstein_petit
                        nation2 = "liechtenstein.png"

                    if surface_drapeau_zimbabwe.collidepoint(event.pos):
                        affichage_drapeau2 = True
                        affichage2 = drapeau_zimbabwe_petit
                        nation2 = "zimbabwe.png"

                    if surface_drapeau_togo.collidepoint(event.pos):
                        affichage_drapeau2 = True
                        affichage2 = drapeau_togo_petit
                        nation2 = "togo.png"

                    if surface_drapeau_bielorussie.collidepoint(event.pos):
                        affichage_drapeau2 = True
                        affichage2 = drapeau_bielorussie_petit
                        nation2 = "bielorussie.png"

                if rectangle_bouton_commencer.collidepoint(event.pos):
                    if PLAYER_2_GAMEMODE == False:
                        if nom1 != "" and nation1 != "":
                            valider = True

                        connexion = sqlite3.connect("basetp.db")
                        cursor = connexion.cursor()
                        contenu = cursor.execute("SELECT * FROM participants")
                        for row in contenu:
                            if nom1 == row[2] and nation1 != row[1]:
                                valider = False
                    try:
                        if valider:
                            # requête de création d'une table participants
                            requete = """INSERT INTO participants(nation, nom, temps) 
                                                        VALUES
                                                        (?, ?, ?)"""

                            cursor.execute(requete, (nation1, nom1, 0))  # exécuter la requête
                            connexion.commit()  # Valider l'exécution de la requête
                            connexion.close()
                            lancement = False
                            reglements()


                        if not valider:
                            print("Il ne peut pas y avoir deux {} pour deux nations différentes. Veuillez changer votre nom ou nation.".format(nom1.title()))
                    except UnboundLocalError:
                        pass

                    if PLAYER_2_GAMEMODE == True:
                        if nom1 != "" and nom2 != "" and nation1 != "" and nation2 != "":
                            valider1 = True
                            valider2 = True

                        connexion = sqlite3.connect("basetp.db")
                        cursor = connexion.cursor()
                        contenu = cursor.execute("SELECT * FROM participants")
                        for row in contenu:
                            if nom1 == row[2] and nation1 != row[1] :
                                valider1 = False

                            if nom2 == row[2] and nation2 != row[1]:
                                valider2 = False
                    try:
                        if valider1 and valider2:
                            # Ajout du CPU dans la DB

                            ai_pays = ["canada.png", "etats_unis.png", "fidji.png", "vietnam.png", "kirghizistan.png",
                                       "liechtenstein.png", "zimbabwe.png", "togo.png", "bielorussie.png"]
                            for row in contenu:
                                if row[2] == "CPU":
                                    try:
                                        ai_pays.remove(row[1])
                                    except ValueError:
                                        pass

                            requete2 = """INSERT INTO participants(nation, nom, temps) VALUES (?, ?, ?)"""
                            nation_ai = random.choice(ai_pays)
                            cursor.execute(requete2, (nation_ai, "CPU", 0))
                            connexion.commit()


                            # Ajout de P1 et P2
                            requete = """INSERT INTO participants(nation, nom, temps) 
                                                        VALUES
                                                        (?, ?, ?)"""

                            cursor.execute(requete, (nation1, nom1, 0))  # exécuter la requête
                            connexion.commit()  # Valider l'exécution de la requête

                            requete2 = """INSERT INTO participants(nation, nom, temps) 
                                                        VALUES
                                                        (?, ?, ?)"""

                            cursor.execute(requete2, (nation2, nom2, 0))  # exécuter la requête
                            connexion.commit()  # Valider l'exécution de la requête
                            connexion.close()



                            lancement = False
                            reglements()

                        else:
                            if not valider1:
                                print("Il ne peut pas y avoir deux {} pour deux nations différentes. Veuillez changer votre nom ou nation.".format(nom1.title()))

                            if not valider2:
                                print("Il ne peut pas y avoir deux {} pour deux nations différentes. Veuillez changer votre nom ou nation.".format(nom2.title()))
                    except UnboundLocalError:
                        pass


    pygame.quit()


def reglements():
    global PLAYER_2_GAMEMODE

    pygame.init()  # initialisation de tous les composants de pygame
    ecran = pygame.display.set_mode((650, 500))
    pygame.display.set_caption("Règlements")  # changer le texte de l'onglet

    font = pygame.font.SysFont("Verdana", 15, bold=False)
    titre = pygame.font.SysFont("Verdana", 28, bold=True)
    sous_titre = pygame.font.SysFont("Verdana", 18, bold=True)
    bouton = pygame.font.SysFont("Verdana", 17, bold=False)

    coords_bouton = pygame.Rect(225, 450, 200, 30)
    texte_bouton = bouton.render("DÉBUTER LA PARTIE", 10, (40, 40, 40))

    titre_jeu = titre.render("JEU D'ESQUIVE", 10, (40, 40, 40))
    objectif = sous_titre.render("OBJECTIF", 10, (40, 40, 40))
    deplacement = sous_titre.render("DÉPLACEMENTS", 10, (40, 40, 40))
    configuration = sous_titre.render("CONFIGURATION", 10, (40, 40, 40))
    fin_partie = sous_titre.render("FIN DE LA PARTIE", 10, (40, 40, 40))
    score = sous_titre.render("CALCUL DU SCORE", 10, (40, 40, 40))

    regle_principale1 = font.render("Contrôlez un carré pour éviter des balles qui apparaissent aléatoirement et se", 10, (40, 40, 40))
    regle_principale2 = font.render("déplacent à travers l’écran. Survivez le plus longtemps possible sans être touché.", 10, (40, 40, 40))
    info_balles1 = font.render("Les balles à esquiver ont une taille, une vitesse et une position ", 10, (40, 40, 40))
    info_balles2 = font.render("initiale déterminées aléatoirement au début de chaque partie.", 10, (40, 40, 40))
    score_final = font.render("Le score final du joueur correspond à son temps de survie.", 10, (40, 40, 40))

    if not PLAYER_2_GAMEMODE:
        deplacement_wasd1 = font.render("Le carré peut se déplacer dans toutes les directions grâce aux touches WASD.", 10, (40, 40, 40))
        limites_ecran = font.render("Le carré ne peut pas sortir des limites de l'écran.", 10, (40, 40, 40))
        partie_terminee1 = font.render("Si le carré entre en contact avec au moins une des balles, la partie est terminée.", 10, (40, 40, 40))

    if PLAYER_2_GAMEMODE:
        deplacement_wasd1 = font.render("Le carré du premier joueur est rouge et se déplace avec WASD.", 10, (40, 40, 40))
        deplacement_wasd2 = font.render("Le carré du deuxième joueur est bleu et se déplace avec les touches fléchées.", 10, (40, 40, 40))
        limites_ecran = font.render("Aucun carré ne peut sortir des limites de l'écran.", 10, (40, 40, 40))
        partie_terminee1 = font.render("Si un des carrés entre en contact avec au moins une des balles,", 10, (40, 40, 40))
        partie_terminee2 = font.render("son carré disparait et les autres carrés continuent de jouer.", 10, (40, 40, 40))

    lancement = True

    while lancement:
        pygame.display.flip()
        ecran.fill((200, 250, 255))

        pygame.draw.rect(ecran, (200, 200, 200), coords_bouton)
        ecran.blit(texte_bouton, (237, 453))

        ecran.blit(titre_jeu, (200, 25))
        ecran.blit(objectif, (275, 70))
        ecran.blit(regle_principale1, (28, 95))
        ecran.blit(regle_principale2, (15, 115))
        ecran.blit(deplacement, (242, 150))

        ecran.blit(configuration, (233, 230))
        ecran.blit(info_balles1, (83, 255))
        ecran.blit(info_balles2, (90, 275))
        ecran.blit(fin_partie, (230, 310))


        if not PLAYER_2_GAMEMODE:
            ecran.blit(deplacement_wasd1, (28, 175))
            ecran.blit(limites_ecran, (140, 195))
            ecran.blit(partie_terminee1, (20, 335))
            ecran.blit(score, (227, 370))
            ecran.blit(score_final, (100, 395))

        if PLAYER_2_GAMEMODE:
            ecran.blit(deplacement_wasd1, (85, 175))
            ecran.blit(deplacement_wasd2, (30, 195))
            ecran.blit(partie_terminee1, (80, 335))
            ecran.blit(partie_terminee2, (100, 355))

            ecran.blit(score, (227, 390))
            ecran.blit(score_final, (100, 415))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                lancement = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if coords_bouton.collidepoint(event.pos):
                    lancement = False
                    jeu()

    pygame.quit()


def jeu():
    global PLAYER_2_GAMEMODE, nation1, nation2, nation_ai, nom1, nom2, ordre_gagnant_nom, ordre_gagnant_pays

    def greyscale(surface: pygame.Surface):
        '''PLUGIN POUR RENDRE LES DRAPEAUX GRIS QUAND ILS PERDENT'''
        arr = pygame.surfarray.array3d(surface)
        # calulates the avg of the "rgb" values, this reduces the dim by 1
        mean_arr = np.mean(arr, axis=2)
        # restores the dimension from 2 to 3
        mean_arr3d = mean_arr[..., np.newaxis]
        # repeat the avg value obtained before over the axis 2
        new_arr = np.repeat(mean_arr3d[:, :, :], 3, axis=2)
        # return the new surface
        return pygame.surfarray.make_surface(new_arr)

    font = pygame.font.SysFont("Verdana", 15, bold=False)

    time_before_game = pygame.time.get_ticks()
    connexion = sqlite3.connect("basetp.db")
    cursor = connexion.cursor()

    pygame.init()  # initialisation de tous les composants de pygame

    ecran_largeur, ecran_hauteur = 700, 350
    jeu_largeur, jeu_hauteur = 500, 350
    ecran = pygame.display.set_mode((ecran_largeur, ecran_hauteur))

    pygame.display.set_caption("Jeu d'esquive")  # affichage de texte de fenetre

    red = (255, 0, 0)  # P1 COLOR
    blue = (0, 0, 255)  # P2 COLOR
    black = (0, 0, 0)  # AI color

    orange = (255, 127, 0)
    ordre_perdant_nom = []
    ordre_perdant_pays = []

    # Prototype for the ball dictionary, each ball index contains their x,y coords (top left side) and their xy speed
    """dictio_balle = {index de la balle: [left x, top y, vitesse_x, vitesse_y, diameter x, diameter y]}"""
    dictio_balle = {}
    liste_number = [0, 1, 2, 3, 4]  # SIMPLEMENT CHANGER LA LISTE POUR AUGMENTER LE NOMBRE DE BALLES!
    for i in liste_number:
        # Randomize les paramètres des balles
        diameter = random.randint(30, 50)
        dictio_balle[i] = [random.randint(0, jeu_largeur - 50), random.randint(0, jeu_hauteur - 50),
                           random.randint(-5, 5), random.randint(-5, 5), diameter, diameter]

    # JOUEUR 1
    player_1_status = 0  # Joueur 1 vivant
    player_1_x = 300  # Coord x de départ du joueur 1
    player_1_y = 40  # Coord y de départ du joueur 1

    # JOUEUR 2
    player_2_status = 0  # Joueur 2 vivant
    player_2_x = 150  # Coord x de départ du joueur 2
    player_2_y = 40  # Coord y de départ du joueur 2

    # AI
    ai_status = 0  # AI vivant
    ai_x = 250  # Coord x de départ du AI
    ai_y = 300  # Coord y de départ du AI

    horloge = pygame.time.Clock()

    LANCEMENT = True
    while LANCEMENT:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # constante QUIT
                LANCEMENT = False

        '''INPUT MOVEMENT'''
        pression = pygame.key.get_pressed()  # tuple pour détecter notre touche
        # Movement of player 1
        if pression[pygame.K_a]:  # en crochets la touche pressée
            if player_1_x > 0:
                player_1_x -= 5
        if pression[pygame.K_d]:
            if player_1_x < jeu_largeur - 25:
                player_1_x += 5
        if pression[pygame.K_w]:  # en crochets la touche pressée
            if player_1_y > 0:
                player_1_y -= 5
        if pression[pygame.K_s]:
            if player_1_y < jeu_hauteur - 25:
                player_1_y += 5

        # Movement of player 2
        if PLAYER_2_GAMEMODE:
            if pression[pygame.K_LEFT]:  # en crochets la touche pressée
                if player_2_x > 0:
                    player_2_x -= 5
            if pression[pygame.K_RIGHT]:
                if player_2_x < jeu_largeur - 25:
                    player_2_x += 5
            if pression[pygame.K_UP]:  # en crochets la touche pressée
                if player_2_y > 0:
                    player_2_y -= 5
            if pression[pygame.K_DOWN]:
                if player_1_y < jeu_hauteur - 25:
                    player_2_y += 5

            # Movement of the AI
            if ai_x > 0 and ai_x < jeu_largeur - 25:
                ai_x += random.randint(-10, 10)
            if ai_y > 0 and ai_y < jeu_hauteur - 25:
                ai_y += random.randint(-10, 10)

        '''GRAPHICS'''
        # Wipe the screen
        ecran.fill((200, 250, 255))

        pygame.draw.line(ecran, (0,0,0), (500,0), (500,350), width=3)

        # Légende joueur 1
        joueur_1_name = font.render(nom1, 10,
                                    (40, 40, 40))
        drapeau_joueur_1 = pygame.image.load(nation1)
        drapeau_joueur_1 = pygame.transform.scale(drapeau_joueur_1, (125, 65))
        if player_1_status == 1:
            drapeau_joueur_1 = greyscale(drapeau_joueur_1)
        ecran.blit(drapeau_joueur_1, (558, 30))
        ecran.blit(joueur_1_name, (558, 5))
        p1_legend = pygame.Rect(516, 50, 25, 25)
        pygame.draw.rect(ecran, red, p1_legend)


        if PLAYER_2_GAMEMODE:
            # Légende joueur 2
            joueur_2_name = font.render(nom2,
                                        10, (40, 40, 40))
            drapeau_joueur_2 = pygame.image.load(nation2)
            drapeau_joueur_2 = pygame.transform.scale(drapeau_joueur_2, (125, 65))
            if player_2_status == 1:
                drapeau_joueur_2 = greyscale(drapeau_joueur_2)
            ecran.blit(drapeau_joueur_2, (558, 142))
            ecran.blit(joueur_2_name, (558, 112))
            p2_legend = pygame.Rect(516, 162, 25, 25)
            pygame.draw.rect(ecran, blue, p2_legend)

            # Légende AI
            ai_name = font.render("CPU", 10, (40, 40, 40))
            drapeau_ai = pygame.image.load(nation_ai)
            drapeau_ai = pygame.transform.scale(drapeau_ai, (125, 65))
            if ai_status == 1:
                drapeau_ai = greyscale(drapeau_ai)
            ecran.blit(drapeau_ai, (558, 255))
            ecran.blit(ai_name, (558, 225))
            ai_legend = pygame.Rect(516, 275, 25, 25)
            pygame.draw.rect(ecran, black, ai_legend)


        # Moving the balls
        for i in dictio_balle.keys():
            dictio_balle[i][0] += dictio_balle[i][2]  # Change the x coordinate by the x speed
            dictio_balle[i][1] += dictio_balle[i][3]  # Change the y coordinate by the y speed

        # Generate the balls
        liste_balle = []
        for i in dictio_balle.keys():
            # Create a ball at x, y, diameter, diameter
            liste_balle.append(
                pygame.Rect(dictio_balle[i][0], dictio_balle[i][1], dictio_balle[i][4], dictio_balle[i][5]))

        # Flipping speed
        for ball in liste_balle:
            ball_index = liste_balle.index(ball)
            if ball.left <= 0 or ball.right >= jeu_largeur:  # limite X
                dictio_balle[ball_index][2] *= -1  # ou vitesse_balle_x *= -1
            if ball.top <= 0 or ball.bottom >= jeu_hauteur:  # limite Y
                dictio_balle[ball_index][3] *= -1  # ou vitesse_balle_y *= -1

        # Create the rectangles for the players
        player_1_box = pygame.Rect(player_1_x, player_1_y, 25, 25)
        if PLAYER_2_GAMEMODE:
            player_2_box = pygame.Rect(player_2_x, player_2_y, 25, 25)
            ai_box = pygame.Rect(ai_x, ai_y, 25, 25)

        # Statut des joueurs
        if player_1_status == 0:
            pygame.draw.rect(ecran, red, player_1_box)  # Dessine le joueur 1
        if PLAYER_2_GAMEMODE:
            if player_2_status == 0:
                pygame.draw.rect(ecran, blue, player_2_box)  # Dessine le joueur 2
            if ai_status == 0:
                pygame.draw.rect(ecran, black, ai_box)  # Dessine le CPU

        # Verify if a player has died
        for ball in liste_balle:
            if player_1_box.colliderect(ball):
                '''PLUGIN POUR VÉRIFIER LA COLLISION ENTRE 2 RECTANGLES'''
                player_1_status = 1  # Joueur 1 est mort
                if nom1 not in ordre_perdant_nom:
                    ordre_perdant_nom.append(nom1)
                    ordre_perdant_pays.append(nation1)

                    player_1_time = pygame.time.get_ticks()- time_before_game

                    if PLAYER_2_GAMEMODE:
                        contenu = cursor.execute("SELECT * FROM participants")
                        longueur_contenu = 0
                        for row in contenu:
                            longueur_contenu += 1
                        id_joueur_1 = longueur_contenu - 1
                    else:
                        contenu = cursor.execute("SELECT * FROM participants")
                        longueur_contenu = 0
                        for row in contenu:
                            longueur_contenu += 1
                        id_joueur_1 = longueur_contenu
                    requete = "UPDATE participants set (nation, nom, temps)  =  (?, ?, ?) where (id) = (?)"
                    cursor.execute(requete, (nation1, nom1, player_1_time/1000, id_joueur_1))
                    connexion.commit()

            if PLAYER_2_GAMEMODE:
                if player_2_box.colliderect(ball):
                    '''PLUGIN POUR VÉRIFIER LA COLLISION ENTRE 2 RECTANGLES'''
                    player_2_status = 1  # Joueur 2 est mort
                    if nom2 not in ordre_perdant_nom:
                        ordre_perdant_nom.append(nom2)
                        ordre_perdant_pays.append(nation2)

                        player_2_time = pygame.time.get_ticks() - time_before_game
                        contenu = cursor.execute("SELECT * FROM participants")
                        longueur_contenu = 0
                        for row in contenu:
                            longueur_contenu += 1
                        id_joueur_2 = longueur_contenu
                        requete = "UPDATE participants set (nation, nom, temps)  =  (?, ?, ?) where (id) = (?)"
                        cursor.execute(requete, (nation2, nom2, player_2_time/1000, id_joueur_2))
                        connexion.commit()

                if ai_box.colliderect(ball):
                    '''PLUGIN POUR VÉRIFIER LA COLLISION ENTRE 2 RECTANGLES'''
                    ai_status = 1  # Joueur 2 est mort
                    if "CPU" not in ordre_perdant_nom:
                        ordre_perdant_nom.append("CPU")
                        ordre_perdant_pays.append(nation_ai)

                        ai_time = pygame.time.get_ticks() - time_before_game
                        contenu = cursor.execute("SELECT * FROM participants")
                        longueur_contenu = 0
                        for row in contenu:
                            longueur_contenu += 1
                        id_ai = longueur_contenu - 2
                        requete = "UPDATE participants set (nation, nom, temps)  =  (?, ?, ?) where (id) = (?)"
                        cursor.execute(requete, (nation_ai, "CPU", ai_time/1000, id_ai))
                        connexion.commit()

        # Dessiner l'ellipse avec les coordonnées de chaque BALLE dans la liste
        for i in liste_balle:
            pygame.draw.ellipse(ecran, orange, i)

        horloge.tick(60)  # 60 frames per second

        pygame.display.flip()  # mise a jour de l'ecran apres un nouvel objet inséré

        # FIN DE LA PARTIE
        if PLAYER_2_GAMEMODE:
            if len(ordre_perdant_nom) == 3:
                LANCEMENT = False
                '''PLUGIN POUR CRÉER UN DÉLAI DE 3 SECONDES'''
                time.sleep(3)
                ordre_gagnant_nom = ordre_perdant_nom[::-1]
                ordre_gagnant_pays = ordre_perdant_pays[::-1]
                podium()
                accueil()

        else:
            if len(ordre_perdant_nom) == 1:
                LANCEMENT = False
                '''PLUGIN POUR CRÉER UN DÉLAI DE 3 SECONDES'''
                time.sleep(3)
                accueil()

    connexion.close()
    pygame.quit()  # désinitialiser les composants de pygame


def podium():
    global ordre_gagnant_nom, ordre_gagnant_pays
    pygame.init()  # initialisation de tous les composants de pygame

    medail1 = emoji.emojize(':1st_place_medal:')
    medail2 = emoji.emojize(':2nd_place_medal:')
    medail3 = emoji.emojize(':3rd_place_medal:')


    ecran = pygame.display.set_mode((500, 400))
    pygame.display.set_caption("Podium")  # changer le texte de l'onglet

    lancement = True


    rect_bouton = pygame.Rect(175, 30, 150, 50)
    x, y = 65, 100
    while lancement:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # constante QUIT
                lancement = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if rect_bouton.collidepoint(pygame.mouse.get_pos()):
                    lancement = False

        ecran.fill((200, 250, 255))

        texte = pygame.font.SysFont("Calibri", 25,)
        texte = texte.render(medail1, 10, (0, 0, 0))
        ecran.blit(texte, (75, 170))

        image1 = pygame.image.load(ordre_gagnant_pays[0])
        image1 = pygame.transform.scale(image1, (70, 38))
        ecran.blit(image1, (x, y))

        image2 = pygame.image.load(ordre_gagnant_pays[1])
        image2 = pygame.transform.scale(image2, (70, 38))
        ecran.blit(image2, (x+150, y+75))




        image = pygame.image.load(ordre_gagnant_pays[2])
        image = pygame.transform.scale(image, (70, 38))
        ecran.blit(image, (x+300, y+150))


        pygame.draw.rect(ecran, (50, 155, 215), rect_bouton)

            # dessiner un rectangle qui est en fait un carré
        rect1 = pygame.Rect(50, 150, 100, 250 )
        pygame.draw.rect(ecran, (225, 175, 20), rect1)  # le 15 pour l'épaisseur ou mettre 0/rien pour tout remplir

        pygame.draw.rect(ecran, (190, 210, 220), (200, 225, 100, 200))  #argent

        pygame.draw.rect(ecran, (170, 85, 5), (350, 300, 100, 150)) #bronze


        texte = pygame.font.SysFont("impact", 30, bold = False)
        texte = texte.render("1", 10, (200, 150, 0))
        ecran.blit(texte, (90, 170))

        texte2 = pygame.font.SysFont("impact", 30, bold = False)
        texte2 = texte2.render("2", 10, (165, 185, 195))
        ecran.blit(texte2, (240, 245))

        texte3 = pygame.font.SysFont("impact", 30, bold = False)
        texte3 = texte3.render("3", 10, (145, 60, 0))
        ecran.blit(texte3, (390, 320))




        texte = pygame.font.SysFont("impact", 15, bold = False)
        texte = texte.render(ordre_gagnant_nom[0], 10, (200, 150, 0))
        ecran.blit(texte, (80, 70))

        texte2 = pygame.font.SysFont("impact", 15, bold = False)
        texte2 = texte2.render(ordre_gagnant_nom[1], 10, (165, 185, 195))
        ecran.blit(texte2, (230, 145))

        texte3 = pygame.font.SysFont("impact", 15, bold = False)
        texte3 = texte3.render(ordre_gagnant_nom[2], 10, (145, 60, 0))
        ecran.blit(texte3, (380, 220))





        texte3 = pygame.font.SysFont("impact", 20, bold = False)
        texte3 = texte3.render("terminé", 10, (10, 115, 175))
        ecran.blit(texte3, (220, 45))

        pygame.display.flip()

    pygame.quit()  # desinitailiser les composants de pygame

accueil()


