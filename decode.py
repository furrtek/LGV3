# LGV3 radio frame decoder
# See LICENSE file
# furrtek 2019/02

# usage: python decode.py BBD_xxxx_low

import sys, wave, struct

def compute_crc(data):
	init = 0x1D0F
	remainder = init;
	polynomial = 0x1021

	for byte in data:
		remainder ^= (byte << 8)
		for bit in range(0, 8):
			if (remainder & 0x8000):
				remainder = ((remainder << 1) & 0xFFFF) ^ polynomial
			else:
				remainder = ((remainder << 1) & 0xFFFF)
	return remainder ^ 0xFFFF

if len(sys.argv) != 2:
	exit()
file_stub = sys.argv[1]

wav_file = wave.open(file_stub + ".wav", "rb")

n_samples = wav_file.getnframes()
sample_rate = wav_file.getframerate()
print("Opened " + file_stub + ".wav - " + str(sample_rate) + "Hz, " + str(n_samples) + " samples")

text_file = open("decoded_" + file_stub + ".txt", "w")

print("Raw decoded bytes will be written to decoded_" + file_stub + ".txt")

#waveData = wav_file.readframes(n_samples)
#data = struct.unpack("<" + str(n_samples) + "h", waveData)		# Signed short, little endian

ch = ""
shifter = "                    "
same_counter = 0
prev_sample = 0
prev_bit = 0
state = 0
tprint = 0
for i in range(0, n_samples):
	# Report progress every 5s of the input wav file
    tprint += 1
    if (tprint > sample_rate * 5):
		tprint = 0
		print(str(int(float(i) / n_samples * 100)) + "%")
	
    waveData = wav_file.readframes(1)
    data = int(struct.unpack("<h", waveData)[0])
    #if int(data[i]) >= 0:
    if data >= 0:
		sample = 1
    else:
		sample = 0
	
    if sample != prev_sample:
		# Got a transition, center of symbol is on next sample
		sample_timer = 1
	
    prev_sample = sample
	
    if sample_timer > 0:
		sample_timer -= 1
    else:
		sample_timer = 3	# Center of next symbol is in 4 samples
		
		bit = sample
	
		# Shift left and insert bit
		shifter = shifter[1:20] + str(bit)
		
		if state == 0:
			# Waiting for preamble
			if shifter == "01010101010101010101":
				ts = i / float(sample_rate)
				print("\033[0;30;47mPreamble get @ sample %u (%.1f s)\033[0m" % (i, ts))
				text_file.write(str("%07.2fs" % ts).zfill(6) + "  ")
				state = 1
		elif state == 1:
			# Waiting for sync word start
			if shifter[-2:] == "00":
				#print("Sync get:"),
				state = 2
		elif state == 2:
			# Waiting for sync word end (0x2DD4)
			if (shifter[-16:] == "0010110111010100") :
				#print(hex(int(shifter[-16:], 2)))
				#text_file.write(hex(int(shifter[-16:], 2)) + "  ")
				# Init Manchester decoder variables
				dm = ""		# Decoded bitstream
				oe = 0		# Odd/even bit flag
				print("Raw:"),
				state = 3
		elif state == 3:
			if oe == 1:
				# Manchester decode
				if prev_bit == 1 and bit == 0:
					dm += "1"
				elif prev_bit == 0 and bit == 1:
					dm += "0"
				else:
					# Manchester coding error, assume end of packet
					n_bytes = len(dm) // 8
					pkt = []
					for j in range(0, n_bytes):
						byte = int(dm[j * 8:j * 8 + 8], 2)
						pkt.append(byte)
						hex_byte = format(byte, 'X').zfill(2)
						print(hex_byte),
						text_file.write(hex_byte + " ")
					text_file.write("\n")
					print("")
					
					# Valid packets should be at least 3 bytes (L CRC CRC)
					if len(pkt) >= 3:
						packet_length = pkt[0]
						
						crc_pkt = 0
						if len(pkt) >= packet_length + 3:
							crc_hi = pkt[packet_length + 1]
							crc_lo = pkt[packet_length + 2]
							crc_pkt = crc_hi * 256 + crc_lo
						
						computed_crc = compute_crc(pkt[0:packet_length + 1])
						
						print("Length: %u, CRC: %04X" % (packet_length, crc_pkt)),
						if (crc_pkt == computed_crc):
							print("\033[0;32m(GOOD)\033[0m")
						else:
							print("\033[0;31m(BAD: %04X)\033[0m" % computed_crc)
						
						packet_type = pkt[1]
						if (packet_type == 0x96):
							if (len(pkt) >= 4):
								joueur = pkt[3]
								salle = pkt[2]
							else:
								joueur = 0
								salle = 0
							print("Report touche joueur %u (salle %u)" % (joueur, salle))
							if (len(pkt) >= 12):
								seconds = pkt[10] + pkt[11] * 256
								minutes = seconds // 60
							else:
								minutes = 0
								seconds = 0
							seconds = seconds % 60
							if (len(pkt) >= 12):
								print("Temps ecoule: %u:%u" % (minutes, seconds))
						elif packet_type == 0x0D:
							print("Game over salle %u !" % pkt[6])
						elif packet_type == 0x01:
							print("Requete dump joueur %u ?" % pkt[4])
						elif packet_type == 0x41:
							if (len(pkt) >= 24):
								seconds = pkt[22] + pkt[23] * 256
								minutes = seconds // 60
								seconds = seconds % 60
							else:
								minutes = 0
								seconds = 0
							if (len(pkt) >= 11):
								salle = pkt[10]
								joueur = pkt[4]
							else:
								salle = 0
								joueur = 0
							print("Dump joueur %u ?: salle %u, temps max %u:%u" % (joueur, salle, minutes, seconds))
						elif packet_type == 0x02:
							pseudo = ""
							for t in range(10, 25):
								pseudo += chr(pkt[t]).decode('latin1')
							equipe = pkt[26]
							seconds = pkt[28] + pkt[29] * 256
							minutes = seconds // 60
							seconds = seconds % 60
							print("Config joueur %u: salle %u, pseudo '%s', equipe %u, temps max %u:%u" % (pkt[4], pkt[8], pseudo, equipe, minutes, seconds))
						elif packet_type == 0x42:
							print("Ack config joueur %u" % pkt[4])
						elif packet_type == 0x03:
							print("Broadcast noms equipes salle %u:" % pkt[6])
							n = (packet_length - 6) // 18
							for p in range(0, n):
								pseudo = ""
								for t in range(2, 17):
									pseudo += chr(pkt[7 + 18 * p + t]).decode('latin1')	# Accents possibles
								print("  %u : '%s'" % (pkt[7 + 18 * p + 1], pseudo))
						elif packet_type == 0x0F:
							print("Req 0F? joueur %u" % pkt[4])
						elif packet_type == 0x4F:
							print("Ack 0F? joueur %u" % pkt[4])
						elif packet_type == 0x04:
							print("Broadcast pseudos salle %u:" % pkt[6])
							n = (packet_length - 6) // 18
							for p in range(0, n):
								s = 7 + 18 * p
								pseudo = ""
								for t in range(2, 17):
									pseudo += chr(pkt[s + t]).decode('latin1')
								print("  %u : '%s' type %u, equipe %u" % (pkt[s + 1], pseudo, pkt[s + 0], pkt[s + 18]))
						
						print("")
					
					state = 0
			oe ^= 1
		prev_bit = bit

text_file.close()
