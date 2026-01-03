# Aplicație pentru gestionarea unei biblioteci mici

Un sistem complet de management pentru o bibliotecă mică, scris în Python.

## Autor 

- **Nume:** [AnufrievAlexandr] 
- **Grupă:** [1.2] 
- **Email:** [alexandranufriev@student.upt.ro] 
- **An academic:** 2025-2026 

## Descriere 

Library Manager este o aplicație CLI (Command Line Interface)destinată gestionării eficiente a unei biblioteci de dimensiuni mici. Aplicația rezolvă problema organizării fizice și logice a cărților, permițând bibliotecarului să țină o evidență clară a stocului, a utilizatorilor și a împrumuturilor. Prin automatizarea calculelor de penalități și a verificării disponibilității, sistemul elimină erorile umane și simplifică procesul de administrare.

## Tehnologii folosite
- **Limbaj:** Python 3.10+
- **Biblioteci:**
  - `argparse` - pentru gestionarea argumentelor din linia de comandă
  - `json` - pentru persistența datelor
  - `csv` - pentru importul și exportul datelor
  - `datetime` - pentru gestionarea datelor calendaristice și calculul penalităților
  - `unittest` - pentru testarea automată a funcționalităților
- **Tools:** Git, Docker, GitHub Actions

## Cerințe sistem
- Python 3.10 sau mai nou
- Sistem de operare: Windows, Linux sau macOS
- Docker (opțional, pentru rularea în container)

## Instalare 

```bash 
# Clone repository
 git clone https://github.com/username/project.git 
cd project
 
## Exemple de utilizare

### 1. Adăugarea unei cărți noi

Adaugă o carte în inventar specificând detaliile necesare.
```bash
$ python src/main.py add_book "The Great Gatsby" "F. Scott Fitzgerald" --isbn 9780743273565 --category "Classic"
```

### 2. Împrumutarea unei cărți
Înregistrează un împrumut pentru un utilizator existent.
```bash
$ python src/main.py borrow "The Great Gatsby" --user_id 1001 --days 14
```

### 3. Generarea unui raport de întârzieri
Verifică ce cărți nu au fost returnate la timp și calculează penalitățile.
```bash
$ python src/main.py report --overdue
```

### 4. Căutare avansată
Caută cărți după un anumit autor.
```bash
$ python src/main.py search "Orwell" --type author
```

[Includeti minimum 5 exemple diverse care demonstrează toate functionalitătile majore] Functionalităti implementate 
[x] Functionalitate 1 
[x] Functionalitate 2 
[x] Functionalitate 3
[ ] Functionalitate bonus (optional, pentru viitor) 
Structura proiectului 
project/ 
|── src/ 
|       |── main.py          - [descriere] 
|       |── module1.py       - [descriere] 
|       |── module2.py      - [descriere] 
|── data/ 
|      └── example.csv      - [descriere] 
|── tests/ 
       └── test_main.py     -[descriere]  
Decizie de design
 [Explicati 2-3 decizii tehnice importante pe care le-ati luat: 
De ce ati ales această structură de date? 
De ce acest algoritm si nu altul? 
Cum ati rezolvat o problemă complexă?] Probleme întâlnite si solutii 
Problemă: [descriere] Solutie: [cum ati rezolvat] 
Problemă: [descriere] Solutie: [cum ati rezolvat]
 Testare 
# Cum să rulati testele 
[comenzi de test] 
[Descrieti ce ati testat si cum] 
Docker 
# Build imagine 
docker build -t project-name . 

# Rulare container 
docker run project-name [args] Resurse folosite 
[Link documentatie oficială] [Tutorial relevant] 
[Stack Overflow thread util]
 [Articol/blog post] 
Licentă 
MIT License / GPL / etc. 
Contact 
Pentru întrebări: [email] 