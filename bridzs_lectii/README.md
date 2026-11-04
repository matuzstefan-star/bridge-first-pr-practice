# Lecții de bridge 2/1 (în maghiară) pentru prietenul lui Steffy

Generatorul lecțiilor de bridge (sistemul 2/1 GF), scrise în maghiară. Steffy le ține pe WhatsApp.

## Fișiere

| Fișier | Ce face |
|---|---|
| `bridzs_doc.py` | Funcțiile comune: validarea donelor (13 cărți/mână, 52 distincte, puncte) și documentul Word. Conține și donele Lecției 1 (`DEALS`, `BASICS_1`). |
| `lecke2.py` | Donele, temele și dicționarul Lecției 2. |
| `cards.py` | Imaginile PNG: `_barat` = doar mâna prietenului (Sud), `_Steffy` = toate cele 4 mâini. |
| `export_desktop.py` | Copiază imaginile ca JPG plus documentele Word în `Desktop\Bridzs lectii\Lectia N\{Pentru prieten, Pentru mine}`. |

## Cum se generează (din acest folder)

```bash
python -X utf8 bridzs_doc.py "<OUT>/Bridzs_2-1_Lecke_1.docx"
python -X utf8 lecke2.py "<OUT>/Bridzs_2-1_Lecke_2.docx"
python -X utf8 cards.py "<OUT>"
python -X utf8 export_desktop.py "<OUT>" 1 2
```

Pentru o lecție nouă: copiezi `lecke2.py` ca `lecke3.py`, schimbi `DEALS`, temele și dicționarul, apoi adaugi lecția în `cards.py` (bucla din `main`).

Dependențe: `python-docx` și `Pillow`. Pentru verificarea vizuală: Word (export PDF prin COM) și `pymupdf`.
