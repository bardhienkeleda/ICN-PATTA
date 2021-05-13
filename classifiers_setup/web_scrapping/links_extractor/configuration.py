MAX_DEPTH = 12  # maximum click depth
MIN_DEPTH = 2 # minimum click depth
MAX_WAIT = 10  # maximum amount of time to wait between HTTP requests
MIN_WAIT = 5  # minimum amount of time allowed between HTTP requests
DEBUG = True  # set to True to enable useful console output

# use this single item list to test how a site responds to this crawler
# be sure to comment out the list below it.
#ROOT_URLS = ["https:///digg.com/"]

#HOME_URLS = ["http://apache.org","http://web.mit.edu","http://www.gnu.org", "http://www.washington.edu"]
#urls = ['http://www.spettacolovivo.it']

urls = ['http://baidu.com/', 'http://apache.org', 'http://web.mit.edu', 'http://www.gnu.org', 'http://www.washington.edu',      'http://www.tripod.lycos.com', 'http://www.tapad.com', 'http://gohoi.com/', 'http://www.ox.ac.uk','http://sigonews.com',
'http://itfactly.com', 'http://www.nyu.edu', 'http://www.bizrate.com', 'http://imageshack.us', 'http://www.chinanews.com',
'http://www.ufl.edu', 'http://icio.us', 'http://www.bu.edu', 'http://www.wikidot.com', 'http://alternativenation.net',
'http://www.rai.it', 'http://www.treccani.it', 'http://www.palermotoday.it', 'http://www.italia.it/en/home.html',
'http://tamilyogi.cool', 'http://www.governo.it', 'http://www.salute.gov.it/portale/home.html',
'http://www.spettacolovivo.it', 'http://asianews.it', 'http://www.mapei.com', 'http://www.tusciaweb.eu',
'http://senato.it/home', 'http://www.lse.ac.uk', 'http://www.exeter.ac.uk',
'http://www.leeds.ac.uk', 'http://www.imperial.ac.uk', 'http://www.open.ac.uk', 'http://www.reading.ac.uk',
'http://uea.ac.uk', 'http://www.irishnews.com', 'http://www.kit.edu']

# must use a valid user agent or sites will hate you
USER_AGENT = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_3) ' \
'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'

domains = ['baidu', 'apache', 'mit', 'gnu','washington',  'lycos', 'tapad', 'gohoi', 'ox', 'sigonews', 'itfactly',  'nyu', 'bizrate','imageshack', 'chinanews', 'ufl','icio',  'bu', 'wikidot',
   'alternativenation', 'rai', 'treccani', 'palermotoday',
   'italia', 'tamilyogi', 'governo','spettacolovivo', 'asianews', 'mapei',
   'salute', 'tusciaweb', 'senato', 'lse',
   'leeds', 'imperial','open', 'exeter', 'reading', 'uea',
   'irishnews', 'kit']
