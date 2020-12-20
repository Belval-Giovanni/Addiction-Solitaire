import random
#Salut Giovanni 
# VARIABLES GLOBALES :

n = -1

k = 0

paires = [] #paire de cartes cliqué ;  elem[1] = carte a cliqué

nbBrassages = 3

grille = list(range(52))


# FONCTION UTILE:
#_____________________________________________________________________________

def table(contenu):
    return '<table >'+contenu+'</table>'

def tr(contenu):
    return '<tr>'+contenu+'</tr>'

def td(contenu):
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
    for i in range(2,11):
        for j in ['C','D','H','S']:
            cartes.append(str(i)+j)

    for i in ['J','K','Q']:
        for j in ['C','D','H','S']:
            cartes.append(i+j)

    for i in range(4):
        cartes.append('empty')

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
    n = -1

    return tableDeJeu

def getImgCard(index): #retourne ne contenu d'une carte d'index
                       #donné en argument

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

def getCard(index): # donne le str(numero) de la carte a la case index
    #retourne le numero et la couleur de la carte sous forme de texte

    case = document.querySelector("#case"+str(index))
    img = getImgCard(index)
    if img[7:-4][:-1].isnumeric():
        return img[7:-4]
    else:
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
        #la mise en chriffre de ses cartes permet une meilleur manipulation
        #ce celle-ci
    return

def bouton(name,function):
    if function == '':
         return '<button>'+name+'</button>'
    else:
         return '<button onclick = '+function+'()>'+name+'</button>'

def getLime():
    global paires
    lime = []
    for paire in paires:
        lime.append(paire[1])
    return lime

#_____________________________________________________________________________



# FONCTIONS IMPORTANTE POUR LE JEU:
#_____________________________________________________________________________

def vert():#colore en vert toute les cartes dont les positions sont
                  #notée dans la variables globale lime
    for e in getLime():
            case = document.querySelector("#case"+str(e))
            case.setAttribute("style", "background-color: lime")
    return

def unLime():#retire tout les attribut vers des case
    for i in getLime():
        case = document.querySelector("#case"+str(i))
        case.setAttribute("style", "background-color: ''")
    return

def carteJouable(index):
    #determine si la carte d'index index est jouables
    #dans ce cas , elle ajoute sa position aisni que celle de l'endroit
    #ou elle peut etre jouée dans la variable globale paires
    #et la colore en vert
    global grille
    global paires #contient des listes de deux index a echangé en cas de
                  #clic sur l'une des cartes jouables

    if index in [0,13,26,39]:
        for k in grille:
            if getCard(k)[:-1] == '2' :
                paires.append([index,k])

    else:
        carte = getCard(index-1)
        color = carte[-1]

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
        if getCard(j) == 'empty':
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

    unLime()
    detectionCards()
    cartesBienPlacer()
    etat()

    return

def positionValide(index):
    if getCard(index) == 'empty':return False
    if not(index%13):
        return True if getCard(index)[:-1] == '2' else False
    else:
        return positionValide(index-1) and \
        getCard(index-1)==str(int(getCard(index)[:-1])-1)+getCard(index)[-1]

def cartesBienPlacer():
    global grille
    grille.copy()
    for i in grille.copy():
        if positionValide(i):
            grille.remove(i)
    return

def brassez(liste):
    cartesBienPlacer()
    global grille
    global k

    bad = melangeur(list(map(getCard,liste)))
    for i in range(len(bad)):
        if bad[i][:-1] == '11':
            bad[i] = 'J'+bad[i][-1]

        elif bad[i][:-1] == '12':
            bad[i] = 'Q'+bad[i][-1]

        elif bad[i][:-1] == '13':
            bad[i] = 'K'+bad[i][-1]

    bad = list(map(img,bad))
    for i in grille:
        case = document.querySelector("#case"+str(i))
        case.innerHTML = bad[k]
        k+=1
    k = 0
    return

def bouton_Melange(): #actione les evenement lorsqu'on veut brasser les cartes

    global grille
    global nbBrassages

    nbBrassages -=1
    unLime()

    brassez(grille)
    detectionCards()

    texte = document.querySelector("#texte")
    texte.innerHTML = 'vous pouvez encore '+\
    bouton('brasser les cartes','bouton_Melange')+\
    ' '+str(nbBrassages)+' fois'
    print(nbBrassages)
    etat()
    return


#_____________________________________________________________________________
def init():

    global nbBrassages
    global paires
    global grille

    nbBrassages = 3
    paires = []
    grille = list(range(52))
    main = document.querySelector("#main")
    main.innerHTML = plateauInitial(melangeur(createPlateCard()))+\
    '<p id = "texte">vous pouvez encore '+\
    bouton('brasser les cartes','bouton_Melange')+\
    ' '+str(nbBrassages)+' fois'+'</p>'+\
    '<p id ="new">  '+bouton('nouvelle partie','init')+'</p>'
    detectionCards()
    return

def etat():

    global nbBrassages
    global grille

    texte = document.querySelector("#texte")
    victoire = positionValide(11) and positionValide(24)
    victoire = victoire and positionValide(37) and positionValide(50)
    
    if victoire:
        texte.innerHTML = 'vous avez gagnez'
        return

    if paires == [] and nbBrassages == 0:
        texte.innerHTML = 'vous avez perdu'
        return

    if paires == []:
        texte.innerHTML = 'vous devez'+\
        bouton('brasser les cartes','bouton_Melange')
        return

    if nbBrassages == 0:
        texte.innerHTML = 'vous ne pouvez plus brassez les cartes'
        return
