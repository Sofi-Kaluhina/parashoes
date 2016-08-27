__author__ = 'markel'

import os
from tornado import gen
from tornado.options import options
from random import randint


brands = '''Agnès b.
Badgley Mischka
Balenciaga
Bally Shoe
Balmain (fashion house)
Neil Barrett (fashion designer)
Belle & Bunty
Bellville Sassoon
Benson & Clegg
Berluti
Beulah London
Dirk Bikkembergs
Bill Blass Group
Manolo Blahnik
Ozwald Boateng
BodyMap
Boglioli
Bonia (fashion)
Bontoni
Borsalino
Hugo Boss
Bottega Veneta
PORNHUB'''

brands_description = '''Agnès had mixed twins at 19 and she separated from their father Christian Bourgois at 20. She graduated from École du Louvre in Paris. A career soon followed when her personal style caught the eyes of Elle magazine staffers at a Paris flea market.
James Mischka began at Rice University as a biomedical engineering major and ultimately graduated with degrees in art history and managerial studies in 1985. Badgley and Mischka met at Parsons School of Design in Manhattan. The two launched the label Badgley Mischka in 1988, though their bridal business launched in 1993.
Bally was founded by Carl Franz Bally. His original family business was the manufacture of elastic ribbon.
Balmain (French: [balmɛ̃]) is a haute couture fashion house that was founded by Pierre Balmain. Balmain was born in 1914 in France. His father owned a drapery business and his mother and sister owned a fashion boutique where he often worked after his father’s death in 1921.
Neil Barrett was born in Devon, South West England. Both his grandfather and great-grandfather were master tailors.
Bellville Sassoon is a high end British fashion salon originally based on Pavilion Road, Knightsbridge, London, now located at 18 Culford Gardens in Chelsea.
Benson & Clegg is a British firm of bespoke tailors in London's Jermyn Street, founded in 1937.
Berluti is a subsidiary brand of LVMH that manufactures and retails menswear.
Beulah London is a luxury fashion founded, in 2011, by English aristocrat Lady Natasha Rufus Isaacs and fashion designer Lavinia Brennan.
Dirk Bikkembergs (born January 2, 1959) is a Belgian fashion designer.
Bill Blass Group replaces what was formerly Bill Blass Limited, a fashion house founded by American designer Bill Blass. Chris Benz is the Creative Director of the group.
Blahnik was born and raised in Santa Cruz de la Palma, in the Canary Islands (Spain).
Boateng, whose parents emigrated from Ghana in the 1950s, was born in 1967 in Muswell Hill, North London.
BodyMap (also sometimes written as Bodymap or Body Map) was an influential British fashion label of the 1980s
Boglioli is a men's tailoring family business originally based in the Italian town of Gambara.
Bonia Group is an international luxury fashion retailer based in Malaysia which has more than 700 sales outlets and 70 boutiques across Asia.
Bontoni is a third-generation Italian family company that produces a very exclusive line of bespoke and ready-made men's dress shoes.
Borsalino is a hat company known particularly for its fedoras.
Hugo Boss AG, often styled as BOSS, is a German luxury fashion house.
Bottega Veneta is an Italian luxury goods house best known for its leather goods which are sold worldwide.
Bla bla bla
Bla bla
PornHub account'''

clothing = '''Aba
Acrilan fabric
Acrylic fiber
Aertex
Airdura
Airguard
Alençon lace
Angora
Antique satin
Argentan lace
Argentella lace
Armenian needlelace
Baize
Ballistic nylon
Bamboo
Ban-Lon
Barathea
Barkcloth
Batik
Batiste
Battenberg lace
Bedford cord
Benaras
Bengaline silk
Beta cloth
Bird's-Eye Weave
Bobbinet
Boiled wool
Bombazine
Bouclé
Braid
Brilliantine
Broadcloth
Brocade
Broderie Anglaise
Buckram
Bunting
Burano lace
Buratto lace
Burlap
C change
Calico
Cambric
Camel's hair
Camlet
Canvas
Capilene
Carbon fiber
Carrickmacross lace
Casement
Cashmere
Cavalry twill
Cedar bark
Challis
Chambray
Chantilly lace
Char cloth
Charmeuse
Charvet
Cheesecloth
Chenille
Chiengora
Chiffon
Chino
Chintz
Cloqué
Cloth of gold
Conductive
Coolmax
Coir
Cordura
Corduroy
Cotton duck
Coutel
Crape
Crêpe-back satin
Crêpe de Chine
Cretonne
Crimplene
Crinoline
Crochet
Cotton
Damask
Darlexx
Dazzle
Delaine wool
Denim
Dimity
Dobby
Doeskin
Donegal tweed
Dotted Swiss
Double cloth
Double knitting
Double weave
Dowlas
Drill
Drugget
Duck
Dupioni silk
Dungarees
Dyneema
Eyelet
Egyptian cotton
E-textiles
Faille
Faux fur
Felt
Filet/Lacis lace
Fishnet
Flannel
Flannelette
Fleece
Foulard
Fustian
Gabardine
Gannex
Gauze
Gazar
Georgette
Ghalamkar
Gingham
Gore-Tex
Grenadine
Grenfell Cloth
Grosgrain
Habutai
Halas lace
Haircloth
Harris Tweed
Heather knit
Hemp
Herringbone
Himroo
Hodden
Holland cloth
Hollie Point lace
Hopsack
Houndstooth check
Indian cotton
Intarsia
Interlock
Irish linen
Jacquard
Jacquard knit
Jamdani
Jersey
Jute
Jaconet
Kemp
Kenmare Lace
Kerseymere
Kevlar
Khādī
Khaki
Khaki drill
Kente cloth
Kincob
Knit
Lace
Lambswool
Lamé
Lampas
Lantana
Lanon
Lawn cloth
Lazzer
Leather
Leatherette
Leno
Limerick lace
Linen
Linsey-woolsey
Loden
Longcloth
Loop knit
Lumalive
Lycra knit
Machine knitting
Mackinaw
Madapolam
Madras
Malimo
Marquisette
Matelassé
Melton
Merino
Mesh
Microfibre
Milliskin
Mockado
Mohair
Moire
Moleskin
Monk's cloth
Moquette
Mouflon
Mousseline
Muslin
Natural fiber
Neoprene
Nomex
Nylon
Oilskin
Organdy
Organza
Osnaburg
Ottoman
Oxford
Omran
Paduasoy
Paisley
Panné velvet
Peau de Soie
Percale
Piqué
Plissé
Plush
Point de France lace
Point de Gaze lace
Point de Venise lace
Pointelle
Polar fleece
Pongee
Poplin
Punto in Aria lace
Polyester
Qiviut
Quilting
Raschel knit
Rakematiz
Rayadillo
Rayon
Raw silk
Rep
Reticella lace
Ribbon lace
Rib knit
Rib weave
Rinzu
Ripstop
Ripstop nylon
Russell cord
Saga Nishiki
Sailcloth
Samite
Sateen
Satin
Saye
Scarlet
Scrim
Seersucker
Sequin
Serge
Shantung
Sharkskin
Shot silk
Silk
Silk Noil
Silnylon
Smartwool
Songket
Spandex
Stockinette
Stub-tex
Stuff
Suede
Surah
SympaTex
Taffeta
Tais
Tammana
Tambour lace
Tapestry
Tartan
Teneriffe lace
Terrycloth
Terry velour
Ticking
Toile
Tricot knit
Tulle netting
Tussar silk
Tweed
Twill
terrywool
terrycotton
terrysilk
Ultrasuede
Velour
Velours du Kasaï
Velvet
Velveteen
Venetian Lace
Venetian Wool
Ventile
Vinyl coated polyester
Viyella
Voile
Vintage
Wadmal
Whipcord
Wigan
Windstopper
Worcester
Worsted wool
Wool
Youghal lace
Yarn
Zephyr
Zibeline
Zorbeez'''

@gen.coroutine
def get_random_products(full=True):
	result = []
	if full:
		for i, img in enumerate(os.listdir(options.media_dir + '/product/')):
			result.append({
				'id': i,
				'name': brands.split('\n')[i],
				'description': brands_description.split('\n')[i],
				'price': randint(150, 500),
				'material': clothing.split('\n')[randint(0, len(clothing.split('\n'))-1)],
				'photo': 'http://bulavka:8080/media/product/' + img
			})
	else:
		for i, img in enumerate(os.listdir(options.media_dir + '/product/')):
			result.append({
				'id': i,
				'name': brands.split('\n')[i],
				'price': randint(150, 500),
				'photo': 'http://bulavka:8080/media/product/' + img
			})
	return result

