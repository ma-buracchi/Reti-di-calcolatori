'''
Created on 23/dic/2014

@author: Marco
'''
from random import randint

class TcpProtocol:
    """
    Classe che implementa un 'simulatore' del protocollo TCP lato sender
    """

# con questa classe i test funzionano tutti con qualunque indice di partenza 
# ma devo aggiungere la base a 2 controlli dei test.
    
    def __init__( self , ssthresh , mss , is_reno ):
        self.toSend = []
        self.state = 0 
        # 0 = slow start, 1 = fast recovery, 2 = congestion avoidance
        self.dupAckCount = 0
        self.ssthresh = ssthresh
        self.mss = mss
        self.cwnd = mss
        self.reno = is_reno
        x = randint(5000 , 10000)
        self.nextSeqNum = x
        self.sendBase = x
        self.lastByteSent = x
        
    def send( self , b ):
        self.toSend.append([self.nextSeqNum , b , 0]) # il terzo valore indica
        # lo stato di invio. 0 = non inviato, 1 = inviato in attesa di ack,
        # 2 = ack ricevuto.
        self.nextSeqNum += b
        
    def do_send( self ):
        i = 0
        while i < len(self.toSend) and self.toSend[i][2] != 0:
            i += 1
        if i == len(self.toSend):
            return (-1 , -1)
        else:
            if self.lastByteSent-self.sendBase+self.toSend[i][1] <= self.cwnd:
                self.lastByteSent += self.toSend[i][1]
                self.toSend[i][2] = 1
                return self.toSend[i][0] , self.toSend[i][1]
            else:
                return -1 , -1
        
    def ack( self , n ):
        if n > self.sendBase:
            for pack in self.toSend:
                if pack[0] < n and pack[2] != 2:
                    pack[2] = 2
            self.newAck()
            self.sendBase = n
        elif n == self.sendBase:
            self.duplicateAck(n)
        else:
            self.newAck()
            
    def newAck(self):
        self.dupAckCount = 0
        if self.state == 0:
            self.slowStart()
        elif self.state == 1:
            self.fastRecovery()
        elif self.state == 2:
            self.congestionAvoidance()
        #transmit new segment as allowed
        
    def slowStart(self):
        self.cwnd += self.mss
        if self.cwnd >= self.ssthresh:
            self.state = 2
    
    def fastRecovery(self):
        self.cwnd = self.ssthresh
        self.state = 2
        
    def congestionAvoidance(self):
        self.cwnd += max(1 , (self.mss * self.mss) / self.cwnd)
        
    def duplicateAck(self , n):
        if self.state == 0 or self.state == 2:
            self.dupAckCount += 1
            if self.dupAckCount == 3:
                self.tripleDupAck()
                # retransmit missing segment
        else:
            self.cwnd += self.mss
            # transmit new segment as allowed
    
    def tripleDupAck(self):
        self.ssthresh = self.cwnd / 2
        if self.reno == True:
            self.cwnd , self.state = self.ssthresh + 3*self.mss , 1
        else:
            self.dupAckCount , self.cwnd , self.state = 0 , self.mss , 0
        for pack in self.toSend:
            if pack[2] == 1:
                pack[2] = 0
                self.lastByteSent -= pack[1]
                break
                
    def time_out( self ):
        self.state , self.dupAckCount = 0 , 0
        self.ssthresh , self.cwnd = self.cwnd / 2 , self.mss
        for pack in self.toSend:
            if pack[2] == 1:
                pack[2] = 0
                self.lastByteSent -= pack[1]
                break
        # retransmit missing segment
        return
    
    def get_duplicated_ack_count( self ):
        return self.dupAckCount
    
    def next_to_send( self ):
        for pack in self.toSend:
            if pack[2] == 0 and \
            self.lastByteSent-self.sendBase < self.cwnd:
                return pack[0] , pack[1]
        return self.nextSeqNum , -1
    
    def next_to_ack( self ):
        for pack in self.toSend:
            if pack[2] == 1:
                return pack[0] + pack[1]
        return -1
    
    def get_cwnd( self ):
        return self.cwnd
    
    def get_ssthresh( self ):
        return self.ssthresh