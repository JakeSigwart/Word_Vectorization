# Word_Vectorization
This project is an attempt to parse words from the Seinfeld Chronicles dataset: https://www.kaggle.com/thec03u5/seinfeld-chronicles and train vector representations of the words in the dataset. The training is done using Tensorflow.
## Getting Started
The code in this repository can be downloaded and used on your machine by creating a folder for the project with the proper folders for the dataset, Tensorflow model and word vectors.
## Prerequisites
A Windows machine with Python 3.6.5 was used to run all of the code. The following libraries were installed: Numpy, Scipy, Pandas, Tensorflow-1.8.0. Tensorflow can be installed on windows with the following command:
```
C:\> pip install tensorflow
```

## Downloding and Parsing the Dataset with Seinfeld_reader
Create folders named: 'data', 'embeddings', 'emb_model' and 'predict_model'. Download the dataset from: https://www.kaggle.com/thec03u5/seinfeld-chronicles and place the csv files directly into the 'data' folder. Run the following commands in a python file located in the project folder:
```
from Seinfeld_reader import *
path = os.path.dirname(__file__)
s = Seinfeld_reader()
lines = s.read_csv_scripts(path+"\\data\\scripts.csv")
words = s.extract_words()
s.save_extracted_words(path+"\\data\\scripts.pickle")
```
This will save the scripts as an array of lines with each line consisting of an array of string words. This way, the data only has to be parsed one time. This file can be opened with the following command:
```
s.load_extracted_words(path+"\\data\\scripts.pickle")
```

## Batching Data with Seinfeld_reader
Obviously, flattening all of the lines into one array is not ideal but, it should be sufficient for learning the contexts of words. We flatten the arrays of lines to make it simpler to retreive data batches. The training program uses the following commands to batch data:
```
data_path = os.path.dirname(__file__)+'\\data\\script.pickle'
reader = Seinfeld_reader()
reader.load_extracted_words(data_path)
reader.flatten_words()
word_batch, targets = reader.get_data_batch(64, 16, random_batch=False, allow_overlap=True)
```
This code will return word_batch a 2-D array of string words it contains 64 phrases each being 16 words long. The targets is a 1-D array of string words which are the words after each phrase in word_batch.

## Tokenize Words
Each word is assigned a unique index in the embeddings. To begin a new Tokenization or open the existing file, call the following:
```
token_save_path = os.path.dirname(__file__)+'\\embeddings'
token = Tokenize_words(token_save_path)
```
## Batching During Training
Call the following commands in the training loop to get data batches:
```
word_batch, targets = reader.get_data_batch( batch_size, window_size, random_batch=True, allow_overlap=True)
word_indicies, target_indicies = token.lookup_batch(word_batch, targets)
```




