import time

book_id = 0  # Unique book identifier in the library

class Book:
    '''Describes book-object'''
    
    def __init__(self, title, author, book_id, 
                 rang = None, year_of_publishing = None):
        '''Initialize a book with title, author`name, rang of book and
        year of publishing.'''
        self.id = book_id
        self.title = title
        self.author = author
        self.rang = rang
        self.year_of_publishing = year_of_publishing
        self.is_checked_out = False  # Checked out status.
        self.date_of_return = None  # Date of return in Linux format.
        
    def lend_out_book(self, number_of_days):
        '''Landing the book out. If it is possible (return True).
        Return False if it can`t be made.'''
        if not self.is_checked_out:
            self.date_of_return = int(time.time()) + 60*60*24*number_of_days
            self.is_checked_out = True
            return True
        else: return False
        
    def return_of_book(self):
        if self.is_checked_out:
            self.date_of_return = None
            self.is_checked_out = False
            return True
        else: return False
        
        
class Library:
    '''Describes library object.'''
    
    def __init__(self, name_of_lib = ''):
        #global book_id
        self.name_of_lib = name_of_lib
        self.readers = []  # List of readers.
        self.book_titles = []  # List of book names.
        self.index_of_books = {}  # Dictionary of indexes of books.
        
    def add_book(self, title, author, rang = None, year_of_publishing = None):
        '''Add new book to a library. Make unique identifier for it.'''
        global book_id
        book_id += 1
        book = Book(title, author, book_id, rang, year_of_publishing)
        self.book_titles.append([book.title, book_id])
        self.index_of_books.update({book_id: book})
        return book_id

    def remove_book(self, book_id):
        pass

    def find_book_by_title(self, search_flag, book_title):
        """ Find _one_ free book with suitable title
        :param search_flag: determine type of searching: (['0', '1', '2'])
        0 - search one suitable free book,
        1 - search all suitable free books, 2 - search all suitable books
        :type search_flag: str
        :param book_title: whole title or part of title which will be searched
        :type book_title: string
        :return: library id of suitable book or -1 in case of search failure
        :rtype: int
        """
        if search_flag == '0':
            for title in self.book_titles:
                if (book_title in title[0] and
                    getattr(self.index_of_books[int(title[1])], 'is_checked_out') == False):
                    return [title[1]]
            return []
        elif search_flag == '1':
            suitable_id_list = []
            for title in self.book_titles:
                if (book_title in title[0] and
                    getattr(self.index_of_books[int(title[1])], 'is_checked_out') == False):
                    suitable_id_list.append(title[1])
            return suitable_id_list
        else:
            suitable_id_list = []
            for title in self.book_titles:
                if book_title in title[0]:
                    suitable_id_list.append(title[1])
            return suitable_id_list


            
    def find_books(self, search_parameter, search_value):
        ''' Find books with determined attribute and its value.
        :param search_parameter: book attribute for searching
        :param search_value: book attribute`s value
        :return:
        '''
        # Check that search parameter exists:
        try:
            getattr(Book, search_parameter)
        except:
            return False
        
        suitable_books = []
        for book in self.index_of_books.keys():
            if (str(getattr(book, search_parameter)) == str(search_value) or
                str(search_value) in str(getattr(book, search_parameter))):
                suitable_books.append(book)
                
        return suitable_books
            
        

    
        
        