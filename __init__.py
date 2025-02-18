from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from collections import Counter
from datetime import datetime
from urllib.request import urlopen
import sqlite3
                                                                                                                                       
app = Flask(__name__)                                                                                                                  
                                                                                                                                       
@app.route('/')
def hello_world():
     return render_template("hello.html")


@app.route("/contact/")
def MaPremiereAPI():
    return render_template("contact.html")

  
@app.route('/tawarano/')
def meteo():
    response = urlopen('https://samples.openweathermap.org/data/2.5/forecast?lat=0&lon=0&appid=xxx')
    raw_content = response.read()
    json_content = json.loads(raw_content.decode('utf-8'))
    results = []
    for list_element in json_content.get('list', []):
        dt_value = list_element.get('dt')
        temp_day_value = list_element.get('main', {}).get('temp') - 273.15 # Conversion de Kelvin en °c 
        results.append({'Jour': dt_value, 'temp': temp_day_value})
    return jsonify(results=results)


@app.route("/rapport/")
def mongraphique():
    return render_template("graphique.html")

@app.route("/histogramme/")
def monhistogramme():
    return render_template("histogramme.html")

@app.route('/extract-minutes/')
def extract():
    # URL de l'API GitHub pour récupérer les commits
    url = 'https://api.github.com/repos/OpenRSI/5MCSI_Metriques/commits'

    # Récupérer les commits depuis l'API GitHub avec urllib
    response = urlopen(url)
    raw_content = response.read()
    commits_data = json.loads(raw_content.decode('utf-8'))

    # Extraire les minutes des commits
    commit_minutes = []
    for commit in commits_data:
        commit_date = commit['commit']['author']['date']
        minute = extract_minutes(commit_date)
        commit_minutes.append(minute)

    # Compter les commits par minute
    minute_counts = Counter(commit_minutes)

    # Créer la structure des résultats à renvoyer sous forme de JSON
    results = [{'minute': minute, 'count': minute_counts[minute]} for minute in sorted(minute_counts.keys())]

    return jsonify(results=results)

def extract_minutes(date_string):
    """ Extraire la minute d'une date au format ISO 8601 """
    date_object = datetime.strptime(date_string, '%Y-%m-%dT%H:%M:%SZ')
    return date_object.minute


@app.route("/commits/")
def commits():
    return render_template("commits.html")

if __name__ == "__main__":
  app.run(debug=True)

