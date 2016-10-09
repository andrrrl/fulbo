#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals
import sys
import re
from lxml.html import parse
from yt import YT

class FArg():
    
    if len(sys.argv) == 2:
        busqueda = sys.argv[1]
        
        # Así no hay que andar escribiendo nombres infames :-P
        if busqueda     == 'Ra sin club':
            busqueda        = 'Racing'
        elif busqueda   == 'Bosta':
            busqueda        = 'Boca'
        elif busqueda   == 'Gallis':
            busquda         = 'River'
        elif busqueda   == 'Rojo': # xD
            busqueda        = 'Independiente'
        
    else:
        busqueda = False

    resultados = False

    ## Fuente de datos
    data_source = 'http://www.futbolargentino.com/primera-division/posiciones/index.aspx?o=2'
    data_source_name = 'FARG'
    
    i = 1
    lista_p = []
    lista_d = []
    lista_h = []
    lista_t = []
    lista_c = []
    lista_de_partidos = []

    if data_source_name == 'FPT':
        css_campeonato = ['h2#site-description'] # nombre del campeonato
        css_partido = ['.programacion-partido'] # equipos (Local / Visitante) [1:-1]
        css_dia     = ['.fecha'] # Día del partido [1:-1]
        css_hora    = ['.hora'] # Hora del partido [1:-1]
        css_transmite = ['.transmite'] # Transmisión TV
        css_torneo  = ['.torneo'] # Nombre del torneo
        format_string = True

    if data_source_name == 'FARG':
        css_campeonato = ['.tablaMenuFase unlink span'] # nombre del campeonato
        css_partido = ['#resultados0 tr .SCequloc', '#resultados0 tr .SCequvis'] # equipos (Local / Visitante)
        css_dia     = ['#resultados0 tr .SCfec'] # Día del partido
        css_hora    = ['#resultados0 tr .SChor'] # Hora del partido
        css_transmite = [] # Transmisión TV
        css_torneo  = ['.tablaMenuFase unlink span'] # Nombre del torneo
        format_string = False

    ## Obtener raíz de datos
    # dp = parse(data_source).getroot()
    # 
    # for p, t1, t2 in zip(zip(dp.cssselect('#resultados0 tr .SCequloc'), dp.cssselect('#resultados0 tr .SCequvis')), dp.cssselect('#resultados0 tr .SCfec'), dp.cssselect('#resultados0 tr .SChor')):
    #     
    #     p = (p[0].text_content() + ' vs. ' + p[1].text_content()).encode('utf-8')
    #     print p
    #     if i > 20:
    #         break
    #     i = i + 1
    # 
    # 
    # exit()

    def __init__(self):
        print "\rCargando próximos partidos...",

        # partidos programados
        dp = parse(self.data_source).getroot()

        t = dp.cssselect('.tablaMenuFase .unlink')

        t = t[0]

        for p, f, h in zip(
            zip(
                dp.cssselect('#resultados0 tr .SCequloc'), dp.cssselect('#resultados0 tr .SCequvis')
            ), 
            dp.cssselect('#resultados0 tr .SCfec'), 
            dp.cssselect('#resultados0 tr .SChor'), 
            ):
            
            if len(self.css_partido) == 2:
                p = (p[0].text_content() + ' vs. ' + p[1].text_content()).encode('utf-8')
            else:
                p = p.text_content()

            if self.busqueda:
                e = p.encode('utf-8')
                self.resultado = re.findall(self.busqueda, e)
                if self.resultado:
                    self.resultados = True
                    self.lista_p.append(p)
                    self.lista_d.append(f.text_content())
                    self.lista_h.append(h.text_content())
                    self.lista_t.append('---')
                    self.lista_c.append(t.text_content())
                    continue
            else:
                print p
                self.lista_p.append(p)
                self.lista_d.append(f.text_content())
                self.lista_h.append(h.text_content())
                self.lista_t.append('---')
                self.lista_c.append(t.text_content())

            
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
    FArg()