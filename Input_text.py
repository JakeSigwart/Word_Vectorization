import os
import string

class Input_text:
	
	def __init__(self, txt_path):  #File location
		self.path = txt_path
		self.reader = open(self.path, 'r')
		self.end = False
		self.reader.seek(0)
		self.word_pointer = 0
		self.first_batch = True
		self.before_array = []
		self.target = ''
		self.after_array = []
	
	#Defines a fixed window with:  number of words to parse before, number of words to parse after target word
	def define_window_size(self, window_before, window_after):
		self.before = window_before
		self.after = window_after
	
	def define_stop_chars(self, stop_chars):
		self.stop_chars = append_to_array([], stop_chars)
		
	#Returns: array of word before, target word, array of words after target word
	def get_next_word(self):
		word = ''
		while 1==1:
			c = self.reader.read(1)
			if not c in self.stop_chars:
				break
			if c=='':
				self.end = True
		while not c in self.stop_chars and not self.end:
			word = word + c
			c = self.reader.read(1)
			if c=='':
				self.end = True
		self.word_pointer = self.word_pointer + 1
		return word
		
	def get_next_batch(self):
		if self.first_batch:
			self.before_array = []
			self.after_array = []
			for n in range(0, self.before):
				word = self.get_next_word()
				self.before_array.append(word)
			self.target = self.get_next_word()
			for n in range(0, self.after):
				word = self.get_next_word()
				self.after_array.append(word)
			self.first_batch = False
		else:
			if self.before>0:
				self.before_array[0:-1] = self.before_array[1:]
				self.before_array[-1] = self.target
			if self.after>0:
				self.target = self.after_array[0]
			else:
				self.target = self.get_next_word()
			if self.after>0:
				self.after_array[0:-1] = self.after_array[1:]
				self.after_array[-1] = self.get_next_word()
			self.first_batch = False
		return self.before_array, self.target, self.after_array, self.end
			
	def close_reader(self):
		self.reader.close()



		
		
		
def append_to_array(array, elements):
	if isinstance(elements, str):
		array.append(elements)
	elif isinstance(elements, list):
		array.extend(elements)
	else:
		print('Type other than: list, string tried to be added to array and failed')
	return array

