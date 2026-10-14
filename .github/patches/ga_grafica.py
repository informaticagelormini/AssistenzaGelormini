"""Grafica di Informatica Gelormini sul sorgente di RustDesk (Flutter desktop).

Colori del sito www.informaticagelormini.com (blu #3C6DF0, blu notte #181B31/#1A2240) e riquadro con slogan e contatti
sotto ID e password, in tutte e due le versioni (tecnico e clienti). Ogni sostituzione e' su testo esatto con un numero
di occorrenze atteso: se RustDesk cambia il sorgente la compilazione si FERMA qui invece di produrre un programma diverso
da quello voluto. Si lancia dalla radice del sorgente di RustDesk.
"""
import sys

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

# 2. riquadro Informatica Gelormini sotto ID e password
cambia(HOME, "      if (!isOutgoingOnly) buildPasswordBoard(context),\n",
       "      if (!isOutgoingOnly) buildPasswordBoard(context),\n      gaRiquadroGelormini(context),\n", 1)

RIQUADRO = r'''

// --- Informatica Gelormini (aggiunto in compilazione da .github/patches/ga_grafica.py) ---
const String _gaSito = "https://www.informaticagelormini.com";
const String _gaTelefono = "tel:+393392885800";
const String _gaWhatsApp = "https://wa.me/393392885800";
const String _gaMail = "mailto:info@informaticagelormini.com";
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
