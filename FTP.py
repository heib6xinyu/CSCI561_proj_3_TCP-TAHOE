# -*- coding: utf-8 -*-
"""
I am following the document write up by @author: Xiaoyu Tongyang( [Github](https://github.com/fengkeyleaf/), fengkeyleaf@gmail.com )


@author: xh1165@rit.edu
"""
import sys
from sender import sender

def main():
    HOST=sys.argv[1]
    PORT=int(sys.argv[2])
    dest=sys.argv[3]
    dest_PORT=int(sys.argv[4])

    #take command line argument 
    sd=sender(HOST, PORT, dest, dest_PORT)
    #TODO: transfer receiver to another file
    #receiver=receiver(HOST, PORT, dest, dest_PORT)
    print("Commands are:")
    print("connect: connect to remote myftp")
    print("put: send file ")
    print("get: receive file ")
    print("quit: exit myftp ")

    while True:
        inp=input()
        
        if inp=="connect" or inp=="c":
            sd.connect()
        elif inp=="put" or inp=="p":
            inp_file_name=input("Enter file name: ")
            #TODO:
            sd.send(inp_file_name)

        elif inp=="get" or inp=="g":
            inp_file_name=input("Enter file name: ")
            print("not implement yet")
            #receiver.askfor(inp_file_name)
        elif inp=="quit" or inp=='q':
            break

            


if __name__ == '__main__':
    main()