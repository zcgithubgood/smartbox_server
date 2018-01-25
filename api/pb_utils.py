# -*- coding:utf-8 -*-
import struct



PACK_FORMAT = '>i'

def write_multiple_messages(io, *messages):
    #print "write_multiple_messages"
    for m in messages:
        bytes = m.SerializeToString()
        #print m
        #print len(bytes)
        io.write(struct.pack(PACK_FORMAT, len(bytes)))
        #io.write(struct.pack(PACK_FORMAT, len(bytes).SerializeToString()))
        io.write(bytes)


def read_message_buf(io):
    print "read_message_buf"
    print io
    length = struct.unpack(PACK_FORMAT, io.read(4))[0]
    buf = io.read(length)

    #print "length"
    #print length
    #print buf

    return buf
