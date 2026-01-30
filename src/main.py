#!/usr/bin/env python3
import argparse
import csv
import json
import os
import sys
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Fix pentru encoding Unicode pe Windows
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')

# Configurare cai fisiere
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
DATA_FILE = os.path.join(DATA_DIR, 'library_data.json')
DATE_FORMAT = "%Y-%m-%d"
PENALTY_PER_DAY = 1  # 1 RON per zi penalitatea in caz de intarziere

# Creare folder data daca nu exista
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)


class LibraryManager:
    """
    Clasa principala pentru gestionarea bibliotecii.
    Gestioneaza: Books, Users, Loans
    """

    def __init__(self, data_file: str = DATA_FILE):
        """Initializeaza managerul de biblioteca"""
        self.data_file = data_file
        self.data: Dict[str, List[Dict]] = {
            "books": [],
            "users": [],
            "loans": []
        }
        self._load_data()

    def _load_data(self) -> None:
        """Incarca datele din fisierul JSON"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    loaded_data = json.load(f)
                    for key in self.data.keys():
                        if key in loaded_data:
                            self.data[key] = loaded_data[key]
            except json.JSONDecodeError:
                pass

    def _save_data(self) -> None:
        """Salveaza datele in fisierul JSON"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def _generate_book_id(self) -> int:
        """Genereaza un ID unic pentru carte"""
        if not self.data["books"]:
            return 1
        return max(book.get("id", 0) for book in self.data["books"]) + 1

    # Gestionare carti
    
    def add_book(self, title: str, author: str, isbn: str = None,
                 category: str = None, year: int = None) -> None:
        """Adauga o carte noua in biblioteca"""
        # Validare unicitate
        if isbn:
            if any(book.get("isbn") == isbn for book in self.data["books"]):
                print(f"EROARE! O carte cu ISBN {isbn} exista deja!")
                return
        else:
            if any(book.get("title", "").lower() == title.lower() and 
                   book.get("author", "").lower() == author.lower() for book in self.data["books"]):
                print(f"EROARE! Cartea '{title}' de '{author}' exista deja in biblioteca.")
                return

        # Validare an
        if year:
            current_year = datetime.now().year
            if year < 1450 or year > current_year + 1:
                print(f"EROARE! Anul {year} nu este valid (1450-{current_year})!")
                return

        new_book = {
            "id": self._generate_book_id(),
            "title": title,
            "author": author,
            "isbn": isbn if isbn else "N/A",
            "category": category if category else "Necategorizat",
            "year": year,
            "status": "DISPONIBIL",
            "date_added": datetime.now().strftime(DATE_FORMAT),
            "loan_count": 0
        }

        self.data["books"].append(new_book)
        self._save_data()

        print("")
        print("▀" * 50)
        print("      CARTE ADAUGATA CU SUCCES!")
        print("▀" * 50)
        print(f"  ID:        {new_book['id']}")
        print(f"  Titlu:     {title}")
        print(f"  Autor:     {author}")
        print(f"  ISBN:      {new_book['isbn']}")
        print(f"  Categorie: {new_book['category']}")
        if year:
            print(f"  An:        {year}")
        print(f"  Status:    DISPONIBIL")
        print(f"  Data:      {new_book['date_added']}")
        print("▀" * 50)
        print("")

    def list_books(self, status: str = None) -> None:
        """Listeaza toate cartile din biblioteca"""
        books = self.data["books"]

        # Filtrare dupa status
        if status:
            status_upper = status.upper()
            if status_upper == "BORROWED":
                status_upper = "IMPRUMUTAT"
            elif status_upper == "AVAILABLE":
                status_upper = "DISPONIBIL"
            books = [b for b in books if b.get("status", "").upper() == status_upper]

        if not books:
            if not status:
                print("\n Nu exista carti in biblioteca.\n")
            else:
                print(f"\n Nu exista carti cu status '{status}'.\n")
            return

        header_text = "CATALOG BIBLIOTECA" if not status else f"CARTI - {status.upper()}"
        print("")
        print("▀" * 75)
        print(f"  {header_text} ({len(books)} total)")
        print("▀" * 75)
        print(f"{'ID':<4} {'Titlu':<28} {'Autor':<22} {'Status':<12} {'Categorie':<10}")
        for book in books:
            title = book['title'][:26] + ".." if len(book['title']) > 28 else book['title']
            author = book['author'][:20] + ".." if len(book['author']) > 22 else book['author']
            print(f"{book['id']:<4} {title:<28} {author:<22} {book['status']:<12} {book.get('category', 'N/A'):<10}")

        print("▀" * 75)
        print("")

    def search_books(self, query: str, search_type: str = "title") -> None:
        """Cauta carti dupa diferite criterii"""
        query_lower = query.lower()
        results = []

        for book in self.data["books"]:
            found = False
            if search_type == "title" and query_lower in book.get("title", "").lower():
                found = True
            elif search_type == "author" and query_lower in book.get("author", "").lower():
                found = True
            elif search_type == "isbn" and query_lower in book.get("isbn", "").lower():
                found = True
            elif search_type == "category" and query_lower in book.get("category", "").lower():
                found = True

            if found:
                results.append(book)

        if not results:
            print(f"\n Nu s-au gasit carti pentru '{query}' (cautare dupa {search_type})\n")
            return

        print("")
        print("▀" * 60)
        print(f"  Rezultate cautare {search_type}: \"{query}\"")
        print("▀" * 60)

        for i, book in enumerate(results, 1):
            status_icon = "[OK]" if book['status'] == "DISPONIBIL" else "X"
            popular = " (Popular!)" if book.get('loan_count', 0) > 10 else ""

            print(f"\n{i}. {book['title']}")
            print(f"   Autor: {book['author']}")
            print(f"   ISBN: {book.get('isbn', 'N/A')}")
            print(f"   Status: {status_icon} {book['status']}")

            if book['status'] == "IMPRUMUTAT":
                for loan in self.data["loans"]:
                    if loan.get("book_id") == book["id"] and loan.get("status") == "ACTIV":
                        print(f"   Returnare estimata: {loan.get('return_date', 'N/A')}")
                        break

            print(f"   Categorie: {book.get('category', 'N/A')}")
            if book.get('year'):
                print(f"   An publicare: {book['year']}")
            print(f"   Imprumuturi totale: {book.get('loan_count', 0)}{popular}")

        print(f"\n  Total gasite: {len(results)} carti")
        print("▀" * 60)
        print("")

    def _find_book(self, identifier: str) -> Optional[Dict]:
        """Gaseste o carte dupa titlu, ISBN sau ID"""
        for book in self.data["books"]:
            if book.get("title", "").lower() == identifier.lower():
                return book
            if book.get("isbn", "") == identifier:
                return book
            if str(book.get("id", "")) == identifier:
                return book
        return None

    def delete_book(self, identifier: str) -> None:
        """Sterge o carte din catalog"""
        # Verificare duplicate la titlu
        matches = [b for b in self.data["books"] if b.get("title", "").lower() == identifier.lower()]
        if len(matches) > 1:
            print(f"\nEROARE! Exista {len(matches)} carti cu titlul '{identifier}'.")
            print("Care dintre ele doresti sa o stergi?")
            for m in matches:
                print(f"  [ID: {m['id']}] {m['title']} - {m['author']} (ISBN: {m.get('isbn', 'N/A')})")
            
            try:
                valid_ids = [str(m['id']) for m in matches]
                while True:
                    choice = input("\nIntrodu ID-ul corect (sau Enter pentru anulare): ").strip()
                    if not choice:
                        print("Operatiune anulata.")
                        return
                    if choice not in valid_ids:
                        print(f"EROARE! ID-ul '{choice}' nu e in lista de mai sus.")
                        print(f"Introdu unul dintre: {', '.join(valid_ids)}")
                        continue
                    # Apelam recursiv cu ID-ul ales
                    self.delete_book(choice)
                    return
            except KeyboardInterrupt:
                print("\nOperatiune anulata.")
                return

        book = self._find_book(identifier)

        if not book:
            print(f"EROARE! Cartea '{identifier}' nu a fost gasita!")
            return

        if book['status'] != "DISPONIBIL":
            print("EROARE! Nu poti sterge o carte care este imprumutata!")
            return

        self.data["books"].remove(book)
        self._save_data()

        print(f"\n Cartea '{book['title']}' a fost stearsa din catalog.\n")

    # Gestionare utilizatori
    
    def add_user(self, name: str, user_id: str, email: str = None) -> None:
        """Inregistreaza un utilizator nou"""
        user_id = str(user_id)

        for user in self.data["users"]:
            if str(user.get("id")) == user_id:
                print(f"EROARE! Un utilizator cu ID {user_id} exista deja!")
                return

        if email and '@' not in email:
            print("EROARE! Formatul email-ului nu este valid!")
            return

        new_user = {
            "id": user_id,
            "name": name,
            "email": email if email else "N/A",
            "registration_date": datetime.now().strftime(DATE_FORMAT),
            "active_loans": 0,
            "total_loans": 0,
            "total_penalties": 0,
            "status": "ACTIV"
        }

        self.data["users"].append(new_user)
        self._save_data()

        print("")
        print("▀" * 50)
        print("      UTILIZATOR ADAUGAT CU SUCCES!")
        print("▀" * 50)
        print(f"  Nume:              {name}")
        print(f"  ID:                {user_id}")
        print(f"  Email:             {new_user['email']}")
        print(f"  Data inregistrare: {new_user['registration_date']}")
        print(f"  Carti imprumutate: 0")
        print(f"  Status:            ACTIV")
        print("▀" * 50)
        print("")

    def list_users(self) -> None:
        """Listeaza toti utilizatorii"""
        users = self.data["users"]

        if not users:
            print("\n Nu exista utilizatori inregistrati.\n")
            return

        print("")
        print("▀" * 80)
        print(f"  UTILIZATORI INREGISTRATI ({len(users)} total)")
        print("▀" * 80)
        print(f"{'ID':<10} {'Nume':<25} {'Email':<25} {'Impr. Active':<10} {'Status':<10}")
        print("░" * 80)

        for user in users:
            name = user['name'][:23] + ".." if len(user['name']) > 25 else user['name']
            email = user.get('email', 'N/A')[:23] + ".." if len(user.get('email', 'N/A')) > 25 else user.get('email', 'N/A')
            status = user.get('status', 'N/A')
            print(f"{user['id']:<10} {name:<25} {email:<25} {user.get('active_loans', 0):<10} {status:<10}")
        print("▀" * 80)
        print("")

    def _find_user(self, user_id: str) -> Optional[Dict]:
        """Gaseste un utilizator dupa ID"""
        user_id = str(user_id)
        for user in self.data["users"]:
            if str(user.get("id")) == user_id:
                return user
        return None

    def deactivate_user(self, user_id: str) -> None:
        """Dezactiveaza un utilizator"""
        user = self._find_user(user_id)
        if not user:
            print(f"EROARE! Utilizatorul cu ID '{user_id}' nu exista!")
            return

        if user.get('active_loans', 0) > 0:
            print(f"EROARE! Utilizatorul are {user['active_loans']} imprumuturi active!")
            print("Returneaza cartile inainte de a dezactiva contul.")
            return

        user['status'] = "INACTIV"
        self._save_data()

        print(f"\n Utilizatorul '{user['name']}' a fost dezactivat.\n")

    def reactivate_user(self, user_id: str) -> None:
        """Reactiveaza un utilizator inactiv."""
        user = self._find_user(user_id)
        if not user:
            print(f"EROARE! Utilizatorul cu ID '{user_id}' nu exista!")
            return

        if user.get('status') == "ACTIV":
            print(f"Utilizatorul '{user['name']}' este deja activ.")
            return

        user['status'] = "ACTIV"
        self._save_data()

        print(f"\nUtilizatorul '{user['name']}' a fost reactivat cu succes.\n")

    # Gestionare imprumuturi

    def borrow_book(self, identifier: str, user_id: str, days: int = 14) -> None:
        """Imprumuta o carte"""
        print("\nVerificare disponibilitate...")

        user_id = str(user_id)

        # Verificare ambiguitate (duplicate la titlu)
        matches = [b for b in self.data["books"] 
                   if b.get("title", "").lower() == identifier.lower() and b["status"] == "DISPONIBIL"]
        if len(matches) > 1:
            print(f"\nExista {len(matches)} carti disponibile cu titlul '{identifier}'.")
            print("Care dintre ele doresti sa o imprumuti?")
            for m in matches:
                print(f"  [ID: {m['id']}] {m['title']} - {m['author']} (ISBN: {m.get('isbn', 'N/A')})")
            
            try:
                valid_ids = [str(m['id']) for m in matches]
                while True:
                    choice = input("\nIntrodu ID-ul corect (sau Enter pentru anulare): ").strip()
                    if not choice:
                        print("Operatiune anulata.")
                        return
                    if choice not in valid_ids:
                        print(f"EROARE! ID-ul '{choice}' nu e in lista de mai sus.")
                        print(f"Introdu unul dintre: {', '.join(valid_ids)}")
                        continue
                    # Apelam recursiv cu ID-ul ales
                    self.borrow_book(choice, user_id, days)
                    return
            except KeyboardInterrupt:
                print("\nOperatiune anulata.")
                return

        book = self._find_book(identifier)
        if not book:
            print(f"EROARE! Cartea '{identifier}' nu a fost gasita!")
            return

        user = self._find_user(user_id)
        if not user:
            print(f"EROARE! Utilizatorul cu ID '{user_id}' nu exista!")
            return

        if user.get('status') != "ACTIV":
            print("EROARE! Contul utilizatorului este inactiv!")
            return

        if book["status"] != "DISPONIBIL":
            print(f"EROARE! Cartea '{book['title']}' nu este disponibila!")
            for loan in self.data["loans"]:
                if loan.get("book_id") == book["id"] and loan.get("status") == "ACTIV":
                    print(f"         Returnare estimata: {loan.get('return_date', 'N/A')}")
                    break
            return

        if days < 1 or days > 60:
            print("EROARE! Perioada de imprumut trebuie sa fie intre 1 si 60 de zile!")
            return

        print("Carte disponibila!")
        print("Utilizator valid!")

        loan_date = datetime.now()
        return_date = loan_date + timedelta(days=days)

        loan = {
            "id": len(self.data["loans"]) + 1,
            "book_id": book["id"],
            "book_title": book["title"],
            "user_id": user_id,
            "user_name": user["name"],
            "loan_date": loan_date.strftime(DATE_FORMAT),
            "return_date": return_date.strftime(DATE_FORMAT),
            "actual_return_date": None,
            "status": "ACTIV",
            "penalty": 0
        }

        self.data["loans"].append(loan)

        book["status"] = "IMPRUMUTAT"
        book["loan_count"] = book.get("loan_count", 0) + 1

        user["active_loans"] = user.get("active_loans", 0) + 1
        user["total_loans"] = user.get("total_loans", 0) + 1

        self._save_data()

        print("")
        print("▀" * 50)
        print("      IMPRUMUT INREGISTRAT!")
        print("▀" * 50)
        print(f"  Carte:         {book['title']} ({book['author']})")
        print(f"  Utilizator:    {user['name']} (ID: {user_id})")
        print(f"  Data imprumut: {loan['loan_date']}")
        print(f"  Data returnare: {loan['return_date']} ({days} zile)")
        print("▀" * 50)
        print(f"\n⚠️  Reminder: Returneaza cartea pana la {loan['return_date']}")
        print("   pentru a evita penalitati!\n")

    def return_book(self, identifier: str, user_id: str) -> None:
        """Returneaza o carte imprumutata"""
        print("\nProcesare returnare...")

        user_id = str(user_id)

        # Verificare ambiguitate (duplicate la titlu) - doar cartile imprumutate
        matches = [b for b in self.data["books"] 
                   if b.get("title", "").lower() == identifier.lower() and b["status"] == "IMPRUMUTAT"]
        if len(matches) > 1:
            print(f"\nExista {len(matches)} carti imprumutate cu titlul '{identifier}'.")
            print("Care dintre ele doresti sa o returnezi?")
            for m in matches:
                print(f"  [ID: {m['id']}] {m['title']} - {m['author']} (ISBN: {m.get('isbn', 'N/A')})")
            
            try:
                valid_ids = [str(m['id']) for m in matches]
                while True:
                    choice = input("\nIntrodu ID-ul corect (sau Enter pentru anulare): ").strip()
                    if not choice:
                        print("Operatiune anulata.")
                        return
                    if choice not in valid_ids:
                        print(f"EROARE! ID-ul '{choice}' nu e in lista de mai sus.")
                        print(f"Introdu unul dintre: {', '.join(valid_ids)}")
                        continue
                    # Apelam recursiv cu ID-ul ales
                    self.return_book(choice, user_id)
                    return
            except KeyboardInterrupt:
                print("\nOperatiune anulata.")
                return

        book = self._find_book(identifier)
        if not book:
            print(f"EROARE! Cartea '{identifier}' nu a fost gasita!")
            return

        user = self._find_user(user_id)
        if not user:
            print(f"EROARE! Utilizatorul cu ID '{user_id}' nu exista!")
            return

        active_loan = None
        for loan in self.data["loans"]:
            if (loan.get("book_id") == book["id"] and
                str(loan.get("user_id")) == user_id and
                loan.get("status") == "ACTIV"):
                active_loan = loan
                break

        if not active_loan:
            print(f"EROARE! Nu exista un imprumut activ pentru '{book['title']}' de catre utilizatorul {user_id}!")
            return

        today = datetime.now()
        due_date = datetime.strptime(active_loan["return_date"], DATE_FORMAT)
        loan_days = (today - datetime.strptime(active_loan["loan_date"], DATE_FORMAT)).days

        penalty = 0
        overdue_days = 0

        if today.date() > due_date.date():
            overdue_days = (today.date() - due_date.date()).days
            penalty = overdue_days * PENALTY_PER_DAY

        active_loan["actual_return_date"] = today.strftime(DATE_FORMAT)
        active_loan["status"] = "RETURNAT"
        active_loan["penalty"] = penalty

        book["status"] = "DISPONIBIL"

        user["active_loans"] = max(0, user.get("active_loans", 1) - 1)
        user["total_penalties"] = user.get("total_penalties", 0) + penalty

        self._save_data()

        print("")
        print("▀" * 50)
        print("      CARTE RETURNATA CU SUCCES!")
        print("▀" * 50)
        print(f"  Carte:             {book['title']}")
        print(f"  Utilizator:        {user['name']}")
        print(f"  Data imprumut:     {active_loan['loan_date']}")
        print(f"  Data returnare:    {today.strftime(DATE_FORMAT)}")
        print(f"  Zile imprumut:     {loan_days} zile")

        if overdue_days > 0:
            print(f"  ⚠️  Intarziere:    {overdue_days} zile")
            print(f"    Penalitate:    {penalty} RON")
        else:
            print("  Returnat la timp!")
            print("  Fara penalitati!")

        print("▀" * 50)
        print("\n📚 Cartea este acum DISPONIBILA pentru imprumut.\n")

    # Rapoarte  

    def generate_report(self, report_type: str, top: int = 10) -> None:
        """Genereaza diverse rapoarte"""
        if report_type == "overdue":
            self._report_overdue()
        elif report_type == "borrowed":
            self._report_borrowed()
        elif report_type == "popular":
            self._report_popular(top)
        elif report_type == "users":
            self._report_active_users(top)
        else:
            print(f"EROARE! Tip raport invalid: {report_type}")
            print("Tipuri disponibile: overdue, borrowed, popular, users")

    def _report_overdue(self) -> None:
        """Raport cu cartile intarziate"""
        today = datetime.now().date()
        overdue_list = []

        for loan in self.data["loans"]:
            if loan.get("status") == "ACTIV":
                due_date = datetime.strptime(loan["return_date"], DATE_FORMAT).date()
                if today >= due_date:
                    days = (today - due_date).days
                    loan_copy = loan.copy()
                    loan_copy["overdue_days"] = days
                    loan_copy["current_penalty"] = days * PENALTY_PER_DAY
                    overdue_list.append(loan_copy)

        print("")
        print("▀" * 65)
        print(f"  RAPORT CARTI INTARZIATE - {today}")
        print("▀" * 65)

        if not overdue_list:
            print("\n  Nu exista carti intarziate!\n")
            print("▀" * 65)
            print("")
            return

        print(f"\n  {len(overdue_list)} carti sunt returnate cu intarziere:\n")

        total_penalties = 0
        for i, loan in enumerate(overdue_list, 1):
            book = self._find_book(str(loan["book_id"]))
            author = book.get("author", "N/A") if book else "N/A"

            print(f"  {i}. {loan['book_title']} ({author})")
            print(f"     Utilizator: {loan['user_name']} (ID: {loan['user_id']})")
            print(f"     Deadline: {loan['return_date']}")

            if loan["overdue_days"] == 0:
                print(f"     Intarziere: 0 zile (scadent ASTAZI!)")
            else:
                print(f"     Intarziere: {loan['overdue_days']} zile")

            print(f"     Penalitate: {loan['current_penalty']} RON")
            total_penalties += loan["current_penalty"]
            print("")

        print("░" * 65)
        print(f"  Total penalitati de colectat: {total_penalties} RON")
        print("")
        print("  Actiuni recomandate:")
        for loan in overdue_list:
            if loan["overdue_days"] == 0:
                print(f"    ✉ Trimite reminder catre {loan['user_name']} (scadent astazi)")
            else:
                print(f"    ✉ Trimite notificare penalitate catre {loan['user_name']}")
        print("▀" * 65)
        print("")

    def _report_borrowed(self) -> None:
        """Raport cu cartile imprumutate"""
        active = [loan for loan in self.data["loans"] if loan.get("status") == "ACTIV"]

        print("")
        print("▀" * 75)
        print(f"  CARTI IMPRUMUTATE ({len(active)} total)")
        print("▀" * 75)

        if not active:
            print("\n  Nu exista carti imprumutate in acest moment.\n")
            print("▀" * 75)
            print("")
            return

        print(f"{'ID':<5} {'Titlu':<22} {'Imprumutat de':<18} {'Imprumut':<12} {'Return':<12}")
        print("░" * 75)

        for loan in active:
            title = loan['book_title'][:20] + ".." if len(loan['book_title']) > 22 else loan['book_title']
            name = loan['user_name'][:16] + ".." if len(loan['user_name']) > 18 else loan['user_name']
            print(f"{loan['book_id']:<5} {title:<22} {name:<18} {loan['loan_date']:<12} {loan['return_date']:<12}")

        print("▀" * 75)
        print("")

    def _report_popular(self, top: int = 10) -> None:
        """Raport cu cartile populare"""
        sorted_books = sorted(
            self.data["books"],
            key=lambda x: x.get("loan_count", 0),
            reverse=True
        )[:top]

        print("")
        print("▀" * 60)
        print(f"  TOP {min(top, len(sorted_books))} CARTI POPULARE")
        print("▀" * 60)

        if not sorted_books:
            print("\n  Nu exista carti in biblioteca.\n")
            print("▀" * 60)
            return

        for i, book in enumerate(sorted_books, 1):
            count = book.get('loan_count', 0)
            if count > 0:
                print(f"  {i}. \"{book['title']}\" - {count} imprumuturi")

        print("▀" * 60)
        print("")

    def _report_active_users(self, top: int = 10) -> None:
        """Raport cu utilizatorii activi"""
        # Filtram doar utilizatorii activi (status != INACTIV) cu cel putin 1 imprumut
        active_users = [u for u in self.data["users"] 
                        if u.get("status", "ACTIV") != "INACTIV" and u.get("total_loans", 0) > 0]
        sorted_users = sorted(
            active_users,
            key=lambda x: x.get("total_loans", 0),
            reverse=True
        )[:top]

        print("")
        print("▀" * 60)
        print(f"  TOP {len(sorted_users)} UTILIZATORI ACTIVI")
        print("▀" * 60)

        if not sorted_users:
            print("\n  Nu exista utilizatori activi cu imprumuturi.\n")
            print("▀" * 60)
            return

        for i, user in enumerate(sorted_users, 1):
            count = user.get('total_loans', 0)
            print(f"  {i}. {user['name']} - {count} imprumuturi")
        print("▀" * 60)
        print("")

    def show_statistics(self, top: int = 5) -> None:
        """Afiseaza statistici complete despre biblioteca"""
        books = self.data["books"]
        users = self.data["users"]
        loans = self.data["loans"]

        total_books = len(books)
        available_books = len([b for b in books if b.get("status") == "DISPONIBIL"])
        borrowed_books = total_books - available_books

        total_users = len(users)
        active_users = len([u for u in users if u.get("active_loans", 0) > 0])

        total_loans = len(loans)
        active_loans = len([l for l in loans if l.get("status") == "ACTIV"])

        today = datetime.now().date()
        overdue_count = 0
        for loan in loans:
            if loan.get("status") == "ACTIV":
                due_date = datetime.strptime(loan["return_date"], DATE_FORMAT).date()
                if today > due_date:
                    overdue_count += 1

        categories = set(b.get("category", "N/A") for b in books)
        authors = set(b.get("author", "N/A") for b in books)

        returned = [l for l in loans if l.get("status") == "RETURNAT"]
        on_time = len([l for l in returned if l.get("penalty", 0) == 0])
        on_time_rate = (on_time / len(returned) * 100) if returned else 100

        total_penalties = sum(l.get("penalty", 0) for l in returned)

        current_month = datetime.now().strftime("%B %Y")

        print("")
        print("▀" * 60)
        print(f"  STATISTICI BIBLIOTECA - {current_month}")
        print("▀" * 60)
        
        print("\n  COLECTIE:")
        print(f"    Total carti:    {total_books}")
        print(f"    Categorii:      {len(categories)}")
        print(f"    Autori unici:   {len(authors)}")

        print("\n  STATUS CARTI:")
        if total_books > 0:
            available_pct = (available_books / total_books) * 100
            borrowed_pct = (borrowed_books / total_books) * 100
            bar_available = "█" * int(available_pct / 5) + "░" * (20 - int(available_pct / 5))
            bar_borrowed = "█" * int(borrowed_pct / 5) + "░" * (20 - int(borrowed_pct / 5))
            print(f"    Disponibile: {available_books} ({available_pct:.1f}%) {bar_available}")
            print(f"    Imprumutate: {borrowed_books} ({borrowed_pct:.1f}%) {bar_borrowed}")
        else:
            print("    Nu exista carti.")
        print("\n  UTILIZATORI:")
        print(f"    Total inregistrati:     {total_users}")
        print(f"    Cu imprumuturi active:  {active_users}")
        print("\n  IMPRUMUTURI:")
        print(f"    Total (toate timpurile): {total_loans}")
        print(f"    Active:                  {active_loans}")
        print(f"    Intarziate:              {overdue_count}")
        print(f"    Rata returnare la timp:  {on_time_rate:.0f}%")

        if books:
            print(f"\n  TOP {top} CARTI POPULARE:")
            sorted_books = sorted(books, key=lambda x: x.get("loan_count", 0), reverse=True)[:top]
            for i, book in enumerate(sorted_books, 1):
                count = book.get('loan_count', 0)
                if count > 0:
                    print(f"  {i}. \"{book['title']}\" - {count} imprumuturi")

        if books:
            print(f"\n  TOP 3 CATEGORII:")
            cat_count = {}
            for b in books:
                cat = b.get("category", "N/A")
                cat_count[cat] = cat_count.get(cat, 0) + 1
            sorted_cats = sorted(cat_count.items(), key=lambda x: x[1], reverse=True)[:3]
            for i, (cat, count) in enumerate(sorted_cats, 1):
                pct = (count / total_books * 100) if total_books > 0 else 0
                print(f"  {i}. {cat} - {count} carti ({pct:.1f}%)")

        if users:
            print(f"\n  TOP 3 UTILIZATORI ACTIVI:")
            sorted_users = sorted(users, key=lambda x: x.get("total_loans", 0), reverse=True)[:3]
            for i, user in enumerate(sorted_users, 1):
                count = user.get('total_loans', 0)
                if count > 0:
                    print(f"  {i}. {user['name']} - {count} imprumuturi")

        print(f"\n  VENITURI (din penalitati):")
        print(f"    Total colectat: {total_penalties} RON")
        print("")
        print("▀" * 60)
        print("")

    # Import/Export

    def export_data(self, destination: str) -> None:
        """Exporta datele in format CSV (folder complet sau fisier unic)"""
        
        # Cazul 1: Export intr-un singur fisier
        if destination.lower().endswith(".csv"):
            book_fieldnames = ['id', 'title', 'author', 'isbn', 'category', 'year', 'status', 'date_added', 'loan_count']
            
            try:
                # Verificam daca exista folderul parinte, daca e data o cale
                parent_dir = os.path.dirname(destination)
                if parent_dir and not os.path.exists(parent_dir):
                    os.makedirs(parent_dir, exist_ok=True)

                with open(destination, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.DictWriter(f, fieldnames=book_fieldnames, extrasaction='ignore')
                    writer.writeheader()
                    if self.data["books"]:
                        writer.writerows(self.data["books"])
                
                print(f"\nExportat catalogul de carti ({len(self.data['books'])} carti) in '{destination}'")
                return
            except Exception as e:
                print(f"EROARE la exportul in fisier: {e}")
                return

        # Cazul 2: Export complet intr-un folder
        folder = destination
        os.makedirs(folder, exist_ok=True)

        print("\nExport in desfasurare (Backup complet)...")

        active = [l for l in self.data["loans"] if l.get("status") == "ACTIV"]

        # Export catalog carti
        books_file = os.path.join(folder, "library_catalog.csv")
        book_fieldnames = ['id', 'title', 'author', 'isbn', 'category', 'year', 'status', 'date_added', 'loan_count']
        with open(books_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=book_fieldnames, extrasaction='ignore')
            writer.writeheader()
            if self.data["books"]:
                writer.writerows(self.data["books"])

        # Export utilizatori
        users_file = os.path.join(folder, "users.csv")
        user_fieldnames = ['id', 'name', 'email', 'registration_date', 'active_loans', 'total_loans', 'status']
        with open(users_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=user_fieldnames, extrasaction='ignore')
            writer.writeheader()
            if self.data["users"]:
                writer.writerows(self.data["users"])

        # Export imprumuturi active
        active_loans_file = os.path.join(folder, "active_loans.csv")
        loan_fieldnames = ['id', 'book_id', 'book_title', 'user_id', 'user_name', 'loan_date', 'return_date', 'status']
        with open(active_loans_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=loan_fieldnames, extrasaction='ignore')
            writer.writeheader()
            if active:
                writer.writerows(active)

        # Export istoric complet
        history_file = os.path.join(folder, "user_history.csv")
        with open(history_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=loan_fieldnames + ['actual_return_date', 'penalty'], extrasaction='ignore')
            writer.writeheader()
            if self.data["loans"]:
                writer.writerows(self.data["loans"])

        print(f"\nExportat {len(self.data['books'])} carti")
        print(f"Exportat {len(self.data['users'])} utilizatori")
        print(f"Exportat {len(active)} imprumuturi active")

        print(f"\nFisiere generate in '{folder}/':")
        print("  • library_catalog.csv (catalog complet)")
        print("  • users.csv (lista utilizatori)")
        print("  • active_loans.csv (imprumuturi active)")
        print("  • user_history.csv (istoric complet)")
        print("\nExport complet.")

    def import_data(self, filename: str) -> None:
        """Importa carti din fisier CSV"""
        if not os.path.exists(filename):
            print(f"EROARE! Fisierul '{filename}' nu exista!")
            return

        print(f"\nImport din {filename}...")

        imported = 0
        ignored = 0

        try:
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                for row in reader:
                    isbn = row.get('isbn', row.get('ISBN', ''))
                    if isbn and isbn != 'N/A':
                        exists = any(b.get('isbn') == isbn for b in self.data["books"])
                        if exists:
                            ignored += 1
                            continue

                    title = row.get('title', row.get('titlu', '')).strip()
                    author = row.get('author', row.get('autor', '')).strip()

                    if not title or not author:
                        ignored += 1
                        continue

                    year_str = row.get('year', row.get('an', ''))
                    year = int(year_str) if year_str and str(year_str).isdigit() else None

                    book = {
                        "id": self._generate_book_id(),
                        "title": title,
                        "author": author,
                        "isbn": isbn if isbn else "N/A",
                        "category": row.get('category', row.get('categorie', 'Necategorizat')),
                        "year": year,
                        "status": "DISPONIBIL",
                        "date_added": datetime.now().strftime(DATE_FORMAT),
                        "loan_count": 0
                    }
                    self.data["books"].append(book)
                    imported += 1

            self._save_data()
            print(f" Importat {imported} carti noi!")
            if ignored > 0:
                print(f" {ignored} inregistrari ignorate (duplicate sau invalide).")
            print("")

        except Exception as e:
            print(f"EROARE! Eroare la import: {e}")


def create_parser() -> argparse.ArgumentParser:
    """Creeaza parserul pentru linia de comanda"""
    # Determinam numele comenzii in functie de sistem (Windows vs Linux/Docker)
    cmd_name = ".\\library_manager" if sys.platform == "win32" else "library_manager"

    parser = argparse.ArgumentParser(
        prog=cmd_name,
        add_help=False,
        description="""
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
                       LIBRARY MANAGER - CLI
              Sistem de management pentru biblioteca
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄
""",
        formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=r"""
▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀▀
                         EXEMPLE DE UTILIZARE
▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄▄

  CARTI:
    Adaugare:
      library_manager add_book "1984" "G. Orwell" --isbn 978-0451 --category Fiction
    Listare:
      library_manager list                    (toate cartile)
      library_manager list --status borrowed  (doar cele imprumutate)
    Cautare (dupa titlu, autor, isbn sau categorie):
      library_manager search --author "Orwell"
      library_manager search --category "SF"
    Stergere:
      library_manager delete_book "1984"
      library_manager delete_book "978-0451" (Dupa ISBN)

  UTILIZATORI:
    Adaugare:
      library_manager add_user "Ion Popescu" --id 1001 --email "ion@test.com"
    Listare:
      library_manager list --type users
    Dezactivare/Reactivare:
      library_manager delete_user 1001
      library_manager reactivate_user 1001

  IMPRUMUTURI:
    Imprumut:
      library_manager borrow "1984" --user_id 1001 --days 14
    Returnare:
      library_manager return "1984" --user_id 1001

  RAPOARTE SI STATISTICI:
    Statistici generale (top carti, autori, categorii):
      library_manager stats
      library_manager stats --top 10
    Rapoarte specifice:
      library_manager report --overdue    (intarzieri)
      library_manager report --borrowed   (carti imprumutate)
      library_manager report --popular    (cele mai imprumutate)
      library_manager report --users      (activitate utilizatori)

  EXPORT/IMPORT:
    Export:
      library_manager export backup_folder        (exporta tot intr-un folder)
      library_manager export catalog_carti.csv    (exporta doar catalogul)
    Import:
      library_manager import carti_noi.csv        (din folderul curent)
      library_manager import "C:\\Users\\Eu\\Desktop\\import.csv" (cale completa)
""".replace("library_manager", cmd_name)
    )

    parser.add_argument(
        '-h', '--help',
        action='help',
        default=argparse.SUPPRESS,
        help='Afiseaza mesajul de ajutor'
    )

    subparsers = parser.add_subparsers(dest="command", title="Comenzi disponibile", metavar="")

    p = subparsers.add_parser("add_book", help="Adauga o carte noua")
    p.add_argument("title", help="Titlul cartii")
    p.add_argument("author", help="Autorul cartii")
    p.add_argument("--isbn", help="Codul ISBN")
    p.add_argument("--category", help="Categoria cartii")
    p.add_argument("--year", type=int, help="Anul publicarii")

    p = subparsers.add_parser("add_user", help="Adauga un utilizator nou")
    p.add_argument("name", help="Numele utilizatorului")
    p.add_argument("--id", required=True, dest="user_id", help="ID-ul utilizatorului")
    p.add_argument("--email", help="Adresa de email")

    p = subparsers.add_parser("list", help="Listeaza carti sau utilizatori")
    p.add_argument("--type", choices=["books", "users"], default="books", help="Ce sa listeze")
    p.add_argument("--status", help="Filtreaza dupa status (available/borrowed)")

    p = subparsers.add_parser("search", help="Cauta carti")
    p.add_argument("query", nargs="?", help="Termen de cautare (optional)")
    p.add_argument("--title", help="Cauta dupa titlu")
    p.add_argument("--author", help="Cauta dupa autor")
    p.add_argument("--isbn", help="Cauta dupa ISBN")
    p.add_argument("--category", help="Cauta dupa categorie")

    p = subparsers.add_parser("borrow", help="Imprumuta o carte")
    p.add_argument("book", help="Titlul sau ISBN-ul cartii")
    p.add_argument("--user_id", required=True, help="ID-ul utilizatorului")
    p.add_argument("--days", type=int, default=14, help="Numarul de zile (default: 14)")

    p = subparsers.add_parser("return", help="Returneaza o carte")
    p.add_argument("book", help="Titlul sau ISBN-ul cartii")
    p.add_argument("--user_id", required=True, help="ID-ul utilizatorului")

    p = subparsers.add_parser("delete_book", help="Sterge o carte")
    p.add_argument("book", help="Titlul sau ISBN-ul cartii")

    p = subparsers.add_parser("delete_user", help="Dezactiveaza un utilizator")
    p.add_argument("user_id", help="ID-ul utilizatorului")

    p = subparsers.add_parser("reactivate_user", help="Reactiveaza un utilizator")
    p.add_argument("user_id", help="ID-ul utilizatorului de reactivat")

    p = subparsers.add_parser("report", help="Genereaza rapoarte")
    p.add_argument("--overdue", action="store_true", help="Raport carti intarziate")
    p.add_argument("--borrowed", action="store_true", help="Raport carti imprumutate")
    p.add_argument("--popular", action="store_true", help="Raport carti populare")
    p.add_argument("--users", action="store_true", help="Raport utilizatori activi")
    p.add_argument("--top", type=int, default=10, help="Numarul de rezultate pentru top")

    p = subparsers.add_parser("stats", help="Afiseaza statistici")
    p.add_argument("--top", type=int, default=5, help="Numarul de rezultate pentru top-uri")

    p = subparsers.add_parser("export", help="Exporta datele in fisiere CSV")
    p.add_argument("folder", help="Folderul unde se vor genera fisierele CSV (ex: backup)")

    p = subparsers.add_parser("import", help="Importa carti din CSV")
    p.add_argument("filename", help="Fisierul CSV de importat")

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    manager = LibraryManager()

    if args.command == "add_book":
        manager.add_book(args.title, args.author, args.isbn, args.category, args.year)

    elif args.command == "add_user":
        manager.add_user(args.name, args.user_id, args.email)

    elif args.command == "list":
        if args.type == "users":
            manager.list_users()
        else:
            if args.status and args.status.lower() == "borrowed":
                manager.generate_report("borrowed")
            else:
                manager.list_books(args.status)

    elif args.command == "search":
        if args.author:
            manager.search_books(args.author, "author")
        elif args.title:
            manager.search_books(args.title, "title")
        elif args.isbn:
            manager.search_books(args.isbn, "isbn")
        elif args.category:
            manager.search_books(args.category, "category")
        elif args.query:
            manager.search_books(args.query, "title")
        else:
            print("\n EROARE! Specifica un criteriu de cautare!")
            print("Exemple:")
            print('  search --author "Orwell"')
            print('  search --title "1984"')
            print('  search --isbn "9780451524935"')
            print('  search --category "Fiction"')

    elif args.command == "borrow":
        manager.borrow_book(args.book, args.user_id, args.days)

    elif args.command == "return":
        manager.return_book(args.book, args.user_id)

    elif args.command == "delete_book":
        manager.delete_book(args.book)

    elif args.command == "delete_user":
        manager.deactivate_user(args.user_id)

    elif args.command == "reactivate_user":
        manager.reactivate_user(args.user_id)

    elif args.command == "report":
        if args.overdue:
            report_type = "overdue"
        elif args.borrowed:
            report_type = "borrowed"
        elif args.popular:
            report_type = "popular"
        elif args.users:
            report_type = "users"
        else:
            report_type = "overdue"
        manager.generate_report(report_type, args.top)

    elif args.command == "stats":
        manager.show_statistics(args.top)

    elif args.command == "export":
        manager.export_data(args.folder)

    elif args.command == "import":
        manager.import_data(args.filename)

if __name__ == "__main__":
    main()