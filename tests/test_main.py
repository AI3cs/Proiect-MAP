#!/usr/bin/env python3
"""
Teste pentru Library Manager
"""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from main import LibraryManager


class TestBooks(unittest.TestCase):
    
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.temp_file.close()
        self.manager = LibraryManager(self.temp_file.name)
    
    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            try:
                os.unlink(self.temp_file.name)
            except PermissionError:
                pass
    
    def test_add_book_simple(self):
        self.manager.add_book("Carte Test", "Autor Test")
        self.assertEqual(len(self.manager.data["books"]), 1)
        self.assertEqual(self.manager.data["books"][0]["title"], "Carte Test")
        self.assertEqual(self.manager.data["books"][0]["author"], "Autor Test")
        self.assertEqual(self.manager.data["books"][0]["status"], "DISPONIBIL")
    
    def test_add_book_complete(self):
        self.manager.add_book("1984", "George Orwell", "9780451524935", "Fiction", 1949)
        book = self.manager.data["books"][0]
        self.assertEqual(book["isbn"], "9780451524935")
        self.assertEqual(book["category"], "Fiction")
        self.assertEqual(book["year"], 1949)
    
    def test_duplicate_isbn(self):
        self.manager.add_book("Carte 1", "Autor 1", "123456")
        self.manager.add_book("Carte 2", "Autor 2", "123456")
        self.assertEqual(len(self.manager.data["books"]), 1)
    
    def test_unique_ids(self):
        self.manager.add_book("Carte 1", "Autor 1")
        self.manager.add_book("Carte 2", "Autor 2")
        self.assertEqual(self.manager.data["books"][0]["id"], 1)
        self.assertEqual(self.manager.data["books"][1]["id"], 2)
    
    def test_find_book_by_title(self):
        self.manager.add_book("Carte Test", "Autor Test")
        book = self.manager._find_book("Carte Test")
        self.assertIsNotNone(book)
        self.assertEqual(book["title"], "Carte Test")
    
    def test_find_book_by_isbn(self):
        self.manager.add_book("Carte Test", "Autor Test", "123456")
        book = self.manager._find_book("123456")
        self.assertIsNotNone(book)
    
    def test_book_not_found(self):
        book = self.manager._find_book("Nu exista")
        self.assertIsNone(book)


class TestUsers(unittest.TestCase):
    
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.temp_file.close()
        self.manager = LibraryManager(self.temp_file.name)
    
    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            try:
                os.unlink(self.temp_file.name)
            except PermissionError:
                pass
    
    def test_add_user(self):
        self.manager.add_user("Ion Popescu", "1001")
        self.assertEqual(len(self.manager.data["users"]), 1)
        self.assertEqual(self.manager.data["users"][0]["name"], "Ion Popescu")
        self.assertEqual(self.manager.data["users"][0]["id"], "1001")
    
    def test_add_user_with_email(self):
        self.manager.add_user("Ion Popescu", "1001", "ion@test.com")
        self.assertEqual(self.manager.data["users"][0]["email"], "ion@test.com")
    
    def test_duplicate_id(self):
        self.manager.add_user("User 1", "1001")
        self.manager.add_user("User 2", "1001")
        self.assertEqual(len(self.manager.data["users"]), 1)
    
    def test_find_user(self):
        self.manager.add_user("Ion Popescu", "1001")
        user = self.manager._find_user("1001")
        self.assertIsNotNone(user)
        self.assertEqual(user["name"], "Ion Popescu")


class TestLoans(unittest.TestCase):
    
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.temp_file.close()
        self.manager = LibraryManager(self.temp_file.name)
    
    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            try:
                os.unlink(self.temp_file.name)
            except PermissionError:
                pass
    
    def test_borrow_success(self):
        self.manager.add_book("Carte Test", "Autor Test")
        self.manager.add_user("Ion Popescu", "1001")
        self.manager.borrow_book("Carte Test", "1001", 14)
        self.assertEqual(len(self.manager.data["loans"]), 1)
        self.assertEqual(self.manager.data["loans"][0]["status"], "ACTIV")
        book = self.manager._find_book("Carte Test")
        self.assertEqual(book["status"], "IMPRUMUTAT")
        user = self.manager._find_user("1001")
        self.assertEqual(user["active_loans"], 1)
    
    def test_book_unavailable(self):
        self.manager.add_book("Carte Test", "Autor Test")
        self.manager.add_user("User 1", "1001")
        self.manager.add_user("User 2", "1002")
        self.manager.borrow_book("Carte Test", "1001")
        self.manager.borrow_book("Carte Test", "1002")
        self.assertEqual(len(self.manager.data["loans"]), 1)
    
    def test_return_success(self):
        self.manager.add_book("Carte Test", "Autor Test")
        self.manager.add_user("Ion Popescu", "1001")
        self.manager.borrow_book("Carte Test", "1001")
        self.manager.return_book("Carte Test", "1001")
        self.assertEqual(self.manager.data["loans"][0]["status"], "RETURNAT")
        book = self.manager._find_book("Carte Test")
        self.assertEqual(book["status"], "DISPONIBIL")
        user = self.manager._find_user("1001")
        self.assertEqual(user["active_loans"], 0)
    
    def test_loan_count(self):
        self.manager.add_book("Carte Test", "Autor Test")
        self.manager.add_user("Ion Popescu", "1001")
        self.manager.borrow_book("Carte Test", "1001")
        self.manager.return_book("Carte Test", "1001")
        self.manager.borrow_book("Carte Test", "1001")
        self.manager.return_book("Carte Test", "1001")
        book = self.manager._find_book("Carte Test")
        self.assertEqual(book["loan_count"], 2)
        user = self.manager._find_user("1001")
        self.assertEqual(user["total_loans"], 2)


class TestPersistence(unittest.TestCase):
    
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.temp_file.close()
        self.manager = LibraryManager(self.temp_file.name)
    
    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            try:
                os.unlink(self.temp_file.name)
            except PermissionError:
                pass
    
    def test_persistent_data(self):
        self.manager.add_book("Carte Test", "Autor Test")
        self.manager.add_user("Ion Popescu", "1001")
        manager2 = LibraryManager(self.temp_file.name)
        self.assertEqual(len(manager2.data["books"]), 1)
        self.assertEqual(len(manager2.data["users"]), 1)


class TestValidations(unittest.TestCase):
    
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.temp_file.close()
        self.manager = LibraryManager(self.temp_file.name)
    
    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)
    
    def test_borrow_nonexistent_book(self):
        self.manager.add_user("Ion Popescu", "1001")
        initial_count = len(self.manager.data["loans"])
        self.manager.borrow_book("Nu Exista", "1001")
        self.assertEqual(len(self.manager.data["loans"]), initial_count)
    
    def test_borrow_nonexistent_user(self):
        self.manager.add_book("Carte Test", "Autor Test")
        initial_count = len(self.manager.data["loans"])
        self.manager.borrow_book("Carte Test", "9999")
        self.assertEqual(len(self.manager.data["loans"]), initial_count)


class TestOperations(unittest.TestCase):

    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False)
        self.temp_file.close()
        self.manager = LibraryManager(self.temp_file.name)
    
    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.unlink(self.temp_file.name)

    def test_delete_book_by_title(self):
        self.manager.add_book("De Sters", "Autor X")
        self.assertEqual(len(self.manager.data["books"]), 1)
        self.manager.delete_book("De Sters")
        self.assertEqual(len(self.manager.data["books"]), 0)

    def test_delete_book_by_isbn(self):
        self.manager.add_book("Dublura", "Autor Y", isbn="111")
        self.manager.add_book("Dublura", "Autor Y", isbn="222")
        self.assertEqual(len(self.manager.data["books"]), 2)
        
        # Stergem doar a doua carte folosind ISBN-ul
        self.manager.delete_book("222")
        self.assertEqual(len(self.manager.data["books"]), 1)
        self.assertEqual(self.manager.data["books"][0]["isbn"], "111")

    def test_delete_active_user(self):
        self.manager.add_user("User Act", "5000")
        self.manager.deactivate_user("5000")
        user = self.manager._find_user("5000")
        self.assertEqual(user["status"], "INACTIV")

    def test_reactivate_user(self):
        self.manager.add_user("User React", "6000")
        self.manager.deactivate_user("6000")
        self.manager.reactivate_user("6000")
        user = self.manager._find_user("6000")
        self.assertEqual(user["status"], "ACTIV")


if __name__ == "__main__":
    unittest.main(verbosity=2)
