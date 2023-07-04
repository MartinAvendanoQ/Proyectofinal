import socket #use a predefined function socket in order to get connected different terminals
import random  #use a predefined function random in order to obtain ramdom values
import os  # use a predefined function in order to clear terminal screen

def palabra_adivinar(): 
    lista_palabras = ["perro", "gato", "leon","conejo","ardilla","ballena","tortuga","elefante","venado","buitre",
                  "tlaxcala", "colima","guerrero","puebla","veracruz", "monterrey","oaxaca","zacatecas","tamaulipas","guanajuato",
                  "manzana","pera","mango","platano","guayaba","melon","kiwi","papaya","sandia","pina",
                  "refrigerador","television","microondas","licuadora","tostadora","plancha","lavadora","boiler","freidora","cafetera",
                  "españa","italia","francia","noruega","suecia","portugal","alemania","belgica","polonia","suecia",
                  "falda","vestido","short","playera","blusa","sueter","calcetin","chaleco","gorra","brasier"]   # create a list of words

    indice1 = random.randint(0,len(lista_palabras))    # generates an integer number between 0 and the length of the list of words
    palabra1 = lista_palabras[indice1]      # chose ramdomly a word from the list of words
    return indice1, palabra1    #Python allows to return several values

def palabra_guiones(palabra):
    palabra_temp2 = ""    # create a word (with no characters)
    for c in palabra:    # create a word of  n-underscores depending on the size of the word that is going to be guessed
        palabra_temp2 += "_"   # notice how to add a new underscore ahead, each time
    return palabra_temp2  # return the string of underscores

def pista_tipo(indice):
    if indice >=0 and indice<=9:   # depending on the range of index, the word is categorized within a group of animals, cities, fruits, etc
        mess = "La palabra es un animal"
    elif indice >=10 and indice<=19:
        mess = "La palabra es un estado de la Republica Mexicana"
    elif indice >=20 and indice<=29:
        mess = "La palabra es una fruta"
    elif indice >=30 and indice<=39:
        mess = "la palabra es un electrodomestico"
    elif indice >=40 and indice<=49:
        mess = "la palabra es un pais Europeo"
    else:
        mess = "La palabra es una prenda para vestir"
    return mess    

def palabra_ingresada(letra,palabra,letras_ingresadas):
    
    letras_ingresadas.append(letra.lower())  # add the letter entered by user to string letras_ingresadas and convert it into lowercase

    palabra_ingresada = ""  #the set of letters that the user has guessed (at the begining with no characters)

    for con in palabra:   #loop for that runs over the length of the variable palabra
        if con in letras_ingresadas:   # if each letter in palabra coincides with the list of letras_ingresadas, copy con to palabra_ingresada. In other case, print underscore
            palabra_ingresada += con
        else:
            palabra_ingresada += "_"

    return palabra_ingresada  #return the guessed word up to the moment

def juego(conn):  # the argument conn serves to send messages to client
    indice, palabra = palabra_adivinar()   # the two values returned by module palabra_adivinar
    oportunidades = 13   #number of opportunities to guess 
    mess1 = "La palabra a adivinar tiene la siguiente forma: " + palabra_guiones(palabra) + ". Tienes " + str(oportunidades) + " oportunidades." # concatenate different strings
    conn.send(mess1.encode())   # send message to the client
    
    letras_ingresadas = []    #Global variable. create a list (empty at the begining)   of entered letters that increases as it is entered each leter
    while True:
        letra = conn.recv(1024).decode()    # receives the letter entered by client
        letraold = letra   # saves the response of the client
        palabra_ingresada_temp = palabra_ingresada(letra,palabra,letras_ingresadas)   #assigns the guessed word up to the moment 

        oportunidades -= 1   # the variable oportunidades decreases in one    
        if "_" not in palabra_ingresada_temp or letraold==palabra:  # if there is no more blank spaces, or the client guess the whole word, the programm finishes
            termina_juego = 1
            conn.send(str(termina_juego).encode())    # send value to the client
            break

        elif oportunidades == 0:   #the program finishes when the trials are equal to zero
            termina_juego = 2
            conn.send(str(termina_juego).encode())    # send value to the client
            break
        elif letraold == "pista" and oportunidades < 7:   # if the client enter "pista" this sentence is executed
            mess2 = pista_tipo(indice)    # tells the client about the word identity
            conn.send(mess2.encode())
            oportunidades += 1   # the variable oportunidades does not decreases in this case
        else: 
            if letra in palabra_ingresada_temp:
                mess3 = "adivinaste una letra, "
            else:
                mess3 = "la letra no esta en la palabra, "
            mess2 = mess3 + "Quedan " + str(oportunidades) + " oportunidades. " + palabra_ingresada_temp  #concatenate different strings
            conn.send(mess2.encode())   # send message to the client
        
      
    chr = conn.recv(1024).decode()    # receives temporal empty word in order to send a string with the guessed word
    mess2 = palabra  #the word in question es printed at the end of execution
    conn.send(mess2.encode())   # send message to the client

def server_connection():     # this module only gets the connection with client
    #get the hostname
    host = socket.gethostname()
    port = 5020   #initiate port no. above 1024

    server_socket = socket.socket()   #get instance
    # look closely. The bind() function takes tuple as argument
    server_socket.bind((host, port))   # bind host address and port together

    #configure how many client the server canlisten simultanously
    server_socket.listen(2)
    conn, address = server_socket.accept()   #accept new connection. The function server_socket returns 2 values, conn and address
    print("Conexión de la dirección: " + str(address))
    return conn

def server_program(conn):   # this module executes the main programm
    while True:
        #receive data stream. It won't accept data packet greater than 1024 bytes
        data = conn.recv(1024).decode()
        
        if not data:
            #if data is not received break
            break

        if data == "jugar":
            print("Mensaje recibido del jugador: " + str(data))   #print the message received from client in terminal
            juego(conn)
        elif data == "bye":
            print("Mensaje recibido del jugador: " + str(data))   #print the message received from client in terminal       
            conn.send(data.encode())  
        else:
            conn.send(data.encode())   # send data to the client
    conn.close()     # close the connection if no data is received

if __name__ == "__main__":
    os.system('cls')   # clear the terminal screen
    conn1 = server_connection()
    server_program(conn1)
