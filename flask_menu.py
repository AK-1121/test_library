import datetime
import time

from flask import Flask, render_template, request
from library_lib import Library, Book, User


app = Flask(__name__)

@app.route('/hello')
def hello_world():
    return "Hello magic world!!!"

@app.route('/')
def list_menu():
    pass

@app.route('/show_books')
def show_books():
    books_list = library.list_all_books()
    for book in books_list:
        # Устанавливаем значение "Выдана" или "Не выдана":
        if book.is_checked_out == 1:
            book.status = "Выдана"
        elif book.is_checked_out == 0:
            book.status = "Не выдана"
        else:
            book.status = book.is_checked_out

        book.expired_flag = False
        book.warning_color = 'white'
        if book.date_of_return:
            # Проверяем, не просрочена ли книга:
            print("XS: " + str(book.date_of_return))
            if int(book.date_of_return) < datetime.datetime.now().timestamp():
                book.expired_flag = True
                book.warning_color = 'red'
            # Переводим дату возврата из Unix timestamp:
            book.date_of_return_str = datetime.datetime.fromtimestamp(int(book.date_of_return)).strftime("%Y-%m-%d")
        else:
            book.date_of_return_str = '-'

    return render_template('show_books.html', lib_name=library.name_of_lib, books=books_list)

@app.route('/add_book')
def add_book():
    pass

@app.route('/search_book')
def search_book():
    pass

@app.route('/show_users')
def show_users():
    pass

@app.route('/add_user')
def add_user():
    pass

@app.route('/user/<int:user_id>', methods=['GET', 'POST'])
def show_user(user_id):
    # Если пришли данные из формы страницы, то обрабатываем их:
    if request.form:
        return_books_id = request.form.getlist("return_book_id")
        # Возврат книг посетителя:
        if return_books_id:
            for book_id in return_books_id:
                result = library.return_book(book_id, user_id)
                print("Return result: %s" % result)


    user = library.session.query(User).filter(User.user_id == user_id).first()
    print('UU: ' + str((user)))
    if not user:  # Проверяем, найден ли пользователь с таким ID
        return 'Can`t find such user! :('
    else:
        # Если у пользователя на руках есть книги (список list_of_book_id - не пуст) - запрашиваем их данные:
        borrowed_books = []
        if user.list_of_books_id:
            borrowed_books = library.session.query(Book).filter(Book.book_id.in_(user.list_of_books_id)).all()

        for i in range(len(borrowed_books)):
            if borrowed_books[i].date_of_return < time.time():
                borrowed_books[i].warning_color = "#FF0000"
            borrowed_books[i].date_of_return_human_format = datetime.datetime.fromtimestamp(
                borrowed_books[i].date_of_return).strftime("%d-%m-%Y")

        return render_template('user_card.html', user=user, books=borrowed_books)

if __name__ == '__main__':
    library = Library('Детскя библиотека №28')
    app.debug = True
    app.run()
