#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 10 16:27:48 2020

@author: maison
"""
import requests
import re
from bs4 import BeautifulSoup
import psycopg2

import config
import time

conn = psycopg2.connect(database="bdd_rkalamani", user=config.user,password=config.password, host='127.0.0.1') 
cur = conn.cursor()






def DernierNumeroPage():
    url = "https://chucknorrisfacts.net/facts.php?page=1" 
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'}

    reponse = requests.get(url, headers = header)# Cette ligne de commande m'affiche l'etat de la connexion tout en esperant la reponse 200 pou ok

    soup = BeautifulSoup(reponse.content, 'html.parser') # on analyse le contenu de la page web selectionnée avec l'analyseur html html.parser
    l=[]
    for a in soup.find_all('a'): # parcourt l'ensemble des balises 
        if 'href' in a.attrs:
            l.append(a['href']) 
            
    urlfin = l[-4]
    urlfin=str(urlfin) # conversion de cet url en string pour pouvoir manipuler cette chaine de caractère
    Nnpg=urlfin[len(urlfin)-3:len(urlfin)] # extraction de la chaine de caractère les caractères compris entre la longeur totale de la chaine et la longeur totale de la chaine-3
    return(Nnpg) # sort de la fonction la variable qui contient la dernière page

#La fonction  recupPage va scraper le contenu de la page numérotée p et va être stocké dans la table  que j'appelle Chuck  
def recupPage(page):
    
    url = "https://chucknorrisfacts.net/facts.php?page={}" .format(page)
    print("")
    print('Récupération de', url)
   
    
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.66 Safari/537.36'}
    reponse = requests.get(url, headers=header)# Affiche l'état de connexion par un code qui sera : 200
    
    if reponse.ok : 
        print(reponse)
        print("scraping de la page {} en cours".format(page))
        
        time.sleep(1) #c'est le temps d'arret en les pages 
        
        soup = BeautifulSoup(reponse.content, 'html.parser') # on analyse le contenu de la page web selectionnée 
        # Va parcourir l'emsemble des blocs de la page web qui contient les balises p  et les balises span contenant les attributs out5Class et  voteClass
        blocks = soup.select("#content > div:nth-of-type(n+2)") # '#content > div:nth-of-type(n+2)' est obtenu grâce à l'extension Chrome web scraper. Va cherhcher les selecteurs css de la page à scraper et les ressort sous forme de liste 
    
        for block in blocks: # Va parcourir l'emsemble des selecteurs css de la page scrapé
            blague = block.select_one("p")# Dans chaque selecteur css, on selectione le contenue entre les balises <p>...</p>
            if blague is not None: # On prend que les selecteurs css qui ne sont pas vide
                id = block.select_one("ul.star-rating").attrs['id'] # Dans chaque selecteur css, on selectione le contenue entre les balises <ul>...</ul> de classe star-rating de l'atrtibut id
                note = block.select_one("span.out5Class") # Dans chaque selecteur css, on selectione le contenue entre les balises <span>...</span> de classe out5Class
                vote = block.select_one('span.votesClass') # Dans chaque selecteur css, on selectione le contenue entre les balises <span>...</span> de classe voteClass
                cur.execute("""INSERT INTO public."Chuck" VALUES (%s, %s, %s, %s) ON CONFLICT (id) DO NOTHING;""", (int(id[6:]), blague.text,float(note.text) ,int(vote.text[:-6]) ))
                # Execute la requete sql : insert la ligne scrapée dans la table Chuck pour les colonnes suivantes : int(id[6:])signifie le contenu de la variable id emputer des 6 premiers caractères et de nature int, blague.text signifie le contenu de la variable blague est de nature text, float(note.text) signifie que la nature de cette variable est float, int(vote.text[:-6])signifie que le contenu de cette variable est de type int et est emputé des 6 derniers caracteres   
    else : # Erreur de statut qui empêche le web scraping
        print(reponse)
        print("")
        print("Erreur de connexion")
            
# Scraper l'emsemble des pages du site Chuck Norris fact et stocke les données dans la base de données            
print("Vidage de la table Chuck ")
cur.execute('TRUNCATE TABLE public."Chuck"')
print("")
print("Début de remplissage de la table Chuck")
dn = int(DernierNumeroPage())
            
for page in range(1,dn+1):
    recupPage(page)
    
print("")    
print("Fin de remplissage de la table Chuck")
print("")

#print(cur.fetchall()) # affiche le nombre de lignes dans la table de la bdd

conn.commit()# valide toute les transactions (modifications) de la tables
conn.close() #Ferme la connexion à la base de données