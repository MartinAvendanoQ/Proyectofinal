import socket
import os

def client_connection():
    host = socket.gethostname()  #as both code is running on same pc
    port = 5020    # socket server port number

    client_socket = socket.socket()  #instantiate
    client_socket.connect((host, port))   # connet to the server

    # Here it ends the code lines that initiate the conection between server and client
    return client_socket

def client_program(client_socket):
    mess4 = " "
    while mess4.lower().strip()  != "bye":   #while the word be different from "bye", the program executes
        mess4 = input("¡Hola! Bienvenido al juego de adivina la pabra. Ingresa la palabra \"jugar\" para adivinar la palabra, o bien, \"bye\" para salir: ")    # print the prompt -> and take input from client

        while mess4 != "bye" and mess4 != "jugar":  # repeat up to a valid reponse is entered
            mess4 = input("Opcion no valida. Ingresa la palabra \"jugar\" para adivinar la palabra, o bien, \"bye\" para salir: ")

        while True:   # while is true up to a break is reached, for example, when the word has been guessed, the number of trials has ended or is typed "bye"
            client_socket.send(mess4.lower().strip().encode())   # convert into lowercase and send message to server 
            mess4 = client_socket.recv(1024).decode()   #receive response

            if mess4 == "1":   #under this condition a message is displayed and the game ends
                print("Muy bien!!! Has adivinado la palabra: ")
                break
            elif mess4 == "2":     #under this condition a message is displayed and the game ends
                print("Lo siento, has terminado con tus oportunidades!!!, la palabra era: ")
                break
            elif mess4 == "bye":   #under this contidion a message is displayed and the game
                print("Mensaje del jefe: "  +mess4)   #show in terminal
                break
            else:      # in this case, continue the game
                print("Mensaje del jefe: "  +mess4)   #show in terminal
                mess4 = input("Mensaje del jefe: Ingrese una letra para adivinar, o bien, \"pista\" \
para obtener una pista de la identidad de la palabra (solo despues que queden 7 intentos): ")   # again take input and the first letter
    
        if mess4 != "bye":   # if the received word is not "bye", the programa print the word that should be guessed
            mess4 = " "
            client_socket.send(mess4.encode())   #send a server in order to receive the word that should be guessed 
            mess4 = client_socket.recv(1024).decode()   #receive response
            print("   " + mess4)

    client_socket.close()    #close the connection

if __name__ == "__main__":
    os.system('cls')   # clear the terminal screen
    client_socket1 = client_connection()
    client_program(client_socket1)
