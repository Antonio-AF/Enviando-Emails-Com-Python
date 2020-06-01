#!/usr/bin/env python
# -*- coding: utf-8 -*-

import traceback
import sqlite3
import gi

gi.require_version('Gtk', '3.0')

from gi.repository import Gtk
builder = Gtk.Builder()
builder.add_from_file('interface_envia_email.ui')

class Handler(object):
	
	def __init__(self, *args, **kwargs):
		super(Handler, self).__init__(*args,**kwargs)
		
		#Carrega minha Stack
		self.Stack = Gtk.Stack
		self.Stack = builder.get_object('stack')
		
		#Define a conexão com o banco de dados
		self.conn = sqlite3.connect('/home/michael/Projetos/servidor_email/Data/base_email.db')
		self.cur = self.conn.cursor()
		
		#Carrega componentes view cad_email
		self.entry_email = builder.get_object('entry_email')
		self.entry_nome = builder.get_object('entry_nome')
		self.bt_salvar = builder.get_object('bt_salvar')
		self.lb_retorno_cadastro = builder.get_object('lb_retorno_cadastro')
		
		#Carrega componentes view editar cad_email
		self.bt_atualizar = builder.get_object("bt_atualizar")
		self.bt_excluir = builder.get_object("bt_excluir")
		self.bt_voltar = builder.get_object("bt_voltar")
		
		#tree view
		self.tree_view = builder.get_object("tree_view")
		self.lst_dados = Gtk.ListStore
		self.lst_dados = builder.get_object('lst_dados')
		
		#colunas treeview
		self.coluna = {"cod": 0, "nome": 1, 
					   "email": 2, "enviado": 3,
					   "retorno": 4, "excluir": 5} 
		
	#####-----VIEW CADASTRAR EMAIL-----######
	def ao_clicar_encerar(self, *args):
		Gtk.main_quit()
	
	def ao_clicar_em_alterar_excluir(self, *args):
		self.Stack.set_visible_child_name('alterar_excluir')
	
	#grava novo e-mail
	def ao_clicar_em_salvar(self, *args):
		if self.bt_salvar.get_label() == 'Salvar':
			try:
				email = self.entry_email.get_text()
				nome = self.entry_nome.get_text()
				self.cur.execute("insert into contato_email (nome, email, enviado) values ('%s','%s','N')" %(nome,email))					
				self.conn.commit()
				self.lb_retorno_cadastro.set_text("Cadastrado com sucesso!")
			except:
				self.lb_retorno_cadastro.set_text("Desculpe Ocorreu um erro\n"
													"Tente mais tarde")
			finally:
				self.bt_salvar.set_label('LIMPAR')
		else:
			self.entry_email.set_text('')
			self.lb_retorno_cadastro.set_text('')
			self.entry_nome.set_text('')
			self.bt_salvar.set_label('Salvar')
	 	                            
	def ao_clicar_em_altear_excluir(self, *args):
		pass
		
	######-----######-----######-----######
	
	#########################################
	#########################################
	######-----VIEW ALTERAR EDITAR-----######
	
	# ----------- toolbar -------------- 
	def ao_clicar_em_voltar(self, *args):
		self.Stack.set_visible_child_name('cadastrar')
		print("clicou em voltar", args)
		
	def ao_clicar_em_atualizar(self, *args):
		print("clicou em atualizar", args)
		self.lst_dados.clear()
		self.cur.execute("select * from contato_email")
		retorno_pesquisa = self.cur.fetchall()
		for imprimir_lista in retorno_pesquisa:
			_cod = imprimir_lista[0]
			_nome = imprimir_lista[1] 
			_email = imprimir_lista[2]
			_enviado = imprimir_lista[3]
			_retorno = 	imprimir_lista[4]
			_excluir = imprmir_lista=False
			lista_email = [str(_cod), _nome, _email, _enviado, _retorno, _excluir]
			print(lista_email)
			self.lst_dados.append(lista_email)
					
	# ------------ tree view ------------
	def ao_alterar_nome(self, *args):
		print("clicou em altear nome", args)
		linha = args[1]
		novo_texto = args[2]
		self.lst_dados[linha][self.coluna["nome"]] = novo_texto
		cod_alterado = self.tree_view.get_model()[linha][self.coluna["cod"]]
		print(cod_alterado)
		
	def ao_alterar_email(self, *args):
		print("clicou em alterar email", args)
		linha = args[1]
		novo_texto = args[2]
		self.lst_dados[linha][self.coluna["email"]] = novo_texto
		cod_alterado = self.tree_view.get_model()[linha][self.coluna["cod"]]
		print(cod_alterado)
	
	def ao_marcar_como_excluir(self, *args):
		self.render_excluir = builder.get_object('render_excluir')
		print("marcou como excluir", args)
		marcou_excluir = args[1]
		self.lst_dados[marcou_excluir][self.coluna["excluir"]] = not self.lst_dados[marcou_excluir][self.coluna["excluir"]]
	
	def ao_clilcar_em_excluir(self, *args):
		print("clicou em excluir", args)
		print(self.lst_dados)

	######-----######-----######-----########
	#########################################
	#########################################
	
builder.connect_signals(Handler())
window = builder.get_object('main_window')
window.show_all()

if __name__=='__main__':
	Gtk.main()
