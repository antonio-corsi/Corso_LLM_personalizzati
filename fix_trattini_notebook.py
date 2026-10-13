# -*- coding: utf-8 -*-
"""
Correzione per Quarto: sostituisce le righe-separatore fatte di soli
trattini (---) con *** nelle celle Markdown dei notebook.

PERCHE' SERVE
-------------
In Quarto una riga `---` preceduta da una riga vuota (o a inizio cella)
apre un blocco di metadati YAML: il testo che segue viene letto come
YAML e, se e' prosa normale, la generazione fallisce con "YAMLException".
In Markdown `***` disegna la stessa identica linea orizzontale di `---`,
ma per Quarto non ha alcun significato speciale: la sostituzione e'
quindi invisibile nell'aspetto e risolutiva per l'errore.

CHE COSA FA (e che cosa NON tocca)
----------------------------------
- Sostituisce una riga di soli trattini (3 o piu') SOLO se e' la prima
  riga della cella oppure e' preceduta da una riga vuota: sono i casi
  che Quarto scambia per apertura YAML.
- NON tocca le righe di trattini precedute da testo (possibili
  "sottolineature" di titolo in stile setext: innocue per Quarto).
- NON tocca nulla dentro i blocchi di codice delimitati da ```.
- NON tocca le celle di codice, gli output, i metadati del notebook.

USO
---
Salvare questo file nella radice del repository (accanto ai notebook)
ed eseguire:
    python fix_trattini_notebook.py
I file vengono modificati sul posto; Git conserva comunque le versioni
precedenti, quindi ogni modifica resta reversibile.
"""

import glob
import json

# Tipi di file da curare: notebook e pagine Markdown.
NOTEBOOK = "*.ipynb"
MARKDOWN = "*.md"


def correggi_righe(righe: list[str]) -> tuple[list[str], int]:
    """
    Riceve le righe di una cella Markdown (ognuna con il proprio '\n'
    finale, come nei notebook) e restituisce (righe corrette, numero
    di sostituzioni fatte).
    """
    nuove: list[str] = []
    sostituzioni = 0
    dentro_codice = False          # vero quando siamo tra due righe ```
    precedente_vuota = True        # la prima riga conta come "dopo vuota"

    for riga in righe:
        contenuto = riga.rstrip("\n")
        s = contenuto.strip()

        # Apertura/chiusura di un blocco di codice recintato (```).
        if s.startswith("```"):
            dentro_codice = not dentro_codice
            nuove.append(riga)
            precedente_vuota = False
            continue

        # Riga di soli trattini, fuori dal codice, dopo riga vuota
        # (o a inizio cella): e' il caso pericoloso -> diventa ***.
        if (
            not dentro_codice
            and s != ""
            and set(s) == {"-"}
            and len(s) >= 3
            and precedente_vuota
        ):
            terminatore = "\n" if riga.endswith("\n") else ""
            nuove.append("***" + terminatore)
            sostituzioni += 1
            precedente_vuota = False
            continue

        nuove.append(riga)
        precedente_vuota = (s == "")

    return nuove, sostituzioni


def correggi_markdown(percorso: str) -> int:
    """
    Applica la stessa cura a un file .md. Se il file inizia con un vero
    blocco di front matter YAML (--- ... --- in testa), quel blocco viene
    conservato cosi' com'e': li' i trattini sono legittimi.
    """
    with open(percorso, encoding="utf-8") as f:
        testo = f.read()

    righe = [r + "\n" for r in testo.splitlines()]
    if testo and not testo.endswith("\n") and righe:
        righe[-1] = righe[-1][:-1]      # l'ultima riga non aveva l'a-capo

    inizio = 0
    # Front matter vero: il file APRE con --- e piu' avanti c'e' la chiusura.
    if righe and righe[0].strip() == "---":
        for i in range(1, len(righe)):
            if righe[i].strip() in ("---", "..."):
                inizio = i + 1          # correggiamo solo da qui in poi
                break

    corrette, n = correggi_righe(righe[inizio:])
    if n:
        with open(percorso, "w", encoding="utf-8", newline="\n") as f:
            f.write("".join(righe[:inizio] + corrette))
    return n


def main() -> None:
    totale = 0
    for percorso in sorted(glob.glob(MARKDOWN)):
        n = correggi_markdown(percorso)
        if n:
            print(f"{percorso}: {n} righe '---' sostituite con '***'")
            totale += n
        else:
            print(f"{percorso}: nessuna modifica necessaria")

    for percorso in sorted(glob.glob(NOTEBOOK)):
        with open(percorso, encoding="utf-8") as f:
            nb = json.load(f)

        fatte = 0
        for cella in nb.get("cells", []):
            if cella.get("cell_type") != "markdown":
                continue
            righe, n = correggi_righe(cella.get("source", []))
            if n:
                cella["source"] = righe
                fatte += n

        if fatte:
            with open(percorso, "w", encoding="utf-8", newline="\n") as f:
                json.dump(nb, f, ensure_ascii=False, indent=1)
                f.write("\n")
            print(f"{percorso}: {fatte} righe '---' sostituite con '***'")
            totale += fatte
        else:
            print(f"{percorso}: nessuna modifica necessaria")

    print(f"\nTotale sostituzioni: {totale}")
    if totale:
        print("Ora rilanciare: quarto preview")


if __name__ == "__main__":
    main()
