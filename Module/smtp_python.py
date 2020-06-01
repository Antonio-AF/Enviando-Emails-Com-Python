#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smtplib
import traceback
import time
import sqlite3 as banco
import email.message
import base64

#Captura a senha do servidor de email
conn = banco.connect('/home/michael/Projetos/servidor_email/Data/base_email.db')
cur = conn.cursor()

def msg():
	html = """
<!DOCTYPE html>
<html lang="pt-br">
	<head>
		<meta charset="utf-8">        
        <style>
			body {background-color: #fff;}
			p {color: #000}
			h1 {color: #000}
		</style>
	</head>
	<body>
	<center>
		<h1>Olá Você recebeu minha mensagem!</h1>
		<p>Isso significa que você pode receber minhas novidades sobre o mundo de desenvolvimento de software</p>
		<p>Deu um pulinho em meu canal, lá temos novidades interessantes pra você</p>
		<p>Aprenda como desenvolver software utilizando o GTK, Glade e o Python</p>
		<p>Tudo isso utilizando Software Livre! Linux</p>
		<a href="https://www.youtube.com/channel/UCBM7dWCV68KU4UiTIF_BbAQ?view_as=subscriber">Clique Aqui - Michael de Mattos - YouTube</a> 
	</center>
	
	</body>
	<center><p>Conto com vocês!</p></center>
</html>

"""
	return html.encode('utf-8')
	
def minha_senha():
	sql_selec_senha = ("select senha from email_senha where email = 'chelmto3000@gmail.com' and ativo = 'S'")
	cur.execute(sql_selec_senha)
	for senha in cur:
		return senha[0]
								
#Função para o envio do e-mail
def enviar_email(servidor, porta=None, tipo_conexao=None, senha=minha_senha(), 
				 origem=None, destino=None, mensagem=msg(), assunto=None,
				 nome=None, anexo=None):
	
	if servidor == 'smtp.gmail.com':
		
		try:
			_origem = origem
			_destino = [destino]
			_senha = senha
			_assunto = assunto
			_mensagem = mensagem
			_nome = nome
			
			msg = email.message.Message()
			msg['Subject'] = _assunto
			msg['From'] = _origem
			msg['To'] = _destino[0]
			msg.add_header('Content-Type', 'text/html')
			msg.set_payload(_mensagem, charset='utf-8')
			
			servidor_smtp = smtplib.SMTP_SSL(servidor, porta)
			 
			# Login Credentials for sending the mail
			servidor_smtp.login(msg['From'], _senha)
 
			servidor_smtp.sendmail(msg['From'], [msg['To']], msg.as_string())
											 				
			#encera a conexão
			servidor_smtp.quit()
			
		except Exception:
			traceback.print_exc()
		
		finally:
			pass
