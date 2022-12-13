# -*- coding: utf-8 -*-
"""
receiver

I am following the document write up by @author: Xiaoyu Tongyang( [Github](https://github.com/fengkeyleaf/), fengkeyleaf@gmail.com )
@author: xh1165@rit.edu

"""
import time
import socket
import struct
from collections import OrderedDict

class receiver:

    def __init__(self, HOST, PORT, dest, dest_PORT):
        self.HOST = HOST
        self.PORT = PORT
        self.seq=0
        self.ack=0
        self.is_SYN=0
        self.is_FIN=0
        self.dest=dest
        self.dest_PORT=dest_PORT
        self.received={}

        self.rec_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
        self.rec_sock.bind((self.HOST,self.PORT))
        self.rec_sock.settimeout(4)
        
        self.send_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM);
    '''
    Checksum script from 
    https://gist.github.com/pklaus/856268/b7194182270c816dee69438b54e42116ab31e53b
    Edited the this_val variable assignment which throws an Exception
    '''
    def checksum(self,source_string):
            #TODO: Q1:do I need padding?
            
            sum = 0
            count_to = (len(source_string) / 2) * 2
            count = 0
            while count < count_to:
                this_val = source_string[count + 1]*256+source_string[count]
                sum = sum + this_val
                sum = sum & 0xffffffff 
                count = count + 2
            if count_to < len(source_string):
                sum = sum + ord(source_string[len(source_string) - 1])
                sum = sum & 0xffffffff 
            sum = (sum >> 16) + (sum & 0xffff)
            sum = sum + (sum >> 16)
            answer = ~sum
            answer = answer & 0xffff
            answer = answer >> 8 | (answer << 8 & 0xff00)
            return answer
    
    
            
    def make_pkt( self,seq, ack, is_SYN, is_FIN, data):
        #pself.acket=seq,self.ack,is_syn,is_fin,checksum,data
        packet = struct.pack('IIBB',seq,ack,is_SYN,is_FIN)+data
        checksum = self.checksum(packet)
        packet_with_checksum=struct.pack('IIBBI',seq,ack,is_SYN,is_FIN,checksum)+data
        return packet_with_checksum
    
    def decode_pkt(self,p):
        #4+4+1+1+4
        header = p[:16]
        header = struct.unpack('IIBBI', header)
        seq=header[0]
        ack=header[1]
        is_SYN=header[2]
        is_FIN=header[3]
        checksum=header[4]
        data=p[16:]
        return seq,ack,is_SYN,is_FIN,checksum,data
    
    #get the packet, extract real checksum from it, compute the pself.acket checksum and compare it with real checksum
    def not_corrupt(self,source_string,checksum):
        checksum_check=self.checksum(source_string)
        return checksum_check == checksum

    


    

    
    def receive_pkt_event(self,p):
        r_seq,r_ack,r_is_SYN,r_is_FIN,r_checksum, r_data=self.decode_pkt(p)
        
        if self.not_corrupt(p, r_checksum):
            if r_is_FIN!=1:
                #if r_is_Fin ==1, sender want to close connection
                
                self.received[r_seq]=r_data
                self.act=r_seq+1
                self.seq+=1
                ackpkt = self.make_pkt( self.seq,  self.act, self.is_SYN, self.is_FIN, 0)
                self.send_sock.sendto(ackpkt, (self.dest,self.dest_PORTPORT))
            if r_is_FIN==1:
                #end connection, write out the received data 
                actual_file = OrderedDict(sorted(self.receive.items()))
                #TODO: write it to a file
        
    
    
    def receive(self):
         while True:
             try:
                 response, src_add = self.rec_sock.recvfrom(1024)

                 self.receive_pkt_event(response)
    
             except socket.timeout:
                 print('Request timed out')
                 
            
            
    def askfor(inp_file_name):
        #ask sender to send file
        print("Haven't developed this method")
        #TODO:
        return
        

        main()