import time
from sqlalchemy import ForeignKey, MetaData, Table, Column, INTEGER, String, create_engine, exists, and_
from sqlalchemy.orm import mapper, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
#from sqlalchemy.ext.declarative import declarative_base

book_id = 0  # Unique book identifier in the library
Base = declarative_base()  # Parent class for Book and User

class Book(Base):
    '''Describes book-object'''
    __table__ = Table('books', Base.metadata,
                           Column('book_id', INTEGER, primary_key=True),
                           Column('title', String(200), nullable=False),
                           Column('author', String(200), nullable=False),
                           Column('book_code', String(20)),
                           Column('group_code', String(20)),
                           Column('year_of_publishing', INTEGER),
                           Column('is_checked_out', INTEGER),  # True if book is checked out.
                           Column('date_of_return', INTEGER),  # Store as Unix Time
                           #Column('user_id', INTEGER, ForeignKey('users.user_id')),  # User ID who took the book
                           Column('user_id', INTEGER),  # User ID who took the book
                           Column('info1', String(200)),  # Reserved field 1.
                           Column('info2', String(200)),  # Reserved filed 2.
                           )

    def __init__(self, book_id, title, author,
                 book_code = None, group_code = None, year_of_publishing = None):
        '''Initialize a book with title, author`name, rang of book and
        year of publishing.'''
        self.book_id = book_id  # Unique book ID.
        self.title = title  # Title of the book.
        self.author = author  # Book author.
        self.book_code = book_code  # Book code.
        self.group_code = group_code  # Group of books code.
        self.year_of_publishing = year_of_publishing
        self.is_checked_out = False  # Checked out status.
        self.date_of_return = None  # Date of return in Linux format.
        self.user_id = None  # User ID who took the book.
        self.info1 = ''  # Reserved parameter 1.
        self.info2 = ''  # Reserved parameter 2.

    def __repr__(self):
        """ __repr__ should return a printable representation of the object
        :rtype: str
        """
        return ('<Book: "{0}" {1} \n Book ID: {6} Book code: {2} \n'
                'Book group: {3} Is checked out: {4}. Date of return: {5}>'
                ).format(self.title, self.author, self.book_code,
                         self.group_code, self.is_checked_out,
                         self.date_of_return, self.book_id)

        
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
        

user_id = 0  # Unique user identifier in the library.

class User(Base):
    __table__ = Table('users', Base.metadata,
                           Column('user_id', INTEGER, primary_key=True),
                           Column('name', String(100), nullable=False),
                           Column('passport_id', String(50), nullable=False),
                           Column('address', String(250), nullable=False),
                           Column('phone', String(25)),
                           Column('list_of_books_id', String(250)),
                           Column('info11', String(200)),  # Reserved field 1.
                           Column('info12', String(200)),  # Reserved filed 2.
                           )
    """
    Class describes library user (visitor).
    """
    def __init__(self, user_id, name, passport_id, address, phone=None):
        self.user_id = user_id
        self.name = name
        self.passport_id = passport_id
        self.address = address
        self.phone = phone
        self.list_of_books_id = '-'

    def change_user_data(self, parameter, parameter_value):
        pass


class Library:
    '''Describes library object.'''
    
    def __init__(self, name_of_lib = '', lib_path = 'library.db'):
        #global book_id
        self.name_of_lib = name_of_lib
        self.readers = []  # List of readers.
        self.book_titles = []  # List of book names.
        self.index_of_books = {}  # Dictionary of indexes of books.
        #  DB section:
        #self.db = create_engine('sqlite:///library.db', echo=True)  # Access the DB Engine
        #self.db = create_engine('sqlite:///library.db', echo=False)  # Access the DB Engine
        self.db = create_engine('sqlite:///{0}'.format(lib_path), echo=False)  # Access the DB Engine
        #  echo=False – if True, the Engine will log all statements as well as\n"
        #  a repr() of their parameter lists to the engines logger, which \n"
        #  defaults to sys.stdout\n"
        #metadata1 = MetaData()
        #metadata = MetaData()
        """
        self.users = Table('users', metadata1,
                           Column('user_id', INTEGER, primary_key=True),
                           Column('name', String(100), nullable=False),
                           Column('passport_id', String(50), nullable=False),
                           Column('address', String(250), nullable=False),
                           Column('phone', String(25)),
                           Column('list_of_books_id', String(250)),
                           Column('info11', String(200)),  # Reserved field 1.
                           Column('info12', String(200)),  # Reserved filed 2.
                           )



        self.books = Table('books', metadata,
                           Column('book_id', INTEGER, primary_key=True),
                           Column('title', String(200), nullable=False),
                           Column('author', String(200), nullable=False),
                           Column('book_code', String(20)),
                           Column('group_code', String(20)),
                           Column('year_of_publishing', INTEGER),
                           Column('is_checked_out', INTEGER),  # True if book is checked out.
                           Column('date_of_return', INTEGER),  # Store as Unix Time
                           #Column('user_id', INTEGER, ForeignKey('users.user_id')),  # User ID who took the book
                           Column('user_id', INTEGER),  # User ID who took the book
                           Column('info1', String(200)),  # Reserved field 1.
                           Column('info2', String(200)),  # Reserved filed 2.
                           )
        """
        #metadata.create_all(self.db)
        Base.metadata.create_all(self.db)
        #metadata1.create_all(self.db)
        self.Session = sessionmaker(bind=self.db)
        self.session = self.Session()
        #mapper(User, self.users)
        #mapper(Book, self.books, non_primary=True)
        #mapper(Book, self.books)

        
    def add_book(self, title, author, book_code = None, group_code = None,
                 year_of_publishing = None):
        '''Add new book to a library. Make unique identifier for it.'''
        # Find index (book_id) of last book in books table:
        try:
            book_id = self.session.query(Book).order_by(Book.book_id.desc()).first().book_id
        except:  # in case of there are no books in DB:
            book_id = 0
        book = Book(book_id + 1, title, author, book_code, group_code, year_of_publishing)
        self.session.add(book)
        self.session.commit()
        return book_id

    def add_user(self, name, passport_id, address, phone=None):
        """ Add new user to a library """
        # Find index user_id of last user in table users:
        try:
            user_id = self.session.query(User).order_by(User.user_id.desc()).first().user_id
        except:  # in case of no users in db:
            user_id = 0
        user = User(user_id + 1, name, passport_id, address, phone)
        self.session.add(user)
        self.session.commit()
        return user_id

    def list_all_users(self):
        return self.session.query(User).all()

    def remove_user(self, user_id):
        """
        :param user_id: Remove user from db by user_id
        :type user_id: int or str
        :return: True or False
        :rtype: bool
        """
        result_of_removing = self.session.query(User).filter_by(user_id = int(user_id)).delete()
        self.session.commit()
        if result_of_removing:
            return True
        else:
            return False


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

    def list_all_books(self):
        """
        :return: list of all books in the library
        :rtype: list
        """
        return self.session.query(Book).all()
            
    def find_books(self, search_parameter, search_value):
        ''' Find books with determined attribute and its value.
        :param search_parameter: book attribute for searching
        :param search_value: book attribute`s value
        :return: 1) in case of correct search parameters return tuple:
            (a, b) where a - list of suitable book objects,
            b - list of book attributes
            2) in case of incorrect search parameters return tuple: ('Err', 'Err')
        '''
        try:
            suitable_books = self.session.query(Book).filter(getattr(Book, search_parameter) == search_value).all()
            return (suitable_books, [col.name for col in self.books.columns])
        except:
            return ('Err', 'Err')

    def hand_out_book(self, book_id, user_id):
        """ Give a book to a user
        :param book_id:
        :return:
        """
        #try:
        # Check that user with given ID exists (check_user = 1 if user exists):
        #check_user = self.session.query(exists().where(User.user_id == int(user_id))).scalar()
        #current_user = self.session.query(exists().where(User.user_id == int(user_id))).first()
        current_user = self.session.query(User).filter(User.user_id == int(user_id)).first()
        #print('CU: ' + str(type(current_user)) + ' - ' + str(current_user) + ' -- ' + str(current_user.passport_id))
        # Check that book with such ID is free (check_book = 1 if book exists and free):
        #check_book = self.session.query(Book).filter(and_(Book.book_id == int(book_id),
        #                                                Book.is_checked_out == 0)).count()
        current_book = self.session.query(Book).filter(and_(Book.book_id == int(book_id),
                                                        Book.is_checked_out == 0)).first()
        #print('CB: ' + str(type(current_book)) + str(current_book))
        if current_user and current_book:
            now_time = int(time.time())
            return_date = (now_time // 86400) * 86400 + 1209600  # Get date of return in Linux format.
            result = self.session.query(Book).filter_by(book_id = int(book_id)).update({'is_checked_out':1,
                                                                                        'user_id': user_id,
                                                                                        'date_of_return': return_date})
            self.session.query(User).filter_by(user_id = int(user_id)).update({
                'list_of_books_id': current_user.list_of_books_id + book_id + '-'})
            self.session.commit()
            return 'Book was successfully lent out.'
        elif not current_book:
            return 'Can`t find such free book.'
        else:
            return 'Can`t find such active user.'
        #except Exception as e:
        #    print('Error during renting a book: ' + str(Exception) + ' - ' + str(e))

    def return_book(self, book_id, user_id):
        """
        Run this function when library visitor return a book
        :param book_id: Book ID
        :param user_id: User ID
        :return: 0 - Book was successfully returned.
                 1 - Can`t find user with such ID.
                 2 - User with such ID didn't lend a book with given ID.
        """
        current_user = self.session.query(User).filter(User.user_id == int(user_id)).first()
        if not current_user:
            return 1
        elif book_id not in current_user.list_of_books_id:
            return 2
        else:
            self.session.query(Book).filter_by(book_id = int(book_id)).update({
                'is_checked_out':0, 'user_id':None, 'date_of_return': None})
            self.session.query(User).filter_by(user_id = int(user_id)).update({
                'list_of_books_id': current_user.list_of_books_id.replace(book_id, '').replace('--', '-')})
            self.session.commit()
            return 0
        

    
        
        