#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
import sqlite3
import base64
import gi

gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

builder = Gtk.Builder()
builder.add_from_file('cad_mensagem.glade')

#codigicação em base 64
def codifica_mensagem(msg):
	msg_base64 = base64.b64encode(msg.encode('utf-8'))
	return msg_base64

#decodificação em base 64
def decodifica_mensagem(msg_codificada):
	msg = base64.b64decode(msg_codificada)
	return msg.decode('utf-8')

class Handler(object):
	
	def __init__(self, *args, **kwargs):
		super(Handler, self).__init__(*args,**kwargs)
		
		#Define a conexão
		self.conn = sqlite3.connect('/home/michael/Projetos/servidor_email/Data/base_email.db')
		self.cur = self.conn.cursor()
		
		#Carrega componentes
		self.bt_salvar = builder.get_object('bt_salvar')
		self.bt_limpar = builder.get_object('bt_limpar')
		self.entry_msg_email = builder.get_object('entry_msg_email') # <<<= Meu Text Buffer
		self.lb_retorno_cadastro = builder.get_object('lb_retorno_cadastro')
		
	#Destroy a execução
	def on_cad_mensagem_destroy(self, *args):
		self.cur.close()
		self.conn.close()	
		Gtk.main_quit()
	
	#Volta ao menu principal
	def on_bt_voltar_clicked(self, *args):
		Gtk.main_quit()
	
	def on_bt_salvar_clicked(self, *args):
		if self.bt_salvar.get_label() == 'SALVAR':
			try:
				mensagem = self.entry_msg_email.get_text() # <<<= Meu Text Buffer
				msg_codificada = codifica_mensagem(msg=mensagem)
				self.cur.execute("update mensagem_email set mensagem = '%s' where cod_mensagem_email = 1" %(msg_codificada))					
				self.conn.commit()
				self.lb_retorno_cadastro.set_text("Mensagem atualizada com sucesso!")
			
			except Exception:
				self.lb_retorno_cadastro.set_text(str(traceback.print_exc()))
				
	#limpa o conteudo da textview
	def on_bt_limpar_clicked(self, *args):
		self.entry_msg_email.set_text('')
		self.lb_retorno_cadastro.set_text('')
	
builder.connect_signals(Handler())
window = builder.get_object('cad_mensagem')
window.show_all()

if __name__=='__main__':
	Gtk.main()
	
