# -*- coding: utf-8 -*-
try:
    from lib.client import cfscraper, USER_AGENT
except ImportError:
    from client import cfscraper, USER_AGENT
try:
    from lib.helper import *
except ImportError:
    from helper import *
import re
try:
    from lib import jsunpack
except ImportError:
    import jsunpack

try:
    from lib import tear
except ImportError:
    import tear


class VOD1:
    def __init__(self,url):
        self.base = url

    def soup(self,src):
        soup = BeautifulSoup(src,'html.parser')
        return soup
    
    def get_packed_data(self,html):
        packed_data = ''
        try:
            for match in re.finditer(r'''(eval\s*\(function\(p,a,c,k,e,.*?)</script>''', html, re.DOTALL | re.I):
                r = match.group(1)
                t = re.findall(r'(eval\s*\(function\(p,a,c,k,e,)', r, re.DOTALL | re.IGNORECASE)
                if len(t) == 1:
                    if jsunpack.detect(r):
                        packed_data += jsunpack.unpack(r)
                else:
                    t = r.split('eval')
                    t = ['eval' + x for x in t if x]
                    for r in t:
                        if jsunpack.detect(r):
                            packed_data += jsunpack.unpack(r)
        except:
            pass
        return packed_data

    def pesquisa_filmes(self,url,pesquisa):
        itens_pesquisa = []
        next_page = False
        page = ''
        if pesquisa:
            url = '%s/?s=%s'%(self.base,quote_plus(pesquisa))           
        try:
            #headers.update({'Cookie': 'XCRF%3DXCRF'})
            r = cfscraper.get(url,headers={'Cookie': 'XCRF%3DXCRF'})
            src = r.text
            soup = self.soup(src)
            box = soup.find("div", {"id": "box_movies"})
            movies = box.findAll("div", {"class": "movie"})
            for i in movies:
                name = i.find('h2').text
                try:
                    name = name.decode('utf-8')
                except:
                    pass
                try:
                    year = i.find('span', {'class': 'year'}).text
                    year = year.replace('–', '')
                except:
                    year = ''
                img = i.find('div', {'class': 'imagen'})
                iconimage = img.find('img').get('src', '')
                iconimage = iconimage.replace('-120x170', '')
                link = img.find('a').get('href', '')
                if '/tvshows/' in link:
                    name = '%s (Série)'%name
                else:
                    if 'hdcam' in link and not 'hdcam' in name.lower():
                        name = '%s (Filme) (HDCAM)'%name
                    else:
                        name = '%s (Filme)'%name
                if year:
                    name = '[B]%s (%s)[/B]'%(name,str(year))
                else:
                    name = '[B]%s[/B]'%name                
                itens_pesquisa.append((name,iconimage,link))
            try:
                div = soup.find('div', {'id': 'paginador'}).find('div', {'class': 'paginado'})
                current = div.find('span', {'class': 'current'}).text
                a = div.findAll('a')
                for i in a:
                    href = i.get('href', '')
                    nxt = str(int(current) + 1)
                    if nxt in href:
                        next_page = href
                        try:
                            page_ = next_page.split('page/')[1]
                            try:
                                page = page_.split('/')[0]
                            except:
                                page = page_
                        except:
                            pass
                        break

            except:
                pass
        except:
            pass
        return itens_pesquisa, next_page, page 

    def scraper_filmes(self, url=''):
        if not url:
            url = self.base + '/category/ultimos-filmes/'
        filmes = []
        next_page = False
        page = ''
        try:
            #headers.update({'Cookie': 'XCRF%3DXCRF'})
            r = cfscraper.get(url,headers={'Cookie': 'XCRF%3DXCRF'})
            src = r.text
            soup = self.soup(src)
            box = soup.find("div", {"id": "box_movies"})
            movies = box.findAll("div", {"class": "movie"})
            for i in movies:
                name = i.find('h2').text
                img = i.find('div', {'class': 'imagen'})
                iconimage = img.find('img').get('src', '')
                iconimage = iconimage.replace('-120x170', '')
                link = img.find('a').get('href', '')                
                try:
                    name = name.decode('utf-8')
                except:
                    pass
                try:
                    year = i.find('span', {'class': 'year'}).text
                    year = year.replace('–', '')
                except:
                    year = ''
                if year:
                    if 'hdcam' in link and not 'hdcam' in name.lower():
                        name = '[B]%s (%s) (HDCAM)[/B]'%(name,str(year))
                    else:
                        name = '[B]%s (%s)[/B]'%(name,str(year))
                else:
                    if 'hdcam' in link and not 'hdcam' in name.lower():
                        name = '[B]%s (HDCAM)[/B]'%name
                    else:
                        name = '[B]%s[/B]'%name
                filmes.append((name,iconimage,link))
            try:
                div = soup.find('div', {'id': 'paginador'}).find('div', {'class': 'paginado'})
                current = div.find('span', {'class': 'current'}).text
                a = div.findAll('a')
                for i in a:
                    href = i.get('href', '')
                    nxt = str(int(current) + 1)
                    if nxt in href:
                        next_page = href
                        try:
                            page_ = next_page.split('page/')[1]
                            try:
                                page = page_.split('/')[0]
                            except:
                                page = page_
                        except:
                            pass
                        break

            except:
                pass
        except:
            pass
        return filmes, next_page, page

    def opcoes_filmes(self,url):
        opcoes = []      
        try:
            #headers.update({'Cookie': 'XCRF%3DXCRF'})
            r = cfscraper.get(url,headers={'Cookie': 'XCRF%3DXCRF'})
            src = r.text
            soup = self.soup(src)
            player = soup.find('div', {'id': 'player-container'})
            botoes = player.find('ul', {'class': 'player-menu'})
            op = botoes.findAll('li')
            op_list = []
            if op:
                for i in op:
                    a = i.find('a')
                    id_ = a.get('href', '').replace('#', '')
                    op_name = a.text
                    try:
                        op_name = op_name.decode('utf-8')
                    except:
                        pass
                    op_name = op_name.replace(' 1', '').replace(' 2', '').replace(' 3', '').replace(' 4', '').replace(' 5', '')
                    op_name = op_name.strip()
                    op_name = op_name.upper()
                    op_list.append((op_name,id_))
            if op_list:
                for name, id_ in op_list:
                    iframe = player.find('div', {'class': 'play-c'}).find('div', {'id': id_}).find('iframe').get('src', '')
                    if not 'streamtape' in iframe:
                        link = self.base + '/' + iframe
                    else:
                        link = iframe
                    opcoes.append((name,link))

        except:
            pass
        return opcoes

    def scraper_series(self, url=''):
        if not url:
            url = self.base + '/tvshows/'          
        series = []
        next_page = False
        page = ''
        try:
            #headers.update({'Cookie': 'XCRF%3DXCRF'})
            r = cfscraper.get(url,headers={'Cookie': 'XCRF%3DXCRF'})
            src = r.text
            soup = self.soup(src)
            box = soup.find("div", {"id": "box_movies"})
            movies = box.findAll("div", {"class": "movie"})
            for i in movies:
                name = i.find('h2').text
                try:
                    name = name.decode('utf-8')
                except:
                    pass
                try:
                    year = i.find('span', {'class': 'year'}).text
                    year = year.replace('–', '')
                except:
                    year = ''
                if year:
                    name = '[B]%s (%s)[/B]'%(name,str(year))
                else:
                    name = '[B]%s[/B]'%name
                img = i.find('div', {'class': 'imagen'})
                iconimage = img.find('img').get('src', '')
                iconimage = iconimage.replace('-120x170', '')
                link = img.find('a').get('href', '')
                series.append((name,iconimage,link))
            try:
                div = soup.find('div', {'id': 'paginador'}).find('div', {'class': 'paginado'})
                current = div.find('span', {'class': 'current'}).text
                a = div.findAll('a')
                for i in a:
                    href = i.get('href', '')
                    nxt = str(int(current) + 1)
                    if nxt in href:
                        next_page = href
                        try:
                            page_ = next_page.split('page/')[1]
                            try:
                                page = page_.split('/')[0]
                            except:
                                page = page_
                        except:
                            pass
                        break

            except:
                pass
        except:
            pass
        return series, next_page, page

    def scraper_temporadas_series(self,url):
        url_original = url       
        list_seasons = []
        serie_name_final = ''
        img = ''
        fanart = ''        
        try:
            #headers.update({'Cookie': 'XCRF%3DXCRF'})
            r = cfscraper.get(url, headers={'Cookie': 'XCRF%3DXCRF'})
            src = r.text
            soup = self.soup(src)
            # info
            try:
                div_img = soup.find('div', {'id': 'movie'}).find('div', {'class': 'post'}).find('div', {'class': 'headingder'})
                fanart = div_img.find('div', class_=lambda x: x and 'lazyload' in x).get('data-bg', '')
                img = div_img.find('img', {'class': 'lazyload'}).get('data-src', '')
                try:
                    serie_name = div_img.find('div', {'class': 'datos'}).find('div', {'class': 'dataplus'}).find('h1').text
                    try:
                        serie_name = serie_name.decode('utf-8')
                    except:
                        pass
                    serie_name_final = '[B]:::: SÉRIE: %s ::::[/B]'%serie_name
                except:
                    pass
            except:
                pass
            s = soup.find('div', {'id': 'movie'}).find('div', {'class': 'post'}).find('div', {'id': 'cssmenu'}).find('ul').findAll('li', {'class': 'has-sub'})
            for n, i in enumerate(s):
                n += 1
                name = '[B]TEMPORADA %s[/B]'%str(n)
                season = str(n)
                list_seasons.append((season,name,url_original))
        except:
            pass
        return serie_name_final, img, fanart, list_seasons 

    def scraper_episodios_series(self,url,season):
        list_episodes = []
        serie_name_final = ''
        img = ''
        fanart = ''        
        try:
            #headers.update({'Cookie': 'XCRF%3DXCRF'})
            r = cfscraper.get(url, headers={'Cookie': 'XCRF%3DXCRF'})
            src = r.text
            soup = self.soup(src)
            # info
            try:
                div_img = soup.find('div', {'id': 'movie'}).find('div', {'class': 'post'}).find('div', {'class': 'headingder'})
                fanart = div_img.find('div', class_=lambda x: x and 'lazyload' in x).get('data-bg', '')
                img = div_img.find('img', {'class': 'lazyload'}).get('data-src', '')
                try:
                    serie_name = div_img.find('div', {'class': 'datos'}).find('div', {'class': 'dataplus'}).find('h1').text
                    try:
                        serie_name = serie_name.decode('utf-8')
                    except:
                        pass
                    serie_name_final = '[B]:::: SÉRIE: %s ::::[/B]'%serie_name
                except:
                    pass
            except:
                pass
            s = soup.find('div', {'id': 'movie'}).find('div', {'class': 'post'}).find('div', {'id': 'cssmenu'}).find('ul').findAll('li', {'class': 'has-sub'})
            for n, i in enumerate(s):
                n += 1
                if int(season) == n:
                    e = i.find('ul').findAll('li')
                    for n, i in enumerate(e):
                        n += 1
                        e_info = i.find('a')
                        link = e_info.get('href')
                        ep_name = e_info.find('span', {'class': 'datix'}).text
                        try:
                            ep_name = ep_name.decode('utf-8')
                        except:
                            pass
                        ep_name = ep_name.strip()
                        name_especial = '[B]%s - %s x %s - %s[/B]'%(serie_name,str(season),str(n),ep_name)
                        ep_name2 = '[B]%s - %s[/B]'%(str(n),ep_name)
                        list_episodes.append((ep_name2,name_especial,link))
                    break
        except:
            pass
        return serie_name_final, img, fanart, list_episodes                                  
    


class VOD2:
    def __init__(self, url):
        self.base = url

    def tvshows(self,imdb,season,episode):
        stream = ''
        try:
            if imdb and season and episode:
                url = '{0}/serie/{1}/{2}/{3}'.format(self.base,imdb,season,episode)
                parsed_url_r = urlparse(url)
                r_ = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_url_r)
                r = cfscraper.get(url)
                src = r.text
                soup = BeautifulSoup(src, 'html.parser')
                div = soup.find('div', class_='episodeOption active')
                data_contentid = div['data-contentid']
                api = '{0}/api'.format(self.base)
                r = cfscraper.post(api,data={'action': 'getOptions', 'contentid': data_contentid})
                src = r.json()
                id_ = src['data']['options'][0]['ID']
                r = cfscraper.post(api,data={'action': 'getPlayer', 'video_id': id_})
                src = r.json()
                video_url = src['data']['video_url']
                video_hash = video_url.split('/')[-1]
                parsed_url = urlparse(video_url)
                origin = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_url)
                player = '{uri.scheme}://{uri.netloc}/player/index.php?data={0}&do=getVideo'.format(video_hash, uri=parsed_url)
                r = cfscraper.get(video_url, headers={'Referer': self.base + '/'})
                cookies_dict = r.cookies.get_dict()
                r = cfscraper.post(player,headers={'Origin': origin, 'x-requested-with': 'XMLHttpRequest'}, data={'hash': str(video_hash), 'r': r_}, cookies=cookies_dict)
                src = r.json()
                stream = src['videoSource'] + '|User-Agent=' + quote_plus(USER_AGENT)
        except:
            pass
        return stream
    
    def movie(self,imdb):
        stream = ''
        try:
            if imdb:
                url = '{0}/filme/{1}'.format(self.base,imdb)
                parsed_url_r = urlparse(url)
                r_ = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_url_r)
                r = cfscraper.get(url)
                src = r.text
                soup = BeautifulSoup(src, 'html.parser')
                div = soup.find('div',{'class': 'players_select'}) # dublado
                data_id = div.find('div', {'class': 'player_select_item'}).get('data-id', '')
                api = '{0}/api'.format(self.base)
                r = cfscraper.post(api,data={'action': 'getPlayer', 'video_id': data_id})
                src = r.json()
                video_url = src['data']['video_url']
                video_hash = video_url.split('/')[-1]
                parsed_url = urlparse(video_url)
                origin = '{uri.scheme}://{uri.netloc}'.format(uri=parsed_url)
                player = '{uri.scheme}://{uri.netloc}/player/index.php?data={0}&do=getVideo'.format(video_hash, uri=parsed_url)
                r = cfscraper.get(video_url, headers={'Referer': self.base + '/'})
                cookies_dict = r.cookies.get_dict()
                r = cfscraper.post(player,headers={'Origin': origin, 'x-requested-with': 'XMLHttpRequest'}, data={'hash': str(video_hash), 'r': r_}, cookies=cookies_dict)
                src = r.json()
                stream = src['videoSource'] + '|User-Agent=' + quote_plus(USER_AGENT)
        except:
            pass
        return stream


    
class Tube:
    def __init__(self,url):
        self.api = 'https://www.youtube.com/youtubei/v1/player'
        self.key = 'AIzaSyAO_FJ2SlqU8Q4STEHLGCilw_Y9_11qcW8'
        self.length = 0
        self.title = ''
        self.author = ''
        self.thumbnail = ''
        self.url = ''
        self.itag_map = {'5': '240', '6': '270', '17': '144', '18': '360', '22': '720', '34': '360', '35': '480',
    '36': '240', '37': '1080', '38': '3072', '43': '360', '44': '480', '45': '720', '46': '1080',
    '82': '360 [3D]', '83': '480 [3D]', '84': '720 [3D]', '85': '1080p [3D]', '100': '360 [3D]',
    '101': '480 [3D]', '102': '720 [3D]', '92': '240', '93': '360', '94': '480', '95': '720',
    '96': '1080', '132': '240', '151': '72', '133': '240', '134': '360', '135': '480',
    '136': '720', '137': '1080', '138': '2160', '160': '144', '264': '1440',
    '298': '720', '299': '1080', '266': '2160', '167': '360', '168': '480', '169': '720',
    '170': '1080', '218': '480', '219': '480', '242': '240', '243': '360', '244': '480',
    '245': '480', '246': '480', '247': '720', '248': '1080', '271': '1440', '272': '2160',
    '302': '2160', '303': '1080', '308': '1440', '313': '2160', '315': '2160', '59': '480'}
        self.headers = {'User-Agent': 'com.google.android.apps.youtube.music/', 'Accept-Language': 'en-US,en'}
        self.result = self.scrape_api(self.get_id(url))                     
        
    def get_id(self,url):
        video_id = ''
        video_id_match = re.search(r'v=([A-Za-z0-9_-]+)', url)
        if video_id_match:
            video_id += video_id_match.group(1)
        return video_id
    
    def pick_source(self,sources):
        return sources[0][1]

    def __key(self, item):
        try:
            return int(re.search(r'(\d+)', item[0]).group(1))
        except:
            return 0 

    def select_video(self,sources):
        if sources:
            sources.sort(key=self.__key, reverse=True)
            video = self.pick_source(sources)
        else:
            video = ''
        return video                
    
    def scrape_api(self,video_id):
        api = self.api + '?videoId=' + video_id + '&key=' + self.key + '&contentCheckOk=True&racyCheckOk=True'
        json_music = {
            "context": {
                "client": {
                    "androidSdkVersion": 30,
                    "clientName": "ANDROID_MUSIC",
                    "clientVersion": "5.16.51"
                }
            }
        }
        json_normal = {
            "context": {
                "client": {
                    "androidSdkVersion": 30,
                    "clientName": "ANDROID_EMBEDDED_PLAYER",
                    "clientScreen": "EMBED",
                    "clientVersion": "17.31.35"
                }
            }
        }
        result = {}
        response_music = requests.post(api, headers=self.headers, json=json_music)
        if response_music.status_code == 200:
            r = response_music.json()
            details = r['videoDetails']
            self.length = int(details['lengthSeconds'])
            self.title = details['title']
            self.author = details['author']
            thumb = details['thumbnail']['thumbnails']
            try:
                select_thumb = [image['url'] for image in thumb][-1]
                self.thumbnail = select_thumb
            except:
                pass
            ok_music = r.get("streamingData", False)
            if ok_music:
                result = r
        if not result:
            response_music = requests.post(api, headers=self.headers, json=json_normal)
            if response_music.status_code == 200:
                r = response_music.json()
                ok_normal = r.get("streamingData", False)
                if ok_normal:
                    result = r
        if result:
            videos = result['streamingData']['formats']
            sources = [(v['qualityLabel'], v['url']) for v in videos]
            sources = [(self.itag_map.get(quality, 'Unknown Quality [%s]' % quality), stream) for quality, stream in sources]
            self.url = self.select_video(sources)

        return result

# youtube2
class Tube2:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0'}
        self.service = 'https://www.y2mate.com'
        self.itag_map = {'5': '240', '6': '270', '17': '144', '18': '360', '22': '720', '34': '360', '35': '480',
        '36': '240', '37': '1080', '38': '3072', '43': '360', '44': '480', '45': '720', '46': '1080',
        '82': '360 [3D]', '83': '480 [3D]', '84': '720 [3D]', '85': '1080p [3D]', '100': '360 [3D]',
        '101': '480 [3D]', '102': '720 [3D]', '92': '240', '93': '360', '94': '480', '95': '720',
        '96': '1080', '132': '240', '151': '72', '133': '240', '134': '360', '135': '480',
        '136': '720', '137': '1080', '138': '2160', '160': '144', '264': '1440',
        '298': '720', '299': '1080', '266': '2160', '167': '360', '168': '480', '169': '720',
        '170': '1080', '218': '480', '219': '480', '242': '240', '243': '360', '244': '480',
        '245': '480', '246': '480', '247': '720', '248': '1080', '271': '1440', '272': '2160',
        '302': '2160', '303': '1080', '308': '1440', '313': '2160', '315': '2160', '59': '480'}

    def extract_id(self,url):
        v_id = url.split('v=')[1]
        try:
            v_id = v_id.split('&')[0]
        except:
            pass
        return v_id

    def get_info(self,url):
        params = {'k_query': url,
                  'k_page': 'home',
                  'hl': 'en',
                  'q_auto': '1'}
        origin = self.service
        referer = self.service + '/youtube/' + self.extract_id(url)
        headers = self.headers
        headers.update({'Origin': origin, 'Referer': referer})
        r = requests.post(self.service + '/mates/analyzeV2/ajax',headers=headers,data=params)
        if r.status_code == 200:
            return r.json()
        else:
            return {}
        
    def pick_source(self,sources):
        return sources[0][1]

    def __key(self, item):
        try:
            return int(re.search(r'(\d+)', item[0]).group(1))
        except:
            return 0 

    def select_video(self,sources):
        if sources:
            sources.sort(key=self.__key, reverse=True)
            video = self.pick_source(sources)
        else:
            video = ''
        return video          
    
    def get_video(self,url):
        d = self.get_info(url)
        if d:
            title = d['title']
            links = d['links']['mp4']
            keys_ = [(v, links[v]['k']) for v in links if not str(v) == 'auto' and not '3gp' in str(v)]
            keys = []
            for quality, k in keys_:
                try:
                    keys.append((self.itag_map.get(quality, 'Unknown Quality [%s]' % quality), k))
                except:
                    pass
            key = self.select_video(keys)
            params = {'vid': self.extract_id(url),
                    'k': key}
            origin = self.service          
            referer = self.service + '/youtube/' + self.extract_id(url)
            headers = self.headers
            headers.update({'Origin': origin, 'Referer': referer})
            count = 0
            while True:
                count += 1
                try:
                    r = requests.post(self.service + '/mates/convertV2/index',headers=headers,data=params)
                    if r.status_code == 200:
                        src = r.json()
                        status = src['c_status']
                        if status == 'CONVERTED':
                            download = src['dlink']
                            return download
                except:
                    pass
                if count == 15:
                    break          
        return ''    
    
class Resolver:
    def __init__(self):
        self.headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0'}

    def soup(self,src):
        soup = BeautifulSoup(src,'html.parser')
        return soup

    def get_packed_data(self,html):
        packed_data = ''
        try:
            for match in re.finditer(r'''(eval\s*\(function\(p,a,c,k,e,.*?)</script>''', html, re.DOTALL | re.I):
                r = match.group(1)
                t = re.findall(r'(eval\s*\(function\(p,a,c,k,e,)', r, re.DOTALL | re.IGNORECASE)
                if len(t) == 1:
                    if jsunpack.detect(r):
                        packed_data += jsunpack.unpack(r)
                else:
                    t = r.split('eval')
                    t = ['eval' + x for x in t if x]
                    for r in t:
                        if jsunpack.detect(r):
                            packed_data += jsunpack.unpack(r)
        except:
            pass
        return packed_data

    def append_headers(cls,headers):
        return '|%s' % '&'.join(['%s=%s' % (key, quote_plus(headers[key])) for key in headers]) 
    
    def pick_source(self,sources):
        return sources[0][1]
    
    def last_url(cls,url,headers):
        stream = ''
        try:
            r = requests.head(url,headers=headers,allow_redirects=True)
            stream = r.url
        except:
            pass
        return stream    

    def resolve_streamtape(self,url,referer):
        headers = self.headers
        link = ''
        try:
            correct_url = url.replace('/v/', '/e/')
            try:
                r = requests.head(correct_url,headers=headers,allow_redirects=True)
                correct_url = r.url
            except:
                pass            
            parsed_uri = urlparse(correct_url)
            protocol = parsed_uri.scheme
            host = parsed_uri.netloc
            if not referer:
                referer = '%s://%s/'%(protocol,host)
            headers.update({'Referer': referer})
            r = requests.get(correct_url,headers=headers)
            data = r.text
            link_part1_re = re.compile('<div.+?style="display:none;">(.*?)&token=.+?</div>').findall(data)
            link_part2_re = re.compile("&token=(.*?)'").findall(data)
            if link_part1_re and link_part2_re:
                part1 = link_part1_re[0]
                part2 = link_part2_re[-1]
                part1 = part1.replace(' ', '')
                if 'streamtape' in part1:
                    try:
                        part1 = part1.split('streamtape')[1]
                        final = 'streamtape' + part1 + '&token=' + part2
                        stream = 'https://' + final + '&stream=1'
                        last_stream = self.last_url(stream,headers=headers)
                        if last_stream:
                            link = last_stream + self.append_headers(headers)
                        else:
                            link = ''
                    except:
                        link = ''
                elif 'get_video' in part1:
                    try:
                        part1_1 = part1.split('get_video')[0]
                        part1_2 = part1.split('get_video')[1]
                        part1_1 = part1_1.replace('/', '')
                        part1 = part1_1 + '/get_video' + part1_2
                        final = part1 + '&token=' + part2
                        stream = 'https://' + final + '&stream=1'
                        last_stream = self.last_url(stream,headers=headers)
                        if last_stream:
                            link = last_stream + self.append_headers(headers)
                        else:
                            link = ''
                    except:
                        link = ''
        except:
            pass           
        return link
    
    def resolve_mixdrop(self,url,referer):
        headers = self.headers
        url = url.replace('.club', '.co')
        try:
            url = url.split('?')[0]
        except:
            pass
        try:
            #r = requests.head(url,headers={'User-Agent': cls.rand_ua()},allow_redirects=True)
            r = requests.head(url,headers=headers,allow_redirects=True)
            url = r.url
        except:
            pass
        stream = ''
        parsed_uri = urlparse(url)
        protocol = parsed_uri.scheme
        host = parsed_uri.netloc
        # if host.endswith('.club'):
        #     host = host.replace('.club', '.co')
        rurl = 'https://%s/'%host
        if referer:
            rurl = referer   
        #headers = {'Origin': rurl[:-1],'Referer': rurl, 'User-Agent': cls.rand_ua()}
        headers = {'Origin': rurl[:-1],'Referer': rurl, 'User-Agent': headers['User-Agent']}
        try:
            html = requests.get(url,headers=headers,allow_redirects=True).text
            #r = re.search(r'location\s*=\s*"([^"]+)', html)
            r = re.search(r'''location\s*=\s*["']([^'"]+)''', html)
            if r:
                url = 'https://%s%s'%(host,r.group(1))
                html = requests.get(url,headers=headers,allow_redirects=True).text
            if '(p,a,c,k,e,d)' in html:
                html = self.get_packed_data(html)
            r = re.search(r'(?:vsr|wurl|surl)[^=]*=\s*"([^"]+)', html)
            if r:
                surl = r.group(1)
                if surl.startswith('//'):
                    surl = 'https:' + surl
                #headers.pop('Origin')
                headers.update({'Referer': url})
                # headers.update({'Origin': 'https://mdzsmutpcvykb.net'})
                # headers.update({'Referer': 'https://mdzsmutpcvykb.net/'})
                stream = surl + self.append_headers(headers)
                return stream
        except:
            pass
        return 

    def resolve_brplayer(self,url):
        headers = self.headers
        parsed_uri = urlparse(url)
        protocol = parsed_uri.scheme
        host = parsed_uri.netloc        
        try:
            #headers = {'User-Agent': cls.FF_USER_AGENT}
            html = requests.get(url,headers=headers).text
            r = re.search(r'sniff\("[^"]+","([^"]+)","([^"]+)".+?],([^,]+)', html)
            if r:
                source = "https://{0}/m3u8/{1}/{2}/master.txt?s=1&cache={3}".format(
                    host, r.group(1), r.group(2), r.group(3)
                ) 
                headers.update({'Referer': url})
                return source + self.append_headers(headers)
        except:
            pass
        return ''

    def StreamWishResolver(self,url):
        headers = self.headers
        try:
            media_id = url.split('/')[4]
        except:
            media_id = ''
        if '$$' in media_id:
            media_id, referer = media_id.split('$$')
            if not referer.endswith('/'):
                referer = referer + '/'
        else:
            referer = False
        if referer:
            headers.update({'Referer': referer})
        parsed_uri = urlparse(url)
        protocol = parsed_uri.scheme
        host = parsed_uri.netloc
        rurl = 'https://%s/'%host            
        try:
            r = requests.get(url,headers=headers)
            cookies = r.cookies
            src = r.text           
            source = re.findall(r'''sources:\s*\[{file:\s*["'](?P<url>[^"']+)''', src)[-1]
            headers = {'Origin': rurl[:-1],'Referer': rurl, 'User-Agent': headers['User-Agent']}
            if cookies:
                encoded_cookies = urlencode(cookies)
                headers.update({'Cookie': encoded_cookies}) 
            return source + self.append_headers(headers)
        except:
            pass      
        return

    def resolve_youtube(self,url):
        yt= Tube(url)
        stream = yt.url
        if not stream:
            stream = Tube2().get_video(url)
        return stream
    
    def resolve_vimeo(self,url):
        headers = self.headers
        try:
            if '/video/' in url:
                media_id = url.split('/video/')[1]
            else:
                media_id = url.split('/')[-1]
            try:
                media_id = media_id.split('?')[0]
            except:
                pass
        except:
            media_id = ''
        if media_id:
            if '$$' in media_id:
                media_id, referer = media_id.split('$$')
                referer = referer + '/'
                headers.update({'Referer': referer})
            else:
                referer = False
            try:
                web_url = 'https://player.vimeo.com/video/%s/config'%media_id
                if not referer:
                    headers.update({'Referer': 'https://vimeo.com/',
                                    'Origin': 'https://vimeo.com'})
                data = requests.get(web_url,headers=headers).json()
                sources = [(vid['height'], vid['url']) for vid in data.get('request', {}).get('files', {}).get('progressive', {})]
                if sources:
                    sources.sort(key=lambda x: x[0], reverse=True)
                    return self.pick_source(sources) + self.append_headers(headers)
                else:
                    hls = data.get('request', {}).get('files', {}).get('hls')
                    if hls:
                        src = hls.get('cdns', {}).get(hls.get('default_cdn'), {}).get('url')
                        if src:
                            return src + self.append_headers(headers)
            except:
                pass
        return

    
    def resolve_pornhub(self,url):
        headers = self.headers
        parsed_uri = urlparse(url)
        protocol = parsed_uri.scheme
        host = parsed_uri.netloc
        #host = host.replace('pt.', '')      
        #host_url = 'https://www.{0}/'.format(host)
        host_url = 'https://{0}/'.format(host)
        try:
            media_id = url.split('viewkey=')[1]
            try:
                media_id = media_id.split('&')[0]
            except:
                pass
        except:
            media_id = ''
        if media_id:
            web_url = host_url + 'view_video.php?viewkey=' + media_id
            headers.update({'Referer': host_url,
                   'Cookie': 'accessAgeDisclaimerPH=1; accessAgeDisclaimerUK=1'})
            html = requests.get(web_url,headers=headers).text
            sources = []
            qvars = re.search(r'qualityItems_[^\[]+(.+?);', html)
            if qvars:
                sources = json.loads(qvars.group(1))
                sources = [(src.get('text'), src.get('url')) for src in sources if src.get('url')]
            if not sources:
                sections = re.findall(r'(var\sra[a-z0-9]+=.+?);flash', html)
                for section in sections:
                    pvars = re.findall(r'var\s(ra[a-z0-9]+)=([^;]+)', section)
                    link = re.findall(r'var\smedia_\d+=([^;]+)', section)[0]
                    link = re.sub(r"/\*.+?\*/", '', link)
                    for key, value in pvars:
                        link = re.sub(key, value, link)
                    link = link.replace('"', '').split('+')
                    link = [i.strip() for i in link]
                    link = ''.join(link)
                    if 'urlset' not in link:
                        r = re.findall(r'(\d+p)', link, re.I)
                        if r:
                            sources.append((r[0], link))
            if not sources:
                fvars = re.search(r'flashvars_\d+\s*=\s*(.+?);\s', html)
                if fvars:
                    sources = json.loads(fvars.group(1)).get('mediaDefinitions')
                    sources = [(src.get('quality'), src.get('videoUrl')) for src in sources if
                           type(src.get('quality')) is not list and src.get('videoUrl')]
            if sources:
                headers.update({'Origin': host_url[:-1]})
                stream = self.pick_source(sources)
                if 'master.m3u8' in stream:
                    stream = stream.replace('/master.m3u8', '/index-f1-v1-a1.m3u8')
                return stream + self.append_headers(headers)
        return

    def resolve_doramasonline(self,url):
        headers = self.headers
        headers.update({'Referer': 'https://doramasonline.org/'})
        stream = ''
        sub = ''
        try:
            r = requests.get(url,headers=headers)
            src = r.text
        except:
            src = ''

        try:
            sources_pattern = r'sources:\s*\[(.*?)\]'
            url_pattern = r'"file":"(.*?)"'

            sources_match = re.search(sources_pattern, src, re.DOTALL)
            if sources_match:
                sources_text = sources_match.group(1)
                sources_urls = re.findall(url_pattern, sources_text)
                stream = sources_urls[-1] + self.append_headers(headers)
        except:
            pass

        try:
            tracks_pattern = r'tracks:\s*\[(.*?)\]'
            url_pattern = r'file:\s*"(.*?)",\s*\n\s*label:\s*"Português"'

            tracks_match = re.search(tracks_pattern, src, re.DOTALL)
            if tracks_match:
                tracks_text = tracks_match.group(1)
                sub = re.findall(url_pattern, tracks_text)[-1]
        except:
            pass
        if not stream:
            try:
                j = re.findall(r'var jw = (.*?)<', src)[0]
                stream = json.loads(j).get('file', '')
                if stream:
                    stream = stream + self.append_headers(headers)
            except:
                pass
        return stream, sub
            
                            
    def resolve_csst(self,url):
        headers = self.headers
        headers.update({'Referer': 'https://doramasonline.org/'})
        stream = ''
        sub = ''
        try:
            r = requests.get(url,headers=headers, allow_redirects=True)
            src = r.text
        except:
            src = '' 

        try:
            v = re.findall(r'id:.+?subtitle: "(.*?)".+?file:"(.*?)"', src, re.DOTALL|re.MULTILINE)[-1]
            subtitle = v[0]
            if subtitle:
                try:
                    subtitle = subtitle.split(']')[1]
                except:
                    pass
                try:
                    subtitle = subtitle.split(',')[0]
                except:
                    pass
                sub = subtitle
            videos = v[1].split(',')
            stream = re.findall(r'\[(.*?)\](.+)', videos[-1])[0][1]
        except:
            pass
        return stream, sub
    #net
    def resolve_vod1(self,url):
        parsed_url = urlparse(url)
        referer = '%s://%s/'%(parsed_url.scheme,parsed_url.netloc)        
        stream = ''
        headers = self.headers
        headers.update({'Cookie': 'XCRF%3DXCRF', 'Referer': referer})
        try:
            # find player
            r = cfscraper.get(url,headers=headers)
            src = r.text
            soup = self.soup(src)
            url = soup.find('div', {'id': 'content'}).find_all('a')[0].get('href', '')
        except:
            pass        
        try:
            r = cfscraper.get(url,headers=headers)
            src = r.text
            regex_pattern = r'<source[^>]*\s+src="([^"]+)"'
            alto = []
            baixo = []
            matches = re.findall(regex_pattern, src)
            for match in matches:
                if 'ALTO' in match:
                    alto.append(match)
                if 'alto' in match:
                    alto.append(match)
                if 'BAIXO' in match:
                    baixo.append(match)
                if 'baixo' in match:
                    baixo.append(match)
            if alto:
                stream = alto[-1] + '|User-Agent=' + USER_AGENT + '&Referer=' + headers['Referer'] + '&Cookie=' + headers['Cookie']
            elif baixo:
                stream = baixo[-1] + '|User-Agent=' + USER_AGENT + '&Referer=' + headers['Referer'] + '&Cookie=' + headers['Cookie']   
        except:
            pass
        return stream        
    
    def resolve_filemoon(self,url):
        headers = self.headers
        parsed_uri = urlparse(url)
        protocol = parsed_uri.scheme
        host = parsed_uri.netloc
        #host = host.replace('pt.', '')      
        #host_url = 'https://www.{0}/'.format(host)
        host_url = 'https://{0}/'.format(host)        
        try:
            if '/e/' in url:
                media_id = url.split('/e/')[1]
            else:
                media_id = url.split('/')[-1]
            try:
                media_id = media_id.split('?')[0]
            except:
                pass
        except:
            media_id = ''
        if media_id:
            if '$$' in media_id:
                media_id, referer = media_id.split('$$')
                referer = referer + '/'
                headers.update({'Referer': referer})
            else:
                referer = False
        try:
            html = requests.get(url,headers=headers).text
            html += self.get_packed_data(html)
            r = re.search(r'var\s*postData\s*=\s*(\{.+?\})', html, re.DOTALL)
            if r:
                r = r.group(1)
                pdata = {
                'b': re.findall(r"b:\s*'([^']+)", r)[0],
                'file_code': re.findall(r"file_code:\s*'([^']+)", r)[0],
                'hash': re.findall(r"hash:\s*'([^']+)", r)[0]
                }
                headers.update({
                'Referer': url,
                'Origin': host_url[:-1],
                'X-Requested-With': 'XMLHttpRequest'
                })
                edata = requests.post(host_url + 'dl', data=pdata, headers=headers).json()[0]               
                surl = tear.tear_decode(edata.get('file'), edata.get('seed'))
                if surl:
                    headers.pop('X-Requested-With')
                    return surl + self.append_headers(headers)
            else:
                r = re.search(r'sources:\s*\[{\s*file:\s*"([^"]+)', html, re.DOTALL)
                if r:
                    headers.update({
                    'Referer': url,
                    'Origin': host_url[:-1]
                    })
                    return r.group(1) + self.append_headers(headers)
            return
        except:
            pass
        return


    def resolverurls(self,url,referer):
        stream = ''
        sub = ''
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        domain = domain.replace('www.', '').replace('ww3.', '').replace('ww4.', '')
        #streamtape
        if domain in ['streamtape.com', 'strtape.cloud', 'streamtape.net', 'streamta.pe', 'streamtape.site',
               'strcloud.link', 'strtpe.link', 'streamtape.cc', 'scloud.online', 'stape.fun',
               'streamadblockplus.com', 'shavetape.cash', 'streamtape.to', 'streamta.site',
               'streamadblocker.xyz', 'tapewithadblock.org', 'adblocktape.wiki'] or 'streamtape' in domain:
            stream = self.resolve_streamtape(url,referer) 
        elif domain in ['mixdrop.co', 'mixdrop.to', 'mixdrop.sx', 'mixdrop.bz', 'mixdrop.ch',
               'mixdrp.co', 'mixdrp.to', 'mixdrop.gl', 'mixdrop.club', 'mixdroop.bz',
               'mixdroop.co', 'mixdrop.vc', 'mixdrop.ag', 'mdy48tn97.com',
               'md3b0j6hj.com', 'mdbekjwqa.pw', 'mdfx9dc8n.net', 'mdzsmutpcvykb.net', 'mixdrop.is', 'mixdrop.nu'] or 'mixdrop' in domain:
            stream = self.resolve_mixdrop(url,referer) 
        elif domain in ['\x62\x72\x70\x6c\x61\x79\x65\x72\x2e\x73\x69\x74\x65', '\x77\x61\x74\x63\x68\x2e\x62\x72\x70\x6c\x61\x79\x65\x72\x2e\x73\x69\x74\x65']:
            stream = self.resolve_brplayer(url)
        elif domain in ['streamwish.com', 'streamwish.to', 'ajmidyad.sbs', 'khadhnayad.sbs', 'yadmalik.sbs',
               'hayaatieadhab.sbs', 'kharabnahs.sbs', 'atabkhha.sbs', 'atabknha.sbs', 'atabknhk.sbs',
               'atabknhs.sbs', 'abkrzkr.sbs', 'abkrzkz.sbs', 'wishembed.pro', 'mwish.pro', 'strmwis.xyz',
               'awish.pro', 'dwish.pro', 'vidmoviesb.xyz', 'embedwish.com', 'cilootv.store', 'uqloads.xyz',
               'tuktukcinema.store', 'doodporn.xyz', 'ankrzkz.sbs', 'volvovideo.top', 'streamwish.site',
               'wishfast.top', 'ankrznm.sbs', 'sfastwish.com', 'eghjrutf.sbs', 'eghzrutw.sbs',
               'playembed.online', 'egsyxurh.sbs', 'egtpgrvh.sbs', 'flaswish.com', 'obeywish.com',
               'cdnwish.com', 'jodwish.com', 'asnwish.com', 'gsfqzmqu.sbs'] or 'wish' in domain:
            stream = self.StreamWishResolver(url)
        elif domain in ['youtube.com']:
            stream = self.resolve_youtube(url)
        elif domain in ['vimeo.com', 'player.vimeo.com']:
            stream = self.resolve_vimeo(url)
        elif domain in ['pornhub.com', 'pt.pornhub.com']:
            stream = self.resolve_pornhub(url)
        elif '\x64\x6f\x72\x61\x6d\x61\x73\x6f\x6e\x6c\x69\x6e\x65' in domain:
            stream, sub = self.resolve_doramasonline(url)
        elif domain in ['csst.online'] or 'csst' in domain:
            stream, sub = self.resolve_csst(url)
        elif domain in ['filemoon.sx', 'filemoon.to', 'filemoon.in', 'filemoon.link', 'filemoon.nl',
               'filemoon.wf', 'cinegrab.com', 'filemoon.eu', 'filemoon.art', 'moonmov.pro',
               'kerapoxy.cc'] or 'filemoon' in domain:
            stream = self.resolve_filemoon(url)
        elif '\x6e\x65\x74\x63\x69\x6e\x65' in domain:
            stream = self.resolve_vod1(url)
        try:
            stream = stream.strip()
        except:
            pass
        return stream, sub                                    

