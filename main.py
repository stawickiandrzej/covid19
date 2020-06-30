from flask import Flask, render_template, request, flash, redirect, session, abort, url_for
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from flask import Response
import io
import os
import pandas as pd
from sqlalchemy.orm import sessionmaker
from tabledef import *
import requests


class SiteUtils():
  # Metoda pobierająca dane z API
  def request_active_covid_cases(self):
    # Pobierz liczbę zakażeń koronawirusem w Polsce
    zakazenia = requests.get("https://api.covid19api.com/country/poland")
    return zakazenia

  def prepare_data(self):
    zakazenia = self.request_active_covid_cases()
    df = pd.read_json(zakazenia.content)
    return df

  def create_figure(self):
    df = self.prepare_data()
    # Tworzymy wykres
    plot = df['Active'].plot(title="Aktywne przypadki koronawirusa")
    fig = plot.get_figure()
    plot.set_xlabel("Dni")
    plot.set_ylabel("Liczba przypadków")
    return fig


engine = create_engine('sqlite:///tutorial.db', echo=True)
app = Flask(
  __name__,
  template_folder='templates',
  static_folder='static',
  )

app.secret_key = os.urandom(12)

utils = SiteUtils()

@app.route('/')
def home():
  if not session.get('logged_in'):
    return render_template('login.html')
  else:
    return covid()

@app.route('/login', methods=['POST'])
def do_admin_login():
  error = None 
  POST_USERNAME = str(request.form['username'])
  POST_PASSWORD = str(request.form['password'])

  Session = sessionmaker(bind=engine)
  s = Session()
  query = s.query(User).filter(User.username.in_([POST_USERNAME]), User.password.in_([POST_PASSWORD]) )
  result = query.first()
  if result:
    session['logged_in'] = True
  else:  
    flash('No user or wrong password provided')
  return home()


@app.route("/logout")
def logout():
  session['logged_in'] = False
  return home()


@app.route('/covid19')
def covid():
  return render_template('index.html')


@app.route('/plot.png')
def plot_png():
    fig=utils.create_figure()
    output=io.BytesIO()
    FigureCanvas(fig).print_png(output)
    return Response(output.getvalue(), mimetype='image/png')


if __name__ == '__main__':
  app.run(
    debug=True)





