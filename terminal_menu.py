# For Python 3:

import sys
from library_lib import Library

class Menu:

    def __init__(self):
        self.library = Library('Lib01')
        self.choice = { '1': self.show_books,
                        '2': self.add_book,
                        '3': self.search_by_attribute,
                        '4': self.search_by_title,
                        'q': self.quit,
                      }
                      
    def display_menu(self):
        print('\n1 - Show books.\n2 - Add book.\n' +
              '3 - Search book by attribute \n4 - Search book by title\n' +
              'q - Quit')    
                      
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
        for book in list_of_books:
            print (('Book Title: {0}\n Book author: {1}\n' + 
                   'Book Id: {2}\n Publishing year: {3}\n').format(book.title, 
                    book.author, book.id, book.year_of_publishing) +
                    '-'*20)
    
    def show_books(self):
        print('\nList of all books in the library:')
        self.print_list_of_books(self.library.index_of_books.values())
                    
    def add_book(self):
        title = input('Title: ')
        author = input('Author: ')
        book_code = input('Book code: ')
        group_code = input('Group code: ')
        year = input('Year of publishing: ')
        self.library.add_book(title, author, book_code, group_code, year)
        
    def search_by_attribute(self):
        print ('Avalibale attributes to search: ' +
               'title, author, rang, year')
        attribute = input('Attribute name: ')
        attr_value = input('Attribute value: ')
        print('Suitable books:')
        self.print_list_of_books(self.library.find_books(attribute, attr_value))
        
    def search_by_title(self):
        flag = '-1'
        while flag not in ['0', '1', '2']:
            if flag !='-1': print('I don`t understand your choice.')
            print('0 - if want to find only one free book\n'
                  '1 - if you want to find all suitable free books\n'
                  '2 - if you want to find all suitable books')
            flag = input('Your choose: ')
        title_for_search = input('Title or part of it: ')
        print('Suitable books: ')
        self.print_list_of_books(
            [self.library.index_of_books[book_id]
             for book_id in self.library.find_book_by_title(flag, title_for_search)
             ]
        )

        
    def quit(self):
        print('Library closed.')
        sys.exit(0)
        


if __name__ == '__main__':
    Menu().run()
    
    
        
              