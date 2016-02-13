'''
Created on 14/nov/2014

@author: Marco Buracchi
'''

def checkReg( regs , n):
    for x in regs:
        if x not in range( n ):
            return 1
    return 0
    
def isZero( i ):
    if i == 0:
        return 1
    else:
        return 0
    
def push( line , parameters ):
    if checkReg( [int( line[1] )] , len( parameters['regs'] ) ):
        return "ERROR"
    else:
        parameters['stack'].append( parameters['regs'][int( line[1] )] )
        return "OK"

def pop( line , parameters ):
    if checkReg( [int( line[1] )] , len( parameters['regs'] ) ) or \
    isZero( len( parameters['stack'] ) ):
        return "ERROR"
    else:
        parameters['regs'][int( line[1] )] = parameters['stack'].pop()
        return "OK"

def add( line , parameters ):
    if checkReg( [int(line[1] ) , int( line[2] ) , int( line[3] )] , \
    len( parameters['regs'] ) ):
        return "ERROR"
    else:
        parameters['regs'][int( line[3] )] = parameters['regs'][int( line[1] )]\
        + parameters['regs'][int( line[2] )]
        return "OK"
    
def sub( line , parameters ):
    if checkReg( [int( line[1] ) , int( line[2] ) , int( line[3] )] , \
    len( parameters['regs'] ) ):
        return "ERROR"
    else:
        parameters['regs'][int( line[3] )] = parameters['regs'][int( line[1] )]\
        - parameters['regs'][int( line[2] )]
        return "OK"
    
def div( line , parameters ):
    if checkReg( [int( line[1] ) , int( line[2] ) , int( line[3] )] , \
    len( parameters['regs'] ) ) or isZero( parameters['regs'][int( line[2] )] ):
            return "ERROR"
    else :
        parameters['regs'][int( line[3] )] = parameters['regs'][int( line[1] )]\
        / parameters['regs'][int( line[2] )]
        return "OK"
    
def mul( line , parameters ):
    if checkReg( [ int( line[1] ) , int( line[2] ) , int( line[3] ) ] , \
    len( parameters['regs'] ) ):
        return "ERROR"
    else:
        parameters['regs'][int( line[3] )] = parameters['regs'][int( line[1] )]\
        * parameters['regs'][int( line[2] )]
        return "OK"

def inputStream( line , parameters ):
    if checkReg( [int( line[1] )] , len( parameters['regs'] ) ) or \
    isZero( len( parameters['sin'] ) ):
        return "ERROR"
    else:
        parameters['regs'][int( line[1] )] = parameters['sin'].pop( 0 )
        return "OK"
    
def outputStream( line , parameters ):
    if checkReg( [int( line[1] )] , len( parameters['regs'] ) ):
        return "ERROR"
    else:
        parameters['sout'].insert( 0, parameters['regs'][int( line[1] )] )
        return "OK"

def exitPrg( line , parameters ):
    return "EXIT"

operazioni = { 
    'PUSH': push ,
    'POP' : pop ,
    'ADD' : add , 
    'SUB' : sub , 
    'DIV' : div ,
    'MUL' : mul ,
    'INPUT' : inputStream ,
    'OUTPUT' : outputStream ,
    'EXIT' : exitPrg
}

def runSMProgram ( prg , stack , regs , sin , sout ):
    parameters = {'stack':stack , 'regs':regs , 'sin':sin , 'sout':sout}
    result = fileReader( prg , parameters )
    return result
    
def fileReader( prg , parameters ):
    f = open( prg, 'r' )
    for line in f:
        result = executeLine( line.split() , parameters )
        if result == 'ERROR':
            return 'ERROR'
        elif result == 'EXIT':
            return 'OK'
    return 'OK'
               
def executeLine ( line , parameters ):
    if line[0] in operazioni.keys():
        result = operazioni[line[0]]( line , parameters )
        return result
    else:
        return "ERROR"
        