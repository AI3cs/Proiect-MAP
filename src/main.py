import argparse
import json
import os
from datetime import datetime, timedelta
from typing import List, Dict, Optional

# am configurat caile
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
DATA_FILE = os.path.join(DATA_DIR, 'library_data.json')
DATE_FORMAT = "%Y-%m-%d"

# am creat director data
os.makedirs(DATA_DIR, exist_ok=True)


class LibraryManager:
    """Gestionează entitățile bibliotecii: Cărți, Utilizatori și Împrumuturi"""

    def __init__(self, data_file: str = DATA_FILE):
        """Inițializează managerul de bibliotecă"""
        self.data_file = data_file
        self.data: Dict[str, List[Dict]] = {
            "books": [],
            "users": [],
            "loans": []
        }
        self.load_data()

    def load_data(self) -> None:
        """Încarcă datele din fișierul JSON"""
        if os.path.exists(self.data_file):
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    self.data = json.load(f)
                print(f"✓ Date încărcate din {self.data_file}")
            except json.JSONDecodeError:
                print(f"[WARN] Fișier corupt. Se începe cu bază de date goală.")

    def save_data(self) -> None:
        """Salvează datele în fișierul JSON"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    # gestionare carti 
    def add_book(self, title: str, author: str, isbn: str, category: str, year: int = None) -> None:
        """Adaugă o carte nouă în catalog"""
        # TODO: Implementez adăugarea cărții
        pass

    def list_books(self) -> None:
        """Listează toate cărțile din bibliotecă"""
        # TODO: Implementez listarea cărților
        pass

    def search_books(self, query: str, search_type: str = "title") -> None:
        """Caută cărți după diverse criterii"""
        # TODO: Implementez căutarea
        pass

    #gestionarea utilizatorilor
    
    def add_user(self, name: str, user_id: str, email: str = None) -> None:
        """Înregistrează un utilizator nou"""
        # TODO: Implementez adăugarea utilizatorului
        pass

    def list_users(self) -> None:
        """Listează toți utilizatorii"""
        # TODO: Implementez listarea utilizatorilor
        pass

    #imprumuturi 
    
    def borrow_book(self, identifier: str, user_id: str, days: int = 14) -> None:
        """Împrumută o carte (după titlu sau ISBN)"""
        # TODO: Implementează împrumutul
        pass

    def return_book(self, identifier: str, user_id: str) -> None:
        """Returnează o carte împrumutată"""
        # TODO: Implementează returnarea
        pass

    #rapoarte
    
    def generate_report(self, report_type: str) -> None:
        """Generează diverse rapoarte"""
        # TODO: Implementează rapoartele
        pass

    #statistici
    
    def show_stats(self) -> None:
        """Afișează statistici despre bibliotecă"""
        # TODO: Implementează statisticile
        pass


def setup_argument_parser() -> argparse.ArgumentParser:
    """Configurează parserul de argumente pentru CLI"""
    parser = argparse.ArgumentParser(
        description="Library Manager - Sistem de management pentru bibliotecă",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple de utilizare:
  %(prog)s add_book "1984" "George Orwell" --isbn 9780451524935 --category "Fiction"
  %(prog)s add_user "Popescu Ion" --id 1001
  %(prog)s borrow "1984" --user_id 1001 --days 14
  %(prog)s return "1984" --user_id 1001
  %(prog)s search "Orwell" --type author
  %(prog)s report --overdue
        """
    )
    
    subparsers = parser.add_subparsers(dest="command", help="Comenzi disponibile")

    # TODO: Adaug toate subcomenzile aici
    
    return parser


def main():
    """Funcția principală a aplicației"""
    parser = setup_argument_parser()
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    manager = LibraryManager()
    
    # TODO: Implementez logica pentru fiecare comandă
    
    print(f"Comandă primită: {args.command}")
    print("TODO: Implementează această funcționalitate")


if __name__ == "__main__":
    main()