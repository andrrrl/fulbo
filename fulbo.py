#!/usr/bin/python
# -*- coding: utf-8 -*-

import subprocess
import os
from datetime import datetime
from lxml.html import parse

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

#import ConfigParser

from farg import FArg as FPT
# from fpt import FPT
from yt import YT

class Handlers:
	
	def ConfigSectionMap(self, section):
		dict1 = {}
		options = Config.options(section)
		for option in options:
			try:
				dict1[option] = Config.get(section, option)
				if dict1[option] == -1:
					DebugPrint("skip: %s" % option)
			except:
				print("exception on %s!" % option)
				dict1[option] = None
		return dict1
	
	def onDeleteEvent(self, *args):
		
		proc = subprocess.Popen(["pkill", "-f", "vlc"], stdout=subprocess.PIPE)
		proc.wait()
				
		Gtk.main_quit(*args)

	def onRowActivated(self, *args):
		
		#Config = ConfigParser.ConfigParser()
		#Config.read("fulbo.ini")
		
		transmission = [ u'tv pública', u'tvp', u'360 tv', u'dxtv', u'canal 9' ]
		channels = {
			transmission[0]: 'tvp',
			transmission[1]: 'tvp',
			transmission[2]: '360',
			transmission[3]: 'dtv',
			transmission[4]: 'c9'
		}
		#channels = self.ConfigSectionMap("Canales")
		
		selection = treeview.get_selection()
		model, treeiter = selection.get_selected()
		if treeiter != None:
			cell_text = unicode(model[treeiter][3],'utf-8').lower()
		
		i = 0
		for channel in transmission:
		
			if channel in cell_text:
				tv_channel = channels[channel]
				watch = subprocess.Popen( [ 'tv', tv_channel ] )
			
		if cell_text == 'youtube':
			live_yt = YT().get_live_urls()
			watch = subprocess.Popen( [ 'vlc', live_yt[unicode(model[treeiter][0], 'utf-8')], '> /dev/null &2>1' ] )
			
	def button_is_clicked(self, button):
		## The ".run()" method is used to launch the about window.
		ouraboutwindow.run()
		## This is just a workaround to enable closing the about window.
		ouraboutwindow.hide()

	def enter_button_clicked(self, button):
		## The ".get_text()" method is used to grab the text from the entry box. The "get_active_text()" method is used to get the selected item from the Combo Box Text widget, here, we merged both texts together".
		print ourentry.get_text() + ourcomboboxtext.get_active_text()

	def url_partido(treeview, path, c1, c2):
		print treeview.get_selection()
		#self.resultado = re.findall(self.busqueda, e)
		
	def on_update_button(self, button):
		AppBuilder().show_results()
		

class AppBuilder:
	
	def __init__(self):
	
		global treeview
		
		builder = Gtk.Builder()
		builder.add_from_file("pyfulbo.glade")
		builder.connect_signals(Handlers())
		
		self.window 	= builder.get_object("window1")
		treeview 		= builder.get_object("treeview1")
		self.partidos 	= builder.get_object("liststore1")
		update_btn 		= builder.get_object("button_update")
		
		statusbar   = builder.get_object("statusbar1")
		context     = statusbar.get_context_id("author")
		statusbar.push(context, "by Andrrr")
		
		treeview.set_model(self.partidos)
	
	def load_data(self):
		self.show_results()
		self.show_window()
		
	def show_results(self):
		# próximos partidos 
		matches_list = FPT().partidos()
		self.update_list(self.partidos, matches_list[0], matches_list[1], matches_list[2], matches_list[3], matches_list[4])
		print 'Listo (a las ' + datetime.now().strftime('%H:%M') + ' hs).'

	
	def update_list(self, partidos, partido, dia, horario, tv, torneo):
		print 'Actualizando lista...'
		for p, d, h, t, c in zip(partido, dia, horario, tv, torneo):
			self.partidos.append( [ p, d, h, t, c ] )
	
	def show_window(self):	
		## Give that developer a cookie !
		#treeview.connect("row-activated", open_url_partido)
		#window.connect("delete-event", main_quit)
		#window.connect('destroy', main_quit)
		self.window.show_all()
		Gtk.main()

if __name__ == '__main__':
	AppBuilder().load_data()
