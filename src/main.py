import argparse
import json
import os
from datetime import datetime
from typing import List, Dict

# Configurare cai fisiere
BASE_DIR = os. path.dirname(os.path.abspath(__file__))
DATA_DIR = os. path.join(BASE_DIR, '..', 'data')
DATA_FILE = os. path.join(DATA_DIR, 'library_data.json')
DATE_FORMAT = "%Y-%m-%d"

# Creare director date daca nu exista
os.makedirs(DATA_DIR, exist_ok=True)


class LibraryManager:
    """Gestioneaza entitatile bibliotecii:  Carti, Utilizatori si Imprumuturi"""

    def __init__(self, data_file: str = DATA_FILE):
        """Initializeaza managerul de biblioteca"""
        self. data_file = data_file
        self.data: Dict[str, List[Dict]] = {
            "books": [],
            "users": [],
            "loans": []
        }
        self. load_data()

    def load_data(self) -> None:
        """Incarca datele din fisierul JSON"""
        if os.path. exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    incarcate = json.load(f)
                    self.data. update(incarcate)
            except json.JSONDecodeError:
                pass

    def save_data(self) -> None:
        """Salveaza datele in fisierul JSON"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    # gestionare carti

    def add_book(self, title: str, author:  str, isbn: str, category: str, year: int = None) -> None:
        """Adauga o carte noua in catalog"""
        if any(b['isbn'] == isbn for b in self.data['books']):
            print(f"Eroare: Cartea cu ISBN {isbn} exista deja in sistem.")
            return

        noua_carte = {
            "title": title,
            "author": author,
            "isbn":  isbn,
            "category": category,
            "year": year,
            "available": True,
            "date_added": datetime. now().strftime(DATE_FORMAT)
        }

        self.data['books'].append(noua_carte)
        self.save_data()
        print(f"Carte adaugata cu succes:  '{title}' de {author}")

    def list_books(self) -> None:
        """Listeaza toate cartile din biblioteca"""
        if not self.data['books']:
            print("Biblioteca nu are carti inregistrate.")
            return

        print("\nCatalog Carti:")
        print(f"{'ISBN':<15} {'Titlu':<30} {'Autor':<20} {'Status'}")
        print("-" * 85)
        for carte in self.data['books']:
            status = "Disponibil" if carte['available'] else "Imprumutat"
            print(f"{carte['isbn']:<15} {carte['title'][: 28]:<30} {carte['author'][: 18]:<20} {status}")
        print("-" * 85)

    def search_books(self, query: str, search_type: str = "title") -> None:
        """Cauta carti dupa diverse criterii (titlu, autor, isbn)"""
        rezultate = []
        cautare_lower = query.lower()

        for carte in self.data['books']: 
            valoare_camp = str(carte.get(search_type, "")).lower()
            if cautare_lower in valoare_camp:
                rezultate.append(carte)

        if not rezultate:
            print(f"Nu s-au gasit rezultate pentru:  '{query}'")
            return

        print(f"\nRezultate cautare ({len(rezultate)}):")
        for b in rezultate: 
            print(f"- {b['title']} ({b['author']}) [ISBN: {b['isbn']}]")

    # gestionare utilizatori

    def add_user(self, name: str, user_id: str, email: str = None) -> None:
        """Inregistreaza un utilizator nou in sistem"""
        if any(u['id'] == user_id for u in self. data['users']):
            print(f"Eroare:  Utilizatorul cu ID {user_id} este deja inregistrat.")
            return

        nou_utilizator = {
            "name":  name,
            "id": user_id,
            "email": email,
            "active": True,
            "registration_date": datetime. now().strftime(DATE_FORMAT)
        }

        self.data['users']. append(nou_utilizator)
        self.save_data()
        print(f"Utilizator inregistrat:  {name} (ID: {user_id})")

    def list_users(self) -> None:
        """Listeaza toti utilizatorii inregistrati"""
        if not self.data['users']:
            print("Nu exista utilizatori inregistrati.")
            return

        print("\nLista Utilizatori:")
        for u in self.data['users']:
            print(f"ID: {u['id']} | Nume: {u['name']} | Email:  {u. get('email', 'N/A')}")

    # Statistici
    def show_stats(self) -> None:
        """Afiseaza statistici de baza despre biblioteca"""
        nr_carti = len(self.data['books'])
        nr_utilizatori = len(self.data['users'])
        print(f"\nStatistici Biblioteca:")
        print(f"- Total carti in catalog: {nr_carti}")
        print(f"- Total utilizatori inscrisi: {nr_utilizatori}")


def setup_argument_parser() -> argparse.ArgumentParser:
    """Configureaza parserul de argumente pentru CLI"""
    parser = argparse.ArgumentParser(
        description="Manager Biblioteca - Sistem de gestiune",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest="command", help="Comenzi disponibile")

    p_add = subparsers.add_parser("add_book", help="Adauga o carte noua")
    p_add.add_argument("title", help="Titlul cartii")
    p_add.add_argument("author", help="Autorul cartii")
    p_add.add_argument("--isbn", required=True, help="Codul ISBN unic")
    p_add. add_argument("--category", required=True, help="Categoria cartii")
    p_add.add_argument("--year", type=int, help="Anul aparitiei")

    subparsers.add_parser("list", help="Listeaza catalogul de carti")

    p_user = subparsers. add_parser("add_user", help="Inregistreaza un utilizator nou")
    p_user.add_argument("name", help="Numele complet")
    p_user.add_argument("--id", required=True, help="ID-ul unic de utilizator")
    p_user.add_argument("--email", help="Adresa de email")

    p_search = subparsers.add_parser("search", help="Cauta carti in catalog")
    p_search. add_argument("query", help="Termenul de cautare")
    p_search.add_argument("--type", default="title",
                          choices=["title", "author", "isbn"],
                          help="Criteriul de cautare")

    subparsers.add_parser("stats", help="Afiseaza statistici")

    return parser


def main():
    """Functia principala a aplicatiei"""
    parser = setup_argument_parser()
    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    manager = LibraryManager()

    if args.command == "add_book":
        manager. add_book(args.title, args. author, args.isbn, args.category, args.year)
    elif args.command == "list": 
        manager.list_books()
    elif args.command == "add_user": 
        manager.add_user(args.name, args.id, args.email)
    elif args.command == "search": 
        manager.search_books(args.query, args.type)
    elif args. command == "stats": 
        manager.show_stats()


if __name__ == "__main__": 
    main()