#!/usr/bin/env python
from brmdoor_nfc import NFCDevice, NFCError
from binascii import hexlify

def formatAPDU(apdu):
	return " ".join(["%02X" % ord(b) for b in apdu])
	
# Reading of file E104, where usually NDEF message is
hex_apdus = [
	"00 A4 04 00 07 D2760000850101",
	"00 a4 00 0c 02 E104",
	"00 b0 00 00 30",
]

# Yubikey Neo command for HMAC-SHA1 of string 'Sample #2'
#hex_apdus = [
#	"00 A4 04 00 07 A0 00 00 05 27 20 01",
#	"00 01 38 00 09 53 61 6D 70 6C 65 20 23 32"
#]

apdus = [hex_apdu.replace(" ","").decode("hex") for hex_apdu in hex_apdus]

try:
	nfc = NFCDevice()
	uid = nfc.scanUID()
	print "UID", hexlify(uid)
	nfc.close()
	nfc.open()

	print "Now trying to send ISO14443-4 APDUs"
	try:
		nfc.selectPassiveTarget()
		for apdu in apdus:
			print "Command APDU:", formatAPDU(apdu)
			rapdu = nfc.sendAPDU(apdu)
			print "Response APDU valid: %s, SW %04x, data %s" % (rapdu.valid(), rapdu.sw(), hexlify(rapdu.data()))
	except NFCError, e:
		print "Failed to transmit APDU:", e.what()

	print "Device is opened:", nfc.opened()
	print "Closing device"
	nfc.close()
	print "Device is opened:", nfc.opened()
	nfc.unload()
except NFCError, e:
	print "Reading UID failed:", e.what()
