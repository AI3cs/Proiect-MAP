# Aplicație pentru gestionarea unei biblioteci mici

Un sistem complet de management pentru o bibliotecă mică, scris în Python.

## Autor

- **Nume:** Anufriev Alexandr
- **Grupă:** 1.1
- **Email:** alexandranufriev@student.upt.ro
- **An academic:** 2025-2026

## Descriere

Library Manager este o aplicație CLI (Command Line Interface) destinată gestionării eficiente a unei biblioteci de dimensiuni mici. Aplicația rezolvă problema organizării cărților, permițând bibliotecarului să țină o evidență clară a stocului, a utilizatorilor și a împrumuturilor. Prin automatizarea calculelor de penalități și a verificării disponibilității, sistemul elimină erorile umane și simplifică procesul de administrare.

> **📚 Documentație:** Pentru un ghid detaliat al tuturor funcționalităților și comenzilor, consultați [Manualul de Utilizare](./docs/manual_utilizare.md).

## Tehnologii folosite
- **Limbaj:** Python 3.12
- **Biblioteci:**
  - `argparse` - pentru gestionarea argumentelor din linia de comandă
  - `json` - pentru persistența datelor
  - `csv` - pentru importul și exportul datelor
  - `datetime` - pentru gestionarea datelor calendaristice și calculul penalităților
  - `unittest` - pentru testarea automată a funcționalităților
- **Tools:** Git, Docker, GitHub Actions

## Cerințe sistem
- **Python 3.12+** 
- **Git** (pentru clonare)
- **Docker** (pentru rularea în container)
- **Sistem de operare:** Windows, Linux sau macOS

## Instalare (Clonare)

```bash
git clone https://github.com/AI3cs/Proiect-MAP.git
cd Proiect-MAP
```

## Exemple de utilizare

> **Notă:** Comenzile diferă în funcție de sistemul de operare:
> - **Windows:** folosiți `.\library_manager`
> - **Linux/macOS:** folosiți `python3 src/main.py`

### Vizualizarea comenzilor disponibile (Help)
Pentru a vedea toate comenzile și opțiunile disponibile:

**Windows:**
```powershell
.\library_manager --help
```

**Linux/macOS:**
```bash
python3 src/main.py --help
```

### 1. Adăugarea unei cărți noi

Adaugă o carte în inventar specificând detaliile necesare.

**Windows:**
```bash
.\library_manager add_book "1984" "G. Orwell" --isbn 9780451524935 --category "Fiction"
```

**Linux/macOS:**
```bash
python3 src/main.py add_book "1984" "G. Orwell" --isbn 9780451524935 --category "Fiction"
```

### 2. Împrumutarea unei cărți
Înregistrează un împrumut pentru un utilizator existent.

**Windows:**
```bash
.\library_manager borrow "1984" --user_id 1001 --days 14
```

**Linux/macOS:**
```bash
python3 src/main.py borrow "1984" --user_id 1001 --days 14
```

### 3. Generarea unui raport de întârzieri
Verifică ce cărți nu au fost returnate la timp și calculează penalitățile.

**Windows:**
```bash
.\library_manager report --overdue
```

**Linux/macOS:**
```bash
python3 src/main.py report --overdue
```

### 4. Căutare avansată
Caută cărți după un anumit autor.

**Windows:**
```bash
.\library_manager search "Orwell" --type author
```

**Linux/macOS:**
```bash
python3 src/main.py search "Orwell" --type author
```

### 5. Export de siguranță (Backup)
Exportă toate datele din sistem într-un folder de backup pentru siguranță.

**Windows:**
```bash
.\library_manager export data/backup
```

**Linux/macOS:**
```bash
python3 src/main.py export data/backup
```

> **💡 Notă:** Folosiți calea `data/backup` pentru a vă asigura că datele sunt salvate în folderul proiectului și nu se pierd.

## Funcționalități implementate
- Gestiune Cărți (Adăugare, Ștergere, Căutare, Listare)
- Gestiune Utilizatori (Înregistrare, Dezactivare, Reactivare)
- Sistem Împrumuturi (Check-out, Check-in, Calcul Penalități)
- Rapoarte și Statistici (Topuri, Grafice ASCII, Filtrare)
- Persistență Date (Salvare automată în JSON)
- Import/Export CSV (Migrare date)

## Structura proiectului
```
proiect/
├── src/
│   └── main.py             - Codul sursă principal al aplicației
├── data/
│   └── library_data.json   - Baza de date în format JSON (generată automat)
├── docs/
│   └── manual_utilizare.md - Documentație extinsă pentru utilizatori
├── tests/
│   ├── __init__.py         - Marker pentru pachetul de teste
│   └── test_main.py        - Teste unitare
├── .gitignore              - Fișiere excluse din sistemul de versionare
├── Dockerfile              - Configurare pentru containerizare Docker
├── library_manager.bat     - Script utilitar pentru rulare rapidă pe Windows
└── README.md               - Documentația principală a proiectului
```

## Decizii de design
1. **Stocare JSON vs SQL**: Am ales să folosesc fișiere JSON pentru stocarea datelor în locul unei baze de date SQL.
   - *Motiv:* Pentru o bibliotecă mică, setup-ul unui server SQL este o complexitate inutilă. JSON oferă portabilitate maximă (fișierul poate fi copiat/mutat ușor) și este nativ în Python, permițând o dezvoltare rapidă fără dependențe externe grele.
2. **Arhitectură Monolitică Modulară**: Am păstrat tot codul într-un singur fișier (`main.py`) dar organizat în clasă (`LibraryManager`).
   - *Motiv:* Simplifică procesul de livrare și rulare pentru utilizator (un singur script de rulat). Structura internă a clasei separă logic metodele de gestionare (cărți, utilizatori, împrumuturi), păstrând codul curat.

## Probleme întâlnite și soluții
**Problemă:** Ștergerea cărților duplicate (mai multe cărți cu același titlu dar ISBN diferit).
**Soluție:** Am implementat un sistem de identificare prin ISBN. Dacă utilizatorul cere ștergerea după titlu și există duplicate, sistemul verifică dacă argumentul dat este un ISBN valid și șterge cartea corectă. Astfel, nu se șterg accidental cărțile greșite.

**Problemă:** Pierderea datelor la oprirea aplicației.
**Soluție:** Am implementat metodele `_load_data` și `_save_data` care sunt apelate automat la inițializare și după fiecare modificare, asigurând persistența datelor în `library_data.json`.

## Testare
### Cum să rulați testele
Proiectul include o suită de teste folosind modulul standard `unittest`. Pentru a rula toate testele:

**Windows:**
```bash
python -m unittest discover tests/ -v
```

**Linux/macOS:**
```bash
python3 -m unittest discover tests/ -v
```

Am testat scenarii pozitive (adăugare corectă, împrumut reușit) și scenarii negative (împrumut carte inexistentă, validare ISBN duplicat), asigurând robustețea aplicației.

## Docker

> ⚠️ **IMPORTANT - Persistența datelor:** Comenzile care modifică date (add_book, borrow, export, etc.) necesită `-v "${PWD}/data:/app/data"` pentru a salva modificările pe calculatorul dumneavoastră. **Fără `-v`, datele există doar în container și dispar când acesta se oprește!** Comenzile `stats` și `list` pot fi rulate fără `-v` pentru testare rapidă.

### Opțiunea A: Folosește Imaginea de pe DockerHub (Recomandat)
Fără să clonați proiectul, puteți rula direct:
```bash
docker pull alx17608/library-manager:latest
docker run alx17608/library-manager:latest stats
```

> **Linux:** Dacă primiți eroarea `permission denied`, adăugați `sudo` înaintea comenzilor (vedeți secțiunea Permisiuni Docker mai jos).

**Mod Interactiv (cu persistență):**
```powershell
docker run -it -v "${PWD}/data:/app/data" --entrypoint /bin/sh alx17608/library-manager:latest
```
Apoi în container: `library_manager add_book "Carte" "Autor"` → `exit`

---

### Opțiunea B: Build Local
După clonarea repo-ului:
```bash
docker build -t library-manager .
docker run library-manager stats
```

> **Linux:** Dacă primiți eroarea `permission denied`, adăugați `sudo` înaintea comenzilor sau configurați grupul docker (vedeți secțiunea Permisiuni Docker mai jos).

**Mod Interactiv (cu persistență):**
```bash
docker run -it -v "${PWD}/data:/app/data" --entrypoint /bin/sh library-manager
```

În modul interactiv, rulați comenzile **direct cu `library_manager`** (fără `python3 src/main.py`):
```bash
# În container:
library_manager stats
library_manager add_book "Test" "Autor"
library_manager export data/backup
exit
```

> **💡 Notă:** Comanda `library_manager` funcționează doar **înăuntrul containerului Docker**. Dacă rulați aplicația direct pe Linux/macOS (fără Docker), folosiți `python3 src/main.py`.

#### 💾 Import/Export în modul interactiv

Când lucrați în modul interactiv Docker, **asigurați-vă că exportați datele în folderul montat** (`data/`):

**✅ Corect** (datele rămân pe calculatorul dumneavoastră):
```bash
library_manager export data/backup
```

**❌ Greșit** (datele se pierd la ieșirea din container):
```bash
library_manager export backup
```

---

### Comenzi Utile Docker 
> **Notă:** Înlocuiți `library-manager` cu `alx17608/library-manager:latest` dacă folosiți **Opțiunea A** (imaginea de pe DockerHub).

| Acțiune | Comandă |
|---------|---------|
| Adăugare carte | `docker run -v "${PWD}/data:/app/data" library-manager add_book "1984" "Orwell"` |
| Listare cărți | `docker run -v "${PWD}/data:/app/data" library-manager list` |
| Export backup | `docker run -v "${PWD}/data:/app/data" library-manager export data/backup` |
| Import CSV | `docker run -v "${PWD}/data:/app/data" library-manager import data/carti.csv` |

> **Notă:** Docker vede doar fișierele din folderul `data`. Dacă aveți fișierul pe Desktop, copiați-l întâi în `data/`!

---

### Permisiuni Docker (Linux)

Dacă primiți eroarea `permission denied while trying to connect to the Docker daemon socket`, adăugați `sudo` înaintea oricărei comenzi Docker:

```bash
# Adăugați sudo înaintea oricărei comenzi Docker:
sudo docker pull alx17608/library-manager:latest
sudo docker run alx17608/library-manager:latest stats
sudo docker build -t library-manager .
```



## Resurse folosite
- [Documentație Python argparse](https://docs.python.org/3/library/argparse.html)
- [Python JSON Module](https://docs.python.org/3/library/json.html)
- [Unit Testing framework](https://docs.python.org/3/library/unittest.html)

## Contact
Pentru întrebări: alexandranufriev@student.upt.ro