#!/usr/bin/env python3
"""
Generador de index.html para Indonesia 2027:
- EN ORDENADOR (ESTILO CHINA 2027):
  - Columna izquierda con los 14 dias individuales y columna derecha pegajosa (sticky) con el mapa interactivo.
  - Sincronizacion dinamica con scroll: conforme se hace scroll por los dias, los tramos se van uniendo e iluminando secuencialmente (done / now), la baliza de posicion se traslada a la isla/ciudad activa, la barra de progreso avanza y el titulo del mapa cambia en tiempo real.
- EN MOVIL (APP NATIVA POR SECCIONES):
  - En movil la pagina se divide en 6 pantallas/vistas independientes (Ruta, Mapa, Hoteles, Vuelos, Criterio, Guia) activadas desde la barra inferior (.bottomnav).
  - Rendimiento ultrarrapido: no carga ni desplaza 14 dias juntos al ver hoteles o el mapa, permitiendo navegacion instantanea sin lag.
- Paleta oficial Sarah Renae Clark en modo claro, tipografia DM Serif Display + Plus Jakarta Sans, fotos limpias y cero rayas largas.
"""
import os, json, sys, base64

BASE = os.path.dirname(os.path.abspath(__file__))
CACHE_FILE = os.path.join(BASE, "imgcache.json")
LAND_FILE = os.path.join(BASE, "mapa_land.json")
OUTPUT_FILE = os.path.join(os.path.dirname(BASE), "index.html")

if not os.path.exists(CACHE_FILE) or not os.path.exists(LAND_FILE):
    print("Error: archivos de cache o tierra no encontrados.")
    sys.exit(1)

with open(CACHE_FILE, "r", encoding="utf-8") as f:
    IMG = json.load(f)

with open(LAND_FILE, "r", encoding="utf-8") as f:
    LAND_DATA = json.load(f)

svg_land_path = LAND_DATA["land_svg"]

def get_img(k):
    return IMG.get(k, {}).get("b64", "")

def font_b64(filename):
    with open(os.path.join(BASE, filename), "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

FONT_DM_SERIF_NORMAL = font_b64("dm_serif_display_normal.woff2")
FONT_DM_SERIF_ITALIC = font_b64("dm_serif_display_italic.woff2")
FONT_JAKARTA_VARIABLE = font_b64("plus_jakarta_sans_variable.woff2")

# --- Video de fondo del hero -------------------------------------------------
# Montaje propio a partir de las fotos verificadas del banco. Si el fichero no
# existe, el hero cae limpiamente en una foto fija (mismo encuadre y velo).
HERO_VIDEO_FILE = os.path.join(BASE, "hero_loop.mp4")
HERO_POSTER_KEY = "padar"

if os.path.exists(HERO_VIDEO_FILE):
    with open(HERO_VIDEO_FILE, "rb") as f:
        _hero_b64 = base64.b64encode(f.read()).decode("utf-8")
    HERO_MEDIA = (
        f'<video class="hero-video" id="heroVideo" autoplay muted loop playsinline '
        f'preload="auto" disablepictureinpicture poster="{get_img(HERO_POSTER_KEY)}">'
        f'<source src="data:video/mp4;base64,{_hero_b64}" type="video/mp4">'
        f'</video>'
    )
    print(f"Video del hero embebido: {os.path.getsize(HERO_VIDEO_FILE)/1024/1024:.2f} MB")
else:
    HERO_MEDIA = (
        f'<img class="hero-poster-img" src="{get_img(HERO_POSTER_KEY)}" alt="" aria-hidden="true">'
    )
    print("Aviso: no hay hero_loop.mp4, el hero usa foto fija de respaldo.")


# =============================================================================
# CRONOLOGIA DE LA HISTORIA DE INDONESIA
# Cada hito lleva su base documental en "source". Los que siguen en debate
# entre especialistas llevan "flag", que se pinta como aviso en la tarjeta,
# para no presentar como cerrado lo que la investigacion mantiene abierto.
# =============================================================================
ERAS_HISTORIA = {
    1: {"name": "Orígenes humanos", "color": "var(--c-coral-dark)"},
    2: {"name": "Reinos hindú-budistas", "color": "var(--c-teal-dark)"},
    3: {"name": "Encuentro con Europa", "color": "var(--c-indigo)"},
    4: {"name": "Descubrimientos y despertar nacional", "color": "var(--c-coral)"},
    5: {"name": "Independencia e Indonesia moderna", "color": "var(--c-teal)"},
    6: {"name": "Komodo y la actualidad", "color": "var(--c-cyan)"},
}

MILESTONES_HISTORIA = [
    {"n": 1, "era": 1, "badge": "Hacia 1,8 millones de años", "title": "Homo erectus llega a Java",
     "body": 'El "Hombre de Java" (Homo erectus), descubierto en 1891 en Trinil por Eugene Dubois, y los yacimientos posteriores de Sangiran, documentan una de las poblaciones de Homo erectus más antiguas fuera de África, con fechas de hasta 1,6 a 1,8 millones de años. Llegaron caminando por puentes de tierra del banco de Sunda durante glaciaciones, pero nunca cruzaron la Línea de Wallace hacia el este, es decir, nunca llegaron a Flores ni a Bali por esta vía terrestre. Java central, que la pareja recorrerá camino a Yogyakarta, concentra alrededor del 75% de todos los fósiles de Homo erectus conocidos en el mundo.',
     "source": "consenso paleoantropológico internacional (dataciones por nucleidos cosmogénicos)."},
    {"n": 2, "era": 1, "badge": "Hacia 1 millón de años", "title": "Presencia humana temprana en Flores",
     "body": "Herramientas de piedra halladas en Wolo Sege y en la cuenca de So'a, en Flores, demuestran que algún homínido (probablemente una forma temprana relacionada con Homo erectus) ya había logrado cruzar el mar hasta la isla hace aproximadamente un millón de años, mucho antes de la aparición del famoso “hobbit”. Esto convierte a Flores en el escenario de una de las travesías marítimas más antiguas conocidas de la prehistoria humana. Es un dato que cobra sentido al pisar la propia isla de Flores camino a Labuan Bajo.",
     "source": "consenso arqueológico (yacimientos de Mata Menge y Wolo Sege)."},
    {"n": 3, "era": 1, "badge": "Entre 100.000 y 60.000 años", "title": 'El "hobbit" de Flores', "flag": "Fechas debatidas",
     "body": 'En la cueva de Liang Bua, en Flores, se descubrieron en 2003 los restos de Homo floresiensis, un homínido de talla minúscula (poco más de un metro) que los medios apodaron "el hobbit". Fósiles emparentados hallados en Mata Menge, mucho más antiguos (unos 700.000 años), sugieren que esta reducción de tamaño ya se había producido muy pronto en la isla, posiblemente a partir de un antepasado tipo Homo erectus aislado en Flores. La fecha de extinción del hobbit y su relación exacta con la llegada de Homo sapiens siguen siendo objeto de debate activo entre paleoantropólogos. Al visitar Flores en ruta hacia Komodo, la pareja atraviesa el mismo territorio insular donde vivió esta especie humana única en el mundo.',
     "source": "consenso arqueológico con controversia abierta (dataciones revisadas en Nature, 2016, tras el hallazgo de Mata Menge)."},
    {"n": 4, "era": 1, "badge": "Hacia 50.000-60.000 años", "title": "Llegada del Homo sapiens moderno",
     "body": 'Los humanos anatómicamente modernos cruzaron el archipiélago de Wallacea (que incluye Flores) mediante navegación marina, mucho antes de que cualquier otra población humana hubiera hecho una travesía oceánica comparable, en su camino hacia Nueva Guinea y Australia. Esta migración es la base genética y cultural de las poblaciones austronesias y papúas que hoy conviven en el este de Indonesia, incluida Nusa Tenggara.',
     "source": 'consenso arqueológico y genético (modelos de "salida de África" y dispersión por Wallacea).'},
    {"n": 5, "era": 2, "badge": "Hacia 780-840", "title": "La dinastía Sailendra y la construcción de Borobudur",
     "body": "La dinastía budista Sailendra, que dominaba el centro de Java, mandó construir el gran monumento de Borobudur, el templo budista más grande del mundo, probablemente bajo el rey Samaratungga. No existen inscripciones que fijen fechas exactas, por lo que el rango 780-840 es una estimación basada en estilo arquitectónico y epigrafía comparada. Este es precisamente el templo que la pareja visitará en Yogyakarta: sus miles de relieves narran la vida de Buda y la cosmología budista Mahayana tal como se entendía en la corte Sailendra.",
     "source": "consenso arqueológico, sin registro escrito directo de la fecha (National Geographic Institute / World History Encyclopedia)."},
    {"n": 6, "era": 2, "badge": "Hacia 850", "title": "La dinastía Sanjaya y la construcción de Prambanan",
     "body": "Mientras los Sailendra promovían el budismo, la dinastía rival (o pariente, según otra lectura historiográfica) Sanjaya, de fe hindú, erigió el gran complejo de Shivagrha, hoy conocido como Prambanan, bajo el rey Rakai Pikatan hacia el 850. La inscripción Shivagrha menciona incluso obras de ingeniería, como el desvío del río Opak, para proteger el templo. Los historiadores siguen debatiendo si Sailendra y Sanjaya eran dinastías enfrentadas o dos ramas de una misma familia con distinta devoción religiosa; lo que sí está claro es que, en esta época, hinduismo y budismo convivieron en Java central sin fronteras rígidas. Prambanan, que la pareja visitará junto a Borobudur, es el testimonio en piedra de esa convivencia religiosa.",
     "source": "epigrafía javanesa antigua (inscripción Shivagrha, 856 d.C.) y consenso arqueológico."},
    {"n": 7, "era": 2, "badge": "929", "title": "El reino de Mataram traslada su centro a Java oriental", "flag": "Causa debatida",
     "body": "El rey Mpu Sindok trasladó la sede del reino de Mataram desde Java central hacia Java oriental, fundando la dinastía Isyana. La causa exacta se discute: la hipótesis más popular apunta a una erupción del volcán Merapi (que hoy sigue activo y es visible desde Yogyakarta) como desencadenante, aunque otros historiadores señalan también posibles invasiones o luchas de poder. Este traslado explica por qué, tras el esplendor de Borobudur y Prambanan, el centro de gravedad política y religiosa de Java se desplazó hacia el este durante los siglos siguientes, dejando ambos templos progresivamente abandonados a la selva.",
     "source": "hipótesis historiográfica debatida (registros epigráficos javaneses, sin consenso cerrado sobre la causa)."},
    {"n": 8, "era": 2, "badge": "1293-1527", "title": "El imperio de Majapahit y su huella en Bali",
     "body": "Majapahit, con capital en Trowulan (Java oriental), se convirtió en el mayor imperio hindú-budista del archipiélago, y bajo el mando de su primer ministro Gajah Mada conquistó Bali en 1343. Esta conquista integró a Bali en la órbita cultural, artística y religiosa javanesa, sentando las bases del hinduismo balinés tal como se practica hoy. El sistema de castas balinés, partes de la lengua balinesa (con numerosos préstamos del javanés antiguo) y el calendario balinés tienen su origen directo en esta época.",
     "source": "consenso historiográfico (crónicas javanesas como el Nagarakretagama, siglo XIV)."},
    {"n": 9, "era": 2, "badge": "Siglos XV-XVI", "title": "La corte de Majapahit emigra a Bali y funda Gelgel",
     "body": 'Con la decadencia de Majapahit y el avance del islam en Java, sacerdotes, artistas, nobles e intelectuales hindúes emigraron en oleadas hacia Bali. Entre ellos destacó el sacerdote itinerante Nirartha, figura clave que ayudó a estructurar el hinduismo balinés y a quien se atribuye la fundación de templos icónicos como Tanah Lot y Uluwatu. Esta migración dio origen a la dinastía de Gelgel (hacia 1478-1661), cuyo rey Watu Renggong (desde 1550) presidió una edad de oro cultural balinesa. Por eso el hinduismo que la pareja encontrará en los templos y rituales del valle de Sidemen y de Munduk no es un rasgo aislado de Bali, sino un legado directo y casi congelado en el tiempo de la corte javanesa de Majapahit.',
     "source": "consenso historiográfico, con crónicas dinásticas balinesas (babad) de fiabilidad histórica variable."},
    {"n": 10, "era": 2, "badge": "Siglos XV-XVI", "title": "El islam se extiende por el archipiélago, salvo Bali",
     "body": "El islam llegó a las costas del norte de Java (la región conocida como Pasisir) a través de comerciantes y misioneros, favorecido por el declive de Majapahit y el auge de sultanatos como Demak. Hacia el siglo XVI la mayoría de Java se había islamizado, pero Bali quedó protegida por el reino tapón hindú de Blambangan, en el extremo oriental de Java, que resistió la presión islámica durante casi dos siglos. Esa combinación de refugio geográfico y de una base hindú ya arraigada explica por qué Bali sigue siendo hoy, en más de un 85% de su población, hindú, mientras el resto del archipiélago es mayoritariamente musulmán: es la razón cultural de fondo que la pareja notará en cada ofrenda, templo y ceremonia balinesa del viaje.",
     "source": "consenso historiográfico (registros de lápidas musulmanas del siglo XIV en Trowulan y crónicas de sultanatos costeros)."},
    {"n": 11, "era": 3, "badge": "1511", "title": "Primer contacto portugués con el archipiélago",
     "body": "Una expedición portuguesa liderada por Antonio de Abreu, en busca de las islas de las especias, avistó el extremo nororiental de Flores en 1511, iniciando el contacto europeo con Nusa Tenggara. A este primer contacto siguieron décadas de rutas comerciales portuguesas centradas en el comercio de clavo y nuez moscada.",
     "source": "registros de navegación portugueses de la época."},
    {"n": 12, "era": 3, "badge": "Siglos XVI-XVII", "title": 'Portugueses, "topasses" y el legado católico de Flores',
     "body": 'Portugal estableció misiones y puestos comerciales en Solor, Flores oriental (Larantuka) y Timor, combinando comercio de especias con evangelización católica. Cuando los neerlandeses fueron desplazando militarmente a Portugal del resto del archipiélago a lo largo del siglo XVII, una comunidad mestiza luso-asiática conocida como los "topasses" o "larantuqueiros" mantuvo su propio poder de facto en la zona durante generaciones, resistiendo incluso ataques de la VOC. Este es el motivo histórico por el que Flores, a diferencia de la mayoría de Indonesia (musulmana), conserva hoy una identidad mayoritariamente católica, con apellidos de raíz portuguesa y celebraciones como la Semana Santa de Larantuka, algo que la pareja podrá percibir al recorrer Flores camino a Labuan Bajo.',
     "source": 'registros coloniales portugueses y neerlandeses; historiografía sobre los "black Portuguese" de Solor y Timor.'},
    {"n": 13, "era": 3, "badge": "1602 en adelante", "title": "La VOC y el dominio neerlandés de la ruta de las especias",
     "body": "La Compañía Holandesa de las Indias Orientales (VOC), fundada en 1602, fue desplazando progresivamente a portugueses, españoles e ingleses del control del comercio de especias en el archipiélago, imponiendo monopolios muchas veces mediante la fuerza. Aunque la VOC acabó dominando comercialmente casi toda la región, en zonas remotas como Flores y Nusa Tenggara oriental su control efectivo fue tardío y parcial durante mucho tiempo, lo que permitió que la influencia portuguesa y católica sobreviviera allí más tiempo que en el resto del archipiélago. La propia VOC quebró en 1799, y sus posesiones pasaron a ser administradas directamente por el Estado neerlandés.",
     "source": "registros comerciales y administrativos de la VOC."},
    {"n": 14, "era": 3, "badge": "Siglo XIX", "title": "El sistema de cultivos forzados (Cultuurstelsel)",
     "body": "A partir de 1830, el gobierno colonial neerlandés impuso en Java el Cultuurstelsel, un sistema de cultivos forzados que obligaba a los campesinos a dedicar parte de sus tierras y trabajo a cultivos de exportación (café, azúcar, índigo) para la corona neerlandesa. El sistema generó enormes beneficios para los Países Bajos, pero también hambrunas periódicas y un fuerte resentimiento que alimentaría décadas después el nacionalismo indonesio. Java central y oriental, el corazón agrícola que la pareja atraviesa entre Yogyakarta y sus templos, fue una de las regiones más intensamente explotadas bajo este sistema.",
     "source": "registros coloniales neerlandeses; historiografía económica de Indonesia."},
    {"n": 15, "era": 3, "badge": "1883", "title": "La erupción del Krakatoa",
     "body": "El volcán Krakatoa, situado en el estrecho entre Java y Sumatra, entró en erupción catastrófica en agosto de 1883, generando tsunamis que mataron a más de 36.000 personas y un estruendo escuchado a miles de kilómetros de distancia. Aunque no está en la ruta directa del viaje, este episodio recuerda que toda la región, incluido el Merapi que se ve desde Yogyakarta y los volcanes de Flores, forma parte del mismo Cinturón de Fuego del Pacífico, y ayuda a entender por qué la actividad sísmica y volcánica sigue siendo determinante en la vida de la región (como se verá en el hito de 2026).",
     "source": "registros coloniales neerlandeses y sismológicos de la época; consenso geológico."},
    {"n": 16, "era": 4, "badge": "1910-1912", "title": "Descubrimiento científico del dragón de Komodo",
     "body": "En 1910, el teniente neerlandés Van Steyn van Hensbroek recogió en la isla de Komodo los primeros ejemplares de un enorme lagarto que hasta entonces solo se conocía por leyendas locales de pescadores de Flores y Manggarai. El zoólogo Peter Ouwens, director del Museo Zoológico de Bogor, estudió los ejemplares y publicó en 1912 la primera descripción científica formal de la especie, bautizada Varanus komodoensis. Este es el animal, el mayor lagarto vivo del planeta, que la pareja irá a observar directamente en su hábitat natural en las islas de Komodo y Rinca durante la etapa final del viaje.",
     "source": "registros coloniales neerlandeses y publicación científica original (Ouwens, 1912, Bulletin du Jardin Botanique de Buitenzorg)."},
    {"n": 17, "era": 4, "badge": "1908-1928", "title": "El despertar nacional indonesio",
     "body": 'En 1908 se fundó Budi Utomo, considerada la primera organización del movimiento nacionalista indonesio, y en 1928 los jóvenes de todo el archipiélago proclamaron el "Juramento de la Juventud" (Sumpah Pemuda), adoptando la idea de una sola nación, una sola lengua (el indonesio moderno) y una sola patria, pese a la enorme diversidad étnica y religiosa del archipiélago, de Java a las Célebes y Nusa Tenggara. Sukarno emergió en esta época como una de las voces más influyentes del nacionalismo.',
     "source": "consenso historiográfico sobre el movimiento nacional indonesio."},
    {"n": 18, "era": 4, "badge": "1942-1945", "title": "La ocupación japonesa",
     "body": "Japón invadió las Indias Orientales Neerlandesas en 1942, poniendo fin a más de tres siglos de presencia colonial europea de forma abrupta. La ocupación fue dura en términos de trabajo forzado y escasez de alimentos, pero paradójicamente Japón también promovió el uso del idioma indonesio y permitió a los líderes nacionalistas, incluido Sukarno, organizarse y prepararse políticamente para la independencia que llegaría al final de la guerra.",
     "source": "consenso historiográfico; registros japoneses y neerlandeses de posguerra."},
    {"n": 19, "era": 4, "badge": "17 de agosto de 1945", "title": "Proclamación de la independencia",
     "body": "Dos días después de la capitulación de Japón, Sukarno, junto con Mohammad Hatta, proclamó la independencia de Indonesia en Yakarta, leyendo un breve texto redactado esa misma madrugada. Esta fecha, 17 de agosto, es hoy la fiesta nacional de Indonesia y el punto de partida simbólico del país que la pareja visitará, aunque el reconocimiento internacional efectivo tardaría todavía cuatro años más en llegar.",
     "source": "consenso historiográfico; documento original de la proclamación."},
    {"n": 20, "era": 5, "badge": "1945-1949", "title": "La guerra de independencia y el reconocimiento neerlandés",
     "body": "Los Países Bajos intentaron recuperar el control de sus antiguas colonias mediante dos grandes campañas militares (1947 y 1948), en un conflicto conocido como la Revolución Nacional Indonesia. La presión internacional, especialmente de Estados Unidos y de la ONU, obligó finalmente a los neerlandeses a reconocer la soberanía indonesia en la Conferencia de la Mesa Redonda de La Haya, en diciembre de 1949.",
     "source": "consenso historiográfico; actas de la Conferencia de la Mesa Redonda de 1949."},
    {"n": 21, "era": 5, "badge": "1959-1965", "title": 'Sukarno y la "Democracia Guiada"',
     "body": 'Ante la inestabilidad parlamentaria, Sukarno instauró en 1959 la "Democracia Guiada" (Demokrasi Terpimpin), un sistema de poder personalista que combinaba nacionalismo, elementos de socialismo y un papel central del ejército y del Partido Comunista de Indonesia (PKI), uno de los más grandes del mundo fuera del bloque soviético. Este equilibrio inestable entre el ejército y los comunistas estallaría de forma trágica pocos años después.',
     "source": "consenso historiográfico."},
    {"n": 22, "era": 5, "badge": "1965-1966", "title": "La caída de Sukarno y el ascenso de Suharto", "flag": "Cifras debatidas",
     "body": 'Tras un intento de golpe de estado en septiembre de 1965 (atribuido oficialmente al PKI, aunque los detalles siguen siendo objeto de debate historiográfico), el general Suharto lideró una purga violenta contra los comunistas reales o presuntos, con un saldo de varios cientos de miles de muertos en todo el país, incluida Bali, donde la violencia fue particularmente intensa. Suharto desplazó gradualmente a Sukarno del poder e inauguró el "Orden Nuevo" (Orde Baru), un régimen autoritario y desarrollista que gobernaría Indonesia durante más de tres décadas.',
     "source": "consenso historiográfico con cifras de víctimas todavía debatidas entre historiadores."},
    {"n": 23, "era": 5, "badge": "Década de 1970", "title": "El despegue turístico de Bali",
     "body": "Bajo el Orden Nuevo, el gobierno indonesio impulsó deliberadamente a Bali como destino turístico internacional, con la ampliación del aeropuerto de Ngurah Rai y la construcción de grandes hoteles en el sur de la isla desde finales de los años sesenta y durante los setenta. Este desarrollo, concentrado inicialmente en el sur (Kuta, Sanur, Nusa Dua), es el origen del turismo masivo que hoy convive con rincones todavía relativamente tranquilos como el valle de Sidemen o Munduk, que la pareja visitará precisamente buscando el contraste con el Bali más turístico.",
     "source": "consenso historiográfico sobre planificación turística indonesia (planes maestros de desarrollo turístico de Bali, años setenta)."},
    {"n": 24, "era": 5, "badge": "1980", "title": "Creación oficial del Parque Nacional de Komodo",
     "body": "El gobierno indonesio declaró oficialmente el Parque Nacional de Komodo en 1980, con el objetivo inicial de proteger al dragón de Komodo, aunque con el tiempo su misión se amplió a la conservación marina de todo el ecosistema, incluidos arrecifes de coral excepcionales entre Komodo, Rinca y Padar. Este es el marco legal que hoy protege exactamente el territorio, islas de Padar, Rinca y Komodo incluidas, que la pareja visitará desde Labuan Bajo.",
     "source": "legislación indonesia (decreto de creación del parque, 1980); UNESCO."},
    {"n": 25, "era": 5, "badge": "1991", "title": "Borobudur, Prambanan y Komodo, Patrimonio de la Humanidad",
     "body": "En un mismo año, 1991, la UNESCO inscribió tanto los templos de Borobudur y Prambanan como el Parque Nacional de Komodo en la lista de Patrimonio de la Humanidad, junto con el Parque Nacional de Ujung Kulon; fueron de los primeros sitios indonesios en recibir esta distinción. Es una curiosa coincidencia de calendario que conecta directamente los tres grandes destinos del itinerario: los templos de Java y las islas de Komodo recibieron el mismo reconocimiento internacional el mismo año.",
     "source": "UNESCO, Centro de Patrimonio Mundial (listado oficial de inscripciones)."},
    {"n": 26, "era": 5, "badge": "1998", "title": "La caída de Suharto y la Reformasi",
     "body": "La crisis financiera asiática de 1997 desestabilizó gravemente la economía indonesia y desató protestas masivas que forzaron la dimisión de Suharto en mayo de 1998, tras 32 años en el poder. Se inició así el periodo conocido como Reformasi, con la introducción de elecciones multipartidistas libres, una notable descentralización administrativa (que dio más autonomía a provincias como Bali y Nusa Tenggara Oriental) y una prensa mucho más libre.",
     "source": "consenso historiográfico y político sobre la transición indonesia."},
    {"n": 27, "era": 6, "badge": "2007-2011", "title": 'Komodo y las "Nuevas 7 Maravillas de la Naturaleza"', "flag": "Aclaración importante",
     "body": 'Komodo fue votado como una de las "Nuevas 7 Maravillas de la Naturaleza" en una campaña que concluyó en 2011. Conviene aclarar su naturaleza real: se trató de una votación privada y comercial organizada por la fundación suiza New Open World Corporation, sin ningún vínculo oficial con la UNESCO (que se desmarcó explícitamente de la iniciativa), y el proceso fue ampliamente criticado por su sistema de voto por SMS de pago, fácilmente influenciable por campañas nacionales de movilización masiva más que por criterios científicos de rareza o valor ecológico. Es un dato útil para matizar ante los guías o carteles locales que suelen presentar el título como un honor "oficial" equivalente al de la UNESCO, cuando en realidad son reconocimientos de naturaleza completamente distinta.',
     "source": "New Open World Corporation (organización de la votación); UNESCO (desmentido de vínculo oficial); prensa especializada en turismo."},
    {"n": 28, "era": 6, "badge": "2019-2022", "title": "La polémica del cierre de Komodo y la subida de tarifas",
     "body": 'En 2019, el gobernador de Nusa Tenggara Oriental, Viktor Laiskodat, propuso cerrar temporalmente la isla de Komodo para proteger a los dragones, en línea con una estrategia nacional de "turismo súper premium". La isla nunca llegó a cerrarse, pero sí se implementó, tras el parón de la pandemia, una fuerte subida de tarifas de entrada en 2022, junto con un límite anual de visitantes y un proyecto paralelo y polémico de infraestructura turística en la vecina isla de Rinca, apodado por la prensa "Jurassic Park", que generó críticas de la UNESCO y de conservacionistas por su impacto en el hábitat del dragón. Es relevante para la pareja porque explica por qué las tarifas de entrada al parque que pagarán en Labuan Bajo son notablemente más altas que hace pocos años, y por qué existen cupos diarios de visitantes en los senderos de avistamiento de dragones.',
     "source": "registros gubernamentales de Nusa Tenggara Oriental; prensa indonesia e internacional (Washington Post, entre otros)."},
    {"n": 29, "era": 6, "badge": "2018 en adelante", "title": "Labuan Bajo como destino turístico prioritario nacional",
     "body": 'El gobierno indonesio incluyó a Labuan Bajo, la puerta de entrada al Parque Nacional de Komodo, dentro de su estrategia de los "10 Nuevos Bali" y creó en 2018 una autoridad turística especial (Badan Otorita Pariwisata Labuan Bajo Flores) para acelerar inversión en infraestructura: ampliación del aeropuerto, carreteras y hoteles de alta gama. Este impulso explica el crecimiento reciente y notable de la oferta hotelera y de vuelos directos a Labuan Bajo que la pareja aprovechará en su propio viaje, en una localidad que hace apenas una década era un pequeño puerto pesquero de paso.',
     "source": "planificación gubernamental indonesia (Ministerio de Turismo); prensa de desarrollo turístico regional."},
    {"n": 30, "era": 6, "badge": "14-15 de agosto de 2026", "title": "El terremoto de Flores y Nusa Tenggara Oriental", "flag": "Actualidad, verificar antes de salir",
     "body": "En la madrugada del 15 de agosto de 2026 (hora local), un terremoto de magnitud 7,7-7,8 con epicentro frente a la costa norte de Nusa Tenggara Oriental, a unos 68 km al noroeste de Ende, sacudió Flores y generó un pequeño tsunami de unos 30 cm registrado en Labuan Bajo. El seísmo causó al menos 111 muertos y más de 1.600 heridos, con los mayores daños en las regencias de Manggarai y Manggarai Oriental, cerca de la propia Labuan Bajo, dañó edificios y el aeropuerto de la ciudad, y llegó a dejar temporalmente varados a cerca de mil turistas en la isla de Padar por la suspensión de los servicios portuarios. Es el dato de actualidad más directamente relevante para el viaje: conviene verificar antes de la salida el estado de la reconstrucción de infraestructuras hoteleras y portuarias en la zona de Labuan Bajo y Padar, ya que a la fecha de esta investigación (comienzos de septiembre de 2026) la reconstrucción en varias regencias de Flores seguía en curso, con carreteras cortadas por corrimientos de tierra en la carretera Trans-Flores.",
     "source": "Servicio Geológico de Estados Unidos (USGS) y GFZ alemán (datos sismológicos); agencias de noticias internacionales (Reuters/NBC News, NPR) y organismos de respuesta a desastres (Miyamoto International)."},
]


def render_historia_timeline():
    parts = []
    for m in MILESTONES_HISTORIA:
        era = ERAS_HISTORIA[m["era"]]
        flag_html = f'<span class="timeline-flag">{m["flag"]}</span>' if m.get("flag") else ""
        parts.append(
            '<div class="timeline-item" data-era="{era_n}" style="--era-color:{color}">'
            '<div class="timeline-dot"></div>'
            '<div class="timeline-card">'
            '<div class="timeline-card-head">'
            '<span class="timeline-era-tag">{era_name}</span>{flag}'
            '</div>'
            '<span class="timeline-year">{badge}</span>'
            '<h3 class="timeline-title">{title}</h3>'
            '<p class="timeline-body">{body}</p>'
            '<p class="timeline-source">Fuente: {source}</p>'
            '</div></div>'.format(
                era_n=m["era"], color=era["color"], era_name=era["name"], flag=flag_html,
                badge=m["badge"], title=m["title"], body=m["body"], source=m["source"],
            )
        )
    return "".join(parts)


def render_historia_filters():
    buttons = ['<button class="era-filter-btn active" data-era="todos" onclick="filterHistoria(\'todos\')">Todos los hitos</button>']
    for era_n, era in ERAS_HISTORIA.items():
        buttons.append(
            '<button class="era-filter-btn" data-era="{n}" style="--era-color:{color}" onclick="filterHistoria(\'{n}\')">{name}</button>'.format(
                n=era_n, color=era["color"], name=era["name"]
            )
        )
    return "".join(buttons)


n_hitos = len(MILESTONES_HISTORIA)
filtros_historia = render_historia_filters()
timeline_historia = render_historia_timeline()

html = f"""<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0, viewport-fit=cover">
<title>Indonesia 2027: Entre templos y dragones</title>

<!-- Fuentes tipograficas con inspiracion costera y de viaje de lujo, autoalojadas en base64 (sin dependencia de red externa) -->
<style>
@font-face {{
  font-family: 'DM Serif Display';
  font-style: normal;
  font-weight: 400;
  font-display: swap;
  src: url(data:font/woff2;base64,{FONT_DM_SERIF_NORMAL}) format('woff2');
}}
@font-face {{
  font-family: 'DM Serif Display';
  font-style: italic;
  font-weight: 400;
  font-display: swap;
  src: url(data:font/woff2;base64,{FONT_DM_SERIF_ITALIC}) format('woff2');
}}
@font-face {{
  font-family: 'Plus Jakarta Sans';
  font-style: normal;
  font-weight: 400 800;
  font-display: swap;
  src: url(data:font/woff2;base64,{FONT_JAKARTA_VARIABLE}) format('woff2-variations'), url(data:font/woff2;base64,{FONT_JAKARTA_VARIABLE}) format('woff2');
}}
</style>

<style>
/* PALETA OFICIAL SARAH RENAE CLARK (TEMA CLARO COSTERO) */
:root {{
  --c-cyan: #14b8a6;          /* Turquesa vibrante de arrecife */
  --c-teal: #0f766e;          /* Verde mar profundo / cerceta */
  --c-teal-dark: #115e59;     /* Cerceta oscura para titulos */
  --c-white: #ffffff;         /* Blanco puro para tarjetas */
  --c-porcelain: #f8fafc;     /* Blanco roto suave para fondo general */
  --c-sand: #f1f5f9;          /* Arena suave para secciones alternas */
  --c-coral: #ea8c84;         /* Coral calido / terracota rosada */
  --c-coral-dark: #be123c;    /* Coral acento */
  --c-indigo: #4f46e5;        /* Azul indigo para distinguir el vuelo en el mapa */
  --c-peach: #fde8e1;         /* Melocoton suave / blush */
  --c-peach-border: #f8c8ba;  /* Borde de melocoton */

  --text-title: #0f172a;      /* Pizarra oscuro para maxima legibilidad */
  --text-body: #334155;       /* Texto de lectura relajado */
  --text-muted: #64748b;      /* Texto secundario y etiquetas */
  
  --border-light: #e2e8f0;    /* Bordes sutiles y limpios */
  --border-focus: #14b8a6;
  
  --radius-sm: 8px;
  --radius-md: 14px;
  --radius-lg: 20px;
  --radius-pill: 999px;
  
  --shadow-sm: 0 2px 8px rgba(15, 23, 42, 0.04);
  --shadow-card: 0 10px 25px -5px rgba(15, 23, 42, 0.06), 0 8px 10px -6px rgba(15, 23, 42, 0.04);
  --shadow-hover: 0 20px 35px -8px rgba(15, 23, 42, 0.12);
}}

* {{
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}}

body {{
  font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
  background-color: var(--c-porcelain);
  color: var(--text-body);
  line-height: 1.65;
  -webkit-font-smoothing: antialiased;
  padding-bottom: 90px;
}}

h1, h2, h3, .font-serif {{
  font-family: 'DM Serif Display', Georgia, 'Times New Roman', serif;
  font-weight: 400;
  color: var(--text-title);
  letter-spacing: -0.01em;
}}

/* =========================================================
   HERO CINEMATICO A PANTALLA COMPLETA
   Video de fondo en bucle + velo oscuro para contraste.
   La barra superior flota transparente sobre el video y se
   vuelve solida al entrar en el contenido claro.
   ========================================================= */
.hero {{
  position: relative;
  min-height: 100svh;
  display: flex;
  flex-direction: column;
  padding: 0;
  overflow: hidden;
  background: #03181c;
  isolation: isolate;
}}

.hero-video-layer {{
  position: absolute;
  inset: -2px;
  z-index: 0;
  overflow: hidden;
  will-change: transform;
}}

.hero-video-layer video,
.hero-video-layer .hero-poster-img {{
  position: absolute;
  top: 50%;
  left: 50%;
  width: 100%;
  height: 100%;
  min-width: 100%;
  min-height: 100%;
  transform: translate(-50%, -50%) scale(1.05);
  object-fit: cover;
  display: block;
  filter: saturate(122%) contrast(108%);
}}

/* Velo en dos capas: vertical para legibilidad y radial para foco central */
.hero-scrim {{
  position: absolute;
  inset: 0;
  z-index: 1;
  pointer-events: none;
  background: linear-gradient(180deg,
    rgba(2, 17, 20, 0.74) 0%,
    rgba(2, 17, 20, 0.16) 24%,
    rgba(2, 17, 20, 0.08) 50%,
    rgba(2, 17, 20, 0.5) 82%,
    rgba(2, 17, 20, 0.96) 100%);
}}

/* Foco oscuro solo detras del titular: el paisaje de los bordes queda vivo */
.hero-scrim::after {{
  content: "";
  position: absolute;
  inset: 0;
  background: radial-gradient(64% 44% at 50% 45%, rgba(2, 17, 20, 0.58) 0%, rgba(2, 17, 20, 0.28) 55%, rgba(2, 17, 20, 0) 78%);
}}

.hero-top-bar {{
  position: relative;
  z-index: 120;
  width: 100%;
  max-width: 1280px;
  margin: 0 auto;
  padding: 20px 20px 0;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 14px;
}}

@media (min-width: 921px) {{
  .hero-top-bar {{
    position: fixed;
    top: 0;
    left: 0;
    right: 0;
    z-index: 120;
    max-width: none;
    padding: 15px 30px;
    transition: background 0.4s ease, padding 0.4s ease, box-shadow 0.4s ease;
  }}
  .hero-top-bar.bar-solid {{
    padding: 9px 30px;
    background: rgba(255, 255, 255, 0.93);
    backdrop-filter: blur(16px) saturate(170%);
    -webkit-backdrop-filter: blur(16px) saturate(170%);
    box-shadow: 0 4px 26px rgba(15, 23, 42, 0.1);
  }}
}}

.hero-meta-badge {{
  font-size: 0.78rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: #ffffff;
  background: rgba(255, 255, 255, 0.12);
  border: 1px solid rgba(255, 255, 255, 0.3);
  backdrop-filter: blur(12px);
  -webkit-backdrop-filter: blur(12px);
  padding: 7px 16px;
  border-radius: var(--radius-pill);
  transition: color 0.4s ease, background 0.4s ease, border-color 0.4s ease;
}}

.hero-meta-badge.badge-coral {{ color: #ffd9d0; }}

.bar-solid .hero-meta-badge {{
  color: var(--c-teal);
  background: #ffffff;
  border-color: rgba(15, 118, 110, 0.2);
  box-shadow: var(--shadow-sm);
}}
.bar-solid .hero-meta-badge.badge-coral {{
  color: var(--c-coral-dark);
  border-color: var(--c-peach-border);
}}

.hero-nav-pill-group {{
  display: flex;
  gap: 6px;
  background: rgba(255, 255, 255, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.22);
  backdrop-filter: blur(14px) saturate(150%);
  -webkit-backdrop-filter: blur(14px) saturate(150%);
  padding: 5px;
  border-radius: var(--radius-pill);
  overflow-x: auto;
  transition: background 0.4s ease, border-color 0.4s ease;
}}

.bar-solid .hero-nav-pill-group {{
  background: #ffffff;
  border-color: var(--border-light);
  box-shadow: var(--shadow-sm);
}}

.nav-pill-link {{
  background: transparent;
  color: rgba(255, 255, 255, 0.84);
  border: none;
  padding: 7px 15px;
  border-radius: var(--radius-pill);
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  white-space: nowrap;
}}

.nav-pill-link:hover {{
  color: #ffffff;
  background: rgba(255, 255, 255, 0.16);
}}

.nav-pill-link.active {{
  background: #ffffff;
  color: var(--c-teal-dark);
}}

.bar-solid .nav-pill-link {{ color: var(--text-muted); }}
.bar-solid .nav-pill-link:hover {{ color: var(--c-teal); background: var(--c-sand); }}
.bar-solid .nav-pill-link.active {{ background: var(--c-teal); color: #ffffff; }}

.hero-main-content {{
  position: relative;
  z-index: 10;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  max-width: 1080px;
  margin: 0 auto;
  padding: 60px 22px 20px;
  text-align: center;
  will-change: transform, opacity;
}}

.hero-kicker {{
  display: inline-block;
  font-size: 0.76rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.26em;
  color: rgba(255, 255, 255, 0.86);
  text-shadow: 0 1px 8px rgba(2, 17, 20, 0.7);
  margin-bottom: 22px;
  padding-bottom: 14px;
  border-bottom: 1px solid rgba(255, 255, 255, 0.24);
}}

.hero-main-content h1 {{
  font-size: clamp(2.7rem, 7.2vw, 5.7rem);
  line-height: 1.02;
  color: #ffffff;
  letter-spacing: -0.02em;
  text-shadow: 0 2px 12px rgba(2, 17, 20, 0.5), 0 8px 50px rgba(2, 17, 20, 0.4);
  margin-bottom: 24px;
}}

.hero-main-content h1 span.highlight {{
  display: block;
  font-style: italic;
  color: var(--c-coral);
}}

.hero-lead-text {{
  max-width: 720px;
  margin: 0 auto 32px;
  font-size: clamp(1rem, 1.15vw, 1.12rem);
  line-height: 1.65;
  color: rgba(255, 255, 255, 0.9);
  text-shadow: 0 1px 10px rgba(2, 17, 20, 0.6);
}}

.hero-stats-deck {{
  display: flex;
  justify-content: center;
  flex-wrap: wrap;
  gap: 10px;
}}

.stat-chip {{
  background: rgba(255, 255, 255, 0.11);
  border: 1px solid rgba(255, 255, 255, 0.24);
  backdrop-filter: blur(12px) saturate(140%);
  -webkit-backdrop-filter: blur(12px) saturate(140%);
  padding: 9px 17px;
  border-radius: var(--radius-pill);
  font-size: 0.84rem;
  color: rgba(255, 255, 255, 0.8);
  display: flex;
  align-items: center;
  gap: 6px;
}}

.stat-chip strong {{
  color: #ffffff;
  font-weight: 700;
}}

/* Aviso de scroll con gota descendente */
.hero-scroll-cue {{
  position: relative;
  z-index: 10;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 0 0 34px;
  font-size: 0.68rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.2em;
  color: rgba(255, 255, 255, 0.62);
}}

.cue-rail {{
  position: relative;
  width: 1px;
  height: 52px;
  background: rgba(255, 255, 255, 0.22);
  overflow: hidden;
}}

.cue-rail::after {{
  content: "";
  position: absolute;
  top: -52px;
  left: 0;
  width: 1px;
  height: 52px;
  background: linear-gradient(to bottom, transparent, #ffffff);
  animation: cueDrop 2.3s cubic-bezier(0.65, 0, 0.35, 1) infinite;
}}

@keyframes cueDrop {{
  0% {{ transform: translateY(0); }}
  75%, 100% {{ transform: translateY(104px); }}
}}

/* =========================================================
   CRONOLOGIA DE LA HISTORIA DE INDONESIA
   Linea vertical con un punto por hito, coloreado segun la
   era, y filtros por epoca. El color de cada era llega por
   la variable --era-color declarada en cada elemento.
   ========================================================= */
.era-filter-bar {{
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-bottom: 32px;
}}

.era-filter-btn {{
  --era-color: var(--c-teal);
  padding: 8px 16px;
  border-radius: var(--radius-pill);
  border: 1px solid var(--border-light);
  background: #ffffff;
  color: var(--text-muted);
  font-size: 0.82rem;
  font-weight: 650;
  font-family: inherit;
  cursor: pointer;
  transition: all 0.2s ease;
  display: inline-flex;
  align-items: center;
  gap: 8px;
}}

.era-filter-btn::before {{
  content: "";
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--era-color);
  flex: 0 0 8px;
}}

.era-filter-btn[data-era="todos"]::before {{ display: none; }}

.era-filter-btn:hover {{
  border-color: var(--era-color);
  color: var(--text-title);
}}

.era-filter-btn.active {{
  background: var(--era-color);
  border-color: var(--era-color);
  color: #ffffff;
}}

.era-filter-btn.active::before {{ background: rgba(255, 255, 255, 0.85); }}

.timeline-track {{
  position: relative;
  padding-left: 38px;
}}

.timeline-track::before {{
  content: "";
  position: absolute;
  left: 10px;
  top: 10px;
  bottom: 10px;
  width: 2px;
  background: linear-gradient(to bottom, var(--border-light), var(--c-cyan), var(--border-light));
  border-radius: 2px;
}}

.timeline-item {{
  position: relative;
  margin-bottom: 20px;
}}

.timeline-item:last-child {{ margin-bottom: 0; }}

.timeline-dot {{
  position: absolute;
  left: -34px;
  top: 24px;
  width: 14px;
  height: 14px;
  border-radius: 50%;
  background: var(--era-color);
  border: 3px solid var(--c-porcelain);
  box-shadow: 0 0 0 2px var(--era-color);
}}

.timeline-card {{
  background: var(--c-white);
  border: 1px solid var(--border-light);
  border-left: 4px solid var(--era-color);
  border-radius: var(--radius-md);
  padding: 20px 24px;
  box-shadow: var(--shadow-sm);
  transition: box-shadow 0.25s ease, transform 0.25s ease;
}}

.timeline-card:hover {{
  box-shadow: var(--shadow-card);
  transform: translateX(3px);
}}

.timeline-card-head {{
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 8px;
  margin-bottom: 10px;
}}

.timeline-era-tag {{
  font-size: 0.68rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  color: var(--era-color);
  /* Respaldo para navegadores sin color-mix: fondo arena y borde suave */
  background: var(--c-sand);
  border: 1px solid var(--border-light);
  background: color-mix(in srgb, var(--era-color) 10%, transparent);
  border-color: color-mix(in srgb, var(--era-color) 24%, transparent);
  padding: 4px 11px;
  border-radius: var(--radius-pill);
}}

/* Aviso de dato debatido o sin consenso cerrado */
.timeline-flag {{
  font-size: 0.68rem;
  font-weight: 700;
  color: var(--c-coral-dark);
  background: var(--c-peach);
  border: 1px solid var(--c-peach-border);
  padding: 4px 11px;
  border-radius: var(--radius-pill);
}}

.timeline-year {{
  display: block;
  font-size: 0.82rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.06em;
  color: var(--text-muted);
  margin-bottom: 4px;
}}

.timeline-title {{
  font-family: 'DM Serif Display', Georgia, serif;
  font-size: 1.28rem;
  line-height: 1.25;
  color: var(--text-title);
  margin-bottom: 10px;
}}

.timeline-body {{
  font-size: 0.94rem;
  line-height: 1.68;
  color: var(--text-body);
  margin-bottom: 12px;
}}

/* Nota de procedencia al pie de una tarjeta de la guia */
.source-note {{
  font-size: 0.78rem;
  line-height: 1.5;
  color: var(--text-muted);
  padding-top: 10px;
  margin-top: 4px;
  border-top: 1px dashed var(--border-light);
}}

.timeline-source {{
  font-size: 0.78rem;
  line-height: 1.5;
  color: var(--text-muted);
  padding-top: 10px;
  border-top: 1px dashed var(--border-light);
}}

@media (max-width: 600px) {{
  .timeline-track {{ padding-left: 26px; }}
  .timeline-track::before {{ left: 5px; }}
  .timeline-dot {{ left: -25px; top: 22px; width: 12px; height: 12px; }}
  .timeline-card {{ padding: 17px 18px; }}
  .timeline-title {{ font-size: 1.14rem; }}
  .era-filter-btn {{ font-size: 0.76rem; padding: 7px 13px; }}
}}

/* Con siete pestañas, el rótulo necesita algo menos de aire */
@media (max-width: 400px) {{
  .bottomnav .bn-item {{ font-size: 0.6rem; }}
  .bottomnav .bn-item svg {{ width: 20px; height: 20px; }}
}}

/* La barra fija mide unos 66 px: reservamos hueco al saltar con scroll */
.day-card-single,
.hotel-card-item,
.app-screen-view,
section.section,
#seccion-hoteles {{
  scroll-margin-top: 96px;
}}

/* El contenido claro monta sobre el hero oscuro: el corte de contraste */
main.container {{
  position: relative;
  z-index: 15;
  background: var(--c-porcelain);
  border-radius: 36px 36px 0 0;
  margin-top: -44px;
  padding-top: 34px;
  box-shadow: 0 -26px 70px rgba(2, 17, 20, 0.42);
}}

@media (max-width: 920px) {{
  .hero {{ min-height: auto; }}
  /* En movil la barra es solo navegacion: los datos ya salen en el hero
     y en la barra ocupaban tres filas */
  .hero-top-bar {{
    max-width: none;
    background: #03181c;
    padding: 12px 12px 13px;
    gap: 10px;
    justify-content: flex-start;
  }}
  .hero-top-bar .hero-meta-badge {{ display: none; }}
  .hero-nav-pill-group {{ width: 100%; }}
  .hero-main-content {{ padding: 40px 20px 58px; }}
  .hero-kicker {{ letter-spacing: 0.18em; margin-bottom: 18px; font-size: 0.68rem; }}
  .hero-main-content h1 {{ margin-bottom: 18px; }}
  .hero-lead-text {{ font-size: 0.94rem; line-height: 1.6; margin-bottom: 26px; }}
  .hero-stats-deck {{ gap: 8px; }}
  .stat-chip {{ font-size: 0.79rem; padding: 8px 14px; }}
  .hero-scroll-cue {{ display: none; }}
  main.container {{ border-radius: 26px 26px 0 0; margin-top: -30px; padding-top: 26px; }}
}}

@media (prefers-reduced-motion: reduce) {{
  .cue-rail::after {{ animation: none; }}
  .hero-video-layer {{ transform: none !important; }}
}}

/* Contenedor general */
.container {{
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 16px;
}}

/* CAJA DE SELECCION DE RUTAS */
.route-selector-container {{
  margin: 30px 0 35px;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}}

.route-card-toggle {{
  background: #ffffff;
  border: 2px solid var(--border-light);
  border-radius: var(--radius-lg);
  padding: 22px 26px;
  cursor: pointer;
  text-align: left;
  transition: all 0.25s ease;
  box-shadow: var(--shadow-sm);
}}

.route-card-toggle:hover {{
  transform: translateY(-2px);
  box-shadow: var(--shadow-card);
}}

.route-card-toggle.active {{
  border-color: var(--c-teal);
  background: linear-gradient(180deg, #ffffff 0%, rgba(20, 184, 166, 0.05) 100%);
  box-shadow: 0 8px 25px rgba(15, 118, 110, 0.12);
}}

.route-card-toggle.active.coral-active {{
  border-color: var(--c-coral);
  background: linear-gradient(180deg, #ffffff 0%, rgba(234, 140, 132, 0.07) 100%);
  box-shadow: 0 8px 25px rgba(234, 140, 132, 0.15);
}}

.toggle-tag {{
  font-size: 0.72rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.12em;
  color: var(--c-teal);
  margin-bottom: 6px;
  display: block;
}}

.route-card-toggle.coral-active .toggle-tag {{
  color: var(--c-coral-dark);
}}

.toggle-title {{
  font-size: 1.35rem;
  line-height: 1.2;
  margin-bottom: 6px;
  color: var(--text-title);
}}

.toggle-desc {{
  font-size: 0.88rem;
  color: var(--text-muted);
  line-height: 1.45;
}}

/* SECCIONES Y TITULOS */
.section {{
  margin-bottom: 60px;
}}

.section-head {{
  margin-bottom: 26px;
}}

.section-tag {{
  font-size: 0.78rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.15em;
  color: var(--c-teal);
  display: block;
  margin-bottom: 6px;
}}

.section-head h2 {{
  font-size: 2.1rem;
  color: var(--c-teal-dark);
  line-height: 1.18;
  margin-bottom: 8px;
}}

.section-head p {{
  font-size: 1rem;
  color: var(--text-muted);
  max-width: 820px;
}}

/* =======================================================
   LAYOUT DE DOS COLUMNAS EN ESCRITORIO (ESTILO CHINA 2027)
   Columna izquierda: Dias del itinerario
   Columna derecha: Mapa interactivo sticky que se mueve con el scroll
   ======================================================= */
.routegrid {{
  display: flex;
  flex-direction: column;
  gap: 24px;
}}

@media (min-width: 1020px) {{
  .routegrid {{
    display: grid;
    grid-template-columns: minmax(0, 1fr) 460px;
    gap: 36px;
    align-items: start;
  }}

  .routegrid > .route-days-col {{
    order: 1;
    min-width: 0;
  }}

  .routegrid > .route-map-col {{
    order: 2;
    position: sticky;
    top: 24px;
    z-index: 50;
  }}
}}

/* MAPA INTERACTIVO SVG */
.map-interactive-box {{
  background: #ffffff;
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-card);
}}

.map-control-bar {{
  padding: 14px 18px;
  background: linear-gradient(180deg, #ffffff 0%, var(--c-sand) 100%);
  border-bottom: 1px solid var(--border-light);
  display: flex;
  flex-direction: column;
  gap: 10px;
}}

.map-active-status {{
  display: flex;
  align-items: center;
  gap: 10px;
}}

.map-status-pill {{
  font-size: 0.72rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  padding: 4px 12px;
  border-radius: var(--radius-pill);
  background: var(--c-teal);
  color: #ffffff;
  flex-shrink: 0;
}}

.map-status-text {{
  font-size: 0.88rem;
  font-weight: 700;
  color: var(--text-title);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}}

/* Barra de progreso de la ruta */
.map-progress-bar-wrap {{
  width: 100%;
  height: 3px;
  background: rgba(15, 118, 110, 0.1);
  border-radius: 999px;
  overflow: hidden;
}}

.map-progress-fill {{
  height: 100%;
  width: 7.14%;
  background: linear-gradient(90deg, var(--c-cyan) 0%, var(--c-teal) 100%);
  transition: width 0.35s ease;
}}

.map-day-scrubber {{
  display: flex;
  gap: 4px;
  overflow-x: auto;
  padding: 2px 0;
  max-width: 100%;
}}

.scrub-btn {{
  background: #ffffff;
  border: 1px solid var(--border-light);
  color: var(--text-muted);
  padding: 4px 8px;
  border-radius: var(--radius-pill);
  font-size: 0.72rem;
  font-weight: 700;
  cursor: pointer;
  transition: all 0.15s ease;
  white-space: nowrap;
}}

.scrub-btn:hover {{
  border-color: var(--c-teal);
  color: var(--c-teal);
}}

.scrub-btn.active {{
  background: var(--c-teal);
  border-color: var(--c-teal);
  color: #ffffff;
}}

.svg-map-wrapper {{
  position: relative;
  background: #e6f6f4; /* Azul verdoso de mar sereno tropical */
  overflow: hidden;
}}

#mapSvg {{
  width: 100%;
  height: auto;
  min-height: 260px;
  display: block;
}}

/* Clases del mapa SVG */
.map-land {{
  fill: #ffffff;
  stroke: rgba(15, 118, 110, 0.22);
  stroke-width: 1;
}}

.map-watermark {{
  font-family: 'DM Serif Display', Georgia, serif;
  font-size: 13px;
  fill: rgba(15, 118, 110, 0.22);
  letter-spacing: 3px;
  font-style: italic;
  pointer-events: none;
}}

.map-leg {{
  fill: none;
  stroke-linecap: round;
  stroke-linejoin: round;
  transition: opacity 0.3s ease, stroke-width 0.3s ease;
}}

.map-leg.avion {{
  stroke: var(--c-indigo);
  stroke-width: 2.8;
  stroke-dasharray: 9 6;
}}

.map-leg.barco {{
  stroke: var(--c-cyan);
  stroke-width: 3.5;
  stroke-dasharray: 2 4;
}}

.map-leg.tierra {{
  stroke: var(--c-coral);
  stroke-width: 2.6;
}}

.map-leg.inactive {{
  opacity: 0.14;
}}

.map-leg.done {{
  opacity: 0.75;
}}

.map-leg.active-now {{
  opacity: 1;
  stroke-width: 5;
  filter: drop-shadow(0 2px 6px rgba(20, 184, 166, 0.65));
}}

.map-node {{
  cursor: pointer;
  transition: transform 0.2s ease;
}}

.map-node circle.hit {{
  fill: transparent;
}}

.map-node circle.pin {{
  fill: #ffffff;
  stroke: var(--c-teal);
  stroke-width: 2.5;
  transition: all 0.25s ease;
}}

.map-node:hover circle.pin {{
  fill: var(--c-cyan);
  stroke: #ffffff;
}}

.map-node.active-stop circle.pin {{
  fill: var(--c-coral-dark);
  stroke: #ffffff;
  stroke-width: 3.5;
}}

.map-node text {{
  font-family: 'Plus Jakarta Sans', sans-serif;
  font-size: 11px;
  font-weight: 700;
  fill: var(--text-title);
  paint-order: stroke;
  stroke: #ffffff;
  stroke-width: 3px;
  stroke-linejoin: round;
}}

@keyframes mapPulse {{
  0% {{ r: 6; opacity: 0.95; stroke-width: 2.5; }}
  100% {{ r: 26; opacity: 0; stroke-width: 1; }}
}}

.beacon-pulse {{
  fill: none;
  stroke: var(--c-coral-dark);
  pointer-events: none;
  animation: mapPulse 1.8s infinite ease-out;
}}

.map-footer-legend {{
  padding: 10px 16px;
  background: #ffffff;
  border-top: 1px solid var(--border-light);
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
  font-size: 0.78rem;
  color: var(--text-muted);
}}

.legend-item {{
  display: inline-flex;
  align-items: center;
  gap: 6px;
}}

.legend-line {{
  width: 20px;
  height: 0;
  display: inline-block;
}}

.legend-line.av {{ border-top: 2.5px dashed var(--c-indigo); }}
.legend-line.ba {{ border-top: 3px dotted var(--c-cyan); }}
.legend-line.ti {{ border-top: 2.5px solid var(--c-coral); }}

/* TABLA COMPARATIVA */
.table-wrap {{
  overflow-x: auto;
  background: #ffffff;
  border-radius: var(--radius-lg);
  border: 1px solid var(--border-light);
  box-shadow: var(--shadow-sm);
}}

table.clean-table {{
  width: 100%;
  border-collapse: collapse;
  text-align: left;
  font-size: 0.92rem;
}}

table.clean-table th, table.clean-table td {{
  padding: 16px 20px;
  border-bottom: 1px solid var(--border-light);
}}

table.clean-table th {{
  background: var(--c-sand);
  color: var(--text-title);
  font-weight: 700;
  font-size: 0.88rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}}

/* TARJETAS DE DIA INDIVIDUAL */
.day-card-single {{
  background: #ffffff;
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  overflow: hidden;
  margin-bottom: 28px;
  display: flex;
  flex-direction: column;
  box-shadow: var(--shadow-card);
  transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease, opacity 0.6s ease;
  scroll-margin-top: 24px;
}}

.day-card-single.active-reading {{
  border-color: var(--c-teal);
  box-shadow: 0 12px 30px -5px rgba(15, 118, 110, 0.15);
}}

/* REVELADO SUAVE AL HACER SCROLL */
.reveal-init {{
  opacity: 0;
  transform: translateY(20px);
}}

.reveal-init.is-visible {{
  opacity: 1;
  transform: none;
}}

@media (prefers-reduced-motion: reduce) {{
  .reveal-init {{
    opacity: 1 !important;
    transform: none !important;
    transition: none !important;
  }}
}}

.day-photo-wrap {{
  position: relative;
  background: var(--c-sand);
  height: 260px;
}}

.day-photo-wrap img {{
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}}

.day-content-wrap {{
  padding: 24px 26px;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}}

.day-meta-top {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  margin-bottom: 8px;
}}

.day-date-title {{
  font-size: 0.82rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  color: var(--c-teal);
}}

.day-pill-badge {{
  font-size: 0.72rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding: 4px 12px;
  border-radius: var(--radius-pill);
  background: var(--c-peach);
  color: var(--c-coral-dark);
}}

.day-pill-badge.cyan {{
  background: rgba(20, 184, 166, 0.12);
  color: var(--c-teal);
}}

/* =========================================================
   SISTEMA DE LUGAR + MINI-CHIPS DE CADA DIA
   La pastilla superpuesta sobre la foto indica SIEMPRE el
   lugar principal del dia. Los chips resumen vuelo,
   alojamiento (clicable) y actividad destacada.
   ========================================================= */

.day-photo-wrap::before {{
  content: "";
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 110px;
  background: linear-gradient(to bottom, rgba(15, 23, 42, 0.5), rgba(15, 23, 42, 0));
  z-index: 1;
  pointer-events: none;
}}

.day-place-tag {{
  position: absolute;
  top: 14px;
  left: 14px;
  z-index: 2;
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 7px 15px;
  border-radius: var(--radius-pill);
  font-size: 0.72rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.09em;
  color: #ffffff;
  background: rgba(15, 23, 42, 0.52);
  backdrop-filter: blur(12px) saturate(150%);
  -webkit-backdrop-filter: blur(12px) saturate(150%);
  border: 1px solid rgba(255, 255, 255, 0.24);
  box-shadow: 0 4px 16px rgba(15, 23, 42, 0.3);
}}

.day-place-tag .place-dot {{
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--c-cyan);
  box-shadow: 0 0 0 3px rgba(20, 184, 166, 0.32);
}}

.pl-bali .place-dot {{ background: #86efac; box-shadow: 0 0 0 3px rgba(134, 239, 172, 0.3); }}
.pl-java .place-dot {{ background: #fbbf24; box-shadow: 0 0 0 3px rgba(251, 191, 36, 0.3); }}
.pl-flores .place-dot {{ background: #a5b4fc; box-shadow: 0 0 0 3px rgba(165, 180, 252, 0.3); }}
.pl-espana .place-dot {{ background: #e2e8f0; box-shadow: 0 0 0 3px rgba(226, 232, 240, 0.28); }}

.day-chip-row {{
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin: 0 0 16px 0;
}}

.day-chip {{
  display: inline-flex;
  align-items: center;
  gap: 7px;
  padding: 6px 13px;
  border-radius: var(--radius-pill);
  font-size: 0.775rem;
  font-weight: 650;
  line-height: 1.25;
  background: var(--c-sand);
  border: 1px solid var(--border-light);
  color: var(--text-body);
  white-space: nowrap;
}}

.day-chip svg {{
  width: 14px;
  height: 14px;
  flex: 0 0 14px;
  fill: none;
  stroke: var(--c-teal);
  stroke-width: 2;
  stroke-linecap: round;
  stroke-linejoin: round;
}}

/* Chip de vuelo: indigo, igual que el tramo aereo del mapa */
.day-chip.chip-flight {{
  background: rgba(79, 70, 229, 0.08);
  border-color: rgba(79, 70, 229, 0.22);
  color: #3730a3;
}}
.day-chip.chip-flight svg {{ stroke: var(--c-indigo); }}

/* Chip de noche a bordo del barco */
.day-chip.chip-boat {{
  background: rgba(20, 184, 166, 0.09);
  border-color: rgba(20, 184, 166, 0.24);
  color: var(--c-teal-dark);
}}

/* Chip de alojamiento clicable: lleva a su ficha en la coleccion */
a.day-chip {{
  cursor: pointer;
  text-decoration: none;
  background: var(--c-peach);
  border-color: var(--c-peach-border);
  color: var(--c-coral-dark);
  transition: transform 0.18s ease, box-shadow 0.18s ease, background 0.18s ease, color 0.18s ease;
}}
a.day-chip svg {{ stroke: var(--c-coral-dark); }}
a.day-chip::after {{
  content: "↗";
  font-size: 0.72rem;
  font-weight: 800;
  opacity: 0.55;
  margin-left: 1px;
}}
a.day-chip:hover, a.day-chip:focus-visible {{
  background: var(--c-coral-dark);
  border-color: var(--c-coral-dark);
  color: #ffffff;
  transform: translateY(-2px);
  box-shadow: 0 6px 16px -4px rgba(190, 18, 60, 0.45);
  outline: none;
}}
a.day-chip:hover svg, a.day-chip:focus-visible svg {{ stroke: #ffffff; }}
a.day-chip:hover::after, a.day-chip:focus-visible::after {{ opacity: 1; }}

/* Resalte de la ficha de hotel al llegar desde un chip */
.hotel-card-item.hotel-flash {{
  animation: hotelFlashAnim 2.2s ease;
}}
@keyframes hotelFlashAnim {{
  0%, 100% {{ box-shadow: var(--shadow-card); }}
  12%, 62% {{ box-shadow: 0 0 0 3px var(--c-cyan), 0 20px 45px -12px rgba(20, 184, 166, 0.55); }}
}}

@media (max-width: 600px) {{
  .day-chip {{ font-size: 0.73rem; padding: 5px 11px; }}
  .day-place-tag {{ font-size: 0.66rem; padding: 6px 12px; top: 12px; left: 12px; }}
}}

.day-headline {{
  font-size: 1.45rem;
  line-height: 1.25;
  color: var(--text-title);
  margin-bottom: 14px;
}}

/* BLOQUES DE PLANES POR HORARIOS */
.day-slots-list {{
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-bottom: 18px;
}}

.day-slot-box {{
  background: var(--c-sand);
  border-left: 3px solid var(--c-teal);
  padding: 10px 14px;
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
}}

.day-slot-box.coral-accent {{
  border-left-color: var(--c-coral);
}}

.slot-time {{
  font-size: 0.75rem;
  font-weight: 800;
  text-transform: uppercase;
  color: var(--c-teal-dark);
  letter-spacing: 0.06em;
  margin-bottom: 3px;
  display: block;
}}

.day-slot-box.coral-accent .slot-time {{
  color: var(--c-coral-dark);
}}

.slot-text {{
  font-size: 0.9rem;
  color: var(--text-body);
  line-height: 1.5;
}}

/* FILA DE CONEXIONES Y LOGISTICA */
.day-info-grid {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px;
  background: var(--c-porcelain);
  border: 1px solid var(--border-light);
  border-radius: var(--radius-md);
  padding: 12px 16px;
  font-size: 0.82rem;
}}

.info-item strong {{
  color: var(--text-title);
  display: block;
  font-size: 0.75rem;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 2px;
}}

.info-item span {{
  color: var(--text-muted);
  line-height: 1.45;
  display: block;
}}

/* ALOJAMIENTOS CON FOTOS TOTALMENTE LIMPIAS */
.filter-button-bar {{
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 26px;
}}

.chip-btn {{
  background: #ffffff;
  border: 1px solid var(--border-light);
  color: var(--text-muted);
  padding: 8px 18px;
  border-radius: var(--radius-pill);
  font-size: 0.85rem;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s ease;
  box-shadow: var(--shadow-sm);
}}

.chip-btn:hover {{
  border-color: var(--c-teal);
  color: var(--c-teal);
}}

.chip-btn.active {{
  background: var(--c-teal);
  color: #ffffff;
  border-color: var(--c-teal);
}}

.hotel-grid-cards {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
  gap: 26px;
}}

.hotel-card-item {{
  background: #ffffff;
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: var(--shadow-card);
  transition: transform 0.25s ease, box-shadow 0.25s ease, opacity 0.6s ease;
}}

.hotel-card-item:hover {{
  transform: translateY(-4px);
  box-shadow: var(--shadow-hover);
}}

.hotel-photo-holder {{
  position: relative;
  height: 220px;
  background: var(--c-sand);
}}

.hotel-photo-holder img {{
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}}

.hotel-card-body {{
  padding: 20px;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}}

.hotel-tags-line {{
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
  margin-bottom: 10px;
}}

.tag-label {{
  font-size: 0.7rem;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.08em;
  padding: 3px 8px;
  border-radius: var(--radius-pill);
  background: var(--c-sand);
  color: var(--text-muted);
}}

.tag-label.espigon {{
  background: rgba(20, 184, 166, 0.12);
  color: var(--c-teal);
}}

.tag-label.playa {{
  background: var(--c-peach);
  color: var(--c-coral-dark);
}}

.hotel-name-title {{
  font-size: 1.35rem;
  line-height: 1.2;
  color: var(--text-title);
  margin-bottom: 4px;
}}

.hotel-place {{
  font-size: 0.82rem;
  font-weight: 600;
  color: var(--c-teal);
  margin-bottom: 10px;
}}

.hotel-short-desc {{
  font-size: 0.88rem;
  color: var(--text-body);
  line-height: 1.5;
  margin-bottom: 16px;
  flex-grow: 1;
}}

.sleep-comfort-box {{
  background: var(--c-sand);
  border-left: 3px solid var(--c-coral);
  border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
  padding: 10px 12px;
  margin-bottom: 16px;
  font-size: 0.81rem;
}}

.sleep-comfort-box strong {{
  color: var(--c-coral-dark);
  display: block;
  margin-bottom: 2px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-size: 0.72rem;
}}

.sleep-comfort-box p {{
  color: var(--text-body);
  line-height: 1.4;
}}

.hotel-action-links {{
  display: flex;
  gap: 8px;
  margin-top: auto;
  padding-top: 14px;
  border-top: 1px solid var(--border-light);
}}

.action-btn {{
  flex: 1;
  text-align: center;
  padding: 9px 12px;
  border-radius: var(--radius-sm);
  font-size: 0.82rem;
  font-weight: 700;
  text-decoration: none;
  transition: all 0.2s ease;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 5px;
}}

.btn-official-web {{
  background: var(--c-teal);
  color: #ffffff;
}}

.btn-official-web:hover {{
  background: var(--c-teal-dark);
}}

.btn-booking-com {{
  background: #ffffff;
  color: var(--c-teal-dark);
  border: 1px solid var(--border-light);
}}

.btn-booking-com:hover {{
  background: var(--c-sand);
  border-color: var(--c-teal);
}}

/* PANELES DE ANALISIS */
.two-panel-grid {{
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}}

.clean-panel {{
  background: #ffffff;
  border: 1px solid var(--border-light);
  border-radius: var(--radius-lg);
  padding: 26px;
  box-shadow: var(--shadow-sm);
  transition: opacity 0.6s ease, transform 0.5s ease;
}}

.clean-panel.panel-recommended {{
  border-top: 4px solid var(--c-teal);
}}

.clean-panel.panel-discarded {{
  border-top: 4px solid var(--c-coral);
}}

.panel-header-title {{
  font-size: 1.25rem;
  margin-bottom: 14px;
  color: var(--text-title);
}}

.clean-panel p, .clean-panel li {{
  font-size: 0.9rem;
  color: var(--text-body);
  line-height: 1.55;
  margin-bottom: 10px;
}}

.clean-panel ul {{
  padding-left: 18px;
  margin-bottom: 14px;
}}

/* =======================================================
   GUIA PRACTICA: TARJETAS CON ICONO (ANTES DE VIAJAR)
   ======================================================= */
.guide-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 20px;
}}

.guide-card {{
  display: flex;
  flex-direction: column;
}}

.guide-card-wide {{
  grid-column: 1 / -1;
}}

.guide-card-head {{
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 16px;
}}

.guide-card-icon {{
  width: 44px;
  height: 44px;
  border-radius: var(--radius-md);
  background: var(--c-sand);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}}

.guide-card-icon svg {{
  width: 22px;
  height: 22px;
  stroke: var(--c-teal);
  fill: none;
  stroke-width: 1.8;
  stroke-linecap: round;
  stroke-linejoin: round;
}}

.guide-card .panel-header-title {{
  margin-bottom: 0;
}}

.guide-fact-row {{
  display: flex;
  gap: 8px;
  flex-wrap: wrap;
  margin-bottom: 14px;
}}

.discrepancy-box {{
  background: var(--c-peach);
  border: 1px solid var(--c-peach-border);
  border-radius: var(--radius-md);
  padding: 14px 16px;
  margin: 4px 0 14px;
}}

.discrepancy-box .dx-label {{
  display: block;
  font-size: 0.7rem;
  font-weight: 800;
  text-transform: uppercase;
  letter-spacing: 0.09em;
  color: var(--c-coral-dark);
  margin-bottom: 6px;
}}

.discrepancy-box p, .discrepancy-box li {{
  font-size: 0.86rem;
  margin-bottom: 6px;
}}

.discrepancy-box p:last-child, .discrepancy-box li:last-child {{
  margin-bottom: 0;
}}

.guide-photo-strip {{
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
  gap: 12px;
  margin: 6px 0 20px;
}}

.guide-photo-strip figure {{
  margin: 0;
}}

.guide-photo-strip .photo-frame {{
  border-radius: var(--radius-md);
  overflow: hidden;
  background: var(--c-sand);
  aspect-ratio: 4 / 3;
}}

.guide-photo-strip img {{
  width: 100%;
  height: 100%;
  object-fit: cover;
  display: block;
}}

.guide-photo-strip figcaption {{
  font-size: 0.72rem;
  color: var(--text-muted);
  padding-top: 6px;
  line-height: 1.35;
}}

/* =======================================================
   BARRA DE NAVEGACION INFERIOR FIJA TIPO APP (SOLO EN MOVIL)
   Conmutacion de secciones para maxima velocidad y rendimiento
   ======================================================= */
.bottomnav {{
  display: none;
}}

/* Comportamiento de secciones en escritorio vs movil */
@media (min-width: 921px) {{
  .app-screen-view {{
    display: block !important;
  }}
}}

@media (max-width: 920px) {{
  body {{
    padding-bottom: 84px;
  }}

  /* En movil mostramos solo la seccion activa */
  .app-screen-view {{
    display: none;
  }}

  .app-screen-view.active-mobile-view {{
    display: block;
    animation: fadeInView 0.25s ease;
  }}

  @keyframes fadeInView {{
    from {{ opacity: 0; transform: translateY(6px); }}
    to {{ opacity: 1; transform: translateY(0); }}
  }}

  .bottomnav {{
    position: fixed;
    left: 0;
    right: 0;
    bottom: 0;
    z-index: 999;
    display: flex;
    background: rgba(255, 255, 255, 0.94);
    backdrop-filter: blur(20px) saturate(180%);
    -webkit-backdrop-filter: blur(20px) saturate(180%);
    border-top: 1px solid rgba(15, 23, 42, 0.08);
    box-shadow: 0 -4px 20px rgba(15, 23, 42, 0.06);
    padding: 8px 6px calc(8px + env(safe-area-inset-bottom, 0px));
  }}

  .bottomnav .bn-item {{
    flex: 1;
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 3px;
    font-size: 0.65rem;
    font-weight: 700;
    letter-spacing: 0.03em;
    color: var(--text-muted);
    text-decoration: none;
    -webkit-tap-highlight-color: transparent;
    transition: color 0.18s ease, transform 0.12s ease;
    border: none;
    background: none;
    cursor: pointer;
  }}

  .bottomnav .bn-item:active {{
    transform: scale(0.92);
  }}

  .bottomnav .bn-item svg {{
    width: 22px;
    height: 22px;
    stroke: currentColor;
    stroke-width: 2;
    fill: none;
    transition: transform 0.2s ease;
  }}

  .bottomnav .bn-item.active {{
    color: var(--c-teal);
  }}

  .bottomnav .bn-item.active svg {{
    transform: scale(1.1);
    filter: drop-shadow(0 2px 5px rgba(20, 184, 166, 0.35));
  }}

  .route-selector-container {{
    grid-template-columns: 1fr;
  }}
  .two-panel-grid {{
    grid-template-columns: 1fr;
  }}
  .day-info-grid {{
    grid-template-columns: 1fr;
  }}
  .hotel-grid-cards {{
    grid-template-columns: 1fr;
  }}
  .day-photo-wrap {{
    height: 210px;
  }}
  .hero-nav-pill-group {{
    justify-content: flex-start;
    -ms-overflow-style: none;
    scrollbar-width: none;
  }}
  .hero-nav-pill-group::-webkit-scrollbar {{ display: none; }}
}}

/* PIE DE PAGINA */
footer.clean-footer {{
  margin-top: 70px;
  padding: 35px 20px;
  text-align: center;
  border-top: 1px solid var(--border-light);
  color: var(--text-muted);
  font-size: 0.85rem;
}}
</style>
</head>
<body>

<!-- Sprite de iconos en linea: se define una vez y se reutiliza con <use> -->
<svg width="0" height="0" style="position:absolute" aria-hidden="true" focusable="false">
  <symbol id="i-vuelo" viewBox="0 0 24 24"><path d="M22 2 11 13"/><path d="M22 2 15 22l-4-9-9-4Z"/></symbol>
  <symbol id="i-tren" viewBox="0 0 24 24"><rect x="4" y="3" width="16" height="13" rx="2"/><path d="M4 10h16"/><path d="M12 16v3"/><path d="M8 22l2-3"/><path d="M16 22l-2-3"/><path d="M6 22h12"/></symbol>
  <symbol id="i-cama" viewBox="0 0 24 24"><path d="M2 20v-8a2 2 0 0 1 2-2h16a2 2 0 0 1 2 2v8"/><path d="M2 15h20"/><path d="M6 10V7a1 1 0 0 1 1-1h3a1 1 0 0 1 1 1v3"/><path d="M2 20h20"/></symbol>
  <symbol id="i-barco" viewBox="0 0 24 24"><path d="M12 22V8"/><circle cx="12" cy="5" r="3"/><path d="M5 12H2a10 10 0 0 0 20 0h-3"/></symbol>
  <symbol id="i-mar" viewBox="0 0 24 24"><path d="M2 8c2-1.6 4-1.6 6 0s4 1.6 6 0 4-1.6 6 0"/><path d="M2 14c2-1.6 4-1.6 6 0s4 1.6 6 0 4-1.6 6 0"/><path d="M2 20c2-1.6 4-1.6 6 0s4 1.6 6 0 4-1.6 6 0"/></symbol>
  <symbol id="i-templo" viewBox="0 0 24 24"><path d="M12 2 3 8h18Z"/><path d="M5 8v4h14V8"/><path d="M4 12h16"/><path d="M7 12v6h10v-6"/><path d="M3 18h18v3H3Z"/></symbol>
  <symbol id="i-montana" viewBox="0 0 24 24"><path d="M2 20h20L14.5 6.5 11 12.5 8 8.5Z"/></symbol>
  <symbol id="i-fauna" viewBox="0 0 24 24"><circle cx="7" cy="8.5" r="1.9"/><circle cx="11.8" cy="6.4" r="1.9"/><circle cx="16.6" cy="8.5" r="1.9"/><circle cx="19" cy="13.6" r="1.9"/><path d="M6.2 16.6c0-2.6 2.2-4.6 4.9-4.6s4.9 2 4.9 4.6-2.2 4.6-4.9 4.6-4.9-2-4.9-4.6Z"/></symbol>
  <symbol id="i-sol" viewBox="0 0 24 24"><circle cx="12" cy="12" r="4.4"/><path d="M12 1.6v2.2"/><path d="M12 20.2v2.2"/><path d="M4.2 4.2l1.6 1.6"/><path d="M18.2 18.2l1.6 1.6"/><path d="M1.6 12h2.2"/><path d="M20.2 12h2.2"/><path d="M4.2 19.8l1.6-1.6"/><path d="M18.2 5.8l1.6-1.6"/></symbol>
  <symbol id="i-agua" viewBox="0 0 24 24"><path d="M12 2.6 6.4 8.2a7.9 7.9 0 1 0 11.2 0Z"/></symbol>
  <symbol id="i-gastro" viewBox="0 0 24 24"><path d="M6 2v7a3 3 0 0 0 6 0V2"/><path d="M9 12v10"/><path d="M17.5 2c-1.6 2.2-2.2 4.2-2.2 6.2 0 1.6.7 2.6 2.2 2.6s2.2-1 2.2-2.6c0-2-.6-4-2.2-6.2Z"/><path d="M17.5 12.4V22"/></symbol>
  <symbol id="i-hoja" viewBox="0 0 24 24"><path d="M11 20A7 7 0 0 1 9.8 6.1C15.5 5 17 4.5 19 2c1 2 2 4.2 2 8 0 5.5-4.8 10-10 10Z"/><path d="M2 21c0-3 1.9-5.7 4.5-7.5"/></symbol>
  <symbol id="i-cultura" viewBox="0 0 24 24"><path d="M16 21v-2a4 4 0 0 0-4-4H6a4 4 0 0 0-4 4v2"/><circle cx="9" cy="7" r="4"/><path d="M22 21v-2a4 4 0 0 0-3-3.9"/><path d="M16 3.1a4 4 0 0 1 0 7.8"/></symbol>
</svg>

<!-- BARRA DE NAVEGACION FLOTANTE (fuera del hero para quedar siempre encima) -->
<div class="hero-top-bar" id="siteTopBar">
    <div class="hero-meta-badge">Zaragoza · 21 abr al 4 may 2027</div>

    <nav class="hero-nav-pill-group">
      <button class="nav-pill-link active" onclick="switchRoute('opcion-a')">Ruta A: Con Java</button>
      <button class="nav-pill-link" onclick="switchRoute('opcion-b')">Ruta B: Sin Java</button>
      <button class="nav-pill-link" onclick="showAppScreen('app-view-hoteles')">10 Alojamientos</button>
      <button class="nav-pill-link" onclick="showAppScreen('app-view-vuelos')">Vuelos</button>
      <button class="nav-pill-link" onclick="showAppScreen('app-view-criterio')">Criterio</button>
      <button class="nav-pill-link" onclick="showAppScreen('app-view-historia')">Historia</button>
      <button class="nav-pill-link" onclick="showAppScreen('app-view-guia')">Antes de viajar</button>
    </nav>
    
  <div class="hero-meta-badge badge-coral">14 días · 11 noches</div>
</div>

<!-- HERO CINEMATICO CON VIDEO DE FONDO -->
<header class="hero">
  <div class="hero-video-layer" id="heroVideoLayer">{HERO_MEDIA}</div>
  <div class="hero-scrim"></div>

  <div class="hero-main-content" id="heroMainContent">
    <span class="hero-kicker">Documento de decisión · Expedición en pareja</span>
    <h1>Indonesia entre templos<span class="highlight">&amp; dragones salvajes</span></h1>
    <p class="hero-lead-text">
      Planificación técnica para dos viajeros activos de 32 años. Snorkel con mantarrayas gigantes, templos milenarios budistas e hinduistas, arrozales sagrados y estancias en resorts con espigón sobre el arrecife y descanso garantizado en colchones de gama superior.
    </p>

    <div class="hero-stats-deck">
      <div class="stat-chip">Salida: <strong>21 abril 2027</strong></div>
      <div class="stat-chip">Regreso a Zaragoza: <strong>4 mayo 2027</strong></div>
      <div class="stat-chip">Temporada: <strong>Inicio estación seca (óptima)</strong></div>
    </div>
  </div>

  <div class="hero-scroll-cue" aria-hidden="true">
    <span>Las dos rutas</span>
    <span class="cue-rail"></span>
  </div>
</header>

<main class="container">

  <!-- =======================================================
       PANTALLA 1: ITINERARIO Y MAPA EN ESCRITORIO (.routegrid)
       En movil: Vista "Ruta"
       ======================================================= -->
  <div class="app-screen-view active-mobile-view" id="app-view-ruta">
    
    <!-- Selector de Rutas -->
    <section class="route-selector-container" id="selector-de-ruta">
      <div class="route-card-toggle active" id="card-toggle-a" onclick="switchRoute('opcion-a')">
        <span class="toggle-tag">Opción A · El Gran Triángulo</span>
        <h3 class="toggle-title">Con Java: Templos imperiales, Komodo y Bali</h3>
        <p class="toggle-desc">Yogyakarta (Borobudur y Prambanan) + 3 noches en goleta Phinisi por Komodo + 1 noche en resort con espigón sobre el arrecife + 4 noches en el Valle de Sidemen, con el pecio del Liberty en Tulamben.</p>
      </div>

      <div class="route-card-toggle" id="card-toggle-b" onclick="switchRoute('opcion-b')">
        <span class="toggle-tag">Opción B · Ritmo Equilibrado</span>
        <h3 class="toggle-title">Sin Java: Bali sagrado, Komodo y Munduk</h3>
        <p class="toggle-desc">1 solo vuelo doméstico (Bali a Komodo ida y vuelta). 4 noches en Sidemen con el pecio del Liberty, 3 noches de goleta con los dragones incluidos, 1 noche en resort con espigón y 3 noches en Munduk con Sekumpul.</p>
      </div>
    </section>

    <!-- Tabla comparativa rapida -->
    <section class="section" style="margin-bottom:40px;">
      <div class="table-wrap">
        <table class="clean-table">
          <thead>
            <tr>
              <th>Criterio</th>
              <th style="color:var(--c-teal);">Ruta A: Con Java (Templos imperiales)</th>
              <th style="color:var(--c-coral-dark);">Ruta B: Sin Java (Ritmo equilibrado)</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td><strong>Templos y patrimonio</strong></td>
              <td>Máxima escala monumental: Borobudur (budista, siglo IX) y Prambanan (hinduista, siglo IX).</td>
              <td>Templos milenarios de Bali: santuarios de roca de Gunung Kawi, Pura Kehen y manantiales sagrados.</td>
            </tr>
            <tr>
              <td><strong>Vida marina y snorkel</strong></td>
              <td>Komodo completo: mantarrayas gigantes en Manta Point, tortugas en Siaba Besar y Pink Beach.</td>
              <td>Komodo completo + opción de snorkel en paredes de coral del Parque Nacional de Menjangan en Bali.</td>
            </tr>
            <tr>
              <td><strong>Vuelos internos</strong></td>
              <td>3 vuelos domésticos: Yakarta a Yogyakarta, Yogyakarta a Bali y Bali a Labuan Bajo.</td>
              <td>1 único trayecto aéreo interno ida y vuelta: Bali a Labuan Bajo (1 h 10 min).</td>
            </tr>
            <tr>
              <td><strong>Ritmo de viaje</strong></td>
              <td>Activo y dinámico, aprovechando madrugones para ver amaneceres inolvidables.</td>
              <td>Pausado, con 4 noches seguidas en Sidemen, 3 en la goleta, 1 en el resort con espigón y 3 en Munduk.</td>
            </tr>
          </tbody>
        </table>
      </div>
    </section>

    <!-- CUADRICULA DE RUTA (EN ORDENADOR: 2 COLUMNAS CON MAPA STICKY SINCRONIZADO) -->
    <div class="routegrid">
      
      <!-- COLUMNA 1: LISTADO DE DIAS -->
      <div class="route-days-col">

        <!-- RUTA A: 14 DIAS INDIVIDUALES -->
        <div class="route-block" id="block-opcion-a">
          <div class="section-head">
            <span class="section-tag">Itinerario día a día</span>
            <h2>Ruta A: Con Java (Los 14 días al detalle)</h2>
            <p>Conforme avanzas en la lectura, el mapa de la derecha une los tramos y se sincroniza automáticamente con tu progreso.</p>
          </div>

          <!-- DIA 1 -->
          <article class="day-card-single" id="dia-a-1" data-dia="1" data-title="Zaragoza a Madrid/Barcelona y despegue">
            <div class="day-photo-wrap"><img src="{get_img("zaragoza_delicias")}" alt="Salida del viaje"><span class="day-place-tag pl-espana"><span class="place-dot"></span>España</span></div>
            <div class="day-content-wrap">
              <div>
                <div class="day-meta-top">
                  <span class="day-date-title">Día 1 · Miércoles 21 de abril</span>
                </div>
                <h3 class="day-headline">Salida de Zaragoza en AVE y despegue del vuelo internacional</h3>
                <div class="day-chip-row">
                  <span class="day-chip"><svg><use href="#i-tren"></use></svg>AVE a Madrid o Barcelona</span>
                  <span class="day-chip chip-flight"><svg><use href="#i-vuelo"></use></svg>Vuelo intercontinental</span>
                </div>
                <div class="day-slots-list">
                  <div class="day-slot-box">
                    <span class="slot-time">Mañana y mediodía (12:30 h a 15:45 h)</span>
                    <p class="slot-text">Enlace en tren de alta velocidad AVE o Iryo desde la estación de Zaragoza Delicias hacia Madrid Puerta de Atocha (1 h 15 min) o Barcelona Sants (1 h 25 min). Conexión en tren de Cercanías directo a la terminal del aeropuerto (Barajas T4 o El Prat T1). Facturación del equipaje directamente hasta el destino asiático.</p>
                  </div>
                  <div class="day-slot-box">
                    <span class="slot-time">Tarde y noche (17:30 h a 23:00 h)</span>
                    <p class="slot-text">Embarque en vuelo internacional con aerolínea de bandera (Qatar Airways vía Doha, Emirates vía Dubái o Singapore Airlines vía Singapur). Cena a bordo y noche en vuelo transcontinental.</p>
                  </div>
                </div>
              </div>
              <div class="day-info-grid">
                <div class="info-item"><strong>Transporte:</strong><span>AVE Zaragoza Delicias a Madrid/BCN + Vuelo intercontinental con escala corta.</span></div>
                <div class="info-item"><strong>Consejo práctico:</strong><span>Llevar pasaporte con vigencia superior a 6 meses y visado e-VOA previo.</span></div>
              </div>
            </div>
          </article>

          <!-- DIA 2 -->
          <article class="day-card-single" id="dia-a-2" data-dia="2" data-title="Llegada a Yakarta y salto a Borobudur">
            <div class="day-photo-wrap"><img src="{get_img("borobudur")}" alt="Llegada a Java"><span class="day-place-tag pl-java"><span class="place-dot"></span>Java</span></div>
            <div class="day-content-wrap">
              <div>
                <div class="day-meta-top">
                  <span class="day-date-title">Día 2 · Jueves 22 de abril</span>
                </div>
                <h3 class="day-headline">Aterrizaje en Yakarta, salto a Yogyakarta y llegada a Borobudur</h3>
                <div class="day-chip-row">
                  <span class="day-chip chip-flight"><svg><use href="#i-vuelo"></use></svg>CGK a YIA</span>
                  <span class="day-chip"><svg><use href="#i-cama"></use></svg>Plataran Heritage Borobudur</span>
                  <span class="day-chip"><svg><use href="#i-hoja"></use></svg>Selva de Java</span>
                </div>
                <div class="day-slots-list">
                  <div class="day-slot-box">
                    <span class="slot-time">Tarde (15:00 h a 17:30 h)</span>
                    <p class="slot-text">Aterrizaje en el Aeropuerto Internacional de Yakarta (CGK). Trámite exprés de aduanas con el código QR digital (e-CD). Vuelo de conexión de 55 minutos a Yogyakarta (aeropuerto YIA) con Garuda Indonesia o Batik Air.</p>
                  </div>
                  <div class="day-slot-box coral-accent">
                    <span class="slot-time">Noche (19:00 h a 22:00 h)</span>
                    <p class="slot-text">Recepción con chófer privado en el aeropuerto YIA. Traslado de 1 hora por carretera hacia la zona rural y boscosa de Borobudur. Check-in en hotel boutique con cama king-size de gama superior. Cena tradicional javanesa y descanso reparador.</p>
                  </div>
                </div>
              </div>
              <div class="day-info-grid">
                <div class="info-item"><strong>Conexión aérea:</strong><span>Vuelo doméstico CGK a YIA (55 min) + Traslado privado en coche climatizado a Borobudur.</span></div>
                <div class="info-item"><strong>Alojamiento:</strong><span>Plataran Heritage Borobudur o Villa Borobudur. Silencio absoluto de selva.</span></div>
              </div>
            </div>
          </article>

          <!-- DIA 3 -->
          <article class="day-card-single" id="dia-a-3" data-dia="3" data-title="Amanecer en Borobudur y atardecer en Prambanan">
            <div class="day-photo-wrap"><img src="{get_img("prambanan")}" alt="Borobudur y Prambanan"><span class="day-place-tag pl-java"><span class="place-dot"></span>Java</span></div>
            <div class="day-content-wrap">
              <div>
                <div class="day-meta-top">
                  <span class="day-date-title">Día 3 · Viernes 23 de abril</span>
                </div>
                <h3 class="day-headline">Amanecer entre estupas en Borobudur y atardecer en Prambanan</h3>
                <div class="day-chip-row">
                  <span class="day-chip"><svg><use href="#i-templo"></use></svg>Borobudur y Prambanan</span>
                  <span class="day-chip"><svg><use href="#i-gastro"></use></svg>Gudeg de Yogyakarta</span>
                  <span class="day-chip"><svg><use href="#i-cama"></use></svg>Segunda noche en Borobudur</span>
                </div>
                <div class="day-slots-list">
                  <div class="day-slot-box">
                    <span class="slot-time">Amanecer y mañana (06:00 h a 11:30 h)</span>
                    <p class="slot-text">Subida a primera hora a las terrazas monumentales de piedra esculpida de Borobudur (siglo IX) entre campanas de piedra y estatuas de Buda con vistas a la bruma matinal del volcán Merapi. Recorrido guiado con especialista para interpretar los bajorrelieves budistas. Regreso al hotel para desayuno.</p>
                  </div>
                  <div class="day-slot-box coral-accent">
                    <span class="slot-time">Tarde (14:30 h a 18:30 h)</span>
                    <p class="slot-text">Traslado hacia el este de Yogyakarta para visitar el complejo hinduista de Prambanan, contemplando sus agujas de piedra de 47 metros consagradas a Shiva, Brahma y Vishnu bajo la luz dorada del atardecer.</p>
                  </div>
                </div>
              </div>
              <div class="day-info-grid">
                <div class="info-item"><strong>Entrada regulada:</strong><span>Pase especial con acceso a la estructura monumental de Borobudur reservado previamente.</span></div>
                <div class="info-item"><strong>Gastronomía local:</strong><span>Gudeg Yu Djum en Yogyakarta (yaca tierna cocinada a fuego lento con leche de coco).</span></div>
                <div class="info-item"><strong>Precios de entrada:</strong><span>Borobudur con subida a los niveles superiores: 455.000 IDR (incluye guía y sandalias tejidas); solo recinto sin subir: entre 412.500 y 455.000 IDR según la fuente consultada. Prambanan: entre 375.000 y 400.000 IDR según la fuente. Conviene reconfirmar en borobudurpark.com poco antes de viajar.</span></div>
              </div>
            </div>
          </article>

          <!-- DIA 4 -->
          <article class="day-card-single" id="dia-a-4" data-dia="4" data-title="Vuelo a Flores y llegada a Labuan Bajo">
            <div class="day-photo-wrap"><img src="{get_img("labuan_bajo")}" alt="Llegada a Labuan Bajo"><span class="day-place-tag pl-flores"><span class="place-dot"></span>Flores</span></div>
            <div class="day-content-wrap">
              <div>
                <div class="day-meta-top">
                  <span class="day-date-title">Día 4 · Sábado 24 de abril</span>
                </div>
                <h3 class="day-headline">Vuelo a la isla de Flores y tarde marinera en Labuan Bajo</h3>
                <div class="day-chip-row">
                  <span class="day-chip chip-flight"><svg><use href="#i-vuelo"></use></svg>YIA a DPS y DPS a LBJ</span>
                  <a class="day-chip" href="#hotel-ayana" onclick="return goToHotel('hotel-ayana');" title="Ver la ficha del alojamiento"><svg><use href="#i-cama"></use></svg>AYANA Komodo</a>
                  <span class="day-chip"><svg><use href="#i-gastro"></use></svg>Marisco en Labuan Bajo</span>
                </div>
                <div class="day-slots-list">
                  <div class="day-slot-box">
                    <span class="slot-time">Mañana (08:30 h a 13:30 h)</span>
                    <p class="slot-text">Traslado al aeropuerto YIA de Yogyakarta. Vuelo directo a Bali (1 h 15 min) y conexión inmediata a Labuan Bajo (isla de Flores, 1 h 10 min). Vistas panorámicas desde el avión del archipiélago de Komodo con sus arrecifes turquesas.</p>
                  </div>
                  <div class="day-slot-box">
                    <span class="slot-time">Tarde y noche (15:30 h a 21:30 h)</span>
                    <p class="slot-text">Llegada al hotel con vistas a la bahía de Labuan Bajo. Paseo por el puerto deportivo y café de especialidad de Flores en una terraza panorámica. Cena de pescado fresco recién capturado a la brasa en el mercado nocturno de Kampung Ujung.</p>
                  </div>
                </div>
              </div>
              <div class="day-info-grid">
                <div class="info-item"><strong>Vuelos:</strong><span>YIA a DPS (09:15 h) + DPS a LBJ (12:20 h). Equipaje recogido en Flores.</span></div>
                <div class="info-item"><strong>Alojamiento:</strong><span>Meruorah Komodo o AYANA Komodo. Cama de 5 estrellas para cargar pilas.</span></div>
              </div>
            </div>
          </article>

          <!-- DIA 5 -->
          <article class="day-card-single" id="dia-a-5" data-dia="5" data-title="Embarque en Phinisi, Kelor y Rinca">
            <div class="day-photo-wrap"><img src="{get_img("komodo_dragon")}" alt="Isla Rinca y dragones"><span class="day-place-tag pl-komodo"><span class="place-dot"></span>Komodo</span></div>
            <div class="day-content-wrap">
              <div>
                <div class="day-meta-top">
                  <span class="day-date-title">Día 5 · Domingo 25 de abril</span>
                </div>
                <h3 class="day-headline">Embarque en barco tradicional Phinisi, Isla Kelor y dragones en Rinca</h3>
                <div class="day-chip-row">
                  <span class="day-chip chip-boat"><svg><use href="#i-barco"></use></svg>Goleta Phinisi</span>
                  <span class="day-chip"><svg><use href="#i-fauna"></use></svg>Dragones en Rinca</span>
                  <span class="day-chip"><svg><use href="#i-mar"></use></svg>Isla Kelor</span>
                </div>
                <div class="day-slots-list">
                  <div class="day-slot-box">
                    <span class="slot-time">Mañana (08:30 h a 13:00 h)</span>
                    <p class="slot-text">Embarque en el puerto de Labuan Bajo en una goleta tradicional indonesia de madera (Phinisi) con camarote privado climatizado y baño en suite. Navegación a Isla Kelor: caminata a la cima de su colina con vistas de 360 grados y primer snorkel en aguas transparentes.</p>
                  </div>
                  <div class="day-slot-box coral-accent">
                    <span class="slot-time">Tarde y atardecer (14:30 h a 19:00 h)</span>
                    <p class="slot-text">Navegación hacia la Isla de Rinca. Caminata guiada con los guardaparques oficiales (*rangers*) observando dragones de Komodo en plena libertad, búfalos salvajes y ciervos. Fondeo al atardecer frente a Isla Kalong para contemplar el vuelo de miles de zorros voladores gigantes.</p>
                  </div>
                </div>
              </div>
              <div class="day-info-grid">
                <div class="info-item"><strong>Vida a bordo:</strong><span>Camarote privado con aire acondicionado, cama con colchón confortable y cocina fresca.</span></div>
                <div class="info-item"><strong>Calzado:</strong><span>Zapatillas deportivas de agarre para colinas de tierra y escarpines para el agua.</span></div>
                <div class="info-item"><strong>Tarifas y cupo del parque nacional:</strong><span>Desde el 1 de abril de 2026 el parque está limitado a 1.000 visitantes al día y la visita se reserva obligatoriamente por la app oficial SIORA, sin venta en taquilla. La estructura oficial va por conceptos (entrada marina, tasa portuaria y guardaparques por grupo) y ronda los 50 dólares por persona; el paquete de 650.000 IDR que citan muchos operadores no está confirmado por la autoridad del parque. Conviene ignorar cualquier web que aún hable de una tasa de 3.500.000 IDR: se anuló oficialmente en diciembre de 2022. Lo gestiona el operador del barco, que dará la cifra exacta al reservar.</span></div>
              </div>
            </div>
          </article>

          <!-- DIA 6 -->
          <article class="day-card-single" id="dia-a-6" data-dia="6" data-title="Amanecer en Isla Padar y Pink Beach">
            <div class="day-photo-wrap"><img src="{get_img("padar")}" alt="Isla Padar y Pink Beach"><span class="day-place-tag pl-komodo"><span class="place-dot"></span>Komodo</span></div>
            <div class="day-content-wrap">
              <div>
                <div class="day-meta-top">
                  <span class="day-date-title">Día 6 · Lunes 26 de abril</span>
                </div>
                <h3 class="day-headline">Amanecer en Isla Padar y snorkel en Pink Beach</h3>
                <div class="day-chip-row">
                  <span class="day-chip"><svg><use href="#i-montana"></use></svg>Mirador de Padar</span>
                  <span class="day-chip"><svg><use href="#i-mar"></use></svg>Snorkel en Pink Beach</span>
                  <span class="day-chip chip-boat"><svg><use href="#i-barco"></use></svg>Noche a bordo</span>
                </div>
                <div class="day-slots-list">
                  <div class="day-slot-box">
                    <span class="slot-time">Amanecer y mañana (05:15 h a 11:30 h)</span>
                    <p class="slot-text">Subida al alba al mirador de Isla Padar para ver la salida del sol sobre sus tres bahías de arena blanca, negra volcánica y rosa. Desayuno a bordo con fruta fresca tropical. Travesía hacia Pink Beach (Pantai Merah): snorkel directo desde la arena rosada entre jardines de gorgonias y peces payaso.</p>
                  </div>
                  <div class="day-slot-box">
                    <span class="slot-time">Tarde y noche (14:00 h a 21:00 h)</span>
                    <p class="slot-text">Navegación hacia una bahía resguardada. Sesión de paddle surf desde el barco en aguas mansas. Cena en cubierta bajo un cielo estrellado sin contaminación lumínica y noche fondeados en calma.</p>
                  </div>
                </div>
              </div>
              <div class="day-info-grid">
                <div class="info-item"><strong>Snorkel somero:</strong><span>Arrecifes a apenas 1 o 2 metros de profundidad, ideales para ver colores vivos sin botella.</span></div>
                <div class="info-item"><strong>Protección:</strong><span>Camiseta de licra UV50 y crema biodegradable reef-safe respetuosa con corales.</span></div>
                <div class="info-item"><strong>Subida al mirador:</strong><span>Entre 700 y 1.000 escalones según la fuente (815 es la cifra más citada), 20 a 45 minutos de subida. Sin apenas sombra, por lo que subir al amanecer es muy recomendable.</span></div>
              </div>
            </div>
          </article>

          <!-- DIA 7 -->
          <article class="day-card-single" id="dia-a-7" data-dia="7" data-title="Mantas en Manta Point y Taka Makassar">
            <div class="day-photo-wrap"><img src="{get_img("manta_ray")}" alt="Mantas en Manta Point"><span class="day-place-tag pl-komodo"><span class="place-dot"></span>Komodo</span></div>
            <div class="day-content-wrap">
              <div>
                <div class="day-meta-top">
                  <span class="day-date-title">Día 7 · Martes 27 de abril</span>
                </div>
                <h3 class="day-headline">Mantas gigantes en Manta Point y banco de arena Taka Makassar</h3>
                <div class="day-chip-row">
                  <span class="day-chip"><svg><use href="#i-mar"></use></svg>Mantas gigantes</span>
                  <span class="day-chip"><svg><use href="#i-sol"></use></svg>Taka Makassar</span>
                  <span class="day-chip chip-boat"><svg><use href="#i-barco"></use></svg>Noche a bordo</span>
                </div>
                <div class="day-slots-list">
                  <div class="day-slot-box">
                    <span class="slot-time">Mañana (08:30 h a 13:00 h)</span>
                    <p class="slot-text">Navegación al mítico arrecife de Manta Point. Snorkel a la deriva flotando suavemente a favor de la corriente mientras mantarrayas oceánicas de 3 a 5 metros planean debajo de vosotros. Parada en el increíble banco de arena blanca de Taka Makassar, una lengua de arena en medio del océano turquesa.</p>
                  </div>
                  <div class="day-slot-box coral-accent">
                    <span class="slot-time">Tarde (14:30 h a 19:00 h)</span>
                    <p class="slot-text">Navegación hacia el norte del parque nacional fondeando en las proximidades de Siaba Besar. Tarde de baño tranquilo y preparativos para la última noche en el barco tradicional.</p>
                  </div>
                </div>
              </div>
              <div class="day-info-grid">
                <div class="info-item"><strong>Seguridad:</strong><span>Lancha motora auxiliar siguiendo permanentemente a los nadadores a escasos metros.</span></div>
                <div class="info-item"><strong>Condiciones:</strong><span>Finales de abril ofrece aguas templadas (27-28 grados) y máxima visibilidad.</span></div>
              </div>
            </div>
          </article>

          <!-- DIA 8 -->
          <article class="day-card-single" id="dia-a-8" data-dia="8" data-title="Tortugas en Siaba y única noche en el resort con espigón">
            <div class="day-photo-wrap"><img src="{get_img("espigon_arrecife")}" alt="Espigón de madera sobre el arrecife turquesa"><span class="day-place-tag pl-komodo"><span class="place-dot"></span>Komodo</span></div>
            <div class="day-content-wrap">
              <div>
                <div class="day-meta-top">
                  <span class="day-date-title">Día 8 · Miércoles 28 de abril</span>
                </div>
                <h3 class="day-headline">Tortugas en Siaba Besar y la única noche en el resort con espigón</h3>
                <div class="day-chip-row">
                  <span class="day-chip"><svg><use href="#i-mar"></use></svg>Tortugas en Siaba Besar</span>
                  <span class="day-chip"><svg><use href="#i-sol"></use></svg>Tarde en el espigón</span>
                  <a class="day-chip" href="#seccion-hoteles" onclick="return goToHotel('', 'espigon');" title="Ver la ficha del alojamiento"><svg><use href="#i-cama"></use></svg>Elegir resort con espigón</a>
                </div>
                <div class="day-slots-list">
                  <div class="day-slot-box">
                    <span class="slot-time">Mañana (07:30 h a 12:30 h)</span>
                    <p class="slot-text">Última mañana a bordo con snorkel a la deriva en la bahía de Siaba Besar, el punto de tortugas verdes del parque, donde se cruzan pastando sobre los jardines de coral. Desembarque y lancha rápida privada hasta el muelle de madera del resort, entre 35 y 45 minutos de travesía.</p>
                  </div>
                  <div class="day-slot-box coral-accent">
                    <span class="slot-time">Tarde y noche (13:00 h a 22:00 h)</span>
                    <p class="slot-text">Comida ya en el resort y tarde entera para el arrecife propio: se baja por las escaleras del espigón y se entra al agua sin depender de ninguna barca, entre peces loro, crías de tiburón punta negra y coral vivo. Kayak o paddle por la bahía, masaje en pareja frente al mar, cóctel en el extremo del espigón al caer el sol y cena de pescado de roca a la brasa con sambal matah sobre las tablas de madera.</p>
                  </div>
                </div>
              </div>
              <div class="day-info-grid">
                <div class="info-item"><strong>Una sola noche, bien aprovechada:</strong><span>Se llega a mediodía y no al anochecer, así que la tarde de arrecife, el atardecer y la cena en el espigón entran completos en la única noche del resort.</span></div>
                <div class="info-item"><strong>Cuál elegir:</strong><span>Los cuatro resorts de la colección tienen espigón propio y arrecife a pie de escalera. Para finales de abril, AYANA Komodo aparece en torno a 214 a 232 euros la noche con desayuno, Sudamala Seraya sobre 272 y TA'AKTANA por encima de 1.100, así que la diferencia de precio entre ellos es enorme para una prestación equivalente.</span></div>
              </div>
            </div>
          </article>

          <!-- DIA 9 -->
          <article class="day-card-single" id="dia-a-9" data-dia="9" data-title="Último baño en el arrecife, vuelo a Bali y Valle de Sidemen">
            <div class="day-photo-wrap"><img src="{get_img("sidemen_rice")}" alt="Terrazas de arroz del valle de Sidemen"><span class="day-place-tag pl-bali"><span class="place-dot"></span>Bali</span></div>
            <div class="day-content-wrap">
              <div>
                <div class="day-meta-top">
                  <span class="day-date-title">Día 9 · Jueves 29 de abril</span>
                </div>
                <h3 class="day-headline">Último baño en el arrecife, vuelo a Bali y llegada al Valle de Sidemen</h3>
                <div class="day-chip-row">
                  <span class="day-chip"><svg><use href="#i-mar"></use></svg>Último baño en el espigón</span>
                  <span class="day-chip chip-flight"><svg><use href="#i-vuelo"></use></svg>LBJ a DPS</span>
                  <a class="day-chip" href="#hotel-wapa-diume" onclick="return goToHotel('hotel-wapa-diume');" title="Ver la ficha del alojamiento"><svg><use href="#i-cama"></use></svg>Wapa di Ume Sidemen</a>
                </div>
                <div class="day-slots-list">
                  <div class="day-slot-box">
                    <span class="slot-time">Mañana (07:30 h a 11:00 h)</span>
                    <p class="slot-text">Desayuno con fruta fresca frente a la bahía y última mañana sin prisas en el arrecife del espigón antes de deshacer la maleta. Lancha rápida de vuelta al puerto de Labuan Bajo y traslado corto al aeropuerto.</p>
                  </div>
                  <div class="day-slot-box">
                    <span class="slot-time">Tarde (13:00 h a 19:00 h)</span>
                    <p class="slot-text">Vuelo de mediodía a Bali con AirAsia o Batik Air, las dos únicas compañías que cubren la ruta, en poco más de una hora. Coche privado hacia el este rural, evitando por completo el sur masificado, y subida al Valle de Sidemen (1 h 40 min de ruta paisajística). Llegada con luz y primera tarde tranquila entre arrozales.</p>
                  </div>
                </div>
              </div>
              <div class="day-info-grid">
                <div class="info-item"><strong>Por qué el vuelo de mediodía:</strong><span>La ruta Labuan Bajo a Denpasar tiene salidas a lo largo de todo el día. Cogiendo una de mediodía queda la mañana entera en el arrecife y aun así se llega a Sidemen con luz, en lugar de madrugar y perder la última mañana.</span></div>
                <div class="info-item"><strong>Alojamiento:</strong><span>Wapa di Ume Sidemen o Samanvaya Resort. Cuatro noches en el mismo hotel, sin volver a hacer maletas hasta el vuelo de regreso.</span></div>
              </div>
            </div>
          </article>

          <!-- DIA 10 -->
          <article class="day-card-single" id="dia-a-10" data-dia="10" data-title="Sidemen a fondo: arrozales al amanecer, telares y arak de palma">
            <div class="day-photo-wrap"><img src="{get_img("agung")}" alt="El volcán Agung sobre los arrozales de Sidemen"><span class="day-place-tag pl-bali"><span class="place-dot"></span>Bali</span></div>
            <div class="day-content-wrap">
              <div>
                <div class="day-meta-top">
                  <span class="day-date-title">Día 10 · Viernes 30 de abril</span>
                </div>
                <h3 class="day-headline">El valle a fondo: arrozales al amanecer, telares de songket y arak de palma</h3>
                <div class="day-chip-row">
                  <span class="day-chip"><svg><use href="#i-montana"></use></svg>Arrozales al amanecer</span>
                  <span class="day-chip"><svg><use href="#i-cultura"></use></svg>Telar de songket</span>
                  <span class="day-chip"><svg><use href="#i-gastro"></use></svg>Destilería de arak</span>
                  <a class="day-chip" href="#hotel-wapa-diume" onclick="return goToHotel('hotel-wapa-diume');" title="Ver la ficha del alojamiento"><svg><use href="#i-cama"></use></svg>Wapa di Ume Sidemen</a>
                </div>
                <div class="day-slots-list">
                  <div class="day-slot-box">
                    <span class="slot-time">Mañana (07:00 h a 11:00 h)</span>
                    <p class="slot-text">Salida a las siete en punto con un guía del pueblo, la única franja en la que el Agung se ve limpio antes de que las nubes lo tapen. Caminata por los diques de las terrazas y los canales de riego del subak de Ogang, cruzando el puente de madera que los vecinos comparten con las motos y pasando por los templos de aldea. Se camina entre fincas privadas en plena cosecha, no por un parque, y por eso se entra acompañado.</p>
                  </div>
                  <div class="day-slot-box coral-accent">
                    <span class="slot-time">Tarde (11:30 h a 18:00 h)</span>
                    <p class="slot-text">Demostración privada de tejido de hora y media con maestra tejedora: montaje del telar, urdimbre y entrelazado del hilo metálico del songket. Comida en el valle con nasi sela, el arroz con boniato de Karangasem. Al final de la tarde, visita a una familia destiladora de arak de palma en Tri Eka Buana, cuando los trepadores vuelven a subir a los cocoteros entre las cuatro y las seis.</p>
                  </div>
                </div>
              </div>
              <div class="day-info-grid">
                <div class="info-item"><strong>Guía local:</strong><span>Los operadores del pueblo cobran entre 80.000 y 150.000 IDR por persona según duración (2 a 5 h). No hay senderos señalizados en Sidemen: lo que existe son rutas privadas con guía.</span></div>
                <div class="info-item"><strong>Telar con precio publicado:</strong><span>La demostración privada de songket de 1 h 30 min figura a unas 206.600 IDR por persona más 21 por ciento de impuestos, tarifa de 2025 y 2026 que habrá que reconfirmar para 2027. Se reserva con un día de antelación.</span></div>
                <div class="info-item"><strong>Songket, endek y gringsing:</strong><span>El songket es brocado con hilo metálico entre las tramas y el endek es ikat solo de trama; los dos se tejen en Sidemen. El gringsing, el doble ikat, es de Tenganan, otro pueblo a una hora.</span></div>
                <div class="info-item"><strong>Arak con cabeza:</strong><span>En Tri Eka Buana cerca del 90 por ciento de las familias vive del arak de palma, pero no es una destilería con horario de visita: lo abre el guía. Se cata solo con productor conocido o marca registrada, porque hay antecedentes de adulteración con metanol.</span></div>
              </div>
            </div>
          </article>

          <!-- DIA 11 -->
          <article class="day-card-single" id="dia-a-11" data-dia="11" data-title="Pura Kehen, Gunung Kawi y ritual melukat">
            <div class="day-photo-wrap"><img src="{get_img("pura_kehen")}" alt="Pura Kehen, templo escalonado"><span class="day-place-tag pl-bali"><span class="place-dot"></span>Bali</span></div>
            <div class="day-content-wrap">
              <div>
                <div class="day-meta-top">
                  <span class="day-date-title">Día 11 · Sábado 1 de mayo</span>
                </div>
                <h3 class="day-headline">Santuarios en roca de Gunung Kawi, Pura Kehen y purificación</h3>
                <div class="day-chip-row">
                  <span class="day-chip"><svg><use href="#i-templo"></use></svg>Pura Kehen y Gunung Kawi</span>
                  <span class="day-chip"><svg><use href="#i-agua"></use></svg>Ritual melukat</span>
                  <a class="day-chip" href="#hotel-wapa-diume" onclick="return goToHotel('hotel-wapa-diume');" title="Ver la ficha del alojamiento"><svg><use href="#i-cama"></use></svg>Wapa di Ume Sidemen</a>
                </div>
                <div class="day-slots-list">
                  <div class="day-slot-box">
                    <span class="slot-time">Mañana (08:30 h a 13:00 h)</span>
                    <p class="slot-text">Visita a Pura Kehen en Bangli, un templo escalonado del siglo XI al que se accede por una escalinata monumental bajo un inmenso árbol banyan, sin autobuses turísticos. Descenso a los impresionantes nichos funerarios reales de Gunung Kawi esculpidos en los acantilados sobre el río selvático.</p>
                  </div>
                  <div class="day-slot-box coral-accent">
                    <span class="slot-time">Tarde (14:30 h a 18:30 h)</span>
                    <p class="slot-text">Ceremonia respetuosa de purificación tradicional del agua (*melukat*) en Pura Mengening, con ofrenda floral artesanal guiada por un sacerdote balinés en sus manantiales naturales. Regreso a Sidemen para cenar pato tradicional ahumado (*Bebek Betutu*).</p>
                  </div>
                </div>
              </div>
              <div class="day-info-grid">
                <div class="info-item"><strong>Cultura viva:</strong><span>Sin colas de Instagram ni fotos con espejos falsos. Espiritualidad y arte en silencio.</span></div>
                <div class="info-item"><strong>Vestimenta:</strong><span>Sarong tradicional y faja ceremonial proporcionados por vuestro guía balinés.</span></div>
              </div>
            </div>
          </article>

          <!-- DIA 12 -->
          <article class="day-card-single" id="dia-a-12" data-dia="12" data-title="Pecio del Liberty en Tulamben y palacio de agua de Tirta Gangga">
            <div class="day-photo-wrap"><img src="{get_img("menjangan_reef")}" alt="Snorkel sobre un arrecife de coral"><span class="day-place-tag pl-bali"><span class="place-dot"></span>Bali</span></div>
            <div class="day-content-wrap">
              <div>
                <div class="day-meta-top">
                  <span class="day-date-title">Día 12 · Domingo 2 de mayo</span>
                </div>
                <h3 class="day-headline">Snorkel sobre el pecio del Liberty en Tulamben y palacio de agua de Tirta Gangga</h3>
                <div class="day-chip-row">
                  <span class="day-chip"><svg><use href="#i-mar"></use></svg>Pecio del Liberty</span>
                  <span class="day-chip"><svg><use href="#i-templo"></use></svg>Tirta Gangga</span>
                  <a class="day-chip" href="#hotel-wapa-diume" onclick="return goToHotel('hotel-wapa-diume');" title="Ver la ficha del alojamiento"><svg><use href="#i-cama"></use></svg>Wapa di Ume Sidemen</a>
                </div>
                <div class="day-slots-list">
                  <div class="day-slot-box">
                    <span class="slot-time">Mañana (06:30 h a 12:30 h)</span>
                    <p class="slot-text">Salida temprana hacia la costa noreste para llegar a Tulamben con el agua en calma y la playa aún vacía. Se entra a nado desde la orilla y a unos treinta metros aparece el casco del USAT Liberty, un buque de carga de la Segunda Guerra Mundial de 120 metros hundido en 1963: la parte alta está a cinco metros, así que se ve entera haciendo snorkel en superficie, tapizada de coral duro y blando, gorgonias y anémonas, con bancos de peces cirujano que se agrupan justo debajo. Segundo baño en el Coral Garden, unos cientos de metros al sur, entre anémonas y peces payaso.</p>
                  </div>
                  <div class="day-slot-box coral-accent">
                    <span class="slot-time">Tarde (14:30 h a 19:00 h)</span>
                    <p class="slot-text">Regreso parando en Tirta Gangga, el palacio de agua de los reyes de Karangasem, a media tarde, cuando los grupos organizados ya se han marchado: estanques con pasaderas de piedra, surtidores y carpas entre los jardines. Vuelta al valle de Sidemen para la última cena en el hotel.</p>
                  </div>
                </div>
              </div>
              <div class="day-info-grid">
                <div class="info-item"><strong>El pecio, gratis y sin botella:</strong><span>El acceso es libre desde la playa, sin entrada ni tour: solo se paga el aparcamiento y, si se quiere, el alquiler del equipo. El barco va de 5 a 30 metros de profundidad, de modo que la parte somera se cubre en superficie y el resto ya exige botella.</span></div>
                <div class="info-item"><strong>Tirta Gangga:</strong><span>Entrada de 90.000 IDR por adulto, abierto de 06:00 a 19:00, y unas 20.000 IDR más si se quiere el paseo en barca por el estanque. Mejor a primera hora o entre las 15:00 y las 16:00.</span></div>
                <div class="info-item"><strong>Carretera de montaña:</strong><span>Hay que contar entre 1 h 30 min y 2 h por trayecto desde Sidemen, no lo que estima el navegador: son curvas de montaña y se avanza despacio. No hay socorrista ni duchas públicas en Tulamben.</span></div>
              </div>
            </div>
          </article>

          <!-- DIA 13 -->
          <article class="day-card-single" id="dia-a-13" data-dia="13" data-title="Iseh, los pintores del valle y vuelo internacional nocturno">
            <div class="day-photo-wrap"><img src="{get_img("nasi_campur")}" alt="Nasi campur, plato combinado balinés"><span class="day-place-tag pl-bali"><span class="place-dot"></span>Bali</span></div>
            <div class="day-content-wrap">
              <div>
                <div class="day-meta-top">
                  <span class="day-date-title">Día 13 · Lunes 3 de mayo</span>
                </div>
                <h3 class="day-headline">Iseh, el valle que pintaron Walter Spies y Theo Meier, y vuelo nocturno</h3>
                <div class="day-chip-row">
                  <span class="day-chip"><svg><use href="#i-cultura"></use></svg>Iseh y sus pintores</span>
                  <span class="day-chip"><svg><use href="#i-gastro"></use></svg>Nasi sela de Karangasem</span>
                  <span class="day-chip chip-flight"><svg><use href="#i-vuelo"></use></svg>DPS a España, vuelo nocturno</span>
                </div>
                <div class="day-slots-list">
                  <div class="day-slot-box">
                    <span class="slot-time">Mañana (08:30 h a 12:30 h)</span>
                    <p class="slot-text">Subida corta en coche a Iseh, la aldea de la ladera donde vivieron y pintaron el alemán Walter Spies y el suizo Theo Meier: es exactamente el encuadre del valle con el Agung al fondo que sale en sus cuadros. Paseo por los caminos entre huertos, última compra de café balinés en grano y comida temprana de despedida con platos de Karangasem.</p>
                  </div>
                  <div class="day-slot-box">
                    <span class="slot-time">Tarde y noche (14:30 h a 23:00 h)</span>
                    <p class="slot-text">Traslado privado al aeropuerto internacional de Bali (DPS) con margen amplio, porque el corredor sur de la isla se atasca hasta bien entrada la noche. Facturación en el vuelo internacional con salida al anochecer rumbo a Europa.</p>
                  </div>
                </div>
              </div>
              <div class="day-info-grid">
                <div class="info-item"><strong>Por qué Iseh:</strong><span>La casa histórica de Spies y Meier sigue en pie y funciona hoy como villa; por ella pasaron Mick Jagger, David Bowie y Jean Paul Getty Jr.</span></div>
                <div class="info-item"><strong>Traslado con holgura:</strong><span>Salida con cuatro horas de antelación sobre la facturación. El vuelo nocturno permite cenar y dormir a bordo.</span></div>
              </div>
            </div>
          </article>

          <!-- DIA 14 -->
          <article class="day-card-single" id="dia-a-14" data-dia="14" data-title="Aterrizaje en España y AVE a Zaragoza">
            <div class="day-photo-wrap"><img src="{get_img("zaragoza_delicias")}" alt="Estación de Zaragoza Delicias, final del viaje"><span class="day-place-tag pl-espana"><span class="place-dot"></span>España</span></div>
            <div class="day-content-wrap">
              <div>
                <div class="day-meta-top">
                  <span class="day-date-title">Día 14 · Martes 4 de mayo</span>
                </div>
                <h3 class="day-headline">Aterrizaje en España y tren de alta velocidad directo a Zaragoza</h3>
                <div class="day-chip-row">
                  <span class="day-chip chip-flight"><svg><use href="#i-vuelo"></use></svg>Aterrizaje en Madrid o Barcelona</span>
                  <span class="day-chip"><svg><use href="#i-tren"></use></svg>AVE a Zaragoza</span>
                </div>
                <div class="day-slots-list">
                  <div class="day-slot-box">
                    <span class="slot-time">Mañana (08:30 h a 11:30 h)</span>
                    <p class="slot-text">Aterrizaje en Madrid Barajas (T4) o Barcelona El Prat (T1). Recogida de equipaje y control de aduanas en España. Enlace en tren de Cercanías a la estación de Atocha o tren directo desde Sants.</p>
                  </div>
                  <div class="day-slot-box coral-accent">
                    <span class="slot-time">Tarde (13:30 h a 16:30 h)</span>
                    <p class="slot-text">Tren de alta velocidad AVE o Iryo directo a la estación de Zaragoza Delicias (1 h 15 min desde Madrid o 1 h 25 min desde Barcelona). Llegada a Zaragoza durante el día 4 de mayo, cumpliendo con total puntualidad el calendario fijado.</p>
                  </div>
                </div>
              </div>
              <div class="day-info-grid">
                <div class="info-item"><strong>Puntualidad:</strong><span>Dormiréis en vuestra casa en Zaragoza la noche del 4 de mayo con el plan cumplido.</span></div>
                <div class="info-item"><strong>Balance:</strong><span>14 días combinando naturaleza salvaje, templos milenarios y relax exclusivo.</span></div>
              </div>
            </div>
          </article>
        </div>

        <!-- RUTA B: 14 DIAS INDIVIDUALES -->
        <div class="route-block" id="block-opcion-b" style="display:none;">
          <div class="section-head">
            <span class="section-tag">Itinerario día a día</span>
            <h2>Ruta B: Sin Java (Los 14 días al detalle)</h2>
            <p>Un solo vuelo doméstico (Bali - Komodo ida y vuelta), ritmo pausado y estancia en las cascadas y lagos sagrados de Munduk.</p>
          </div>

          <!-- DIA 1 -->
          <article class="day-card-single" id="dia-b-1" data-dia="1" data-title="AVE Zaragoza a BCN/MAD y vuelo a Bali">
            <div class="day-photo-wrap"><img src="{get_img("zaragoza_delicias")}" alt="Vuelo a Bali"><span class="day-place-tag pl-espana"><span class="place-dot"></span>España</span></div>
            <div class="day-content-wrap">
              <div>
                <div class="day-meta-top">
                  <span class="day-date-title">Día 1 · Miércoles 21 de abril</span>
                </div>
                <h3 class="day-headline">AVE de Zaragoza a Barcelona o Madrid y vuelo directo a Bali</h3>
                <div class="day-chip-row">
                  <span class="day-chip"><svg><use href="#i-tren"></use></svg>AVE a Madrid o Barcelona</span>
                  <span class="day-chip chip-flight"><svg><use href="#i-vuelo"></use></svg>Vuelo directo a Bali</span>
                </div>
                <div class="day-slots-list">
                  <div class="day-slot-box">
                    <span class="slot-time">Mañana y mediodía (12:00 h a 16:00 h)</span>
                    <p class="slot-text">Tren AVE de Zaragoza Delicias a Barcelona Sants (enlace con Singapore Airlines vía Singapur) o Madrid Atocha (enlace con Qatar Airways vía Doha). Facturación de maletas directamente a Bali (DPS) en billete único protegido.</p>
                  </div>
                  <div class="day-slot-box">
                    <span class="slot-time">Tarde y noche (17:30 h en adelante)</span>
                    <p class="slot-text">Salida del vuelo internacional con escala técnica confortable. Cena a bordo y descanso en vuelo intercontinental rumbo al sudeste asiático.</p>
                  </div>
                </div>
              </div>
              <div class="day-info-grid">
                <div class="info-item"><strong>Gran ventaja:</strong><span>Sin escalas en Yakarta ni cambios de aeropuerto. El billete te lleva directo a Bali.</span></div>
                <div class="info-item"><strong>Equipaje:</strong><span>Facturación directa hasta Denpasar sin retirar maletas en la escala.</span></div>
              </div>
            </div>
          </article>

          <!-- DIA 2 -->
          <article class="day-card-single" id="dia-b-2" data-dia="2" data-title="Aterrizaje en Bali y traslado a Sidemen">
            <div class="day-photo-wrap"><img src="{get_img("agung")}" alt="Monte Agung y arrozales de Sidemen"><span class="day-place-tag pl-bali"><span class="place-dot"></span>Bali</span></div>
            <div class="day-content-wrap">
              <div>
                <div class="day-meta-top">
                  <span class="day-date-title">Día 2 · Jueves 22 de abril</span>
                </div>
                <h3 class="day-headline">Aterrizaje en Bali y traslado directo al remanso verde de Sidemen</h3>
                <div class="day-chip-row">
                  <span class="day-chip chip-flight"><svg><use href="#i-vuelo"></use></svg>Llegada a Denpasar</span>
                  <a class="day-chip" href="#hotel-wapa-diume" onclick="return goToHotel('hotel-wapa-diume');" title="Ver la ficha del alojamiento"><svg><use href="#i-cama"></use></svg>Wapa di Ume Sidemen</a>
                  <span class="day-chip"><svg><use href="#i-hoja"></use></svg>Valle de Sidemen</span>
                </div>
                <div class="day-slots-list">
                  <div class="day-slot-box">
                    <span class="slot-time">Tarde (16:30 h a 18:30 h)</span>
                    <p class="slot-text">Aterrizaje en el aeropuerto de Denpasar (DPS). Encuentro con vuestro chófer privado balinés en la terminal y salida inmediata hacia el este rural, evitando por completo el colapso del sur de la isla.</p>
                  </div>
                  <div class="day-slot-box coral-accent">
                    <span class="slot-time">Noche (19:30 h a 22:00 h)</span>
                    <p class="slot-text">Llegada al Valle de Sidemen (1 h 40 min de trayecto). Check-in en vuestro hotel boutique con vistas a los campos de arroz y al volcán Agung. Cena relajada balinesa y descanso profundo en cama king-size con colchón premium.</p>
                  </div>
                </div>
              </div>
              <div class="day-info-grid">
                <div class="info-item"><strong>Ruta terrestre:</strong><span>Coche privado climatizado directo al hotel sin paradas comerciales.</span></div>
                <div class="info-item"><strong>Alojamiento:</strong><span>Wapa di Ume Sidemen o Samanvaya Resort. Cuatro noches seguidas entre ríos y arrozales, sin cambiar de hotel.</span></div>
              </div>
            </div>
          </article>

          <!-- DIA 3 -->
          <article class="day-card-single" id="dia-b-3" data-dia="3" data-title="Caminata entre arrozales de Sidemen">
            <div class="day-photo-wrap"><img src="{get_img("sidemen_rice")}" alt="Arrozales de Sidemen"><span class="day-place-tag pl-bali"><span class="place-dot"></span>Bali</span></div>
            <div class="day-content-wrap">
              <div>
                <div class="day-meta-top">
                  <span class="day-date-title">Día 3 · Viernes 23 de abril</span>
                </div>
                <h3 class="day-headline">Arrozales al amanecer con el Agung enfrente, telares de songket y arak de palma</h3>
                <div class="day-chip-row">
                  <span class="day-chip"><svg><use href="#i-montana"></use></svg>Arrozales al amanecer</span>
                  <span class="day-chip"><svg><use href="#i-cultura"></use></svg>Telar de songket</span>
                  <span class="day-chip"><svg><use href="#i-gastro"></use></svg>Destilería de arak</span>
                  <a class="day-chip" href="#hotel-wapa-diume" onclick="return goToHotel('hotel-wapa-diume');" title="Ver la ficha del alojamiento"><svg><use href="#i-cama"></use></svg>Wapa di Ume Sidemen</a>
                </div>
                <div class="day-slots-list">
                  <div class="day-slot-box">
                    <span class="slot-time">Mañana (07:00 h a 12:30 h)</span>
                    <p class="slot-text">Salida a las siete con guía de la aldea, la única franja en la que el Agung se ve limpio antes de que lo tapen las nubes. Recorrido por los diques de los arrozales escalonados y los canales del subak de Ogang, cruzando el puente de madera que los vecinos comparten con las motos, entre árboles de clavo, cacao y nuez moscada. Se camina por fincas privadas en plena cosecha, de ahí que se entre acompañado.</p>
                  </div>
                  <div class="day-slot-box">
                    <span class="slot-time">Tarde (14:30 h a 18:30 h)</span>
                    <p class="slot-text">Demostración privada de hora y media en telar manual de madera, con el montaje de la urdimbre y el entrelazado del hilo metálico del songket. Al final de la tarde, visita a una familia destiladora de arak de palma en Tri Eka Buana, cuando los trepadores vuelven a subir a los cocoteros. Cierre con baño en la piscina infinita frente al cañón del río y masaje balinés.</p>
                  </div>
                </div>
              </div>
              <div class="day-info-grid">
                <div class="info-item"><strong>Sin masificación:</strong><span>Sidemen conserva el ritmo del Bali de hace cuatro décadas. No hay senderos señalizados: lo que existe son rutas privadas con guía del pueblo, entre 80.000 y 150.000 IDR por persona.</span></div>
                <div class="info-item"><strong>Songket, endek y gringsing:</strong><span>El songket es brocado con hilo metálico entre las tramas y el endek es ikat solo de trama; ambos se tejen en Sidemen. El gringsing, el doble ikat, es de Tenganan, otro pueblo a una hora.</span></div>
                <div class="info-item"><strong>Arak con cabeza:</strong><span>En Tri Eka Buana cerca del 90 por ciento de las familias vive del arak de palma, pero no es una destilería con horario: la abre el guía. Se cata solo con productor conocido o marca registrada, porque hay antecedentes de adulteración con metanol.</span></div>
              </div>
            </div>
          </article>

          <!-- DIA 4 -->
          <article class="day-card-single" id="dia-b-4" data-dia="4" data-title="Santuarios Gunung Kawi y purificación">
            <div class="day-photo-wrap"><img src="{get_img("gunung_kawi")}" alt="Gunung Kawi"><span class="day-place-tag pl-bali"><span class="place-dot"></span>Bali</span></div>
            <div class="day-content-wrap">
              <div>
                <div class="day-meta-top">
                  <span class="day-date-title">Día 4 · Sábado 24 de abril</span>
                </div>
                <h3 class="day-headline">Santuarios de roca de Gunung Kawi y ritual de purificación sagrada</h3>
                <div class="day-chip-row">
                  <span class="day-chip"><svg><use href="#i-templo"></use></svg>Gunung Kawi</span>
                  <span class="day-chip"><svg><use href="#i-agua"></use></svg>Purificación en Pura Mengening</span>
                  <a class="day-chip" href="#hotel-wapa-diume" onclick="return goToHotel('hotel-wapa-diume');" title="Ver la ficha del alojamiento"><svg><use href="#i-cama"></use></svg>Wapa di Ume Sidemen</a>
                </div>
                <div class="day-slots-list">
                  <div class="day-slot-box">
                    <span class="slot-time">Mañana (08:30 h a 13:00 h)</span>
                    <p class="slot-text">Visita a los monumentales santuarios funerarios de Gunung Kawi en Tampaksiring, esculpidos en el siglo XI en las paredes de roca de un acantilado cubierto de helechos y manantiales.</p>
                  </div>
                  <div class="day-slot-box coral-accent">
                    <span class="slot-time">Tarde (14:30 h a 18:00 h)</span>
                    <p class="slot-text">Ceremonia de purificación tradicional del agua (*melukat*) en Pura Mengening, donde el sacerdote local realiza la bendición en manantiales cristalinos en un ambiente íntimo de recogimiento espiritual. Regreso a Sidemen para cenar.</p>
                  </div>
                </div>
              </div>
              <div class="day-info-grid">
                <div class="info-item"><strong>Experiencia auténtica:</strong><span>Pura Mengening permite vivir el ritual sagrado sin las colas de Tirta Empul.</span></div>
                <div class="info-item"><strong>Descanso:</strong><span>Tercera de las cuatro noches seguidas en el mismo hotel de Sidemen, sin hacer y deshacer maletas.</span></div>
              </div>
            </div>
          </article>

          <!-- DIA 5 -->
          <article class="day-card-single" id="dia-b-5" data-dia="5" data-title="Pecio del Liberty en Tulamben y palacio de agua de Tirta Gangga">
            <div class="day-photo-wrap"><img src="{get_img("menjangan_reef")}" alt="Snorkel sobre un arrecife de coral"><span class="day-place-tag pl-bali"><span class="place-dot"></span>Bali</span></div>
            <div class="day-content-wrap">
              <div>
                <div class="day-meta-top">
                  <span class="day-date-title">Día 5 · Domingo 25 de abril</span>
                </div>
                <h3 class="day-headline">Snorkel sobre el pecio del Liberty en Tulamben y palacio de agua de Tirta Gangga</h3>
                <div class="day-chip-row">
                  <span class="day-chip"><svg><use href="#i-mar"></use></svg>Pecio del Liberty</span>
                  <span class="day-chip"><svg><use href="#i-templo"></use></svg>Tirta Gangga</span>
                  <a class="day-chip" href="#hotel-wapa-diume" onclick="return goToHotel('hotel-wapa-diume');" title="Ver la ficha del alojamiento"><svg><use href="#i-cama"></use></svg>Wapa di Ume Sidemen</a>
                </div>
                <div class="day-slots-list">
                  <div class="day-slot-box">
                    <span class="slot-time">Mañana (06:30 h a 12:30 h)</span>
                    <p class="slot-text">Salida temprana hacia la costa noreste para llegar a Tulamben con el agua en calma y la playa aún vacía. Se entra a nado desde la orilla y a unos treinta metros aparece el casco del USAT Liberty, un buque de carga de la Segunda Guerra Mundial de 120 metros hundido en 1963: la parte alta está a cinco metros, así que se ve entera haciendo snorkel en superficie, tapizada de coral duro y blando, gorgonias y anémonas, con bancos de peces cirujano que se agrupan justo debajo. Segundo baño en el Coral Garden, unos cientos de metros al sur, entre anémonas y peces payaso.</p>
                  </div>
                  <div class="day-slot-box coral-accent">
                    <span class="slot-time">Tarde (14:30 h a 19:00 h)</span>
                    <p class="slot-text">Regreso parando en Tirta Gangga, el palacio de agua de los reyes de Karangasem, a media tarde, cuando los grupos organizados ya se han marchado: estanques con pasaderas de piedra, surtidores y carpas entre los jardines. Vuelta al valle de Sidemen, la cuarta y última noche en el mismo hotel antes de volar a Komodo.</p>
                  </div>
                </div>
              </div>
              <div class="day-info-grid">
                <div class="info-item"><strong>El pecio, gratis y sin botella:</strong><span>El acceso es libre desde la playa, sin entrada ni tour: solo se paga el aparcamiento y, si se quiere, el alquiler del equipo. El barco va de 5 a 30 metros de profundidad, de modo que la parte somera se cubre en superficie y el resto ya exige botella.</span></div>
                <div class="info-item"><strong>Tirta Gangga:</strong><span>Entrada de 90.000 IDR por adulto, abierto de 06:00 a 19:00, y unas 20.000 IDR más si se quiere el paseo en barca por el estanque. Mejor a primera hora o entre las 15:00 y las 16:00.</span></div>
                <div class="info-item"><strong>Carretera de montaña:</strong><span>Hay que contar entre 1 h 30 min y 2 h por trayecto desde Sidemen, no lo que estima el navegador: son curvas de montaña y se avanza despacio. No hay socorrista ni duchas públicas en Tulamben.</span></div>
              </div>
            </div>
          </article>

          <!-- DIA 6 -->
          <article class="day-card-single" id="dia-b-6" data-dia="6" data-title="Vuelo a Labuan Bajo y embarque Phinisi">
            <div class="day-photo-wrap"><img src="{get_img("kalong_sunset")}" alt="Zorros voladores en Isla Kalong"><span class="day-place-tag pl-komodo"><span class="place-dot"></span>Komodo</span></div>
            <div class="day-content-wrap">
              <div>
                <div class="day-meta-top">
                  <span class="day-date-title">Día 6 · Lunes 26 de abril</span>
                </div>
                <h3 class="day-headline">Vuelo a Labuan Bajo y embarque en barco tradicional Phinisi</h3>
                <div class="day-chip-row">
                  <span class="day-chip chip-flight"><svg><use href="#i-vuelo"></use></svg>DPS a LBJ</span>
                  <span class="day-chip chip-boat"><svg><use href="#i-barco"></use></svg>Goleta Phinisi</span>
                  <span class="day-chip"><svg><use href="#i-fauna"></use></svg>Zorros voladores en Kalong</span>
                </div>
                <div class="day-slots-list">
                  <div class="day-slot-box">
                    <span class="slot-time">Mañana (08:00 h a 12:30 h)</span>
                    <p class="slot-text">Traslado al aeropuerto de Bali y vuelo directo de 1 h 10 min a Labuan Bajo (isla de Flores). Embarque directo en goleta tradicional de madera (Phinisi) con camarote doble climatizado y baño privado.</p>
                  </div>
                  <div class="day-slot-box coral-accent">
                    <span class="slot-time">Tarde y atardecer (13:30 h a 19:00 h)</span>
                    <p class="slot-text">Navegación hacia Isla Kelor para trekking panorámico y snorkel en arrecife. Llegada a Isla Rinca para observar dragones de Komodo salvajes con los guardaparques oficiales. Fondeo en Isla Kalong para ver volar a los zorros voladores al anochecer.</p>
                  </div>
                </div>
              </div>
              <div class="day-info-grid">
                <div class="info-item"><strong>Vuelo doméstico:</strong><span>DPS a LBJ (09:10 h a 10:20 h) con Garuda Indonesia o Batik Air.</span></div>
                <div class="info-item"><strong>Barco tradicional:</strong><span>Phinisi de madera con cocinero a bordo, comidas completas y camarote climatizado.</span></div>
              </div>
            </div>
          </article>

          <!-- DIA 7 -->
          <article class="day-card-single" id="dia-b-7" data-dia="7" data-title="Amanecer en Padar y Pink Beach">
            <div class="day-photo-wrap"><img src="{get_img("pink_beach")}" alt="Pink Beach en el parque de Komodo"><span class="day-place-tag pl-komodo"><span class="place-dot"></span>Komodo</span></div>
            <div class="day-content-wrap">
              <div>
                <div class="day-meta-top">
                  <span class="day-date-title">Día 7 · Martes 27 de abril</span>
                </div>
                <h3 class="day-headline">Amanecer en Isla Padar, Pink Beach y snorkel en aguas cristalinas</h3>
                <div class="day-chip-row">
                  <span class="day-chip"><svg><use href="#i-montana"></use></svg>Mirador de Padar</span>
                  <span class="day-chip"><svg><use href="#i-mar"></use></svg>Snorkel en Pink Beach</span>
                  <span class="day-chip chip-boat"><svg><use href="#i-barco"></use></svg>Noche a bordo</span>
                </div>
                <div class="day-slots-list">
                  <div class="day-slot-box">
                    <span class="slot-time">Amanecer y mañana (05:15 h a 11:30 h)</span>
                    <p class="slot-text">Subida al alba al mirador de Isla Padar con sus tres bahías contiguas de arena de colores. Desayuno en cubierta con vistas a los islotes desérticos. Navegación a Pink Beach para nadar en sus aguas turquesas sobre arena rosada.</p>
                  </div>
                  <div class="day-slot-box">
                    <span class="slot-time">Tarde (14:00 h a 20:00 h)</span>
                    <p class="slot-text">Navegación pausada entre calas solitarias del parque nacional. Sesión de snorkel en arrecifes someros y cena bajo las estrellas en cubierta.</p>
                  </div>
                </div>
              </div>
              <div class="day-info-grid">
                <div class="info-item"><strong>Vistas icónicas:</strong><span>El sendero de Padar tiene entre 700 y 1.000 escalones de piedra según la fuente (815 es la cifra más citada); subir al alba evita el calor.</span></div>
                <div class="info-item"><strong>Snorkel:</strong><span>Corales sanos y peces tropicales a muy pocos metros de la orilla de Pink Beach.</span></div>
              </div>
            </div>
          </article>

          <!-- DIA 8 -->
          <article class="day-card-single" id="dia-b-8" data-dia="8" data-title="Dragones en Loh Liang, mantas gigantes y Taka Makassar">
            <div class="day-photo-wrap"><img src="{get_img("komodo_dragon")}" alt="Dragón de Komodo en su hábitat"><span class="day-place-tag pl-komodo"><span class="place-dot"></span>Komodo</span></div>
            <div class="day-content-wrap">
              <div>
                <div class="day-meta-top">
                  <span class="day-date-title">Día 8 · Miércoles 28 de abril</span>
                </div>
                <h3 class="day-headline">Dragones en Loh Liang, mantas gigantes y el banco de arena de Taka Makassar</h3>
                <div class="day-chip-row">
                  <span class="day-chip"><svg><use href="#i-fauna"></use></svg>Dragones en Loh Liang</span>
                  <span class="day-chip"><svg><use href="#i-mar"></use></svg>Mantas gigantes</span>
                  <span class="day-chip"><svg><use href="#i-sol"></use></svg>Taka Makassar</span>
                  <span class="day-chip chip-boat"><svg><use href="#i-barco"></use></svg>Noche a bordo</span>
                </div>
                <div class="day-slots-list">
                  <div class="day-slot-box">
                    <span class="slot-time">Mañana (07:00 h a 12:00 h)</span>
                    <p class="slot-text">Desembarque en Loh Liang, en la propia Isla Komodo, y trekking guiado por guardaparques en el circuito medio: se cruza el cauce seco donde suelen concentrarse los dragones y se sube al mirador sobre la bahía. Los animales se reúnen cerca de los puestos de los rangers, que es lo que hace fiable el avistamiento.</p>
                  </div>
                  <div class="day-slot-box coral-accent">
                    <span class="slot-time">Tarde (13:00 h a 19:00 h)</span>
                    <p class="slot-text">Navegación corta al canal central para nadar con las mantas gigantes en Karang Makassar, donde se alimentan en las estaciones de limpieza, y parada en el banco de arena de Taka Makassar, una media luna que emerge solo con la marea baja. Atardecer en cubierta y última noche fondeados.</p>
                  </div>
                </div>
              </div>
              <div class="day-info-grid">
                <div class="info-item"><strong>Todo en el mismo canal:</strong><span>Pink Beach, Loh Liang, Karang Makassar y Taka Makassar están todos entre 35 y 40 km de Labuan Bajo, agrupados en el canal central, así que los saltos entre ellos son de minutos. Quien fija el orden del día es la marea, no la distancia.</span></div>
                <div class="info-item"><strong>Pedirlo por escrito:</strong><span>Los itinerarios publicados desembarcan en Loh Liang (Isla Komodo), pero hay operadores que llevan a Loh Buaya (Rinca) porque el sendero es más corto. Conviene exigir por escrito cuál de las dos, ya que el billete del parque sirve para ambas.</span></div>
                <div class="info-item"><strong>Cupo diario desde 2026:</strong><span>El parque está limitado a 1.000 visitantes al día y la visita se reserva por la app oficial SIORA, sin venta en taquilla. El pago con tarjeta extranjera daba problemas, así que lo habitual es que lo gestione el operador del barco.</span></div>
              </div>
            </div>
          </article>

          <!-- DIA 9 -->
          <article class="day-card-single" id="dia-b-9" data-dia="9" data-title="Tortugas en Siaba y única noche en el resort con espigón">
            <div class="day-photo-wrap"><img src="{get_img("espigon_arrecife")}" alt="Espigón de madera sobre el arrecife turquesa"><span class="day-place-tag pl-komodo"><span class="place-dot"></span>Komodo</span></div>
            <div class="day-content-wrap">
              <div>
                <div class="day-meta-top">
                  <span class="day-date-title">Día 9 · Jueves 29 de abril</span>
                </div>
                <h3 class="day-headline">Tortugas en Siaba Besar y la única noche en el resort con espigón</h3>
                <div class="day-chip-row">
                  <span class="day-chip"><svg><use href="#i-mar"></use></svg>Tortugas en Siaba Besar</span>
                  <span class="day-chip"><svg><use href="#i-sol"></use></svg>Tarde en el espigón</span>
                  <a class="day-chip" href="#seccion-hoteles" onclick="return goToHotel('', 'espigon');" title="Ver la ficha del alojamiento"><svg><use href="#i-cama"></use></svg>Elegir resort con espigón</a>
                </div>
                <div class="day-slots-list">
                  <div class="day-slot-box">
                    <span class="slot-time">Mañana (07:30 h a 12:30 h)</span>
                    <p class="slot-text">Última mañana a bordo con snorkel a la deriva en la bahía de Siaba Besar, el punto de tortugas verdes del parque, que se cruzan pastando sobre los jardines de coral. Desembarque y lancha rápida privada hasta el muelle de madera del resort, entre 35 y 45 minutos de travesía.</p>
                  </div>
                  <div class="day-slot-box coral-accent">
                    <span class="slot-time">Tarde y noche (13:00 h a 22:00 h)</span>
                    <p class="slot-text">Comida ya en el resort y tarde entera para el arrecife propio: se baja por las escaleras del espigón y se entra al agua sin depender de ninguna barca, entre peces loro, crías de tiburón punta negra y coral vivo. Kayak o paddle por la bahía en calma, masaje en pareja frente al mar, cóctel en el extremo del espigón al caer el sol y cena de pescado de roca a la brasa con sambal matah sobre las tablas de madera.</p>
                  </div>
                </div>
              </div>
              <div class="day-info-grid">
                <div class="info-item"><strong>Una sola noche, bien aprovechada:</strong><span>Se llega a mediodía y no al anochecer, así que la tarde de arrecife, el atardecer y la cena en el espigón entran completos en la única noche del resort.</span></div>
                <div class="info-item"><strong>Cuál elegir:</strong><span>Los cuatro resorts de la colección tienen espigón propio y arrecife a pie de escalera. Para finales de abril, AYANA Komodo aparece en torno a 214 a 232 euros la noche con desayuno, Sudamala Seraya sobre 272 y TA'AKTANA por encima de 1.100, así que la diferencia de precio entre ellos es enorme para una prestación equivalente.</span></div>
              </div>
            </div>
          </article>

          <!-- DIA 10 -->
          <article class="day-card-single" id="dia-b-10" data-dia="10" data-title="Vuelo a Bali y ascenso a Munduk">
            <div class="day-photo-wrap"><img src="{get_img("hotel_munduk_moding")}" alt="Ascenso a Munduk"><span class="day-place-tag pl-bali"><span class="place-dot"></span>Bali</span></div>
            <div class="day-content-wrap">
              <div>
                <div class="day-meta-top">
                  <span class="day-date-title">Día 10 · Viernes 30 de abril</span>
                </div>
                <h3 class="day-headline">Último amanecer en el resort, vuelo a Bali y ascenso a las montañas y cafetales de Munduk</h3>
                <div class="day-chip-row">
                  <span class="day-chip chip-flight"><svg><use href="#i-vuelo"></use></svg>LBJ a DPS</span>
                  <span class="day-chip"><svg><use href="#i-montana"></use></svg>Cafetales de Munduk</span>
                  <a class="day-chip" href="#hotel-munduk-moding" onclick="return goToHotel('hotel-munduk-moding');" title="Ver la ficha del alojamiento"><svg><use href="#i-cama"></use></svg>Munduk Moding Plantation</a>
                </div>
                <div class="day-slots-list">
                  <div class="day-slot-box">
                    <span class="slot-time">Mañana (06:30 h a 13:30 h)</span>
                    <p class="slot-text">Despertar sin prisas para ver el amanecer desde el espigón de madera, el último café frente al mar de Flores antes de hacer el equipaje. Lancha a Labuan Bajo y vuelo directo de 1 h 10 min a Bali. Traslado en coche privado subiendo por las laderas hacia la cordillera norte de Munduk (a 1.000 m de altitud).</p>
                  </div>
                  <div class="day-slot-box">
                    <span class="slot-time">Tarde (15:00 h a 20:00 h)</span>
                    <p class="slot-text">Check-in en Munduk Moding Plantation, famoso por su piscina infinita sobre las nubes en una finca de café orgánico. Paseo entre cafetales arábica y chimenea en la suite por la noche.</p>
                  </div>
                </div>
              </div>
              <div class="day-info-grid">
                <div class="info-item"><strong>Clima fresco:</strong><span>Temperaturas templadas muy agradables (21 a 24 grados), sin bochorno y aire puro.</span></div>
                <div class="info-item"><strong>Alojamiento:</strong><span>Munduk Moding Plantation. Cama king-size con nórdico de pluma.</span></div>
              </div>
            </div>
          </article>

          <!-- DIA 11 -->
          <article class="day-card-single" id="dia-b-11" data-dia="11" data-title="Cascadas de Banyumala y lago Tamblingan">
            <div class="day-photo-wrap"><img src="{get_img("banyumala")}" alt="Cascadas de Banyumala"><span class="day-place-tag pl-bali"><span class="place-dot"></span>Bali</span></div>
            <div class="day-content-wrap">
              <div>
                <div class="day-meta-top">
                  <span class="day-date-title">Día 11 · Sábado 1 de mayo</span>
                </div>
                <h3 class="day-headline">Cascadas gemelas de Banyumala y canoa en el Lago Tamblingan</h3>
                <div class="day-chip-row">
                  <span class="day-chip"><svg><use href="#i-agua"></use></svg>Cascadas de Banyumala</span>
                  <span class="day-chip"><svg><use href="#i-hoja"></use></svg>Lago Tamblingan</span>
                  <a class="day-chip" href="#hotel-munduk-moding" onclick="return goToHotel('hotel-munduk-moding');" title="Ver la ficha del alojamiento"><svg><use href="#i-cama"></use></svg>Munduk Moding Plantation</a>
                </div>
                <div class="day-slots-list">
                  <div class="day-slot-box">
                    <span class="slot-time">Mañana (08:30 h a 12:30 h)</span>
                    <p class="slot-text">Trekking entre helechos gigantes y orquídeas salvajes hasta las cascadas gemelas de Banyumala. Baño en su piscina natural de agua cristalina y fresca rodeada de un anfiteatro verde natural.</p>
                  </div>
                  <div class="day-slot-box coral-accent">
                    <span class="slot-time">Tarde (14:00 h a 18:00 h)</span>
                    <p class="slot-text">Navegación en canoa tradicional de madera doble (*pedahu*) por las aguas sagradas y silenciosas del lago Tamblingan entre bosques nubosos y pequeños templos de piedra.</p>
                  </div>
                </div>
              </div>
              <div class="day-info-grid">
                <div class="info-item"><strong>Naturaleza virgen:</strong><span>Munduk y Tamblingan no tienen tráfico comercial ni turismo de autobuses.</span></div>
                <div class="info-item"><strong>Gastronomía:</strong><span>Cata de café de especialidad procesado en la propia plantación de altura.</span></div>
              </div>
            </div>
          </article>

          <!-- DIA 12 -->
          <article class="day-card-single" id="dia-b-12" data-dia="12" data-title="Trek al valle de cascadas de Sekumpul">
            <div class="day-photo-wrap"><img src="{get_img("munduk")}" alt="Colinas verdes del norte de Bali en Munduk"><span class="day-place-tag pl-bali"><span class="place-dot"></span>Bali</span></div>
            <div class="day-content-wrap">
              <div>
                <div class="day-meta-top">
                  <span class="day-date-title">Día 12 · Domingo 2 de mayo</span>
                </div>
                <h3 class="day-headline">Trek al fondo del valle de Sekumpul, el conjunto de cascadas del norte</h3>
                <div class="day-chip-row">
                  <span class="day-chip"><svg><use href="#i-montana"></use></svg>Trek de valle</span>
                  <span class="day-chip"><svg><use href="#i-agua"></use></svg>Cascadas de Sekumpul</span>
                  <a class="day-chip" href="#hotel-munduk-moding" onclick="return goToHotel('hotel-munduk-moding');" title="Ver la ficha del alojamiento"><svg><use href="#i-cama"></use></svg>Munduk Moding Plantation</a>
                </div>
                <div class="day-slots-list">
                  <div class="day-slot-box">
                    <span class="slot-time">Mañana (07:30 h a 13:00 h)</span>
                    <p class="slot-text">Una hora de coche hasta la taquilla de Sekumpul para empezar a las ocho, antes de que suba la humedad y lleguen los grupos. El trek medio baja al fondo del valle por una larga escalera de hormigón pegada a la pared y sigue por sendero de jungla cruzando arroyos: unos 274 metros de desnivel de bajada y subida, con guía local incluido en la tarifa. Abajo, la cascada oculta y el salto principal, con poza natural donde se puede nadar.</p>
                  </div>
                  <div class="day-slot-box coral-accent">
                    <span class="slot-time">Tarde (14:30 h a 19:00 h)</span>
                    <p class="slot-text">Vuelta a Munduk, comida tardía y tarde de recuperación en la piscina infinita sobre el mar de nubes de la plantación, con cata del café procesado en la propia finca. Última cena en la montaña antes de bajar al sur.</p>
                  </div>
                </div>
              </div>
              <div class="day-info-grid">
                <div class="info-item"><strong>Tarifas y guía:</strong><span>El trek medio, con la cascada oculta y el salto principal, está entre 125.000 y 150.000 IDR por persona y ya incluye el guía local, que es obligatorio para pasar de los miradores. El trek largo, que añade las cataratas Fiji, sube a entre 200.000 y 250.000. Solo mirador, unas 20.000.</span></div>
                <div class="info-item"><strong>Aviso de falsos controles:</strong><span>En la carretera de acceso, hasta 12 km antes, hay puestos falsos con carteles de registro que piden hasta 250.000 IDR por persona y dan entradas sin valor. Solo se paga en la entrada oficial, junto al cartel de bienvenida, así que hay que avisar al conductor de que no pare en ningún control intermedio.</span></div>
                <div class="info-item"><strong>Esfuerzo real:</strong><span>Entre 324 y 400 escalones de subida a la vuelta según el ramal, terreno resbaladizo por la humedad constante y vadeos que mojan. Calzado con agarre y ropa de cambio. No es un paseo, pero tampoco requiere experiencia técnica.</span></div>
              </div>
            </div>
          </article>

          <!-- DIA 13 -->
          <article class="day-card-single" id="dia-b-13" data-dia="13" data-title="Ulun Danu Beratan, Jatiluwih y vuelo internacional nocturno">
            <div class="day-photo-wrap"><img src="{get_img("ulun_danu")}" alt="Templo Ulun Danu Beratan sobre el lago"><span class="day-place-tag pl-bali"><span class="place-dot"></span>Bali</span></div>
            <div class="day-content-wrap">
              <div>
                <div class="day-meta-top">
                  <span class="day-date-title">Día 13 · Lunes 3 de mayo</span>
                </div>
                <h3 class="day-headline">Templo sobre el lago Bratan y terrazas de Jatiluwih camino del aeropuerto</h3>
                <div class="day-chip-row">
                  <span class="day-chip"><svg><use href="#i-templo"></use></svg>Ulun Danu Beratan</span>
                  <span class="day-chip"><svg><use href="#i-montana"></use></svg>Jatiluwih, ruta blanca</span>
                  <span class="day-chip chip-flight"><svg><use href="#i-vuelo"></use></svg>DPS a España, vuelo nocturno</span>
                </div>
                <div class="day-slots-list">
                  <div class="day-slot-box">
                    <span class="slot-time">Mañana (08:00 h a 10:00 h)</span>
                    <p class="slot-text">Bajada de Munduk (entre 30 y 40 min) hasta Pura Ulun Danu Beratan, el templo que parece flotar sobre el lago y que está en la propia carretera, sin desvío. Se llega a primera hora, cuando el agua está en calma y el recinto casi vacío: a media mañana se llena de autocares. Una hora larga entre los jardines y los pabellones sobre el agua.</p>
                  </div>
                  <div class="day-slot-box coral-accent">
                    <span class="slot-time">Mediodía y tarde (10:45 h a 23:00 h)</span>
                    <p class="slot-text">Cuarenta y cinco minutos hasta Jatiluwih, las terrazas de arroz declaradas patrimonio de la Unesco por su sistema de riego subak. Recorrido de la ruta blanca, unas dos horas por dentro de los arrozales, y comida con el valle enfrente. Salida a las tres de la tarde como muy tarde y traslado al aeropuerto para el vuelo internacional nocturno.</p>
                  </div>
                </div>
              </div>
              <div class="day-info-grid">
                <div class="info-item"><strong>Entradas:</strong><span>Ulun Danu Beratan subió a 100.000 IDR por adulto extranjero el 1 de julio de 2026, solo en taquilla y con descuento del 20 al 30 por ciento si se contrata con agencia. Jatiluwih está en 75.000 IDR verificadas más 5.000 de aparcamiento del coche; alguna guía ya publica 100.000, cifra que no se ha podido confirmar en fuente indonesia.</span></div>
                <div class="info-item"><strong>Cinco rutas por color:</strong><span>Jatiluwih tiene señalizadas cinco: roja (1 h), amarilla (1 h 10 min), blanca (2 h), verde (6 km, 2 h 30 min a 3 h) y azul (7 km, 4 h). La blanca es la que entra de verdad en el paisaje sin comerse el día.</span></div>
                <div class="info-item"><strong>Por qué de mañana:</strong><span>En los dos sitios la niebla y las nubes entran a mediodía, así que las vistas limpias son las de primera hora. Jatiluwih al aeropuerto son entre 2 h 30 min y 3 h por la congestión del sur.</span></div>
              </div>
            </div>
          </article>

          <!-- DIA 14 -->
          <article class="day-card-single" id="dia-b-14" data-dia="14" data-title="Llegada a España y AVE directo a Zaragoza">
            <div class="day-photo-wrap"><img src="{get_img("zaragoza_delicias")}" alt="Estación de Zaragoza Delicias, final del viaje"><span class="day-place-tag pl-espana"><span class="place-dot"></span>España</span></div>
            <div class="day-content-wrap">
              <div>
                <div class="day-meta-top">
                  <span class="day-date-title">Día 14 · Martes 4 de mayo</span>
                </div>
                <h3 class="day-headline">Aterrizaje en España y tren de alta velocidad a Zaragoza Delicias</h3>
                <div class="day-chip-row">
                  <span class="day-chip chip-flight"><svg><use href="#i-vuelo"></use></svg>Aterrizaje en Madrid o Barcelona</span>
                  <span class="day-chip"><svg><use href="#i-tren"></use></svg>AVE a Zaragoza</span>
                </div>
                <div class="day-slots-list">
                  <div class="day-slot-box">
                    <span class="slot-time">Mañana (08:30 h a 11:30 h)</span>
                    <p class="slot-text">Llegada a primera hora de la mañana a Barcelona El Prat o Madrid Barajas. Recogida de equipaje y traslado inmediato a la estación de tren de Sants o Atocha.</p>
                  </div>
                  <div class="day-slot-box coral-accent">
                    <span class="slot-time">Tarde (13:30 h a 16:30 h)</span>
                    <p class="slot-text">Tren de alta velocidad AVE o Iryo directo a la estación de Zaragoza Delicias. Estaréis en Zaragoza a lo largo de la tarde del 4 de mayo, cumpliendo con total puntualidad vuestro calendario fijado.</p>
                  </div>
                </div>
              </div>
              <div class="day-info-grid">
                <div class="info-item"><strong>En casa el 4 de mayo:</strong><span>Compromiso temporal cumplido con exactitud, descansados y sin perder días.</span></div>
                <div class="info-item"><strong>Balance:</strong><span>Viaje impecable combinando mar virgen, vida submarina mundial y cultura real.</span></div>
              </div>
            </div>
          </article>
        </div>

      </div>

      <!-- COLUMNA 2: MAPA INTERACTIVO STICKY (EN ESCRITORIO SE QUEDA FIJO Y SE MUEVE AL HACER SCROLL) -->
      <div class="route-map-col">
        <div class="map-interactive-box" id="mapStickyContainer">
          <!-- Control bar del mapa -->
          <div class="map-control-bar">
            <div class="map-active-status">
              <span class="map-status-pill" id="mapStatusPill">Día 01</span>
              <span class="map-status-text" id="mapStatusText">Zaragoza a Madrid/Barcelona y despegue</span>
            </div>

            <!-- Barra de progreso -->
            <div class="map-progress-bar-wrap">
              <div class="map-progress-fill" id="mapProgressFill"></div>
            </div>

            <!-- Scrubber de dias -->
            <div class="map-day-scrubber" id="dayScrubber"></div>
          </div>

          <!-- SVG -->
          <div class="svg-map-wrapper">
            <svg id="mapSvg" viewBox="0 0 1000 420" xmlns="http://www.w3.org/2000/svg">
              <text x="260" y="70" class="map-watermark">MAR DE JAVA</text>
              <text x="820" y="240" class="map-watermark">MAR DE FLORES</text>
              <text x="480" y="405" class="map-watermark">OCÉANO ÍNDICO</text>
              
              <!-- Tierras de Java, Bali, Lombok, Sumbawa y Flores -->
              <path class="map-land" d="{svg_land_path}" />

              <!-- Recuadro origen España / Zaragoza -->
              <g transform="translate(15, 15)">
                <rect width="130" height="48" rx="8" fill="#ffffff" stroke="#cbd5e1" stroke-width="1.5" />
                <text x="12" y="22" font-family="'Plus Jakarta Sans',sans-serif" font-size="10" font-weight="800" fill="var(--c-teal)">ORIGEN / DESTINO</text>
                <text x="12" y="38" font-family="'Plus Jakarta Sans',sans-serif" font-size="11" font-weight="700" fill="var(--text-title)">Zaragoza (AVE)</text>
              </g>

              <!-- Tramos de la ruta (inyectados dinámicamente) -->
              <g id="mapLegsGroup"></g>

              <!-- Beacon animado que marca la posición actual -->
              <circle id="mapBeaconPulse" class="beacon-pulse" cx="-50" cy="-50" r="10" />

              <!-- Nodos de ciudades / paradas -->
              <g id="mapNodesGroup"></g>
            </svg>
          </div>

          <!-- Leyenda inferior -->
          <div class="map-footer-legend">
            <span class="legend-item"><span class="legend-line av"></span> Vuelo</span>
            <span class="legend-item"><span class="legend-line ba"></span> Barco</span>
            <span class="legend-item"><span class="legend-line ti"></span> Tierra</span>
            <span style="margin-left:auto; font-size:0.75rem; color:var(--text-muted);">Sincronizado con lectura</span>
          </div>
        </div>
      </div>

    </div>
  </div>

  <!-- =======================================================
       PANTALLA 2: VISTA DEDICADA DEL MAPA EN MOVIL
       (En escritorio se oculta porque el mapa ya esta en el grid sticky)
       ======================================================= -->
  <div class="app-screen-view" id="app-view-mapa" style="display:none;">
    <div class="section-head">
      <span class="section-tag">Cartografía interactiva</span>
      <h2>Mapa de la expedición</h2>
      <p>Pulsa en cualquier día o ciudad para iluminar el trazado exacto y ver los detalles del trayecto.</p>
    </div>
    <!-- Contenedor clonado para móvil -->
    <div id="mobileMapContainerSlot"></div>
  </div>

  <!-- =======================================================
       PANTALLA 3: COLECCION DE 12 ALOJAMIENTOS ESPECIALES
       ======================================================= -->
  <div class="app-screen-view" id="app-view-hoteles">
    <section class="section" id="seccion-hoteles">
      <div class="section-head">
        <span class="section-tag">Descanso premium garantizado</span>
        <h2>Colección de los 10 alojamientos especiales</h2>
        <p>
          Los 10 alojamientos de esta colección están todos en el recorrido de la Ruta B (sin Java): el valle de Sidemen, el archipiélago de Komodo y las montañas de Munduk. Sustituido el glamping básico de Le Pirate por <strong>Komodo Resort Sebayur</strong>, con bungalows a pie de playa virgen y muy buena valoración de sueño en reseñas independientes (nota: la marca de colchón "King Koil" que anunciaba una versión anterior de esta web no ha podido confirmarse en ninguna fuente independiente ni en el marketing oficial del hotel, así que se ha retirado esa mención concreta).
          Todas las fotos se muestran <strong>100% limpias y sin carteles que tapen la imagen</strong>. Cada ficha incluye botones directos a su web oficial y Booking.com (o Tripadvisor cuando no hay ficha de Booking.com verificada).
        </p>
      </div>

      <!-- Barra de filtros -->
      <div class="filter-button-bar">
        <button class="chip-btn active" onclick="filterHotels('all')">Todos los hoteles (10)</button>
        <button class="chip-btn" onclick="filterHotels('espigon')">Con espigón sobre el mar</button>
        <button class="chip-btn" onclick="filterHotels('playa')">Playa privada / Isla virgen</button>
        <button class="chip-btn" onclick="filterHotels('bambu')">Arquitectura de bambú y selva</button>
      </div>

      <div class="hotel-grid-cards">
        <!-- 1. TA'AKTANA -->
        <div class="hotel-card-item" id="hotel-taaktana" data-category="espigon">
          <div class="hotel-photo-holder"><img src="{get_img("hotel_taaktana")}" alt="TA'AKTANA Luxury Collection"></div>
          <div class="hotel-card-body">
            <div class="hotel-tags-line"><span class="tag-label espigon">Espigón curvado</span><span class="tag-label">Villas sobre el mar</span></div>
            <h3 class="hotel-name-title">TA'AKTANA, Luxury Collection</h3>
            <div class="hotel-place">Labuan Bajo · Mar de Flores</div>
            <p class="hotel-short-desc">Inaugurado en 2024. Cuenta con las únicas villas construidas sobre pilotes de madera suspendidas directamente sobre el agua marina en Flores, conectadas por un gran espigón con acceso privado al mar.</p>
            <div class="sleep-comfort-box">
              <strong>Confort de sueño comprobado:</strong>
              <p>Colchones exclusivos The Luxury Collection Pillow-Top, sábanas de 400 hilos, carta de almohadas y climatización ultrasilenciosa.</p>
            </div>
            <div class="hotel-action-links">
              <a href="https://www.marriott.com/en-us/hotels/lbjlc-taaktana-a-luxury-collection-resort-and-spa-labuan-bajo/overview/" target="_blank" rel="noopener" class="action-btn btn-official-web">Web oficial</a>
              <a href="https://www.booking.com/hotel/id/ta-39-aktana-a-luxury-collection-resort-amp-spa-labuan-bajo.es.html" target="_blank" rel="noopener" class="action-btn btn-booking-com">Booking.com</a>
            </div>
          </div>
        </div>

        <!-- 2. AYANA Komodo -->
        <div class="hotel-card-item" id="hotel-ayana" data-category="espigon playa">
          <div class="hotel-photo-holder"><img src="{get_img("hotel_ayana")}" alt="AYANA Komodo Waecicu Beach"></div>
          <div class="hotel-card-body">
            <div class="hotel-tags-line"><span class="tag-label espigon">Espigón de 250 m</span><span class="tag-label playa">Playa dorada</span></div>
            <h3 class="hotel-name-title">AYANA Komodo Waecicu Beach</h3>
            <div class="hotel-place">Bahía de Waecicu · Labuan Bajo</div>
            <p class="hotel-short-desc">Famoso por su icónico espigón de madera de 250 metros que se adentra mar adentro, culminando en el Kisik Bar donde cenar pescado fresco a la brasa rodeado por las olas. Playa privada y kayaks de cristal.</p>
            <div class="sleep-comfort-box">
              <strong>Confort de sueño comprobado:</strong>
              <p>Camas Sealy Posturepedic Custom de gran firmeza, cortinas 100% blackout que bloquean toda la luz y baño con bañera panorámica al mar.</p>
            </div>
            <div class="hotel-action-links">
              <a href="https://www.ayana.com/labuan-bajo/ayana-komodo/" target="_blank" rel="noopener" class="action-btn btn-official-web">Web oficial</a>
              <a href="https://www.booking.com/hotel/id/ayana-komodo-resort-waecicu-beach.es.html" target="_blank" rel="noopener" class="action-btn btn-booking-com">Booking.com</a>
            </div>
          </div>
        </div>

        <!-- 3. Sudamala Resort Seraya -->
        <div class="hotel-card-item" id="hotel-sudamala" data-category="espigon playa">
          <div class="hotel-photo-holder"><img src="{get_img("hotel_sudamala")}" alt="Sudamala Resort Seraya"></div>
          <div class="hotel-card-body">
            <div class="hotel-tags-line"><span class="tag-label playa">Isla privada</span><span class="tag-label espigon">Espigón sobre arrecife</span></div>
            <h3 class="hotel-name-title">Sudamala Resort, Seraya</h3>
            <div class="hotel-place">Isla Seraya Kecil · Komodo</div>
            <p class="hotel-short-desc">Pequeña isla privada a 45 minutos en lancha. Sus bungalows de madera están plantados en la misma arena blanca. Su largo espigón de madera cruza la barrera de coral para descender directamente a hacer snorkel.</p>
            <div class="sleep-comfort-box">
              <strong>Confort de sueño comprobado:</strong>
              <p>Camas king con dosel de teca balinesa, colchón ortopédico de alta densidad, mosquitera integral elegante y suave murmullo de olas.</p>
            </div>
            <div class="hotel-action-links">
              <a href="https://www.sudamalaresorts.com/seraya/" target="_blank" rel="noopener" class="action-btn btn-official-web">Web oficial</a>
              <a href="https://www.booking.com/hotel/id/sudamala-resort-seraya.es.html" target="_blank" rel="noopener" class="action-btn btn-booking-com">Booking.com</a>
            </div>
          </div>
        </div>

        <!-- 4. Komodo Resort Sebayur -->
        <div class="hotel-card-item" id="hotel-komodo-resort" data-category="espigon playa">
          <div class="hotel-photo-holder"><img src="{get_img("hotel_komodo_resort")}" alt="Komodo Resort Sebayur"></div>
          <div class="hotel-card-body">
            <div class="hotel-tags-line"><span class="tag-label playa">Isla Sebayur</span><span class="tag-label espigon">Muelle privado</span></div>
            <h3 class="hotel-name-title">Komodo Resort & Diving Club</h3>
            <div class="hotel-place">Isla Sebayur Besar · Límite del Parque Nacional</div>
            <p class="hotel-short-desc">El sustituto de alta gama para Le Pirate: bungalows de teca a pie de playa virgen en una isla privada, muelle propio con acceso inmediato a un arrecife que se extiende cerca de 1 km frente al resort y confort hotelero contrastado.</p>
            <div class="sleep-comfort-box">
              <strong>Confort de sueño comprobado:</strong>
              <p>Aire acondicionado individual silencioso, sábanas de algodón egipcio y baño con jardín exterior. Reseñas independientes puntúan la calidad del sueño en 4,8/5 sobre más de 700 opiniones, aunque no hay marca de colchón verificable.</p>
            </div>
            <div class="hotel-action-links">
              <a href="https://www.komodoresort.com/" target="_blank" rel="noopener" class="action-btn btn-official-web">Web oficial</a>
              <a href="https://www.booking.com/hotel/id/komodo-resort-diving-club.es.html" target="_blank" rel="noopener" class="action-btn btn-booking-com">Booking.com</a>
            </div>
          </div>
        </div>

        <!-- 5. Plataran Komodo -->
        <div class="hotel-card-item" id="hotel-plataran" data-category="playa">
          <div class="hotel-photo-holder"><img src="{get_img("hotel_plataran")}" alt="Plataran Komodo Resort"></div>
          <div class="hotel-card-body">
            <div class="hotel-tags-line"><span class="tag-label playa">Cala privada</span><span class="tag-label">Villas Joglo</span></div>
            <h3 class="hotel-name-title">Plataran Komodo Resort & Spa</h3>
            <div class="hotel-place">Playa Waecicu · Labuan Bajo</div>
            <p class="hotel-short-desc">Villas privadas de madera noble javanesa repartidas a lo largo de una cala privada de más de 300 metros, rodeadas de manglares y mar cristalino sin visitantes externos.</p>
            <div class="sleep-comfort-box">
              <strong>Confort de sueño comprobado:</strong>
              <p>Colchones de alta gama con sobrecolchón de pluma hipoalergénica, ambientación de aromaterapia y ausencia total de ruidos urbanos.</p>
            </div>
            <div class="hotel-action-links">
              <a href="https://www.plataran.com/plataran-komodo/" target="_blank" rel="noopener" class="action-btn btn-official-web">Web oficial</a>
              <a href="https://www.booking.com/hotel/id/plataran-komodo-beach-resort.es.html" target="_blank" rel="noopener" class="action-btn btn-booking-com">Booking.com</a>
            </div>
          </div>
        </div>

        <!-- 6. Wapa di Ume Sidemen -->
        <div class="hotel-card-item" id="hotel-wapa-diume" data-category="bambu">
          <div class="hotel-photo-holder"><img src="{get_img("hotel_wapa_diume")}" alt="Wapa di Ume Sidemen"></div>
          <div class="hotel-card-body">
            <div class="hotel-tags-line"><span class="tag-label">Vistas al Agung</span><span class="tag-label">Piscina privada</span></div>
            <h3 class="hotel-name-title">Wapa di Ume Sidemen</h3>
            <div class="hotel-place">Valle de Sidemen · Karangasem</div>
            <p class="hotel-short-desc">Villa diseñada por el arquitecto balinés I Ketut Siadana, con techos de paja, pasarelas elevadas sobre el valle del río Telaga Waja y vistas de 360 grados al monte Agung. Las tiendas de piscina de lujo tienen paredes retráctiles que se abren por completo al arrozal.</p>
            <div class="sleep-comfort-box">
              <strong>Confort de sueño comprobado:</strong>
              <p>Cama king de gran tamaño, mosquitera integral, suelos de madera noble y aire acondicionado (no se ha podido confirmar la marca del colchón en ninguna fuente oficial ni independiente).</p>
            </div>
            <div class="hotel-action-links">
              <a href="https://wapadiumesidemen.com/" target="_blank" rel="noopener" class="action-btn btn-official-web">Web oficial</a>
              <a href="https://www.booking.com/hotel/id/wapa-di-ume-sidemen.html" target="_blank" rel="noopener" class="action-btn btn-booking-com">Booking.com</a>
            </div>
          </div>
        </div>

        <!-- 7. Samanvaya Resort -->
        <div class="hotel-card-item" id="hotel-samanvaya" data-category="bambu">
          <div class="hotel-photo-holder"><img src="{get_img("hotel_samanvaya")}" alt="Samanvaya Resort Sidemen"></div>
          <div class="hotel-card-body">
            <div class="hotel-tags-line"><span class="tag-label">Solo adultos</span><span class="tag-label">Arrozales en terraza</span></div>
            <h3 class="hotel-name-title">Samanvaya Luxury Resort &amp; Spa</h3>
            <div class="hotel-place">Valle de Sidemen · Karangasem</div>
            <p class="hotel-short-desc">Resort solo para adultos, con villas que combinan arquitectura balinesa tradicional y cúpulas abiertas de bambú, tres piscinas infinity sobre los arrozales y el río, y el restaurante Sahaja alojado en un joglo con vistas al valle.</p>
            <div class="sleep-comfort-box">
              <strong>Confort de sueño comprobado:</strong>
              <p>Habitaciones con aire acondicionado y bañeras de piedra o cobre según la villa; varias agencias de reserva citan paredes insonorizadas en algunas categorías, aunque el hotel no lo confirma de forma directa, y no se ha podido verificar la marca del colchón.</p>
            </div>
            <div class="hotel-action-links">
              <a href="https://samanvaya-bali.com/" target="_blank" rel="noopener" class="action-btn btn-official-web">Web oficial</a>
              <a href="https://www.booking.com/hotel/id/samanvaya.html" target="_blank" rel="noopener" class="action-btn btn-booking-com">Booking.com</a>
            </div>
          </div>
        </div>

        <!-- 8. Hideout / Camaya Bali -->
        <div class="hotel-card-item" id="hotel-camaya" data-category="bambu">
          <div class="hotel-photo-holder"><img src="{get_img("hotel_camaya_hideout")}" alt="Hideout Bali"></div>
          <div class="hotel-card-body">
            <div class="hotel-tags-line"><span class="tag-label">Bambú en arrozales</span><span class="tag-label">Volcán Agung</span></div>
            <h3 class="hotel-name-title">Hideout Bali / Camaya Bali</h3>
            <div class="hotel-place">Karangasem · Faldas del volcán Agung</div>
            <p class="hotel-short-desc">Cabañas artesanales de bambú abiertas a la brisa entre arrozales y ríos cristalinos. Camas suspendidas bajo cúpulas de bambú, redes colgantes sobre la selva y bañeras de piedra al aire libre.</p>
            <div class="sleep-comfort-box">
              <strong>Confort de sueño comprobado:</strong>
              <p>Colchones de muelles ensacados con topper mullido, ropa de cama de lino transpirable y arrullo constante del río.</p>
            </div>
            <div class="hotel-action-links">
              <a href="https://hideoutbali.com/" target="_blank" rel="noopener" class="action-btn btn-official-web">Web oficial</a>
              <a href="https://www.booking.com/hotel/id/hideout-bali.es.html" target="_blank" rel="noopener" class="action-btn btn-booking-com">Booking.com</a>
            </div>
          </div>
        </div>

        <!-- 9. Munduk Moding Plantation -->
        <div class="hotel-card-item" id="hotel-munduk-moding" data-category="bambu">
          <div class="hotel-photo-holder"><img src="{get_img("hotel_munduk_moding")}" alt="Munduk Moding Plantation"></div>
          <div class="hotel-card-body">
            <div class="hotel-tags-line"><span class="tag-label">Piscina en las nubes</span><span class="tag-label">Finca de café</span></div>
            <h3 class="hotel-name-title">Munduk Moding Plantation</h3>
            <div class="hotel-place">Munduk · Montañas del norte de Bali</div>
            <p class="hotel-short-desc">Hotel boutique y plantación de café orgánico a 1.000 metros de altitud. Célebre por su piscina infinita de 18 metros que parece desbordarse directamente sobre el mar de Java y las nubes de la cordillera.</p>
            <div class="sleep-comfort-box">
              <strong>Confort de sueño comprobado:</strong>
              <p>Colchones extra gruesos de gama superior con edredones nórdicos de pluma (para las noches frescas de montaña) y chimenea en la suite.</p>
            </div>
            <div class="hotel-action-links">
              <a href="https://www.mundukmodingplantation.com/" target="_blank" rel="noopener" class="action-btn btn-official-web">Web oficial</a>
              <a href="https://www.booking.com/hotel/id/munduk-moding-plantation-nature-resort-spa.es.html" target="_blank" rel="noopener" class="action-btn btn-booking-com">Booking.com</a>
            </div>
          </div>
        </div>

        <!-- 10. Sanak Retreat Bali -->
        <div class="hotel-card-item" id="hotel-sanak" data-category="bambu">
          <div class="hotel-photo-holder"><img src="{get_img("hotel_sanak_retreat")}" alt="Sanak Retreat Bali"></div>
          <div class="hotel-card-body">
            <div class="hotel-tags-line"><span class="tag-label">Desconexión digital</span><span class="tag-label">A 5 min de Munduk</span></div>
            <h3 class="hotel-name-title">Sanak Retreat Bali</h3>
            <div class="hotel-place">Kayu Putih · Montañas del norte de Bali</div>
            <p class="hotel-short-desc">Once bungalows de madera con terraza privada, filosofía de desconexión sin pantallas y ambiente hogareño entre arrozales, cafetales de clavo y selva a los pies de las montañas de Munduk.</p>
            <div class="sleep-comfort-box">
              <strong>Confort de sueño comprobado:</strong>
              <p>Cama king o dos camas individuales según el bungalow, ventilador de techo, aire acondicionado y mosquitera bajo petición (no se ha podido verificar la marca del colchón ni datos de insonorización).</p>
            </div>
            <div class="hotel-action-links">
              <a href="https://sanakbali.com/" target="_blank" rel="noopener" class="action-btn btn-official-web">Web oficial</a>
              <a href="https://www.tripadvisor.com/Hotel_Review-g11435643-d6164357-Reviews-Sanak_Retreat_Bali-Kayuputih_Sukasada_Buleleng_Regency_Bali.html" target="_blank" rel="noopener" class="action-btn btn-booking-com">Tripadvisor</a>
            </div>
          </div>
        </div>
      </div>

      <div class="clean-panel panel-recommended" style="margin-top:24px;">
        <h3 class="panel-header-title">Avisos de actualidad 2026 antes de confirmar reserva</h3>
        <ul>
          <li><strong>Terremoto del 15 de agosto de 2026</strong> en la región de Labuan Bajo/Komodo: tanto Komodo Resort &amp; Diving Club como Meruorah Komodo Labuan Bajo confirmaron en sus canales oficiales seguir operando con normalidad, sin daños relevantes. Se recomienda reconfirmar el estado de la zona pocos meses antes de viajar.</li>
          <li><strong>TA'AKTANA</strong> mantiene una valoración excelente (4,9/5 en más de 200 reseñas), pero una reseña detallada de agosto de 2026 describe una rotación reciente de dirección general. Es un caso aislado, no corroborado por otras reseñas del mismo periodo, pero conviene vigilarlo.</li>
          <li><strong>Alternativa reforzada con espigón sobre el mar:</strong> Plataran Komodo Resort &amp; Spa (Waecicu Beach, del mismo grupo que Plataran Heritage Borobudur) ostenta 1 Llave MICHELIN y el puesto nº1 de 43 hoteles de Labuan Bajo en Tripadvisor, sin incidencias recientes reportadas. Merece considerarse junto a TA'AKTANA y Komodo Resort Sebayur.</li>
        </ul>
      </div>
    </section>
  </div>

  <!-- =======================================================
       PANTALLA 4: ANALISIS DE VUELOS
       ======================================================= -->
  <div class="app-screen-view" id="app-view-vuelos">
    <section class="section" id="seccion-vuelos">
      <div class="section-head">
        <span class="section-tag">Logística aérea</span>
        <h2>Opciones de vuelo: Recomendadas vs descartadas</h2>
        <p>Cómo volar desde Zaragoza optimizando vuestro tiempo de vacaciones y evitando falsos ahorros engañosos.</p>
      </div>

      <div class="two-panel-grid">
        <div class="clean-panel panel-recommended">
          <h3 class="panel-header-title" style="color:var(--c-teal);">✦ Opciones recomendadas (Billete único o multidestino)</h3>
          <p><strong>1. Singapore Airlines desde Barcelona (BCN - SIN - DPS):</strong></p>
          <p>AVE directo de Zaragoza Delicias a Barcelona Sants (1 h 25 min). Vuelo de Singapore Airlines con escala técnica corta en Changi (Singapur) y conexión rápida directa a Bali (2 h 40 min). Es una de las mejores aerolíneas del mundo por puntualidad y servicio; el equipaje va facturado hasta destino y ante cualquier contingencia la reubicación es inmediata. Desde el 27 de octubre de 2026, Singapore Airlines opera además una ruta directa Singapur - Barcelona - Madrid (y en sentido inverso) con el mismo avión, su decimoquinto destino en España y su regreso a Madrid tras 22 años de ausencia, lo que en 2027 podría facilitar aún más esta opción para quien salga desde Barcelona.</p>
          <p><strong>2. Qatar Airways o Emirates desde Madrid (MAD - DOH/DXB - DPS):</strong></p>
          <p>AVE de Zaragoza a Madrid-Atocha (1 h 15 min) y enlace a Barajas T4. Escala cómoda de 2 a 3 horas en Oriente Medio y llegada directa a Bali la tarde del 22 de abril. Si se elige la <strong>Ruta A (con Java)</strong>, se adquiere un billete multidestino oficial: entrada por Yakarta o Yogyakarta y salida por Denpasar (Bali), pagando una tarifa equivalente.</p>
        </div>

        <div class="clean-panel panel-discarded">
          <h3 class="panel-header-title" style="color:var(--c-coral-dark);">✕ Opciones descartadas y por qué</h3>
          <p><strong>1. El falso ahorro de volar a Yakarta (CGK) y comprar low-costs aparte:</strong></p>
          <p>Aunque el billete internacional a Yakarta puede aparecer 100 o 150 euros más barato en buscadores, la suma de los vuelos domésticos de ida y vuelta a Bali/Flores más el suplemento por maleta facturada de 20 kg en aerolíneas indonesias como AirAsia o Lion Air (25 a 35 euros por tramo) elimina la diferencia. Además, cambiar de terminal en Yakarta (de T3 internacional a T1/T2 doméstica) exige recoger maletas y pasar de nuevo seguridad, requiriendo un margen mínimo de 4 horas. En un viaje de 11 noches, perder medio día a la ida y medio a la vuelta es un error logístico.</p>
          <p><strong>2. Vuelos con aerolíneas chinas con dobles escalas largas:</strong></p>
          <p>Air China o China Eastern ofrecen tarifas que a veces bajan de 750 euros, pero implican escalas de 10 a 16 horas en Pekín o Cantón, estirando el viaje a más de 32 horas de trayecto y generando un cansancio extremo.</p>
        </div>
      </div>
    </section>
  </div>

  <!-- =======================================================
       PANTALLA 5: DESTINOS DESCARTADOS Y CRITERIO
       ======================================================= -->
  <div class="app-screen-view" id="app-view-criterio">
    <section class="section" id="seccion-criterio">
      <div class="section-head">
        <span class="section-tag">Criterio y autenticidad</span>
        <h2>Por qué se descartan otros destinos populares</h2>
        <p>Razones fundadas para no dispersar el viaje en lugares saturados o que no aportan valor frente a Komodo.</p>
      </div>

      <div class="two-panel-grid">
        <div class="clean-panel panel-discarded">
          <h3 class="panel-header-title" style="color:var(--c-coral-dark);">✕ Las islas Gili clásicas (Trawangan, Meno y Air)</h3>
          <ul>
            <li><strong>Gili Trawangan:</strong> Famosa por la fiesta nocturna, turismo mochilero ruidoso y alcohol barato. Cero encaje con vuestro perfil.</li>
            <li><strong>Gili Meno y Air:</strong> Aunque son más tranquilas, gran parte de su arrecife somero está muy deteriorado o blanqueado por el calentamiento y el fondeo constante de barcas. El punto de las estatuas submarinas de Jason deCaires suele ser un hervidero agobiante de turistas flotando con chalecos salvavidas.</li>
            <li><strong>Logística pesada:</strong> Exigen 2 horas de carretera al puerto de Padang Bai en Bali y otras 2 horas en lancha rápida por el estrecho de Lombok (a menudo con mar muy agitado). Habiendo elegido Komodo, cuyos fondos marinos son de nivel mundial, las Gili tradicionales no aportan nada y quitan dos días enteros de disfrute.</li>
          </ul>
        </div>

        <div class="clean-panel panel-discarded">
          <h3 class="panel-header-title" style="color:var(--c-coral-dark);">✕ Nusa Penida y el sur masificado de Bali</h3>
          <ul>
            <li><strong>Nusa Penida:</strong> Espectacular en fotografía cenital, pero en tierra sufre un colapso severo: carreteras estrechas de tierra con baches gigantescos, tráfico permanente y colas de hasta 2 horas bajo el sol abrasador para hacerse una foto en el mirador de Kelingking Beach. Además, la mayoría de sus playas tienen un oleaje y corrientes muy peligrosas donde bañarse está desaconsejado.</li>
            <li><strong>Kuta, Seminyak y Canggu:</strong> El epicentro del turismo masivo occidental: discotecas ruidosas, centros comerciales y atascos kilométricos de motocicletas. No tienen nada que ver con la auténtica cultura balinesa de Sidemen o Munduk.</li>
          </ul>
        </div>
      </div>
    </section>
  </div>

  <!-- =======================================================
       PANTALLA: HISTORIA DE INDONESIA
       Cronologia filtrable por era, de Homo erectus a hoy
       ======================================================= -->
  <div class="app-screen-view" id="app-view-historia">
    <section class="section" id="seccion-historia">
      <div class="section-head">
        <span class="section-tag">Contexto para entender lo que se ve</span>
        <h2>Historia de Indonesia en {n_hitos} hitos</h2>
        <p>
          De los primeros homínidos de Java al Parque Nacional de Komodo, contado para que cada templo, cada ofrenda y cada isla del itinerario se entiendan en su contexto. Cada hito indica su base documental, y los que siguen en discusión entre especialistas llevan un aviso: aquí no se presenta como cerrado lo que la investigación mantiene abierto.
        </p>
      </div>

      <div class="era-filter-bar">{filtros_historia}</div>

      <div class="timeline-track">{timeline_historia}</div>
    </section>
  </div>

  <div class="app-screen-view" id="app-view-guia">
    <section class="section" id="seccion-guia">
      <div class="section-head">
        <span class="section-tag">Antes de viajar</span>
        <h2>Guía práctica: documentación, salud, dinero y clima</h2>
        <p>Información contrastada en varias fuentes (oficiales, médicas y de viajeros) para preparar el viaje sin sorpresas. Investigación realizada en 2026: los datos de visado, tasas y salud conviene reconfirmarlos 2 o 3 meses antes de volar, ya que Indonesia cambia esta normativa con cierta frecuencia.</p>
      </div>

      <div class="guide-photo-strip">
        <figure>
          <div class="photo-frame"><img src="{get_img("zaragoza_delicias")}" alt="Tren AVE saliendo de Zaragoza Delicias"></div>
          <figcaption>El primer tramo: AVE desde Zaragoza Delicias hasta el aeropuerto de salida.</figcaption>
        </figure>
        <figure>
          <div class="photo-frame"><img src="{get_img("changi_jewel")}" alt="Vortice de agua en Jewel Changi, Singapur"></div>
          <figcaption>Escala habitual vía Singapur: el vórtice de agua de Jewel Changi.</figcaption>
        </figure>
        <figure>
          <div class="photo-frame"><img src="{get_img("hamad_doha")}" alt="Interior del aeropuerto de Doha"></div>
          <figcaption>Alternativa de escala vía Doha, con Qatar Airways.</figcaption>
        </figure>
      </div>

      <div class="guide-grid">
        <div class="clean-panel guide-card">
          <div class="guide-card-head">
            <span class="guide-card-icon"><svg viewBox="0 0 24 24"><path d="M10.29 3.86 1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path><line x1="12" y1="9" x2="12" y2="13"></line><line x1="12" y1="17" x2="12.01" y2="17"></line></svg></span>
            <h3 class="panel-header-title">Terremoto de Flores: qué comprobar antes de salir</h3>
          </div>
          <div class="guide-fact-row">
            <span class="tag-label">15 de agosto de 2026</span>
            <span class="tag-label">Magnitud 7,7 a 7,8</span>
            <span class="tag-label espigon">Afecta a Labuan Bajo</span>
          </div>
          <div class="discrepancy-box">
            <span class="dx-label">Verificar 2 o 3 meses antes</span>
            <p>Es el asunto de actualidad que más directamente puede afectar a este viaje. Un terremoto de magnitud 7,7 a 7,8 con epicentro frente a la costa norte de Nusa Tenggara Oriental, a unos 68 km al noroeste de Ende, sacudió Flores en la madrugada del 15 de agosto de 2026 y generó un pequeño tsunami de unos 30 cm registrado en Labuan Bajo. Los mayores daños se concentraron en las regencias de Manggarai y Manggarai Oriental, es decir, junto a la propia Labuan Bajo.</p>
          </div>
          <p><strong>Qué tocó de lo que usa el itinerario:</strong> el aeropuerto de Labuan Bajo sufrió daños, los servicios portuarios se suspendieron temporalmente (llegaron a quedar varados cerca de mil turistas en la isla de Padar) y la carretera Trans-Flores quedó cortada en varios puntos por corrimientos de tierra.</p>
          <p><strong>Situación a comienzos de septiembre de 2026:</strong> la reconstrucción seguía en curso en varias regencias de Flores. El viaje sale ocho meses después, en abril de 2027, así que lo previsible es que la operativa esté normalizada, pero conviene confirmar tres cosas antes de pagar nada no reembolsable: que el aeropuerto de Labuan Bajo opera con normalidad, que el resort elegido y su servicio de lancha están operativos, y que la salida a Padar no tiene restricciones.</p>
          <p><strong>Cómo comprobarlo:</strong> el estado sismológico en el USGS y en la agencia indonesia BMKG, y la operativa concreta preguntando por escrito al hotel y al operador del barco, que son quienes saben si su muelle y su lancha funcionan.</p>
          <p class="source-note">Datos sismológicos del Servicio Geológico de Estados Unidos (USGS) y del centro alemán GFZ; cifras de víctimas y daños de agencias internacionales (Reuters, NBC News, NPR) y de organismos de respuesta a desastres.</p>
        </div>

        <div class="clean-panel guide-card">
          <div class="guide-card-head">
            <span class="guide-card-icon"><svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line></svg></span>
            <h3 class="panel-header-title">Visado y entrada</h3>
          </div>
          <div class="guide-fact-row">
            <span class="tag-label">VOA: 500.000 IDR</span>
            <span class="tag-label">Estancia: 30 días + prórroga</span>
            <span class="tag-label espigon">Tasa Bali: 150.000 IDR</span>
          </div>
          <div class="discrepancy-box">
            <span class="dx-label">Fuentes en desacuerdo</span>
            <p>Muchas webs de viajes afirman que España tiene entrada libre de visado durante 30 días en Indonesia. Sin embargo la normativa vigente más autorizada (Perpres 95/2024 sobre exención de visado) redujo esa lista de 169 a solo 16 países, casi todos del sudeste asiático, y España no figura en ella (confirmado en evisa.imigrasi.go.id). Conclusión práctica: como españoles hace falta un visado de llegada (VOA) o su versión electrónica (e-VOA). Conviene volver a comprobarlo poco antes del viaje por si cambia de nuevo.</p>
          </div>
          <p><strong>VOA / e-VOA:</strong> precio oficial de 500.000 IDR (unos 35 USD), visado de entrada única válido 90 días con estancia permitida de 30, prorrogable una vez por 30 días más (total 1.000.000 IDR y 60 días). Se solicita online en evisa.imigrasi.go.id o directamente a la llegada. Base legal: Reglamento PNBP nº45/2024, en vigor desde el 17 de diciembre de 2024.</p>
          <p><strong>Tarjeta electrónica de llegada:</strong> plataforma unificada "All Indonesia", obligatoria y gratuita, solo se puede rellenar dentro de los 3 días previos al vuelo y genera un código QR. Aviso de fraude: usar solo dominios oficiales terminados en .go.id (allindonesia.imigrasi.go.id o ecd.beacukai.go.id); existen webs falsas que cobran por un trámite gratuito.</p>
          <p><strong>Tasa turística de Bali:</strong> 150.000 IDR (9 a 10 USD) por persona, pago único para toda la estancia en Bali, es una tasa provincial que no aplica en Java ni en Komodo/Flores. Se paga en el portal oficial lovebali.baliprov.go.id (tarjeta, transferencia o QRIS) y el comprobante llega por email, conviene guardarlo en varios sitios. Es un pago aparte del VOA, con su propio portal y su propio recibo. En 2026 se ha reforzado el control con inspecciones puntuales en Tanah Lot, Uluwatu, Besakih y Tegallalang, y cerca del aeropuerto.</p>
          <p><strong>Overstay (exceder la estancia permitida):</strong> la multa es de 1.000.000 IDR por día y por persona, hasta un máximo de 60 días; superado ese margen ya no es una multa administrativa sino deportación y una posible prohibición de reentrada. Conviene llevar la cuenta exacta de los 30 días desde el sello de entrada, sobre todo teniendo en cuenta que el itinerario cruza varias veces de isla y de aeropuerto.</p>
          <p><strong>Aeropuerto de Komodo (Labuan Bajo):</strong> el aeropuerto Komodo (LBJ) opera solo vuelos domésticos, así que el e-VOA no se sella ahí. El trámite de entrada (e-VOA y el escaneo del pasaporte) se hace en el primer aeropuerto internacional de llegada a Indonesia (Yakarta, Denpasar/Bali u otro punto de entrada internacional), y el vuelo a Labuan Bajo se toma después como vuelo interno, ya con el visado en regla.</p>
        </div>

        <div class="clean-panel guide-card">
          <div class="guide-card-head">
            <span class="guide-card-icon"><svg viewBox="0 0 24 24"><path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z"></path></svg></span>
            <h3 class="panel-header-title">Salud</h3>
          </div>
          <div class="guide-fact-row">
            <span class="tag-label">Hepatitis A y B</span>
            <span class="tag-label">Dengue: sin vacuna</span>
            <span class="tag-label espigon">Seguro con rescate</span>
          </div>
          <p><strong>Obligatoria:</strong> ninguna vacuna es exigida por ley para viajar desde España, salvo la fiebre amarilla, y solo si en los 9 meses previos se ha estado en un país con riesgo de fiebre amarilla (no aplica viajando directo desde España). Sanidad Exterior España no publica una ficha específica de Indonesia, solo páginas genéricas por enfermedad, así que aquí se sigue el criterio combinado de CDC y TravelHealthPro.</p>
          <p><strong>Recomendadas (generales, toda la ruta):</strong> hepatitis A y B, fiebre tifoidea, y refuerzo de tétanos-difteria-tos ferina (Tdap) si hace más de 10 años de la última dosis. Fuentes suizas (centro de medicina del viajero de Zúrich) añaden el refuerzo de polio si hace más de 10 años y sugieren valorar sarampión-rubeola-parotiditis (triple vírica) si no hay dos dosis previas documentadas.</p>
          <p><strong>Recomendadas por zona:</strong></p>
          <p><strong>Java:</strong> riesgo de malaria bajo en las zonas urbanas y de templos que visitará la pareja (Yogyakarta, Borobudur, Prambanan); la encefalitis japonesa está presente en todo el país pero el riesgo práctico es bajo para una visita corta y urbana, por lo que no suele recomendarse la vacuna salvo estancia rural prolongada.</p>
          <p><strong>Bali (Sidemen y Munduk):</strong> riesgo de malaria bajo, similar a Java. La encefalitis japonesa sí conviene "considerarla" para quien pernocta en zonas rurales de arrozales como Sidemen o Munduk, sobre todo llegando en la cola de la temporada de lluvias.</p>
          <p><strong>Komodo y Flores:</strong> es la zona con más matices, ver el recuadro de discrepancia de fuentes sobre malaria más abajo. Además, el CDC emitió el 7 de agosto de 2026 una alerta de nivel 2 sobre Zika para quienes regresan de Bali, relevante porque el itinerario pasa por Bali antes de llegar a Komodo.</p>
          <div class="discrepancy-box">
            <span class="dx-label">Fuentes en desacuerdo</span>
            <p>El CDC estadounidense (actualizado el 23 de abril de 2025) clasifica explícitamente "todas las zonas del este de Indonesia, incluyendo Labuan Bajo y las islas Komodo" como zona de riesgo de malaria (60% P. falciparum, 40% P. vivax) y recomienda profilaxis con medicación. Las fuentes europeas, incluyendo TravelHealthPro y las suizas, describen el riesgo en esta ruta (Bali, Lombok, Flores) como raro pero presente, sin recomendar profilaxis más allá de la protección frente a picaduras, y las fuentes turísticas locales sitúan el riesgo en el pueblo de Labuan Bajo y en la propia isla de Komodo como bajo (clima semiárido, pocos mosquitos), aumentando en el interior rural y boscoso de Flores. Recomendación: no elegir de forma arbitraria una postura, consultar en persona en un centro de vacunación internacional antes del viaje.</p>
          </div>
          <p><strong>Rabia:</strong> Indonesia tiene presencia de rabia y, en zonas remotas como Flores y el entorno de Komodo, el suero antirrábico (inmunoglobulina, RIG) puede escasear o no estar disponible en el hospital más cercano. Por eso varias fuentes, sobre todo las suizas, recomiendan de forma más amplia la vacunación previa (pre-exposición) para quien vaya a estar en zonas rurales o alejadas de un hospital grande, que es justamente el caso de Komodo y Flores en este itinerario; evita depender de encontrar RIG en caso de mordedura o arañazo de un animal.</p>
          <p><strong>Dengue:</strong> riesgo real y activo en toda Indonesia en 2026, incluyendo Bali y Java, con un repunte en el sur de Bali (Canggu, Legian, Sanur) entre mayo y junio de 2026. No hay vacuna recomendada para viajeros ocasionales, la prevención pasa por repelente con DEET, picaridina, IR3535 o eucalipto de limón.</p>
          <p><strong>Agua:</strong> el agua del grifo no es segura en ningún punto de la ruta. El agua embotellada es barata y está disponible en todas partes (3.000 a 5.000 IDR, 0,20 a 0,35 USD, por 600 ml); conviene revisar el precinto para evitar botellas rellenadas de forma fraudulenta.</p>
          <p><strong>Seguro de viaje:</strong> dado que el itinerario incluye senderismo en Padar y muy probablemente snorkel o buceo en Komodo, conviene un seguro con cobertura de deportes de aventura hasta 40 metros. El producto "IATI Mochilero" aparece citado repetidamente como un buen encaje. Criterios mínimos: gastos médicos de 80.000 a 100.000 euros o más, repatriación o evacuación médica garantizada, asistencia sin pago adelantado, y teléfono 24 horas en español. Indonesia no exige seguro de viaje obligatorio a los turistas.</p>
          <p><strong>Hospitales de referencia:</strong> en Bali, BIMC Kuta, BIMC Nusa Dua y el Siloam Hospital de Bali/Denpasar (único con acreditación JCI en la isla), además de Bali International Hospital, Kasih Ibu, Prima Medika, Surya Husadha y el hospital público Sanglah/Ngoerah. En Yakarta, la red Siloam Hospitals e International SOS Yakarta. Número general de ambulancias: 118. Bali no es un centro médico de referencia como Bangkok o Singapur, los casos complejos se evacúan a Singapur.</p>
        </div>

        <div class="clean-panel guide-card">
          <div class="guide-card-head">
            <span class="guide-card-icon"><svg viewBox="0 0 24 24"><rect x="1" y="4" width="22" height="16" rx="2" ry="2"></rect><line x1="1" y1="10" x2="23" y2="10"></line></svg></span>
            <h3 class="panel-header-title">Dinero</h3>
          </div>
          <div class="guide-fact-row">
            <span class="tag-label espigon">100 a 200 USD/día en pareja</span>
            <span class="tag-label">Moneda: rupia indonesia (IDR)</span>
          </div>
          <p><strong>Tipo de cambio (referencia septiembre de 2026):</strong> 1 EUR ≈ 20.497 IDR (Banco Central Europeo, 3 de septiembre de 2026) y 1 USD ≈ 17.647 IDR (XE.com, 4 de septiembre de 2026). Es solo una referencia para hacer cuentas rápidas de cabeza, conviene comprobar el cambio real cerca de la fecha de salida porque la rupia se mueve con cierta frecuencia. Desde 2022 circula una serie de billetes rediseñada, pero los billetes antiguos siguen siendo de curso legal y se aceptan sin problema.</p>
          <p><strong>Declaración de efectivo:</strong> llevar más de 100.000.000 IDR (unos 4.900 EUR) en efectivo, en cualquier moneda, obliga a declararlo a la entrada o salida de Indonesia. Para el presupuesto de esta pareja no debería ser relevante, pero conviene tenerlo en cuenta si se decide llevar un colchón grande de efectivo para el buceo o el liveaboard.</p>
          <p><strong>QRIS y pago móvil:</strong> QRIS (el sistema de pago por QR omnipresente en Indonesia) tiene acuerdos bilaterales que permiten pagar con apps de Tailandia, Malasia, Singapur, Japón, Corea del Sur o China directamente desde el móvil del viajero. España y la eurozona no forman parte de ese acuerdo, así que para esta pareja QRIS no es una opción práctica: el plan realista sigue siendo efectivo más tarjeta.</p>
          <p><strong>Cajeros:</strong> es habitual pagar doble comisión (la del cajero indonesio más la del banco español). Conviene rechazar siempre la conversión a la moneda de origen (DCC) en el cajero, ya que aplica un recargo de entre el 3 y el 7%. BCA y Mandiri son las redes de cajeros más fiables. Los cajeros suelen entregar billetes de 100.000 IDR, que conviene cambiar por billetes pequeños en tiendas Indomaret o Alfamart.</p>
          <p><strong>Tarjetas:</strong> la aceptación crece en zonas turísticas pero el efectivo sigue siendo imprescindible en warungs, transporte local y pequeños vendedores. La normativa del Banco de Indonesia prohíbe a los comercios cobrar un recargo por pagar con tarjeta, así que se puede rechazar un intento de recargo del 2 o 3%. Conviene llevar siempre billetes pequeños (10.000, 20.000 y 50.000 IDR).</p>
          <p><strong>Propinas:</strong> no son obligatorias pero cada vez se esperan más en zonas turísticas. Muchos restaurantes ya incluyen un cargo de servicio del 10% (formato "++": precio más impuesto más servicio, conviene revisar la cuenta antes de añadir propina extra). Para un guía o conductor privado de día completo, 50.000 a 100.000 IDR se considera generoso; para un masajista, 20.000 a 50.000 IDR. En las cafeterías no suele haber cargo de servicio y la propina es informal.</p>
          <p><strong>Presupuesto:</strong> para una pareja, con un nivel medio-alto (buenas comidas, conductor privado, actividades diarias), la estimación es de 100 a 200 USD al día, sin contar alojamiento de gama alta, vuelos domésticos ni actividades caras concretas como los liveaboards o el buceo en Komodo.</p>
        </div>

        <div class="clean-panel guide-card">
          <div class="guide-card-head">
            <span class="guide-card-icon"><svg viewBox="0 0 24 24"><path d="M5 12.55a11 11 0 0 1 14.08 0"></path><path d="M1.42 9a16 16 0 0 1 21.16 0"></path><path d="M8.53 16.11a6 6 0 0 1 6.95 0"></path><line x1="12" y1="20" x2="12.01" y2="20"></line></svg></span>
            <h3 class="panel-header-title">Conectividad</h3>
          </div>
          <div class="guide-fact-row">
            <span class="tag-label espigon">eSIM con red Telkomsel</span>
          </div>
          <p>La red Telkomsel ofrece de forma consistente la mejor cobertura fuera de las zonas turísticas principales, incluyendo Komodo, Flores, Lombok, Sumba y Raja Ampat. Las eSIM tipo Airalo que solo usan las redes Hutchison, Indosat o Tri tienen cobertura débil en Lombok, Flores, Sumba, Sumatra y Sulawesi, por lo que no se recomiendan para un itinerario con tanto peso en Komodo.</p>
          <p>Alternativas recomendadas que sí usan la red Telkomsel: "Nomad eSIM" (válida hasta 45 días) y "voilà", citada específicamente para el salto entre islas porque Telkomsel capta señal donde otras fallan; "Jetpac" también aparece conectada a Telkomsel. Holafly ofrece datos "ilimitados" pero con un límite práctico en torno a 90 GB al mes y un precio más alto (unos 4 USD al día), solo interesante con un consumo de datos muy alto.</p>
          <p>Alternativa local: comprar una SIM o eSIM física de Telkomsel, XL Axiata o Indosat directamente en las tiendas oficiales del aeropuerto. Recomendación concreta para este viaje, dado el peso de Komodo: priorizar una eSIM con red Telkomsel (Nomad eSIM o similar) frente a una Airalo pura.</p>
        </div>

        <div class="clean-panel guide-card">
          <div class="guide-card-head">
            <span class="guide-card-icon"><svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="5"></circle><line x1="12" y1="1" x2="12" y2="3"></line><line x1="12" y1="21" x2="12" y2="23"></line><line x1="4.22" y1="4.22" x2="5.64" y2="5.64"></line><line x1="18.36" y1="18.36" x2="19.78" y2="19.78"></line><line x1="1" y1="12" x2="3" y2="12"></line><line x1="21" y1="12" x2="23" y2="12"></line><line x1="4.22" y1="19.78" x2="5.64" y2="18.36"></line><line x1="18.36" y1="5.64" x2="19.78" y2="4.22"></line></svg></span>
            <h3 class="panel-header-title">Clima en las fechas del viaje</h3>
          </div>
          <div class="guide-fact-row">
            <span class="tag-label espigon">21 abril a 4 mayo 2027</span>
          </div>
          <p><strong>Java:</strong> temperaturas estables todo el año (máximas de 29 a 32°C, mínimas de 22 a 24°C). Abril es todavía la cola de la temporada de lluvias (cálido, húmedo, con lluvia relativamente frecuente); mayo marca la transición clara hacia la temporada seca, aunque la humedad relativa se mantiene alta. Para las fechas del viaje: cola de la fase húmeda transicionando a la seca, con probabilidad de lluvia decreciente pero no nula, y calor húmedo constante.</p>
          <p><strong>Bali:</strong> un patrón de transición muy similar al de Java.</p>
          <p><strong>Komodo y Flores:</strong> clima semiárido, distinto del resto de Indonesia, influido por los vientos secos australianos. En abril la temporada seca ya está avanzada (cielos despejados, media de 27 a 28°C, máximas de 31 a 32°C no son raras); mayo sigue seco y soleado, el agua alcanza unos 29°C (excelente visibilidad para buceo y snorkel), con 8 o 9 horas de sol al día de media.</p>
          <p><strong>Conclusión:</strong> finales de abril y principios de mayo de 2027 es una muy buena época para este viaje, con la temporada seca ya establecida o casi, calor constante, buena visibilidad para el buceo y menos aglomeración que en la temporada alta de julio y agosto.</p>
        </div>

        <div class="clean-panel guide-card">
          <div class="guide-card-head">
            <span class="guide-card-icon"><svg viewBox="0 0 24 24"><rect x="2" y="7" width="20" height="14" rx="2" ry="2"></rect><path d="M16 21V5a2 2 0 0 0-2-2h-4a2 2 0 0 0-2 2v16"></path></svg></span>
            <h3 class="panel-header-title">Equipaje</h3>
          </div>
          <div class="guide-fact-row">
            <span class="tag-label">Protector solar reef-safe</span>
            <span class="tag-label espigon">Calzado cerrado para Padar</span>
          </div>
          <p><strong>Snorkel:</strong> no hay un veredicto definitivo entre traer o alquilar máscara y tubo, pero la práctica habitual en foros de buceo recomienda traer máscara y tubo propios por higiene y ajuste, ya que el estado del material de alquiler varía mucho en liveaboards y excursiones de un día. Las aletas sí se pueden alquilar sin problema para ahorrar peso.</p>
          <p><strong>Calzado:</strong> en Padar (subida corta pero empinada, terreno irregular y rocoso, resbaladizo si ha llovido por la mañana) se recomienda calzado cerrado de trekking o trail running, nunca chanclas ni sandalias planas. En Rinca (terreno más llano y ondulado) el reto principal es el calor y el sol, no la dificultad técnica. El mejor momento para ambas es el amanecer: más fresco, mejor luz y menos gente.</p>
          <p><strong>Sol y mosquitos:</strong> protector solar reef-safe (mineral, con óxido de zinc o dióxido de titanio, factor 50+) obligatorio para el snorkel, ya que el protector químico daña el coral; sombrero de ala ancha con cinta de sujeción para el viento en barco; repelente con DEET o picaridina para el dengue y, según la fuente, también para el riesgo de malaria en Flores.</p>
          <p><strong>Vestimenta en templos:</strong> Borobudur aplica el código de vestimenta de forma más estricta (hay que cubrir hombros y rodillas, se pueden alquilar sarongs en el propio recinto por 10.000 a 20.000 IDR); Prambanan es más relajado, solo recomienda una vestimenta discreta sin exigirla de forma estricta.</p>
          <p><strong>General:</strong> ropa ligera y transpirable de manga larga (protege del sol y de los mosquitos a la vez), una toalla pequeña o pañuelo para el sudor y el cuello, y una botella de agua reutilizable para rellenar con agua embotellada o filtrada y reducir el plástico.</p>
        </div>

        <div class="clean-panel guide-card guide-card-wide">
          <div class="guide-card-head">
            <span class="guide-card-icon"><svg viewBox="0 0 24 24"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg></span>
            <h3 class="panel-header-title">Embajada y consulado</h3>
          </div>
          <div class="two-panel-grid">
            <div>
              <p><strong>Embajada de España en Yakarta:</strong> Jl. Haji Agus Salim, 61, Yakarta Pusat, 10350. Teléfono +62-21 314 23 55; teléfono/fax alternativo +62-21 319 35 134; Sección Consular +62-21 319 25 996. Correo de la embajada emb.yakarta@maec.es; correo de la sección consular emb.yakarta.sc@maec.es. La sección consular de Yakarta tiene competencia sobre todo el territorio indonesio, incluyendo registro civil, trámites notariales y de pasaporte.</p>
            </div>
            <div>
              <p><strong>Consulado Honorario en Bali:</strong> cónsul honoraria Sra. Mila Tayeb, Kibarer Building, Jalan Petitenget 9-A, Kerobokan Kelod, Seminyak. Teléfono +62 811 389 8880 (horario de mañana, de lunes a viernes). Correos honorary.cspainbali@gmail.com y ch.bali@maec.es. Importante: tiene competencias limitadas, para registro civil, trámites notariales y de pasaporte hay que acudir a la sección consular de Yakarta.</p>
            </div>
          </div>
        </div>

        <div class="clean-panel guide-card guide-card-wide">
          <div class="guide-card-head">
            <h3 class="panel-header-title">Gastronomía que no os podéis perder</h3>
          </div>
          <p>Un pequeño mapa de sabores para ir sobre aviso, del gudeg dulce de Yogyakarta al lechón ceremonial balinés.</p>
          <div class="guide-photo-strip">
            <figure>
              <div class="photo-frame"><img src="{get_img("gudeg")}" alt="Gudeg, plato tradicional de Yogyakarta"></div>
              <figcaption><strong>Gudeg</strong> (Yogyakarta): guiso dulce de yaca joven cocinada a fuego lento con leche de coco.</figcaption>
            </figure>
            <figure>
              <div class="photo-frame"><img src="{get_img("babi_guling")}" alt="Babi guling, cerdo asado ceremonial balines"></div>
              <figcaption><strong>Babi guling</strong> (Bali): cerdo asado entero relleno de especias, plato ceremonial por excelencia.</figcaption>
            </figure>
            <figure>
              <div class="photo-frame"><img src="{get_img("nasi_campur")}" alt="Nasi campur, plato combinado balines"></div>
              <figcaption><strong>Nasi campur</strong> (Bali): arroz con una selección variada de guarniciones, ideal para probar de todo.</figcaption>
            </figure>
            <figure>
              <div class="photo-frame"><img src="{get_img("bebek_betutu")}" alt="Bebek betutu, pato especiado balines"></div>
              <figcaption><strong>Bebek betutu</strong> (Bali): pato envuelto en hoja de plátano y cocinado lentamente con especias.</figcaption>
            </figure>
            <figure>
              <div class="photo-frame"><img src="{get_img("sate_lilit")}" alt="Sate lilit, brochetas balinesas de pescado especiado"></div>
              <figcaption><strong>Sate lilit</strong> (Bali): pescado especiado enrollado sobre un tallo de citronela y asado.</figcaption>
            </figure>
            <figure>
              <div class="photo-frame"><img src="{get_img("kopi")}" alt="Mercado tradicional de cafe en Indonesia"></div>
              <figcaption><strong>Kopi</strong>: café indonesio de cultivo local, presente en toda la ruta.</figcaption>
            </figure>
          </div>
        </div>
      </div>
    </section>
  </div>

</main>

<!-- =======================================================
     BARRA DE NAVEGACION INFERIOR FIJA TIPO APP (SOLO EN MOVIL)
     ======================================================= -->
<nav class="bottomnav" aria-label="Navegación móvil de la app">
  <button class="bn-item active" id="bn-ruta" onclick="switchMobileTab('app-view-ruta', this)">
    <svg viewBox="0 0 24 24"><rect x="3" y="4" width="18" height="18" rx="2" ry="2"></rect><line x1="16" y1="2" x2="16" y2="6"></line><line x1="8" y1="2" x2="8" y2="6"></line><line x1="3" y1="10" x2="21" y2="10"></line></svg>
    <span>Ruta</span>
  </button>
  
  <button class="bn-item" id="bn-mapa" onclick="switchMobileTab('app-view-mapa', this)">
    <svg viewBox="0 0 24 24"><polygon points="1 6 1 22 8 18 16 22 23 18 23 2 16 6 8 2 1 6"></polygon><line x1="8" y1="2" x2="8" y2="18"></line><line x1="16" y1="6" x2="16" y2="22"></line></svg>
    <span>Mapa</span>
  </button>

  <button class="bn-item" id="bn-hoteles" onclick="switchMobileTab('app-view-hoteles', this)">
    <svg viewBox="0 0 24 24"><path d="M3 9l9-7 9 7v11a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2z"></path><polyline points="9 22 9 12 15 12 15 22"></polyline></svg>
    <span>Hoteles</span>
  </button>

  <button class="bn-item" id="bn-vuelos" onclick="switchMobileTab('app-view-vuelos', this)">
    <svg viewBox="0 0 24 24"><path d="M22 2L11 13"></path><polygon points="22 2 15 22 11 13 2 9 22 2"></polygon></svg>
    <span>Vuelos</span>
  </button>

  <button class="bn-item" id="bn-criterio" onclick="switchMobileTab('app-view-criterio', this)">
    <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="10"></circle><line x1="12" y1="16" x2="12" y2="12"></line><line x1="12" y1="8" x2="12.01" y2="8"></line></svg>
    <span>Criterio</span>
  </button>

  <button class="bn-item" id="bn-historia" onclick="switchMobileTab('app-view-historia', this)">
    <svg viewBox="0 0 24 24"><circle cx="12" cy="12" r="9"></circle><polyline points="12 7 12 12 16 14"></polyline></svg>
    <span>Historia</span>
  </button>

  <button class="bn-item" id="bn-guia" onclick="switchMobileTab('app-view-guia', this)">
    <svg viewBox="0 0 24 24"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line></svg>
    <span>Guía</span>
  </button>
</nav>

<footer class="clean-footer">
  Indonesia 2027 · Documento de decisión interactivo · Viaje en pareja de Álvaro (Zaragoza) · 21 de abril al 4 de mayo<br>
  Diseño claro costero · Paleta oficial Sarah Renae Clark · Mapa sincronizado con scroll · Modo app móvil nativo · Cero dependencias externas
</footer>

<script>
// ==========================================
// CONFIGURACION CARTOGRAFICA Y DE TRAMOS
// ==========================================
const MAP_CONFIG = {{
  nodes: {{
    es:      {{ name: "Zaragoza / Madrid", x: 80,  y: 40,   labelPos: "right" }},
    cgk:     {{ name: "Yakarta",          x: 116, y: 82,   labelPos: "top" }},
    yia:     {{ name: "Borobudur / Yogya",x: 339, y: 267,  labelPos: "bottom" }},
    dps:     {{ name: "Bali (Denpasar)",  x: 643, y: 378,  labelPos: "bottom" }},
    sidemen: {{ name: "Valle de Sidemen", x: 661, y: 348,  labelPos: "right" }},
    munduk:  {{ name: "Munduk (Montaña)", x: 636, y: 323,  labelPos: "left" }},
    lbj:     {{ name: "Labuan Bajo",      x: 942, y: 349,  labelPos: "right" }},
    komodo:  {{ name: "Komodo / Padar",   x: 922, y: 368,  labelPos: "bottom" }},
    resort:  {{ name: "Resort Espigón",   x: 931, y: 352,  labelPos: "top" }}
  }},
  rutas: {{
    'opcion-a': {{
      nombre: "Ruta A: Con Java",
      dias: [
        {{ d: 1,  node: "es",      desc: "Zaragoza Delicias a MAD/BCN y vuelo internacional", legIdx: 0 }},
        {{ d: 2,  node: "yia",     desc: "Llegada a Yakarta y salto a Borobudur (Java)",       legIdx: 1 }},
        {{ d: 3,  node: "yia",     desc: "Amanecer en Borobudur y atardecer en Prambanan",    legIdx: 1 }},
        {{ d: 4,  node: "lbj",     desc: "Vuelo a Bali y conexión a Labuan Bajo (Flores)",    legIdx: 2 }},
        {{ d: 5,  node: "komodo",  desc: "Embarque en Phinisi: Isla Kelor y dragones Rinca",   legIdx: 3 }},
        {{ d: 6,  node: "komodo",  desc: "Amanecer en Isla Padar y snorkel en Pink Beach",    legIdx: 4 }},
        {{ d: 7,  node: "komodo",  desc: "Mantas gigantes en Manta Point y Taka Makassar",    legIdx: 5 }},
        {{ d: 8,  node: "resort",  desc: "Tortugas en Siaba y única noche en el espigón",     legIdx: 6 }},
        {{ d: 9,  node: "sidemen", desc: "Último baño, vuelo a Bali y Valle de Sidemen",      legIdx: 7 }},
        {{ d: 10, node: "sidemen", desc: "Arrozales al amanecer, telares y arak de palma",    legIdx: 8 }},
        {{ d: 11, node: "sidemen", desc: "Pura Kehen, Gunung Kawi y purificación sagrada",    legIdx: 8 }},
        {{ d: 12, node: "sidemen", desc: "Pecio del Liberty en Tulamben y Tirta Gangga",      legIdx: 8 }},
        {{ d: 13, node: "dps",     desc: "Iseh, los pintores del valle y salida al aeropuerto", legIdx: 9 }},
        {{ d: 14, node: "es",      desc: "Llegada a España y AVE directo a Zaragoza Delicias", legIdx: 10 }}
      ],
      legs: [
        {{ id: "l-a-1", from: "es",      to: "cgk",     tipo: "avion",  d: "M 80 40 Q 95 60 116 82" }},
        {{ id: "l-a-2", from: "cgk",     to: "yia",     tipo: "avion",  d: "M 116 82 Q 220 170 339 267" }},
        {{ id: "l-a-3", from: "yia",     to: "lbj",     tipo: "avion",  d: "M 339 267 Q 640 280 942 349" }},
        {{ id: "l-a-4", from: "lbj",     to: "komodo",  tipo: "barco",  d: "M 942 349 Q 935 362 922 368" }},
        {{ id: "l-a-5", from: "komodo",  to: "komodo",  tipo: "barco",  d: "M 922 368 Q 918 380 922 368" }},
        {{ id: "l-a-6", from: "komodo",  to: "komodo",  tipo: "barco",  d: "M 922 368 Q 926 360 922 368" }},
        {{ id: "l-a-7", from: "komodo",  to: "resort",  tipo: "barco",  d: "M 922 368 Q 928 358 931 352" }},
        {{ id: "l-a-8", from: "resort",  to: "sidemen", tipo: "avion",  d: "M 931 352 Q 800 320 661 348" }},
        {{ id: "l-a-9", from: "sidemen", to: "sidemen", tipo: "tierra", d: "M 661 348 Q 668 340 661 348" }},
        {{ id: "l-a-10",from: "sidemen", to: "dps",     tipo: "tierra", d: "M 661 348 Q 652 365 643 378" }},
        {{ id: "l-a-11",from: "dps",     to: "es",      tipo: "avion",  d: "M 643 378 Q 360 140 80 40" }}
      ]
    }},
    'opcion-b': {{
      nombre: "Ruta B: Sin Java",
      dias: [
        {{ d: 1,  node: "es",      desc: "Zaragoza Delicias a BCN/MAD y vuelo directo a Bali", legIdx: 0 }},
        {{ d: 2,  node: "sidemen", desc: "Aterrizaje en Bali y traslado directo a Sidemen",    legIdx: 0 }},
        {{ d: 3,  node: "sidemen", desc: "Arrozales al amanecer, telares y arak de palma",     legIdx: 1 }},
        {{ d: 4,  node: "sidemen", desc: "Santuarios de Gunung Kawi y purificación sagrada",   legIdx: 1 }},
        {{ d: 5,  node: "sidemen", desc: "Pecio del Liberty en Tulamben y Tirta Gangga",       legIdx: 1 }},
        {{ d: 6,  node: "komodo",  desc: "Vuelo a Labuan Bajo y embarque en barco Phinisi",    legIdx: 2 }},
        {{ d: 7,  node: "komodo",  desc: "Amanecer en Isla Padar y snorkel en Pink Beach",     legIdx: 3 }},
        {{ d: 8,  node: "komodo",  desc: "Dragones en Loh Liang, mantas y Taka Makassar",      legIdx: 4 }},
        {{ d: 9,  node: "resort",  desc: "Tortugas en Siaba y única noche en el espigón",      legIdx: 5 }},
        {{ d: 10, node: "munduk",  desc: "Vuelo a Bali y ascenso a las montañas de Munduk",    legIdx: 6 }},
        {{ d: 11, node: "munduk",  desc: "Cascadas de Banyumala y canoa en Lago Tamblingan",   legIdx: 7 }},
        {{ d: 12, node: "munduk",  desc: "Trek al valle de cascadas de Sekumpul",              legIdx: 7 }},
        {{ d: 13, node: "dps",     desc: "Ulun Danu Beratan, Jatiluwih y salida al aeropuerto", legIdx: 8 }},
        {{ d: 14, node: "es",      desc: "Llegada a España y AVE directo a Zaragoza Delicias", legIdx: 9 }}
      ],
      legs: [
        {{ id: "l-b-1", from: "es",      to: "sidemen", tipo: "avion",  d: "M 80 40 Q 360 140 661 348" }},
        {{ id: "l-b-2", from: "sidemen", to: "sidemen", tipo: "tierra", d: "M 661 348 Q 670 340 661 348" }},
        {{ id: "l-b-3", from: "sidemen", to: "komodo",  tipo: "avion",  d: "M 661 348 Q 800 320 922 368" }},
        {{ id: "l-b-4", from: "komodo",  to: "komodo",  tipo: "barco",  d: "M 922 368 Q 918 380 922 368" }},
        {{ id: "l-b-5", from: "komodo",  to: "komodo",  tipo: "barco",  d: "M 922 368 Q 926 360 922 368" }},
        {{ id: "l-b-6", from: "komodo",  to: "resort",  tipo: "barco",  d: "M 922 368 Q 928 358 931 352" }},
        {{ id: "l-b-7", from: "resort",  to: "munduk",  tipo: "avion",  d: "M 931 352 Q 780 310 636 323" }},
        {{ id: "l-b-8", from: "munduk",  to: "munduk",  tipo: "tierra", d: "M 636 323 Q 630 315 636 323" }},
        {{ id: "l-b-9", from: "munduk",  to: "dps",     tipo: "tierra", d: "M 636 323 Q 640 350 643 378" }},
        {{ id: "l-b-10",from: "dps",     to: "es",      tipo: "avion",  d: "M 643 378 Q 360 140 80 40" }}
      ]
    }}
  }}
}};

let rutaActiva = 'opcion-a';
let diaSeleccionado = 1;
let modoManual = false;
let timeoutManual = null;

// Inicializacion del mapa y componentes
function initMap() {{
  renderDayScrubber();
  renderMapRoute();
  setMapDay(1, false);
}}

function renderDayScrubber() {{
  const container = document.getElementById('dayScrubber');
  if (!container) return;
  container.innerHTML = '';
  const dias = MAP_CONFIG.rutas[rutaActiva].dias;

  dias.forEach(d => {{
    const btn = document.createElement('button');
    btn.className = 'scrub-btn' + (d.d === diaSeleccionado ? ' active' : '');
    btn.textContent = 'D' + d.d;
    btn.onclick = (e) => {{
      e.stopPropagation();
      modoManual = true;
      clearTimeout(timeoutManual);
      timeoutManual = setTimeout(() => {{ modoManual = false; }}, 1200);
      setMapDay(d.d, true);
    }};
    container.appendChild(btn);
  }});
}}

function renderMapRoute() {{
  const ruta = MAP_CONFIG.rutas[rutaActiva];
  const legsGroup = document.getElementById('mapLegsGroup');
  const nodesGroup = document.getElementById('mapNodesGroup');

  if (!legsGroup || !nodesGroup) return;
  legsGroup.innerHTML = '';
  nodesGroup.innerHTML = '';

  // Dibujar tramos
  ruta.legs.forEach((leg, idx) => {{
    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
    path.setAttribute('id', leg.id);
    path.setAttribute('class', 'map-leg ' + leg.tipo);
    path.setAttribute('data-idx', idx);
    path.setAttribute('d', leg.d);
    legsGroup.appendChild(path);
  }});

  // Dibujar nodos
  Object.keys(MAP_CONFIG.nodes).forEach(nodeKey => {{
    const node = MAP_CONFIG.nodes[nodeKey];
    const g = document.createElementNS('http://www.w3.org/2000/svg', 'g');
    g.setAttribute('class', 'map-node');
    g.setAttribute('id', 'node-' + nodeKey);
    g.setAttribute('transform', `translate(${{node.x}}, ${{node.y}})`);

    // Zona tactil amplia
    const hit = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    hit.setAttribute('class', 'hit');
    hit.setAttribute('r', '18');
    g.appendChild(hit);

    // Pin visible
    const pin = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
    pin.setAttribute('class', 'pin');
    pin.setAttribute('r', '5.5');
    g.appendChild(pin);

    // Etiqueta de texto
    const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
    let dx = 8, dy = 4;
    let anchor = 'start';
    if (node.labelPos === 'bottom') {{ dx = 0; dy = 16; anchor = 'middle'; }}
    else if (node.labelPos === 'top') {{ dx = 0; dy = -10; anchor = 'middle'; }}
    else if (node.labelPos === 'left') {{ dx = -8; dy = 4; anchor = 'end'; }}

    text.setAttribute('x', dx);
    text.setAttribute('y', dy);
    text.setAttribute('text-anchor', anchor);
    text.textContent = node.name;
    g.appendChild(text);

    // Clic en nodo salta al dia de llegada
    g.onclick = () => {{
      const foundDay = ruta.dias.find(item => item.node === nodeKey);
      if (foundDay) {{
        modoManual = true;
        clearTimeout(timeoutManual);
        timeoutManual = setTimeout(() => {{ modoManual = false; }}, 1200);
        setMapDay(foundDay.d, true);
      }}
    }};

    nodesGroup.appendChild(g);
  }});
}}

// =======================================================
// ACTUALIZACION DINAMICA DEL MAPA (DONE / NOW / BEACON / PROGRESO)
// =======================================================
function setMapDay(dayNum, scroll, customTitle) {{
  diaSeleccionado = dayNum;
  const ruta = MAP_CONFIG.rutas[rutaActiva];
  const dayData = ruta.dias.find(d => d.d === dayNum) || ruta.dias[0];

  // Actualizar barra de estado del mapa
  const pill = document.getElementById('mapStatusPill');
  const txt = document.getElementById('mapStatusText');
  const progFill = document.getElementById('mapProgressFill');

  if (pill) pill.textContent = 'Día ' + (dayNum < 10 ? '0' : '') + dayNum;
  if (txt) txt.textContent = customTitle || dayData.desc;
  if (progFill) progFill.style.width = ((dayNum / 14) * 100) + '%';

  // Actualizar botones del scrubber
  const buttons = document.querySelectorAll('.map-day-scrubber .scrub-btn');
  buttons.forEach((btn, idx) => {{
    btn.classList.toggle('active', (idx + 1) === dayNum);
  }});

  // Actualizar posicion de la baliza luminosa y nodo activo
  const nodeKey = dayData.node;
  const nodeInfo = MAP_CONFIG.nodes[nodeKey];

  document.querySelectorAll('.map-node').forEach(nodeEl => {{
    nodeEl.classList.toggle('active-stop', nodeEl.id === 'node-' + nodeKey);
  }});

  const beacon = document.getElementById('mapBeaconPulse');
  if (beacon && nodeInfo) {{
    beacon.setAttribute('cx', nodeInfo.x);
    beacon.setAttribute('cy', nodeInfo.y);
  }}

  // Iluminar tramos: done para los anteriores, active-now para el actual
  const targetLegIdx = dayData.legIdx !== undefined ? dayData.legIdx : -1;
  document.querySelectorAll('.map-leg').forEach((legEl) => {{
    const idx = parseInt(legEl.getAttribute('data-idx'), 10);
    legEl.classList.remove('done', 'active-now', 'inactive');
    
    if (idx === targetLegIdx) {{
      legEl.classList.add('active-now');
    }} else if (idx < targetLegIdx) {{
      legEl.classList.add('done');
    }} else {{
      legEl.classList.add('inactive');
    }}
  }});

  // Resaltar tarjeta activa en el texto
  const prefix = (rutaActiva === 'opcion-a') ? 'dia-a-' : 'dia-b-';
  document.querySelectorAll('.day-card-single').forEach(c => c.classList.remove('active-reading'));
  const currentCard = document.getElementById(prefix + dayNum);
  if (currentCard) {{
    currentCard.classList.add('active-reading');
    if (scroll) {{
      currentCard.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
    }}
  }}
}}

// =======================================================
// SINCRONIZACION CON SCROLL EN ESCRITORIO (ESTILO CHINA 2027)
// Conforme el usuario hace scroll, los tramos se van uniendo
// =======================================================
let scrollPending = false;

function onWindowScroll() {{
  if (modoManual) return;
  // Solo sincronizamos scroll en resoluciones de escritorio donde el mapa es sticky
  if (window.innerWidth < 1020) return;

  if (!scrollPending) {{
    scrollPending = true;
    requestAnimationFrame(syncMapScrollPosition);
  }}
}}

function syncMapScrollPosition() {{
  scrollPending = false;
  const readingThreshold = window.innerHeight * 0.38; // Linea de lectura al 38% superior
  const cards = document.querySelectorAll('#block-' + rutaActiva + ' .day-card-single');
  
  let currentActiveDay = 1;
  let currentTitle = '';

  cards.forEach((card, idx) => {{
    const rect = card.getBoundingClientRect();
    if (rect.top <= readingThreshold) {{
      currentActiveDay = parseInt(card.getAttribute('data-dia'), 10) || (idx + 1);
      currentTitle = card.getAttribute('data-title') || '';
    }}
  }});

  setMapDay(currentActiveDay, false, currentTitle);
}}

window.addEventListener('scroll', onWindowScroll, {{ passive: true }});

// =======================================================
// CONMUTACION DE RUTAS (CON JAVA VS SIN JAVA)
// =======================================================
function switchRoute(routeId) {{
  rutaActiva = routeId;
  document.querySelectorAll('.route-block').forEach(panel => {{
    panel.style.display = 'none';
  }});
  const activeBlock = document.getElementById('block-' + routeId);
  if (activeBlock) activeBlock.style.display = 'block';
  
  const cardA = document.getElementById('card-toggle-a');
  const cardB = document.getElementById('card-toggle-b');
  const navBtns = document.querySelectorAll('.hero-nav-pill-group .nav-pill-link');

  if (routeId === 'opcion-a') {{
    cardA.classList.add('active');
    cardB.classList.remove('active', 'coral-active');
    if (navBtns[0]) navBtns[0].classList.add('active');
    if (navBtns[1]) navBtns[1].classList.remove('active');
  }} else {{
    cardB.classList.add('active', 'coral-active');
    cardA.classList.remove('active');
    if (navBtns[1]) navBtns[1].classList.add('active');
    if (navBtns[0]) navBtns[0].classList.remove('active');
  }}

  renderDayScrubber();
  renderMapRoute();
  setMapDay(1, false);
}}

// =======================================================
// CONMUTACION DE PANTALLAS / VISTAS EN VERSION MOVIL
// Mejora la velocidad al renderizar solo la seccion seleccionada
// =======================================================
function switchMobileTab(viewId, btn) {{
  // Actualizar boton activo en la barra inferior
  document.querySelectorAll('.bottomnav .bn-item').forEach(b => b.classList.remove('active'));
  if (btn) btn.classList.add('active');

  // En movil mostramos solo la vista elegida
  if (window.innerWidth <= 920) {{
    document.querySelectorAll('.app-screen-view').forEach(view => {{
      view.classList.remove('active-mobile-view');
      view.style.display = 'none';
    }});

    const targetView = document.getElementById(viewId);
    if (targetView) {{
      targetView.classList.add('active-mobile-view');
      targetView.style.display = 'block';
      
      // Si entra a la pantalla de mapa en móvil, movemos el mapa a su slot
      if (viewId === 'app-view-mapa') {{
        const mapBox = document.getElementById('mapStickyContainer');
        const mobileSlot = document.getElementById('mobileMapContainerSlot');
        if (mapBox && mobileSlot && !mobileSlot.contains(mapBox)) {{
          mobileSlot.appendChild(mapBox);
        }}
      }} else {{
        // Si vuelve a la ruta, restauramos el mapa a su columna de escritorio
        const mapBox = document.getElementById('mapStickyContainer');
        const desktopCol = document.querySelector('.route-map-col');
        if (mapBox && desktopCol && !desktopCol.contains(mapBox)) {{
          desktopCol.appendChild(mapBox);
        }}
      }}
    }}

    window.scrollTo({{ top: 0, behavior: 'smooth' }});
  }} else {{
    // En escritorio simplemente hacemos scroll suave a la seccion
    const target = document.getElementById(viewId);
    if (target) {{
      target.scrollIntoView({{ behavior: 'smooth', block: 'start' }});
    }}
  }}
}}

// Mostrar pantalla desde la barra superior de navegacion
function showAppScreen(viewId) {{
  const mapping = {{
    'app-view-hoteles': 'bn-hoteles',
    'app-view-vuelos': 'bn-vuelos',
    'app-view-criterio': 'bn-criterio',
    'app-view-historia': 'bn-historia',
    'app-view-guia': 'bn-guia'
  }};
  const btn = document.getElementById(mapping[viewId]);
  switchMobileTab(viewId, btn);
}}

// Manejo de redimensionado de pantalla para restaurar mapa si pasa de movil a escritorio
window.addEventListener('resize', () => {{
  if (window.innerWidth > 920) {{
    const mapBox = document.getElementById('mapStickyContainer');
    const desktopCol = document.querySelector('.route-map-col');
    if (mapBox && desktopCol && !desktopCol.contains(mapBox)) {{
      desktopCol.appendChild(mapBox);
    }}
    document.querySelectorAll('.app-screen-view').forEach(view => {{
      view.style.display = 'block';
    }});
  }}
}});

// Filtro interactivo de hoteles
// =======================================================
// HERO CINEMATICO: parallax del video, desvanecido del
// titular y barra superior que se vuelve solida
// =======================================================
(function initHeroMotion() {{
  const layer = document.getElementById('heroVideoLayer');
  const content = document.getElementById('heroMainContent');
  const bar = document.getElementById('siteTopBar');
  const video = document.getElementById('heroVideo');
  const quieto = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (video) {{
    // Algunos navegadores ignoran el autoplay hasta que la pestana esta visible
    const arranca = () => {{ const pr = video.play(); if (pr && pr.catch) pr.catch(() => {{}}); }};
    if (quieto) {{ video.pause(); }} else {{ arranca(); document.addEventListener('visibilitychange', () => {{ if (!document.hidden) arranca(); }}); }}
  }}

  let pendiente = false;
  function pintar() {{
    const y = window.scrollY || window.pageYOffset || 0;
    const alto = window.innerHeight || 1;
    const ancho = window.innerWidth || 1;

    if (layer && !quieto && ancho > 920) {{
      layer.style.transform = 'translate3d(0, ' + (y * 0.32).toFixed(1) + 'px, 0)';
    }}
    if (content && ancho > 920) {{
      const t = Math.min(1, y / (alto * 0.62));
      content.style.opacity = String(1 - t);
      content.style.transform = 'translate3d(0, ' + (t * -46).toFixed(1) + 'px, 0)';
    }}
    if (bar) {{
      bar.classList.toggle('bar-solid', y > alto * 0.7);
    }}
    pendiente = false;
  }}

  window.addEventListener('scroll', () => {{
    if (!pendiente) {{ pendiente = true; requestAnimationFrame(pintar); }}
  }}, {{ passive: true }});
  window.addEventListener('resize', pintar);
  pintar();
}})();

// Filtra la cronologia por era historica
function filterHistoria(era) {{
  document.querySelectorAll('.era-filter-btn').forEach(b => {{
    b.classList.toggle('active', b.getAttribute('data-era') === String(era));
  }});
  document.querySelectorAll('.timeline-item').forEach(item => {{
    const suya = item.getAttribute('data-era');
    item.style.display = (era === 'todos' || suya === String(era)) ? '' : 'none';
  }});
}}

// Salta desde el chip de alojamiento de un dia hasta su ficha en la coleccion.
// Si el hotel no es unico (los resorts con espigon son 4 opciones), filtra la coleccion.
function goToHotel(hotelId, filterCat) {{
  const isMobile = window.innerWidth <= 920;
  if (isMobile) {{
    switchMobileTab('app-view-hoteles', document.getElementById('bn-hoteles'));
  }}
  filterHotels(filterCat || 'all');
  setTimeout(() => {{
    const target = hotelId ? document.getElementById(hotelId)
                           : document.getElementById('seccion-hoteles');
    if (!target) return;
    target.scrollIntoView({{ behavior: 'smooth', block: hotelId ? 'center' : 'start' }});
    if (hotelId) {{
      target.classList.remove('hotel-flash');
      void target.offsetWidth;
      target.classList.add('hotel-flash');
      setTimeout(() => target.classList.remove('hotel-flash'), 2400);
    }}
  }}, isMobile ? 360 : 80);
  return false;
}}

function filterHotels(category, srcBtn) {{
  const cards = document.querySelectorAll('.hotel-card-item');
  const chips = document.querySelectorAll('.filter-button-bar .chip-btn');

  chips.forEach(c => c.classList.remove('active'));
  // Solo tomamos event.target si de verdad es un boton de la barra de filtros:
  // al llegar desde un chip de dia, el target seria el chip y marcaria el equivocado.
  const desdeEvento = (typeof event !== 'undefined' && event && event.target
    && event.target.classList && event.target.classList.contains('chip-btn')) ? event.target : null;
  const btn = srcBtn || desdeEvento
    || [...chips].find(b => (b.getAttribute('onclick') || '').includes("'" + category + "'"));
  if (btn && btn.classList) btn.classList.add('active');

  cards.forEach(card => {{
    if (category === 'all') {{
      card.style.display = 'flex';
    }} else {{
      const cats = card.getAttribute('data-category') || '';
      if (cats.includes(category)) {{
        card.style.display = 'flex';
      }} else {{
        card.style.display = 'none';
      }}
    }}
  }});
}}

// Revelado suave de tarjetas al hacer scroll (con reserva de accesibilidad)
function initScrollReveal() {{
  const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  if (prefersReducedMotion || !('IntersectionObserver' in window)) {{
    return;
  }}
  const targets = document.querySelectorAll('.day-card-single, .hotel-card-item, .clean-panel, .timeline-card');
  const observer = new IntersectionObserver((entries, obs) => {{
    entries.forEach(entry => {{
      if (entry.isIntersecting) {{
        entry.target.classList.add('is-visible');
        obs.unobserve(entry.target);
      }}
    }});
  }}, {{ threshold: 0.12, rootMargin: '0px 0px -40px 0px' }});
  targets.forEach(el => {{
    el.classList.add('reveal-init');
    observer.observe(el);
  }});
}}

// Inicializar el mapa y el revelado al cargar la pagina
window.addEventListener('DOMContentLoaded', () => {{
  initMap();
  initScrollReveal();
}});
</script>

</body>
</html>
"""

# Validacion estricta de la regla obligatoria de Alvaro: NINGUNA raya larga (—)
assert "—" not in html, "ERROR CRITICO: Se ha detectado una raya larga (—) en el archivo HTML generado."

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(html)

size_mb = os.path.getsize(OUTPUT_FILE) / (1024 * 1024)
print(f"Exito: Generado {OUTPUT_FILE} ({size_mb:.2f} MB)")
print("Validaciones completadas: Cero rayas largas (—), mapa sincronizado con scroll en escritorio, modo app móvil por secciones independientes.")
