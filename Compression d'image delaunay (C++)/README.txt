-Extraire le contenu de l'archive projet dans un même dossier.
-Créer un projet C++ et y ajouter tous les fichiers .cpp et .h présents dans l'archive dossier SAUF main.cpp et mainbis.cpp


-SI VOUS ETES SOUS WINDOWS: ajouter main.cpp, et compilez directement, les fichiers executables devraient pouvoir être lancés.

-SI VOUS N'ETES PAS SOUS WINDOWS: - ajouter mainbis.cpp.

Note: Si vous n'utilisez pas windows, vous pouvez directement lancer les scripts python imagematrix.py pour générer les matrices et matriximage.py pour mettre les résultats en image,
si vous avez python installé ainsi que les librairies utilisées (à savoir matplotlib, PIL (python image library) et numpy ). Sinon, j'ai préparé dans le dossier test, des images ainsi que 
les fichiers .txt contenant leur matrices respectives. Et vous pouvez utiliser directement mainbis.cpp qui prend le chemin de ces fichiers .txt pour effectuer le traitement, mais il ne sera
sans doute pas possible d'afficher le résultat en image.

-si vous avez python installé: 1- executez imagematrix.py et saisissez le chemin de l'image a compresser (le fichier texte sera dans le dossier textfiles)
                               2- lancez le code C++, et donnez l'adresse du fichier txt associé a l'image saisie précédemment.
                               3- executez matriximage.py et visualisez l'image résultat dans le dossier resultimages.

-SI vous voulez lancer manuellement l'executable pour generer l'image résultat (dans le dossier bin\matriximage\matriximage.exe) il faut copier les fichiers temp.txt et le
resultimages dans le dossier \bin\matriximage et executer manuellement matriximage.exe