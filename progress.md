# Progreso del proyecto: Indonesia 2027, entre templos y dragones

Documento de seguimiento del estado del proyecto, decisiones adoptadas, arquitectura técnica, peticiones e incidencias o limitaciones encontradas.

Última actualización: 4 de septiembre de 2026.

---

## 1. Contexto y objetivos del viaje

* **Viajeros:** Dos personas jóvenes (32 años), muy activas, sin interés en fiesta nocturna ni turismo masificado.
* **Prioridades:** Snorkel de primer nivel (no bucean con botella), naturaleza salvaje y cultura ancestral auténtica sin trampas para turistas.
* **Fechas del viaje:** Salida el 21 de abril y regreso asegurado a Zaragoza el 4 de mayo (14 días naturales, 11 noches netas en Indonesia).
* **Conexiones:** Salida y llegada desde Zaragoza Delicias en tren de alta velocidad enlazando con vuelos internacionales en Madrid (MAD) o Barcelona (BCN).
* **Confort del sueño (requisito crítico):** Máxima comodidad durmiendo. Colchones hoteleros de alta gama contrastados, climatización silenciosa e insonorización.
* **Diseño visual:** Estilo editorial de viaje costero en **modo claro**, aplicando estrictamente la paleta de Sarah Renae Clark: fondo claro porcelana (`#f8fafc`), títulos en cerceta profunda (`#0f766e`), acentos turquesa (`#14b8a6`), detalles coral (`#ea8c84`) y melocotón suave (`#fde8e1`). Cero fondos oscuros.
* **Tipografía:** Títulos con personalidad de playa y resort de lujo (`DM Serif Display`) y cuerpo con máxima legibilidad moderna (`Plus Jakarta Sans`), ambas autoalojadas en base64 (ver sección 2-G).

---

## 2. Decisiones de diseño y mejoras aplicadas

### A. Sincronización del mapa con scroll en escritorio (estilo China 2027)
* **Cuadrícula en dos columnas (`.routegrid`):** En pantallas grandes (>= 1020px), los 14 días se leen en la columna izquierda mientras el mapa interactivo permanece anclado en la columna derecha de forma pegajosa (`position: sticky; top: 24px`).
* **Unión dinámica de tramos al hacer scroll:** Conforme el usuario baja por la página leyendo los días:
  * El tramo del día activo se enciende con resplandor turquesa y trazo grueso (`active-now`).
  * Los tramos ya recorridos quedan marcados en trazo visible (`done`).
  * La baliza animada de localización (*beacon pulse*) se traslada en tiempo real al nodo de la ciudad o isla donde transcurre la jornada.
  * La barra superior del mapa actualiza dinámicamente el día ("Día 06"), el título exacto del plan y la barra de progreso general de la ruta.

### B. Versión móvil como app nativa por pantallas/secciones independientes
* **Arquitectura de vistas separadas para móvil:** En lugar de forzar un desplazamiento interminable por toda la web en pantallas pequeñas, la versión móvil divide la experiencia en **6 pantallas o vistas exclusivas**:
  1. **Ruta:** El selector de itinerarios, la tabla resumen y las fichas de los 14 días con sus fotos limpias y planes por franjas horarias.
  2. **Mapa:** Pantalla dedicada de mapa a ancho completo con su selector táctil de días (`D1` a `D14`), baliza activa y leyenda.
  3. **Hoteles:** Catálogo interactivo de los 10 alojamientos especiales con botones de filtro rápido (espigón, playa, bambú) y enlaces directos.
  4. **Vuelos:** Panel comparativo de billetes multidestino recomendados frente a falsos ahorros descartados.
  5. **Criterio:** Argumentario técnico de descarte de las Gili tradicionales, Nusa Penida y zonas masificadas del sur.
  6. **Guía (nueva):** Guía práctica de "Antes de viajar" con documentación, salud, dinero, conectividad, clima, equipaje, embajada y gastronomía (ver sección 2-H).
* **Velocidad y rendimiento radical:** La barra inferior fija (`.bottomnav`), ahora con 6 pestañas, conmuta entre pantallas de forma instantánea mediante JavaScript ligero (`switchMobileTab`), ocultando las secciones inactivas para no sobrecargar la memoria del navegador móvil ni fatigar el scroll.
* **Ergonomía táctil:** Soporte de área segura para iPhone (`env(safe-area-inset-bottom)`), botones de más de 44px de zona de contacto y micro-animación elástica al pulsar (`scale(0.92)`).
* **Escritorio:** Las 6 vistas se muestran simultáneamente en cascada vertical (`@media (min-width: 921px)`) y una píldora de navegación superior (`showAppScreen`) permite saltar directamente a cualquier sección, incluida la nueva "Antes de viajar".

### C. Limpieza radical de las fotos
* **Cero carteles sobre la imagen:** Se han eliminado todos los carteles, píldoras y banners opacos que tapaban las fotos en las tarjetas de hoteles y destinos.
* La fotografía se muestra completamente limpia, nítida y visible al 100%.
* Toda la información de etiquetas, tipología de espigón, ubicación y confort de colchón se ubica ordenadamente en el cuerpo inferior de la tarjeta, sobre fondo blanco limpio.

### D. Ampliación fotográfica y reasignación por contenido real
* El banco de fotos ha crecido de 26 a **55 imágenes** verificadas a ojo en `fuentes/hoja_contactos.jpg` (Regla 4). De ellas, **38 se usan activamente** en la web y **17 quedan disponibles mas no usadas** (ver detalle al final de esta sección).
* Se añadieron fotos de transporte (AVE Zaragoza Delicias, Jewel Changi, aeropuerto de Doha), de Java (Taman Sari, Kraton, relieve y amanecer de Borobudur, volcán Merapi, ballet Ramayana, Ratu Boko, gudeg), de Komodo/Flores (Labuan Bajo, muelle de Kelor, Rinca, Kanawa) y de Bali (monte Agung, Tirta Empul, Pura Mengening, canang sari, penjor, Munduk, Ulun Danu Bratan, arrecife de Menjangan) y de gastronomía balinesa (babi guling, nasi campur, bebek betutu, sate lilit, café).
* Un repaso dedicado, contrastando cada tarjeta de día con su texto real, corrigió varias fotos que se repetían entre jornadas distintas sin relación con el contenido descrito: se reasignaron `labuan_bajo` (llegada a Labuan Bajo), `pink_beach` (Isla Padar y Pink Beach), `agung` (arrozales con el monte Agung), `kalong_sunset` (zorros voladores al atardecer), y `pura_kehen` / `sidemen_rice` / `gunung_kawi` / `munduk` / `phinisi_boat` repartidas de forma coherente con el texto de cada día, en lugar de estar duplicadas.
* **Fotos deliberadamente no usadas (17):** `amanjiwo`, `borobudur_relief`, `borobudur_setumbu`, `canang_sari`, `kanawa`, `kelor`, `menjangan_reef`, `merapi`, `penjor`, `pura_mengening`, `ramayana_ballet`, `ratu_boko`, `rinca`, `tirta_empul`, `ulun_danu`, `yogya_kraton`, `yogya_tamansari`. Se han dejado fuera para no saturar de fotos repetidas los mismos días o secciones (varias son variantes alternativas de un lugar ya ilustrado con otra imagen mejor encajada en el texto); quedan disponibles en el banco por si en el futuro se amplía algún día o sección concreta.

### E. Los 14 días descritos individualmente uno a uno
Tanto la **Ruta A (Con Java)** como la **Ruta B (Sin Java)** desglosan ahora los 14 días de forma estrictamente individual:
* **Día 1 a Día 14 individuales:** Cada día cuenta con su propia tarjeta, su fotografía correspondiente, franjas horarias detalladas (Mañana, Tarde, Noche), conexiones exactas (AVE Zaragoza, vuelos domésticos, traslados en lancha rápida y coche privado), recomendaciones gastronómicas locales sin turistadas y consejos prácticos.
* **Correcciones de investigación incorporadas tras verificación cruzada de fuentes:**
  * Día A-3 (Borobudur/Prambanan): añadida nota sobre discrepancia de precios de entrada entre fuentes oficiales y agencias.
  * Día A-5 (Komodo): añadida nota de discrepancia sobre la tasa del parque nacional (tres versiones de precio encontradas según fuente) y referencia al sistema de reserva SIORA.
  * Días A-6 / B-6 (Isla Padar): corregido el número real de escalones/pasos del mirador, antes inexacto.
  * Sección de vuelos: añadida la nueva ruta directa Singapur-Barcelona-Madrid de Singapore Airlines, operativa desde el 27 de octubre de 2026, relevante para quien salga desde Barcelona.

### F. Confort de descanso y enlaces directos en los 10 alojamientos (curados para la Ruta B)
* **Curación por ruta (4 de septiembre de 2026):** a petición expresa del usuario, la colección se depuró para dejar solo alojamientos que están realmente en el recorrido de la Ruta B (sin Java): Menjangan Dynasty Resort, The Menjangan, Bambu Indah (Ubud/Sayan) y los dos hoteles de Lombok (Gili Asahan Eco Lodge y Jeeva Beloam Beach Camp) se retiraron por pertenecer a zonas de la Ruta A o a una extensión de Lombok fuera de las dos rutas del itinerario.
* Para completar de nuevo el objetivo de 10 fichas se investigaron y añadieron 3 alojamientos reales y verificados, todos en zonas que la Ruta B sí visita:
  1. **Wapa di Ume Sidemen** y **Samanvaya Luxury Resort & Spa**, ambos en el valle de Sidemen (Karangasem), la misma zona donde el itinerario ya aloja a la pareja los días 2 a 4.
  2. **Sanak Retreat Bali**, a 5 minutos del pueblo de Munduk, como alternativa a Munduk Moding Plantation en la etapa de montaña de los días 11 a 13.
  * Las tres fichas usan fotos reales verificadas una a una (dormitorio o villa, sin gente reconocible ni carteles) descargadas directamente del dominio oficial de cada hotel, y el detalle de confort de sueño indica explícitamente cuándo la marca del colchón o el aislamiento acústico no ha podido verificarse en ninguna fuente, en vez de inventarlo.
* Sustituido Le Pirate Island por **Komodo Resort & Diving Club (Isla Sebayur)**, con bungalows a pie de playa virgen y muy buena valoración de sueño en reseñas independientes.
* **Corrección factual importante:** la mención anterior a colchones "King Koil" en este hotel no pudo confirmarse en ninguna fuente independiente ni en el marketing oficial del hotel, así que se ha retirado esa afirmación concreta del texto para no dar por hecho un dato no verificado (disciplina de exactitud, ver sección 4).
* Las 10 tarjetas de hotel disponen de botones directos a:
  1. Su **sitio web oficial**.
  2. Su perfil en **Booking.com** (Sanak Retreat Bali enlaza a Tripadvisor en su lugar, al no existir todavía una ficha de Booking.com verificada para ese alojamiento).
  3. Bloque específico de confort de colchón y descanso.
* **Nuevo panel "Avisos de actualidad 2026 antes de confirmar reserva"** en la pantalla de Hoteles, que recoge tres hallazgos de investigación reciente sin ocultar matices:
  1. El terremoto del 15 de agosto de 2026 en la región de Labuan Bajo/Komodo, con confirmación oficial de Komodo Resort & Diving Club y Meruorah Komodo Labuan Bajo de que siguen operando con normalidad.
  2. Una reseña aislada de agosto de 2026 sobre rotación de dirección en TA'AKTANA, presentada como caso no corroborado por otras reseñas.
  3. Plataran Komodo Resort & Spa como alternativa reforzada con espigón sobre el mar (1 Llave MICHELIN, nº1 de 43 hoteles de Labuan Bajo en Tripadvisor).

### G. Autoalojamiento de tipografías (sin dependencia de Google Fonts CDN)
* Las fuentes `DM Serif Display` (normal e itálica) y `Plus Jakarta Sans` (variable, pesos 400 a 800) se descargaron y se embeben directamente en el CSS como `@font-face` en base64, eliminando la llamada externa a `fonts.googleapis.com` que existía antes.
* Refuerza el principio de autocontenido total del documento: la web funciona sin conexión a internet y sin depender de la disponibilidad de servidores de terceros.

### H. Nueva sección "Antes de viajar": guía práctica de documentación, salud, dinero y clima
* Nueva pantalla/vista (`app-view-guia`, pestaña "Guía" en móvil, píldora "Antes de viajar" en escritorio) construida a partir de una investigación dedicada sobre requisitos reales de entrada, salud, dinero, conectividad, clima, equipaje y gastronomía en Indonesia.
* Incluye una franja fotográfica de 3 imágenes (tren AVE, Jewel Changi, aeropuerto de Doha) y una cuadrícula de 8 tarjetas con icono propio:
  1. **Visado y entrada:** coste del VOA, duración de estancia y prórroga, tasa de Bali.
  2. **Salud:** vacunas recomendadas, seguro con rescate.
  3. **Dinero:** presupuesto diario en pareja, moneda, aviso sobre doble comisión y conversión DCC en cajeros.
  4. **Conectividad:** datos prácticos de eSIM/roaming.
  5. **Clima:** qué esperar en la estación seca de abril.
  6. **Equipaje:** recomendaciones específicas para snorkel y trekking ligero.
  7. **Embajada y consulado** (tarjeta ancha): datos de contacto de emergencia en Indonesia.
  8. **Gastronomía** (tarjeta ancha, con franja de 6 fotos): platos locales recomendados sin trampas para turistas (babi guling, nasi campur, bebek betutu, sate lilit, gudeg, café indonesio).
* **Discrepancias de investigación mostradas sin resolver arbitrariamente** (componente reutilizable `.discrepancy-box`), siguiendo el principio ya aplicado en la sección de días y hoteles de no ocultar cuando las fuentes no coinciden:
  1. Muchas webs de viajes afirman que España tiene entrada libre de visado 30 días en Indonesia; sin embargo la normativa vigente (Perpres 95/2024 sobre exención de visado) redujo esa lista a solo 16 países, casi todos del sudeste asiático, y España no figura en ella, por lo que en la práctica se necesita el VOA de pago.
  2. El nivel de riesgo de malaria: los CDC estadounidenses marcan riesgo para ciertas zonas rurales de Indonesia, mientras que fuentes europeas y locales lo describen como bajo para el itinerario turístico planeado; se presentan ambas posturas para que la decisión final de profilaxis sea informada.

### I. Revelado suave de tarjetas al hacer scroll ("más wow" visual)
* Las tarjetas de día (`.day-card-single`), de hotel (`.hotel-card-item`) y los paneles limpios (`.clean-panel`, incluidas las nuevas tarjetas de la Guía) aparecen con una suave transición de opacidad y desplazamiento vertical (`opacity` + `translateY`) al entrar en el viewport, mediante `IntersectionObserver`.
* **Doblemente defensivo:** la animación se desactiva por completo (contenido siempre visible desde el primer render) si el navegador no soporta `IntersectionObserver`, o si el sistema del usuario tiene activada la preferencia `prefers-reduced-motion: reduce`. En ningún caso el contenido puede quedar oculto si falla JavaScript.
* Verificado con pruebas de navegador reales (Playwright) en viewport móvil (390x844) y de escritorio (1440x900): las tarjetas se revelan correctamente al hacer scroll, sin interferir con el estado `active-reading` del día activo ni con la sincronización del mapa en escritorio.

### J. Portada cinematográfica con vídeo de fondo (4 de septiembre de 2026)
* **Petición:** *"rediseña la home, necesito algun video inspiracional de fondo... juega con los contrastes y el scroll...no se, la veo descafeinada"*, con una imagen de referencia (una foto de Raja Ampat publicada por GetYourGuide) y el comentario *"justamente sitios como ese es lo que queriamos para visitar porque son super bonitos"*.
* **Vídeo construido, no descargado.** No existe material de vídeo real y verificado de la ruta con licencia utilizable, y el banco de stock está prohibido por el propio cliente. La solución ha sido montar el vídeo desde cero: `fuentes/hero_loop.mp4`, 20 s en bucle continuo, 1280x720, 24 fps, 1,81 MB, sin audio. Seis planos con zoom lento y desplazamiento (efecto Ken Burns generado frame a frame con PIL, 480 fotogramas) y fundidos encadenados; el último plano funde con el primero para que el bucle no dé salto. Codificado con `libx264`, CRF 34, preset `veryslow`, más una gradación de color (`saturation=1.24`, `contrast=1.06`) para acercarlo al turquesa saturado de la referencia.
* **Origen de los seis planos, todos de Wikimedia Commons con licencia libre y descargados en 3840 px:** Isla Padar (CC BY-SA 4.0, James Mamoto), Pink Beach de Komodo (CC BY-SA 2.0), manta gigante (CC BY-SA 4.0, Daniel Sasse), cascada de Banyumala (CC BY-SA 4.0), terrazas de arroz de Jatiluwih (CC BY-SA 4.0, Anggabuana) y dragón de Komodo en Rinca (CC BY-SA 4.0, Charles J. Sharp).
* **Respuesta honesta sobre la referencia:** se ha advertido al cliente de que la foto que envió es de **Raja Ampat (Papúa Occidental)**, a unos 2.000 km de Komodo, que **no está en ninguna de las dos rutas** y que incluirla exigiría vuelos adicionales vía Sorong. Lo más parecido de su itinerario es Isla Padar, que es justamente el plano de apertura del vídeo.
* **Degradación limpia:** si `hero_loop.mp4` no existe, `build.py` emite una foto fija con el mismo encuadre y velo en lugar del `<video>`, sin romper nada. El vídeo va silenciado, en bucle, con `playsinline`, y se pausa si el sistema tiene `prefers-reduced-motion: reduce`.
* **Contraste y scroll:** velo en dos capas (vertical fuerte solo arriba y abajo, radial suave centrado únicamente detrás del titular) para que el paisaje de los bordes quede vivo en lugar de apagado; parallax del vídeo al 32 por ciento del scroll; desvanecido y elevación del titular; barra de navegación que flota transparente sobre el vídeo y se vuelve blanca sólida al superar el 70 por ciento de la altura de pantalla; y el bloque de contenido claro monta 44 px sobre el hero oscuro con esquinas redondeadas, que es el corte de contraste pedido.
* **Detalle técnico relevante:** la barra tuvo que **salir del `<header class="hero">`** porque el hero declara `isolation: isolate` y creaba un contexto de apilamiento propio, de modo que el `z-index` de la barra quedaba por debajo de `main` y el contenido la tapaba al hacer scroll. En móvil la barra queda en flujo normal con fondo oscuro propio y oculta los dos distintivos de metadatos, que ocupaban tres filas.

### K. Sistema de lugar y mini-chips en las tarjetas de día (4 de septiembre de 2026)
* **Petición:** *"en la pastilla verde dopnde pone relax ahi quiero que pongas siempre el lugar principal: komodo, bali, java... el resto de cosas de relax ponlo en mini empoticonos (alojamiento y que al cliclo te lleve al hotel, si ese dia toca vuelo...) hazlo bien y mejora la UX/UI"*.
* **La pastilla ahora es de lugar y va superpuesta sobre la foto**, arriba a la izquierda, con cristal oscuro difuminado y un punto de color por región: Komodo (turquesa), Bali (verde), Java (ámbar), Flores (índigo claro) y España (gris). Se ha añadido un degradado en la parte superior de cada foto para garantizar el contraste sea clara u oscura la imagen. La antigua `day-pill-badge`, que mezclaba lugar y tema ("Relax y espigón", "Segunda jornada de paraíso"), ha desaparecido del HTML.
* **Fila de mini-chips bajo el titular**, 80 en total repartidos por los 28 días, con iconos SVG de trazo servidos desde un sprite `<symbol>` definido una sola vez y reutilizado con `<use>` (13 iconos: vuelo, tren, cama, ancla, mar, templo, montaña, fauna, sol, agua, gastronomía, hoja y cultura). Los de vuelo van en índigo, el mismo color que el tramo aéreo del mapa; los de noche a bordo en turquesa.
* **Los 13 chips de alojamiento son clicables** y llevan a la ficha del hotel en la colección, que se resalta con una animación al llegar. Se han añadido anclas `id` a las 10 fichas, que no las tenían. Cuando el alojamiento no es único (los cuatro resorts con espigón de Komodo son a elegir), el chip abre la colección ya filtrada por esa categoría. Cuando el hotel no está en la colección (los de Java, que son de la Ruta A), el chip es informativo y no enlaza, en lugar de fingir un enlace roto.
* **Correcciones de la función de filtro:** `filterHotels` dependía del `event.target` global, así que al invocarla desde un chip marcaba como activo el propio chip en vez del botón de filtro. Ahora solo acepta `event.target` si es realmente un botón de la barra, y admite llamada programática.
* **Y un fallo tipográfico:** la flecha del chip enlazable se escribió como `content: "\2197"` dentro del f-string de Python, que interpretó `\21` como escape octal y renderizaba literalmente "97" en pantalla. Sustituido por el carácter directo.

### L. Una sola jornada de relax y reestructuración de ambas rutas (4 de septiembre de 2026)
* **Peticiones:** *"no queremos bautismo de buceo"* y *"en la ruta A tambien tienes que quitar la Segunda jornada de relax en la playa virgen y atardecer en el mar para poder hacer y ver ms cosas. con este criterio de una noche de relax quiza puedas reestructurar parte de las rutas a y b para aprovechar mejor el viaje y ver mas cosas"*.
* **Fuera el bautismo de buceo (día 10 de la Ruta B).** El *Discover Scuba Diving* se ha sustituido por snorkel guiado en Tatawa Kecil y Sebayur Kecil, y el dato de precio del buceo por el argumento real de que los mejores fondos del parque están entre 1 y 4 metros y se ven igual de bien en superficie.
* **Ruta A, día 9:** las dos jornadas de relax se han fusionado en una sola, que absorbe lo mejor de ambas (snorkel desde el espigón y paddle por la mañana, masaje en pareja y cena de pescado a la brasa en el espigón por la tarde). Se ha añadido un apartado que explica por qué solo una noche de playa.
* **Ruta A, el día liberado va a Bali.** El vuelo de Labuan Bajo a Denpasar se adelanta al día 10 y el día 11 es nuevo: el valle de Sidemen a fondo. Con eso Sidemen pasa de 2 a 3 noches y la Ruta A deja de rozar el valle.
* **Ruta A, día 13 reescrito** para no duplicar el trekking de arrozales que ahora está en el día 11: pasa a ser Iseh, la aldea donde vivieron y pintaron Walter Spies y Theo Meier, con la vista al Agung que sale en sus cuadros.
* **Ruta B, día 13:** era solo el traslado de Munduk al aeropuerto. Ahora incluye Pura Ulun Danu Beratan a primera hora (está en la propia carretera, sin desvío) y las terrazas de Jatiluwih con la ruta blanca de unas dos horas. Los tiempos por tramo dan holgura sobrada con el vuelo nocturno.
* **Ruta B, día 3 enriquecido** con los mismos datos verificados: salida a las 07:00 (única franja con el Agung despejado), telar de songket y destilería de arak.
* **Datos verificados que se han incorporado:** en Sidemen no hay senderos señalizados, solo rutas privadas con guía del pueblo entre 80.000 y 150.000 IDR por persona, porque se camina por fincas en plena cosecha; la demostración privada de songket de hora y media figura a unas 206.600 IDR por persona más 21 por ciento de impuestos (tarifa de 2025-2026, a reconfirmar para 2027); en Tri Eka Buana cerca del 90 por ciento de las familias vive del arak de palma y los trepadores suben entre las 06:00 y las 08:00 y entre las 16:00 y las 18:00; Ulun Danu Beratan subió a 100.000 IDR por adulto extranjero el 1 de julio de 2026; Jatiluwih está en 75.000 IDR más 5.000 de aparcamiento y tiene cinco rutas señalizadas por color; y la ruta Labuan Bajo a Denpasar la cubren solo AirAsia y Batik Air, en 1 h 05 min a 1 h 15 min, con tres salidas antes del mediodía.
* **Tres correcciones factuales detectadas en la investigación:** el *gringsing* (doble ikat) es de **Tenganan**, no de Sidemen, que teje songket y endek; *Telaga Waja* es un **río** de rafting, no un pueblo; y el mirador de Bukit Cinta no está en Sidemen sino a unos 45 min hacia Amlapura.
* **Datos que se han dejado explícitamente sin cerrar** en lugar de rellenarlos con cifras plausibles: el precio y el horario del taller Pelangi no están publicados (hay que llamar); la subida de Jatiluwih a 100.000 IDR que publica una guía no se ha podido corroborar en ningún medio indonesio, así que se muestra la cifra verificada de 75.000 junto al aviso; y los horarios de vuelo de abril de 2027 todavía no se pueden confirmar.
* **Se ha añadido un aviso de seguridad sobre el arak:** hay antecedentes de adulteración con metanol, así que solo se cata con productor conocido o marca registrada.

### M. Fotos corregidas por incoherencia con el contenido (4 de septiembre de 2026)
* **Petición:** *"lo primero es que la cambies porque no pega"*, sobre la foto del día 9 de la Ruta B.
* **Día 9 de la Ruta B:** mostraba una goleta phinisi navegando a vela en un día cuyo contenido es relax en el espigón del resort. Sustituida por el espigón de madera de la isla de Kanawa visto desde el aire, con el arrecife nítido bajo el agua turquesa y las colinas áridas de Komodo al fondo (Wikimedia Commons, `File:Kanawa Island from Above.jpg`, CC BY-SA 4.0, SunDawn). Nueva clave `espigon_arrecife` en el banco.
* **Días 14 de ambas rutas:** mostraban el lago Tamblingan y el templo de Ulun Danu, ambos en Bali, en una jornada que se pasa aterrizando en España y cogiendo el AVE. Ahora cierran las dos con la estación de Zaragoza Delicias, la misma del día 1, lo que además cierra el círculo narrativo.
* **Se descartaron tres candidatas** por no corresponder al contenido: un muelle de hormigón en Komodo, una vista lejana del puerto de Loh Liang con veinte barcos, y una foto oficial de un resort en contraluz donde el agua sale plateada y no se ve el arrecife.
* **Y un fallo del menú:** la barra superior seguía diciendo "12 Alojamientos" cuando la colección se había curado a 10.

### N. Una sola noche en el resort con espigón y reequilibrio de las dos rutas (4 de septiembre de 2026)
* **Petición:** *"en el resort exclusivo con espigón solo nos podemos permitir una noche, cuadra eso bien en todas las opciones de viaje"*.
* **Punto de partida auditado:** la Ruta A dormía **2 noches** en el resort (días 8 y 9) y la Ruta B dormía **3** (días 8, 9 y 10). Había que reubicar una noche en A y dos en B.
* **Decisión del cliente, consultada antes de tocar nada:** las noches liberadas van **a Bali**, y la única noche de resort se aprovecha **de principio a fin** (llegada a mediodía en lugar de al anochecer).
* **Ruta A resultante:** día 8, tortugas en Siaba Besar de camino, llegada al resort a mediodía y tarde entera de arrecife, atardecer y cena en el espigón, la única noche. Día 9, última mañana en el arrecife, vuelo de mediodía y llegada a Sidemen con luz. Los días 10 y 11 son Sidemen a fondo y los templos, y el **día 12 es nuevo**. Sidemen pasa a **4 noches seguidas**.
* **Ruta B resultante:** los dragones se han movido al crucero, igual que ya hacía la Ruta A en Rinca, y el **día 8 concentra Loh Liang, las mantas de Karang Makassar y Taka Makassar**. El resort queda en el día 9 con una sola noche, el día 10 vuela a Munduk y **los días 5 y 12 son nuevos**. Reparto final: 4 noches en Sidemen, 3 en la goleta, 1 en el resort y 3 en Munduk.
* **Día nuevo en las dos rutas, el pecio del USAT Liberty en Tulamben:** un buque de carga de 120 m hundido en 1963, a **30 metros de la orilla** y con la parte alta a **5 metros**, así que se recorre **haciendo snorkel en superficie, sin botella y sin entrada**. De vuelta, Tirta Gangga a media tarde (90.000 IDR, abierto de 06:00 a 19:00), cuando ya se han ido los grupos. Aviso incluido: hay que contar 1 h 30 min a 2 h de coche por trayecto, no lo que estima el navegador, porque es carretera de montaña.
* **Día nuevo en la Ruta B, el trek de Sekumpul:** el conjunto de cascadas del norte, a una hora de Munduk, con unos **274 metros de desnivel** de bajada y subida y entre 324 y 400 escalones a la vuelta. Trek medio entre 125.000 y 150.000 IDR por persona, guía local incluido y obligatorio. Se ha incorporado el **aviso de los falsos controles de carretera**, que hasta 12 km antes piden hasta 250.000 IDR por persona y entregan entradas sin valor: solo se paga en la entrada oficial.
* **Datos de precio que reordenaron el problema.** Consultados con fechas reales (28 al 29 de abril de 2027, 2 adultos, precio total): **AYANA Komodo 164 euros** la noche, 214 a 232 con desayuno; **Sudamala Seraya 272**; **Plataran 422**; **TA'AKTANA 1.118**. Es decir, la noche de resort con espigón **no es intrínsecamente caudosa: depende por completo de cuál de los cuatro se elija**, y AYANA, que es precisamente el del espigón icónico, sale más barato que un buen hotel del pueblo de Labuan Bajo. Esto se ha dejado escrito en la ficha del día para que la elección sea informada.
* **Alternativa descartada con datos:** alargar el crucero una noche más **no ahorra, es lo segundo más caro del viaje**. Prorrateando las tarifas publicadas por persona y viaje, una noche extra de goleta en camarote doble con baño privado sale entre **740 y 1.480 euros para la pareja**, de tres a nueve veces una noche en AYANA o en Sidemen. Además el formato de 4 noches en barco compartido casi no existe: el operador de referencia no publica ni precios ni barcos y remite a chárter privado a 5.300 dólares la noche.
* **Descartes razonados del norte de Bali:** el templo de **Ulun Danu Tamblingan** no da para jornada porque **solapa al cien por cien** con la canoa del lago que ya estaba programada (las canoas salen literalmente de la puerta del templo), así que se integra como ampliación de la actividad existente. **Los delfines de Lovina se han descartado por ética**: está documentado que las barcas persiguen y rodean a los grupos, y la norma de mantenerse a 25 metros no se cumple de forma consistente. Y la isla **Menjangan**, que es el mejor snorkel de la zona, exige pernoctar en Pemuteran y compite mal con el snorkel de Komodo.
* **Dos datos obsoletos corregidos en el documento:** se ha retirado la mención a una tasa de conservación de la Isla Komodo de 3.500.000 IDR, que **se anuló oficialmente en diciembre de 2022** y sigue circulando por webs sin actualizar; y se ha añadido el dato verificado de que desde el **1 de abril de 2026 el parque está limitado a 1.000 visitantes al día con reserva obligatoria por la app SIORA y sin venta en taquilla**, algo que conviene que gestione el operador del barco porque el pago con tarjeta extranjera daba problemas.
* **Verificación pendiente señalada al cliente, no resuelta por nosotros:** los itinerarios publicados de crucero de 3 noches desembarcan en **Loh Liang (Isla Komodo)**, pero hay operadores que llevan a **Loh Buaya (Rinca)** porque el sendero es más corto. El billete del parque sirve para las dos, así que se recomienda exigir por escrito cuál de ellas antes de contratar.

### O. Cronología de la historia de Indonesia (4 de septiembre de 2026)
* **Origen:** era una sección diseñada y redactada en una tanda anterior que quedó sin insertar por la llegada de otras peticiones. Se ha retomado y montado.
* **Contenido:** **30 hitos repartidos en 6 eras**, desde la llegada del Homo erectus a Java hace 1,8 millones de años hasta el terremoto de Flores de agosto de 2026. Las eras son: orígenes humanos (4 hitos), reinos hindú-budistas (6), encuentro con Europa (5), descubrimientos y despertar nacional (4), independencia e Indonesia moderna (7) y Komodo y la actualidad (4).
* **Cada hito cita su base documental** en una línea al pie, y los **5 que siguen en discusión entre especialistas llevan un aviso visible** en la propia tarjeta (por ejemplo la fecha de extinción del Homo floresiensis, o la causa del traslado del reino de Mataram a Java oriental). El criterio es no presentar como cerrado lo que la investigación mantiene abierto.
* **Enfoque editorial:** cada hito conecta con algo que la pareja va a ver. Java central concentra alrededor del 75 por ciento de los fósiles de Homo erectus del mundo y es el trayecto hacia Yogyakarta; el hinduismo de los templos de Sidemen y Munduk es legado directo de la corte javanesa de Majapahit que emigró a Bali; y Flores, camino de Labuan Bajo, es donde vivió el Homo floresiensis.
* **Diseño:** línea de tiempo vertical con un punto por hito coloreado según su era, tarjeta con borde izquierdo del mismo color, y **barra de filtros por era** que oculta y muestra los hitos. Séptima entrada en el menú superior y en la barra inferior del móvil, verificada a 390 px: los siete botones caben a 54 px cada uno sin cortar ningún rótulo ni provocar desborde horizontal. Las tarjetas entran en la animación de revelado por scroll.
* **Corrección de texto necesaria antes de publicar:** el borrador estaba escrito **en ASCII, sin tildes ni eñes**, y eso no era publicable (en español "anos" no significa lo mismo que "años"). Se restauraron **430 palabras acentuadas** y se validó con una comprobación automática que **elimina todos los diacríticos de ambas versiones y exige que el resultado sea idéntico carácter a carácter**, de modo que quedara demostrado que solo se añadieron signos y no se alteró ni una palabra del contenido. Resultado: idénticos, y sintaxis Python válida.

### P. El terremoto de Flores sale de la cronología y pasa a la guía práctica (4 de septiembre de 2026)
* **Problema detectado al montar la cronología:** el hito más reciente, el terremoto de magnitud 7,7 a 7,8 del **15 de agosto de 2026** frente a la costa norte de Nusa Tenggara Oriental, **solo aparecía dentro de la historia**, cuando es el asunto de actualidad que más directamente afecta a este viaje concreto.
* **Por qué importa aquí:** los mayores daños se concentraron en las regencias de Manggarai y Manggarai Oriental, es decir, junto a la propia Labuan Bajo. **El aeropuerto de Labuan Bajo sufrió daños**, los servicios portuarios se suspendieron temporalmente (llegaron a quedar varados cerca de mil turistas en la isla de Padar) y la carretera Trans-Flores quedó cortada por corrimientos de tierra. El itinerario usa ese aeropuerto, ese puerto y esa isla.
* **Solución:** se ha añadido una tarjeta propia en la guía práctica, la primera de las nueve, con las tres comprobaciones concretas que hay que hacer antes de pagar algo no reembolsable (que el aeropuerto opera con normalidad, que el resort y su lancha están operativos, y que la salida a Padar no tiene restricciones) y dónde comprobarlo (USGS y BMKG para lo sismológico; por escrito al hotel y al operador del barco para la operativa real).
* **Contexto temporal honesto:** a comienzos de septiembre de 2026 la reconstrucción seguía en curso. El viaje sale ocho meses después, en abril de 2027, así que lo previsible es que esté normalizado, y así se dice, sin alarmismo pero sin ocultarlo.

### Q. Publicación en GitHub (4 de septiembre de 2026)
* **Petición:** *"subelo a github y dame el enlace"*. Es la primera autorización expresa para actuar sobre GitHub; hasta este momento no se había creado ni subido nada, por la regla de no tocar GitHub sin permiso explícito.
* **Repositorio:** `alvaroalonsoorigen-eng/indonesia-2027-templos-y-dragones`, **público**, rama `main`, 79 ficheros.
* **Web navegable:** GitHub Pages servido desde la raíz de `main`, en `https://alvaroalonsoorigen-eng.github.io/indonesia-2027-templos-y-dragones/`.
* **Decisiones consultadas antes de publicar**, por tener consecuencias difíciles de revertir:
  * **Visibilidad.** Se ofreció repositorio privado (más seguro, pero GitHub no renderiza el HTML y la URL navegable en privado exige GitHub Pro de pago) frente a público con Pages. El cliente eligió **público con web navegable**.
  * **Fechas del viaje.** Se advirtió de que publicar las fechas exactas de un viaje de dos semanas indica a cualquiera cuándo no hay nadie en casa, y que el documento cita Zaragoza como origen. El cliente respondió que **no le preocupa**, así que se publicó sin alterar el contenido.
* **Comprobaciones hechas antes de subir:**
  * **Búsqueda de credenciales** por los patrones habituales (contraseña, secreto, token, clave de API y el correo del usuario). Las coincidencias resultaron ser falsos positivos: el topónimo *"Secret Gilis"* en un script antiguo de descarga y subcadenas dentro de las fotos en base64. **No se subió ninguna credencial.**
  * **Alcance limitado a esta carpeta.** El repositorio se inicializó dentro de `Indonesia 2027 - Templos y dragones`, no en la raíz de `Viajes`, de modo que **los otros proyectos (Brasil, China, Islandia, Pirineos) quedan fuera** y no se han tocado.
  * **Identidad de git.** No había `user.name` ni `user.email` configurados. Se configuraron **solo en este repositorio** (no en la configuración global del usuario) y con el **correo privado de GitHub** (`242413540+alvaroalonsoorigen-eng@users.noreply.github.com`) en lugar del correo real, precisamente porque el repositorio es público y el correo del autor de un commit queda expuesto de forma permanente.
* **Añadidos para la publicación:** un `README.md` que explica qué es el documento, que `index.html` es una salida generada y no se edita a mano, cómo regenerarlo con los dos scripts, el criterio de exactitud seguido y los créditos fotográficos; y un `.gitignore` para el ruido del sistema, los artefactos de verificación en navegador y la caché de Python.

### R. Revisión e integración del movimiento vinculado al scroll (5 de septiembre de 2026)
* **Origen:** los cambios los preparó otro agente (Codex) en local. La petición fue revisarlos, implantarlos y comprobarlos.
* **Qué aporta:** una secuencia de presentación a pantalla completa con Java, Komodo y Bali, con fundidos reversibles gobernados por el scroll; parallax dentro de las fotos de días y hoteles; entrada progresiva de las tarjetas; relleno de color de los titulares; y el vídeo de portada, que ahora se pausa cuando la portada sale de pantalla. El motor va en tres ficheros separados (`scroll-scenes.html`, `scroll-motion.css` y `scroll-motion.js`) que el generador incrusta, sin ninguna dependencia ni petición externa nueva.
* **Comprobaciones que pasó:**
  * **Reproducibilidad.** Se regeneró `index.html` desde cero y salió **idéntico byte a byte** al que había dejado, lo que confirma que no se editó el HTML a mano y que la regla del proyecto se respetó.
  * **Coherencia de las escenas con el itinerario.** Las tres reutilizan fotos ya verificadas de las fichas (`dia-a-2` Borobudur, `dia-a-6` Padar, `dia-a-10` el Agung sobre los arrozales) y sus textos alternativos coinciden con lo que muestran, incluso después de la reestructuración de días de la víspera.
  * **Degradación segura.** Todo el movimiento cuelga de la clase `motion-ready` que añade el script: si el JavaScript falla, las tarjetas quedan opacas, los titulares recuperan color sólido y las escenas no se muestran. Verificado retirando la clase en caliente.
  * **Movimiento reducido.** Con `prefers-reduced-motion: reduce` se omite la secuencia, se pausa el vídeo, desaparecen las transformaciones y siguen presentes los 28 días y los 30 hitos.
  * **Funcionalidad intacta:** las dos rutas, la sincronización del mapa, los filtros de hoteles y de eras, el salto del chip de día a la ficha del hotel y las siete pantallas del móvil.
* **Regresión encontrada y corregida.** La inclinación de entrada de las tarjetas (`rotate` sobre `.scroll-enter`) ensancha su caja envolvente y provocaba **barra de scroll horizontal en anchos intermedios: 46 px a 1024 px y 28 px a 1280 px**. Se confirmó que era nueva comparando con la versión publicada anterior (0 px) y se aisló la causa anulando solo la rotación (0 px). Corregido con `overflow-x: clip` en `html` y `body`, que a diferencia de `hidden` **no rompe el `position: sticky` del mapa**, cosa que se verificó expresamente. Resultado: **0 px de desbordamiento en 320, 390, 768, 1024, 1280 y 1440 px**, recorriendo la página entera en cada ancho, y el mapa sigue pegándose correctamente.

---

## 3. Estado de los archivos en la carpeta

```
Indonesia 2027 - Templos y dragones/
├── index.html                      <- Documento de decisión interactivo final (8,5 MB, modo claro, vídeo de portada y 7 secciones)
├── README.md                       <- Presentación del repositorio y cómo regenerar el documento
├── .gitignore                      <- Ruido del sistema y artefactos de verificación
├── AGENTS.md                       <- Instrucciones para el agente y reglas del proyecto
├── progress.md                     <- Este registro de seguimiento y decisiones
└── fuentes/
    ├── build.py                    <- Script generador con mapa sincronizado, modo app y guía práctica
    ├── mapa_land.json              <- Polígonos SVG de la costa de Indonesia (14,8 KB)
    ├── hero_loop.mp4               <- Vídeo de fondo de la portada (20 s en bucle, 1,81 MB, montado a partir de 6 fotos)
    ├── build_cache.py              <- Script que procesa las 54 fotos y genera imgcache.json
    ├── imgcache.json               <- Las 54 fotos en base64 WebP de alta calidad (7,0 MB)
    ├── hoja_contactos.jpg          <- Mosaico de verificación visual de las 54 fotos
    ├── dm_serif_display_normal.woff2    <- Fuente de títulos autoalojada
    ├── dm_serif_display_italic.woff2    <- Fuente de títulos (cursiva) autoalojada
    ├── plus_jakarta_sans_variable.woff2 <- Fuente de cuerpo autoalojada (variable, 400-800)
    └── raw/                        <- Fotos individuales en formato WebP (900x580)
```

---

## 4. Verificaciones de calidad pasadas

* **Cero rayas largas:** Verificado mediante aserción en Python en `index.html` y en `progress.md`.
* **Fotos reales verificadas a ojo:** Las 55 imágenes han sido inspeccionadas en `fuentes/hoja_contactos.jpg`.
* **Autocontenido y sin conexión:** Todas las imágenes, tipografías y el mapa van embebidos en base64 (WebP y WOFF2) y SVG vectorial puro; sin librerías externas ni llamadas de red (incluyendo las fuentes, ya autoalojadas).
* **Paleta y diseño:** Modo claro, fondos limpios porcelana, tipografía playera de revista de viajes y fotos 100% despejadas sin carteles invasivos.
* **Disciplina de exactitud factual:** Ningún dato numérico o afirmativo se ha dado por bueno sin verificación cruzada; cuando las fuentes no coincidían (tasas de parques, riesgo de malaria, requisito de visado), se ha optado por mostrar la discrepancia explícitamente en vez de elegir una versión arbitrariamente. Un dato previamente no verificable (mattress "King Koil" en Komodo Resort Sebayur) se retiró del texto al no encontrar respaldo independiente.
* **Verificación visual real en navegador:** Probado con Playwright en viewport móvil (390x844) y de escritorio (1440x900) tras cada tanda de cambios, incluida la navegación entre las 6 pestañas móviles, el filtro de hoteles, la sincronización del mapa con el scroll y la nueva animación de revelado.

---

## 5. Peticiones del usuario, insistencias y limitaciones encontradas

### A. Peticiones resueltas
1. **Mapa interactivo que se mueve con el scroll como el de China 2027:**
   * *Petición:* El mapa en la versión de ordenador debe unir los tramos conforme se hace scroll y pasan los días.
   * *Resolución:* Implementado diseño en dos columnas en ordenador (`.routegrid`) con el mapa interactivo fijo en el lateral (`position: sticky; top: 24px`). Un observador de scroll (`syncMapScrollPosition`) une los tramos progresivamente, resalta el tramo actual con halo brillante, desplaza la baliza de posición y avanza la barra de progreso conforme se leen los días.
2. **Versión móvil dividida en secciones/pantallas (no solo anclas):**
   * *Petición:* En la versión móvil, el menú de abajo no deben ser solo anclas sino estar dividida la home en secciones para mejorar la carga y velocidad.
   * *Resolución:* En pantallas móviles, la web actúa como una aplicación de pantalla completa, ahora con 6 vistas independientes (`app-view-ruta`, `app-view-mapa`, `app-view-hoteles`, `app-view-vuelos`, `app-view-criterio`, `app-view-guia`). Al pulsar una pestaña en la barra inferior se muestra únicamente la vista solicitada y se ocultan las demás, eliminando la sobrecarga de scroll y maximizando la velocidad y fluidez en el teléfono.
3. **Eliminación de Le Pirate Island y búsqueda de colchón de alta calidad:**
   * *Petición:* Quitar Le Pirate Island por considerarlo glamping con descanso deficiente ("necesitamos colchón sí o sí, la comodidad durmiendo es súper importante").
   * *Resolución:* Sustituido por Komodo Resort & Diving Club en Isla Sebayur Besar. La mención inicial a colchones "King Koil" se retiró tras no encontrar respaldo independiente (ver sección 2-F y 4).
4. **Enlaces directos a web oficial y Booking en todos los alojamientos:**
   * *Petición:* Incluir en todos los hoteles su enlace web oficial y el de Booking.com.
   * *Resolución:* Implementado con dos botones dedicados en cada una de las 12 tarjetas.
5. **Fotos no invasivas y sin carteles encima:**
   * *Petición:* El usuario envió una captura señalando lo invasivos que eran los carteles que tapaban la foto.
   * *Resolución:* Eliminados todos los carteles superpuestos; foto 100% despejada.
6. **Fondo claro con la paleta de Sarah Renae Clark y tipografía playera:**
   * *Petición:* El usuario rechazó el fondo oscuro inicial.
   * *Resolución:* Rediseñado en modo claro con blanco porcelana (`#f8fafc`), títulos en cerceta profunda con DM Serif Display y cuerpo en Plus Jakarta Sans, ambas fuentes ahora autoalojadas (ver sección 2-G).
7. **Días descritos de forma individual uno a uno:**
   * *Petición:* Trabajar y describir cada día por separado.
   * *Resolución:* Los 14 días se detallaron uno a uno sin agrupar fechas.
8. **Eliminación de las píldoras de Estilo y Descanso en la cabecera:**
   * *Petición:* El usuario adjuntó una captura indicando "estas dos cosas quítalas" señalando las etiquetas "Estilo: Cero fiesta · Cero turistadas" y "Descanso: Colchones King Koil / Sealy" del hero.
   * *Resolución:* Eliminadas ambas etiquetas de la barra superior del hero, aligerando el bloque visual de cabecera y conservando únicamente los datos esenciales del viaje (fechas de salida y regreso a Zaragoza, y temporada seca óptima).
9. **Revisión a fondo de contenidos (más y mejor explicados, con investigación previa) y de UX/UI ("más wow") en móvil y escritorio:**
   * *Petición:* "Revisa este proyecto a fondo y mejóralo a nivel de contenidos... y a nivel técnico (también UX y UI más wow). Tanto para móvil como para ordenador."
   * *Resolución:* Investigación dedicada sobre logística Java/Komodo, verificación de hoteles, calendario ceremonial y vuelos en Bali, y una guía práctica completa de antes de viajar; ampliación del banco fotográfico de 26 a 55 imágenes con reasignación cuidadosa por contenido real de cada día; nueva sección "Antes de viajar" con 8 tarjetas temáticas; autoalojamiento de tipografías; nuevo panel de avisos de actualidad 2026 en hoteles; y animación de revelado suave al hacer scroll en tarjetas de día, hotel y paneles, con doble red de seguridad de accesibilidad (sin JS ni con `prefers-reduced-motion`, el contenido es siempre visible).
10. **Curación de la colección de alojamientos para que todos pertenezcan a la Ruta B:**
    * *Petición (4 de septiembre de 2026):* "De los alojamientos de ensueño que me has puesto, deja solo los que estén en la Ruta B y después busca nuevos hasta completar los 10 que te pedí."
    * *Resolución:* Verificado día a día el contenido real de la Ruta B (Sidemen, Komodo y Munduk) para confirmar qué hoteles de la colección estaban genuinamente en ese recorrido. Se retiraron 5 fichas ajenas a la Ruta B: Menjangan Dynasty Resort y The Menjangan (Parque Nacional de Bali Occidental, fuera de ambas rutas), Bambu Indah (Ubud/Sayan, solo en la Ruta A), y Gili Asahan Eco Lodge y Jeeva Beloam Beach Camp (Lombok, una extensión que no forma parte de ninguna de las dos rutas). Se investigaron y añadieron 3 alojamientos reales para volver a completar el objetivo de 10 fichas, con foto verificada del dominio oficial de cada uno: Wapa di Ume Sidemen y Samanvaya Luxury Resort & Spa (ambos en el valle de Sidemen, donde el itinerario aloja a la pareja los días 2 a 4) y Sanak Retreat Bali (a 5 minutos de Munduk, alternativa a Munduk Moding Plantation en los días 11 a 13). Se actualizó el título de la sección, el contador del filtro y el texto introductorio para reflejar el nuevo total de 10 y su curación por ruta (ver sección 2-F).

11. **Portada rediseñada con vídeo de fondo:**
    * *Petición (4 de septiembre de 2026):* "Rediseña la home, necesito algún vídeo inspiracional de fondo, juega con los contrastes y el scroll, no sé, la veo descafeinada", con una foto de referencia de Raja Ampat.
    * *Resolución:* Vídeo de 20 s en bucle montado desde cero con seis fotos de Wikimedia Commons en 3840 px (efecto Ken Burns frame a frame y fundidos encadenados, 1,81 MB), hero a pantalla completa, velo reequilibrado para no apagar el paisaje, parallax, barra flotante que se solidifica y contenido claro montando sobre el hero oscuro. Se advirtió de que la foto de referencia es de Papúa y no está en ninguna de las dos rutas.

12. **Pastilla de lugar y mini-chips de día:**
    * *Petición (4 de septiembre de 2026):* "En la pastilla verde donde pone relax ahí quiero que pongas siempre el lugar principal: Komodo, Bali, Java. El resto de cosas de relax ponlo en mini iconos (alojamiento y que al clic te lleve al hotel, si ese día toca vuelo). Hazlo bien y mejora la UX/UI".
    * *Resolución:* Pastilla de lugar superpuesta sobre la foto con punto de color por región, y 80 mini-chips con iconos SVG en los 28 días. Los 13 chips de alojamiento saltan a la ficha del hotel (anclas nuevas en las 10 fichas) o abren la colección filtrada cuando el hotel es a elegir.

13. **Una sola jornada de relax y reestructuración de las rutas:**
    * *Petición (4 de septiembre de 2026):* "No queremos bautismo de buceo" y "en la Ruta A también tienes que quitar la segunda jornada de relax para poder ver más cosas; con este criterio de una noche de relax quizá puedas reestructurar parte de las rutas A y B para aprovechar mejor el viaje".
    * *Resolución:* Fuera el bautismo de buceo del día 10 de la Ruta B. Las dos jornadas de relax de la Ruta A fusionadas en una, y el día liberado dedicado a Bali: el vuelo se adelanta al día 10 y el día 11 es nuevo (el valle de Sidemen a fondo, con trek al amanecer, telar de songket y arak de palma). El día 13 de la Ruta A pasa a Iseh para no duplicar el trekking. El día 13 de la Ruta B deja de ser un traslado y suma Ulun Danu Beratan y Jatiluwih. Todo con datos verificados y con los huecos reconocidos en lugar de rellenados.

14. **Una sola noche en el resort con espigón:**
    * *Petición (4 de septiembre de 2026):* "En el resort exclusivo con espigón solo nos podemos permitir una noche, cuadra eso bien en todas las opciones de viaje".
    * *Resolución:* Auditadas las noches reales (2 en la Ruta A y 3 en la Ruta B), se consultó al cliente dónde reubicarlas y eligió Bali, con la única noche aprovechada entera. La Ruta A gana el día del pecio del Liberty en Tulamben y sube a 4 noches en Sidemen; la Ruta B mueve los dragones al crucero, gana ese mismo día de Tulamben y el trek de Sekumpul, y queda en 4 noches de Sidemen, 3 de goleta, 1 de resort y 3 de Munduk. Se documentó con precios verificados que la noche de resort la encarece el hotel elegido y no el concepto (AYANA 164 euros frente a TA'AKTANA 1.118), y que una noche extra de goleta habría sido de tres a nueve veces más cara.

15. **Cronología de la historia de Indonesia y aviso del terremoto:**
    * *Petición (4 de septiembre de 2026):* "continua", tras completar la reestructuración de las rutas.
    * *Resolución:* Se retomó la sección de historia que quedaba pendiente de insertar: 30 hitos en 6 eras, cada uno con su base documental y con aviso visible en los 5 que siguen en debate, con filtros por época y séptima pestaña en el móvil. El borrador estaba sin tildes y se corrigió con verificación automática de que no se alteró ninguna palabra. Al montarlo se detectó que el terremoto de Flores de agosto de 2026 solo figuraba en la cronología, así que se le dio tarjeta propia en la guía práctica por afectar al aeropuerto de Labuan Bajo, al puerto y a la isla de Padar, que el itinerario usa.

16. **Publicación en GitHub:**
    * *Petición (4 de septiembre de 2026):* "Súbelo a GitHub y dame el enlace".
    * *Resolución:* Repositorio público `indonesia-2027-templos-y-dragones` con GitHub Pages activado, tras consultar visibilidad y exposición de las fechas del viaje, comprobar que no se subía ninguna credencial, limitar el repositorio a esta carpeta para no arrastrar los otros viajes, y configurar la identidad de git solo en local y con el correo privado de GitHub para no exponer el correo real en un repositorio público.

### B. Limitaciones técnicas y aspectos pendientes
1. **Previsualización automatizada integrada mediante subagente de navegador:** Resuelto en esta sesión mediante el servidor MCP de Playwright, ya disponible; se ha verificado visualmente la web completa en viewport móvil y de escritorio tras cada tanda de cambios relevante.
2. **Precios y compra exacta de billetes de avión para abril de 2027:** Las aerolíneas regulares abren inventario de tarifas con un máximo de 330 a 360 días de antelación; las tarifas finales se concretarán en cuanto se abra la venta.
3. **Datos de visado, tasas y salud sujetos a cambio:** La normativa indonesia de exención de visado y las tasas de parques nacionales han cambiado varias veces en los últimos años; se recomienda reconfirmar estos datos 2 o 3 meses antes de volar (advertencia incluida explícitamente en la nueva sección de guía práctica).
4. **Creación del repositorio remoto en GitHub:** Resuelto el 4 de septiembre de 2026. El usuario autorizó expresamente la subida y el proyecto está publicado en `alvaroalonsoorigen-eng/indonesia-2027-templos-y-dragones`, con GitHub Pages sirviendo la web navegable. Ver el apartado Q.

## 5 de septiembre de 2026: movimiento vinculado al scroll

Petición: aumentar el efecto visual del scroll en la guía de Indonesia y mantener todos los cambios en local hasta nueva autorización.

- Secuencia de presentación con Java, Komodo y Bali, con escenario fijo, apertura del encuadre, zoom, fundidos reversibles y movimiento independiente del texto. Java queda identificado como exclusivo de la Ruta A. Las tres imágenes reutilizan los datos ya incrustados en las fichas del itinerario.
- Portada con movimiento a distintas velocidades en el vídeo, el título y las etiquetas. Enlaces para saltar directamente al selector de rutas desde la portada y la secuencia.
- Parallax dentro de las fotos de días y hoteles, entrada gradual de tarjetas y revelado del color de los títulos. Se conserva el scroll nativo y las tarjetas terminan de entrar antes de alcanzar la zona de lectura.
- Motor propio en `fuentes/scroll-motion.js`, estilos en `fuentes/scroll-motion.css` y presentación en `fuentes/scroll-scenes.html`. El generador los incrusta en el HTML final. Sin nuevas dependencias ni peticiones externas. El HTML pasa de 8.51 a 8.52 MiB, un incremento de 15.459 bytes sobre la versión anterior.
- Se animan las fotos y tarjetas próximas a la ventana, con un fotograma solicitado por evento y sin bucle permanente en reposo. El vídeo se pausa cuando la portada sale de pantalla. El mapa evita actualizar repetidamente el mismo día y queda bajo la barra de navegación.
- Menor amplitud en móvil. La presentación se oculta al entrar en otras pantallas móviles. Se conserva la pantalla activa al cambiar entre móvil y escritorio y se puede volver a la ruta desde la navegación superior.
- La preferencia de reducir movimiento se aplica también si cambia con la página abierta: se omite la secuencia, se detiene el vídeo y quedan visibles los contenidos sin movimiento.

Validación local: build reproducible byte a byte; consola sin errores; ambos itinerarios, sus 28 días y sincronización del mapa; siete pantallas móviles y selector manual del mapa; cuatro filtros de hoteles; enlaces desde el día al alojamiento; cinco anchos (320, 390, 768, 1024 y 1440 px) sin desbordamiento horizontal; cambio de preferencia de movimiento en vivo; todas las imágenes cargadas; ninguna petición externa; apertura directa del HTML en modo sin conexión. Revisados visualmente portada, las tres escenas, itinerario y hoteles en capturas de escritorio y móvil con Chromium local.

Revisado e integrado el 5 de septiembre de 2026, ya con el repositorio publicado y autorizado. Ver el apartado R para el resultado de la revisión y la regresión corregida.
