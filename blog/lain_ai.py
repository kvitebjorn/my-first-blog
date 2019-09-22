import constants

import tensorflow as tf
import tensorflow_datasets as tfds

import os
import re
import numpy as np

import matplotlib.pyplot as plt

tf.random.set_seed(1234)

path_to_dataset = os.path.join(constants.LAIN_ROOT, 'data\\layer01.txt')
print( path_to_dataset )
print(tf.__version__)

def preprocess_sentence(sentence):
  sentence = sentence.lower().strip()
  # creating a space between a word and the punctuation following it
  # eg: "he is a boy." => "he is a boy ."
  sentence = re.sub(r"([?.!,])", r" \1 ", sentence)
  sentence = re.sub(r'[" "]+', " ", sentence)
  
  # replacing everything with space except (a-z, A-Z, ".", "?", "!", ",", digits)
  sentence = re.sub(r"[^a-zA-Z0-9?.!,]+", " ", sentence)
  sentence = sentence.strip()
  
  return sentence

def load_conversations():
  inputs, outputs = [], []
  with open(path_to_dataset, 'r') as file:
    lines = file.readlines()
 
  parts = [line for line in lines if line != '\n']
  conversation = [ re.sub(r"([^:]*):", "", part) for part in parts ]
    
  for i in range(len(conversation) - 1):
    inputs.append(preprocess_sentence(conversation[i]))
    outputs.append(preprocess_sentence(conversation[i + 1]))
      
  return inputs, outputs


questions, answers = load_conversations()
print(questions)
print(answers)
