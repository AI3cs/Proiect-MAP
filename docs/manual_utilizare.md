# Manual de Utilizare - Library Manager

## Introducere
Această aplicație este un sistem de gestiune a bibliotecii care rulează în linia de comandă. Permite administrarea cărților, utilizatorilor, împrumuturilor și generarea de rapoarte.

## 1. Instalare și Configurare

### Cerințe
- Python 3.12 sau mai nou instalat.
- Sistem de operare Windows, Linux sau macOS.

### Pași de pornire
1. Deschideți terminalul în folderul proiectului.
2. Rulați comanda de ajutor pentru a verifica dacă totul funcționează:

   **Windows:**
   ```powershell
   .\library_manager --help
   ```
   
   **Linux/macOS:**
   ```bash
   python3 src/main.py --help
   ```

### Rulare în Docker
Dacă folosiți Docker, nu mai este necesar să aveți Python instalat local. Aveți două opțiuni:

**Opțiunea A - Imaginea de pe DockerHub:**
```bash
docker pull alx17608/library-manager:latest
docker run alx17608/library-manager:latest stats
```

**Opțiunea B - Build local:**
```bash
docker build -t library-manager .
docker run library-manager stats
```

**Mod interactiv cu persistență:**
```bash
docker run -it -v "${PWD}/data:/app/data" --entrypoint /bin/sh alx17608/library-manager:latest
# În container:
library_manager add_book "Carte" "Autor"
exit
```

> **Linux:** Dacă primiți eroarea `permission denied`, adăugați `sudo` înaintea comenzilor.

> ⚠️ **IMPORTANT - Persistența datelor:** Flagul `-v "${PWD}/data:/app/data"` montează folderul `data/` în container. **Fără `-v`, toate modificările (exporturi, adăugări de cărți, împrumuturi) SE PIERD când containerul se oprește!** Folosiți întotdeauna `-v` pentru operațiuni cu date.

Pentru detalii complete despre Docker, consultați [README.md](../README.md).

---

## 2. Rularea Testelor
Pentru a verifica integritatea aplicației înainte de utilizare, puteți rula suita de teste automate:

**Windows:**
```powershell
python -m unittest discover tests/ -v
```

**Linux/macOS:**
```bash
python3 -m unittest discover tests/ -v
```

---

## 3. Gestiunea Cărților

### Adăugarea unei cărți
Pentru a adăuga o carte, folosiți comanda `add_book`.

**Windows:**
```powershell
.\library_manager add_book "Titlu Carte" "Nume Autor" --isbn 123456789 --category "SF"
```

**Linux/macOS:**
```bash
python3 src/main.py add_book "Titlu Carte" "Nume Autor" --isbn 123456789 --category "SF"
```

- **Parametri obligatorii:** Titlu, Autor.
- **Parametri opționali:** ISBN, Categorie, An.

### Căutarea cărților
Puteți căuta după titlu, autor sau categorie:

**Windows:**
```powershell
.\library_manager search "Orwell" --type author
.\library_manager search --category "Poezie"
```

**Linux/macOS:**
```bash
python3 src/main.py search "Orwell" --type author
python3 src/main.py search --category "Poezie"
```

### Ștergerea unei cărți
Se poate face după Titlu, ISBN sau ID.

> **Notă:** Dacă există mai multe cărți cu același titlu, aplicația va afișa o listă și vă va întreba care dintre ele doriți să o ștergeți:
> ```
> EROARE! Exista 2 carti cu titlul '1984'.
> Care dintre ele doresti sa o stergi?
>   [ID: 5] 1984 - Orwell (ISBN: 001)
>   [ID: 15] 1984 - Orwell (ISBN: 002)
> Introdu ID-ul corect (sau Enter pentru anulare): _
> ```
> Dacă introduceți un ID greșit, aplicația va cere din nou. Pentru a anula, apăsați Enter fără text.

Exemplu de ștergere:

**Windows:**
```powershell
.\library_manager delete_book "1984"
```

**Linux/macOS:**
```bash
python3 src/main.py delete_book "1984"
```

---

## 4. Gestiunea Utilizatorilor

### Înregistrare utilizator

**Windows:**
```powershell
.\library_manager add_user "Ion Popescu" --id 101 --email "ion@email.com"
```

**Linux/macOS:**
```bash
python3 src/main.py add_user "Ion Popescu" --id 101 --email "ion@email.com"
```

### Dezactivare utilizator
Dacă un utilizator nu mai are drepturi, poate fi dezactivat (împrumuturile active rămân valabile până la returnare):

**Windows:**
```powershell
.\library_manager delete_user 101
```

**Linux/macOS:**
```bash
python3 src/main.py delete_user 101
```

### Reactivare utilizator
Un utilizator dezactivat poate fi reactivat oricând:

**Windows:**
```powershell
.\library_manager reactivate_user 101
```

**Linux/macOS:**
```bash
python3 src/main.py reactivate_user 101
```

---

## 5. Sistemul de Împrumuturi

### Împrumutarea unei cărți
Perioada standard este de 14 zile.

**Windows:**
```powershell
.\library_manager borrow "Titlu Carte" --user_id 101 --days 14
```

**Linux/macOS:**
```bash
python3 src/main.py borrow "Titlu Carte" --user_id 101 --days 14
```

### Returnarea unei cărți
La returnare, sistemul calculează automat dacă există întârzieri și afișează penalitățile (1 RON / zi).

**Windows:**
```powershell
.\library_manager return "Titlu Carte" --user_id 101
```

**Linux/macOS:**
```bash
python3 src/main.py return "Titlu Carte" --user_id 101
```

---

## 6. Rapoarte și Statistici

### Statistici generale
Afișează topul cărților, autorilor și gradul de ocupare al bibliotecii.

**Windows:**
```powershell
.\library_manager stats
```

**Linux/macOS:**
```bash
python3 src/main.py stats
```

### Listarea tuturor cărților
Afișează toate cărțile din bibliotecă:

**Windows:**
```powershell
.\library_manager list
```

**Linux/macOS:**
```bash
python3 src/main.py list
```

### Rapoarte specifice
- **Întârzieri:**

  **Windows:**
  ```powershell
  .\library_manager report --overdue
  ```
  
  **Linux/macOS:**
  ```bash
  python3 src/main.py report --overdue
  ```

- **Împrumuturi Active:**

  **Windows:**
  ```powershell
  .\library_manager report --borrowed
  ```
  
  **Linux/macOS:**
  ```bash
  python3 src/main.py report --borrowed
  ```

- **Cărți Populare:**

  **Windows:**
  ```powershell
  .\library_manager report --popular --top 10
  ```
  
  **Linux/macOS:**
  ```bash
  python3 src/main.py report --popular --top 10
  ```

- **Utilizatori activi:**

  **Windows:**
  ```powershell
  .\library_manager report --users
  ```
  
  **Linux/macOS:**
  ```bash
  python3 src/main.py report --users
  ```

---

## 7. Backup și Restaurare

### Export (Backup)
Salvează toate datele într-un folder specificat.

> **💡 Notă:** Folosiți calea `data/backup_folder` pentru a vă asigura că datele sunt salvate în folderul proiectului.

**Windows:**
```powershell
.\library_manager export data/backup_2026
```

**Linux/macOS:**
```bash
python3 src/main.py export data/backup_2026
```

### Import
Adaugă cărți dintr-un fișier CSV extern.

> **💡 Notă:** Fișierul CSV trebuie să fie în folderul `data/`.

**Windows:**
```powershell
.\library_manager import data/carti_noi.csv
```

**Linux/macOS:**
```bash
python3 src/main.py import data/carti_noi.csv
```

---

## 8. Structura Datelor (Dicționar de Date)

### Cărți (JSON/CSV)
- **id**: Identificator unic numeric (auto-incrementat).
- **isbn**: Cod ISBN unic.
- **status**: `DISPONIBIL` sau `IMPRUMUTAT`.
- **loan_count**: Numărul total de ori când cartea a fost împrumutată.

### Împrumuturi (CSV)
- **loan_date**: Data de început (YYYY-MM-DD).
- **return_date**: Data scadentă calculată (implicit +14 zile).
- **actual_return_date**: Data reală a returnării.
- **penalty**: Valoarea penalității (RON) dacă `actual_return_date` > `return_date`.

---

## 9. Ghid de Rezolvare a Problemelor (Troubleshooting)

### "EROARE! La export trebuie sa dai un FOLDER"
Aplicația detectează dacă s-a cerut export de tip backup (folder) sau catalog (fișier). Asigurați-vă că nu puneți extensia `.csv` dacă doriți backup complet.

### "PermissionError" la ștergerea fișierelor
Dacă primiți erori legate de permisiuni pe Windows, asigurați-vă că niciun fișier `.csv` sau `.json` din folderul `data/` nu este deschis în Excel sau alt editor în timp ce rulați aplicația.


