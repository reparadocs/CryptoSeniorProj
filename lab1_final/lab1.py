from server import generate_token, print_table
import base64
import MT19937

def getMask(val):
        return val  %  0x100000000
 
def shiftedRight (value , shift):
    i  =  0
    result  =  0
    while  i  *  shift  <  32 :
        # undo shift and force the all 1's because of python's bitwise for neg numbers
        mask  =  (getMask(0xffffffff  <<  ( 32  -  shift ))) >>  (shift  *  i )
        # get value from mask
        part  =  value  &  mask
        # OR the two to get the current result
        result =  result | part
        # XOR to get other values
        value  =  value ^ part  >>  shift
        i  +=  1
    return  result
 
def shiftedLeft (value , shift , givenMask):
    i  =  0
    result  =  0
    while  i  *  shift  <  32 :
        mask  =  getMask(0xffffffff >> ( 32  -  shift ))  <<  ( shift  *  i )
        part  =  value  &  mask
        result =  result | part
        value  =  value ^ ( part  <<  shift )  &  givenMask
        i  +=  1
    return result

def unmix(num):
    y = shiftedRight(num, 18)
    y = shiftedLeft(y, 15, 4022730752)
    y = shiftedLeft(y, 7, 2636928640)
    y = shiftedRight(y, 11)
    return int(0xFFFFFFFF & y)

def fill_mt_table():
  mt = []
  f = open('test.txt', 'r')
  for line in f.readlines():
    decoded = base64.b64decode(line.strip())
    array_num = decoded.split(":")
    for num in array_num:
      mt.append(unmix(int(num)))
  return mt

def mt_dup():
  mt = MT19937.MT19937(0)
  new_mt_table = fill_mt_table()
  mt.get_gud(new_mt_table)
  token = str(mt.extract_number())
  for i in range(7):
    token += ":" + str(mt.extract_number())
  return base64.b64encode(token)

print mt_dup()
