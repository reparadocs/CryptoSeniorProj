import binascii
import base64
import string

def ascii_to_hex(ascii_string):
  return binascii.b2a_hex(ascii_string)

def hex_to_ascii(hex_string):
  return binascii.a2b_hex(hex_string)

def ascii_to_base64(ascii_string):
  return base64.encodebytes(ascii_string)

def base64_to_ascii(base64_string):
  return base64.decodebytes(base64_string)

def xor(plaintext, key):
  while len(plaintext) > len(key):
    key = key + key
  return bytes(x ^ y for x, y in zip(plaintext, key))

def index_of_coincidence(eval_string):
  try:
    ascii_string = eval_string.decode('ascii').lower().replace(" ", "")
  except:
    return 0
  ioc = 0
  letters = dict.fromkeys(string.ascii_lowercase, 0)
  for char in ascii_string:
    if char in letters.keys():
      letters[char] += 1
  for char in letters:
    ioc += letters[char] * (letters[char] - 1)
  ioc /= ((len(ascii_string) * (len(ascii_string) - 1)))
  return ioc

def task_b():
  highest_score = 0
  highest_string = ""
  f = open('lab2b.txt', 'r')
  for line in f:
    line = bytes(line.strip(), 'ascii')
    for x in range(256):
      decoded = xor(hex_to_ascii(line), bytes([x]))
      score = index_of_coincidence(decoded)
      if score > highest_score:
        highest_score = score
        highest_string = decoded

  print(highest_string)

def divide(initial, size):
  arr = [bytes([]) for i in range(size)]
  counter = 0
  for char in initial:
    arr[counter % size] += bytes([char])
    counter += 1
  return arr

def undivide(arr):
  consolidated = bytes([])

  for i in range(len(arr[0])):
    for j in range(len(arr)):
      try:
        consolidated += bytes([arr[j][i]])
      except:
        return consolidated

def key_size_index(encoded, size):
  arr = divide(encoded, size)
  avg = 0
  for string in arr:
    avg += index_of_coincidence(string)
  avg /= size
  return avg

def task_c():
  f = open('lab2c.txt', 'r')
  ascii_string = base64_to_ascii(bytes(f.read().strip(), 'ascii'))
  for i in range(10):
    print(key_size_index(ascii_string, i+1))

  key_size = 5
  arr = divide(ascii_string, key_size)
  key = bytes([])
  for word in arr:
    highest_score = 0
    highest_byte = 0
    for x in range(256):
      decoded = xor(word, bytes([x]))
      score = index_of_coincidence(decoded)
      if score > highest_score:
        highest_score = score
        highest_byte = bytes([x])
    key += highest_byte
  total_decode = xor(ascii_string, key)
  print(divide(total_decode, key_size))

  highest_score = 0
  highest_key = 0
  base_key = key[1:]
  for x in range(256):
    key = bytes([x]) + base_key
    decoded = xor(ascii_string, key)
    score = index_of_coincidence(decoded)
    if score > highest_score:
      highest_score = score
      highest_key = x
  key = bytes([highest_key]) + base_key
  total_decode = xor(ascii_string, key)
  print(divide(total_decode, key_size))
  print(total_decode)
  
  highest_score = 0
  highest_key = 0
  base_key_1 = key[:3]
  base_key_2 = bytes([key[4]])
  for x in range(256):
    key = base_key_1 + bytes([x]) + base_key_2
    decoded = xor(ascii_string, key)
    score = index_of_coincidence(decoded)
    if score > highest_score:
      highest_score = score
      highest_key = x
  key = base_key_1 + bytes([highest_key]) + base_key_2
  total_decode = xor(ascii_string, key)
  print(divide(total_decode, key_size))
  print(total_decode)

frequencies = {
  'a': 0.08167, 
  'b': 0.01492, 
  'c': 0.02782,
  'd': 0.04253, 
  'e': 0.12702, 
  'f': 0.02228, 
  'g': 0.02015,
  'h': 0.06094, 
  'i': 0.06966, 
  'j': 0.00153, 
  'k': 0.00772, 
  'l': 0.04025, 
  'm': 0.02406, 
  'n': 0.06749,  
  'o': 0.07507, 
  'p': 0.01929, 
  'q': 0.00095, 
  'r': 0.05987, 
  's': 0.06327, 
  't': 0.09056, 
  'u': 0.02758,
  'v': 0.00978, 
  'w': 0.02360, 
  'x': 0.00150, 
  'y': 0.01974, 
  'z': 0.00074
}

def frequency_score(text):
  text = text.lower().replace(" ", "")
  letters = dict.fromkeys(string.ascii_lowercase, 0)
  for char in text:
    letters[char] += 1

  chi2 = 0
  for i in letters.keys():
    expected = len(text) * frequencies[i]
    difference = letters[i] - expected
    chi2 += difference * difference / expected

  return chi2

def shift(text, val):
  alphabet = bytes(string.ascii_lowercase, 'ascii')
  shifted_a = alphabet[val:] + alphabet[:val]
  translation = bytes.maketrans(alphabet, shifted_a)
  shifted = text.lower().translate(translation)
  return shifted.decode('ascii')

def find_shift(text):
  highest_shift = ""
  highest_score = 10000
  for i in range(26):
    shifted = shift(text, i)
    score = frequency_score(shifted)
    if score < highest_score:
      highest_score = score 
      highest_shift = shifted 
  return highest_shift.encode('ascii')

def task_d():
  f = open('lab2d.txt', 'r')
  ascii_string = bytes(f.read().strip(), 'ascii')
  for i in range(20):
    print(key_size_index(ascii_string, i+1))

  key_size = 14
  divided = divide(ascii_string, key_size)
  fixed_arr = []
  for d in divided:
    fixed_arr.append(find_shift(d))

  print(undivide(fixed_arr))

task_b()
task_c()
task_d()

