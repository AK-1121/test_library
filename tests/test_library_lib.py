import unittest
from sqlalchemy import create_engine, MetaData, Table, Column, String, INTEGER, ForeignKey
from sqlalchemy.orm import mapper, sessionmaker

from library_lib import Library



class LibLabriryTest(unittest.TestCase):
    def setUp(self):
        self.library = Library('Lib_Test', ':memory:')


    def test_add_user__list_all_users__remove_user(self):
        self.library.add_user("Alex Test", 'RG_123123', 'Moscow, Lenin Prospect 232 - flat 17', '+755555-4444')
        self.library.add_user('Mickle O`Conner II', '12FE2322F', 'UK, London Soho Green St. 12', '+3888-2423-2432')
        self.library.add_user('I. A. Ivanov-Petrov', 'WE1231234', 'Moscow Pererva St. 12 - flat 288', '+7(915)555-22-33')
        users = self.library.list_all_users()
        self.assertEqual(3, len(users))
        pasports_id = []
        list_of_id = []
        for user in users:
            pasports_id.append(user.passport_id)
            list_of_id.append(user.user_id)
        self.assertEqual(sorted(pasports_id), sorted(['RG_123123', '12FE2322F', 'WE1231234']))
        # Check removing by ID:
        id_for_removing = list_of_id.pop()
        self.library.remove_user(id_for_removing)
        users = self.library.list_all_users()
        list_of_id_after_removing_one_user = []
        for user in users:
            list_of_id_after_removing_one_user.append(user.user_id)
        self.assertEqual(sorted(list_of_id), sorted(list_of_id_after_removing_one_user))


    def test_add_user_and_test_list_all_books(self):
        self.library.add_book('Maugli', "R. Kipling", 'RT-12342342', 'KT-12', 1882)
        self.library.add_book('Tom Sawyer', "Mark Twain", 'RT-128822', 'KT-86', 1832)
        l = self.library.list_all_books()
        # Check authors:
        self.assertEqual(sorted(['Maugli', 'Tom Sawyer']), sorted([l[0].title, l[1].title]))
        # Check year of publishing:
        self.assertEqual(sorted([1882, 1832]), sorted([l[0].year_of_publishing, l[1].year_of_publishing]))
        # Check total number of books in the library:
        self.assertEqual(2, len(l))


    def tearDown(self):
        del self.library


