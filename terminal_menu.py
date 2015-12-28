# For Python 3:

import sys
from library_lib import Library

class Menu:

    def __init__(self):
        self.library = Library('Lib01')
        self.choice = { '1': self.show_all_books,
                        '2': self.add_book,
                        '3': self.search_by_attribute,
                        '4': self.hand_out_book,
                        '5': self.return_book,
                        '6': self.add_user,
                        '7': self.remove_user,
                        'q': self.quit,
                      }
                      
    def display_menu(self):
        print('\n1 - Show books.\n2 - Add book.\n' +
              '3 - Search book by attribute \n4 - Hand out a book\n'
              '5 - Return a book \n6 - Add user\n'
              '7 - Delete user \nq - Quit')
                      
    def run(self):
        while True:
            self.display_menu()
            choice = str(input('What is your choice? '))
            if choice in self.choice.keys():
                action = self.choice.get(choice)
                action()
            else:
                print('Can`t find such choice.')
                
    def print_list_of_books(self, list_of_books):
        if not list_of_books:
            print('- list is empty')
        else:
            print('Result(s):')
        for book in list_of_books:
            print (('Book Title: {0}\n Book author: {1}\n' + 
                   'Book Id: {2}\n Publishing year: {3}\n').format(book.title, 
                    book.author, book.book_id, book.year_of_publishing) +
                    '-'*20)
    
    def show_all_books(self):
        print('\nList of all books in the library:')
        self.print_list_of_books(self.library.list_all_books())
                    
    def add_book(self):
        title = input('Title: ')
        author = input('Author: ')
        book_code = input('Book code: ')
        group_code = input('Group code: ')
        year = input('Year of publishing: ')
        self.library.add_book(title, author, book_code, group_code, year)
        
    def search_by_attribute(self):
        print ('Available attributes to search: ' +
               'title, author, rang, year')
        attribute = input('Attribute name: ')
        attr_value = input('Attribute value: ')
        suitable_books, list_of_attributes = self.library.find_books(attribute, attr_value)
        if suitable_books == 'Err':
            print('Search parameter is incorrect!')
        else:
            print('')
            self.print_list_of_books(suitable_books)

    def add_user(self):
        name = input('Name: ')
        passport_id = input('Passport ID: ')
        address = input('Address: ')
        phone = input('Phone number: ')
        self.library.add_user(name, passport_id, address, phone)

    def remove_user(self):
        user_id = input('User id: ')
        try:
            remove_result = self.library.remove_user(user_id)
            if remove_result:
                print('User with ID ' + user_id + ' was successfully removed')
            else:
                print('Can`t remove such ID.')
        except Exception as e:
            print('Error was detected: ' + str(Exception) + ' info: ' + str(e))

    def hand_out_book(self):
        book_id = input('Book ID (for rent a book): ')
        user_id = input('User ID (renting a book):   ')
        print(self.library.hand_out_book(book_id, user_id))

    def return_book(self):
        book_id = input('Book ID (returned book): ')
        user_id = input('User ID (user who returns book): ')
        result = self.library.return_book(book_id, user_id)
        if result == 0:
             print('Book with ID: {0} was successfully returned by user with ID: {1}) . '.format(book_id, user_id))
        elif result == 1:
            print('Can`t find user with ID {0}'.format(user_id))
        elif result == 2:
            print('User with ID {0} did not lend out the book with ID {1}'.format(user_id, book_id))
        else:
            print ('Error: unknown return of function')



    def quit(self):
        print('Library closed.')
        sys.exit(0)
        


if __name__ == '__main__':
    Menu().run()
    
    
        
              