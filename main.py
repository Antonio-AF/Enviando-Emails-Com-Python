#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Module.smtp_python import enviar_email
import time
import traceback
import sqlite3

#Define a conexão
conn = sqlite3.connect('/home/michael/Projetos/servidor_email/Data/base_email.db')
cur = conn.cursor()

sql_retonar_email = ("select email from contato_email where enviado = 'N'")
cur.execute(sql_retonar_email)
lista_email = cur.fetchall()

for email in lista_email:
	try:
		print('Enviando email para: {}'.format(email[0]))
		enviar_email(servidor='smtp.gmail.com',
					 porta=465,
					 origem='chelmto3000@gmail.com',
					 destino=email[0],
					 assunto='Aprenda a desenvolver software utilizando software livre Linux',
					 nome='Michael de Mattos')
		print('E-mail enviado com sucesso!\n')

	except Exception:
		sql_atl_email_enviado = ("update contato_email set retorno = '%s' where email = '%s'" %(traceback.print_exc(), email[0]))
		cur.execute(sql_atl_email_enviado)
	
	finally:
		sql_atl_email_enviado = ("update contato_email set enviado = 'S' where email = '%s'" %(email[0]))
		cur.execute(sql_atl_email_enviado)
		conn.commit()
	
	#define o tempo de envio
	time.sleep(3)
		
print("Finalizando a execução do programa!\n"
	  "Não existe mais e-mail a ser enviado")

cur.close()
conn.close()
