import constants

import tensorflow as tf
import tensorflow_datasets as tfds

import os
import re
import numpy as np

import matplotlib.pyplot as plt

tf.random.set_seed(1234)

path_to_dataset_root = os.path.join(constants.LAIN_ROOT, 'data')

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

# OK so there are two major problems right now if the goal is to make this a LAIN bot:
# 1. the data sometimes has multiple Lain statements in a row, so it is not a conversation with another person
# 2. right now i don't structure all the inputs as Lain-only. I literally just do every other line and call it a conversation
#    but i'm afraid that without doing this, i won't have enough samples. 
def load_conversations():
  inputs, outputs = [], []
  
  for root, dirs, files in os.walk(path_to_dataset_root):
    for file in files:
        if file.endswith(".txt"):
          path_to_dataset = os.path.join(root, file)
          
          with open(path_to_dataset, 'r') as file:
            lines = file.readlines()
         
          parts = [line for line in lines if line != '\n']
          conversation = [ re.sub(r"([^:]*):", "", part) for part in parts ]
            
          for i in range(len(conversation) - 1):
            inputs.append(preprocess_sentence(conversation[i]))
            outputs.append(preprocess_sentence(conversation[i + 1]))
      
  return inputs, outputs


questions, answers = load_conversations()

