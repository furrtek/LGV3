# LGV3
Outils et docs concernant les transmissions radio de matériel Laser Tag

Le nom complet de la marque est volontairement omis mais peut être facilement deviné.

Cheminement: **SDR** (RTL-SDR, HackRF,... tant que ça retourne de l'IQ aux alentours de 868MHz c'est bon) -> **Gnuradio-companion** -> **fichiers wav** contenant les canaux démodulés -> **decode.py** pour décoder les trames et avoir les octets bruts dans des fichiers txt

Pour le protocole et les infos radio, voir doc/notes.txt
