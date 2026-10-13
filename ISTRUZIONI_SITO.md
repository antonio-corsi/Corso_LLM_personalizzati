# Come attivare il sito Quarto del corso

Questo pacchetto contiene SOLO i file nuovi da aggiungere al repository
`antonio-corsi/Corso_LLM_personalizzati`. Nessun file esistente viene toccato,
con un'unica eccezione dichiarata: `.gitignore` (è quello attuale, `*.pptx`,
con in più le due righe per le cartelle generate da Quarto).

## File contenuti

```
_quarto.yml                   configurazione del sito (menu, sidebar, tema)
index.qmd                     pagina iniziale con il percorso del corso
materiali.qmd                 pagina con PDF, video, infografiche e dataset
.github/workflows/publish.yml pubblicazione automatica su GitHub Pages
.gitignore                    quello esistente + esclusione di _site/ e .quarto/
ISTRUZIONI_SITO.md            questo file (si può eliminare dopo l'attivazione)
```

## Passi di attivazione (10 minuti)

```bash
# 0. Prerequisito una tantum: installare Quarto da https://quarto.org/docs/get-started/
#    (versione Windows: installer .msi; poi riaprire il terminale)
quarto --version

# 1. Scompattare lo zip NELLA RADICE del repository clonato
#    (i file vanno accanto ai notebook, non in una sottocartella)

# 2. Anteprima locale: si apre il browser e si naviga il sito
quarto preview

# 3. Prima pubblicazione (crea il ramo gh-pages e attiva Pages)
quarto publish gh-pages

# 4. Commit e push dei nuovi file: da qui in poi ogni push aggiorna il sito da solo
git add _quarto.yml index.qmd materiali.qmd .github .gitignore
git commit -m "Aggiunto sito Quarto del corso"
git push
```

L'indirizzo del sito sarà:
`https://antonio-corsi.github.io/Corso_LLM_personalizzati/`

## Note tecniche (perché certe scelte)

- **`execute: enabled: false`** in `_quarto.yml`: i notebook vengono resi
  usando gli **output già salvati** nei file `.ipynb`, senza eseguire il codice
  durante la generazione (altrimenti il server di build dovrebbe installare
  PyTorch). Conseguenza: i notebook **3 e 4** sono attualmente salvati *senza*
  output, quindi sul sito appariranno con il solo codice; per mostrarli
  completi basta eseguirli una volta in locale e salvarli con gli output.
- **Nessun file è stato rinominato**: i nomi con spazi funzionano, nei link
  gli spazi sono scritti come `%20`.
- **Il video (33 MB) e tutti i PDF/PNG** vengono copiati nel sito dalla voce
  `resources:` di `_quarto.yml` e restano scaricabili.
- Il **primo run della Action** parte al push del punto 4: controllare l'esito
  nella scheda *Actions* del repository; eventuali errori di render indicano
  file e riga.
- Se in futuro i `.pptx` dovranno essere pubblicati sul sito, togliere
  `*.pptx` dal `.gitignore` e aggiungere `"*.pptx"` alla lista `resources:`.
