import struct
out = open("123.txt", "w")    # note: 'b' for binary mode, important on Windows
format = "i"                   # one integer
data = struct.pack(format, 24) # pack integer in a binary string
out.write(data)
out.close()

input = open("123.txt", "r")
data = input.read()
input.close()
format = "i"
value, = struct.unpack(format, data) # note the ',' in 'value,': unpack apparently returns a n-uple


