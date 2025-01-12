# -*- coding: utf-8 -*-
try:
    from lib.client import cfscraper
except ImportError:
    from client import cfscraper
try:
    from lib.helper import *
except:
    from helper import *
import re


# def buscar_chaves(dicionario, chave_alvo, caminho_atual=""):
#     if isinstance(dicionario, dict):
#         for chave, valor in dicionario.items():
#             novo_caminho = f"{caminho_atual}['{chave}']" if caminho_atual else f"['{chave}']"
#             if chave == chave_alvo:
#                 print(f"Chave encontrada: {novo_caminho} -> {valor}")
#             buscar_chaves(valor, chave_alvo, novo_caminho)
#     elif isinstance(dicionario, list):
#         for index, item in enumerate(dicionario):
#             novo_caminho = f"{caminho_atual}[{index}]"
#             buscar_chaves(item, chave_alvo, novo_caminho)

class IMDBScraper:
    def __init__(self):
        self.base = 'https://www.imdb.com'
        self.headers = {
        'Accept-Language': 'pt-BR,pt;q=0.9,en;q=0.8'
        }
    def soup(self,html):
        soup = BeautifulSoup(html, 'html.parser')
        return soup

    def search_series(self,search):
        itens = []
        try:
            query = quote(search)
            url = '{0}/find/?q={1}&s=tt&ttype=tv'.format(self.base,query)
            html = cfscraper.get(url,headers=self.headers).text
            json_ = re.findall(r'<script id="__NEXT_DATA__" type="application/json">(.+?)</script>', html,re.DOTALL)[0]
            data = json.loads(json_)
            results = data['props']['pageProps']['titleResults']['results']
            for idx, serie in enumerate(results):
                imdb_id = serie['id']
                page = self.base + '/title/' + imdb_id  +'/?ref_=fn_tt_tt_' + str(idx)
                name = serie['titleNameText']
                try:
                    year = serie['titleReleaseText']
                    try:
                        year = year.split('–')[0]
                    except:
                        pass
                    enable_year = True
                except:
                    enable_year = False
                    year = '0'
                try:
                    img = serie['titlePosterImageModel']['url']
                except:
                    img = ''
                if enable_year:
                    name = name + ' (' + str(year) + ')'
                name = name.replace('&amp;', '&').replace('&apos;', "'")
                itens.append((name,img,page,year,imdb_id))
        except:
            pass       
        return itens


    def series_250(self):
        itens = []
        try:
            url = self.base + '/chart/toptv/?ref_=nv_tvv_250'
            html = cfscraper.get(url,headers=self.headers).text
            soup = self.soup(html)
            ul_element = soup.select('ul[class^="ipc-metadata-list"]')[0]
            li_elements = ul_element.select('li[class^="ipc-metadata-list-summary-item"]')
            if li_elements:
                for li in li_elements:
                    image = str(li.find_all('img')[0].get('src', '')).replace('140_', '800_').replace(',1,', ',').replace(',0,', ',').replace('140,207_', '500,800_').replace('207_', '800_')
                    a = li.select('a[class^="ipc-title-link-wrapper"]')[0]
                    url = self.base + a.get('href', '')
                    try:
                        name = str(a.text).split('. ')[1]
                    except:
                        name = a.text
                    try:
                        name = name.decode('utf-8')
                    except:
                        pass
                    year = str(li.select('div[class$="cli-title-metadata"]')[0].select('span[class$="cli-title-metadata-item"]')[0].text).split('–')[0]
                    try:
                        year = year.decode('utf-8')
                    except:
                        pass
                    imdb_id = re.findall(r'/tt(.*?)/', url)[0]
                    imdb_id = 'tt' + imdb_id
                    name = name.replace('&amp;', '&').replace('&apos;', "'") 
                    description = ''
                    name = name + ' (' + year + ')'
                    itens.append((name,image,url,description,imdb_id))
        except:
            pass             
        return itens 
    
    def series_popular(self):
        itens = [] 
        try:
            url = self.base + '/chart/tvmeter/?ref_=nv_tvv_mptv'
            html = cfscraper.get(url,headers=self.headers).text
            soup = self.soup(html)
            ul_element = soup.select('ul[class^="ipc-metadata-list"]')[0]
            li_elements = ul_element.select('li[class^="ipc-metadata-list-summary-item"]')
            if li_elements:
                for li in li_elements:
                    image = str(li.find_all('img')[0].get('src', '')).replace('140_', '800_').replace(',1,', ',').replace(',0,', ',').replace('140,207_', '500,800_').replace('207_', '800_')
                    a = li.select('a[class^="ipc-title-link-wrapper"]')[0]
                    url = self.base + a.get('href', '')
                    try:
                        name = str(a.text).split('. ')[1]
                    except:
                        name = a.text
                    try:
                        name = name.decode('utf-8')
                    except:
                        pass
                    year = str(li.select('div[class$="cli-title-metadata"]')[0].select('span[class$="cli-title-metadata-item"]')[0].text).split('–')[0]
                    try:
                        year = year.decode('utf-8')
                    except:
                        pass
                    imdb_id = re.findall(r'/tt(.*?)/', url)[0]
                    imdb_id = 'tt' + imdb_id
                    name = name.replace('&amp;', '&').replace('&apos;', "'") 
                    description = ''
                    name = name + ' (' + year + ')'
                    itens.append((name,image,url,description,imdb_id))
        except:
            pass             
        return itens      
  
    
    def imdb_seasons(self,url):
        itens = []
        try:
            html = cfscraper.get(url,headers=self.headers).text
            json_ = re.findall(r'<script id="__NEXT_DATA__" type="application/json">(.+?)</script>', html,re.DOTALL)[0]
            data = json.loads(json_)
            seasons = data['props']['pageProps']['mainColumnData']['episodes']['seasons']
            imdb_id = re.findall(r'/tt(.*?)/', url)[0]
            imdb_id = 'tt' + imdb_id
            season_base_url = self.base + '/title/' + imdb_id + '/episodes/?season='
            # for idx, season in enumerate(seasons, start=1):
            #     name = 'Temporada {0}'.format(str(idx))
            #     url_season = season_base_url + str(idx)
            #     itens.append((str(season['number']), name, url_season))
            for season in seasons:
                season_number = season.get('number', 0) 
                name = 'Temporada {0}'.format(str(season_number))
                url_season = season_base_url + str(season_number)
                itens.append((str(season_number), name, url_season))            
        except:
            pass
        if itens:
            itens = itens[::-1]
        return itens

    def imdb_episodes(self,url):
        itens = []
        try:
            html = cfscraper.get(url,headers=self.headers).text
            json_ = re.findall(r'<script id="__NEXT_DATA__" type="application/json">(.+?)</script>', html,re.DOTALL)[0]
            data = json.loads(json_)
            episodes = data['props']['pageProps']['contentData']['section']['episodes']['items']
            try:
                fanart = data['props']['pageProps']['contentData']['entityMetadata']['primaryImage']['url']
            except:
                fanart = ''
            if episodes:
                for idx, episode in enumerate(episodes, start=1):
                    episode_number = str(idx)
                    name = episode.get('titleText', 'Episodio - ' + episode_number)
                    try:
                        img = episode['image']['url']
                    except:
                        img = ''
                    description = episode.get('plot', '')
                    name = name.replace('&amp;', '&').replace('&apos;', "'")
                    description = description.replace('&amp;', '&').replace('&apos;', "'")
                    itens.append((episode_number,name,img,fanart,description))
        except:
            pass
        return itens
    
    def search_movies(self,search):
        itens = []
        try:
            query = quote(search)
            url = '{0}/find/?q={1}&s=tt&ttype=ft'.format(self.base,query)
            html = cfscraper.get(url,headers=self.headers).text
            json_ = re.findall(r'<script id="__NEXT_DATA__" type="application/json">(.+?)</script>', html,re.DOTALL)[0]
            data = json.loads(json_)
            results = data['props']['pageProps']['titleResults']['results']
            for idx, movie in enumerate(results):
                imdb_id = movie['id']
                page = self.base + '/title/' + imdb_id  +'/?ref_=fn_tt_tt_' + str(idx)
                name = movie['titleNameText']
                try:
                    year = movie['titleReleaseText']
                    try:
                        year = year.split('–')[0]
                    except:
                        pass
                    enable_year = True
                except:
                    enable_year = False
                    year = '0'
                try:
                    img = movie['titlePosterImageModel']['url']
                except:
                    img = ''
                if enable_year:
                    name = name + ' (' + str(year) + ')'
                name = name.replace('&amp;', '&').replace('&apos;', "'")
                itens.append((name,img,page,year,imdb_id))
        except:
            pass       
        return itens   

    def movies_250(self):
        itens = [] 
        try:
            url = self.base + '/chart/top/?ref_=nv_mv_250'
            html = cfscraper.get(url,headers=self.headers).text
            soup = self.soup(html)
            ul_element = soup.select('ul[class^="ipc-metadata-list"]')[0]
            li_elements = ul_element.select('li[class^="ipc-metadata-list-summary-item"]')
            if li_elements:
                for li in li_elements:
                    image = str(li.find_all('img')[0].get('src', '')).replace('140_', '800_').replace(',1,', ',').replace(',0,', ',').replace('140,207_', '500,800_').replace('207_', '800_')
                    a = li.select('a[class^="ipc-title-link-wrapper"]')[0]
                    url = self.base + a.get('href', '')
                    try:
                        name = str(a.text).split('. ')[1]
                    except:
                        name = a.text
                    try:
                        name = name.decode('utf-8')
                    except:
                        pass
                    year = str(li.select('div[class$="cli-title-metadata"]')[0].select('span[class$="cli-title-metadata-item"]')[0].text).split('–')[0]
                    try:
                        year = year.decode('utf-8')
                    except:
                        pass
                    imdb_id = re.findall(r'/tt(.*?)/', url)[0]
                    imdb_id = 'tt' + imdb_id
                    name = name.replace('&amp;', '&').replace('&apos;', "'") 
                    description = ''
                    name = name + ' (' + year + ')'
                    itens.append((name,image,url,description,imdb_id))            
        except:
            pass
        return itens  

    def movies_popular(self):
        itens = [] 
        try:
            url = self.base + '/chart/moviemeter/?ref_=nv_mv_mpm'
            html = cfscraper.get(url,headers=self.headers).text
            soup = self.soup(html)
            ul_element = soup.select('ul[class^="ipc-metadata-list"]')[0]
            li_elements = ul_element.select('li[class^="ipc-metadata-list-summary-item"]')
            if li_elements:
                for li in li_elements:
                    image = str(li.find_all('img')[0].get('src', '')).replace('140_', '800_').replace(',1,', ',').replace(',0,', ',').replace('140,207_', '500,800_').replace('207_', '800_')
                    a = li.select('a[class^="ipc-title-link-wrapper"]')[0]
                    url = self.base + a.get('href', '')
                    try:
                        name = str(a.text).split('. ')[1]
                    except:
                        name = a.text
                    try:
                        name = name.decode('utf-8')
                    except:
                        pass
                    year = str(li.select('div[class$="cli-title-metadata"]')[0].select('span[class$="cli-title-metadata-item"]')[0].text).split('–')[0]
                    try:
                        year = year.decode('utf-8')
                    except:
                        pass
                    imdb_id = re.findall(r'/tt(.*?)/', url)[0]
                    imdb_id = 'tt' + imdb_id
                    name = name.replace('&amp;', '&').replace('&apos;', "'") 
                    description = ''
                    name = name + ' (' + year + ')'
                    itens.append((name,image,url,description,imdb_id))            
        except:
            pass
        return itens  

