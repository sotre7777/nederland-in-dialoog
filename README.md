# Nederland in Dialoog

Een app die een nieuwsbericht in zeven stappen vertaalt naar een eigen afweging, in de taal van elf breed gedragen principes. Van kwestie naar principe, naar wat we al geleerd hebben, naar de afruil, naar wie betaalt, naar wat je zelf doet. Nergens komt een politieke partij voor; die stap zet de gebruiker zelf, met wat hij hier geleerd heeft.

Stand: skelet (25 oktober 2026). Werkt, maar met handmatig gekoppeld nieuws en zonder server.

## De zeven stappen

| Stap | Scherm | Wat de app levert | Regel |
|---|---|---|---|
| 1 Opening | Onderwerpen uit het dagelijkse nieuwsoverzicht; metingen bovenaan | `data/opening.json` | Een meting (CBS, CPB, Rekenkamer) is de schoonste ingang; een incident krijgt een wachttijdlabel |
| 2 Uitzoomen | Twee tot drie principes, elk met de zin uit het bericht die de koppeling draagt | `data/classificatie.json` | De gebruiker kiest. De app kiest nooit. "Geen principe" is een geldige uitkomst |
| 3 Het geleerde | Formulering, beloften, stand per belofte, waar we doorschoten | `data/principes.json` (laag 1 en 3) | Verplichte leestijd: de knop werkt pas als je onderaan bent geweest |
| 4 Afweging | Drie antwoorden: binnen het principe, bij een ander principe, meer belasting | `data/afruilen.json` (laag 2 startset) | Geen vierde knop. "Binnen het principe" vereist dat je noemt wat kleiner wordt |
| 5 Zelfs als | Zin met vaste grammatica en een tijdshorizon | | Alleen de waarom-regel is vrije tekst |
| 6 Mijn deel | De "wat wij zelf doen"-regel van het principe | `data/principes.json` (laag 4, voorlopig) | |
| 7 Terug | Nieuws naast je eigen zin; kopieerbare tekst | | Slotregel: ga hiermee het gesprek aan met de partij waar jij je thuis voelt. Die koppeling maken wij niet |

## Bestanden

```
content/werkdocument-2026-10-25.md   snapshot van het werkdocument (Claude Doc), de bron van alle principetekst
data/principes.json                  elf principes: formulering, beloften, geleerde, scorebord, afruilen, wat wij zelf doen
data/afruilen.json                   startset laag 2: paren van principes, afgeleid uit de formuleringen; niet getoetst
data/classificatie.json              handmatige koppeling nieuwsonderwerp -> principe(s) + dragende zin
data/opening.json                    nieuwsonderwerpen en metingen uit de laatste 3 dagoverzichten, met koppeling
scripts/parse_werkdoc.py             markdown -> secties en principes
scripts/build_principes.py           werkdocument -> data/principes.json
scripts/build_opening.py             nieuwsoverzicht/archief + classificatie -> data/opening.json
scripts/build_app.py                 template + data -> app/index.html
app/template.html                    de app (één pagina, geen build-tooling, marked.js van cdnjs)
app/index.html                       gebouwde app; wordt als Claude-artifact gepubliceerd
```

Bouwen:

```
python3 -I scripts/build_principes.py content/werkdocument-2026-10-25.md data/principes.json
python3 -I scripts/build_opening.py ../nieuwsoverzicht/archief data/classificatie.json data/opening.json 3
python3 -I scripts/build_app.py
```

Het nieuws komt uit [sotre7777/nieuwsoverzicht](https://github.com/sotre7777/nieuwsoverzicht), een dagelijkse cloudtaak die 8–13 onderwerpen en een lijst recente publicaties oplevert.

## Wat nog niet bestaat

- **Automatische koppeling.** `classificatie.json` is met de hand gevuld voor 23–25 oktober. De volgende stap is een dagelijkse taak (zoals het nieuwsoverzicht) die het bestand per nieuw overzicht aanvult met een taalmodel, met dezelfde regels: hoogstens drie kandidaten, per kandidaat de dragende zin, "geen" is een uitkomst. Trefkans tot nu toe: ongeveer de helft van de onderwerpen raakt een principe, en per dag verdient hooguit één bericht de hele cirkel.
- **Trend als reeks.** Het scorebord heeft per belofte een richting als woord ("verbeterd sinds 2021"). Een lijntje per indicator vraagt per belofte één CBS StatLine-tabelcode. Curatiewerk, geen techniek.
- **Startset afruilen (laag 2).** Nu afgeleid uit de kruisverwijzingen in de formuleringen, 18 paren. Moet met de hand worden getoetst en aangevuld.
- **Laag 4 (het WIE).** Alleen de "wat wij zelf doen"-regels; gezin, buurt, markt en overheid als drie actoren is nog niet uitgewerkt.
- **Terugkoppeling.** Elke doorlopen cirkel levert een record op (principe, botsend principe, zin, wie betaalt, horizon). Nu alleen lokaal in de browser. Aggregatie, geanonimiseerd, is de stap naar het signaal voor de overheid uit het werkdocument; de spanning tussen zelfselectie en representativiteit blijft.
- **Eigen onderwerp.** Kan worden ingevoerd, maar zonder koppeling: de gebruiker kiest zelf het principe.

## Niet-onderhandelbaar

Geen partij, geen kabinet, geen bewindspersoon. Niet in de teksten, niet in de koppeling, niet in de uitkomst. Een maatregel is een bijdrage aan een gedeeld doel, wie hem ook nam.
