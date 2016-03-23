#!/usr/bin/python
# -*- coding: utf-8 -*-

import sys
from lxml.html import parse

# Devuelve (o imprime, según el caso) la lista de partidos EN VIVO de Fútbol Para Todos


'''
    Get *LIVE* FPT (Fútbol Para Todos) matches
'''
class YT():
    
    url = 'http://www.futbolparatodos.com.ar/'
    
    def __init__(self):
        print '\rCargando partidos EN VIVO, transmitidos por Youtube... ',
        live_matches     = self.list_live_matches()
        live_tournaments = self.list_live_tournaments()
        
        if len(live_matches) > 0:
            for p, t in zip(live_matches, live_tournaments):
                print p + ' : ' + t
        else:
            print u'ningún partido en vivo en este momento... '
            return
    
    def get_live_matches(self):
        titles = parse(self.url).getroot()
        return titles
    
    '''
        Returns a list of "Team 1 vs Team 2 ... Team N vs Team N1" of matches being played right now (LIVE)
    '''
    def list_live_matches(self):
            
        envivo   = self.get_live_matches()
        partidos = []
           
        for clubs in envivo.cssselect('.envivo'):
            for local, visit in zip(clubs.cssselect('.local .nombreclub'), clubs.cssselect('.visitante .nombreclub')):
                partidos.append(local.text_content() + ' vs. ' + visit.text_content())
                   
        # The list is reversed, so *LIVE* (youtube) links are in the top
        partidos.reverse()
        return partidos
    
    
    '''
        Returns a list of the Tournament names of matches being played right now (LIVE)
    '''
    def list_live_tournaments(self):
        
        envivo   = self.get_live_matches()
        torneos  = []
        
        for clubs in envivo.cssselect('.envivo'):
            for torneo in clubs.cssselect('.torneo-fecha'):
                torneos.append(torneo.text_content())
                
        torneos.reverse()
        return torneos
    
    
    '''
        Returns a list of URLs of matches being played right now (LIVE) thru youtube.com
    '''
    def get_live_urls(self):
        
        fpt = parse(self.url).getroot()
        
        matches = self.list_live_matches()
        
        youtube_urls = {}
        if fpt is None:
            print 'No hay partidos!'
        else:
            for partido, match in zip(fpt.cssselect('iframe'), matches):
                youtube_urls[u' ' + match] = 'http:' + partido.get('src')
        
        print u'fin de carga.'
        return youtube_urls
    
if __name__ == '__main__':
    YT()