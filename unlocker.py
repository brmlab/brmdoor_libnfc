import time
import wiringpi2 as wiringpi

class Unlocker(object):
	"""Abstract class/interface for Unlocker object.
	Unlocker useful for simulation, but does not actually unlock any lock.
	"""
	def __init__(self, config):
		"""
		Creates unlocked instance from config, where section named after
		the class is supposed to exist.
		
		@param config: BrmdoorConfig instance
		"""
		self.config = config.config
		self.lockOpenedSecs = config.lockOpenedSecs
		self.unlockerName = type(self).__name__
	
	def unlock(self):
		"""Unlock lock for given self.lockOpenedSecs.
		In this class case, it's only simulated
		"""
		time.sleep(self.lockOpenedSecs)


class UnlockerWiringPi(Unlocker):
	"""Uses configured pings via WiringPi to open lock.
	"""

	def __init__(self, config):
		Unlocker.__init__(self, config)
		self.lockPin = self.config.getint("UnlockerWiringPi", "lock_pin")
		wiringpi.pinMode(self.lockPin, 1) #output
	
	def unlock(self):
		"""Unlocks lock at configured pin by pulling it high.
		"""
		wiringpi.digitalWrite(self.lockPin, 1)
		time.sleep(self.lockOpenedSecs)
		wiringpi.digitalWrite(self.lockPin, 0)