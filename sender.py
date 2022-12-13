# -*- coding: utf-8 -*-
"""
Sender
I am following the document write up by @author: Xiaoyu Tongyang( [Github](https://github.com/fengkeyleaf/), fengkeyleaf@gmail.com ), 11/23/2022


@author: xh1165@rit.edu
"""
import time
import socket
import struct

class sender:
    def __init__(self, HOST, PORT, dest, dest_PORT):
        self.HOST = HOST
        self.PORT = PORT
#        self.initSeqNum=0
        self.ack=0
        self.seq=0
#        self.window_left=0
        self.cwnd= 1
        self.is_SYN=1
        self.is_FIN=0
        self.default_ssthresh=64
        self.ssthresh=self.default_ssthresh
        self.dest=dest
        self.dest_PORT=dest_PORT
        self.dupAckCount=0
        #self.received=[]

        
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
    
    
        
    def send_data_event(self,d):
        self.seq += 1
        packet = self.make_pkt( self.seq, self.ack, self.is_SYN, self.is_FIN,d)
        self.send_sock.sendto(packet, (self.dest, self.dest_PORT))
    
        return
    
    def receive_pkt_event(self,p):
        
        r_seq,r_ack,r_is_SYN,r_is_FIN,r_checksum, r_data=self.decode_pkt(p)
        
        if self.not_corrupt(p, r_checksum):
            #update parameters
            if r_ack==self.ack:
                self.dupAckCount+=1
            else:
                self.dupAckCount=0
                self.ack=1+r_seq

                #new pkt
        #if corrupted, don't send ack back
        self.tcp_tahoe()
    
    def tcp_tahoe(self):
        if self.dupAckCount <= 3:
            #slowstart

            if self.cwnd < self.ssthresh:
                self.cwnd+=1
             #Congestion Control
                   
            elif self.cwnd >= self.ssthresh:
                self.cwnd += 1//self.cwnd
                        

        else:
            self.ssthresh=self.cwnd//2
            self.cwnd= 1
            self.dupAckCount=0
            #go back to Slow Start
        
    def send(self,inp_file_name):
        self.is_SYN=0
        self.is_FIN=0
        #send selected file
        #1.divide file into data segment d
        print("Haven't developed send from file, send default info instead")
        data = ('A'*512).encode("utf-8")
        #TODO: update it to datasegment from file
        #2.loop through packets and send_data_event(d)
        while True:
            for dataseg in data:
                send_timer=0
                self.send_data_event(dataseg)
                try:
                    response, src_add = self.rec_sock.recvfrom(1024)
                    self.receive_pkt_event(response)
                except socket.timeout:
                    if send_timer <=3:
                        self.seq-=1
                        print("timeout, resend "+self.seq)
                        send_timer+=1
                        return self.send_data_event(0)
                    else:
                        print("close connection")
                        self.is_FIN=1
                        self.send_data_event(0)

                    return
        return
    
    def connect(self):
        #3 way handshake
        self.is_SYN = 1
        data = ('A'*512).encode("utf-8")

        self.send_data_event(data)
        send_timer=1
        try:
            response, src_add = self.rec_sock.recvfrom(1024)
            
        except socket.timeout:
            if send_timer <=3:
                self.seq-=1
                print("timeout, resend ",self.seq)
                send_timer+=1
                return self.send_data_event(data)
            else:
                print("close connection")
                self.is_FIN=1
                self.send_data_event(data)

            return

        
    