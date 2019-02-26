# LGV3 radio sniffer GUI
# See LICENSE file
# furrtek 2019/02

import sys
import glb
from PyQt5.QtWidgets import QApplication, QWidget, QDesktopWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout, QTableWidget
from PyQt5.QtWidgets import QTableWidgetItem, QProgressBar, QComboBox, QGridLayout
from PyQt5.QtGui import QFont
from PyQt5 import QtCore
from sniffer import on_button_equipe, on_button_joueur

def update_equipes():
	table_equipes.setRowCount(len(glb.equipes))
	
	for i, equipe in enumerate(glb.equipes):
		equipe['joueurs'] = 0
		equipe['score'] = 0
		for j in glb.joueurs:
			if j['equipe'] == equipe['n']:
				equipe['joueurs'] += 1
				equipe['score'] += j['score']
		
		item = QTableWidgetItem(str(equipe['n']))
		item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
		table_equipes.setItem(i, 0, item)
		
		item = QTableWidgetItem(equipe['nom'])
		item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
		table_equipes.setItem(i, 1, item)
		
		item = QTableWidgetItem(str(equipe['joueurs']))
		item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
		table_equipes.setItem(i, 2, item)
		
		item = QTableWidgetItem(str(equipe['score']))
		item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
		table_equipes.setItem(i, 3, item)

def update_joueurs():
	table_joueurs.setRowCount(len(glb.joueurs))
	
	for i, joueur in enumerate(glb.joueurs):
		#table_joueurs.setVerticalHeaderItem(i, QTableWidgetItem(str(joueur['n'])))
		item = QTableWidgetItem(str(joueur['n']))
		item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
		table_joueurs.setItem(i, 0, item)
		
		item = QTableWidgetItem(joueur['pseudo'])
		item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
		table_joueurs.setItem(i, 1, item)
		
		# Trouve le nom de l'équipe d'après son numéro
		n = joueur['equipe']
		for e in glb.equipes:
			if e['n'] == n:
				item = QTableWidgetItem(e['nom'])
				item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
				table_joueurs.setItem(i, 2, item)
				break;
		
		item = QTableWidgetItem(str(joueur['donne']))
		item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
		table_joueurs.setItem(i, 3, item)
		
		item = QTableWidgetItem(str(joueur['recu']))
		item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
		table_joueurs.setItem(i, 4, item)
		
		score = (100 * joueur['donne']) - (50 * joueur['recu'])
		joueur['score'] = score
		item = QTableWidgetItem(str(score))
		item.setTextAlignment(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignHCenter)
		table_joueurs.setItem(i, 5, item)
				
		pgbar = QProgressBar()
		pgbar.setRange(0, 65535)
		pgbar.setValue(joueur['vbat'])
		table_joueurs.setCellWidget(i, 6, pgbar)

class App(QWidget):
	def __init__(self):
		super().__init__()
		self.setFixedSize(800, 600)

		sg = QDesktopWidget().screenGeometry()

		widget = self.geometry()
		x = (sg.width() - widget.width()) / 2
		y = (sg.height() - widget.height()) / 2
		self.move(x, y)
		self.setWindowTitle("LGE V3 radio sniffer")
		self.show()
		
def init_gui():
	global table_joueurs
	global table_equipes
	
	glb.app = QApplication(sys.argv)
	glb.window = App()
	
	vlayout = QVBoxLayout()
	glayout = QGridLayout()
	
	glb.label_temps = QLabel()
	glb.label_temps.setFont(QFont('SansSerif', 20))
	glb.label_temps.setFixedWidth(280)
	
	glb.progressbar = QProgressBar()
	
	combo = QComboBox()
	for c in range(1, 6):
		combo.addItem("Salle " + str(c))
	
	table_equipes = QTableWidget(0, 4)
	table_equipes.setFixedHeight(150)
	#table_equipes.setEnabled(0)
	table_equipes.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
	table_equipes.setColumnWidth(0, 50)
	table_equipes.setHorizontalHeaderItem(1, QTableWidgetItem("Nom"))
	table_equipes.setColumnWidth(1, 150)
	table_equipes.setHorizontalHeaderItem(2, QTableWidgetItem("Joueurs"))
	table_equipes.setHorizontalHeaderItem(3, QTableWidgetItem("Score"))
	
	table_joueurs = QTableWidget(0, 7)
	#table_joueurs.setEnabled(0)
	table_joueurs.setHorizontalHeaderItem(0, QTableWidgetItem("ID"))
	table_joueurs.setColumnWidth(0, 50)
	table_joueurs.setHorizontalHeaderItem(1, QTableWidgetItem("Pseudo"))
	table_joueurs.setColumnWidth(1, 150)
	table_joueurs.setHorizontalHeaderItem(2, QTableWidgetItem("Equipe"))
	table_joueurs.setColumnWidth(2, 100)
	table_joueurs.setHorizontalHeaderItem(3, QTableWidgetItem("Donné"))
	table_joueurs.setHorizontalHeaderItem(4, QTableWidgetItem("Reçu"))
	table_joueurs.setHorizontalHeaderItem(5, QTableWidgetItem("Score"))
	table_joueurs.setHorizontalHeaderItem(6, QTableWidgetItem("VBat"))
	
	button_e = QPushButton('Add E')
	button_e.setFixedSize(100, 40)
	button_e.clicked.connect(on_button_equipe)
	button_j = QPushButton('Add J')
	button_j.setFixedSize(100, 40)
	button_j.clicked.connect(on_button_joueur)
	
	glayout.addWidget(QLabel("Suivre:"), 0, 0)
	glayout.addWidget(combo, 0, 1)
	glayout.addWidget(glb.label_temps, 1, 0, 1, 2)
	glayout.addWidget(glb.progressbar, 1, 2)
	
	vlayout.addLayout(glayout)
	vlayout.addWidget(QLabel("Equipes:"))
	vlayout.addWidget(table_equipes)
	vlayout.addWidget(QLabel("Joueurs:"))
	vlayout.addWidget(table_joueurs)
	vlayout.addWidget(button_e)
	vlayout.addWidget(button_j)

	glb.window.setLayout(vlayout)
