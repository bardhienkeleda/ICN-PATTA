KEYWORDS_NUMBER = 100
MAX_WEBPAGES = 40
MIN_WEBPAGES = 10
NUMBER_FEATURES = 900
GRAMS = (1, 1)
PLOT_CON = True

webpages_list = [ 'www.baidu.com', 'apache.org', 'web.mit.edu',
    'www.gnu.org','www.washington.edu', 'www.tripod.lycos.com', 'www.tapad.com',
    'gohoi.com', 'www.ox.ac.uk', 'sigonews.com',
    'itfactly.com', 'www.nyu.edu','www.bizrate.com', 'www.ufl.edu',
    'www.chinanews.com', 'www.bu.edu', 'alternativenation.net', 'www.rai.it',
    'www.treccani.it', 'www.palermotoday.it','www.italia.it', 'tamilyogi.cool',
    'www.governo.it','www.spettacolovivo.it','www.salute.gov.it', 'www.mapei.com',
    'www.tusciaweb.eu','senato.it', 'www.lse.ac.uk', 'www.leeds.ac.uk', 'www.imperial.ac.uk', 'www.open.ac.uk', 'www.exeter.ac.uk',
    'www.reading.ac.uk', 'uea.ac.uk','www.irishnews.com', 'www.kit.edu',
    'asianews.it', 'icio.us', 'imageshack.us', 'www.wikidot.com']
    
min_webpage_list = ['apache.org', 'web.mit.edu', 'asianews.it',
'www.gnu.org','www.chinanews.com',
'imageshack.us','www.italia.it','www.kit.edu',
'www.imperial.ac.uk','icio.us']
#,'sigonews.com', 'www.mapei.com','www.wikidot.com', 'www.tusciaweb.eu', 'senato.it',
#'www.washington.edu', 'www.tripod.lycos.com', 'www.governo.it','www.spettacolovivo.it', 'www.reading.ac.uk']

urls = ['http://baidu.com/', 'http://apache.org', 'http://web.mit.edu', 'http://www.gnu.org', 'http://www.washington.edu',      'http://www.tripod.lycos.com', 'http://www.tapad.com', 'http://gohoi.com/', 'http://www.ox.ac.uk','http://sigonews.com',
'http://itfactly.com', 'http://www.nyu.edu', 'http://www.bizrate.com', 'http://imageshack.us', 'http://www.chinanews.com',
'http://www.ufl.edu', 'http://icio.us', 'http://www.bu.edu', 'http://www.wikidot.com', 'http://alternativenation.net',
'http://www.rai.it', 'http://www.treccani.it', 'http://www.palermotoday.it', 'http://www.italia.it/en/home.html',
'http://tamilyogi.cool', 'http://www.governo.it', 'http://www.salute.gov.it/portale/home.html',
'http://www.spettacolovivo.it', 'http://asianews.it', 'http://www.mapei.com', 'http://www.tusciaweb.eu',
'http://senato.it/home', 'http://www.lse.ac.uk', 'http://www.exeter.ac.uk',
'http://www.leeds.ac.uk', 'http://www.imperial.ac.uk', 'http://www.open.ac.uk', 'http://www.reading.ac.uk',
'http://uea.ac.uk', 'http://www.irishnews.com', 'http://www.kit.edu']


domains = ['baidu', 'apache', 'mit', 'gnu','washington',  'lycos', 'tapad', 'gohoi', 'ox', 'sigonews', 'itfactly',  'nyu', 'bizrate','imageshack', 'chinanews', 'ufl','icio',  'bu', 'wikidot',
   'alternativenation', 'rai', 'treccani',
   'italia', 'tamilyogi', 'governo','spettacolovivo', 'asianews', 'mapei',
   'salute', 'tusciaweb', 'senato', 'lse',
   'leeds', 'imperial','open', 'exeter', 'reading', 'uea',
   'irishnews', 'kit']
   
min_domains = ['apache', 'asianews', 'mit', 'gnu','chinanews', 'imageshack','italia',
'kit', 'imperial', 'icio']
#, 'sigonews', 'mapei', 'wikidot', 'tusciaweb', 'senato', 'washington', 'lycos', 'governo', 'spettacolovivo', 'reading']
