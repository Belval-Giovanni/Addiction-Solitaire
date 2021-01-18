#BELVAL GIOVANNI / matricule : 20139077                       DATE:21/12/2020
#YANN SAAH / matricule : 20061840

#ce programme sert de support pour une application web permettant de jouer
#au jeu addiction solitaire.


import random

# VARIABLES GLOBALES :

n = -1 #permet de numeroté les cases

k = 0

paires = [] #chaque paire represente une carte vide et la carte jouable
            #qui peut se placer a la position de la carte vide
            #respectivement dans cet ordre.

nbBrassages = 3 #represente le nombres de brassages de cartes

grille = list(range(52)) #représente les cartes bien placé du plateau


# FONCTION UTILE:
#_____________________________________________________________________________

def table(contenu):
    return '<table >'+contenu+'</table>'

def tr(contenu):
    return '<tr>'+contenu+'</tr>'

def td(contenu): #je met en place un gestionnaire d'evenement de click de souris
                 #sur chaque case , lors du clic d'une case , si la carte
                 #à l'interieur est jouable , alors elle sera déplacé
    global n
    n+=1
    return '<td onclick ="clic('+str(n)+')"id ="case'+str(n)+'">'\
    +contenu+'</td>'

def img(carte):
    return '<img src=/cards/'+carte+'.svg>'

def grouper(lst, taille):  # taille = taille maximale des groupes
    groupes = []
    accum = []
    for elem in lst:
        accum.append(elem)
        if len(accum) == taille:
            groupes.append(accum)
            accum = []
    if len(accum) > 0:
        groupes.append(accum)
    return groupes

def trJoin(lst): return tr(''.join(lst))

def tableJoin(lst): return table(''.join(lst))

def listeToTable(lst, taille):
    return tableJoin(list(map(trJoin, grouper(list(map(td, lst)), taille))))

def createPlateCard(): #cree une liste de carte ordonnée
    cartes = []
    for i in range(2,11):            #pour chaque carte entre 2 et 10
        for j in ['C','D','H','S']:  #pour chaque couleur
            cartes.append(str(i)+j)  #j'ajoute chaque combinaisons

    for i in ['J','K','Q']:          #de meme pour les cartes hautes
        for j in ['C','D','H','S']:
            cartes.append(i+j)

    for i in range(4):
        cartes.append('empty')       #j'ajoute les emplacements vides

    return cartes

def melangeur(tab): #sert a melanger entre eux les éléments d'un tableau
    l = len(tab)
    for i in range(l-1):
        alea = int(random.random()*l)
        trash = tab[i]  # je conserve la valeur initiale dans une variable
        tab[i] = tab[alea]
        tab[alea] = trash
    return tab

def plateauInitial(cartes): #retourne un tableau de texte representant
                            #des balises HTML d'image pour chacune des
                            #cartes

    global n
    cartes = list(map(img,cartes))
    tableDeJeu =  listeToTable(cartes, 13)
    n = -1     #pour les prochaine partie

    return tableDeJeu

def getImgCard(index): #prend en argument l'index de la case(de 0 à 51)
                       #retourne le contenu de la balise img  dans la balise
                       #td contenant celle-ci


    case = document.querySelector("#case"+str(index))
    img = ''
    open = False

    for e in case.innerHTML:

        if(e =='"'):
            open = not open
            continue

        if(open):
            img += e
    return img

def getCard(index): # prend en argument l'index de la case(de 0 à 51)
    #donne le str(numero) de la carte a la case index
    #retourne le numero et la couleur de la carte sous forme de texte


    case = document.querySelector("#case"+str(index))
    img = getImgCard(index)
    if img[7:-4][:-1].isnumeric():#si la carte est basse
        return img[7:-4] #represente le nom de la carte (couleur et numero)

    else:                #dans le cas d'une carte haute
        num = img[7:-5]
        color = img[7:-4][-1]

        if num == 'J':
            return str(11)+color
        if num == 'Q':
            return str(12)+color
        if num == 'K':
            return str(13)+color
        if img[7:-4] == 'empty':
            return 'empty'
        #la mise en chiffre de ses cartes permet une meilleure manipulation
        #de celles-ci.

def bouton(name,function):#prend en argument le nom d'un bouton et
                          #la fonction à laquelle il fait appel lors
                          #d'un clic sur celui-ci et renvoi le tag
                          #'<button>' avec ces parametres.
    if function == '':
         return '<button>'+name+'</button>'
    else:
         return '<button onclick = '+function+'()>'+name+'</button>'

def getLime(): #renvoi un tableau contenant les cartes a coloré en vert
    global paires
    lime = []
    for paire in paires:
        lime.append(paire[1])#car a la la position 1 de chaque élément de
                             #paires se situe une carte pouvant être jouer
    return lime

#_____________________________________________________________________________



# FONCTIONS IMPORTANTE POUR LE JEU:
#_____________________________________________________________________________

def vert(): #colore en vert toutes les cartes qui peuvent etre joué
    for e in getLime():
            case = document.querySelector("#case"+str(e))
            case.setAttribute("style", "background-color: lime")
    return

def unLime():#enleve les attributs colorés de chaque case
    for i in getLime():
        case = document.querySelector("#case"+str(i))
        case.setAttribute("style", "background-color: ''")
    return

def carteJouable(index):
    #determine si la carte d'index index est jouable
    #dans ce cas , elle ajoute son index ainsi que celui de la case
    #ou elle peut etre jouée dans la variable globale paires
    #et la colore en vert
    global grille
    global paires

    if index in [0,13,26,39]:# sur les cases de gauche , seul les 2 sont OK
        for k in grille:
            if getCard(k)[:-1] == '2' :#les cartes de numero 2 sont jouables
                paires.append([index,k])

    else: #pour les autres emplacements
        carte = getCard(index-1)
        color = carte[-1]
        #si la carte qui précede la carte vide est de meme couleur
        #et est son numéro précédent
        if carte[:-1] in list(map(str,list(range(2,13)))):
            num = int(carte[:-1])
            for k in grille:
                if getCard(k) == str(num+1)+color :
                    paires.append([index,k])

    vert()
    return

def detectionCards():#affiche en vert les cartes sur lesquelles on peut cliqué
                     #pour jouer et ajoutes les paires de positions
                     #(cartes jouable - position où la jouer)
                     #dans la variable globale paires
    global grille
    global paires
    paires = []
    for j in grille:
        if getCard(j) == 'empty':#si la case est vide on regarde quel carte
                                 #peut y etre remplacé
            carteJouable(j)

    return

def clic(index): #actionne les evenement de clic sur une carte jouable(en vert)


    for paire in paires:
        if paire[1] == index :

            #paire[0] contient toujours l'index d'une case avec la
            #carte empty et paire[1] contient l'index de la case avec une
            #carte que l'on peut placer (selon les règles) à la case
            #d'index paire[0] ( qui est donc vide)

            #on echange donc la position des carte d'index paire[0]
            #et paire[1] quand paire[1 ] = index , c'est a dire
            #que l'echange se fait uniquement pour la carte cliqué

            caseOne = document.querySelector('#case'+str(paire[0]))
            trash = caseOne.innerHTML
            caseTwo = document.querySelector('#case'+str(paire[1]))
            caseOne.innerHTML = caseTwo.innerHTML
            caseTwo.innerHTML = trash
            break

    unLime() #on retire tout les attributs vert pour ne pas avoir d'accumulation
    detectionCards()  #on detecte quelles cartes peuvent être joué
    cartesBienPlacer()#on empeche les cartes bien placé de bougé
    etat()            #on verifie l'etat du jeu

    return

def positionValide(index):#prend en paramettre un index et revoi un
                          #booleean indiquant si la carte a cet index
                          #ne dois pas bouger lors de brassages.
    if getCard(index) == 'empty':return False
    if not(index%13):#sur les case de gauche seul les 2 sont bien placé
        return True if getCard(index)[:-1] == '2' else False
    else:
        #sinon une carte est bien placé si toute les cartes précedente ont bien
        #placé et que cette est carte est la suivante de la carte d'index-1
        return positionValide(index-1) and \
        getCard(index-1)==str(int(getCard(index)[:-1])-1)+getCard(index)[-1]

def cartesBienPlacer():#retire des cartes à brasser les cartes bien placé
    global grille
    for i in grille.copy():
        if positionValide(i):#si un index dans grille possede une carte
                             #bien placé alors
            grille.remove(i) #on retire cet index de de grille
    return

def brassez():#sert a brasser les cartes mal placé
    cartesBienPlacer()
    global grille
    global k

    bad = melangeur(list(map(getCard,grille))) #tableau de carte mal placé
                                               #et melangé
    #on remplace les numeros des cartes haute par leur valeur en lettre
    for i in range(len(bad)):
        if bad[i][:-1] == '11':
            bad[i] = 'J'+bad[i][-1]

        elif bad[i][:-1] == '12':
            bad[i] = 'Q'+bad[i][-1]

        elif bad[i][:-1] == '13':
            bad[i] = 'K'+bad[i][-1]

    bad = list(map(img,bad)) #on met tout les élement de bad dans des balises
                             #img
    for i in grille:#pour chaque case mal placé on remplace le contenu de la
                    #balise img de cette case par le contenu d'une autre
                    #balise img (celle d'une autre carte mal placé)
        case = document.querySelector("#case"+str(i))
        case.innerHTML = bad[k]
        k+=1
    k = 0
    return

def bouton_Melange(): #actionne les evenement lorsqu'on veut brasser les cartes

    global grille
    global nbBrassages

    nbBrassages -=1 #on retire une possibilité de brassages
    unLime()

    brassez() #on brasse les cartes
    detectionCards()#on remet en vert les carts jouables

    texte = document.querySelector("#texte")
    texte.innerHTML = 'vous pouvez encore '+\
    bouton('brasser les cartes','bouton_Melange')+\
    ' '+str(nbBrassages)+' fois'
    etat() #on verifie l'etat du jeu
    return


#_____________________________________________________________________________
def init():#initialisation du début de partie

    global nbBrassages
    global paires
    global grille

    #on remet tous les parametres globaux importants a leurs valeurs initiales
    nbBrassages = 3
    paires = []
    grille = list(range(52))
    main = document.querySelector("#main")
    #on met en place le texte et les bouton
    main.innerHTML = plateauInitial(melangeur(createPlateCard()))+\
    '<p id = "texte">vous pouvez encore '+\
    bouton('brasser les cartes','bouton_Melange')+\
    ' '+str(nbBrassages)+' fois'+'</p>'+\
    '<p id ="new">  '+bouton('nouvelle partie','init')+'</p>'

    detectionCards()#on affiche en vert les cartes jouables
    return

def etat():#change les textes ou arrete la partie en fonction de l'etat
           #du jeu (nombre de paire , nombre de brassage restant)

    global nbBrassages
    global grille

    texte = document.querySelector("#texte")
    #victoire = True si toute les cartes sont bien placé
    victoire = positionValide(11) and positionValide(24)
    victoire = victoire and positionValide(37) and positionValide(50)

    if victoire:
        texte.innerHTML = 'vous avez gagnez'
        return

    #si plus aucune carte ne peut bouger et qu'aucun brassage n'est possible
    #c'est un game over
    if paires == [] and nbBrassages == 0:
        texte.innerHTML = 'vous avez perdu'
        return

    #si aucune carte ne peut etre joué il faut brasser
    if paires == []:
        texte.innerHTML = 'vous devez'+\
        bouton('brasser les cartes','bouton_Melange')
        return
    #change le texte pour spécifié que plus aucun brassage n'est possible
    if nbBrassages == 0:
        texte.innerHTML = 'vous ne pouvez plus brassez les cartes'
        return
