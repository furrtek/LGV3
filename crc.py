# RFM69 CRC test
# furrtek 2019/02

data = [0x06, 0x0D, 0xFF, 0xFF, 0xFF, 0xFF, 0x02]

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
remainder ^= 0xFFFF
	
print("Should be F5 39")
print(hex(remainder))
