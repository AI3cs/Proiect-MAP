import argparse
import csv
import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional

# Configurare cai fisiere
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, '..', 'data')
DATA_FILE = os.path.join(DATA_DIR, 'library_data.json')
DATE_FORMAT = "%Y-%m-%d"
PENALITATE_PE_ZI = 1  # 1 RON per zi penalitatea in caz de intarziere

# Creem folderul data daca nu exista
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

class LibraryManager:
    """
    Clasa principala pentru gestionarea bibliotecii.
    Gestioneaza: Carti, Utilizatori, Imprumuturi
    """

    def __init__(self, fisier_date: str = DATA_FILE):
        """Initializeaza managerul de biblioteca"""
        self.fisier_date = fisier_date
        self.date: Dict[str, List[Dict]] = {
            "carti": [],
            "utilizatori": [],
            "imprumuturi": []
        }
        self._incarca_date()

    def _incarca_date(self) -> None:
        """Incarca datele din fisierul JSON (silentios)"""
        if os.path.exists(self.fisier_date):
            try:
                with open(self.fisier_date, 'r', encoding='utf-8') as f:
                    date_incarcate = json.load(f)
                    for cheie in self.date.keys():
                        if cheie in date_incarcate:
                            self.date[cheie] = date_incarcate[cheie]
            except json.JSONDecodeError:
                pass  # Pornim cu baza de date goala

    def _salveaza_date(self) -> None:
        """Salveaza datele in fisierul JSON"""
        with open(self.fisier_date, 'w', encoding='utf-8') as f:
            json.dump(self.date, f, indent=4, ensure_ascii=False)

    def _genereaza_id_carte(self) -> int:
        """Genereaza un ID unic pentru carte"""
        if not self.date["carti"]:
            return 1
        return max(carte.get("id", 0) for carte in self.date["carti"]) + 1

    # Gestionare carti 

    def adauga_carte(self, titlu: str, autor: str, isbn: str = None,
                     categorie: str = None, an: int = None) -> None:
        """Adauga o carte noua in biblioteca"""
        # Validare ISBN unic
        if isbn:
            for carte in self.date["carti"]:
                if carte.get("isbn") == isbn:
                    print(f"EROARE! O carte cu ISBN {isbn} exista deja!")
                    return

        # Validare an
        if an:
            an_curent = datetime.now().year
            if an < 1450 or an > an_curent + 1:
                print(f"EROARE! Anul {an} nu este valid (1450-{an_curent})!")
                return

        carte_noua = {
            "id": self._genereaza_id_carte(),
            "titlu": titlu,
            "autor": autor,
            "isbn": isbn if isbn else "N/A",
            "categorie": categorie if categorie else "Necategorizat",
            "an": an,
            "status": "DISPONIBIL",
            "data_adaugare": datetime.now().strftime(DATE_FORMAT),
            "nr_imprumuturi": 0
        }

        self.date["carti"].append(carte_noua)
        self._salveaza_date()

        print("")
        print("=" * 50)
        print("      ✓ CARTE ADAUGATA CU SUCCES!")
        print("=" * 50)
        print(f"  ID:        {carte_noua['id']}")
        print(f"  Titlu:     {titlu}")
        print(f"  Autor:     {autor}")
        print(f"  ISBN:      {carte_noua['isbn']}")
        print(f"  Categorie: {carte_noua['categorie']}")
        if an:
            print(f"  An:        {an}")
        print(f"  Status:    DISPONIBIL")
        print(f"  Data:      {carte_noua['data_adaugare']}")
        print("=" * 50)
        print("")

    def listeaza_carti(self, status: str = None) -> None:
        """Listeaza toate cartile din biblioteca"""
        carti = self.date["carti"]

        # Filtrez dupa status
        if status:
            status_upper = status.upper()
            if status_upper == "BORROWED":
                status_upper = "IMPRUMUTAT"
            elif status_upper == "AVAILABLE":
                status_upper = "DISPONIBIL"
            carti = [c for c in carti if c.get("status", "").upper() == status_upper]

        if not carti:
            if not status:
                print("\n Nu exista carti in biblioteca.\n")
            else:
                print(f"\n Nu exista carti cu status '{status}'.\n")
            return

        titlu_text = "CATALOG BIBLIOTECA" if not status else f"CARTI - {status.upper()}"
        print("")
        print("=" * 75)
        print(f"  {titlu_text} ({len(carti)} total)")
        print("=" * 75)
        print(f"{'ID':<4} {'Titlu':<28} {'Autor':<22} {'Status':<12} {'Categorie':<10}")
        print("-" * 75)

        for carte in carti:
            titlu = carte['titlu'][:26] + ".." if len(carte['titlu']) > 28 else carte['titlu']
            autor = carte['autor'][:20] + ".." if len(carte['autor']) > 22 else carte['autor']
            status_icon = "✓" if carte['status'] == "DISPONIBIL" else "X"
            print(f"{carte['id']:<4} {titlu:<28} {autor:<22} {status_icon} {carte['status']:<10} {carte.get('categorie', 'N/A'):<10}")

        print("=" * 75)
        print("")

    def cauta_carti(self, termen: str, tip_cautare: str = "title") -> None:
        """Cauta carti dupa diferite criterii"""
        termen_lower = termen.lower()
        rezultate = []

        for carte in self.date["carti"]:
            gasit = False
            if tip_cautare == "title" and termen_lower in carte.get("titlu", "").lower():
                gasit = True
            elif tip_cautare == "author" and termen_lower in carte.get("autor", "").lower():
                gasit = True
            elif tip_cautare == "isbn" and termen_lower in carte.get("isbn", "").lower():
                gasit = True
            elif tip_cautare == "category" and termen_lower in carte.get("categorie", "").lower():
                gasit = True

            if gasit:
                rezultate.append(carte)

        if not rezultate:
            print(f"\n Nu s-au gasit carti pentru '{termen}' (cautare dupa {tip_cautare})\n")
            return

        print("")
        print("=" * 60)
        print(f"  Rezultate cautare {tip_cautare}: \"{termen}\"")
        print("=" * 60)

        for i, carte in enumerate(rezultate, 1):
            status_icon = "✓" if carte['status'] == "DISPONIBIL" else "X"
            popular = " (Popular!)" if carte.get('nr_imprumuturi', 0) > 10 else ""

            print(f"\n{i}. {carte['titlu']}")
            print(f"   Autor: {carte['autor']}")
            print(f"   ISBN: {carte.get('isbn', 'N/A')}")
            print(f"   Status: {status_icon} {carte['status']}")

            # afiseaza data returnare daca e imprumutata
            if carte['status'] == "IMPRUMUTAT":
                for imp in self.date["imprumuturi"]:
                    if imp.get("id_carte") == carte["id"] and imp.get("status") == "ACTIV":
                        print(f"   Returnare estimata: {imp.get('data_retur', 'N/A')}")
                        break

            print(f"   Categorie: {carte.get('categorie', 'N/A')}")
            if carte.get('an'):
                print(f"   An publicare: {carte['an']}")
            print(f"   Imprumuturi totale: {carte.get('nr_imprumuturi', 0)}{popular}")

        print(f"\n  Total gasite: {len(rezultate)} carti")
        print("=" * 60)
        print("")

    def _gaseste_carte(self, identificator: str) -> Optional[Dict]:
        """Gaseste o carte dupa titlu, ISBN sau ID"""
        for carte in self.date["carti"]:
            if carte.get("titlu", "").lower() == identificator.lower():
                return carte
            if carte.get("isbn", "") == identificator:
                return carte
            if str(carte.get("id", "")) == identificator:
                return carte
        return None

    def sterge_carte(self, identificator: str) -> None:
        """Sterge o carte din catalog"""
        carte = self._gaseste_carte(identificator)

        if not carte:
            print(f"EROARE! Cartea '{identificator}' nu a fost gasita!")
            return

        if carte['status'] != "DISPONIBIL":
            print("EROARE! Nu poti sterge o carte care este imprumutata!")
            return

        self.date["carti"].remove(carte)
        self._salveaza_date()

        print(f"\n Cartea '{carte['titlu']}' a fost stearsa din catalog.\n")

    # gestionare utilizatori
    
    def adauga_utilizator(self, nume: str, id_utilizator: str, email: str = None) -> None:
        """Inregistreaza un utilizator nou"""
        id_utilizator = str(id_utilizator)

        # Verificare ID unic
        for user in self.date["utilizatori"]:
            if str(user.get("id")) == id_utilizator:
                print(f"EROARE! Un utilizator cu ID {id_utilizator} exista deja!")
                return

        # Validare email
        if email and '@' not in email:
            print("EROARE! Formatul email-ului nu este valid!")
            return

        utilizator_nou = {
            "id": id_utilizator,
            "nume": nume,
            "email": email if email else "N/A",
            "data_inregistrare": datetime.now().strftime(DATE_FORMAT),
            "imprumuturi_active": 0,
            "total_imprumuturi": 0,
            "total_penalitati": 0,
            "status": "ACTIV"
        }

        self.date["utilizatori"].append(utilizator_nou)
        self._salveaza_date()

        print("")
        print("=" * 50)
        print("      ✓ UTILIZATOR ADAUGAT CU SUCCES!")
        print("=" * 50)
        print(f"  Nume:              {nume}")
        print(f"  ID:                {id_utilizator}")
        print(f"  Email:             {utilizator_nou['email']}")
        print(f"  Data inregistrare: {utilizator_nou['data_inregistrare']}")
        print(f"  Carti imprumutate: 0")
        print(f"  Status:            ACTIV")
        print("=" * 50)
        print("")

    def listeaza_utilizatori(self) -> None:
        """Listeaza toti utilizatorii"""
        utilizatori = self.date["utilizatori"]

        if not utilizatori:
            print("\n Nu exista utilizatori inregistrati.\n")
            return

        print("")
        print("=" * 70)
        print(f"  UTILIZATORI INREGISTRATI ({len(utilizatori)} total)")
        print("=" * 70)
        print(f"{'ID':<10} {'Nume':<25} {'Email':<25} {'Impr. Active':<10}")
        print("-" * 70)

        for user in utilizatori:
            nume = user['nume'][:23] + ".." if len(user['nume']) > 25 else user['nume']
            email = user.get('email', 'N/A')[:23] + ".." if len(user.get('email', 'N/A')) > 25 else user.get('email', 'N/A')
            print(f"{user['id']:<10} {nume:<25} {email:<25} {user.get('imprumuturi_active', 0):<10}")
        print("=" * 70)
        print("")

    def _gaseste_utilizator(self, id_utilizator: str) -> Optional[Dict]:
        """Gaseste un utilizator dupa ID"""
        id_utilizator = str(id_utilizator)
        for user in self.date["utilizatori"]:
            if str(user.get("id")) == id_utilizator:
                return user
        return None

    def dezactiveaza_utilizator(self, id_utilizator: str) -> None:
        """Dezactiveaza un utilizator"""
        utilizator = self._gaseste_utilizator(id_utilizator)
        if not utilizator:
            print(f"EROARE! Utilizatorul cu ID '{id_utilizator}' nu exista!")
            return

        if utilizator.get('imprumuturi_active', 0) > 0:
            print(f"EROARE! Utilizatorul are {utilizator['imprumuturi_active']} imprumuturi active!")
            print("Returneaza cartile inainte de a dezactiva contul.")
            return

        utilizator['status'] = "INACTIV"
        self._salveaza_date()

        print(f"\n Utilizatorul '{utilizator['nume']}' a fost dezactivat.\n")

    #imprumuturi

    def imprumuta_carte(self, identificator: str, id_utilizator: str, zile: int = 14) -> None:
        """Imprumuta o carte (dupa titlu sau ISBN)"""
        print("\nVerificare disponibilitate...")

        id_utilizator = str(id_utilizator)

        # Gasesc cartea
        carte = self._gaseste_carte(identificator)
        if not carte:
            print(f"EROARE! Cartea '{identificator}' nu a fost gasita!")
            return

        # Gasesc utilizatorul
        utilizator = self._gaseste_utilizator(id_utilizator)
        if not utilizator:
            print(f"EROARE! Utilizatorul cu ID '{id_utilizator}' nu exista!")
            return

        # Verific statusul utilizatorului
        if utilizator.get('status') != "ACTIV":
            print("EROARE! Contul utilizatorului este inactiv!")
            return

        # Verific disponibilitate cartii
        if carte["status"] != "DISPONIBIL":
            print(f"EROARE! Cartea '{carte['titlu']}' nu este disponibila!")
            for imp in self.date["imprumuturi"]:
                if imp.get("id_carte") == carte["id"] and imp.get("status") == "ACTIV":
                    print(f"         Returnare estimata: {imp.get('data_retur', 'N/A')}")
                    break
            return

        # Validare numar de zile
        if zile < 1 or zile > 60:
            print("EROARE! Perioada de imprumut trebuie sa fie intre 1 si 60 de zile!")
            return

        print("✓ Carte disponibila!")
        print("✓ Utilizator valid!")

        # Creez imprumutul
        data_imprumut = datetime.now()
        data_retur = data_imprumut + timedelta(days=zile)

        imprumut = {
            "id": len(self.date["imprumuturi"]) + 1,
            "id_carte": carte["id"],
            "titlu_carte": carte["titlu"],
            "id_utilizator": id_utilizator,
            "nume_utilizator": utilizator["nume"],
            "data_imprumut": data_imprumut.strftime(DATE_FORMAT),
            "data_retur": data_retur.strftime(DATE_FORMAT),
            "data_returnare_efectiva": None,
            "status": "ACTIV",
            "penalitate": 0
        }

        self.date["imprumuturi"].append(imprumut)

        # Actualizez statusul cartii
        carte["status"] = "IMPRUMUTAT"
        carte["nr_imprumuturi"] = carte.get("nr_imprumuturi", 0) + 1

        # Actualizez utilizatorul
        utilizator["imprumuturi_active"] = utilizator.get("imprumuturi_active", 0) + 1
        utilizator["total_imprumuturi"] = utilizator.get("total_imprumuturi", 0) + 1

        self._salveaza_date()

        print("")
        print("=" * 50)
        print("      ✓ IMPRUMUT INREGISTRAT!")
        print("=" * 50)
        print(f"  Carte:         {carte['titlu']} ({carte['autor']})")
        print(f"  Utilizator:    {utilizator['nume']} (ID: {id_utilizator})")
        print(f"  Data imprumut: {imprumut['data_imprumut']}")
        print(f"  Data returnare: {imprumut['data_retur']} ({zile} zile)")
        print("=" * 50)
        print(f"\n⚠️  Reminder: Returneaza cartea pana la {imprumut['data_retur']}")
        print("   pentru a evita penalitati!\n")

    def returneaza_carte(self, identificator: str, id_utilizator: str) -> None:
        """Returneaza o carte imprumutata"""
        print("\nProcesare returnare...")

        id_utilizator = str(id_utilizator)

        carte = self._gaseste_carte(identificator)
        if not carte:
            print(f"EROARE! Cartea '{identificator}' nu a fost gasita!")
            return

        utilizator = self._gaseste_utilizator(id_utilizator)
        if not utilizator:
            print(f"EROARE! Utilizatorul cu ID '{id_utilizator}' nu exista!")
            return

        # Caut imprumutul activ
        imprumut_activ = None
        for imp in self.date["imprumuturi"]:
            if (imp.get("id_carte") == carte["id"] and
                str(imp.get("id_utilizator")) == id_utilizator and
                imp.get("status") == "ACTIV"):
                imprumut_activ = imp
                break

        if not imprumut_activ:
            print(f"EROARE! Nu exista un imprumut activ pentru '{carte['titlu']}' de catre utilizatorul {id_utilizator}!")
            return

        # Calculez intarzierea
        data_azi = datetime.now()
        data_limita = datetime.strptime(imprumut_activ["data_retur"], DATE_FORMAT)
        zile_imprumut = (data_azi - datetime.strptime(imprumut_activ["data_imprumut"], DATE_FORMAT)).days

        penalitate = 0
        zile_intarziere = 0

        if data_azi.date() > data_limita.date():
            zile_intarziere = (data_azi.date() - data_limita.date()).days
            penalitate = zile_intarziere * PENALITATE_PE_ZI

        # Actualizez imprumutul
        imprumut_activ["data_returnare_efectiva"] = data_azi.strftime(DATE_FORMAT)
        imprumut_activ["status"] = "RETURNAT"
        imprumut_activ["penalitate"] = penalitate

        # Actualizez disponibilitatea cartii 
        carte["status"] = "DISPONIBIL"

        # Actualizez statusul imprumuturilor utilizatorului
        utilizator["imprumuturi_active"] = max(0, utilizator.get("imprumuturi_active", 1) - 1)
        utilizator["total_penalitati"] = utilizator.get("total_penalitati", 0) + penalitate

        self._salveaza_date()

        print("")
        print("=" * 50)
        print("      ✓ CARTE RETURNATA CU SUCCES!")
        print("=" * 50)
        print(f"  Carte:             {carte['titlu']}")
        print(f"  Utilizator:        {utilizator['nume']}")
        print(f"  Data imprumut:     {imprumut_activ['data_imprumut']}")
        print(f"  Data returnare:    {data_azi.strftime(DATE_FORMAT)}")
        print(f"  Zile imprumut:     {zile_imprumut} zile")
        print("-" * 50)

        if zile_intarziere > 0:
            print(f"  ⚠️  Intarziere:    {zile_intarziere} zile")
            print(f"    Penalitate:    {penalitate} RON")
        else:
            print("  ✓ Returnat la timp!")
            print("  ✓ Fara penalitati!")

        print("=" * 50)
        print("\n📚 Cartea este acum DISPONIBILA pentru imprumut.\n")

   #rapoarte

    def genereaza_raport(self, tip_raport: str, top: int = 10) -> None:
        """Genereaza diverse rapoarte"""
        if tip_raport == "overdue":
            self._raport_intarziate()
        elif tip_raport == "borrowed":
            self._raport_imprumutate()
        elif tip_raport == "popular":
            self._raport_populare(top)
        elif tip_raport == "users":
            self._raport_utilizatori_activi(top)
        else:
            print(f"EROARE! Tip raport invalid: {tip_raport}")
            print("Tipuri disponibile: overdue, borrowed, popular, users")

    def _raport_intarziate(self) -> None:
        """Raport cu cartile intarziate"""
        azi = datetime.now().date()
        intarziate = []

        for imp in self.date["imprumuturi"]:
            if imp.get("status") == "ACTIV":
                data_limita = datetime.strptime(imp["data_retur"], DATE_FORMAT).date()
                if azi >= data_limita:
                    zile = (azi - data_limita).days
                    imp_copie = imp.copy()
                    imp_copie["zile_intarziere"] = zile
                    imp_copie["penalitate_curenta"] = zile * PENALITATE_PE_ZI
                    intarziate.append(imp_copie)

        print("")
        print("=" * 65)
        print(f"  RAPORT CARTI INTARZIATE - {azi}")
        print("=" * 65)

        if not intarziate:
            print("\n  Nu exista carti intarziate!\n")
            print("=" * 65)
            print("")
            return

        print(f"\n  {len(intarziate)} carti sunt returnate cu intarziere:\n")

        total_penalitati = 0
        for i, imp in enumerate(intarziate, 1):
            carte = self._gaseste_carte(str(imp["id_carte"]))
            autor = carte.get("autor", "N/A") if carte else "N/A"

            print(f"  {i}. {imp['titlu_carte']} ({autor})")
            print(f"     Utilizator: {imp['nume_utilizator']} (ID: {imp['id_utilizator']})")
            print(f"     Deadline: {imp['data_retur']}")

            if imp["zile_intarziere"] == 0:
                print(f"     Intarziere: 0 zile (scadent ASTAZI!)")
            else:
                print(f"     Intarziere: {imp['zile_intarziere']} zile")

            print(f"     Penalitate: {imp['penalitate_curenta']} RON")
            total_penalitati += imp["penalitate_curenta"]
            print("")

        print("-" * 65)
        print(f"  Total penalitati de colectat: {total_penalitati} RON")
        print("")
        print("  Actiuni recomandate:")
        for imp in intarziate:
            if imp["zile_intarziere"] == 0:
                print(f"    ✉ Trimite reminder catre {imp['nume_utilizator']} (scadent astazi)")
            else:
                print(f"    ✉ Trimite notificare penalitate catre {imp['nume_utilizator']}")
        print("=" * 65)
        print("")

    def _raport_imprumutate(self) -> None:
        """Raport cu cartile imprumutate"""
        active = [imp for imp in self.date["imprumuturi"] if imp.get("status") == "ACTIV"]

        print("")
        print("=" * 75)
        print(f"  CARTI IMPRUMUTATE ({len(active)} total)")
        print("=" * 75)

        if not active:
            print("\n  Nu exista carti imprumutate in acest moment.\n")
            print("=" * 75)
            print("")
            return

        print(f"{'ID':<5} {'Titlu':<22} {'Imprumutat de':<18} {'Imprumut':<12} {'Return':<12}")
        print("-" * 75)

        for imp in active:
            titlu = imp['titlu_carte'][:20] + ".." if len(imp['titlu_carte']) > 22 else imp['titlu_carte']
            nume = imp['nume_utilizator'][:16] + ".." if len(imp['nume_utilizator']) > 18 else imp['nume_utilizator']
            print(f"{imp['id_carte']:<5} {titlu:<22} {nume:<18} {imp['data_imprumut']:<12} {imp['data_retur']:<12}")

        print("=" * 75)
        print("")

    def _raport_populare(self, top: int = 10) -> None:
        """Raport cu cartile populare"""
        carti_sortate = sorted(
            self.date["carti"],
            key=lambda x: x.get("nr_imprumuturi", 0),
            reverse=True
        )[:top]

        print("")
        print("=" * 60)
        print(f"  TOP {min(top, len(carti_sortate))} CARTI POPULARE")
        print("=" * 60)

        if not carti_sortate:
            print("\n  Nu exista carti in biblioteca.\n")
            print("=" * 60)
            return

        for i, carte in enumerate(carti_sortate, 1):
            nr_imp = carte.get('nr_imprumuturi', 0)
            if nr_imp > 0:
                print(f"  {i}. \"{carte['titlu']}\" - {nr_imp} imprumuturi")

        print("=" * 60)
        print("")

    def _raport_utilizatori_activi(self, top: int = 10) -> None:
        """Raport cu utilizatorii activi"""
        utilizatori_sortati = sorted(
            self.date["utilizatori"],
            key=lambda x: x.get("total_imprumuturi", 0),
            reverse=True
        )[:top]

        print("")
        print("=" * 60)
        print(f"  TOP {min(top, len(utilizatori_sortati))} UTILIZATORI ACTIVI")
        print("=" * 60)

        if not utilizatori_sortati:
            print("\n  Nu exista utilizatori inregistrati.\n")
            print("=" * 60)
            return

        for i, user in enumerate(utilizatori_sortati, 1):
            nr_imp = user.get('total_imprumuturi', 0)
            if nr_imp > 0:
                print(f"  {i}. {user['nume']} - {nr_imp} imprumuturi")
        print("=" * 60)
        print("")

    def afiseaza_statistici(self, top: int = 5) -> None:
        """Afiseaza statistici complete despre biblioteca"""
        carti = self.date["carti"]
        utilizatori = self.date["utilizatori"]
        imprumuturi = self.date["imprumuturi"]

        total_carti = len(carti)
        carti_disponibile = len([c for c in carti if c.get("status") == "DISPONIBIL"])
        carti_imprumutate = total_carti - carti_disponibile

        total_utilizatori = len(utilizatori)
        utilizatori_activi = len([u for u in utilizatori if u.get("imprumuturi_active", 0) > 0])

        total_imprumuturi = len(imprumuturi)
        imprumuturi_active = len([i for i in imprumuturi if i.get("status") == "ACTIV"])

        # Carti intarziate
        azi = datetime.now().date()
        intarziate = 0
        for imp in imprumuturi:
            if imp.get("status") == "ACTIV":
                data_limita = datetime.strptime(imp["data_retur"], DATE_FORMAT).date()
                if azi > data_limita:
                    intarziate += 1

        # Categorii si autori unici
        categorii = set(c.get("categorie", "N/A") for c in carti)
        autori = set(c.get("autor", "N/A") for c in carti)

        # Rata returnare la timp
        returnate = [i for i in imprumuturi if i.get("status") == "RETURNAT"]
        la_timp = len([i for i in returnate if i.get("penalitate", 0) == 0])
        rata_la_timp = (la_timp / len(returnate) * 100) if returnate else 100

        # Total penalitati
        total_penalitati = sum(i.get("penalitate", 0) for i in returnate)

        luna_curenta = datetime.now().strftime("%B %Y")

        print("")
        print("=" * 60)
        print(f"  STATISTICI BIBLIOTECA - {luna_curenta}")
        print("=" * 60)
        
        print("\n  COLECTIE:")
        print(f"    Total carti:    {total_carti}")
        print(f"    Categorii:      {len(categorii)}")
        print(f"    Autori unici:   {len(autori)}")

        print("\n  STATUS CARTI:")
        if total_carti > 0:
            procent_disp = (carti_disponibile / total_carti) * 100
            procent_imp = (carti_imprumutate / total_carti) * 100
            bar_disp = "█" * int(procent_disp / 5) + "░" * (20 - int(procent_disp / 5))
            bar_imp = "█" * int(procent_imp / 5) + "░" * (20 - int(procent_imp / 5))
            print(f"    Disponibile: {carti_disponibile} ({procent_disp:.1f}%) {bar_disp}")
            print(f"    Imprumutate: {carti_imprumutate} ({procent_imp:.1f}%) {bar_imp}")
        else:
            print("    Nu exista carti.")
        print("\n  UTILIZATORI:")
        print(f"    Total inregistrati:     {total_utilizatori}")
        print(f"    Cu imprumuturi active:  {utilizatori_activi}")
        print("\n  IMPRUMUTURI:")
        print(f"    Total (toate timpurile): {total_imprumuturi}")
        print(f"    Active:                  {imprumuturi_active}")
        print(f"    Intarziate:              {intarziate}")
        print(f"    Rata returnare la timp:  {rata_la_timp:.0f}%")

        # Top carti populare
        if carti:
            print(f"\n  TOP {top} CARTI POPULARE:")
            carti_sortate = sorted(carti, key=lambda x: x.get("nr_imprumuturi", 0), reverse=True)[:top]
            for i, carte in enumerate(carti_sortate, 1):
                nr = carte.get('nr_imprumuturi', 0)
                if nr > 0:
                    print(f"  {i}. \"{carte['titlu']}\" - {nr} imprumuturi")

        # Top categorii
        if carti:
            print(f"\n  TOP 3 CATEGORII:")
            cat_count = {}
            for c in carti:
                cat = c.get("categorie", "N/A")
                cat_count[cat] = cat_count.get(cat, 0) + 1
            sorted_cats = sorted(cat_count.items(), key=lambda x: x[1], reverse=True)[:3]
            for i, (cat, count) in enumerate(sorted_cats, 1):
                pct = (count / total_carti * 100) if total_carti > 0 else 0
                print(f"  {i}. {cat} - {count} carti ({pct:.1f}%)")

        # Top utilizatori
        if utilizatori:
            print(f"\n  TOP 3 UTILIZATORI ACTIVI:")
            util_sortati = sorted(utilizatori, key=lambda x: x.get("total_imprumuturi", 0), reverse=True)[:3]
            for i, user in enumerate(util_sortati, 1):
                nr = user.get('total_imprumuturi', 0)
                if nr > 0:
                    print(f"  {i}. {user['nume']} - {nr} imprumuturi")

        print(f"\n  VENITURI (din penalitati):")
        print(f"    Total colectat: {total_penalitati} RON")
        print("")
        print("=" * 60)
        print("")
 #EXPORT IMPORT 

    def exporta_date(self, fisier: str, format_export: str = "csv") -> None:
        """Exporta datele in format CSV"""
        if format_export != "csv":
            print(f"EROARE! Format necunoscut: {format_export}. Foloseste 'csv'.")
            return

        print("\nExport in desfasurare...")

        # Determinam directorul de iesire (implicit folderul data)
        output_dir = os.path.dirname(fisier) or DATA_DIR
        os.makedirs(output_dir, exist_ok=True)

        # Calculam imprumuturile active 
        active = [i for i in self.date["imprumuturi"] if i.get("status") == "ACTIV"]

        # Export catalog de carti
        fisier_carti = os.path.join(output_dir, "library_catalog.csv")
        fieldnames_carti = ['id', 'titlu', 'autor', 'isbn', 'categorie', 'an', 'status', 'data_adaugare', 'nr_imprumuturi']
        with open(fisier_carti, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames_carti, extrasaction='ignore')
            writer.writeheader()
            if self.date["carti"]:
                writer.writerows(self.date["carti"])

        # Export lista de utilizatori
        fisier_util = os.path.join(output_dir, "users.csv")
        fieldnames_util = ['id', 'nume', 'email', 'data_inregistrare', 'imprumuturi_active', 'total_imprumuturi', 'status']
        with open(fisier_util, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames_util, extrasaction='ignore')
            writer.writeheader()
            if self.date["utilizatori"]:
                writer.writerows(self.date["utilizatori"])

        # Export imprumuturi active
        fisier_active = os.path.join(output_dir, "active_loans.csv")
        fieldnames_imp = ['id', 'id_carte', 'titlu_carte', 'id_utilizator', 'nume_utilizator', 'data_imprumut', 'data_retur', 'status']
        with open(fisier_active, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames_imp, extrasaction='ignore')
            writer.writeheader()
            if active:
                writer.writerows(active)

        # 4. Export istoric complet utilizatori
        fisier_history = os.path.join(output_dir, "user_history.csv")
        with open(fisier_history, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames_imp + ['data_returnare_efectiva', 'penalitate'], extrasaction='ignore')
            writer.writeheader()
            if self.date["imprumuturi"]:
                writer.writerows(self.date["imprumuturi"])

        # Mesaje de export
        print(f" Exportat {len(self.date['carti'])} cărți")
        print(f" Exportat {len(self.date['utilizatori'])} utilizatori")
        print(f" Exportat {len(active)} împrumuturi active")

        print("\nFișiere generate:")
        print("• library_catalog.csv (catalog complet)")
        print("• users.csv (lista utilizatori)")
        print("• active_loans.csv (împrumuturi active)")
        print("• user_history.csv (istoric utilizatori)")
        print("\nExport complet.")

    def importa_date(self, fisier: str) -> None:
        """Importa carti din fisier CSV"""
        if not os.path.exists(fisier):
            print(f"EROARE! Fisierul '{fisier}' nu exista!")
            return

        print(f"\nImport din {fisier}...")

        importate = 0
        ignorate = 0

        try:
            with open(fisier, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)

                for rand in reader:
                    # Verific daca exista deja
                    isbn = rand.get('isbn', rand.get('ISBN', ''))
                    if isbn and isbn != 'N/A':
                        exista = any(c.get('isbn') == isbn for c in self.date["carti"])
                        if exista:
                            ignorate += 1
                            continue

                    # Verificare de baza
                    titlu = rand.get('titlu', rand.get('title', '')).strip()
                    autor = rand.get('autor', rand.get('author', '')).strip()

                    if not titlu or not autor:
                        ignorate += 1
                        continue

                    an_str = rand.get('an', rand.get('year', ''))
                    an = int(an_str) if an_str.isdigit() else None

                    carte = {
                        "id": self._genereaza_id_carte(),
                        "titlu": titlu,
                        "autor": autor,
                        "isbn": isbn if isbn else "N/A",
                        "categorie": rand.get('categorie', rand.get('category', 'Necategorizat')),
                        "an": an,
                        "status": "DISPONIBIL",
                        "data_adaugare": datetime.now().strftime(DATE_FORMAT),
                        "nr_imprumuturi": 0
                    }
                    self.date["carti"].append(carte)
                    importate += 1

            self._salveaza_date()
            print(f" Importat {importate} carti noi!")
            if ignorate > 0:
                print(f" {ignorate} inregistrari ignorate (duplicate sau invalide).")
            print("")

        except Exception as e:
            print(f"EROARE! Eroare la import: {e}")

def creeaza_parser() -> argparse.ArgumentParser:
    """Creeaza parserul pentru linia de comanda"""
    parser = argparse.ArgumentParser(
        description="Library Manager - Sistem de management pentru biblioteca ",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Exemple de utilizare:
  %(prog)s add_book "1984" "George Orwell" --isbn 9780451524935 --category "Fiction"
  %(prog)s add_user "Popescu Ion" --id 1001 --email "ion@example.com"
  %(prog)s borrow "1984" --user_id 1001 --days 14
  %(prog)s return "1984" --user_id 1001
  %(prog)s search --author "Orwell"
  %(prog)s search --title "1984"
  %(prog)s list --status borrowed
  %(prog)s report --overdue
  %(prog)s stats
  %(prog)s export catalog.csv
        """
    )

    subparsers = parser.add_subparsers(dest="comanda", help="Comenzi disponibile")

    # adaugare carte
    p = subparsers.add_parser("add_book", help="Adauga o carte noua")
    p.add_argument("title", help="Titlul cartii")
    p.add_argument("author", help="Autorul cartii")
    p.add_argument("--isbn", help="Codul ISBN")
    p.add_argument("--category", help="Categoria cartii")
    p.add_argument("--year", type=int, help="Anul publicarii")

    # adaugare utilizator
    p = subparsers.add_parser("add_user", help="Adauga un utilizator nou")
    p.add_argument("name", help="Numele utilizatorului")
    p.add_argument("--id", required=True, dest="user_id", help="ID-ul utilizatorului")
    p.add_argument("--email", help="Adresa de email")

    # listare
    p = subparsers.add_parser("list", help="Listeaza carti sau utilizatori")
    p.add_argument("--type", choices=["books", "users"], default="books", help="Ce sa listeze")
    p.add_argument("--status", help="Filtreaza dupa status (available/borrowed)")

    # cautare
    p = subparsers.add_parser("search", help="Cauta carti")
    p.add_argument("query", nargs="?", help="Termen de cautare (optional)")
    p.add_argument("--title", help="Cauta dupa titlu")
    p.add_argument("--author", help="Cauta dupa autor")
    p.add_argument("--isbn", help="Cauta dupa ISBN")
    p.add_argument("--category", help="Cauta dupa categorie")

    # imprumut
    p = subparsers.add_parser("borrow", help="Imprumuta o carte")
    p.add_argument("book", help="Titlul sau ISBN-ul cartii")
    p.add_argument("--user_id", required=True, help="ID-ul utilizatorului")
    p.add_argument("--days", type=int, default=14, help="Numarul de zile (default: 14)")

    # returnare
    p = subparsers.add_parser("return", help="Returneaza o carte")
    p.add_argument("book", help="Titlul sau ISBN-ul cartii")
    p.add_argument("--user_id", required=True, help="ID-ul utilizatorului")

    # sterge carte
    p = subparsers.add_parser("delete_book", help="Sterge o carte")
    p.add_argument("book", help="Titlul sau ISBN-ul cartii")

    # sterge utilizator
    p = subparsers.add_parser("delete_user", help="Dezactiveaza un utilizator")
    p.add_argument("user_id", help="ID-ul utilizatorului")

    # report
    p = subparsers.add_parser("report", help="Genereaza rapoarte")
    p.add_argument("--overdue", action="store_true", help="Raport carti intarziate")
    p.add_argument("--borrowed", action="store_true", help="Raport carti imprumutate")
    p.add_argument("--popular", action="store_true", help="Raport carti populare")
    p.add_argument("--users", action="store_true", help="Raport utilizatori activi")
    p.add_argument("--top", type=int, default=10, help="Numarul de rezultate pentru top")

    # statistici
    p = subparsers.add_parser("stats", help="Afiseaza statistici")
    p.add_argument("--top", type=int, default=5, help="Numarul de rezultate pentru top-uri")

    # export
    p = subparsers.add_parser("export", help="Exporta datele in CSV")
    p.add_argument("filename", help="Numele fisierului de export")
    p.add_argument("--format", choices=["csv"], default="csv", help="Formatul exportului")

    # import
    p = subparsers.add_parser("import", help="Importa carti din CSV")
    p.add_argument("filename", help="Fisierul CSV de importat")

    return parser

def main():
    parser = creeaza_parser()
    args = parser.parse_args()

    if not args.comanda:
        parser.print_help()
        return

    manager = LibraryManager()

    # Executie comenzi
    if args.comanda == "add_book":
        manager.adauga_carte(args.title, args.author, args.isbn, args.category, args.year)

    elif args.comanda == "add_user":
        manager.adauga_utilizator(args.name, args.user_id, args.email)

    elif args.comanda == "list":
        if args.type == "users":
            manager.listeaza_utilizatori()
        else:
            manager.listeaza_carti(args.status)

    elif args.comanda == "search":
        if args.author:
            manager.cauta_carti(args.author, "author")
        elif args.title:
            manager.cauta_carti(args.title, "title")
        elif args.isbn:
            manager.cauta_carti(args.isbn, "isbn")
        elif args.category:
            manager.cauta_carti(args.category, "category")
        elif args.query:
            manager.cauta_carti(args.query, "title")
        else:
            print("\n EROARE! Specifica un criteriu de cautare!")
            print("Exemple:")
            print('  search --author "Orwell"')
            print('  search --title "1984"')
            print('  search --isbn "9780451524935"')
            print('  search --category "Fiction"')

    elif args.comanda == "borrow":
        manager.imprumuta_carte(args.book, args.user_id, args.days)

    elif args.comanda == "return":
        manager.returneaza_carte(args.book, args.user_id)

    elif args.comanda == "delete_book":
        manager.sterge_carte(args.book)

    elif args.comanda == "delete_user":
        manager.dezactiveaza_utilizator(args.user_id)

    elif args.comanda == "report":
        if args.overdue:
            tip_raport = "overdue"
        elif args.borrowed:
            tip_raport = "borrowed"
        elif args.popular:
            tip_raport = "popular"
        elif args.users:
            tip_raport = "users"
        else:
            tip_raport = "overdue"
        manager.genereaza_raport(tip_raport, args.top)

    elif args.comanda == "stats":
        manager.afiseaza_statistici(args.top)

    elif args.comanda == "export":
        manager.exporta_date(args.filename, args.format)

    elif args.comanda == "import":
        manager.importa_date(args.filename)


if __name__ == "__main__":
    main()