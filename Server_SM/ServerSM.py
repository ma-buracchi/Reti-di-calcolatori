'''
Created on 15/nov/2014

@author: Marco
'''

import socket
import sys

class Sessione:
    """
    Classe che rappresenta ogni sessione:
    Il costruttore prende come parametro un intero k e crea la nuova sessione
    assegnandole un ID univoco ed una lista di k registri inizialmente
    settati a 0.     
    
    campi:
    - num = ID di sessione
    - registri = coda dei registri
    - stack = stack di valori   
    """
    cont = -1
    
    def __init__( self , k ):
        """
        Costruttore per la classe Sessione che prende come parametro
        un intero k e crea una nuova sessione assegnandole un ID
        univoco ed una lista di k registri inizialmente settati a 0.
        """
        if k < 0:
            raise LessThanZeroRegError("Il numero di registri deve essere >= 0.")
        self.__class__.cont += 1
        self.num = self.__class__.cont
        self.registri = [0] * k
        self.stack = []

class Box:
    """
    Classe contenitore:
    Il costruttore crea una lista vuota.     
    campi:
    - box = una lista di elementi
    metodi:
    - addSessione( self , sessione )
    aggiunge in coda alla lista la sessione data come parametro.
    - findSessione ( self, idSessione )
    cerca l'ID sessione passato nella sua lista di sessioni;
    se la sessione e' presente, restituisce l'indice corrispondente
    nella lista delle sessioni, altrimenti
    solleva una SessionNotFoundError Exception.
    """
    def __init__( self ):
        """
        Il costruttore della classe box.
        Crea una lista vuota
        """
        self.box = []
    
    def addSessione( self , sessione ):
        """
        aggiunge in coda alla lista la sessione data come parametro.
        """
        self.box.append(sessione)
        
    def findSessione(self , idSessione):
        """
        cerca l'ID sessione passato nella sua lista di sessioni;
        se la sessione e' presente, restituisce l'indice corrispondente
        nella lista delle sessioni, altrimenti
        solleva una SessionNotFoundError Exception.
        """
        i = 0
        sessione = self.box[i]
        while i < len(self.box) \
        and sessione.num != idSessione:
            i += 1
            if i == len(self.box):
                raise SessionNotFoundError("Sessione non trovata")
            sessione = self.box[i]
        return i
    
class Error( Exception ):
    """Classe base per le eccezioni definite in questo modulo."""
    pass

class SessionNotFoundError( Error ):
    """Eccezione sollevata quando la sessione cercata non esiste"""
    pass

class LessThanZeroRegError( Error ):
    """Eccezione sollevata perche' si cerca di accedere ad un registro < 0"""
    pass

class InvalidOperationError( Error ):
    """Eccezione sollevata perche' si cerca di eseguire un'operazione non
    prevista dal programma"""
    pass

class ParametersError ( Error ):
    """Eccezione sollevata perche' il numero di parametri forniti
    all'operazione e' sbagliato"""
    pass
    
def start( host , port , listen ):
    """Inizializza la socket, la coda listen ed effettua il bind, restituendo
    la socket cosi' creata
    """
    print 'Starting...'
    sm_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sm_socket.bind((host, port))
    sm_socket.listen( listen )
    print 'Server started at ',host,port
    return sm_socket

def run( sm_socket ):
    """Attende le connessioni e gestisce le richieste dei clienti.
    Restituisce ERROR se durante l'esecuzione dei comandi viene sollevata
    un'eccezione
    """
    while True:
        print 'Accepting connections...'
        client,addr = sm_socket.accept()
        print 'Connection established from ',addr
        try:
            handle_client( client )
        except Exception:
            client.send("ERROR\r\n")
            client.close()
            # il server restuisce ERROR se viene sollevata
            # una qualsiasi eccezione ma sarebbe possibile 
            # implementare gestioni ad hoc per ogni tipo 
            # di eccezione.
#         except SessionNotFoundError:
#             client.send("ERROR: SESSIONE NON TROVATA\r\n")
#             client.close()
#         except LessThanZeroRegError:
#             client.send("ERROR: INSERITO REGISTRO < 0\r\n")
#             client.close()
#         except InvalidOperationError:
#             client.send("ERROR: OPERAZIONE NON VALIDA\r\n")
#             client.close()
#         except ParametersError:
#             client.send("ERROR: INSERITO UN NUMERO DI PARAMETRI ERRATO\r\n")
#             client.close()
#         except IndexError:
#             client.send("ERROR: INSERITO UN INDICE FUORI DAL RANGE\r\n")
#             client.close()  
#         except Exception:
#             client.send("ERROR\r\n")
#             client.close()
        
def handle_client( sm_client ):
    """Passa il cliente in input al raccoglitore di richieste, passa la richiesta
    al gestore di richieste e, in caso di successo, restituisce il messaggio 
    appropriato al cliente e chiude la connessione
    """
    request = collect_request( sm_client )
    result = handle_request(request)
    sm_client.send(result)
    sm_client.close()
    
def collect_request( sm_client ):
    """Con un cliente in input, ne raccoglie la richiesta, la passa al gestore
    di richieste e, in caso di successo, restituisce il messaggio appropriato
    al cliente e chiude la connessione
    """
    request = ""
    while not request.endswith('\r\n'):
        data = sm_client.recv( 1024 )
        request = request + data
    return request

def handle_request( request ):
    """Con una richiesta in input, controlla che la prima parola sia una
    operazione contemplata. In caso di successo passa la richiesta all'operazione
    adeguata e restituisce il messaggio appropriato,
    altrimenti solleva una InvalidOperationError Exception
    """
    splitted_request = request.split()
    if splitted_request[0] not in operazioni:
        raise InvalidOperationError("L'operazione non e' eseguibile")
    result = operazioni[splitted_request[0]](splitted_request)
    return result
    
def init( splitted_request ):
    """Con una richiesta 'INIT n' in input, crea una nuova sessione inizializzando
    un numero di registri pari a n, aggiungendola alla lista di sessioni.
    Restituisce 'OK k' dove k e' l'ID della sessione creata o solleva eccezioni.
    """
    if len(splitted_request) != 2:
        raise ParametersError("Numero di parametri errato")
    nuova_sessione = Sessione( int(splitted_request[1]) )
    boxSessioni.addSessione(nuova_sessione)
    return "OK %i\r\n" %nuova_sessione.num

def close( splitted_request ):
    """Con una richiesta 'CLOSE n' in input, chiude la sessione n, rimuovendola 
    dalla lista di sessioni.
    Restituisce 'OK' o solleva eccezioni.
    """
    if len(splitted_request) != 2:
        raise ParametersError("Numero di parametri errato")
    i = boxSessioni.findSessione( int(splitted_request[1]) )
    del boxSessioni.box[i]
    return "OK\r\n"

def push( splitted_request ):
    """Con una richiesta 'PUSH n i' in input, nella sessione n, inserisce in 
    fondo allo stack il valore contenuto nel registro i-esimo.
    Restituisce 'OK' o solleva eccezioni.
    """
    if len(splitted_request) != 3:
        raise ParametersError("Numero di parametri errato")
    n = int(splitted_request[1])  
    i = int(splitted_request[2]) 
    s = boxSessioni.findSessione( n )
    sessione_corrente = boxSessioni.box[s]
    if i < 0:
        raise LessThanZeroRegError("Inserito registro minore di 0")
    sessione_corrente.stack.append( sessione_corrente.registri[i] )
    return "OK\r\n"

def pop( splitted_request ):
    """Con una richiesta 'POP n i' in input, nella sessione n, rimuove il primo 
    elemento dallo stack salvandolo nel registro i-esimo.
    Restituisce 'OK' o solleva eccezioni.
    """
    if len(splitted_request) != 3:
        raise ParametersError("Numero di parametri errato")
    n = int(splitted_request[1])  
    i = int(splitted_request[2]) 
    s = boxSessioni.findSessione( n )
    sessione_corrente = boxSessioni.box[s]
    if i < 0:
        raise LessThanZeroRegError("Inserito registro minore di 0")
    sessione_corrente.registri[i] = 0
    sessione_corrente.registri[i] = sessione_corrente.stack.pop()
    return "OK\r\n"

def add( splitted_request ):
    """Con una richiesta 'ADD n i j k' in input, nella sessione n, somma i
    valori del registro i-esimo e j-esimo salvando il risultato
    nel registro k-esimo.
    Restituisce 'OK' o solleva eccezioni.
    """
    if len(splitted_request) != 5:
        raise ParametersError("Numero di parametri errato")
    n = int(splitted_request[1])  
    i = int(splitted_request[2]) 
    j = int(splitted_request[3])
    k = int(splitted_request[4])
    s = boxSessioni.findSessione( n )
    sessione_corrente = boxSessioni.box[s]
    if any(x < 0 for x in (i,j,k)):
        raise LessThanZeroRegError("Inserito registro minore di 0")
    sessione_corrente.registri[k] = sessione_corrente.registri[i]\
    + sessione_corrente.registri[j]
    return"OK\r\n"

def sub( splitted_request ):
    """Con una richiesta 'SUB n i j k' in input, nella sessione n, sottrae il
    valore del registro j-esimo dal registro i-esimo salvando il risultato
    nel registro k-esimo.
    Restituisce 'OK' o solleva eccezioni.
    """
    if len(splitted_request) != 5:
        raise ParametersError("Numero di parametri errato")
    n = int(splitted_request[1])  
    i = int(splitted_request[2]) 
    j = int(splitted_request[3])
    k = int(splitted_request[4])
    s = boxSessioni.findSessione( n )
    sessione_corrente = boxSessioni.box[s]
    if any(x < 0 for x in (i,j,k)):
        raise LessThanZeroRegError("Inserito registro minore di 0")
    sessione_corrente.registri[k] = sessione_corrente.registri[i]\
    - sessione_corrente.registri[j]
    return"OK\r\n"  

def mul( splitted_request ):
    """Con una richiesta 'ADD n i j k' in input, nella sessione n, esegue il prodotto
    tra i valori del registro i-esimo e j-esimo salvando il risultato
    nel registro k-esimo.
    Restituisce 'OK' o solleva eccezioni.
    """
    if len(splitted_request) != 5:
        raise ParametersError("Numero di parametri errato")
    n = int(splitted_request[1])  
    i = int(splitted_request[2]) 
    j = int(splitted_request[3])
    k = int(splitted_request[4])
    s = boxSessioni.findSessione( n )
    sessione_corrente = boxSessioni.box[s]
    if any(x < 0 for x in (i,j,k)):
        raise LessThanZeroRegError("Inserito registro minore di 0")
    sessione_corrente.registri[k] = sessione_corrente.registri[i]\
    * sessione_corrente.registri[j]
    return"OK\r\n" 

def div( splitted_request ):
    """Con una richiesta 'ADD n i j k' in input, nella sessione n, esegue il
    rapporto tra i valori del registro i-esimo e j-esimo salvando il risultato
    nel registro k-esimo.
    Restituisce 'OK' o solleva eccezioni.
    """
    if len(splitted_request) != 5:
        raise ParametersError("Numero di parametri errato")
    n = int(splitted_request[1])  
    i = int(splitted_request[2]) 
    j = int(splitted_request[3])
    k = int(splitted_request[4])
    s = boxSessioni.findSessione( n )
    sessione_corrente = boxSessioni.box[s]
    if any(x < 0 for x in (i,j,k)):
        raise LessThanZeroRegError("Inserito registro minore di 0")
    sessione_corrente.registri[k] = sessione_corrente.registri[i]\
    / sessione_corrente.registri[j]
    return"OK\r\n"

def getReg( splitted_request ):
    """Con una richiesta 'GET n i' in input, restitusce il valore contenuto
    nel registro i-esimo della sessione n.
    Restituisce 'OK k' con k = valore richiesto o solleva eccezioni.
    """
    if len(splitted_request) != 3:
        raise ParametersError("Numero di parametri errato")
    n = int(splitted_request[1])
    i = int(splitted_request[2])
    s = boxSessioni.findSessione( n )
    sessione_corrente = boxSessioni.box[s]
    if i < 0:
        raise LessThanZeroRegError("Inserito registro minore di 0")
    return "OK %i\r\n" %sessione_corrente.registri[i]

def setReg( splitted_request ):
    """Con una richiesta 'SET n i k' in input, setta il valore contenuto
    nel registro i-esimo della sessione n uguale a k.
    Restituisce 'OK' o solleva eccezioni.
    """
    if len(splitted_request) != 4:
        raise ParametersError("Numero di parametri errato")
    n = int(splitted_request[1])
    i = int(splitted_request[2])
    k = int(splitted_request[3])
    s = boxSessioni.findSessione( n )
    sessione_corrente = boxSessioni.box[s]
    if i < 0:
        raise LessThanZeroRegError("Inserito registro minore di 0")
    sessione_corrente.registri[i] = k
    return "OK\r\n"

def stack( splitted_request ):
    """Con una richiesta 'STACK n' in input, restituisce 'OK k1 ... kn' dove
    i vari ki sono i valori contenuti nello stack della sesssione n 
    o solleva eccezioni.
    """
    if len(splitted_request) != 2:
        raise ParametersError("Numero di parametri errato")
    n = int(splitted_request[1])
    s = boxSessioni.findSessione( n )
    sessione_corrente = boxSessioni.box[s]
    result = "OK"
    i = 0
    while i < len(sessione_corrente.stack):
        result = result + " "  + str(sessione_corrente.stack[i]) 
        i += 1
    result = result + "\r\n"
    return result
    
operazioni = { 
    'INIT': init ,
    'CLOSE': close ,
    'PUSH': push ,
    'POP' : pop ,
    'ADD' : add , 
    'SUB' : sub , 
    'DIV' : div ,
    'MUL' : mul ,
    'GET' : getReg ,
    'SET' : setReg ,
    'STACK' : stack
}

if __name__ == '__main__':
#     sm_socket = start( sys.argv[1] , int(sys.argv[2]) , int(sys.argv[3]) )
    sm_socket = start( 'localhost' , 8080 , 10 )
    boxSessioni = Box()
    run( sm_socket )