# -*- coding: utf-8 -*-
"""
Created on Sun Nov  2 20:55:05 2014

@author: loreti
"""

import unittest

DEFAULT_SSHTRESH = 64*1024
DEFAULT_MSS = 1460

from MarcoBuracchi2 import TcpProtocol 

class TestTcpSimupator(unittest.TestCase):

    def test_init_reno(self):
        tcp = TcpProtocol( DEFAULT_SSHTRESH , DEFAULT_MSS , True )
        self.assertEqual( tcp.get_ssthresh( ) , DEFAULT_SSHTRESH )
        self.assertEqual( tcp.get_cwnd( ) , DEFAULT_MSS )
        self.assertEqual( tcp.next_to_ack( ) , -1 )
        pack = tcp.next_to_send()
        self.assertEqual( pack[1] , -1 )
        self.assertEqual( tcp.get_duplicated_ack_count( ) , 0 )

    def test_init_tahoe(self):
        tcp = TcpProtocol( DEFAULT_SSHTRESH , DEFAULT_MSS , False )
        self.assertEqual( tcp.get_ssthresh( ) , DEFAULT_SSHTRESH )
        self.assertEqual( tcp.get_cwnd( ) , DEFAULT_MSS )
        self.assertEqual( tcp.next_to_ack( ) , -1 )
        pack = tcp.next_to_send()
        self.assertEqual( pack[1] , -1 )
        self.assertEqual( tcp.get_duplicated_ack_count( ) , 0 )

    def test_send_and_ack_reno(self):
        tcp = TcpProtocol( DEFAULT_SSHTRESH , DEFAULT_MSS , True )
        pack = tcp.next_to_send()
        self.assertEqual( pack[1] , -1 )
        tcp.send( DEFAULT_MSS )
        pack = tcp.next_to_send( )
        self.assertEqual( pack[1] , DEFAULT_MSS )
        self.assertEqual( pack , tcp.do_send( ) )
        self.assertEqual( tcp.next_to_send( ) , (pack[0]+pack[1],-1) )
        self.assertEqual( tcp.next_to_ack( ) , pack[0]+pack[1] )
#         tcp.ack( DEFAULT_MSS )
        # attivare per testare il modulo 2 
        tcp.ack( tcp.sendBase + DEFAULT_MSS )
        self.assertEqual( tcp.next_to_ack( ) , -1 )
        self.assertEqual( tcp.get_cwnd( ) , 2*DEFAULT_MSS )

    def test_send_and_ack_tahoe(self):
        tcp = TcpProtocol( DEFAULT_SSHTRESH , DEFAULT_MSS , False )
        pack = tcp.next_to_send()
        self.assertEqual( pack[1] , -1 )
        tcp.send( DEFAULT_MSS )
        pack = tcp.next_to_send( )
        self.assertEqual( pack[1] , DEFAULT_MSS )
        self.assertEqual( pack , tcp.do_send( ) )
        self.assertEqual( tcp.next_to_send( ) , (pack[0]+pack[1],-1) )
        self.assertEqual( tcp.next_to_ack( ) , pack[0]+pack[1] )
#         tcp.ack( DEFAULT_MSS )
        # attivare per testare il modulo 2 
        tcp.ack( tcp.sendBase + DEFAULT_MSS )
        self.assertEqual( tcp.next_to_ack( ) , -1 )
        self.assertEqual( tcp.get_cwnd( ) , 2*DEFAULT_MSS )

    def test_send_and_ack2_reno(self):
        tcp = TcpProtocol( DEFAULT_SSHTRESH , DEFAULT_MSS , True )
        pack = tcp.next_to_send()
        base = pack[0]
        self.assertEqual( pack[1] , -1 )
        tcp.send( DEFAULT_MSS )
        pack = tcp.next_to_send( )
        self.assertEqual( pack , (base,DEFAULT_MSS) )
        tcp.send( DEFAULT_MSS )
        self.assertEqual( pack , tcp.do_send( ) )
        self.assertEqual( tcp.next_to_send( ) , (base+2*DEFAULT_MSS,-1) )
        tcp.ack( base+DEFAULT_MSS )
        self.assertEqual( tcp.next_to_send( ) , (base+DEFAULT_MSS,DEFAULT_MSS) )
        self.assertEqual( (base+DEFAULT_MSS,DEFAULT_MSS) , tcp.do_send( ) )
        self.assertEqual( tcp.next_to_ack( ) , base+(2*DEFAULT_MSS) )

    def test_send_and_ack2_tahoe(self):
        tcp = TcpProtocol( DEFAULT_SSHTRESH , DEFAULT_MSS , False )
        pack = tcp.next_to_send()
        base = pack[0]
        self.assertEqual( pack[1] , -1 )
        tcp.send( DEFAULT_MSS )
        pack = tcp.next_to_send( )
        self.assertEqual( pack , (base,DEFAULT_MSS) )
        tcp.send( DEFAULT_MSS )
        self.assertEqual( pack , tcp.do_send( ) )
        self.assertEqual( tcp.next_to_send( ) , (base+2*DEFAULT_MSS,-1) )
        tcp.ack( base+DEFAULT_MSS )
        self.assertEqual( tcp.next_to_send( ) , (base+DEFAULT_MSS,DEFAULT_MSS) )
        self.assertEqual( (base+DEFAULT_MSS,DEFAULT_MSS) , tcp.do_send( ) )
        self.assertEqual( tcp.next_to_ack( ) , base+(2*DEFAULT_MSS) )

    def test_cumulative_ack_reno(self):
        packet_size = DEFAULT_MSS/2
        tcp = TcpProtocol( DEFAULT_SSHTRESH , DEFAULT_MSS , True )
        pack = tcp.next_to_send()
        base = pack[0]
        self.assertEqual( pack[1] , -1 )
        tcp.send( packet_size )
        tcp.send( packet_size )
        pack = tcp.next_to_send( )
        self.assertEqual( pack , (base,packet_size) )
        tcp.send( packet_size )
        tcp.do_send( )
        self.assertEqual( tcp.next_to_send( ) , (base+packet_size,packet_size) )
        tcp.do_send( )
        self.assertEqual( tcp.next_to_send( ) , (base+3*packet_size,-1) )
        self.assertEqual( tcp.next_to_ack( ) , base+packet_size )
        tcp.ack( base+2*packet_size )
        self.assertEqual( tcp.next_to_ack( ) , -1 )
        self.assertEqual( tcp.get_cwnd( ) , 2*DEFAULT_MSS )
        tcp.ack( base+packet_size )
        self.assertEqual( tcp.get_cwnd( ) , 3*DEFAULT_MSS )

    def test_cumulative_ack_tahoe(self):
        packet_size = DEFAULT_MSS/2
        tcp = TcpProtocol( DEFAULT_SSHTRESH , DEFAULT_MSS , False )
        pack = tcp.next_to_send()
        base = pack[0]
        self.assertEqual( pack[1] , -1 )
        tcp.send( packet_size )
        tcp.send( packet_size )
        pack = tcp.next_to_send( )
        self.assertEqual( pack , (base,packet_size) )
        tcp.send( packet_size )
        tcp.do_send( )
        self.assertEqual( tcp.next_to_send( ) , (base+packet_size,packet_size) )
        tcp.do_send( )
        self.assertEqual( tcp.next_to_send( ) , (base+3*packet_size,-1) )
        self.assertEqual( tcp.next_to_ack( ) , base+packet_size )
        tcp.ack( base+2*packet_size )
        self.assertEqual( tcp.next_to_ack( ) , -1 )
        self.assertEqual( tcp.get_cwnd( ) , 2*DEFAULT_MSS )
        tcp.ack( base+packet_size )
        self.assertEqual( tcp.get_cwnd( ) , 3*DEFAULT_MSS )

    def test_passage_to_congestion_avoidance_reno( self ):
        packet_size = DEFAULT_MSS
        tcp = TcpProtocol( DEFAULT_SSHTRESH , DEFAULT_MSS , True )
        tcp.send( packet_size )
        pack = tcp.do_send( )
        base = pack[0]
        count = 1
        self.assertEqual( tcp.next_to_ack( ) , base+packet_size )
        while ( tcp.get_cwnd() < DEFAULT_SSHTRESH ):
            tcp.ack( base+(count*packet_size) )
            self.assertEqual( tcp.get_cwnd( ) , (count+1)*DEFAULT_MSS )
            tcp.send( packet_size )
            pack = tcp.do_send(  )
            self.assertEqual( pack , (base+(count*packet_size) , packet_size ) )    
            count += 1
        tcp.ack( base+(count*packet_size) )
        self.assertEqual( tcp.get_cwnd( ) , count*DEFAULT_MSS+max( (DEFAULT_MSS*DEFAULT_MSS)/(count*DEFAULT_MSS) , 1 ) )

    def test_passage_to_congestion_avoidance_tahoe( self ):
        packet_size = DEFAULT_MSS
        tcp = TcpProtocol( DEFAULT_SSHTRESH , DEFAULT_MSS , False )
        tcp.send( packet_size )
        pack = tcp.do_send( )
        base = pack[0]
        count = 1
        self.assertEqual( tcp.next_to_ack( ) , base+packet_size )
        while ( tcp.get_cwnd() < DEFAULT_SSHTRESH ):
            tcp.ack( base+(count*packet_size) )
            self.assertEqual( tcp.get_cwnd( ) , (count+1)*DEFAULT_MSS )
            tcp.send( packet_size )
            pack = tcp.do_send(  )
            self.assertEqual( pack , (base+(count*packet_size) , packet_size ) )    
            count += 1
        tcp.ack( base+(count*packet_size) )
        self.assertEqual( tcp.get_cwnd( ) , count*DEFAULT_MSS+max( (DEFAULT_MSS*DEFAULT_MSS)/(count*DEFAULT_MSS) , 1 ) )

    def test_time_out_reno( self ):
        packet_size = DEFAULT_MSS
        tcp = TcpProtocol( DEFAULT_SSHTRESH , DEFAULT_MSS , True )
        tcp.send( packet_size )
        pack = tcp.do_send( )
        base = pack[0]
        self.assertEqual( tcp.next_to_ack( ) , base+packet_size )
        for count in range(1,25):
            tcp.ack( base+(count*packet_size) )
            self.assertEqual( tcp.get_cwnd( ) , (count+1)*DEFAULT_MSS )
            tcp.send( packet_size )
            pack = tcp.do_send(  )
            self.assertEqual( pack , (base+(count*packet_size) , packet_size ) )    
        tcp.ack( base+(count*packet_size) )
        cwnd = tcp.get_cwnd()
        tcp.time_out()
        self.assertEqual( tcp.get_ssthresh() , cwnd/2 )        
        self.assertEqual( tcp.get_cwnd() , DEFAULT_MSS )
        
    def test_time_out_tahoe( self ):
        packet_size = DEFAULT_MSS
        tcp = TcpProtocol( DEFAULT_SSHTRESH , DEFAULT_MSS , False )
        tcp.send( packet_size )
        pack = tcp.do_send( )
        base = pack[0]
        self.assertEqual( tcp.next_to_ack( ) , base+packet_size )
        for count in range(1,25):
            tcp.ack( base+(count*packet_size) )
            self.assertEqual( tcp.get_cwnd( ) , (count+1)*DEFAULT_MSS )
            tcp.send( packet_size )
            pack = tcp.do_send(  )
            self.assertEqual( pack , (base+(count*packet_size) , packet_size ) )    
        tcp.ack( base+(count*packet_size) )
        cwnd = tcp.get_cwnd()
        tcp.time_out()
        self.assertEqual( tcp.get_ssthresh() , cwnd/2 )
        self.assertEqual( tcp.get_cwnd() , DEFAULT_MSS )       
        
    def test_fast_recovery_reno( self ):        
        packet_size = DEFAULT_MSS/4
        tcp = TcpProtocol( DEFAULT_SSHTRESH , DEFAULT_MSS , True )
        pack = tcp.next_to_send( )
        base = pack[0]
        self.assertEqual( pack[1] , -1 )
        tcp.send( packet_size )
        tcp.send( packet_size )
        tcp.send( packet_size )
        tcp.send( packet_size )
        pack = tcp.next_to_send( )
        self.assertEqual( pack , (base,packet_size) )
        self.assertEqual( tcp.do_send( ) , pack )
        self.assertEqual( tcp.next_to_send( ) , (base+packet_size,packet_size) )
        self.assertEqual( tcp.do_send( ) , (base+packet_size,packet_size) )
        self.assertEqual( tcp.next_to_send( ) , (base+2*packet_size,packet_size) )
        self.assertEqual( tcp.do_send( ) , (base+2*packet_size,packet_size) )
        self.assertEqual( tcp.next_to_send( ) , (base+3*packet_size,packet_size) )
        self.assertEqual( tcp.do_send( ) , (base+3*packet_size,packet_size) )
        tcp.ack( base+packet_size )  
        tcp.ack( base+packet_size )  
        tcp.ack( base+packet_size )  
        self.assertEqual( tcp.get_duplicated_ack_count( ) , 2 )
        tcp.ack( base+packet_size )  
        self.assertEqual( tcp.get_duplicated_ack_count( ) , 3 )
        self.assertEqual( tcp.get_cwnd( ) , DEFAULT_MSS+3*DEFAULT_MSS  )
        self.assertEqual( tcp.next_to_send() , (base+packet_size,packet_size))

    def test_fast_recovery_reno2( self ):        
        packet_size = DEFAULT_MSS/4
        tcp = TcpProtocol( DEFAULT_SSHTRESH , DEFAULT_MSS , True )
        pack = tcp.next_to_send( )
        base = pack[0]
        self.assertEqual( pack[1] , -1 )
        tcp.send( packet_size )
        tcp.send( packet_size )
        tcp.send( packet_size )
        tcp.send( packet_size )
        pack = tcp.next_to_send( )
        self.assertEqual( pack , (base,packet_size) )
        self.assertEqual( tcp.do_send( ) , pack )
        self.assertEqual( tcp.next_to_send( ) , (base+packet_size,packet_size) )
        self.assertEqual( tcp.do_send( ) , (base+packet_size,packet_size) )
        self.assertEqual( tcp.next_to_send( ) , (base+2*packet_size,packet_size) )
        self.assertEqual( tcp.do_send( ) , (base+2*packet_size,packet_size) )
        self.assertEqual( tcp.next_to_send( ) , (base+3*packet_size,packet_size) )
        self.assertEqual( tcp.do_send( ) , (base+3*packet_size,packet_size) )
        tcp.ack( base+packet_size )  
        tcp.ack( base+packet_size )  
        tcp.ack( base+packet_size )  
        self.assertEqual( tcp.get_duplicated_ack_count( ) , 2 )
        tcp.ack( base+packet_size )  
        self.assertEqual( tcp.get_duplicated_ack_count( ) , 3 )
        self.assertEqual( tcp.get_cwnd( ) , DEFAULT_MSS+3*DEFAULT_MSS  )
        self.assertEqual( tcp.next_to_send() , (base+packet_size,packet_size))
        tcp.ack( base+packet_size )  
        tcp.ack( base+4*packet_size )  
        self.assertEqual( tcp.get_cwnd( ) , DEFAULT_MSS )
        
    def test_fast_recovery_reno3( self ):        
        packet_size = DEFAULT_MSS/4
        tcp = TcpProtocol( DEFAULT_SSHTRESH , DEFAULT_MSS , True )
        pack = tcp.next_to_send( )
        base = pack[0]
        self.assertEqual( pack[1] , -1 )
        tcp.send( packet_size )
        tcp.send( packet_size )
        tcp.send( packet_size )
        tcp.send( packet_size )
        pack = tcp.next_to_send( )
        self.assertEqual( pack , (base,packet_size) )
        self.assertEqual( tcp.do_send( ) , pack )
        self.assertEqual( tcp.next_to_send( ) , (base+packet_size,packet_size) )
        self.assertEqual( tcp.do_send( ) , (base+packet_size,packet_size) )
        self.assertEqual( tcp.next_to_send( ) , (base+2*packet_size,packet_size) )
        self.assertEqual( tcp.do_send( ) , (base+2*packet_size,packet_size) )
        self.assertEqual( tcp.next_to_send( ) , (base+3*packet_size,packet_size) )
        self.assertEqual( tcp.do_send( ) , (base+3*packet_size,packet_size) )
        tcp.ack( base+packet_size )  
        tcp.ack( base+packet_size )  
        tcp.ack( base+packet_size )  
        self.assertEqual( tcp.get_duplicated_ack_count( ) , 2 )
        tcp.ack( base+packet_size )  
        self.assertEqual( tcp.get_duplicated_ack_count( ) , 3 )
        self.assertEqual( tcp.get_cwnd( ) , DEFAULT_MSS+3*DEFAULT_MSS  )
        self.assertEqual( tcp.next_to_send() , (base+packet_size,packet_size))
        tcp.ack( base+packet_size )  
        tcp.ack( base+4*packet_size )  
        self.assertEqual( tcp.get_cwnd( ) , DEFAULT_MSS ) 
        tcp.do_send( )
        self.assertEqual( tcp.next_to_send( ) , (base+4*packet_size,-1) )
        
    def test_fast_recovery_reno4( self ):
        packet_size = DEFAULT_MSS
        tcp = TcpProtocol( DEFAULT_SSHTRESH , DEFAULT_MSS , True )
        tcp.send( packet_size )
        pack = tcp.do_send( )
        base = pack[0]
        self.assertEqual( tcp.next_to_ack( ) , base+packet_size )
        count = 1
        self.assertEqual( tcp.next_to_ack( ) , base+packet_size )
        while ( tcp.get_cwnd() < DEFAULT_SSHTRESH ):
            tcp.ack( base+(count*packet_size) )
            self.assertEqual( tcp.get_cwnd( ) , (count+1)*DEFAULT_MSS )
            tcp.send( packet_size )
            pack = tcp.do_send(  )
            self.assertEqual( pack , (base+(count*packet_size) , packet_size ) )    
            count += 1
        tcp.ack( base+(count*packet_size) )
        cwnd = tcp.get_cwnd( )
        self.assertEqual( cwnd , count*DEFAULT_MSS+max( (DEFAULT_MSS*DEFAULT_MSS)/(count*DEFAULT_MSS) , 1 ) )
        tcp.send( packet_size )
        tcp.do_send(  )
        tcp.ack( base+(count*packet_size) )
        tcp.ack( base+(count*packet_size) )
        tcp.ack( base+(count*packet_size) )
        self.assertEqual( tcp.get_duplicated_ack_count( ) , 3 )
        self.assertEqual( tcp.get_ssthresh( ) , cwnd/2 )
        self.assertEqual( tcp.get_cwnd( ) , (cwnd/2)+3*DEFAULT_MSS  )        
        tcp.ack( base+((count+1)*packet_size) )
        self.assertEqual( tcp.get_ssthresh() , cwnd/2 )
        self.assertEqual( tcp.get_cwnd() , tcp.get_ssthresh( ) )    
        
    def test_fast_recovery_tahoe( self ):        
        packet_size = DEFAULT_MSS/4
        tcp = TcpProtocol( DEFAULT_SSHTRESH , DEFAULT_MSS , False )
        pack = tcp.next_to_send( )
        base = pack[0]
        self.assertEqual( pack[1] , -1 )
        tcp.send( packet_size )
        tcp.send( packet_size )
        tcp.send( packet_size )
        tcp.send( packet_size )
        pack = tcp.next_to_send( )
        self.assertEqual( pack , (base,packet_size) )
        self.assertEqual( tcp.do_send( ) , pack )
        self.assertEqual( tcp.next_to_send( ) , (base+packet_size,packet_size) )
        self.assertEqual( tcp.do_send( ) , (base+packet_size,packet_size) )
        self.assertEqual( tcp.next_to_send( ) , (base+2*packet_size,packet_size) )
        self.assertEqual( tcp.do_send( ) , (base+2*packet_size,packet_size) )
        self.assertEqual( tcp.next_to_send( ) , (base+3*packet_size,packet_size) )
        self.assertEqual( tcp.do_send( ) , (base+3*packet_size,packet_size) )
        tcp.ack( base+packet_size )  
        tcp.ack( base+packet_size )  
        tcp.ack( base+packet_size )  
        self.assertEqual( tcp.get_duplicated_ack_count( ) , 2 )
        tcp.ack( base+packet_size )  
        self.assertEqual( tcp.get_duplicated_ack_count( ) , 0 )
        self.assertEqual( tcp.get_cwnd( ) , DEFAULT_MSS  )
        self.assertEqual( tcp.next_to_send() , (base+packet_size,packet_size))            

    def test_fast_recovery_tahoe2( self ):        
        packet_size = DEFAULT_MSS/4
        tcp = TcpProtocol( DEFAULT_SSHTRESH , DEFAULT_MSS , False )
        pack = tcp.next_to_send( )
        base = pack[0]
        self.assertEqual( pack[1] , -1 )
        tcp.send( packet_size )
        tcp.send( packet_size )
        tcp.send( packet_size )
        tcp.send( packet_size )
        pack = tcp.next_to_send( )
        self.assertEqual( pack , (base,packet_size) )
        self.assertEqual( tcp.do_send( ) , pack )
        self.assertEqual( tcp.next_to_send( ) , (base+packet_size,packet_size) )
        self.assertEqual( tcp.do_send( ) , (base+packet_size,packet_size) )
        self.assertEqual( tcp.next_to_send( ) , (base+2*packet_size,packet_size) )
        self.assertEqual( tcp.do_send( ) , (base+2*packet_size,packet_size) )
        self.assertEqual( tcp.next_to_send( ) , (base+3*packet_size,packet_size) )
        self.assertEqual( tcp.do_send( ) , (base+3*packet_size,packet_size) )
        tcp.ack( base+packet_size )  
        tcp.ack( base+packet_size )  
        tcp.ack( base+packet_size )  
        self.assertEqual( tcp.get_duplicated_ack_count( ) , 2 )
        tcp.ack( base+packet_size )  
        self.assertEqual( tcp.get_duplicated_ack_count( ) , 0 )
        self.assertEqual( tcp.get_cwnd( ) , DEFAULT_MSS  )
        self.assertEqual( tcp.next_to_send() , (base+packet_size,packet_size))    
        tcp.ack( base+packet_size )  
        self.assertEqual( tcp.get_duplicated_ack_count() , 1 )
        tcp.ack( base+4*packet_size )  
        self.assertEqual( tcp.get_cwnd( ) , 2*DEFAULT_MSS )
        self.assertEqual( tcp.get_duplicated_ack_count() , 0 )

if __name__ == '__main__':
    unittest.main()
