# LGV3 radio sniffer GUI
# See LICENSE file
# furrtek 2019/02

import sys
import glb
import gui
from random import randint

def s2mmss(s):
	minutes = s // 60
	seconds = s % 60
	mmss = "%02u:%02u" % (minutes, seconds)
	return mmss

def update_time():
	glb.label_temps.setText("Temps: " + s2mmss(time_elapsed) + "/" + s2mmss(time_max))
	glb.progressbar.setRange(0, time_max)
	glb.progressbar.setValue(time_elapsed)

def add_equipe(n, nom):
	glb.equipes.append({'n':n, 'nom':nom, 'joueurs':0})

def add_joueur(n, pseudo, equipe, recu, donne, vbat):
	glb.joueurs.append({'n':n, 'pseudo':pseudo, 'equipe':equipe, 'recu':recu, 'donne':donne, 'vbat':vbat})

def on_button_equipe():
	i = len(glb.equipes)
	add_equipe(i + 1, 'branlos')
	gui.update_equipes()

def on_button_joueur():
	i = len(glb.joueurs)
	add_joueur(i, "joueur" + chr(i + ord('A')), 1, randint(0, 30), randint(0, 30), randint(50000, 65535))
	gui.update_joueurs()
	gui.update_equipes()

# Temps restant
# Statut partie
# Table equipes:
#   NOM | NB JOUEURS | SCORE
# Table joueurs:
#   PSEUDO | EQUIPE | Recu | VBat

if __name__ == '__main__':
	# Debug
	time_elapsed = 456
	time_max = 1200
	
	glb.init()
	
	gui.init_gui()

	update_time()
	
	glb.window.show()
	
	glb.app.exec_()
	
