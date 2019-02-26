# LGV3
Outils et docs concernant les transmissions radio de matériel Laser Tag

Le nom complet de la marque est volontairement omis mais peut être facilement deviné.

Cheminement offline: **SDR** (RTL-SDR, HackRF, ...) -> **fichier IQ** -> **Gnuradio-companion** `lgv3_iq_chan_demod.grc` -> **fichiers wav** contenant les canaux démodulés -> **decode.py** pour décoder les trames et avoir les octets bruts dans des fichiers txt

Cheminement live: **SDR** (RTL-SDR, HackRF, ...) -> **Gnuradio-companion** `lgv3_rx_live.grc` -> **FIFO** -> **decode.py**

Pour le protocole et les infos radio, voir doc/notes.txt

**gui.py** est un mock-up pas encore fonctionnel
