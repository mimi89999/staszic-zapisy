import functools
import datetime as dt
import configparser
from flask import (
    Blueprint, render_template)
from main.db import get_db


bp = Blueprint('zapisy', __name__)


# Index, w którym da się zobaczyć podsumowanie nauczycieli
@bp.route('/')
def index():
    db = get_db()

    # Komunikacja z bazą
    nauczyciele = db.execute(
        'SELECT id, imie, nazwisko, obecny FROM nauczyciele'
    ).fetchall()
    
    # View
    return render_template('zapisy/index.html', nauczyciele=nauczyciele)
    
# View wyboru godziny do zapisu (tu trzeba będzie dopisać jakieś POSTy)
@bp.route('/nauczyciel/<int:id>')
def nauczyciel(id):
    db = get_db()

    # Komunikacja z bazą
    zajete = db.execute(
        'SELECT godzina FROM wizyty WHERE id_nauczyciela = ?', (id,)
    )
    zajete = [dt.datetime.strptime(
        conf['dzien otwarty']['data'] + ' ' + t, '%d/%m/%Y %H:%M')
        for t in zajete]
    imie_nazwisko_nauczyciela = db.execute(
        'SELECT imie, nazwisko FROM nauczyciele WHERE id = ?', (id,)
    ).fetchone()
    # print (imie_nazwisko_nauczyciela['imie'], imie_nazwisko_nauczyciela['nazwisko'])
    
    # Ustawienie wszystkich dat
    conf = configparser.ConfigParser()
    conf.read('./config.ini')
    start = dt.datetime.strptime(
        conf['dzien otwarty']['data'] + ' ' + conf['dzien otwarty']['start'],
        '%d/%m/%Y %H:%M'
    )
    koniec = dt.datetime.strptime(
        conf['dzien otwarty']['data'] + ' ' + conf['dzien otwarty']['koniec'],
        '%d/%m/%Y %H:%M'
    )
    blok = conf['dzien otwarty']['blok']
    blok = [int(s) for s in blok.split(':')]
    blok = dt.timedelta(hours=blok[0], minutes=blok[1])

    # Liczenie wolnych godzin
    rozklad = []
    t = start
    while t < koniec:
        if t in zajete:
            rozklad.append({'start':t, 'koniec':t + blok, 'wolne':False})
        else:
            rozklad.append({'start':t, 'koniec':t + blok, 'wolne':True})
        t += blok

    return render_template('zapisy/nauczyciel.html',
                           rozklad=rozklad,
                           imie = imie_nazwisko_nauczyciela['imie'],
                           nazwisko = imie_nazwisko_nauczyciela['nazwisko'],
    )
