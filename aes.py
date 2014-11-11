#! /usr/bin/env python
# -*- coding: utf-8 -*-




"""---------- General functions and  variables ----------"""

h2b = {"0":"0000", "1":"0001", "2":"0010", "3":"0011",
		"4":"0100", "5":"0101", "6":"0110", "7":"0111",
		"8":"1000", "9":"1001", "a":"1010", "b":"1011",
		"c":"1100", "d":"1101", "e":"1110", "f":"1111"}




S = [['63', '7c', '77', '7b', 'f2', '6b', '6f', 'c5', '30', '01', '67', '2b', 'fe', 'd7', 'ab', '76'],
	['ca', '82', 'c9', '7d', 'fa', '59', '47', 'f0', 'ad', 'd4', 'a2', 'af', '9c', 'a4', '72', 'c0'],
	['b7', 'fd', '93', '26', '36', '3f', 'f7', 'cc', '34', 'a5', 'e5', 'f1', '71', 'd8', '31', '15'],
	['04', 'c7', '23', 'c3', '18', '96', '05', '9a', '07', '12', '80', 'e2', 'eb', '27', 'b2', '75'],
	['09', '83', '2c', '1a', '1b', '6e', '5a', 'a0', '52', '3b', 'd6', 'b3', '29', 'e3', '2f', '84'],
	['53', 'd1', '00', 'ed', '20', 'fc', 'b1', '5b', '6a', 'cb', 'be', '39', '4a', '4c', '58', 'cf'],
	['d0', 'ef', 'aa', 'fb', '43', '4d', '33', '85', '45', 'f9', '02', '7f', '50', '3c', '9f', 'a8'],
	['51', 'a3', '40', '8f', '92', '9d', '38', 'f5', 'bc', 'b6', 'da', '21', '10', 'ff', 'f3', 'd2'],
	['cd', '0c', '13', 'ec', '5f', '97', '44', '17', 'c4', 'a7', '7e', '3d', '64', '5d', '19', '73'],
	['60', '81', '4f', 'dc', '22', '2a', '90', '88', '46', 'ee', 'b8', '14', 'de', '5e', '0b', 'db'],
	['e0', '32', '3a', '0a', '49', '06', '24', '5c', 'c2', 'd3', 'ac', '62', '91', '95', 'e4', '79'],
	['e7', 'c8', '37', '6d', '8d', 'd5', '4e', 'a9', '6c', '56', 'f4', 'ea', '65', '7a', 'ae', '08'],
	['ba', '78', '25', '2e', '1c', 'a6', 'b4', 'c6', 'e8', 'dd', '74', '1f', '4b', 'bd', '8b', '8a'],
	['70', '3e', 'b5', '66', '48', '03', 'f6', '0e', '61', '35', '57', 'b9', '86', 'c1', '1d', '9e'],
	['e1', 'f8', '98', '11', '69', 'd9', '8e', '94', '9b', '1e', '87', 'e9', 'ce', '55', '28', 'df'],
	['8c', 'a1', '89', '0d', 'bf', 'e6', '42', '68', '41', '99', '2d', '0f', 'b0', '54', 'bb', '16']]




def keyToWords(key, Nk):
	keyWords = [[] for i in xrange(Nk)]
	word = 0
	tmp = ""
	for cpt in xrange(len(key)):
		if (cpt % 8 == 0) and (cpt <> 0):
			keyWords[word] = tmp
			word += 1
			tmp = key[cpt]
		else:
			tmp += key[cpt]
	keyWords[word] = tmp
	return keyWords




def int2hex(i):
	tmp = ""
	if (i == 0):
		tmp = '00'
	elif ( i < 16):
		tmp = '0' + hex(i).lstrip('0x')
	elif (i > 255):
		tmp = hex(i).lstrip('0x').rstrip('L')
		if (len(tmp) < 8):
			t = ''
			for i in xrange(8-len(tmp)):
				t += '0'
			tmp = t + tmp
	else:
		tmp = hex(i).lstrip('0x').rstrip('L')
	return tmp




def wortToBytes(w):
	a0 = w[0:2]
	a1 = w[2:4]
	a2 = w[4:6]
	a3 = w[6:8]
	return (a0, a1, a2, a3)




def hex2bin(h):
	tmp = ""
	for item in h:
		tmp += h2b[item]
	return tmp




def bin2byte(b):
	tmp = ''
	if len(b) > 8:
		for cpt in xrange(len(b)-8,len(b)):
			tmp += b[cpt]
	else:
		for i in xrange(8-len(b)):
			tmp += '0'
		tmp = tmp + b
	return tmp




"""---------- AES key functions ----------"""

def subWord(w):
	(a0, a1, a2, a3) = wortToBytes(w)
	return S[int(a0[0], 16)][int(a0[1], 16)] + S[int(a1[0], 16)][int(a1[1], 16)] + S[int(a2[0], 16)][int(a2[1], 16)] + S[int(a3[0], 16)][int(a3[1], 16)]




def rotWord(w):
	(a0, a1, a2, a3) = wortToBytes(w)
	return a1 + a2 + a3 + a0




def rcon(n):
	RCON = ['01000000', '02000000', '04000000', '08000000', '10000000',
			'20000000', '40000000', '80000000', '1b000000', '36000000']
	return RCON[n]




def keyExpansion(key, Nk=4, Nb=4, Nr=10):
	w = [0]*Nb*(Nr + 1)
	kw = keyToWords(key, Nk)

	for i in xrange(Nk):
		w[i] = kw[i]
		print "key round",i , "-->", w[i]

	for i in xrange(Nk, Nb*(Nr + 1)):
		tmp = w[i-1]
		if (i % Nk == 0):
			tmp = int2hex(int(subWord(rotWord(tmp)), 16) ^ int(rcon((i/Nk)-1), 16))
		elif ((Nk > 6) and (i % Nk == 4)):
			tmp = subWord(tmp)
		w[i] = int2hex(int(w[i - Nk], 16) ^ int(tmp, 16))
		print "key round",i , "-->", w[i]
	return w





"""---------- AES cipher functions ----------"""

def gMult(a, b):
	product = '00000000'
	a = hex2bin(a)
	b = hex2bin(b)
	for i in xrange(8):
		if int(b[7], 2) & 1:
			product = bin2byte(bin(int(product, 2) ^ int(a, 2)).lstrip('0b'))
		aHighBit = int(a[0], 2)
		a = bin2byte(bin(int(a, 2) << 1).lstrip('0b'))
		if aHighBit & 1:
			num = hex2bin('1b')
			a = bin2byte(bin(int(a, 2) ^ int(num, 2)).lstrip('0b'))
		b = bin2byte(bin(int(b, 2) >> 1).lstrip('0b'))
	return int(product, 2)




def subBytes(state, Nb):
	tmp = [[0 for i in xrange(Nb)] for i in xrange(Nb)]
	for i in xrange(Nb):
		for j in xrange(Nb):
			tmp[i][j] = S[int(state[i][j][0], 16)][int(state[i][j][1], 16)]
	return tmp




def shiftRows(state, Nb):
	tmp = [[0 for i in xrange(Nb)] for i in xrange(Nb)]
	for i in xrange(Nb):
		for j in xrange(Nb):
			tmp[i][j] = state[i][(j + i) % Nb]
	return tmp




def mixColumns(state, Nb):
	tmp = [[0 for i in xrange(Nb)] for i in xrange(Nb)]
	for i in xrange(Nb):
		tmp[0][i] = int2hex(gMult(state[0][i], '02') ^ gMult(state[1][i], '03') ^ gMult(state[2][i], '01') ^ gMult(state[3][i], '01'))
		tmp[1][i] = int2hex(gMult(state[0][i], '01') ^ gMult(state[1][i], '02') ^ gMult(state[2][i], '03') ^ gMult(state[3][i], '01'))
		tmp[2][i] = int2hex(gMult(state[0][i], '01') ^ gMult(state[1][i], '01') ^ gMult(state[2][i], '02') ^ gMult(state[3][i], '03'))
		tmp[3][i] = int2hex(gMult(state[0][i], '03') ^ gMult(state[1][i], '01') ^ gMult(state[2][i], '01') ^ gMult(state[3][i], '02'))
	return tmp




def addRoundKey(state, roundkey, Nb):
	tmp = [[] for i in xrange(Nb)]
	for i in xrange(Nb):
		for j in xrange(Nb):
			tmp[i].append(int2hex(int(state[i][j], 16) ^ int(roundkey[i][j], 16)))
	return tmp




def createState(block, Nb):
	tmp = [[] for i in xrange(Nb)]
	for cpt in xrange(32):
		if cpt % 8 == 0:
			tmp[0].append(block[cpt:cpt+2])
			tmp[1].append(block[cpt+2:cpt+4])
			tmp[2].append(block[cpt+4:cpt+6])
			tmp[3].append(block[cpt+6:cpt+8])
	return tmp




def createBlock(state, Nb):
	tmp = ""
	for row in xrange(Nb):
		for byte in xrange(Nb):
			tmp += state[byte][row]
	return tmp




def cipher(block, key, Nb=4, Nr=10):
	state = createState(block, Nb)
	roundKey = "".join(key[0:Nb])
	print 'round[ 0 ].input', createBlock(state, Nb)
	print 'round[ 0 ].k_sch', roundKey
	state = addRoundKey(state, createState(roundKey, Nb), Nb)

	for round in xrange(1,Nr):
		print 'round[', round, '].start', createBlock(state, Nb)
		state = subBytes(state, Nb)
		print 'round[', round, '].s_box', createBlock(state, Nb)
		state = shiftRows(state, Nb)
		print 'round[', round, '].s_row', createBlock(state, Nb)
		state = mixColumns(state, Nb)
		print 'round[', round, '].m_col', createBlock(state, Nb)
		roundKey = "".join(key[round*Nb:(round*Nb)+Nb])
		print 'round[', round, '].k_sch', roundKey
		state = addRoundKey(state, createState(roundKey, Nb), Nb)

	print 'round[', round+1, '].start', createBlock(state, Nb)
	state = subBytes(state, Nb)
	print 'round[', round+1, '].s_box', createBlock(state, Nb)
	state = shiftRows(state, Nb)
	print 'round[', round+1, '].s_row', createBlock(state, Nb)
	roundKey = "".join(key[Nr*Nb:(Nr*Nb)+Nb])
	print 'round[', round+1, '].k_sch', roundKey
	state = addRoundKey(state, createState(roundKey, Nb), Nb)
	print 'round[', round+1, '].output', createBlock(state, Nb)
	return createBlock(state, Nb)




if __name__ == "__main__":
	clearBlock = '00112233445566778899aabbccddeeff'

	key128 = '000102030405060708090a0b0c0d0e0f'
	keyExp = keyExpansion(key128, Nk=4, Nb=4, Nr=10)
	cipherBlock = cipher(clearBlock, keyExp, Nb=4, Nr=10)

	key192 = '000102030405060708090a0b0c0d0e0f1011121314151617'
	keyExp = keyExpansion(key192, Nk=6, Nb=4, Nr=12)
	cipherBlock = cipher(clearBlock, keyExp, Nb=4, Nr=12)

	key256 = '000102030405060708090a0b0c0d0e0f101112131415161718191a1b1c1d1e1f'
	keyExp = keyExpansion(key256, Nk=8, Nb=4, Nr=14)
	cipherBlock = cipher(clearBlock, keyExp, Nb=4, Nr=14)
