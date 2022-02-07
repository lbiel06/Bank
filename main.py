from flask import Flask, request, redirect, render_template, session, flash
import bcrypt
import database


app = Flask(__name__)
app.secret_key = '123'


@app.get('/')
def home_page():
    if 'username' not in session:
        return redirect('/login')
    _, _, balance = database.User.find(session['username'])
    return render_template('home.html', balance=balance)


@app.get('/login')
def login_page():
    return render_template('login.html')


@app.post('/login')
def login():
    username = request.form.get('username', '')
    password = request.form.get('password', '')

    if database.User.find(username):
        correct_password = database.User.find(username)[1]

        if bcrypt.checkpw(password.encode(), correct_password.encode()):
            session['username'] = username
            return redirect('/')

    flash('Invalid credentials')

    return redirect('/login')


@app.get('/register')
def register_page():
    return render_template('register.html')


@app.post('/register')
def register():
    username = request.form.get('username', '')
    password = request.form.get('password', '')

    if not (username and password):
        flash('Empty fields')

    if database.User.find(username):
        flash('Username is taken')

    else:
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        database.User.register(username, hashed_password.decode())

        return redirect('/login')

    return redirect('/register')


@app.route('/send', methods=('GET', 'POST'))
def send():
    if request.method == 'GET':
        return redirect('/')

    receiver = request.form.get('to', '')
    ammount = request.form.get('ammount', '')

    # print(receiver, ammount)

    if not (receiver and ammount):
        flash('Empty fields')

    try:
        ammount = int(ammount)
    except:
        return redirect('/')

    if not database.User.find(receiver):
        flash('Receiver does not exist')

    sender_balance = database.User.find(session['username'])[2]

    if ammount > sender_balance:
        flash('Not enough funds')

    else:
        receiver_balance = database.User.find(receiver)[2]
        database.User.set_balance(session['username'], sender_balance - ammount)
        database.User.set_balance(receiver, receiver_balance + ammount)

        flash('The transaction was completed')

    return redirect('/')


@app.get('/logout')
def logout():
    session.pop('username')
    return redirect('/login')


if __name__ == '__main__':
    app.run(debug=True)
