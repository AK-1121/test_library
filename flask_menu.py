import datetime
import time

from flask import Flask, render_template, request, redirect
from flask.ext.login import LoginManager
from library_lib import Library, Book, User, Librarian, current_date, current_dt

user_search_params = {"name": "ФИО", "passport_id": "номер паспорта", "user_id": "внутренний идентификатор",
                      "address": "адрес", "phone": "телефон"}
book_search_params = {"title": "название книги", "author": "автор книги", "year_of_publishing": "год издания",
                      "book_code": "код книги", "group_code": "код раздела"}

app = Flask(__name__)


@app.route('/hello')
def hello_world():
    return "Hello magic world!!!"


@app.route('/show_all_books')
def show_all_books():
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
            if int(book.date_of_return) < datetime.datetime.now().timestamp():
                book.expired_flag = True
                book.warning_color = 'red'
            # Переводим дату возврата из Unix timestamp:
            book.date_of_return_str = datetime.datetime.fromtimestamp(int(book.date_of_return)).strftime("%Y-%m-%d")
        else:
            book.date_of_return_str = '-'

    return render_template('show_all_books.html', lib_name=library.name_of_lib, books=books_list)


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    info_list = []
    if request.form:
        title = request.form['title']
        author = request.form['author']
        year_of_publishing = request.form['year_of_publishing']
        book_code = request.form['book_code']
        group_code = request.form['group_code']
        if title and author and year_of_publishing and book_code and group_code:
            book_id = library.add_book(title, author, book_code, group_code, year_of_publishing)
            info_list.append(str(current_dt()) + " - книга %s - %s (ID: %s) была добавлена" %(title, author, book_id))
            return render_template("add_user.html", info_list=info_list)
        else:
            info_list.append(current_dt() + " Книга не добавлена!!! Не все параметры заполнены!!!")
    else:
        info_list.append("Текущее время: %s" % current_dt())

    return render_template("add_book.html", info_list=info_list)


@app.route('/show_books', methods=['GET', 'POST'])
def show_books():
    if request.form:
        # Process searching of book request:
        search_by = request.form.get("search_by")
        if search_by:
            search_text = request.form.get("search_text")
            suitable_books = library.find_books(search_by, search_text)

            for book in suitable_books:
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
                    if int(book.date_of_return) < datetime.datetime.now().timestamp():
                        book.expired_flag = True
                        book.warning_color = 'red'
                    # Переводим дату возврата из Unix timestamp:
                    book.date_of_return_str = datetime.datetime.fromtimestamp(int(book.date_of_return)).strftime("%Y-%m-%d")
                else:
                    book.date_of_return_str = '-'

            return render_template("show_books.html", suitable_books=suitable_books, search_params=(
                book_search_params[search_by], search_text
            ))
    return render_template("show_books.html")


@app.route('/book/<int:book_id>')
def show_book(book_id):
    book = library.find_books("book_id", book_id)[0]
    book.date_of_return_str = book.date_of_return_str()
    return render_template("book_card.html", book=book)
# ! ---- End of book methods ----- !


# <---- Start of user methods: ---->
@app.route('/')
def list_menu():
    return redirect("/show_users")


@app.route('/show_users', methods=['GET', 'POST'])
def show_users():
    if request.form:
        # Process search users request:
        search_by = request.form.get("search_by")
        if search_by:
            search_text = request.form.get("search_text")
            suitable_users = library.find_users(search_by, search_text)
            return render_template("show_users.html", suitable_users=suitable_users, search_params=(
                                   user_search_params[search_by],  search_text))

    return render_template("show_users.html")


@app.route('/show_all_users')
def show_all_users():
    all_users = library.list_all_users()
    return render_template("show_users.html", suitable_users=all_users, search_params=("Все пользователи", '-'))


# Add new user:
@app.route('/add_user', methods=['GET', 'POST'])
def add_user():
    info_list = []
    if request.form:
        name = request.form['name']
        passport_id = request.form['passport_id']
        address = request.form['address']
        phone = request.form['phone']
        if name and passport_id and address and phone:
            user_id = library.add_user(name, passport_id, address, phone)
            info_list.append(current_dt() + " - пользователь %s (ID: %s) был добавлен" %(name, user_id))
            return render_template("add_user.html", info_list=info_list)
        else:
            info_list.append("Пользователь не добавлен!!! Не все параметры заполнены!!!")

    else:
        info_list.append("Текущее время: %s" % current_dt())

    return render_template("add_user.html", info_list=info_list)


@app.route('/user/<int:user_id>', methods=['GET', 'POST'])
def show_user(user_id):

    user = library.session.query(User).filter(User.user_id == user_id).first()
    if not user:  # Проверяем, найден ли пользователь с таким ID
        return 'Can`t find such user! :('
    else:
        suitable_books = []
        info_list = []  # Information messages.
        info_list.append("Дата возврата для сегодняшнего дня: %s" % datetime.datetime.fromtimestamp(time.time() +
                         14*24*60*60).strftime("%d-%m-%Y"))

        # Если пришли данные из формы страницы, то обрабатываем их:
        if request.form:
            # Возврат книг посетителя:
            print("R_F: " + str(request.form))
            return_books_id = request.form.getlist("return_book_id")
            if return_books_id:
                for book_id in return_books_id:
                    result = library.return_book(book_id, user_id)
                    print("Return result: %s" % result)

            # Поиск книг в библиотеке:
            search_by = request.form.get("search_by")
            if search_by:
                search_text = request.form.get("search_text")
                if search_text:
                    # print("Parameter: %s; Search text: %s" % (search_by, search_text))
                    suitable_books = library.find_books(search_by, search_text)
                    # print("Suitable_books: " + str(suitable_books))
                    for i in range(len(suitable_books)):
                        if suitable_books[i].date_of_return:
                            suitable_books[i].date_of_return_human_format = datetime.datetime.fromtimestamp(
                                suitable_books[i].date_of_return).strftime("%d-%m-%Y")
                        else:
                            suitable_books[i].date_of_return_human_format = "Свободна"

            # Выдача запрошенной книги:
            hand_out_book_id = request.form.get("hand_out_book_id")
            if hand_out_book_id:
                if "successfully" in library.hand_out_book(hand_out_book_id, user_id):
                    book = library.find_books('book_id', hand_out_book_id)[0]
                    info_list.append("Книга: {0} - {1} (Id: {2}) успешно выдана до {3}".format(book.title,
                                     book.author, book.book_id, book.date_of_return_str()))

        # Если у пользователя на руках есть книги (список list_of_book_id - не пуст) - запрашиваем их данные:
        borrowed_books = []
        if user.list_of_books_id:
            borrowed_books = library.session.query(Book).filter(Book.book_id.in_(user.list_of_books_id)).all()

        for i in range(len(borrowed_books)):
            if borrowed_books[i].date_of_return < time.time():
                borrowed_books[i].warning_color = "#FF0000"
            borrowed_books[i].date_of_return_human_format = datetime.datetime.fromtimestamp(
                borrowed_books[i].date_of_return).strftime("%d-%m-%Y")

        return render_template('user_card.html', user=user, books=borrowed_books, suitable_books=suitable_books,
                               info_list=info_list)


# < ---- Start of authorization session ----
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    info_list = []
    if len(request.form['password']) < 5:
        info_list.append(current_dt() + " - ошибка создания пользователя. Пароль слишком короткий (< 5 символов).")
        return render_template('register.html', info_list = info_list)
    # Проверям заполненность обязательных полей в форме:
    elif (request.form['user_name'] and request.form['real_name'] and
            request.form['password'] and request.form['status']):
        librarian = Librarian(request.form['user_name'], request.form['real_name'], request.form['password'],
                              request.form['status'], request.form['email'], request.form['personal_info'],
                              request.form['phone'], request.form['address'])
    else:
        # Составляем список не заполненных обязательных полей в форме:
        tmp_str = ("; ").join(filter(None, ["Логин"*(bool(request.form['user_name'])^1),
                                            "Пароль"*(bool(request.form['password'])^1),
                                            "ФИО"*(bool(request.form['real_name'])^1),
                                            "Статус"*(bool(request.form['status'])^1)]))

        info_list.append(current_dt() + (" - нельзя зарегистрировать пользователя. Необходимые обязательные поля "
                                        "не указаны: " + tmp_str + "."))
        return render_template('register.html', info_list = info_list)
    #print('RRR: ' + str(request.form))
    #print("1: %s, 2: %s, 3: %s, 4: %s, 5: %s, 6: %s, 7: %s, 8: %s" %(
    #      request.form['user_name'], request.form['real_name'], request.form['password'], request.form['status'],
    #      request.form['email'], request.form['personal_info'], request.form['phone'], request.form['address']))
    #librarian = Librarian('testtest', 'Алексей К.', '12341234', '1', "test@tester.ru")
    library.session.add(librarian)
    library.session.commit()
    info_list.append(current_dt() + " - пользователь {0} ({1}) успешно зарегистрирован".format(librarian.user_name,
                                                                                                   librarian.real_name))
    #except Exception as e:
    #    info_list.append(current_dt() + " - пользователя {0} ({1}) зарегистрировать не удалось".format(
    #            librarian.user_name, librarian.real_name) + ' Ошибка: %s (%s)' % (e.__class__, e.__context__))

    return render_template('register.html', info_list = info_list)


if __name__ == '__main__':
    library = Library('Детскя библиотека №28')
    login_manager = LoginManager()
    login_manager.init_app(app)
    app.debug = True
    app.run()

