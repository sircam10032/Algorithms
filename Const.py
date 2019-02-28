from collections import Iterable


class Const:
	BLACK = True
	RED = False
	LEFT = True
	RIGHT = False
	
	class ConstError(TypeError):
		pass
	
	def __init__(self, **kwargs):
		
		if 'keys' in kwargs and 'values' in kwargs:
			keys = kwargs['keys']
			values = kwargs['values']
			if not isinstance(keys, Iterable) or \
				not isinstance(values, Iterable):
				raise Exception('init received uninterable object')
			for k, v in zip(keys, values):
				if not isinstance(k, str):
					continue
				self.__setattr__(k, v)
		
		if 'dict' in kwargs:
			d = kwargs['dict']
			if not isinstance(d, dict):
				raise TypeError('dict received error input')
			for k, v in d.items():
				if not isinstance(k, str):
					continue
				self.__setattr__(k, v)
	
	def __setattr__(self, key, value):
		if key in self.__dict__:
			raise self.ConstError('existed const name')
		self.__dict__[key] = value
