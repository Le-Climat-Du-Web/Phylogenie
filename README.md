# Site Web sur serveur local WAMP
![Zozor](https://blog.nicolashachet.com/wp-content/uploads/2011/05/wamp.png)


## Téléchargement et installation du logiciel Wampserver
https://www.wampserver.com/en/download-wampserver-64bits/


## Insatllation package mod_wsgi

Dans un terminal, tapez les commandes suivantes:
1. pip install mod_wsgi
2. mod_wsgi-express install-module
3. Allez dans votre dossier wamp64\bin\apache\apache2.4.46\conf\httpd.conf
4. Copiez les 3 lignes obtenues en point 2 à la suite des "LoadModule" (l'endroit n'a pas d'importance)

Vous devriez avoir ce genre de lignes

```
# WSGI module
LoadFile "C:/Python37/python37.dll"
LoadModule wsgi_module "C:/Python37/lib/site-packages/mod_wsgi/server/mod_wsgi.cp37-win_amd64.pyd"
WSGIPythonHome "C:/Python37"
WSGIApplicationGroup %{GLOBAL}
````

5. Sauvegardez et fermez le fichier

## Ajout du script .wsgi
Le plus pratique est de mettre ce script dans un dossier dédié. Ici, nous l'appelons, wsgi_scripts.

1. Créez un fichier phylogenie.wsgi et ajoutez ces lignes de code

```
import sys 

#Expand Python classes path with your app's path
sys.path.insert(0, 'C:/wamp64/www/Phylogenie') 

from app import app as application

```

## Configuration du virtual host de Wampserver

1. Créez le virtual host depuis la page d'accueil de Wamp (localhost)

Ajoutez un nouvel virtual host (1)
  
![Zozor](https://zupimages.net/up/20/50/fzu4.png)

    * Entrez le nom du fichier (1)
    * Entrez le chemin complet du fichier (2)
    * Lancez la procédure de création (3)

![Zozor](https://zupimages.net/up/20/50/nzdp.png)


2. Allez dans le fichier wamp64\bin\apache\apache2.4.46\conf\extra\httpd-vhosts.conf
3. Modifiez le code de votre virtual host comme ceci (les chemins sont à modifier en fonction de votre configuration) :

```
#
<VirtualHost *:80>
  ServerName phylogenie
  ServerAlias PY
  DocumentRoot "c:/wamp64/www/phylogenie"
  WSGIScriptAlias / "c:/wamp64/www/phylogenie/wsgi_scripts/phylogenie.wsgi"
  <Directory "c:/wamp64/www/phylogenie/">
    Options +Indexes +Includes +FollowSymLinks +MultiViews
    AllowOverride All
    Require local
  </Directory>
</VirtualHost>

```

4. Sauvegardez et fermez le fichier

## Démarrage de Wampserver 

1. Double cliquer sur l'icone du logiciel
2. Quand le serveur est prêt, il apparait en vert dans le sous-menu de la barre des tâches

![Zozor](https://zupimages.net/up/20/50/0jwl.bmp)

3. Apuyez dessus avec le clic gauche et choisiez "Vos VirtualsHosts"

![Zozor](https://zupimages.net/up/20/50/zygb.bmp)

4. Cliquez sur celui que vous avez créé et qui apparait dans la liste

![Zozor](https://zupimages.net/up/20/50/ehzt.bmp)

--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Configuration utilisée

* Windows 10 64-bits 20H2
* Python 3.7
* biopython 1.78
* numpy 1.19.3
* mod_wsgi 4.7.1
* matplotlib 3.3.3
* Flask 1.1.2 

---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
