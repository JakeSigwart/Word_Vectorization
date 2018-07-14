import os
import re
import random
import pandas as pd
import pickle

#Seinfeld Chronicles Dataset: https://www.kaggle.com/thec03u5/seinfeld-chronicles
#Parse words from the dataset.

class Seinfeld_reader:
	def __init__(self):
		print('New Seinfeld Reader')
		self.word_pointer = 0
		
	#Input: Path to csv file
	#Processing: Add speakers name to beggining of each line.
	#			 A '@' before the speaker's name indicates a new episode.
	def read_csv_scripts(self, csv_path):
		scripts = pd.read_csv(csv_path)
		
		self.dial = scripts['Dialogue']
		self.speaker = scripts['Character']
		self.episode = scripts['SEID']
		
		self.Lines = []
		
		num_lines = len(self.speaker)
		for n in range(0, num_lines):
			if n%500==0:
				print("Reading line: "+str(n)+" from Seinfeld")
			dial_n = self.dial.iloc[n]
			self.Lines.append(dial_n)
		return self.Lines
		
	
	def get_random_lines(self, num_rand=1):
		num_lines = len(self.Lines)
		lines_out = []
		for n in range(0, num_rand):
			index = random.randint(0, num_lines-1)
			lines_out.append(self.Lines[index])
		return lines_out
	

	#Seperate each line into words
	def extract_words(self, stop_chars=['\n', '.', '?', '!', ';', ':', ' ', ',', '"', '[', ']', '(', ')'] ):
		self.words_extracted = []
		for n in range(0, len(self.Lines)):
			if n%2000==0:
				print("Extracting words in line: "+str(n))
			line = self.Lines[n]
			new_words = []
			if isinstance(line, str):
				length_line = len(line)
			else:
				length_line = 0
			pointer = 0
			#for each line
			while pointer < length_line:
				word = ''
				c = ''
				while (c in stop_chars or c=='') and (pointer < length_line):
					c = line[pointer]
					pointer = pointer + 1
				while (not c in stop_chars) and (pointer < length_line):
					word = word + c
					c = line[pointer]
					pointer = pointer + 1
				new_words.append(word)
			self.words_extracted.append(new_words)
		return self.words_extracted
	
	
	def load_extracted_words(self, file_path):
		with open(file_path, 'rb') as f:
			self.words_extracted = pickle.load(f)
			print("Loading extracted words...")
	
	def flatten_words(self):
		self.flat_words = []
		for line in self.words_extracted:
			for word in line:
				self.flat_words.append(word)
		return self.flat_words
	
	#int number of phrases, random_batch=True for phrases randomly selected throughout dataset
	def get_single_batch(self, batch_size, random_batch=False, allow_overlap=True):
		if random_batch:
			self.word_pointer = random.randint(batch_size, len(self.flat_words)-1)
		if self.word_pointer == 0:
			self.word_pointer = batch_size
		batch = self.flat_words[self.word_pointer-batch_size:self.word_pointer]
		target = self.flat_words[self.word_pointer]	
		if allow_overlap:
			self.word_pointer = self.word_pointer + 1
		else:
			self.word_pointer = self.word_pointer + batch_size+1
		return batch, target
		
	#Get a 2-D array. Axis 0: batch index,  Axis 1: word in sentance index
	def get_data_batch(self, batch_depth, batch_size, random_batch=False, allow_overlap=True):
		batches = []
		targets = []
		for c in range(0, batch_depth):
			b,t = self.get_single_batch(batch_size, allow_overlap, random_batch)
			batches.append(b)
			targets.append(t)
		
		return batches, targets
		
		
	def save_extracted_words(self, file_path):
		with open(file_path, 'wb') as f:
			pickle.dump(self.words_extracted, f)
		print("Saving extracted words...")
		
	#HAVING ENCODING ISSUES
	#Save the scripts to a text file
	def save_as_text(self, file_path):
		#self.dial = scripts['Dialogue']
		#self.speaker = scripts['Character']
		#self.episode = scripts['SEID']
		file = open(file_path, 'w')
		num_lines = len(self.speaker)
		last_ep = "S01E01"
		for n in range(0, num_lines):
			if n%2000==0:
				print("Writing line: "+str(n)+" to file")
			speaker_n = self.speaker.iloc[n]
			dial_n = self.dial.iloc[n]
			episode = self.episode.iloc[n]
			if last_ep!=episode:
				file.write("@ "+episode+'\n')
			file.write(str(speaker_n+': \t'+dial_n+'\n'))
			
			last_ep = episode
		file.close()


#Example Usage		
'''
from Tokenize_words import *

path = os.path.dirname(__file__)+'\\data\\Seinfeld\\script.pickle'
s = Seinfeld_reader()
s.load_extracted_words(path)
s.flatten_words()
#print(str(len(s.flat_words)))
b,t = s.get_data_batch( 1, 5000, random_batch=True, allow_overlap=True)
print(b)
print(t)

T = Tokenize_words(' ')
ind = T.lookup(b[0])
print(ind)

'''


