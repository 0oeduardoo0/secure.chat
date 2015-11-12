# -*- coding: utf-8 -*-
from hashlib import sha256

"""
      encode(data, key)

      Algorithm to encode the source

      @param string data : source for encode
      @param string key  :  key to encode

      @return string
"""
def encode(data, key):

  # first obtain a hash for the key
  # by this way we have a long key
  key = sha256(key).hexdigest()
   
  keysize = len(key)
  key_index = 0
  output = ''

  for character in data:
    if key_index >= keysize:
      key_index = 0
         
    result = ord(character) + ord(key[key_index])
         
    output += str(hex(result)).replace('0x','').zfill(3)
         
    key_index += 1

  return output.strip()

"""
      encode(data, key)

      Algorithm to decode the source

      @param string data : source for decode
      @param string key  :  key to decode

      @return string
"""     
def decode(data, key):

  # we need get the hash
  key = sha256(key).hexdigest()
  
  txtsize = len(data)
  keysize = len(key)
  key_index = 0
  output = ''

  count = 0

  while count < txtsize:
    if key_index >= keysize:
      key_index = 0

    character = data[count:count + 3] # read 3 chars

    result = int(character, 16) - ord(key[key_index])
            
    output += chr(result)
         
    key_index += 1
    count += 3
         
  return output.strip()