from flask import Flask, request, render_template
import requests, sqlite3, datetime, eel, webbrowser

app = Flask(__name__)
eel.init("Praktika_2022")

host = 'https://pub.orcid.org/v3.0/'
conn = sqlite3.connect("orcid1.db", check_same_thread=False)
cursor = conn.cursor()

count = 0
global temp
resp = []#?


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        orcid_id = request.form.get('id')
        cursor.execute("SELECT * FROM orcid7")
        print(cursor.execute("SELECT * FROM orcid7"))
        c = 0
        for i in range(19):
            print(c)
            c = c + 1
            resp.append(cursor.fetchmany(size=25))
        rows = resp
        print(resp)
        print("orcid7:")
        f = 1
        for value in cursor.execute("SELECT * FROM orcid7"):
            print(f, value[0], value[1], value[2], value[3], value[4])
            f = f + 1
        print()
        print(rows)
        return render_template("3.html", table=rows)
    else:
        return render_template("1.html")

@app.route('/big_base', methods=['GET'])
def bb():
    mining_search_res = requests.get(host + 'search/?q=affiliation-org-name:"Saint+Petersburg+Mining+University"', headers = {'Accept': 'application/vnd.orcid+json'}).json()['result']
    for i in mining_search_res:#Внос данных в таблицу БД
        orcid_id = i['orcid-identifier']['path']
        mass = []
        person_req = requests.get(host + orcid_id + '/person', headers = {'Accept': 'application/vnd.orcid+json'})
        works_req = requests.get(host + orcid_id + '/works', headers = {'Accept': 'application/vnd.orcid+json'}).json()['group']
        if person_req.json()['name'] is None or person_req.json()['name']['given-names'] is None or person_req.json()['name']['family-name'] is None:# person_req.json():
            name = 'None'
            surname = 'None'
        else:
            name = person_req.json()['name']['given-names']['value']
            surname = person_req.json()['name']['family-name']['value']

        kwords_str = ''
        keywords_req = person_req.json()['keywords']['keyword']
        for i in keywords_req:
            kwords_str = kwords_str + i['content'] + '; '

        mass.append({"name": name, "surname": surname, "keywords": kwords_str})
        print(mass)
        # works_str = ''
        # for i in works_req:
        #     a = i['external-ids']['external-id']
        #     for j in a:
        #         if j['external-id-type'] == "doi":
        #             works_str = works_str + j['external-id-value'] + '; '
    return render_template("5.html", table=mass)




@app.route('/table', methods=['GET', 'POST'])
def table():
    cursor.execute("SELECT * FROM orcid7")
    for i in range(30):
        resp.append(cursor.fetchmany(size=25))
    return render_template("5.html", table=resp)

@app.route('/page<int:page_number>', methods=['GET', 'POST'])#общее для страниц списка
def page(page_number):
    resp = []
    cursor.execute("SELECT * FROM orcid7")
    for i in range(page_number-1):
        cursor.fetchmany(size=25)
    for i in range(1):
        resp.append(cursor.fetchmany(size=25))
    return render_template("5.html", table=resp)

@app.route('/page<int:page_number>/<swap>', methods=['GET', 'POST'])#общее для страниц списка
def list(page_number, swap):
    print(swap)
    if swap == 'next':
        print(swap)
        webbrowser.open('http://127.0.0.1:5000/page'+str(page_number+1))
        #urllib.request.urlopen('http://127.0.0.1:5000/page<int:page_number>')
        #urllib.request.urlopen
        #requests.get(host + orcid_id + '/person', headers = {'Accept': 'application/vnd.orcid+json'})


if __name__ == "__main__":
    app.run(debug=True)

    now = datetime.datetime.now()#time
    time = now.strftime("%H:%M:%S")
    current_hour = datetime.datetime.now().strftime("%H")
    current_min = datetime.datetime.now().strftime("%M")
    current_sec = datetime.datetime.now().strftime("%S")
    if current_hour=='03' and current_min=='0' and current_sec=='0':
        print("DATABASE WILL BE UPDATED")#вот в этой штуке должно быть всё что обновляет ДБ (наверное)

    cursor.execute("""CREATE TABLE IF NOT EXISTS orcid7
                (name text, surname text, orcid_id text UNIQUE, k_words text, works text)
                """)
    conn.commit()

    mining_search_res = requests.get(host + 'search/?q=affiliation-org-name:"Saint+Petersburg+Mining+University"', headers = {'Accept': 'application/vnd.orcid+json'}).json()['result']

    for i in mining_search_res:#Внос данных в little таблицу БД
    orcid_id = i['orcid-identifier']['path']
    person_req = requests.get(host + orcid_id + '/person', headers = {'Accept': 'application/vnd.orcid+json'})
    works_req = requests.get(host + orcid_id + '/works', headers = {'Accept': 'application/vnd.orcid+json'}).json()['group']
    if person_req.json()['name'] is None or person_req.json()['name']['given-names'] is None or person_req.json()['name']['family-name'] is None:# person_req.json():
        name = 'None'
        surname = 'None'
        print(count, orcid_id, "None")
    else:
        count = count + 1
        name = person_req.json()['name']['given-names']['value']
        surname = person_req.json()['name']['family-name']['value']

    kwords_str = ''
    keywords_req = person_req.json()['keywords']['keyword']
    for i in keywords_req:
        kwords_str = kwords_str + i['content'] + '; '

    #этим кодом заносятся doi работ человека в строку
    works_str = ''
    for i in works_req:
        a = i['external-ids']['external-id']
        for j in a:
            if j['external-id-type'] == "doi":
                works_str = works_str + j['external-id-value'] + '; '

    print(name, surname, orcid_id, kwords_str, works_str)
    if cursor.fetchone() is None:
        cursor.execute("INSERT OR REPLACE INTO orcid8(doi, wosid, puy_code, source_name, name, surname, orcid_id, k_words, works) VALUES (?, ?, ?, ?, ?)", (name, surname, orcid_id, kwords_str, works_str))
        conn.commit()


    # for i in mining_search_res:#Внос данных в little таблицу БД
    #     orcid_id = i['orcid-identifier']['path']
    #     person_req = requests.get(host + orcid_id + '/person', headers = {'Accept': 'application/vnd.orcid+json'})
    #     works_req = requests.get(host + orcid_id + '/works', headers = {'Accept': 'application/vnd.orcid+json'}).json()['group']
    #     if person_req.json()['name'] is None or person_req.json()['name']['given-names'] is None or person_req.json()['name']['family-name'] is None:# person_req.json():
    #         name = 'None'
    #         surname = 'None'
    #         print(count, orcid_id, "None")
    #     else:
    #         count = count + 1
    #         name = person_req.json()['name']['given-names']['value']
    #         surname = person_req.json()['name']['family-name']['value']
    #
    #     kwords_str = ''
    #     keywords_req = person_req.json()['keywords']['keyword']
    #     for i in keywords_req:
    #         kwords_str = kwords_str + i['content'] + '; '
    #
    #     #этим кодом заносятся doi работ человека в строку
    #     works_str = ''
    #     for i in works_req:
    #         a = i['external-ids']['external-id']
    #         for j in a:
    #             if j['external-id-type'] == "doi":
    #                 works_str = works_str + j['external-id-value'] + '; '
    #
    #     #а этим
    #
    #     print(name, surname, orcid_id, kwords_str, works_str)
    #     if cursor.fetchone() is None:
    #         cursor.execute("INSERT OR REPLACE INTO orcid7(name, surname, orcid_id, k_words, works) VALUES (?, ?, ?, ?, ?)", (name, surname, orcid_id, kwords_str, works_str))
    #         conn.commit()

