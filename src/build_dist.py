#!/usr/bin/env python3

import sys
import getopt

def main(argv):
  try:
    opts, args = getopt.getopt(argv, "hi:c:v:y", ["help"])
  except getopt.GetoptError:
    print ("./build_dist.py -i <inputfile> -c <minConsonants> -v <minVowels> -y (flag only, should y be treated as vowel)")
    sys.exit(2)

  inputfile = None
  minConsonants = 0
  minVowels = 0
  y_is_vowel = False
  for opt, arg in opts:
    if opt in  ('-h', "--help"):
      print ("./build_dist.py -i <inputfile> -c <minConsonants> -v <minVowels> -y (flag only, should y be treated as vowel)")
      sys.exit()
    elif opt in ("-i"):
      inputfile = arg
    elif opt in ("-c"):
      minConsonants = int(arg)
    elif opt in ("-v"):
      minVowels = int(arg)
    elif opt in ('-y'):
      y_is_vowel = True

  if inputfile == None:
    print ("inputfile required")
    print ("./build_dist.py -i <inputfile> -c <minConsonants> -v <minVowels> -y (flag only, should y be treated as vowel)")
    sys.exit(2)
  
  total_req = (minConsonants + minVowels)
  if total_req > 5:
    print ("Requsted min consonants [{}] and min vowels [{}] exceed five character word length.".format(minConsonants, minVowels))
    sys.exit(2)

  print ("Building distribution from {} with {} min consonants and {} min vowels. 'Y is a vowel'={}...".format(inputfile, minConsonants, minVowels,y_is_vowel))

  data = []
  distro = {}
  with open(inputfile, 'r') as f:
    for line in f:
      data.append(line.strip())
  for word in data:
    i = 0
    for letter in word:
      if not i in distro:
        distro[i] = {}
      if not letter in distro[i]:
        distro[i][letter] = 1
      else:
        distro[i][letter] += 1
      i += 1
  for key in distro:
    # python 3 preserves insert order, sort of letter key
    distro[key] = dict(sorted(distro[key].items(), key = lambda item: item[0]))

  vowels = ['a', 'e', 'i', 'o', 'u'] # not doing y for now
  # unique letters and at least two vowels
  word_weights = {}
  for word in data:
    disallow = False
    n_con = 0
    n_vowels = 0
    duplicates = {}
    for char in word:
      if char in vowels or (char == 'y' and y_is_vowel):
        n_vowels += 1
      else:
        n_con += 1
      if char in duplicates:
        disallow = True
      else:
        duplicates[char] = 1
    if disallow == True or n_vowels < minVowels or n_con < minConsonants:
      continue
    weight = 0
    i = 0
    for letter in word:
      weight += distro[i][letter]
    word_weights[word] = weight

  word_weights = dict(sorted(word_weights.items(), key = lambda item: item[1], reverse = True))
  for word,weight in word_weights.items():
    print (word + ": " + str(weight))

if __name__ == "__main__":
  main(sys.argv[1:])
