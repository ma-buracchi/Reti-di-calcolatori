# -*- coding: utf-8 -*-
"""
Created on Thu Nov 20 09:13:42 2014

@author: federicoschipani
"""

import unittest
import socket

class TestSequenceFunctions(unittest.TestCase):

    def setUp(self):
        self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clientSocket.connect( ('127.0.0.1' , 8080) )        

    #TEST SUGLI ERRORI DI SINTASSI   
    def test_syntax_error(self):
        self.clientSocket.sendall("BUBI\r\n")
        result = self.clientSocket.recv(1024)
        self.assertEquals(result, "ERROR\r\n")
        
    def test_syntax_error2(self):
        self.clientSocket.sendall("INIT 1 2 3\r\n")
        result = self.clientSocket.recv(1024)
        self.assertEquals(result, "ERROR\r\n")
        
    def test_syntax_error3(self):
        self.clientSocket.sendall("INIT asd\r\n")
        result = self.clientSocket.recv(1024)
        self.assertEquals(result, "ERROR\r\n")
        
    def test_syntax_error4(self):
        self.clientSocket.sendall("INIT\r\n")
        result = self.clientSocket.recv(1024)
        self.assertEquals(result, "ERROR\r\n")
        
    def test_syntax_error5(self):
        self.clientSocket.sendall("INIT8\r\n")
        result = self.clientSocket.recv(1024)
        self.assertEquals(result, "ERROR\r\n")      
        
    def test_syntax_error6(self):
        self.clientSocket.sendall("init 1\r\n")
        result = self.clientSocket.recv(1024)
        self.assertEquals(result, "ERROR\r\n")
        
    #TEST INIT
        
    def test_init1(self):
        self.clientSocket.sendall("INIT 10\r\n")
        result = self.clientSocket.recv(1024)
        self.assertEquals(result, "OK 0\r\n")
        
    def test_init2(self):
        self.clientSocket.sendall("INIT 1\r\n")
        result = self.clientSocket.recv(1024)
        self.assertEquals(result, "OK 1\r\n")
        
    #TEST ERRORE SUI REGISTRI
    def test_registerError(self):
        self.clientSocket.sendall("SET 1 3 5\r\n")
        result = self.clientSocket.recv(1024)
        self.assertEquals(result, "ERROR\r\n")
        
    #TEST CHIUSURA SESSIONE
    def test_closeSession(self):
        self.clientSocket.sendall("CLOSE 1\r\n")
        result = self.clientSocket.recv(1024)
        self.assertEquals(result, "OK\r\n")
        
    #TEST ERRORE CHIUSURA SESSIONE
    def test_closeSessionError(self):
        self.clientSocket.sendall("CLOSE 3\r\n")
        result = self.clientSocket.recv(1024)
        self.assertEquals(result, "ERROR\r\n")
        
    #TEST ACCESSO A SESSIONE CHIUSA
    def test_closedSession(self):
        self.clientSocket.sendall("STACK 1\r\n")
        result = self.clientSocket.recv(1024)
        self.assertEquals(result, "ERROR\r\n")
        
    #TEST SET 
    def test_set1(self):
        self.clientSocket.sendall("SET 0 0 3\r\n")
        result = self.clientSocket.recv(1024)
        self.assertEquals(result, "OK\r\n")
        
    def test_set2(self):
        self.clientSocket.sendall("SET 0 1 4\r\n")
        result = self.clientSocket.recv(1024)
        self.assertEquals(result, "OK\r\n")
        
    def test_setError1(self):
        self.clientSocket.sendall("SET 0 20 3\r\n")
        result = self.clientSocket.recv(1024)
        self.assertEquals(result, "ERROR\r\n")
        
    def test_setError2(self):
        self.clientSocket.sendall("SET 4 20 3\r\n")
        result = self.clientSocket.recv(1024)
        self.assertEquals(result, "ERROR\r\n")
        
    #TEST GET
    def test_get(self):
        self.clientSocket.sendall("GET 0 0\r\n")
        result = self.clientSocket.recv(1024)
        self.assertEquals(result, "OK 3\r\n")
        
    def test_getError1(self):
        self.clientSocket.sendall("GET 20 1\r\n")
        result = self.clientSocket.recv(1024)
        self.assertEquals(result, "ERROR\r\n")
        
    def test_getError2(self):
        self.clientSocket.sendall("GET 0 40\r\n")
        result = self.clientSocket.recv(1024)
        self.assertEquals(result, "ERROR\r\n")
        
    #TEST OPERAZIONI MATEMATICHE
    #[3 4 0 0 0 ... 0]
    def test_add(self):
        self.clientSocket.sendall("ADD 0 0 1 2\r\n")
        result = self.clientSocket.recv(1024)
        self.assertEquals(result, "OK\r\n")
        
    def test_addResult(self):
        self.clientSocket.sendall("GET 0 2\r\n")
        result = self.clientSocket.recv(1024)
        self.assertEquals(result, "OK 7\r\n")
        
    #[3 4 7 0 0 ... 0]
    def test_sub(self):
        self.clientSocket.sendall("SUB 0 2 1 3\r\n")
        result = self.clientSocket.recv(1024)
        self.assertEquals(result, "OK\r\n")
        
    def test_subResult(self):
        self.clientSocket.sendall("GET 0 3\r\n")
        result = self.clientSocket.recv(1024)
        self.assertEquals(result, "OK 3\r\n")
        
    #[3 4 7 3 0 ... 0]
    def test_mul(self):
        self.clientSocket.sendall("MUL 0 0 2 4\r\n")
        result = self.clientSocket.recv(1024)
        self.assertEquals(result, "OK\r\n")
        
    def test_mulResult(self):
        self.clientSocket.sendall("GET 0 4\r\n")
        result = self.clientSocket.recv(1024)
        self.assertEquals(result, "OK 21\r\n")
        
    #[3 4 7 3 21 ... 0]
    def test_div(self):
        self.clientSocket.sendall("DIV 0 4 0 5\r\n")
        result = self.clientSocket.recv(1024)
        self.assertEquals(result, "OK\r\n")
        
    def test_divResult(self):
        self.clientSocket.sendall("GET 0 5\r\n")
        result = self.clientSocket.recv(1024)
        self.assertEquals(result, "OK 7\r\n")
        
    #[3 4 7 3 21 3 ... 0]
    def test_divZero(self):
        self.clientSocket.sendall("DIV 0 0 6 7\r\n")
        result = self.clientSocket.recv(1024)
        self.assertEquals(result, "ERROR\r\n")
    #TEST PUSH
    #stack:[]
    def test_push1(self):
        self.clientSocket.sendall("PUSH 0 0\r\n")
        result = self.clientSocket.recv(1024)
        self.assertEquals(result, "OK\r\n")
    #stack:[3]    
    def test_push2(self):
        self.clientSocket.sendall("PUSH 0 1\r\n")
        result = self.clientSocket.recv(1024)
        self.assertEquals(result, "OK\r\n")
    #stack: [4 3]
    def test_push3(self):
        self.clientSocket.sendall("PUSH 0 2\r\n")
        result = self.clientSocket.recv(1024)
        self.assertEquals(result, "OK\r\n")
    #stack:[7 4 3] 
    #TEST STACK 
    def test_stack(self):
       self.clientSocket.sendall("STACK 0\r\n")
       result = self.clientSocket.recv(1024)
       self.assertEquals(result, "OK 3 4 7\r\n")
    #TEST POP
    def test_pop(self):
        self.clientSocket.sendall("POP 0 6\r\n")
        result = self.clientSocket.recv(1024)
        self.assertEquals(result, "OK\r\n")
    def test_resultPop(self):
        self.clientSocket.sendall("GET 0 6\r\n")
        result = self.clientSocket.recv(1024)
        self.assertEquals(result, "OK 7\r\n")
    #[3 4 7 3 21 3 7 ... 0]
if __name__ == '__main__':
#    unittest.main()
    loader = unittest.TestLoader()
    ln = lambda f: getattr(TestSequenceFunctions, f).im_func.func_code.co_firstlineno
    lncmp = lambda a, b: cmp(ln(a), ln(b))
    loader.sortTestMethodsUsing = lncmp
    unittest.main(testLoader=loader, verbosity=2)