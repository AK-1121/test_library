import time
from sqlalchemy import MetaData, Table, Column, INTEGER, String, create_engine
from sqlalchemy.orm import mapper, sessionmaker
#from sqlalchemy.ext.declarative import declarative_base

book_id = 0  # Unique book identifier in the library

class Book:
    '''Describes book-object'''

    def __init__(self, book_id, title, author,
                 book_code = None, group_code = None, year_of_publishing = None):
        '''Initialize a book with title, author`name, rang of book and
        year of publishing.'''
        self.id = book_id  # Unique book ID.
        self.title = title  # Title of the book.
        self.author = author  # Book author.
        self.book_code = book_code  # Book code.
        self.group_code = group_code  # Group of books code.
        self.year_of_publishing = year_of_publishing
        self.is_checked_out = False  # Checked out status.
        self.date_of_return = None  # Date of return in Linux format.
        self.user_id = None  # User ID who took the book.
        self.info1 = ''  # Reserved parameter 1.
        self.info2 = ''  #Reserved parameter 2.

    def __repr__(self):
        """ __repr__ should return a printable representation of the object
        :rtype: str
        """
        return ('<Book: "{0}" {1} \n Book ID: {6} Book code: {2} \n'
                'Book group: {3} Is checked out: {4}. Date of return: {5}>'
                ).format(self.title, self.author, self.book_code,
                         self.group_code, self.is_checked_out,
                         self.date_of_return, self.id)

        
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
        #  DB section:
        self.db = create_engine('sqlite:///library.db', echo=True)  # Access the DB Engine
        #  echo=False – if True, the Engine will log all statements as well as\n"
        #  a repr() of their parameter lists to the engines logger, which \n"
        #  defaults to sys.stdout\n"
        metadata = MetaData()
        self.books = Table('books', metadata,
                           Column('book_id', INTEGER, primary_key=True),
                           Column('title', String(200), nullable=False),
                           Column('author', String(200), nullable=False),
                           Column('book_code', String(20)),
                           Column('group_code', String(20)),
                           Column('year_of_publishing', INTEGER),
                           Column('is_checked_out', INTEGER),  # True if book is checked out.
                           Column('date_of_return', INTEGER),  # Store as Unix Time
                           Column('user_id', INTEGER),  # User ID who took the book
                           Column('info1', String(200)),  # Reserved field 1.
                           Column('info2', String(200)),  # Reserved filed 2.
                           )
        metadata.create_all(self.db)
        self.Session = sessionmaker(bind=self.db)
        self.session = self.Session()
        mapper(Book, self.books)

        
    def add_book(self, title, author, book_code = None, group_code = None,
                 year_of_publishing = None):
        '''Add new book to a library. Make unique identifier for it.'''
        global book_id
        book_id += 1
        user_id, info1, info2 = None, '', ''
        book = Book(book_id, title, author, book_code, group_code, year_of_publishing)
        self.book_titles.append([book.title, book_id])  # add title to list for searching by titles
        self.index_of_books.update({book_id: book})  # add book to dict of book objects
        #self.session.add(book)
        self.session.add(book)
        self.session.commit()
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
        try:
            suitable_books = self.session.query(Book).filter(getattr(Book, search_parameter) == search_value).all()
        except:
            return 'Err'

        print('XXX_Suitable_books: ' + str(type(suitable_books)) + ' -- ' + str(len(suitable_books)))
        print('Columns: ' + str([c.name for c in self.books.columns]))
        #print('dir(self.books): ' + str(dir(self.books)))
        for book in suitable_books:
            for col in self.books.columns:
                print(getattr(book, col.name), end=' - ')
            print('')

        #return suitable_books
            
        

    
        
        