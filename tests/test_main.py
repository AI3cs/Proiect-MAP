#!/usr/bin/env python3
"""
Teste pentru Library Manager
Proiect Sincretic - Tema 22
"""

import json
import os
import sys
import tempfile
import unittest

# adaug calea catre src
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import LibraryManager


class TestCarti(unittest.TestCase):
    """teste pentru functiile cu carti"""
    
    def setUp(self):
        # creez un fisier temporar pentru teste
        self.fisier_temp = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.fisier_temp.close()
        self.manager = LibraryManager(self.fisier_temp.name)
    
    def tearDown(self):
        # sterg fisierul dupa test
        if os.path.exists(self.fisier_temp.name):
            os.unlink(self.fisier_temp.name)
    
    def test_adauga_carte_simplu(self):
        """test adaugare carte cu date minime"""
        self.manager.adauga_carte("Carte Test", "Autor Test")
        
        # verific ca s-a adaugat
        self.assertEqual(len(self.manager.date["carti"]), 1)
        self.assertEqual(self.manager.date["carti"][0]["titlu"], "Carte Test")
        self.assertEqual(self.manager.date["carti"][0]["autor"], "Autor Test")
        self.assertEqual(self.manager.date["carti"][0]["status"], "DISPONIBIL")
    
    def test_adauga_carte_complet(self):
        """test adaugare carte cu toate datele"""
        self.manager.adauga_carte("1984", "George Orwell", "9780451524935", "Fiction", 1949)
        
        carte = self.manager.date["carti"][0]
        self.assertEqual(carte["isbn"], "9780451524935")
        self.assertEqual(carte["categorie"], "Fiction")
        self.assertEqual(carte["an"], 1949)
    
    def test_isbn_duplicat(self):
        """test ca nu se poate adauga carte cu isbn duplicat"""
        self.manager.adauga_carte("Carte 1", "Autor 1", "123456")
        self.manager.adauga_carte("Carte 2", "Autor 2", "123456")
        
        # trebuie sa fie doar o carte
        self.assertEqual(len(self.manager.date["carti"]), 1)
    
    def test_id_uri_unice(self):
        """test ca id-urile sunt unice"""
        self.manager.adauga_carte("Carte 1", "Autor 1")
        self.manager.adauga_carte("Carte 2", "Autor 2")
        
        self.assertEqual(self.manager.date["carti"][0]["id"], 1)
        self.assertEqual(self.manager.date["carti"][1]["id"], 2)
    
    def test_gaseste_carte_titlu(self):
        """test gasire carte dupa titlu"""
        self.manager.adauga_carte("Carte Test", "Autor Test")
        
        carte = self.manager._gaseste_carte("Carte Test")
        self.assertIsNotNone(carte)
        self.assertEqual(carte["titlu"], "Carte Test")
    
    def test_gaseste_carte_isbn(self):
        """test gasire carte dupa isbn"""
        self.manager.adauga_carte("Carte Test", "Autor Test", "123456")
        
        carte = self.manager._gaseste_carte("123456")
        self.assertIsNotNone(carte)
    
    def test_carte_inexistenta(self):
        """test carte care nu exista"""
        carte = self.manager._gaseste_carte("Nu exista")
        self.assertIsNone(carte)


class TestUtilizatori(unittest.TestCase):
    """teste pentru utilizatori"""
    
    def setUp(self):
        self.fisier_temp = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.fisier_temp.close()
        self.manager = LibraryManager(self.fisier_temp.name)
    
    def tearDown(self):
        if os.path.exists(self.fisier_temp.name):
            os.unlink(self.fisier_temp.name)
    
    def test_adauga_utilizator(self):
        """test adaugare utilizator"""
        self.manager.adauga_utilizator("Ion Popescu", "1001")
        
        self.assertEqual(len(self.manager.date["utilizatori"]), 1)
        self.assertEqual(self.manager.date["utilizatori"][0]["nume"], "Ion Popescu")
        self.assertEqual(self.manager.date["utilizatori"][0]["id"], "1001")
    
    def test_adauga_utilizator_email(self):
        """test utilizator cu email"""
        self.manager.adauga_utilizator("Ion Popescu", "1001", "ion@test.com")
        self.assertEqual(self.manager.date["utilizatori"][0]["email"], "ion@test.com")
    
    def test_id_duplicat(self):
        """test ca nu se poate adauga utilizator cu id duplicat"""
        self.manager.adauga_utilizator("User 1", "1001")
        self.manager.adauga_utilizator("User 2", "1001")
        
        self.assertEqual(len(self.manager.date["utilizatori"]), 1)
    
    def test_gaseste_utilizator(self):
        """test gasire utilizator"""
        self.manager.adauga_utilizator("Ion Popescu", "1001")
        
        user = self.manager._gaseste_utilizator("1001")
        self.assertIsNotNone(user)
        self.assertEqual(user["nume"], "Ion Popescu")


class TestImprumuturi(unittest.TestCase):
    """teste pentru imprumuturi"""
    
    def setUp(self):
        self.fisier_temp = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.fisier_temp.close()
        self.manager = LibraryManager(self.fisier_temp.name)
    
    def tearDown(self):
        if os.path.exists(self.fisier_temp.name):
            os.unlink(self.fisier_temp.name)
    
    def test_imprumut_succes(self):
        """test imprumut cu succes"""
        self.manager.adauga_carte("Carte Test", "Autor Test")
        self.manager.adauga_utilizator("Ion Popescu", "1001")
        self.manager.imprumuta_carte("Carte Test", "1001", 14)
        
        # verific ca s-a creat imprumutul
        self.assertEqual(len(self.manager.date["imprumuturi"]), 1)
        self.assertEqual(self.manager.date["imprumuturi"][0]["status"], "ACTIV")
        
        # verific ca cartea e imprumutata
        carte = self.manager._gaseste_carte("Carte Test")
        self.assertEqual(carte["status"], "IMPRUMUTAT")
        
        # verific utilizatorul
        user = self.manager._gaseste_utilizator("1001")
        self.assertEqual(user["imprumuturi_active"], 1)
    
    def test_carte_indisponibila(self):
        """test imprumut carte indisponibila"""
        self.manager.adauga_carte("Carte Test", "Autor Test")
        self.manager.adauga_utilizator("User 1", "1001")
        self.manager.adauga_utilizator("User 2", "1002")
        
        self.manager.imprumuta_carte("Carte Test", "1001")
        self.manager.imprumuta_carte("Carte Test", "1002")
        
        # doar un imprumut
        self.assertEqual(len(self.manager.date["imprumuturi"]), 1)
    
    def test_returnare_succes(self):
        """test returnare carte"""
        self.manager.adauga_carte("Carte Test", "Autor Test")
        self.manager.adauga_utilizator("Ion Popescu", "1001")
        self.manager.imprumuta_carte("Carte Test", "1001")
        self.manager.returneaza_carte("Carte Test", "1001")
        
        # verific ca e returnata
        self.assertEqual(self.manager.date["imprumuturi"][0]["status"], "RETURNAT")
        
        # verific ca cartea e disponibila
        carte = self.manager._gaseste_carte("Carte Test")
        self.assertEqual(carte["status"], "DISPONIBIL")
        
        # verific utilizatorul
        user = self.manager._gaseste_utilizator("1001")
        self.assertEqual(user["imprumuturi_active"], 0)
    
    def test_numarare_imprumuturi(self):
        """test ca se numara corect imprumuturile"""
        self.manager.adauga_carte("Carte Test", "Autor Test")
        self.manager.adauga_utilizator("Ion Popescu", "1001")
        
        # 2 imprumuturi
        self.manager.imprumuta_carte("Carte Test", "1001")
        self.manager.returneaza_carte("Carte Test", "1001")
        self.manager.imprumuta_carte("Carte Test", "1001")
        self.manager.returneaza_carte("Carte Test", "1001")
        
        carte = self.manager._gaseste_carte("Carte Test")
        self.assertEqual(carte["nr_imprumuturi"], 2)
        
        user = self.manager._gaseste_utilizator("1001")
        self.assertEqual(user["total_imprumuturi"], 2)


class TestPersistenta(unittest.TestCase):
    """test salvare date"""
    
    def setUp(self):
        self.fisier_temp = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.fisier_temp.close()
        self.manager = LibraryManager(self.fisier_temp.name)
    
    def tearDown(self):
        if os.path.exists(self.fisier_temp.name):
            os.unlink(self.fisier_temp.name)
    
    def test_date_persistente(self):
        """test ca datele se salveaza"""
        self.manager.adauga_carte("Carte Test", "Autor Test")
        self.manager.adauga_utilizator("Ion Popescu", "1001")
        
        # creez un nou manager cu acelasi fisier
        manager2 = LibraryManager(self.fisier_temp.name)
        
        self.assertEqual(len(manager2.date["carti"]), 1)
        self.assertEqual(len(manager2.date["utilizatori"]), 1)


class TestValidari(unittest.TestCase):
    """teste pentru validari"""
    
    def setUp(self):
        self.fisier_temp = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.fisier_temp.close()
        self.manager = LibraryManager(self.fisier_temp.name)
    
    def tearDown(self):
        if os.path.exists(self.fisier_temp.name):
            os.unlink(self.fisier_temp.name)
    
    def test_imprumut_carte_inexistenta(self):
        """test imprumut carte care nu exista"""
        self.manager.adauga_utilizator("Ion Popescu", "1001")
        
        nr_initial = len(self.manager.date["imprumuturi"])
        self.manager.imprumuta_carte("Nu Exista", "1001")
        
        # nu trebuie sa se creeze imprumut
        self.assertEqual(len(self.manager.date["imprumuturi"]), nr_initial)
    
    def test_imprumut_utilizator_inexistent(self):
        """test imprumut de utilizator inexistent"""
        self.manager.adauga_carte("Carte Test", "Autor Test")
        
        nr_initial = len(self.manager.date["imprumuturi"])
        self.manager.imprumuta_carte("Carte Test", "9999")
        
        # nu trebuie sa se creeze imprumut
        self.assertEqual(len(self.manager.date["imprumuturi"]), nr_initial)


# rulare teste
if __name__ == "__main__":
    unittest.main(verbosity=2)
