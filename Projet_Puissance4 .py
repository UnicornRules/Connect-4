#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Apr  2 01:41:59 2020

@author: chendeb
"""


import numpy as np
import time
import math
import copy 
# ========================= Définition des paramètres =========================
'''
    0 = case vide
   -1 = Joueur 1
    1 = Joueur 2 
'''

# =================== Fonctions de vérification de victoire ===================
    
def VerifH(gr,lignecoup,colonnecoup):
    j = colonnecoup 
    cpt = 0
    listH=[]
    vict = False
    while(j<12 and gr[lignecoup][j] == gr[lignecoup][colonnecoup] ):
        cpt += gr[lignecoup][j] 
        listH.append([lignecoup,j])
        j+=1
    j= colonnecoup 
    while(j >=0 and gr[lignecoup][j] == gr[lignecoup][colonnecoup]):
        cpt += gr[lignecoup][j]
        listH.append([lignecoup,j])
        j-=1
    if(abs(cpt)-1 >= 4):
        vict = True
    return(vict,listH)

def VerifV(gr,lignecoup,colonnecoup):
    i = lignecoup 
    cpt = 0
    listV = []
    vict = False
    while(i<6 and gr[i][colonnecoup ] == gr[lignecoup][colonnecoup ]):
        cpt += gr[i][colonnecoup ]
        listV.append([i,colonnecoup])
        i+=1
    i = lignecoup 
    while(i >=0 and gr[i][colonnecoup ] == gr[lignecoup][colonnecoup ]):
        cpt += gr[i][colonnecoup ]
        listV.append([i,colonnecoup])
        i-=1
    if(abs(cpt)-1 >= 4):
        vict = True
    return(vict,listV)

def VerifD1(gr,lignecoup,colonnecoup):  ## diago montante
    i = lignecoup
    j = colonnecoup
    cpt = 0
    listD1=[]
    vict = False
    while(i<6 and j >= 0 and gr[i][j] == gr[lignecoup][colonnecoup ]):
        cpt+= gr[i][j]
        listD1.append([i,j])
        i+=1
        j-=1
    i = lignecoup 
    j = colonnecoup 
    while( i>=0 and j<12 and gr[i][j] == gr[lignecoup][colonnecoup ]):
        cpt+= gr[i][j]
        listD1.append([i,j])
        i-=1
        j+=1
    if(abs(cpt)-1 >= 4):
        vict = True
    return(vict,listD1)


def VerifD2(gr,lignecoup,colonnecoup):  ##diago descendante
    i = lignecoup
    j = colonnecoup
    listD2 = []
    cpt = 0
    vict = False
    while(i<6 and j < 12 and gr[i][j] == gr[lignecoup][colonnecoup ]):
        cpt += gr[i][j]
        listD2.append([i,j])
        i+=1
        j+=1
    i = lignecoup 
    j = colonnecoup
    while(i >=0 and j >= 0 and gr[i][j] == gr[lignecoup][colonnecoup ] ):
        cpt += gr[i][j]
        listD2.append([i,j])
        i-=1
        j-=1
    if(abs(cpt)-1 >= 4):
        vict = True
    return(vict,listD2)
    
    
def Verif(gr,lignecoup,colonnecoup):
    v = VerifH(gr,lignecoup,colonnecoup)[0] or VerifV(gr,lignecoup,colonnecoup)[0] or VerifD1(gr,lignecoup,colonnecoup)[0] or VerifD2(gr,lignecoup,colonnecoup)[0]
    return(v)


# ======================== Fonctions prises du morpion ========================
    
# actions possibles
def Actions(s):
    A = []
    #parcours de la grille depuis son centre
    for j in [5,6,4,7,3,8,2,9,1,10,0,11]:  
        if s[0][j]==0:
            i=5
            while(i>=0):
                if s[i][j]!=0:
                    i-=1
                else:
                    A.append([i,j])
                    i=5
                    break
    return A


# actualisation de la grille
def Result(s, a, joueur):
    temp=copy.deepcopy(s)
    temp[a[0]] [a[1]] = joueur  # joueur = +-1
    return temp

# la partie est finie ?
def Terminal_test(s):
    if tour == 36:
        return True
    i=0
    j=0
    listH=[]
    listV=[]
    listD1=[]
    listD2=[]
    while i < 6 and fin == False :
        while j<12 and fin == False:
            if(s[i][j]!=0):
            # on stocke les positions où il n'y a pas victoire
                if [i,j] not in listH:
                    v1,A = VerifH(s,i,j)
                    if(v1):
                        return True
                    listH.append(A)
                if [i,j] not in listV:
                    v2,B = VerifV(s,i,j)
                    if(v2):
                        return True
                    listH.append(B)
                if [i,j] not in listD1:
                    v3,C = VerifD1(s,i,j)
                    if(v3):
                        return True
                    listD1.append(C) 
                if [i,j] not in listD2:
                    v4,D = VerifD2(s,i,j)
                    if(v4):
                        return True
                    listD2.append(D)
            j+=1
        i+=1
        j=0
    return False

# ========================== Heuristiques et Utility ========================== 

# m et l prennent les valeurs +1 ou -1
    
def ValMotifs(liste,m,l):
    v=0
    if((f'0{m}{m}{m}0' in liste) or (f'{m}{m}{m}{m}' in liste)):
        return math.inf
    if((f'0{l}{l}{l}0' in liste) or (f'{l}{l}{l}{l}' in liste)):
        return -math.inf
    v+=900000*(liste.count(f'{l}{m}{m}{m}0')+liste.count(f'0{m}{m}{m}{l}'))
    #6v+=800000*liste.count(f'{m}{m}0{m}')
    v+=35000*liste.count(f'{l}{m}{m}{l}')
    v+=45000*(liste.count(f'0{m}{m}{l}')+liste.count(f'{l}{m}{m}0'))
    v+=600000*liste.count(f'0{m}{m}0')
    v+=3000*(liste.count(f'0{m}00')+liste.count(f'00{m}0')+liste.count(f'{m}000')+liste.count(f'000{m}'))
    v+=2000*(liste.count(f'{l}{m}00')+liste.count(f'00{m}{l}'))
    m,l=l,m #pour garder le même code on échange les variable pour calculer les motifs le l'adversaire
    v-=700000*(liste.count(f'{l}{m}{m}{m}0')+liste.count(f'0{m}{m}{m}{l}')+liste.count(f'{m}{m}0{m}'))
    v-=25000*liste.count(f'{l}{m}{m}{l}')
    v-=35000*(liste.count(f'0{m}{m}{l}')+liste.count(f'{l}{m}{m}0'))
    v-=500000*liste.count(f'0{m}{m}0')
    v-=3000*(liste.count(f'0{m}00')+liste.count(f'00{m}0')+liste.count(f'{m}000')+liste.count(f'000{m}'))
    v-=1000*(liste.count(f'{l}{m}00')+liste.count(f'00{m}{l}'))
    return v;

def ValMotifsCol(liste,m,l):
    v=0
    if(f'{m}{m}{m}{m}' in liste):
        return math.inf
    if(f'{l}{l}{l}{l}' in liste or f'0{l}{l}{l}'in liste ):
        return -math.inf
    v+=700000*liste[-5:].count(f'0{m}{m}')
    v+=300000*(liste[-4:].count(f'0{m}{m}')+liste[-4:].count(f'0{m}{m}{l}')+liste[-4:].count(f'{m}{m}{l}{l}'))
    return v;

def Utility(s):
    u = 0
    m=str(joueurLocal) # m = moi
    l=str(-joueurLocal) # l = lui
    
    #Traitement des lignes 
    for i in range(6):
        ligne="".join(str(k) for k in s[i,:])
        if(ligne.count('-1')+ligne.count('1')!=0):
            u+=ValMotifs(ligne,m,l)
        #on affecte aussi une valeur pour les singletons isolés, d'autant plus grande si au centre 
        #on récupère les indices de chaque singleton isolé
        ind=[i+1 for i in range(len(ligne)) if ligne.startswith(f'{l}{m}{l}', i) or ligne.startswith(f'{l}{m}0', i) or ligne.startswith(f'0{m}0', i)] #liste des indices des singletons
        u+=100*(ind.count(5)+ind.count(6))#plus on est auu centre plus c'est valorisé
        u+=90*(ind.count(4)+ind.count(7))
        u+=70*(ind.count(3)+ind.count(8))
        u+=60*(ind.count(2)+ind.count(9))
        u+=30*(ind.count(1)+ind.count(10))
        u+=10*(ind.count(0)+ind.count(11))
    
    #Traitement des colonnes
    for j in range(12):
        colonne="".join(str(k) for k in s[:,j])
        if(colonne.count('-1')+colonne.count('1')!=0):
            u+=ValMotifsCol(colonne,m,l)
    
    #traitement des diagonales
    #les indices pris par diag() vont de -4 à 11 (en négatif les diag qui partent des ligns et en positif des colonnes)
    for k in range(-4,12):
        diagonale="".join(str(e) for e in np.diag(s,k))
        if(diagonale.count('-1')+diagonale.count('1')!=0):
            u+=ValMotifs(diagonale,m,l)
        
    #traiteent des antidiagonales
    for k in range(-4,12):
        antidiagonale="".join(str(e) for e in np.diag(np.fliplr(s),k))
        if(antidiagonale.count('-1')+antidiagonale.count('1')!=0):
            u+=ValMotifs(antidiagonale,m,l)
#    print('utility', u)
    return u



# =========================== Affichage de la grille ==========================



CRED = '\33[31m'
CEND = '\033[0m'
CBLUE   = '\33[34m'

def remplirGrille(joueur, jeu):
    for i in range(grilleDim-1,-1,-1):
        if(grille[i][jeu]==0):
            grille[i][jeu]=joueur
            break
            
def printGrille():
    for i in range(grilleDim):
        print("|",end=' ')
        for j in range(grilleDim):
            if(grille[i][j]==1):
                print(CBLUE+'0'+CEND,end=' ')
            elif grille[i][j]==-1:
                print(CRED+'0'+CEND,end=' ')
            else:
                print(" ",end=' ')
            print("|",end=' ')
        print()
    print("|",end=' ')
    for i in range(grilleDim):
        print("_",end=" ")
        print("|",end=' ')
    print()
    print("|",end=' ')
    for i in range(1,10):
        print(i%10,end=" ")
        print("|",end=' ')
    for i in range(10,13):
        print(i,end="")
        print("|",end=' ')
    print()
    

    
# ======================  Minimax avec élagage Alpha-Bêta =====================


def minimax(position, profondeur, alpha, beta, jmax): #jmax indique si c'est le tour de max ou min 
    Eval=Utility(position)
    fini=Terminal_test(position)
    if profondeur == 0 or fini:
#        print('mini',Utility(position))
#        print(position)
        return Utility(position),None
 
    if jmax: #si c'est le tour du joueur max
        actions=Actions(position)
        maxEval = -math.inf
        maxAction= actions[0]
        for a in actions:
            enfant=Result(position,a,joueurLocal)
            Eval,_ = minimax(enfant, profondeur - 1, alpha, beta, False) #tour du joeur min
            if(Eval>=maxEval):
                maxEval=Eval
                maxAction=a
            alpha = max(alpha, Eval)
            if beta <= alpha: #coupure
                break;
        return maxEval,maxAction[1]
 
    else: #c'est le tour de min 
        actions=Actions(position)
        minEval = +math.inf
        minAction= actions[0]
        for a in actions:
            enfant=Result(position,a,-joueurLocal)
            Eval,_ = minimax(enfant, profondeur - 1, alpha, beta, True) #au tour de max
            if(Eval<=minEval):
                minEval=Eval
                minAction=a
            beta = min(beta, Eval)
            if beta <= alpha: #coupure
                break;
        return minEval,minAction[1]


# =============================================================================
# =============================================================================
# ============================ MISE EN PLACE DU JEU ===========================
# =============================================================================
# =============================================================================

grilleDim=12
grille=np.zeros((grilleDim,grilleDim),dtype=np.byte)

# bien préviser si vous commencer le jeu ou c'est l'adversaire qui commence
joueurLocalquiCommence=True
fin = False


#cette methode est à remplacer par votre une fonction IA qui propose le jeu
def monjeu(s):
    d=time.time()
    hyp = np.array(s)[6:12,:] #on va utiliser partout les arrays de numpy 
    f=time.time()
    r =minimax(hyp, 4, -math.inf, math.inf, True)[1]
    f=time.time()
    print("j'ai réfléchi pendant "+str(round(f-d,4))+"s")
    print("jai joué la colonne",r+1)
    return r

# cette fonction est à remplacer une qui saisie le jeu de l'adversaire à votre IA
def appliqueJeuAdv(jeu):
    print("Le jeu de l'adversaire est ", jeu)
    jeu -= 1
    return jeu
    


if(joueurLocalquiCommence):
    joueurLocal=-1
    joueurDistant=1
else:
    joueurLocal=1
    joueurDistant=-1
    
tour=0
while(True):
    if(joueurLocalquiCommence):
        jeu =monjeu(grille)
        #jouerWEB(idjeu,idjoueurLocal,tour,jeu)
        remplirGrille(joueurLocal,jeu)
        printGrille()
        if Terminal_test(np.array([grille[i] for i in range(6,12)])):
          print('victoire de Joueur 1')
          break;
#        jeuAdv=loopToGetJeuAdv( 10,idjeu,idjoueurDistant,tour)
        jeuAdv =int(input("Dans quelle colonne souhaitez vous jouer (1-12) : "))
        #c'est ce jeu qu'on doit transmettre à notre IA
        jeuAdv = appliqueJeuAdv(jeuAdv)
        remplirGrille(joueurDistant,jeuAdv)
        printGrille()
        if Terminal_test(np.array([grille[i] for i in range(6,12)])):
          print('victoire de Joueur 2')
          break;
    else:
#        jeuAdv=loopToGetJeuAdv( 10,idjeu,idjoueurDistant,tour)
        jeuAdv = int(input("Dans quelle colonne souhaitez vous jouer (1-12) : "))
        #c'est ce jeu qu'on doit transmettre à notre IA
        jeuAdv = appliqueJeuAdv(jeuAdv)
        remplirGrille(joueurDistant,jeuAdv)
        printGrille()
        if Terminal_test(np.array([grille[i] for i in range(6,12)])):
          print('victoire de Joueur 1')
          break;
        jeu =monjeu(grille)
        jouerWEB(idjeu,idjoueurLocal,tour,jeu)
        remplirGrille(joueurLocal,jeu)
        printGrille()
        if Terminal_test(np.array([grille[i] for i in range(6,12)])):
          print('victoire de Joueur 2')
          break;
        
    tour+=1        
    

