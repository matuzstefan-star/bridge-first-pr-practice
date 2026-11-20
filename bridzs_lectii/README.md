# Lecții de bridge 2/1 (în maghiară) pentru prietenul lui Steffy

Generatorul lecțiilor de bridge (sistemul 2/1 GF), scrise în maghiară. Steffy le ține pe WhatsApp.

## Fișiere

| Fișier | Ce face |
|---|---|
| `bridzs_doc.py` | Funcțiile comune: validarea donelor (13 cărți/mână, 52 distincte, puncte) și documentul Word. Conține și donele Lecției 1 (`DEALS`, `BASICS_1`). |
| `lecke2.py` | Donele, temele și dicționarul Lecției 2. |
| `lecke3.py` | Lecția 3: 2♣ forte și deschideri slabe de 2. |
| `lecke4.py` | Lecția 4: licitație competitivă (aici adversarii licitează, vezi `opp_note`). |
| `lecke5.py` | Lecția 5: deschiderile de 1♣ și 1♦, răspunsurile. |
| `lecke6.py` | Lecția 6: al doilea anunț al deschizătorului după 1♣/1♦ (forță, reverz, jump shift, NMF). |
| `lecke7.py` | Lecția 7: deschiderea de 2SZ (20–21). |
| `lecke8.py` | Lecția 8: deschiderea de 1SZ (15–17). |
| `lecke9.py` | Lecția 9: licitație competitivă după deschiderea de 1♣/1♦ (intervențiile adversarilor). |
| `cards.py` | Imaginile PNG: `_barat` = doar mâna prietenului (Sud), `_Steffy` = toate cele 4 mâini. |
| `export_desktop.py` | Copiază imaginile ca JPG plus documentele Word în `Desktop\Bridzs lectii\Lectia N\{Pentru prieten, Pentru mine}`. |

## Cum se generează (din acest folder)

```bash
python -X utf8 bridzs_doc.py "<OUT>/Bridzs_2-1_Lecke_1.docx"
python -X utf8 lecke2.py "<OUT>/Bridzs_2-1_Lecke_2.docx"
python -X utf8 lecke3.py "<OUT>/Bridzs_2-1_Lecke_3.docx"
python -X utf8 lecke4.py "<OUT>/Bridzs_2-1_Lecke_4.docx"
python -X utf8 lecke5.py "<OUT>/Bridzs_2-1_Lecke_5.docx"
python -X utf8 lecke6.py "<OUT>/Bridzs_2-1_Lecke_6.docx"
python -X utf8 lecke7.py "<OUT>/Bridzs_2-1_Lecke_7.docx"
python -X utf8 lecke8.py "<OUT>/Bridzs_2-1_Lecke_8.docx"
python -X utf8 lecke9.py "<OUT>/Bridzs_2-1_Lecke_9.docx"
python -X utf8 cards.py "<OUT>" 9        # fără număr = toate lecțiile
python -X utf8 export_desktop.py "<OUT>" 9
```

Pentru o lecție nouă: copiezi ultimul `lecke<N>.py`, schimbi `DEALS`, temele și dicționarul, apoi adaugi lecția în dicționarul `LESSONS` din `cards.py`.

**Atenție:** `export_desktop.py` suprascrie `Desktop\Bridzs lectii\Lectia N`. Verifică întâi ce lecții există deja acolo.

Dependențe: `python-docx` și `Pillow`. Pentru verificarea vizuală: Word (export PDF prin COM) și `pymupdf`.
