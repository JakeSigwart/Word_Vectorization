import os
import pickle
import numpy as np

#Assign a unique integer to every word encountered.
#These ints will be the perminant index in the embeddings.

class Tokenize_words:
	def __init__(self, save_path):
		self.save_path = save_path
		if os.path.isfile(self.save_path +'\\Tokens.pickle'):
			with open(self.save_path + '\\Tokens.pickle', 'rb') as f:
				self.Tokens = pickle.load(f)
				print("Loading Tokens...")
		else:
			self.Tokens = []
	
	def save(self):
		with open(self.save_path + '\\Tokens.pickle', 'wb') as f:
			pickle.dump(self.Tokens, f)
	
		
	#Get unique index from dictionary. If the word is new, add to dictionary
	def look_up_single(self, word):
		index = -1
		for n in range(0, len(self.Tokens)):
			token = self.Tokens[n]
			if equal_words(token, word):
				index = n
				break
		if index==-1:
			index = len(self.Tokens)
			self.Tokens.append(word)
		return index
	
	#Get the unique ind for a list of words
	def lookup(self, words):
		if type(words)!=list:
			words = [words]
		
		indicies = []
		for word in words:
			indicies.append(self.look_up_single(word))
		out_indices = np.array(indicies, dtype=np.uint32)
		return out_indices
		
	
	#Lookup a 2-D batch of words and labels
	#New entries are added in the order in which they appear in flattened array
	def lookup_batch(self, words_batch, labels):
		#Lookup Labels
		output_lab = []
		num_labels = len(labels)
		for label in labels:
			output_lab.append(self.lookup(label))
		label_indicies = np.reshape(np.array(output_lab, dtype=np.uint32), (num_labels))
		#Lookup batch
		output_bat = []
		for words in words_batch:
			#Append indicies to output
			output_bat.append(self.lookup(words))
		batch_indicies = np.array(output_bat, dtype=np.uint32)
		return batch_indicies, label_indicies



def equal_words(word1, word2):
	state = word1==word2
	return state





