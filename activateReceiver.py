# -*- coding: utf-8 -*-
"""
call receiver
@author: xh1165@rit.rdu
"""

import sys
from receiver import receiver
def main():
    HOST=sys.argv[1]
    PORT=int(sys.argv[2])
    dest=sys.argv[3]
    dest_PORT=int(sys.argv[4])
    print("Receiver listening:")

    rc=receiver(HOST, PORT, dest, dest_PORT)
    rc.receive()
if __name__ == '__main__':
    main()