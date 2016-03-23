#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys
import re
from lxml.html import parse
from yt import YT
            

class FPT():
    
    if len(sys.argv) == 2:
        busqueda = sys.argv[1]
        
        # Así no hay que andar escribiendo nombres infames :-P
        if busqueda     == 'Ra sin club':
            busqueda        = 'Racing'
        elif busqueda   == 'Bosta':
            busqueda        = 'Boca'
        elif busqueda   == 'Gallis':
            busquda         = 'River'
        elif busqueda   == 'Rojo':
            busqueda        = 'Independiente'
        
    else:
        busqueda = False

    resultados = False
    
    i = 1
    lista_p = []
    lista_d = []
    lista_h = []
    lista_t = []
    lista_c = []
    lista_de_partidos = []
 
    def __init__(self):
        print "\rCargando próximos partidos...",
        # partidos programados "NO COMENZADOS"
        dp = parse('http://www.futbolparatodos.com.ar/programacion-de-partidos/').getroot()
            
        for p, f, h, t, c in zip(dp.cssselect('.programacion-partido')[1:-1], dp.cssselect('.fecha')[1:-1], dp.cssselect('.hora')[1:-1], dp.cssselect('.transmite')[1:-1], dp.cssselect('.torneo')[1:-1]):
            
            if self.busqueda:
                e = p.text_content().encode('utf-8')
                self.resultado = re.findall(self.busqueda, e)
                if self.resultado:
                    self.resultados = True
                    self.lista_p.append( u"%s" % re.sub('\s\s+|\t+', ' ', p.text_content()) )
                    self.lista_d.append( u"%s" % re.sub('\s\s+|\t+', ' ', f.text_content()) )
                    self.lista_h.append( u"%s" % re.sub('\s\s+|\t+', ' ', h.text_content()) )
                    self.lista_t.append( u"%s" % re.sub('\s\s+|\t+', ' ', t.text_content()) )
                    self.lista_c.append( u"%s" % re.sub('\s\s+|\t+', ' ', c.text_content()) )
                    continue
            else:
                self.lista_p.append( u"%s" % re.sub('\s\s+|\t+', ' ', p.text_content()) )
                self.lista_d.append( u"%s" % re.sub('\s\s+|\t+', ' ', f.text_content()) )
                self.lista_h.append( u"%s" % re.sub('\s\s+|\t+', ' ', h.text_content()) )
                self.lista_t.append( u"%s" % re.sub('\s\s+|\t+', ' ', t.text_content()) )
                self.lista_c.append( u"%s" % re.sub('\s\s+|\t+', ' ', c.text_content()) )
                #print u"%s" % re.sub('\s\s+|\t+', ' ', c.text_content())

            
            self.i += 1
        
        print "fin de carga."
        
        if self.i == 1:
            print '[Ningún partido próximo a jugarse (cosa rara)]'
        
        self.partidos_yt()

        self.lista_de_partidos = [ self.lista_p, self.lista_d, self.lista_h, self.lista_t, self.lista_c ]
        
    
    def partidos_yt(self):
        
        # partidos en vivo "AHORA" por Youtube
        yt_data = YT()
        yt = yt_data.list_live_matches()
        tr = yt_data.list_live_tournaments()
        
        # En vivo
        for partido_yt, torneo_yt in zip(yt, tr):
            
            if not partido_yt in self.lista_p:
                self.lista_p.insert(0, ' ' + partido_yt )
                self.lista_d.insert(0, 'Hoy' )
                self.lista_h.insert(0, 'En juego' )
                self.lista_t.insert(0, 'Youtube' )
                self.lista_c.insert(0, ' ' + torneo_yt )
        
        if self.i == 1:
            print "No se encontró nada (sito caído? hay internec??) :'("
            exit() 
        elif self.busqueda and not self.resultados:
            print "No se encontraron partidos que coincidan con la búsqueda '%s' :'(" % self.busqueda
            exit()
        
    def partidos(self):
        return self.lista_de_partidos

            
if __name__ == '__main__':
    FPT()
