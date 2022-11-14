import socket
import threading
import time
import pickle
import json

SERVER_IP = socket.gethostbyname(socket.gethostname())
PORT = 5050
print('[ SERVER ] Iniciado no endereço: ', f'{SERVER_IP}:{PORT}')
ADDR = (SERVER_IP, PORT)
FORMATO = 'utf-8'

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

print("[INICIANDO] Iniciando VOTAÇÃO")

# carrega o arquivo usuarios.json e insere na variavel candidatos
with open('candidatos.json', 'r') as candidatos_cadastrados:
    candidados = json.load(candidatos_cadastrados)

# carrega o arquivo usuarios.json e insere na variavel usuários
with open('usuarios.json', 'r') as usuarios_cadastrados:
    usuarios = json.load(usuarios_cadastrados)


def iniciar_autenticacao(login, senha):
    sucesso_autenticacao = False
    
    for usuario in usuarios['usuarios']:
        if login in usuario.values() and senha in usuario.values():
            print(usuario, 'Existe')
            sucesso_autenticacao = True
    
    return sucesso_autenticacao

def contabilizar_voto(voto):
    for candidato in candidados['candidatos']:
        if voto[0] in candidato.values() and voto[1] in candidato.values():
            candidato['total_votos'] += 1 
            print(candidato)


server.listen()

while(True):    
    cliente_socket, endereco = server.accept()
    data = cliente_socket.recv(4096)
    credenciais = pickle.loads(data)

    if iniciar_autenticacao(credenciais[0], credenciais[1]):
        resposta = b'sucesso'
        cliente_socket.sendto(resposta, endereco)
        lista_para_votacao = []
        
        for candidato in candidados['candidatos']:
            lista_para_votacao.append(candidato)
        
        lista_para_votacao = pickle.dumps(lista_para_votacao)

        cliente_socket.sendto(lista_para_votacao, endereco)

        data = cliente_socket.recv(4096)
        voto = pickle.loads(data)
        
        contabilizar_voto(voto)

    else:
        resposta = b'falha'
        cliente_socket.sendto(resposta, endereco)

