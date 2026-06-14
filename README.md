# Metal Gear · Enciclopedia progresiva

> Una enciclopedia interactiva de la saga Metal Gear que se desvela a medida que avanzas en los juegos. Sin spoilers involuntarios.

---

## Historia del proyecto

Metal Gear Solid 4 incluye una base de datos enciclopédica complementaria al propio juego: fichas de personajes, organizaciones y tecnología que se van desbloqueando conforme avanzas por los distintos actos del juego. Siempre me pareció una idea brillante y me quedé con ganas de que existiera algo así para toda la saga, no solo para MGS4.

Hace años empecé a construir eso a mano: un documento que ordenara la historia de Metal Gear de forma que pudiera compartirlo con alguien que estuviera jugando la saga por primera vez sin arruinarle nada. La idea era buena pero el proyecto se quedó a medias, demasiado ambicioso para hacerlo solo en los ratos libres, y lo archivé.

Hace poco lo rescaté. Con ayuda de IA pude no solo terminar lo que había empezado, sino llevarlo mucho más lejos de lo que hubiera hecho solo: retratos dinámicos por juego, logos de organizaciones, artwork de los Metal Gear, hiperenlaces entre entradas, diseño responsive, y una lógica de spoilers bastante más sofisticada de la que yo habría implementado a mano.

El resultado es este archivo HTML autocontenido. Sin servidor, sin base de datos, sin dependencias externas. Solo abrirlo y funciona.

> [!NOTE]
> _Lejos de estar terminada, los resúmenes de cada uno de los personajes, grupos, eventos, etc. están aún en continua revisión. Cualquier sugerencia de cambio, (tanto de estos como de mejora de la  web), como corrección de cualquier texto puedes abrirme una [`issue`](https://github.com/Galphie/metal-gear-wiki/issues/new) e informármelo._
> _Muchas gracias por adelantado._ 
---

## Qué es

Una enciclopedia de la saga Metal Gear dividida en cinco secciones:

- **Personajes** — fichas progresivas con artwork del juego más avanzado que hayas completado
- **Organizaciones** — FOXHOUND, Patriots, MSF, XOF y todas las demás, con sus logos
- **Tecnología** — los Metal Gear y otras armas clave de la saga
- **Cronología** — todos los eventos ordenados por fecha dentro de la ficción
- **Eventos históricos** — los grandes incidentes explicados en detalle

## Cómo funciona

En la barra lateral (o en el menú en móvil) marcas los juegos que has completado. La enciclopedia se desvela progresivamente: solo ves la información de los juegos que ya conoces. Si alguien ha jugado hasta MGS3 y no ha tocado MGS4, no verá nada que no deba ver.

Los hiperenlaces entre entradas funcionan igual: si una entrada menciona a Ocelot y su ficha está sellada, el enlace aparece en ámbar e inactivo.

## Uso

Abre `index.html` en el navegador, o visita la versión publicada:

**[galphie.github.io/metal-gear-wiki](https://galphie.github.io/metal-gear-wiki/)**

---

*Construido con Python + Pillow para el procesado de imágenes y un único archivo HTML autocontenido con todo embebido en base64.*
