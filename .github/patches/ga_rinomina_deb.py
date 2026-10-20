#!/usr/bin/env python3
"""Rinomina il pacchetto .deb di RustDesk costruito da build.py in quello di AssistenzaGelormini (Linux, 20/10/2026).

  ga_rinomina_deb.py <ingresso.deb> <uscita.deb> <nome-minuscolo> <Nome visibile> <ditta> <sito>

Perche' qui e non con i sed di rdgen su build.py: il codice Linux di RustDesk (src/platform/linux.rs) chiama il servizio, il file
.desktop e il processo dell'icona col nome del programma IN MINUSCOLO (get_app_name().to_lowercase()), mentre rdgen rinominava i
file col nome con le maiuscole. Qui tutto prende lo stesso nome minuscolo, e ogni passo si controlla: un percorso o un file
attesi che mancano, o una "rustdesk" rimasta nei file di testo del pacchetto, fermano la costruzione (uscita 1).
"""
import atexit
import hashlib
import os
import re
import shutil
import subprocess
import sys
import tempfile

if len(sys.argv) != 7:
    sys.exit(__doc__)
ingresso, uscita, nome, visibile, ditta, sito = sys.argv[1:]
if not re.fullmatch(r"[a-z][a-z0-9-]+", nome) or nome == "rustdesk":
    sys.exit("nome del pacchetto non valido: %r" % nome)


def esegui(*cmd):
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit("comando fallito (%d): %s\n%s" % (r.returncode, " ".join(cmd), r.stderr[-2000:]))
    return r.stdout


def leggi(p):
    with open(p, encoding="utf-8") as f:
        return f.read()


def scrivi(p, t):
    with open(p, "w", encoding="utf-8") as f:
        f.write(t)


def sposta(da, a):
    if not os.path.lexists(da):
        sys.exit("atteso e assente: %s" % da)
    if os.path.lexists(a):
        sys.exit("destinazione gia' presente: %s" % a)
    os.rename(da, a)


lavoro = tempfile.mkdtemp(prefix="ga-deb-")
R = os.path.join(lavoro, "pacchetto")
atexit.register(shutil.rmtree, lavoro, True)   # anche quando ci si ferma con un errore (NEO 20/10, punto 5)
esegui("dpkg-deb", "-R", ingresso, R)

# preinst ufficiale: "rm -rf /usr/bin/libsciter-gtk.so" da root, senza guardare di chi sia il file (NEO 20/10): il programma
# Flutter non lo usa, sul PC del cliente non si cancella niente che non sia nostro
pre = os.path.join(R, "DEBIAN/preinst")
t = leggi(pre)
riga = "      rm -rf /usr/bin/libsciter-gtk.so\n"
if t.count(riga) != 1:
    sys.exit("preinst: la riga libsciter attesa una volta, trovata %d" % t.count(riga))
scrivi(pre, t.replace(riga, ""))

share = os.path.join(R, "usr/share")
sposta(os.path.join(share, "rustdesk"), os.path.join(share, nome))
sposta(os.path.join(share, nome, "rustdesk"), os.path.join(share, nome, nome))
sposta(os.path.join(share, nome, "files/systemd/rustdesk.service"), os.path.join(share, nome, "files/systemd/%s.service" % nome))
sposta(os.path.join(share, "applications/rustdesk.desktop"), os.path.join(share, "applications/%s.desktop" % nome))
sposta(os.path.join(share, "applications/rustdesk-link.desktop"), os.path.join(share, "applications/%s-link.desktop" % nome))
sposta(os.path.join(share, "icons/hicolor/256x256/apps/rustdesk.png"), os.path.join(share, "icons/hicolor/256x256/apps/%s.png" % nome))
sposta(os.path.join(share, "icons/hicolor/scalable/apps/rustdesk.svg"), os.path.join(share, "icons/hicolor/scalable/apps/%s.svg" % nome))

# file di testo: prima il nome visibile, poi quello minuscolo (percorsi, servizio, comandi, schema dei collegamenti)
testi = [os.path.join(R, "DEBIAN", f) for f in ("control", "postinst", "postrm", "preinst", "prerm")]
testi += [os.path.join(share, nome, "files/systemd/%s.service" % nome),
          os.path.join(share, "applications/%s.desktop" % nome),
          os.path.join(share, "applications/%s-link.desktop" % nome)]
for p in testi:
    t = leggi(p)
    if p.endswith("/control"):
        for chiave, valore in (("Maintainer", "%s <noreply@ga-informatica.com>" % ditta), ("Homepage", sito), ("Package", nome)):
            t, n = re.subn(r"(?m)^%s: .*$" % chiave, "%s: %s" % (chiave, valore), t)
            if n != 1:
                sys.exit("control: %s trovato %d volte invece di 1" % (chiave, n))
    t = t.replace("RustDesk", visibile).replace("rustdesk", nome)
    scrivi(p, t)

# nessuna "rustdesk" deve restare nei file di TESTO del pacchetto (NEO 20/10, punto 4: tutti, non un elenco): DEBIAN, applications,
# files/ del programma; le librerie e i binari restano quelli costruiti
rimasti, guardati = [], 0
for cartella in (os.path.join(R, "DEBIAN"), os.path.join(share, "applications"), os.path.join(share, nome, "files")):
    for base, _, files in os.walk(cartella):
        for f in files:
            p = os.path.join(base, f)
            if f == "md5sums" or os.path.islink(p):
                continue
            with open(p, "rb") as fh:
                b = fh.read()
            if b"\0" in b:
                continue
            guardati += 1
            if b"rustdesk" in b.lower():
                rimasti.append(p[len(R):])
if guardati < len(testi):
    sys.exit("controllo dei testi: guardati %d file, attesi almeno %d" % (guardati, len(testi)))
if rimasti:
    sys.exit("'rustdesk' ancora presente in: %s" % ", ".join(sorted(rimasti)))
if "libsciter" in leggi(pre):
    sys.exit("preinst: libsciter ancora presente")
ctl = leggi(os.path.join(R, "DEBIAN/control"))
if not re.search(r"(?m)^Package: %s$" % re.escape(nome), ctl):
    sys.exit("Package non rinominato nel control")
svc = leggi(os.path.join(share, nome, "files/systemd/%s.service" % nome))
if "ExecStart=/usr/bin/%s --service" % nome not in svc:
    sys.exit("ExecStart del servizio non punta a /usr/bin/%s" % nome)
pi = leggi(os.path.join(R, "DEBIAN/postinst"))
if "ln -f -s /usr/share/%s/%s /usr/bin/%s" % (nome, nome, nome) not in pi or "systemctl enable %s" % nome not in pi:
    sys.exit("postinst non coerente col nome %s" % nome)

# md5sums rifatto sui percorsi nuovi
righe = []
for base, _, files in os.walk(R):
    if os.path.relpath(base, R).split(os.sep)[0] == "DEBIAN":
        continue
    for f in sorted(files):
        p = os.path.join(base, f)
        if os.path.islink(p) or not os.path.isfile(p):
            continue
        with open(p, "rb") as fh:
            righe.append("%s  %s" % (hashlib.md5(fh.read()).hexdigest(), os.path.relpath(p, R)))
scrivi(os.path.join(R, "DEBIAN/md5sums"), "\n".join(sorted(righe, key=lambda r: r[34:])) + "\n")
for s in ("postinst", "postrm", "preinst", "prerm"):
    os.chmod(os.path.join(R, "DEBIAN", s), 0o755)

esegui("dpkg-deb", "--root-owner-group", "-b", R, uscita)
print("pacchetto %s scritto: %s (%d file nel md5sums)" % (nome, uscita, len(righe)))
