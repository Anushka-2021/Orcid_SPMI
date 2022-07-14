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
        cursor.execute("SELECT * FROM orcid8")
        print(cursor.execute("SELECT * FROM orcid8"))
        c = 0
        for i in range(19):
            print(c)
            c = c + 1
            resp.append(cursor.fetchmany(size=25))
        rows = resp
        print(resp)
        print("orcid8:")
        f = 1
        for value in cursor.execute("SELECT * FROM orcid8"):
            print(f, value[0], value[1], value[2], value[3], value[4], value[5], value[6], value[7], value[8], value[9])
            f = f + 1
        print()
        print(rows)
        return render_template("3.html", table=rows)
    else:
        return render_template("1.html")

# @app.route('/big_base', methods=['GET'])
# def bb():
#     mining_search_res = requests.get(host + 'search/?q=affiliation-org-name:"Saint+Petersburg+Mining+University"', headers = {'Accept': 'application/vnd.orcid+json'}).json()['result']
#     for i in mining_search_res:#Внос данных в таблицу БД
#         orcid_id = i['orcid-identifier']['path']
#         mass = []
#         person_req = requests.get(host + orcid_id + '/person', headers = {'Accept': 'application/vnd.orcid+json'})
#         works_req = requests.get(host + orcid_id + '/works', headers = {'Accept': 'application/vnd.orcid+json'}).json()['group']
#         if person_req.json()['name'] is None or person_req.json()['name']['given-names'] is None or person_req.json()['name']['family-name'] is None:# person_req.json():
#             name = 'None'
#             surname = 'None'
#         else:
#             name = person_req.json()['name']['given-names']['value']
#             surname = person_req.json()['name']['family-name']['value']
#
#         kwords_str = ''
#         keywords_req = person_req.json()['keywords']['keyword']
#         for i in keywords_req:
#             kwords_str = kwords_str + i['content'] + '; '
#
#         mass.append({"name": name, "surname": surname, "keywords": kwords_str})
#         print(mass)
#         # works_str = ''
#         # for i in works_req:
#         #     a = i['external-ids']['external-id']
#         #     for j in a:
#         #         if j['external-id-type'] == "doi":
#         #             works_str = works_str + j['external-id-value'] + '; '
#     return render_template("5.html", table=mass)




@app.route('/table', methods=['GET', 'POST'])
def table():
    cursor.execute("SELECT * FROM orcid8")
    for i in range(30):
        resp.append(cursor.fetchmany(size=25))
    return render_template("5.html", table=resp)

@app.route('/page<int:page_number>', methods=['GET', 'POST'])#общее для страниц списка
def page(page_number):
    resp = []
    cursor.execute("SELECT * FROM orcid8")
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

    # cursor.execute("""CREATE TABLE IF NOT EXISTS orcid7
    #             (name text, surname text, orcid_id text UNIQUE, k_words text, works text)
    #             """)
    # conn.commit()

    cursor.execute("""CREATE TABLE IF NOT EXISTS orcid8
                (doi, wosid, summary_str, orcid_id, name, surname, other_names, country, external_ids, k_words)
                """)
    conn.commit()

    mining_search_res = requests.get(host + 'search/?q=affiliation-org-name:"Saint+Petersburg+Mining+University"', headers = {'Accept': 'application/vnd.orcid+json'}).json()['result']
    #cnt = 1
    for i in mining_search_res:#Внос данных в big таблицу БД
        #cnt = cnt + 1
        orcid_id = i['orcid-identifier']['path']
        person_req = requests.get(host + orcid_id + '/person', headers = {'Accept': 'application/vnd.orcid+json'}).json()
        works_req = requests.get(host + orcid_id + '/works', headers = {'Accept': 'application/vnd.orcid+json'}).json()['group']

        if person_req['name'] is None or person_req['name']['given-names'] is None or person_req['name']['family-name'] is None:# person_req.json():
            name = 'None'
            surname = 'None'
        else:
            name = person_req['name']['given-names']['value']
            surname = person_req['name']['family-name']['value']

        kwords_str = ''
        keywords_req = person_req['keywords']['keyword']
        for i in keywords_req:
            kwords_str = kwords_str + i['content'] + '; '

        #last_m_d_pers = person_req['value']#?
        other_names = ''
        for i in person_req['other-names']['other-name']:
            other_names += i['content']#???

        #biography = person_req['biography']#?
        #person_req['researcher-urls']
        country = ''#str(person_req['addresses']['address']['country']['value'])
        for i in person_req['addresses']['address']:
            country += i['country']['value'] + "; "

        external_ids = ''
        for i in person_req['external-identifiers']['external-identifier']:
            external_ids += i['external-id-type'] + ': ' + i['external-id-value'] + '; '


        #этим кодом заносятся вытаскивается всё про работу
        for i in works_req:
            last_m_d = i['last-modified-date']['value']#?

            ids = i['external-ids']['external-id']
            wos = None
            doi = None
            for j in ids:
                if j['external-id-type'] == "wosuid":
                    wos = j['external-id-value']
                if j['external-id-type'] == "doi":
                    wos = j['external-id-value']

            w_summary = i['work-summary']
            summary_str = ''
            for j in w_summary:

                if doi == None and j['external-ids'] != None and j['external-ids']['external-id'] != None:
                    for k in j['external-ids']['external-id']:
                        if k['external-id-type'] == 'doi' and k['external-id-value'] != ('none' or None):
                            doi = k['external-id-value']
                if wos == None and j['external-ids'] != None and j['external-ids']['external-id'] != None:
                    for k in j['external-ids']['external-id']:
                        if k['external-id-type'] == 'wosuid' and k['external-id-value'] != ('none' or None):
                            wos = k['external-id-value']


                put_code = j['put-code']
                source_name = j['source']['source-name']['value']
                work_title = j['title']['title']['value']
                work_type = j['type']

                work_publication_date = ''
                if j['publication-date'] != None:
                    if j['publication-date']['day'] != 'null' and j['publication-date']['day'] != None:
                        work_publication_date += j['publication-date']['day']['value']
                    if j['publication-date']['month'] !='null' and j['publication-date']['month'] != None:
                        work_publication_date += '.' + j['publication-date']['month']['value']
                    else:
                        work_publication_date += '.xx'
                    if j['publication-date']['year'] != 'null' and j['publication-date']['year'] != None:
                        work_publication_date += '.' + j['publication-date']['year']['value']
                    else:
                        work_publication_date += '.xxxx'
                else:
                    work_publication_date = 'None'

                if j['journal-title'] != None:
                    journal_title = j['journal-title']['value']
                summary_str += str(put_code) + ', ' + source_name + ', ' + work_title + ', ' + work_type + ', ' + work_publication_date + ', ' + journal_title + '; '
            print(doi, wos, summary_str, orcid_id, name, surname, other_names, country, external_ids, kwords_str)
            if cursor.fetchone() is None:
                cursor.execute("INSERT OR REPLACE INTO orcid8(doi, wosid, summary_str, orcid_id, name, surname, other_names, country, external_ids, k_words) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", (doi, wos, summary_str, orcid_id, name, surname, other_names, country, external_ids, kwords_str))
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

