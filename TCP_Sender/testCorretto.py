# -*- coding: utf-8 -*-
"""
Created on Sun Nov  2 20:55:05 2014

@author: loreti
"""

from MarcoBuracchi import TcpProtocol
import unittest
import sys


class TestSequenceFunctions(unittest.TestCase):

#     def test01(self):                
#         tcp = TcpProtocol(1024,128, True)
#         tcp.send(100)
#         tcp.send(80)
#         tcp.send(20)
#         n, b = tcp.do_send()
#         self.assertEqual( b , 100 )
#         n1, b1 = tcp.do_send()
#         self.assertEqual( b1 , -1 )  

#     def test02(self):                
#         tcp = TcpProtocol(1024,128, True)
#         tcp.send(20)
#         tcp.send(80)
#         tcp.send(20)
#         n, b = tcp.do_send()
#         self.assertEqual( b , 20 )
#         n1, b1 = tcp.do_send()
#         self.assertEqual( b1 , 80 )     
 
#     def test03(self):
#         tcp = TcpProtocol(500, 100, True)
#         tcp.send(10)
#         n,b = tcp.do_send()  
#         x = tcp.next_to_ack()
#         self.assertEqual(x, n+b)
#  
#     def test04(self):
#         tcp = TcpProtocol(500, 100, True)
#         tcp.send(10)
#         self.assertEqual(tcp.get_cwnd(), 100)
#         self.assertEqual(tcp.get_ssthresh(), 500)
#         tcp.do_send()  
#         self.assertEqual(tcp.get_cwnd(), 100)
#         self.assertEqual(tcp.get_ssthresh(), 500)
#         x = tcp.next_to_ack()
#         self.assertEqual(tcp.get_cwnd(), 100)
#         self.assertEqual(tcp.get_ssthresh(), 500)
#         tcp.ack(x)
#         self.assertEqual(tcp.get_cwnd(), 200)
#         self.assertEqual(tcp.get_ssthresh(), 500)
#          
#     def test05(self):
#         tcp = TcpProtocol(100, 100, True)
#         tcp.send(10)
#         self.assertEqual(tcp.get_cwnd(), 100)
#         self.assertEqual(tcp.get_ssthresh(), 100)
#         tcp.do_send()  
#         self.assertEqual(tcp.get_cwnd(), 100)
#         self.assertEqual(tcp.get_ssthresh(), 100)
#         x = tcp.next_to_ack()
#         self.assertEqual(tcp.get_cwnd(), 100)
#         self.assertEqual(tcp.get_ssthresh(), 100)
#         tcp.ack(x)
#         self.assertEqual(tcp.get_cwnd(), 200)
#         self.assertEqual(tcp.get_ssthresh(), 100)
#       
#         tcp.send(20)
#         self.assertEqual(tcp.get_cwnd(), 200)
#         self.assertEqual(tcp.get_ssthresh(), 100)
#         n,b = tcp.do_send()  
#         self.assertEqual(tcp.get_cwnd(), 200)
#         self.assertEqual(tcp.get_ssthresh(), 100)
#         x = tcp.next_to_ack()
#         self.assertEqual(x, n+b)
#         self.assertEqual(tcp.get_cwnd(), 200)
#         self.assertEqual(tcp.get_ssthresh(), 100)
#         tcp.ack(x)
#         self.assertEqual(tcp.get_cwnd(), 250)
#         self.assertEqual(tcp.get_ssthresh(), 100)
#          
#     def test06(self):
#         tcp = TcpProtocol(500, 80, True)
#         tcp.send(10)
#              
#         tcp.do_send()  
#              
#         x = tcp.next_to_ack()
#              
#         tcp.ack(x)
#              
#         self.assertEqual(tcp.get_cwnd(), 160)
#      
#         tcp.send(10)
#              
#         tcp.do_send()  
#              
#         x = tcp.next_to_ack()
#              
#         tcp.ack(x)
#      
#         self.assertEqual(tcp.get_cwnd(), 240)
#              
#      
#         tcp.send(20)
#         tcp.do_send()
#         tcp.time_out()
#              
#         self.assertEqual(tcp.get_cwnd(), 80)
#         self.assertEqual(tcp.get_ssthresh(), 120)
#           
#     def test07(self):
#         tcp = TcpProtocol(500, 80, False)
#         tcp.send(10)
#              
#         tcp.do_send()  
#              
#         x = tcp.next_to_ack()
#              
#         tcp.ack(x)
#              
#         self.assertEqual(tcp.get_cwnd(), 160)
#      
#         tcp.send(10)
#              
#         tcp.do_send()  
#              
#         x = tcp.next_to_ack()
#              
#         tcp.ack(x)
#      
#         self.assertEqual(tcp.get_cwnd(), 240)
#              
#      
#         tcp.send(20)
#         tcp.do_send()
#         tcp.time_out()
#              
#         self.assertEqual(tcp.get_cwnd(), 80)
#         self.assertEqual(tcp.get_ssthresh(), 120)
  
#     def test08(self):
#         tcp = TcpProtocol(500, 80, False)
#         tcp.send(10)
#              
#         tcp.do_send()  
#              
#         x = tcp.next_to_ack()
#              
#         tcp.ack(x)
#              
#         self.assertEqual(tcp.get_cwnd(), 160)
#      
#         tcp.send(10)
#              
#         tcp.do_send()  
#              
#         x = tcp.next_to_ack()
#              
#         tcp.ack(x)
#      
#         self.assertEqual(tcp.get_cwnd(), 240)
#              
#      
#         tcp.send(20)
#         tcp.do_send()
#         tcp.ack(x)
#      
#         self.assertEqual(tcp.get_cwnd(), 240)
#         self.assertEqual(tcp.get_ssthresh(), 500)
#              
#         tcp.time_out()
#      
#         self.assertEqual(tcp.get_cwnd(), 80)
#         self.assertEqual(tcp.get_ssthresh(), 120)
#   
#     def test09(self):
#         tcp = TcpProtocol(500, 80, False)
#         tcp.send(10)
#              
#         tcp.do_send()  
#              
#         x = tcp.next_to_ack()
#              
#         tcp.ack(x)
#              
#         self.assertEqual(tcp.get_cwnd(), 160)
#      
#         tcp.send(10)
#              
#         tcp.do_send()  
#              
#         x = tcp.next_to_ack()
#              
#         tcp.ack(x)
#      
#         self.assertEqual(tcp.get_cwnd(), 240)
#              
#      
#         tcp.send(20)
#         tcp.do_send()
#         tcp.ack(x)
#         tcp.ack(x)
#         tcp.ack(x)
#         self.assertEqual(tcp.get_cwnd(), 80)
#         self.assertEqual(tcp.get_ssthresh(), 120)
#           
#     def test10(self):
#         tcp = TcpProtocol(500, 80, True)
#         tcp.send(10)
#              
#         tcp.do_send()  
#              
#         x = tcp.next_to_ack()
#              
#         tcp.ack(x)
#              
#         self.assertEqual(tcp.get_cwnd(), 160)
#      
#         tcp.send(10)
#              
#         tcp.do_send()  
#              
#         x = tcp.next_to_ack()
#              
#         tcp.ack(x)
#      
#         self.assertEqual(tcp.get_cwnd(), 240)
#              
#      
#         tcp.send(20)
#         tcp.do_send()
#         tcp.ack(x)
#         tcp.ack(x)
#         tcp.ack(x)
#         self.assertEqual(tcp.get_ssthresh(), 120)
#   
#     def test11(self):
#         tcp = TcpProtocol(500, 80, True)
#         tcp.send(10)
#              
#         tcp.do_send()  
#              
#         x = tcp.next_to_ack()
#              
#         tcp.ack(x)
#              
#         self.assertEqual(tcp.get_cwnd(), 160)
#      
#         tcp.send(10)
#              
#         tcp.do_send()  
#              
#         x = tcp.next_to_ack()
#              
#         tcp.ack(x)
#      
#         self.assertEqual(tcp.get_cwnd(), 240)
#              
#      
#         tcp.send(20)
#         tcp.do_send()
#         tcp.ack(x)
#         tcp.ack(x)
#         tcp.ack(x)
#         self.assertEqual(tcp.get_ssthresh(), 120)
#         self.assertEqual(tcp.get_cwnd(), 360)
#              
#      
#         tcp.ack(x)
#      
#         self.assertEqual(tcp.get_cwnd(), 360+80)
#         self.assertEqual(tcp.get_ssthresh(), 120)
#   
    def test12(self):
        tcp = TcpProtocol(500, 80, False)
        tcp.send(10)
             
        tcp.do_send()  
             
        x = tcp.next_to_ack()
             
        tcp.ack(x)
             
        self.assertEqual(tcp.get_cwnd(), 160)
     
        tcp.send(10)
             
        tcp.do_send()  
             
        x = tcp.next_to_ack()
             
        tcp.ack(x)
     
        self.assertEqual(tcp.get_cwnd(), 240)
             
     
        tcp.send(20)
        tcp.do_send()
        tcp.ack(x)
        tcp.ack(x)
        tcp.ack(x)
        self.assertEqual(tcp.get_cwnd(), 80)
        self.assertEqual(tcp.get_ssthresh(), 120)
     
        tcp.ack(x)
     
        self.assertEqual(tcp.get_cwnd(), 80)
        self.assertEqual(tcp.get_ssthresh(), 120)
 
if __name__ == '__main__':
    unittest.main()
