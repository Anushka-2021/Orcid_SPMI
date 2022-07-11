from flask import Flask, request, jsonify, render_template
import requests, sqlite3, sqlalchemy, json
#from flask_restful import Api, Resourse, reqparse

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

app = Flask(__name__)

host = 'https://pub.orcid.org/v3.0/'
conn = sqlite3.connect("orcid1.db", check_same_thread=False)
cursor = conn.cursor()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        orcid_id = request.form.get('id')
        req = requests.get('https://pub.orcid.org/v3.0/' + orcid_id + '/person', headers = {'Accept': 'application/vnd.orcid+json'})
        name_try = req.json()['name']['given-names']['value']
        surname_try = req.json()['name']['family-name']['value']
        keywords_try = req.json()['keywords']['keyword']
        cursor.execute("SELECT * FROM orcid5 WHERE orcid_id=?", (orcid_id,))
        rows = cursor.fetchone()
        print(rows)

        if cursor.fetchone() is None: #orcid3.query(orcid3).filter_by(orcid_id=orcid_id).first():
            cursor.execute("INSERT OR REPLACE INTO orcid5(name, surname, orcid_id) VALUES (?, ?, ?)", (name_try, surname_try, orcid_id))
            conn.commit()
    #    rows = cursor.execute("SELECT * FROM orcid2")#fetchall()
    #    print(rows)
    #    print(rows['name'])


        print("orcid5:")
        for value in cursor.execute("SELECT rowid, * FROM orcid5"):
            print(value[0], value[1], value[2], value[3])
        print()

        return render_template("2.html", table=rows)
    else:
        return render_template("1.html")
#   req = requests.get(host + '/0000-0002-3707-6813/person', headers = {'Accept': 'application/vnd.orcid+json'})
  #  return req.json['name']['given-names']['value']#, req.json['name']['family-names']['value']

@app.route('/<orcid_id>')
def about_person(orcid_id):
    req = requests.get(host + '/' + orcid_id + '/person', headers = {'Accept': 'application/vnd.orcid+json'})
    return req.json['name']['given-names']['value']#, req.json['name']['family-names']['value']

if __name__ == "__main__":
    app.run(debug=True)
    count = 0
    cursor.execute("""CREATE TABLE IF NOT EXISTS orcid5
                (name text, surname text, orcid_id text UNIQUE)
                """)
    conn.commit()

    mining_search = requests.get(host + 'search/?q=affiliation-org-name:"Saint+Petersburg+Mining+University"', headers = {'Accept': 'application/vnd.orcid+json'})
    mining_search_res = mining_search.json()['result']

    for i in mining_search_res:
        orcid_id = i['orcid-identifier']['path']
        person_req = requests.get(host + orcid_id + '/person', headers = {'Accept': 'application/vnd.orcid+json'})
        if person_req.json()['name'] is None or person_req.json()['name']['given-names'] is None or person_req.json()['name']['family-name'] is None:# person_req.json():
            print(count, orcid_id, "None")
        else:
            count = count + 1
            name = person_req.json()['name']['given-names']['value']
            surname = person_req.json()['name']['family-name']['value']
            if cursor.fetchone() is None:
                cursor.execute("INSERT OR REPLACE INTO orcid5(name, surname, orcid_id) VALUES (?, ?, ?)", (name, surname, orcid_id))
                conn.commit()
    print("!!!")
    print(count)
    print("!!!")

    # for i in mining_search_res:
    #      print(i['orcid-identifiers']['path'])