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
   ```powershell
   .\library_manager --help
   ```

### Rulare în Docker (Linux)
Dacă folosiți Docker, comanda nu necesită prefixul `.\`:
```bash
library_manager list
```
Pentru detalii despre rularea interactivă cu persistența datelor, consultați `README.md`.

---

## 2. Gestiunea Cărților

### Adăugarea unei cărți
Pentru a adăuga o carte, folosiți comanda `add_book`.
```powershell
.\library_manager add_book "Titlu Carte" "Nume Autor" --isbn 123456789 --category "SF"
```
- **Parametri obligatorii:** Titlu, Autor.
- **Parametri opționali:** ISBN, Categorie, An.

### Căutarea cărților
Puteți căuta după titlu, autor sau categorie:
```powershell
.\library_manager search --author "Eminescu"
.\library_manager search --category "Poezie"
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
```powershell
.\library_manager delete_book "1984"
```

---

## 3. Gestiunea Utilizatorilor

### Înregistrare utilizator
```powershell
.\library_manager add_user "Ion Popescu" --id 101 --email "ion@email.com"
```

### Dezactivare utilizator
Dacă un utilizator nu mai are drepturi, poate fi dezactivat (împrumuturile active rămân valabile până la returnare):
```powershell
.\library_manager delete_user 101
```

### Reactivare utilizator
Un utilizator dezactivat poate fi reactivat oricând:
```powershell
.\library_manager reactivate_user 101
```

---

## 4. Sistemul de Împrumuturi

### Împrumutarea unei cărți
Perioada standard este de 14 zile.
```powershell
.\library_manager borrow "Titlu Carte" --user_id 101 --days 14
```

### Returnarea unei cărți
La returnare, sistemul calculează automat dacă există întârzieri și afișează penalitățile (1 RON / zi).
```powershell
.\library_manager return "Titlu Carte" --user_id 101
```

---

## 5. Rapoarte și Statistici

### Statistici generale
Afișează topul cărților, autorilor și gradul de ocupare al bibliotecii.
```powershell
.\library_manager stats
```

### Rapoarte specifice
- **Întârzieri:**
  ```powershell
  .\library_manager report --overdue
  ```
- **Utilizatori activi:**
  ```powershell
  .\library_manager report --users
  ```

---

## 6. Backup și Restaurare

### Export (Backup)
Salvează toate datele într-un folder specificat.
```powershell
.\library_manager export backup_2026
```

### Import
Adaugă cărți dintr-un fișier CSV extern.
```powershell
.\library_manager import carti_noi.csv
```

---

## 7. Structura Datelor (Dicționar de Date)

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

## 8. Ghid de Rezolvare a Problemelor (Troubleshooting)

### "EROARE! La export trebuie sa dai un FOLDER"
Aplicația detectează dacă s-a cerut export de tip backup (folder) sau catalog (fișier). Asigurați-vă că nu puneți extensia `.csv` dacă doriți backup complet.

### "PermissionError" la ștergerea fișierelor
Dacă primiți erori legate de permisiuni pe Windows, asigurați-vă că niciun fișier `.csv` sau `.json` din folderul `data/` nu este deschis în Excel sau alt editor în timp ce rulați aplicația.


