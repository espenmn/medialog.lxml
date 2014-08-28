# -*- coding: utf-8 -*-,

#import logging
#from Acquisition import aq_inner
from zope.i18nmessageid import MessageFactory
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from plone import api
from medialog.lxml.interfaces import ILxmlSettings

import requests
import lxml.html
import urllib 
from lxml.cssselect import CSSSelector
from lxml.html.clean import Cleaner

from DateTime import DateTime
 

class Scrape(BrowserView):
    """   A View that uses lxml to embed external content    """
    
    def scrapetitle(self):
        return self.scrapetitle
    
    def scraped(self):
        selector = '#container' #default value
        #get settings from control panel / registry
        scrape_add_nofollow = api.portal.get_registry_record('medialog.lxml.interfaces.ILxmlSettings.scrape_add_nofollow')
        scrape_allow_tags = api.portal.get_registry_record('medialog.lxml.interfaces.ILxmlSettings.scrape_allow_tags')
        scrape_annoying_tags = api.portal.get_registry_record('medialog.lxml.interfaces.ILxmlSettings.scrape_annoying_tags')
        scrape_comments = api.portal.get_registry_record('medialog.lxml.interfaces.ILxmlSettings.scrape_comments')
        scrape_embedded = api.portal.get_registry_record('medialog.lxml.interfaces.ILxmlSettings.scrape_embedded')
        scrape_forms = api.portal.get_registry_record('medialog.lxml.interfaces.ILxmlSettings.scrape_forms')
        scrape_frames = api.portal.get_registry_record('medialog.lxml.interfaces.ILxmlSettings.scrape_frames')
        scrape_javascript = api.portal.get_registry_record('medialog.lxml.interfaces.ILxmlSettings.scrape_javascript')
        scrape_kill_tags = api.portal.get_registry_record('medialog.lxml.interfaces.ILxmlSettings.scrape_kill_tags')
        scrape_links = api.portal.get_registry_record('medialog.lxml.interfaces.ILxmlSettings.scrape_links')
        scrape_meta = api.portal.get_registry_record('medialog.lxml.interfaces.ILxmlSettings.scrape_meta')
        scrape_page_structure = api.portal.get_registry_record('medialog.lxml.interfaces.ILxmlSettings.scrape_page_structure')
        scrape_processing_instructions = api.portal.get_registry_record('medialog.lxml.interfaces.ILxmlSettings.scrape_processing_instructions')
        scrape_remove_tags = api.portal.get_registry_record('medialog.lxml.interfaces.ILxmlSettings.scrape_remove_tags')
        scrape_remove_unknown_tags = api.portal.get_registry_record('medialog.lxml.interfaces.ILxmlSettings.scrape_remove_unknown_tags')
        scrape_safe_attrs_only = api.portal.get_registry_record('medialog.lxml.interfaces.ILxmlSettings.scrape_safe_attrs_only')
        scrape_scripts = api.portal.get_registry_record('medialog.lxml.interfaces.ILxmlSettings.scrape_scripts')
        scrape_style = api.portal.get_registry_record('medialog.lxml.interfaces.ILxmlSettings.scrape_style')
        scrape_url_pair = api.portal.get_registry_record('medialog.lxml.interfaces.ILxmlSettings.scrape_url_pair')
        scrape_whitelist = api.portal.get_registry_record('medialog.lxml.interfaces.ILxmlSettings.scrape_host_whitelist')
        scrape_whitelist_tags = api.portal.get_registry_record('medialog.lxml.interfaces.ILxmlSettings.scrape_whitelist_tags')
        url = api.portal.get_registry_record('medialog.lxml.interfaces.ILxmlSettings.scrape_url')
        
        #get url if it was set in the request
        if hasattr(self.request, 'url'):
            url = str(urllib.unquote((self.request.url).decode('utf8')))

        #get base url, 
        #if the url is taken from request
        parts = url.split('//', 1)
        this_base_url = parts[0]+'//'+parts[1].split('/', 1)[0]
        
        if this_base_url not in scrape_whitelist:
            return "URL domain is not in whitelist"
            
        #get html from the requested url
        r = requests.get(url)
        tree = lxml.html.fromstring(r.text)
        #this is for use in the createpage view
        self.scrapetitle = (tree.xpath('//title/text()'))[0]# Get page title  
             
        #clean evil stuff
        cleaner = Cleaner(
            add_nofollow = scrape_add_nofollow,
            allow_tags = scrape_allow_tags,
            annoying_tags =  scrape_annoying_tags,
            comments = scrape_comments,
            embedded = scrape_embedded,
            forms = scrape_forms,
            frames =  scrape_frames,
            host_whitelist = scrape_whitelist,
            javascript = scrape_javascript , 
            kill_tags = scrape_kill_tags,
            links = scrape_links ,
            meta = scrape_meta,
            page_structure = scrape_page_structure ,
            processing_instructions = scrape_processing_instructions,
            remove_tags = scrape_remove_tags,
            remove_unknown_tags = scrape_remove_unknown_tags,
            safe_attrs_only = scrape_safe_attrs_only,
            scripts =  scrape_scripts ,
            style = scrape_style, 
            whitelist_tags = scrape_whitelist_tags
        )
        cleaner(tree)
        
        #the parsed DOM Tree
        lxml.html.tostring(tree)

        #relink
        tree.make_links_absolute(this_base_url, resolve_base_href=True)
        tree.rewrite_links(self.repl)
        
        # construct a CSS Selector
        #it the request defines one, use that
        if hasattr(self.request, 'selector'):
            selector = str(urllib.unquote((self.request.selector).decode('utf8')))
        
        #if not, use settings from control panel
        else:
            for pair in scrape_url_pair:
                if pair['scrape_base_url'] in url:
                    selector = pair['scrape_selector']
                    break
                   
        sel = CSSSelector(selector)
                
        # Apply the selector to the DOM tree.
        results = sel(tree)

        # the HTML for the first result.
        if results:
            match = results[0]
            return lxml.html.tostring(match)

        #"Content can not be filtered, returning whole page"
        return lxml.html.tostring(tree)
        
    
    def repl(html, link):
        scrape_url_pair = api.portal.get_registry_record('medialog.lxml.interfaces.ILxmlSettings.scrape_url_pair')
        root_url = api.portal.get().absolute_url()
        
        #dont modyfy image links
        if '/image' in link  or link.endswith('.jpg') or link.endswith('.png') or link.endswith('.gif') or link.endswith('.js') or link.endswith('.jpeg') or link.endswith('.pdf'):
            return link
        
        #point pages for sites enabled in  control panel to embedded view
        for pair in scrape_url_pair:
            if link.startswith(pair['scrape_base_url']):
                return root_url + '/scrape?url=' + link
        
        #for all other links
        return link


class ScrapeView(Scrape):
    """   A Dexterity Content View that uses the scrape view """
            
    def __init__(self, context, request):
          self.context = context
          self.request = request
          #looks ugly, but works
          self.request.selector    =   urllib.quote(context.scrape_selector).decode('utf8') 
          self.request.url         =   urllib.quote(context.scrape_url).decode('utf8')
    
        
        
class CreatePage(Scrape):
    """ Create page from external content"""
    
    def __call__(self):
        #the view is only avalable for folderish content
        folder = self.context
        #get url if it was set in the request
        if hasattr(self.request, 'url'):
            self.request.url = str(urllib.unquote((self.request.url).decode('utf8')))
        
        bodytext = self.scraped()
        scrapetitle = self.scrapetitle.encode('utf8')
        page = api.content.create(container=folder, type='Document', title=scrapetitle, text=bodytext)


class CreatePages(Scrape):
    """ Create pages from list of urls"""
    
    def __call__(self):
        #the view is only avalable for folderish content
        folder = self.context
        #path = self.context.absolute_url() + '/@@createpage'
        
        #view = api.content.get_view(
        #    name='createpage',
        #    context=folder,
        #    request=request,
        #)
        toadd =  u['Tom', 'Aksdal', 'Tom.Aksdal@hfk.no', 'Lærer', '325', '1STD'], ['Lill Kalleklev', 'Almås', 'Lill.Almas@hfk.no', 'Lærer', '423', '2STUSPG'], ['Janne', 'Andersen', 'Janne.Andersen@hfk.no', 'Lærer', '522', '3STUSPI'], ['Ole Kristian', 'Apelseth', '"Ole.Kristian.Apelseth@hfk.no
"', 'Lærer', '324', '1STA'], ['Kjersti Skjåk', 'Astad', 'Kjersti.Skjak.Astad@hfk.no', 'Lærer', '422', '2STUSPE'], ['Anders', 'Bakke', 'Anders.Bakke@hfk.no', 'Lærer', '544', ''], ['Anita Rose', 'Bakke', 'Anita.Bakke@hfk.no', 'Lærer', '347', ''], ['Benedikte Olsbø', 'Berdinessen', 'Benedikte.Olsbo.Berdinessen@hfk.no', 'Lærer', '326', '1STI'], ['Marianne', 'Berentzen', 'Marianne-H.Berentzen@hfk.no', 'IKT konsulent', '', ''], ['Kjell Andreas', 'Berg', 'Kjell.Andreas.Berg@hfk.no', 'Lærer', '522', '3STUSPG'], ['Arvid', 'Berge', 'Arvid.Berge@hfk.no', 'Driftsleder', '', ''], ['Lars', 'Berntsen', 'Lars.Berntsen@hfk.no', 'Avdelingsleder', '236', ''], ['Kari', 'Birkeland', 'Kari.Birkeland@hfk.no', 'Lærer', '523', ''], ['Elisa', 'Bjersand', 'Elisa.Bjersand@hfk.no', 'Avdelingsleder', '235', ''], ['Ann Elise', 'Bjørdal', 'Ann.Elise.Bjordal@hfk.no', 'Renholdsleder', '', ''], ['Bjarte', 'Bjørgaas', 'Bjarte.Bjorgaas@hfk.no', 'Lærer', '544', ''], ['Endre', 'Bjørlykke', '"Endre.Borlykke@hfk.no
"', 'Lærer', '422', '2STUSPB'], ['Anne', 'Bjørnestad', 'Anne.Bjornestad@hfk.no', 'Lærer', '325', '1STF'], ['Ranka', 'Blazevic', 'Ranka.Blazevic@hfk.no', 'Lærer', '422', ''], ['Kjartan', 'Blom', 'Kjartan.Blom@hfk.no', 'Lærer', '543', ''], ['Berit', 'Bomann-Larsen', 'Berit.Bomann-Larsen@hfk.no', 'Lærer', '521', '3STUSPD'], ['William Robert', 'Brown Jr', 'William.Robert.Brown@hfk.no', 'Lærer', '423', ''], ['Akiko', 'Brudvik', 'Akiko.Brudvik@hfk.no', 'Lærer', '543', ''], ['Stig', 'Bruhjell', 'Stig.Bruhjell@hfk.no', 'Lærer', '326', '1STG'], ['Marit', 'Christensen', 'Marit.Christensen@hfk.no', 'Lærer', '523', ''], ['Ingunn Palma', 'Dahle', 'Ingunn.Dahle@hfk.no', 'Lærer', '345', ''], ['Somsuan', 'Dandoy', 'Somsuan.Dandoy@hfk.no', 'Renholder', '', ''], ['Hoang Thanh', 'Dang', 'Hoang.Dang@hfk.no', 'IKT konsulent', '444', ''], ['Ole-Kristian', 'Eide', 'Ole-Kristian.Eide@hfk.no', 'Lærer', '421', ''], ['Stig', 'Eide', 'Stig.Eide@hfk.no', 'Lærer', '543', ''], ['Signe-Bente Thorsen', 'Elgan', 'Signe-Bente.Elgan@hfk.no', 'Lærer', '522', '3STUSPF'], ['Ingunn Anne', 'Engebø', 'Ingunn.Anne.Engebo@hfk.no', 'Lærer', '326', '1STH'], ['Olaug Ø', 'Engesæter', 'Olaug.Engesaeter@hfk.no', 'Ass rektor', '234', ''], ['Odd Øyvind', 'Fjelldal', 'Odd.Oyvind.Fjelldal@hfk.no', 'Lærer', '325', '1STD'], ['Joannis', 'Fogoudrakis', '', 'Psykolog', '449', ''], ['Jori', 'Færevaag', 'Jori.Faerevaag@hfk.no', 'Lærer', '347', ''], ['Bianca Therese', 'Førlandsås', 'Bianca.Therese.Forlandsas@hfk.no', 'Lærer', '326', '1STH'], ['Ingebrigt Olai', 'Gullaksen', 'imnemfa@hotmail.com', 'IKT lærling', '443', ''], ['Eyvor', 'Gyllander', 'Eyvor.Gyllander@hfk.no', 'Lærer', '521', ''], ['Per', 'Haaland', 'Per.Haaland@hfk.no', 'Lærer', '421', ''], ['Odd', 'Haga', 'Odd.Haga@hfk.no', 'Lærer', '346', '2SSSA'], ['Bent Øystein', 'Halden', 'Bent.Oystein.Halden@hfk.no', 'Lærer', '346', '2ISFB'], ['Dag Christian', 'Halvorsen', 'Dag.Christian.Halvorsen@hfk.no', 'Lærer', '324', '1STB'], ['Kirsten', 'Hatlen', '"Kirsten.Hatlen@hfk.no
"', 'Lærer', '544', ''], ['Rannveig Fluge', 'Hausnes', 'Rannveig.Hausnes@hfk.no', 'Lærer', '522', ''], ['Jo Bjørnar', 'Hausnes', 'Jo.Bjornar.Hausnes@hfk.no', 'IKT leder', '443', ''], ['Jiqing ', 'He', 'hejiqing@yahoo.com', 'Lærer', '542', ''], ['Yanming', 'He', 'yummyhym@126.com', 'Lærer', '542', ''], ['Grete', 'Heggertveit', 'Grete.Heggertveit@hfk.no', 'Lærer', '344', ''], ['Bente Sjøstrøm', 'Helland', 'Bente.Helland@hfk.no', 'Miljøfagarbeider', '', ''], ['Siri', 'Hellesøy', 'Siri.Hellesoy@hfk.no', 'Lærer', '543', ''], ['Jarle', 'Henriksen', 'Jarle.Henriksen@hfk.no', 'Lærer', '521', '3STUSPC'], ['Tove', 'Heradstveit', 'Tove.Heradstveit@hfk.no', 'Lærer', '346', '2RLVB'], ['Ann Hilde', 'Hofstad', 'Ann.Hilde.Hofstad@hfk.no', 'Lærer', '344', ''], ['Stine', 'Holmen', 'Stine.Holmen@hfk.no', 'Lærer', '422', '2STUSPA'], ['Torstein', 'Hordvik', 'torstein.hordvik@hfk.no', 'Bibliotekar', '', ''], ['Torrey', 'Hummelsund', 'Torrey.Hummelsund@hfk.no', 'Avdelingsleder', '231', ''], ['Sondre', 'Hvidsten', 'Sondre.Hvidsten@hfk.no', 'Miljøfagarbeider', '', ''], ['Hilda', 'Hønsi', 'Hilda.Honsi@hfk.no', 'Lærer', '423', '2STUSPI'], ['Heidi Rye', 'Høyforsslett', 'Heidi.Hoyforsslett@hfk.no', 'Lærer', '523', '3PBPBYA'], ['Helge Martin', 'Jakobsen', 'Helge.Martin.Jakobsen@hfk.no', 'Lærer', '347', ''], ['Vigdis', 'Johannessen', 'Vigdis.Johannessen@hfk.no', 'Renholder', '', ''], ['Srikantharaja', 'Kanagasabi', 'Srikantharaja.Kanagasabi@hfk.no', 'Renholder', '', ''], ['Siv Britt', 'Karlsen', 'Siv.Karlsen@hfk.no', 'Lærer', '421', ''], ['Lise', 'Klepsvik ', 'lise.klepsvik@bergen.kommune.no', 'Helsesøster', '450', ''], ['Hilde Kaland', 'Kongsrud', 'Hilde.Kongsrud@hfk.no', 'Lærer', '326', '1STG'], ['Martin', 'Kvalø', 'Martin.Kvalo@hfk.no', 'Lærer', '543', ''], ['Marit', 'Lahn-Johannessen', 'Marit.Lahn-Johannessen@hfk.no', 'Lærer', '324', '1STC'], ['Torgeir', 'Larsen', 'Torgeir.Larsen@hfk.no', 'Lærer', '423', '2STUSPH'], ['Agnete Petrea', 'Lind', 'Agnete.Petrea.Lind@hfk.no', 'Lærer', '521', '3STUSPB'], ['Mirjam', 'Lundhaug', 'Mirjam.Lundhaug@hfk.no', 'Lærer', '344', '1HTA'], ['Bjørn ', 'Lyngedal', 'Bjorn.Lyngedal@hfk.no', 'Rektor', '233', ''], ['Mari Skjerdal', 'Lysne', 'Mari.Skjerdal.Lysne@hfk.no', 'Lærer', '422', '2STUSPC'], ['Montserrat', 'Løvaas', 'Montserrat.Lovaas@hfk.no', 'Lærer', '325', '1STE'], ['Mercedes Ayala', 'Morales', 'mercedes.ayala.morales@hfk.no', 'Miljøfagarbeider', '', ''], ['Finn', 'Mortensen', 'Finn.Mortensen@hfk.no', 'Lærer', '523', '3PBPBYA'], ['Åge Ingmar', 'Mortvedt', 'Age.Inge.Mortvedt@hfk.no', 'Lærer', '545', ''], ['Linda Therese', 'Myklebust', 'Linda.Therese.Myklebust@hfk.no', 'Lærer', '345', '1SSB'], ['Ole-Jakob', 'Møklebust', 'Ole-Jakob.Moklebust@hfk.no', 'Lærer', '325', '1STF'], ['Stine Haktorsen', 'Nerhus', 'Stine.Nerhus@hfk.no', 'Lærer', '522', '3STUSPH'], ['Tuyet Cam Thi', 'Nguyen', 'Tuyet.Cam.Thi.Nguyen@hfk.no', 'Renholder', '', ''], ['Christian Lunde', 'Nilsen', 'Christian.Nilsen@hfk.no', 'Lærer', '545', ''], ['Leif-Kjetil', 'Nordanger Mjelde', 'Leif-Kjetil.Nordanger.Mjelde@hfk.no', 'IKT lærling', '444', ''], ['Jan Kristian', 'Olsen', 'Jan.Kristian.Olsen@hfk.no', 'Lærer', '544', ''], ['Maria Jose Sanchez', 'Olsen', 'Maria.Olsen@hfk.no', 'Avdelingsleder', '229', ''], ['Øystein', 'Ormåsen', 'Oystein.Ormasen@hfk.no', 'Lærer', '326', '1STI'], ['Merete Skrede', 'Pontes', 'Merete.Pontes@hfk.no', 'Lærer', '344', '2RLVA'], ['Arnfinn', 'Refvik', 'Arnfinn.Refvik@hfk.no', 'Lærer', '345', '1SSD'], ['Bjørn Rune', 'Roti', 'Bjorn.Rune.Roti@hfk.no', 'Lærer', '545', ''], ['Silvia', 'Rovira Ribó', 'Silvia.Rovira.Ribo@hfk.no', 'Avdelingsleder', '228', ''], ['Grete Karin', 'Rye', 'Grete.Karin.Rye@hfk.no', 'Elevinspektør', '447', ''], ['Ørjan', 'Røthe', 'Orjan.Rothe@bergen.kommune.no', 'Psykolog', '451', ''], ['Sigurd', 'Sandvik', 'Sigurd.Sandvik@hfk.no', 'Lærer', '344', '1HTB'], ['Geir', 'Sandøy', 'Geir.Sandoy@hfk.no', 'Rådgiver', '448', ''], ['Christiane', 'Schmidt', 'Christiane.Schmidt@hfk.no', 'Lærer', '324', '1STC'], ['Ewa Maria', 'Siarkiewicz-Bivand', 'Ewa.Siarkiewicz-Bivand@hfk.no', 'Lærer', '324', '1STB'], ['Ingunn Anita L ', 'Silver', 'ingunn.silver@hfk.no', 'Kontor', '232', ''], ['Lill Mari Vibe', 'Simonsen', 'Lill.Mari.Simonsen@hfk.no', 'Lærer', '523', '3MKMEDA'], ['Rungraporn', 'Siriket', 'Rungraporn.Siriket@hfk.no', 'Renholder', '', ''], ['Britt Heidi', 'Sivertsen', '"Britt.Heidi.Sivertsen@hfk.no
"', 'Lærer', '545', ''], ['Anne-Gerd M', 'Sivertsen', 'anne-gerd.sivertsen@hfk.no', 'Kontor', '232', ''], ['Ida Sæbøe', 'Sjøstrand', 'Ida.Sjostrand@hfk.no', 'Lærer', '544', ''], ['Tove Margrethe', 'Slettebakken', 'Tove.Margret.Slettebakken@hfk.no', 'Lærer', '523', ''], ['Cathrine Børufsen', 'Solberg', 'Cathrine.Solberg@hfk.no', 'Lærer', '545', ''], ['Øyvind', 'Solberg', 'Oyvind.Solberg@hfk.no', 'IKT leder', '443', ''], ['Sissel', 'Solberg-Johansen', 'Sissel.Solberg-Johansen@hfk.no', 'Lærer', '521', '3STUSPA'], ['Silje Monsen', 'Solsvik', 'Silje.Monsen.Solsvik@hfk.no', 'Bibliotekar', '', ''], ['Liv', 'Soulere', 'Liv.Soulere@hfk.no', 'Lærer', '346', ''], ['Brith', 'Spidsø', 'Brith.Spidso@hfk.no', 'Lærer', '345', ''], ['Kristine Sivertsen', 'Stenhaug', 'Kristine.Sivertsen.Stenhaug@hfk.no', 'Adm leder', '232', ''], ['Anny', 'Strand', 'Anny.Strand@hfk.no', 'Lærer', '545', ''], ['Per Christian', 'Strøm', 'Per.Christian.Strom@hfk.no', 'Lærer', '522', ''], ['Haifeng', 'Sun', 'Haifeng.Sun@hfk.no', 'Lærer', '543', ''], ['Gunhild Gundersen', 'Sylte', 'Gunhild.Sylte@hfk.no', 'Lærer', '521', '3STUSPE'], ['Monica', 'Sæther', 'Monica.Saether@hfk.no', 'Lærer', '324', '1STA'], ['Frode', 'Sætre', 'Frode.Saethre@hfk.no', 'Lærer', '346', '2ISFA'], ['Naomi ', 'Søreide', 'Naomi.Soreide@hfk.no', 'Renholder', '', ''], ['Jan Erik', 'Sørensen', 'Jan.Erik.Sorensen@hfk.no', 'Lærer', '345', '1SSC'], ['Tone', 'Taule', 'Tone.Taule@hfk.no', 'Lærer', '421', ''], ['Edeltraud Schmie', 'Thomassen', 'Edeltraud.Thomasen@hfk.no', 'Lærer', '421', ''], ['Vibeke T Falch', 'Thomassen', 'vibeke.thomassen@hfk.no', 'Kontor', '232', ''], ['Sigurlin Thora', 'Thorbergsdottir', 'sigurlin@gmail.com', 'Lærer', '423', ''], ['Mona', 'Thorbjørnsen', 'Mona.Thorbjornsen@bergen.kommune.no', 'Helsesøster', '450', ''], ['Mette Irene', 'Tislevoll', 'Mette.Irene.Tislevoll@hfk.no', 'Lærer', '325', '1STE'], ['Inge Leon', 'Turøy', 'Inge.Leon.Turoy@hfk.no', 'Rådgiver', '446', ''], ['Jorid', 'Valestrand', 'Jorid.Valestrand@hfk.no', 'Rådgiver', '445', ''], ['Hilde', 'Visnes', 'Hilde.Visnes@hfk.no', 'Lærer', '346', ''], ['Erik', 'Vollmer', 'Erik.Vollmer@hfk.no', 'Bibliotekar', '', ''], ['Helen', 'Vølstad', 'Helen.Volstad@hfk.no', 'Lærer', '423', '2STUSPF'], ['Hans Michael', 'Wade', 'Hans.Michael.Wade@hfk.no', 'Lærer', '345', '1SSA'], ['Lisbet Espeland', 'Ystanes', 'Lisbet.Ystanes@hfk.no', 'Lærer', '422', '2STUSPD'], ['Sjur', 'Århus', 'Sjur.Arhus@hfk.no', 'Lærer', '344', '']
        
        for items in toadd:        
            page = api.content.create(container=folder, type='ansatt', title=items[1], e_mail=items[2])
        return "Done"