"""Grafica di Informatica Gelormini sul sorgente di RustDesk (Flutter desktop).

Colori del sito www.informaticagelormini.com (blu #3C6DF0, blu notte #181B31/#1A2240) e riquadro con slogan e contatti
(tecnico: sotto ID e password; clienti: in una seconda colonna a destra, punto 5). Ogni sostituzione e' su testo esatto con un numero
di occorrenze atteso: se RustDesk cambia il sorgente la compilazione si FERMA qui invece di produrre un programma diverso
da quello voluto. Si lancia dalla radice del sorgente di RustDesk, con la variante come argomento:
  tecnico  il programma di Antonio (riceve e si collega), senza la voce "Arresta servizio";
  clienti  il programma da dare ai clienti: SOLO ricevere, impostazioni chiuse, senza "Arresta servizio".
"""
import sys

if len(sys.argv) != 2 or sys.argv[1] not in ("tecnico", "clienti"):
    sys.exit("ga_grafica: uso: ga_grafica.py tecnico|clienti")
VARIANTE = sys.argv[1]

def cambia(percorso, vecchio, nuovo, volte):
    with open(percorso, encoding="utf-8") as f:
        testo = f.read()
    trovate = testo.count(vecchio)
    if trovate != volte:
        sys.exit("ga_grafica: in %s trovate %d occorrenze invece di %d di: %r" % (percorso, trovate, volte, vecchio[:80]))
    with open(percorso, "w", encoding="utf-8") as f:
        f.write(testo.replace(vecchio, nuovo))
    print("ga_grafica: %s: %d sostituzioni" % (percorso, volte))

COMMON = "flutter/lib/common.dart"
HOME = "flutter/lib/desktop/pages/desktop_home_page.dart"

# 1. colori
cambia(COMMON, "static const Color accent = Color(0xFF0071FF);", "static const Color accent = Color(0xFF3C6DF0);", 1)
cambia(COMMON, "static const Color accent50 = Color(0x770071FF);", "static const Color accent50 = Color(0x773C6DF0);", 1)
cambia(COMMON, "static const Color accent80 = Color(0xAA0071FF);", "static const Color accent80 = Color(0xAA3C6DF0);", 1)
cambia(COMMON, "static const Color idColor = Color(0xFF00B6F0);", "static const Color idColor = Color(0xFF3C6DF0);", 1)
cambia(COMMON, "static const Color button = Color(0xFF2C8CFF);", "static const Color button = Color(0xFF3C6DF0);", 1)
cambia(COMMON, "scaffoldBackgroundColor: Color(0xFF18191E),", "scaffoldBackgroundColor: Color(0xFF181B31),", 1)
cambia(COMMON, "dialogBackgroundColor: Color(0xFF18191E),", "dialogBackgroundColor: Color(0xFF181B31),", 1)
cambia(COMMON, "cardColor: Color(0xFF24252B),", "cardColor: Color(0xFF1A2240),", 1)

# 2. riquadro Informatica Gelormini sotto ID e password (tecnico); nei clienti va A DESTRA, punto 5
if VARIANTE == "tecnico":
    cambia(HOME, "      if (!isOutgoingOnly) buildPasswordBoard(context),\n",
           "      if (!isOutgoingOnly) buildPasswordBoard(context),\n      gaRiquadroGelormini(context),\n", 1)

RIQUADRO = r'''

// --- Informatica Gelormini (aggiunto in compilazione da .github/patches/ga_grafica.py) ---
const String _gaSito = "https://www.informaticagelormini.com";
const String _gaTelefono = "tel:+393392885800";
const String _gaWhatsApp = "https://wa.me/393392885800";
// 14/10, tecnico: per ora la casella personale; poi una dedicata (assistenza@) quando il server di posta la crea
const String _gaMail = "mailto:a.gelormini@informaticagelormini.com";
const String _gaPrenota = "https://www.informaticagelormini.com/prenota/";

Widget gaRiquadroGelormini(BuildContext context) {
  final scuro = Theme.of(context).brightness == Brightness.dark;
  final testo = scuro ? Colors.white : const Color(0xFF181B31);
  final tenue = scuro ? const Color(0xFFB8C4E6) : const Color(0xFF4A5572);
  Widget pulsante(String etichetta, IconData icona, String indirizzo) => OutlinedButton.icon(
        onPressed: () => launchUrl(Uri.parse(indirizzo)),
        icon: Icon(icona, size: 16),
        label: Text(etichetta),
        style: OutlinedButton.styleFrom(
          foregroundColor: const Color(0xFF3C6DF0),
          side: const BorderSide(color: Color(0xFF3C6DF0)),
          padding: const EdgeInsets.symmetric(horizontal: 10, vertical: 6),
          visualDensity: VisualDensity.compact,
        ),
      );
  return Container(
    margin: const EdgeInsets.fromLTRB(20, 14, 16, 4),
    padding: const EdgeInsets.all(14),
    decoration: BoxDecoration(
      color: scuro ? const Color(0xFF1A2240) : const Color(0xFFF2F5FD),
      borderRadius: BorderRadius.circular(10),
      // un bordo con raggio deve essere uniforme in Flutter: bordo giallo del sito tutto intorno
      border: Border.all(color: const Color(0xFFFBBF24), width: 1.2),
    ),
    child: Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text("Informatica Gelormini",
            style: TextStyle(fontWeight: FontWeight.w700, fontSize: 14, color: testo)),
        const SizedBox(height: 2),
        Text("Un solo referente, sempre lo stesso: risponde direttamente Antonio.",
            style: TextStyle(fontSize: 12, color: tenue)),
        Text("Vent'anni, oltre 300 clienti a Napoli e Caserta.", style: TextStyle(fontSize: 12, color: tenue)),
        const SizedBox(height: 6),
        Text("Lun-Ven 9:00-19:30 · Sab 9:00-13:00", style: TextStyle(fontSize: 11.5, color: tenue)),
        const SizedBox(height: 10),
        Wrap(spacing: 8, runSpacing: 6, children: [
          pulsante("Chiama 339 288 5800", Icons.call, _gaTelefono),
          pulsante("WhatsApp", Icons.chat, _gaWhatsApp),
          pulsante("Scrivici", Icons.mail_outline, _gaMail),
          pulsante("Prenota", Icons.event_available, _gaPrenota),
        ]),
        const SizedBox(height: 8),
        InkWell(
          onTap: () => launchUrl(Uri.parse(_gaSito)),
          child: Text("www.informaticagelormini.com",
              style: const TextStyle(
                  fontSize: 12, color: Color(0xFF3C6DF0), decoration: TextDecoration.underline)),
        ),
        const SizedBox(height: 4),
        Text("Casalnuovo di Napoli (NA) · P.IVA 08419001212", style: TextStyle(fontSize: 10.5, color: tenue)),
      ],
    ),
  );
}
'''
with open(HOME, "a", encoding="utf-8") as f:
    f.write(RIQUADRO)
with open(HOME, encoding="utf-8") as f:
    if f.read().count("Widget gaRiquadroGelormini(") != 1:
        sys.exit("ga_grafica: riquadro non aggiunto una sola volta")
print("ga_grafica: riquadro aggiunto")

# 3. impostazioni fisse scritte nel programma (src/common.rs, load_custom_client).
# Il 18/10 la voce "Arresta servizio" del menu dell'icona ha CANCELLATO il servizio sul PC del laboratorio
# (tray.rs -> platform::uninstall_service: sc delete): in tutte e due le varianti la si nasconde (hide-stop-service,
# che nasconde anche il pulsante nelle impostazioni). Nella variante clienti in piu': solo ricevere
# (conn-type=incoming) e impostazioni chiuse (disable-settings). Il custom.txt firmato di RustDesk non si usa piu'.
COMMONRS = "src/common.rs"
if VARIANTE == "clienti":
    CLIENTI = ('''    log::info!("GA-VERSIONE-CLIENTI: solo ricevere, impostazioni chiuse");
    let mut hard = config::HARD_SETTINGS.write().unwrap();
    hard.insert("conn-type".to_owned(), "incoming".to_owned());
    hard.insert("disable-settings".to_owned(), "Y".to_owned());
    drop(hard);
    // con le impostazioni chiuse la riga di comando (--password per l'accesso senza presidio, da amministratore) resta permessa:
    // core_main.rs is_cli_setting_change_disabled() la blocca se non c'e' questa chiave (NEO 19/10)
    config::BUILTIN_SETTINGS
        .write()
        .unwrap()
        .insert(keys::OPTION_ALLOW_COMMAND_LINE_SETTINGS_WHEN_SETTINGS_DISABLED.to_owned(), "Y".to_owned());
''')
else:
    CLIENTI = '''    log::info!("GA-VERSIONE-TECNICO");
'''
FISSE = ('''
// --- Informatica Gelormini (aggiunto in compilazione da .github/patches/ga_grafica.py) ---
fn ga_impostazioni_fisse() {
    config::BUILTIN_SETTINGS
        .write()
        .unwrap()
        .insert(keys::OPTION_HIDE_STOP_SERVICE.to_owned(), "Y".to_owned());
    // segno della variante dentro librustdesk.dll, controllato dal workflow (valore in una tabella: il compilatore lo tiene)
    config::BUILTIN_SETTINGS
        .write()
        .unwrap()
        .insert("ga-variante".to_owned(), "GA-VERSIONE-%s".to_owned());
''' % VARIANTE.upper() + CLIENTI + '''}
''')
cambia(COMMONRS, "pub fn load_custom_client() {\n    #[cfg(debug_assertions)]\n",
       "pub fn load_custom_client() {\n    ga_impostazioni_fisse();\n    if true {\n        return;\n    }\n    #[cfg(debug_assertions)]\n", 1)
with open(COMMONRS, "a", encoding="utf-8") as f:
    f.write(FISSE)
with open(COMMONRS, encoding="utf-8") as f:
    t = f.read()
    if t.count("fn ga_impostazioni_fisse()") != 1 or t.count("ga_impostazioni_fisse();") != 1:
        sys.exit("ga_grafica: impostazioni fisse non aggiunte una sola volta")
    if (t.count('"conn-type".to_owned(), "incoming"') == 1) != (VARIANTE == "clienti"):
        sys.exit("ga_grafica: solo-ricevere presente/assente in modo diverso dalla variante")
print("ga_grafica: impostazioni fisse aggiunte, variante %s" % VARIANTE)

# 4. rubrica e collegamenti insieme (tutte e due le varianti).
# MISURA 19/10: col tecnico dentro la rubrica (access_token presente) il client 1.5.0 pretende dal server di rendezvous lo scambio di
# chiavi su TCP (client.rs: legacy_secure = !key.is_empty() && (!token.is_empty() || ...) -> secure_tcp) e lo aspetta 18 s:
# "Failed to secure tcp: deadline has elapsed". hbbs gratuito (rustdesk-server 1.1.16, anche master) non lo implementa; il token
# serve solo al server a pagamento. Uscito dall'account il collegamento riesce (provato 12:29 ufficio -> lab). Quindi al server di
# rendezvous non si manda il token, come RustDesk fa gia' per gli "altri server" (stessa riga, ramo other_server). La rubrica (API) e
# la password salvata nella rubrica personale (try_get_password_from_personal_ab) leggono access_token per conto loro: restano.
CLIENTRS = "src/client.rs"
cambia(CLIENTRS, '            (a.as_ref(), b.as_ref(), c.as_ref(), "")\n        } else {\n            (peer, "", key, token)\n        };\n',
       '            (a.as_ref(), b.as_ref(), c.as_ref(), "")\n        } else {\n            // Informatica Gelormini: niente token al server di rendezvous gratuito (ga_grafica.py, punto 4)\n            let _ = token;\n            (peer, "", key, "")\n        };\n', 1)
print("ga_grafica: token non mandato al server di rendezvous")

# 5. finestra del programma clienti quadrata e con altezza massima fissa (solo variante clienti).
# MISURA 19/10, tecnico: la finestra si dimensiona sull'altezza del contenuto (desktop_home_page.dart _updateWindowSize ->
# getIncomingOnlyHomeSize), largo 280; col riquadro sotto diventava cosi' lunga che sul portatile 187300889 "Installa" restava fuori
# dallo schermo e il programma non si poteva installare. Quindi: riquadro in una seconda colonna A DESTRA (la colonna di sinistra con
# ID, password e Installa resta larga 280 e allo stesso posto della ga4), contenuto scorrevole, altezza della finestra al massimo
# gaAltezzaMassima. NEO giri 1-3 NO-GO su un adattamento DINAMICO allo schermo (lettura dell'area utile, timer, riposizionamento:
# ogni giro un caso nuovo, l'ultimo un ciclo fra due monitor): tolto, la misura e' fissa e non legge lo schermo.
if VARIANTE == "clienti":
    cambia(HOME, "        width: isIncomingOnly ? 280.0 : 200.0,\n",
           "        width: isIncomingOnly ? 280.0 + gaLarghezzaRiquadro : 200.0,\n", 1)
    cambia(HOME, '''            Column(
              children: [
                SingleChildScrollView(
                  controller: _leftPaneScrollController,
                  child: Column(
                    key: _childKey,
                    children: children,
                  ),
                ),
                Expanded(child: Container())
              ],
            ),
''', '''            Column(
              children: [
                Expanded(
                  child: SingleChildScrollView(
                    controller: _leftPaneScrollController,
                    child: Row(
                      key: _childKey,
                      crossAxisAlignment: CrossAxisAlignment.start,
                      children: [
                        SizedBox(width: 280.0, child: Column(children: children)),
                        SizedBox(width: gaLarghezzaRiquadro, child: gaRiquadroGelormini(context)),
                      ],
                    ),
                  ),
                ),
              ],
            ),
''', 1)
    cambia(COMMON, '''  return imcomingOnlyHomeSize +
      Offset(magicWidth, kDesktopRemoteTabBarHeight + magicHeight);
}
''', '''  final ga = imcomingOnlyHomeSize +
      Offset(magicWidth, kDesktopRemoteTabBarHeight + magicHeight);
  // Informatica Gelormini (ga_grafica.py, punto 5): mai piu' alta di gaAltezzaMassima, il resto si scorre
  return Size(ga.width, ga.height > gaAltezzaMassima ? gaAltezzaMassima : ga.height);
}

// --- Informatica Gelormini (aggiunto in compilazione da .github/patches/ga_grafica.py, punto 5) ---
const double gaLarghezzaRiquadro = 300.0;
// 520 punti con la barra del titolo: entra nell'area utile di 1280x720 al 125% (576 - 48 di barra delle applicazioni)
const double gaAltezzaMassima = 520.0;
''', 1)
    with open(HOME, encoding="utf-8") as f:
        if f.read().count("gaRiquadroGelormini(context)") != 1:
            sys.exit("ga_grafica: riquadro della variante clienti non messo una sola volta")
    with open(COMMON, encoding="utf-8") as f:
        if f.read().count("const double gaAltezzaMassima = 520.0;") != 1:
            sys.exit("ga_grafica: altezza massima non aggiunta una sola volta")
    # nella colonna di destra (300 punti) i pulsanti in Wrap andrebbero a capo in modo irregolare: due righe da due, stessa larghezza;
    # il numero passa nel testo. Solo clienti: il riquadro del tecnico resta quello della ga4.
    cambia(HOME, '''        Text("Lun-Ven 9:00-19:30 · Sab 9:00-13:00", style: TextStyle(fontSize: 11.5, color: tenue)),
        const SizedBox(height: 10),
        Wrap(spacing: 8, runSpacing: 6, children: [
          pulsante("Chiama 339 288 5800", Icons.call, _gaTelefono),
          pulsante("WhatsApp", Icons.chat, _gaWhatsApp),
          pulsante("Scrivici", Icons.mail_outline, _gaMail),
          pulsante("Prenota", Icons.event_available, _gaPrenota),
        ]),
''', '''        Text("Tel. e WhatsApp 339 288 5800", style: TextStyle(fontSize: 12, color: tenue)),
        Text("Lun-Ven 9:00-19:30 · Sab 9:00-13:00", style: TextStyle(fontSize: 11.5, color: tenue)),
        const SizedBox(height: 10),
        Row(children: [
          Expanded(child: pulsante("Chiama", Icons.call, _gaTelefono)),
          const SizedBox(width: 8),
          Expanded(child: pulsante("WhatsApp", Icons.chat, _gaWhatsApp)),
        ]),
        const SizedBox(height: 6),
        Row(children: [
          Expanded(child: pulsante("Scrivici", Icons.mail_outline, _gaMail)),
          const SizedBox(width: 8),
          Expanded(child: pulsante("Prenota", Icons.event_available, _gaPrenota)),
        ]),
''', 1)
    # a destra della colonna di ID e password lo spazio c'e' gia' (margine destro 11): 4 invece di 20, pulsanti da 122 punti
    cambia(HOME, "    margin: const EdgeInsets.fromLTRB(20, 14, 16, 4),\n", "    margin: const EdgeInsets.fromLTRB(4, 14, 16, 4),\n", 1)
    print("ga_grafica: finestra clienti a due colonne, altezza massima %d" % 520)
