from bottle import run, route, request, get, post, FormsDict, error
from connection import *
import psycopg2

@route('/', method="get")
def main():
    return '''
<html>
    <head>
        <title>Home page</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">
    </head>
    <body>
        <!-- Nav Bar-->
        <div id="navbar" class="collapse navbar-collapse navbar-inverse">
        <ul class="nav navbar-nav">
            <li class="active"><a href="/">Home</a></li>
            <li><a href="/NewPlayer">New Player</a></li>
        </ul>
        </div><!--/.nav-collapse -->


        <div class="container">
            <div class="starter-template">
                <!-- Main content should go here-->
                <h1>Player Search</h1>
                <h5>If a search field is left empty all results will be returned for that field</h5>
                <h5>Use '%' as a wildcard symbol</h5>
                ''' + search() + '''
            </div>
        </div>
    </body>
</html>
'''


@get('/Search')
def search():
  return '''<form action="/Search" method="post">
                    Name: <input type="text" name="name">
                    Age: <input type="text" name="age">
                    Team: <input type="text" name="team">

                    <input type="submit">
                </form>
                '''

@post('/Search')
def do_search():
  name = request.forms.get('name')
  age = request.forms.get('age')
  team = request.forms.get('team')
  conn = psycopg2.connect(host=url,database=database,user=user, password=password)
  cur = conn.cursor()
  goodsearch = True
  for i in name:
    if i==';' or i == "\'" or i== '\"':
      goodsearch=False
  for i in team:
    if i==';' or i == "\'" or i== '\"':
      goodsearch=False
  if not checkInteger(age):
    goodsearch=False
  if not goodsearch:
    cur.close()
    return error500()
  elif age != '' and team != '' and name != '':
    cur.execute("Select * from players where playername ilike (%s) and age=(%s) and teamname ilike (%s) limit 50;", (name, age, team))
  elif age != '' and team != '':
    cur.execute("Select * from players where and age=(%s) and teamname ilike (%s) limit 50;", (age, team))
  elif team != '' and name != '':
    cur.execute("Select * from players where playername ilike (%s) and teamname ilike (%s) limit 50;", (name, team))
  elif name != '' and age != '':
    cur.execute("Select * from players where playername ilike (%s) and age = (%s) limit 50;", (name, age))
  elif age != '':
    cur.execute("Select * from players where age = (%s) limit 50;", [age])
  elif name != '':
    cur.execute("Select * from players where playername ilike (%s) limit 50;", [name])
  elif team != '':
    cur.execute("Select * from players where teamname ilike (%s) limit 50;", [team])
  elif age == '' and team == '' and name == '':
    cur.execute("Select * from players limit 50;")
  else:
    cur.close()
    return error500()
  s = cur.fetchall()
  cur.close()
  return '''
      <html>
    <head>
        <title>Custom Search</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">
    </head>
    <body>
        <!-- Nav Bar-->
        <div id="navbar" class="collapse navbar-collapse navbar-inverse">
        <ul class="nav navbar-nav">
            <li><a href="/">Home</a></li>
            <li><a href="/NewPlayer">New Player</a></li>
        </ul>
        </div><!--/.nav-collapse -->


        <div class="container">
            <div class="starter-template">
                <!-- Main content should go here-->
                <h1>Players</h1>

                <table class="table table-striped">
                    <tr> <th colspan=1>Name</th> <th colspan=1>Team</th> <th colspan=5>Age</th></Tr>
                    '''+resultToTable(s)+'''
                </table>
            </div>
        </div>
    </body>
</html>
'''

@route('/NewPlayer')
def newplayer():
  return '''
  <html>
    <head>
        <title>New Player</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">
    </head>
    <body>
        <!-- Nav Bar-->
        <div id="navbar" class="collapse navbar-collapse navbar-inverse">
        <ul class="nav navbar-nav">
            <li class="active"><a href="/">Home</a></li>
            <li><a href="/NewPlayer">New Player</a></li>
        </ul>
        </div><!--/.nav-collapse -->


        <div class="container">
            <div class="starter-template">
                <!-- Main content should go here-->
                <h1>Insert a new player</h1>''' + insertplayer() + '''
            </div>
        </div>
    </body>
</html>
'''

@get('/InsertPlayer')
def insertplayer():
  return '''<form action="/InsertPlayer" method="post">
                    Name: <input type="text" name="name">
                    Age: <input type="text" name="age">

                    <input type="submit">
                </form>
                '''

@post('/InsertPlayer')
def do_insertplayer():
  name = request.forms.get('name')
  age = request.forms.get('age')
  conn = psycopg2.connect(host=url,database=database,user=user, password=password)
  cur = conn.cursor()
  goodinsert = True
  for i in name:
    if i==';' or i == "\'" or i== '\"':
      goodinsert=False
  if name=='':
    goodinsert=False
  if not checkInteger(age):
    goodinsert=False
  if goodinsert:
    cur.execute("Insert into players values (%s, null,%s)", (name, age))
    conn.commit()
    cur.close()
    return '''
    <html>
    <head>
        <title>Error 404</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">
    </head>
    <body>
        <!-- Nav Bar-->
        <div id="navbar" class="collapse navbar-collapse navbar-inverse">
        <ul class="nav navbar-nav">
            <li class="active"><a href="/">Home</a></li>
            <li><a href="/NewPlayer">New Player</a></li>
        </ul>
        </div><!--/.nav-collapse -->


        <div class="container">
            <div class="starter-template">
                <!-- Main content should go here-->
                <h1>Player successfully inserted!</h1>
            </div>
        </div>
    </body>
</html>
'''
  else:
    cur.close()
    return error500()

@route('/Edit/<name>')
def edit(name):
  conn = psycopg2.connect(host=url,database=database,user=user, password=password)
  cur = conn.cursor()
  cur.execute("select * from players where playername like (%s)", [name])
  s = cur.fetchone()
  age = str(s[2])
  team = str(s[1])
  return '''
  <html>
    <head>
        <title>Edit Player</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">
    </head>
    <body>
        <!-- Nav Bar-->
        <div id="navbar" class="collapse navbar-collapse navbar-inverse">
        <ul class="nav navbar-nav">
                <li class="active"><a href="/">Home</a></li>
                <li><a href="/NewPlayer">New Player</a></li>
        </ul>
        </div><!--/.nav-collapse -->


        <div class="container">
            <div class="starter-template">
                <!-- Main content should go here-->
                <h1>Edit Player Info</h1>

                <form action="/EditPlayer/'''+name+'''" method="post">
                    Name:<br> <input type="text" name="name" value="'''+name+'''"> <Br>
                    Age:<br> <input type="text" name="age" value="'''+age+'''"><Br>
                    Team:<br> <input type="text" name="team" value="'''+team+'''" disabled><br>
                    <br>
                    <input type="submit">
                </form>
            </div>
        </div>
    </body>
</html>
'''

@post('/EditPlayer/<name>')
def editPlayer(name):
  name2 = request.forms.get('name')
  age = str(request.forms.get('age'))
  conn = psycopg2.connect(host=url,database=database,user=user, password=password)
  cur = conn.cursor()
  goodupdate = True
  for i in name2:
    if i==';' or i == "\'" or i== '\"':
      goodupdate=False
  if name2=='':
    goodupdate=False
  if not checkInteger(age):
    goodupdate=False
  if goodupdate:
    cur.execute("Update players set playername=(%s), age=(%s) where playername like (%s);",(name2,age,name))
    conn.commit()
    cur.close()
    return '''
    <html>
    <head>
        <title>Edit Player</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">
    </head>
    <body>
        <!-- Nav Bar-->
        <div id="navbar" class="collapse navbar-collapse navbar-inverse">
        <ul class="nav navbar-nav">
            <li class="active"><a href="/">Home</a></li>
            <li><a href="/NewPlayer">New Player</a></li>
        </ul>
        </div><!--/.nav-collapse -->


        <div class="container">
            <div class="starter-template">
                <!-- Main content should go here-->
                <h1>Player successfully updated!</h1>
            </div>
        </div>
    </body>
</html>
'''
  else:
    cur.close()
    return error500(name)

@route('/Delete/<name>')
def delete(name):
  conn = psycopg2.connect(host=url,database=database,user=user, password=password)
  cur = conn.cursor()
  cur.execute("Delete from matchplayerresults where playername =(%s);",[name])
  cur.execute("Delete from players where playername=(%s);",[name])
  conn.commit()
  cur.close()
  return '''
  <html>
    <head>
        <title>Delete Player</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">
    </head>
    <body>
        <!-- Nav Bar-->
        <div id="navbar" class="collapse navbar-collapse navbar-inverse">
        <ul class="nav navbar-nav">
            <li class="active"><a href="/">Home</a></li>
            <li><a href="/NewPlayer">New Player</a></li>
        </ul>
        </div><!--/.nav-collapse -->


        <div class="container">
            <div class="starter-template">
                <!-- Main content should go here-->
                <h1>Player successfully deleted!</h1>
            </div>
        </div>
    </body>
</html>
'''

@route('/ShowResults/<name>')
def showResults(name):
  conn = psycopg2.connect(host=url,database=database,user=user, password=password)
  cur = conn.cursor()
  cur.execute("select matchid, heroname, kills, deaths from matchplayerresults where playername=(%s) limit 50;",[name])
  s=cur.fetchall()
  cur.close()
  return '''
      <html>
    <head>
        <title>Show Results</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">
    </head>
    <body>
        <!-- Nav Bar-->
        <div id="navbar" class="collapse navbar-collapse navbar-inverse">
        <ul class="nav navbar-nav">
            <li><a href="/">Home</a></li>
            <li><a href="/NewPlayer">New Player</a></li>
        </ul>
        </div><!--/.nav-collapse -->


        <div class="container">
            <div class="starter-template">
                <!-- Main content should go here-->
                <h1>Showing match results for: '''+name+'''</h1>

                <table class="table table-striped">
                    <tr> <th colspan=1>Match ID</th> <th colspan=1>Hero Name</th> <th colspan=1>Kills</th><th colspan=1>Deaths</th></Tr>
                    '''+resultToTable2(s)+'''
                </table>
            </div>
        </div>
    </body>
</html>
'''

@route('/Add/<name>')
def add(name):
  return '''
  <html>
    <head>
        <title>Add Results</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">
    </head>
    <body>
        <!-- Nav Bar-->
        <div id="navbar" class="collapse navbar-collapse navbar-inverse">
        <ul class="nav navbar-nav">
                <li class="active"><a href="/">Home</a></li>
                <li><a href="/NewPlayer">New Player</a></li>
        </ul>
        </div><!--/.nav-collapse -->


        <div class="container">
            <div class="starter-template">
                <!-- Main content should go here-->
                <h1>Add match results for player: '''+name+'''</h1>

                <form action="/AddResults/'''+name+'''" method="post">
                    Match ID (1-25000):<br> <input type="text" name="matchid"> <Br>
                    Hero Name:<br> <select name="heroname">
                        '''+heroOptions()+'''
                    </select><Br>
                    Kills:<br> <input type="text" name="kills"><br>
                    Deaths:<br> <input type="text" name="deaths"><br>
                    <br>
                    <input type="submit">
                </form>
            </div>
        </div>
    </body>
</html>
'''

@post('/AddResults/<name>')
def addResults(name):
  matchid = str(request.forms.get('matchid'))
  heroname = request.forms.get('heroname')
  kills = str(request.forms.get('kills'))
  deaths = str(request.forms.get('deaths'))
  conn = psycopg2.connect(host=url,database=database,user=user, password=password)
  cur = conn.cursor()
  goodinsert = True
  if not checkInteger(matchid):
    goodinsert=False
  if int(matchid)<1 or int(matchid)>25000:
    goodinsert=False
  if not checkInteger(kills) or int(kills)<0:
    goodinsert=False
  if not checkInteger(deaths) or int(deaths)<0:
    goodinsert=False
  if goodinsert:
    cur.execute("Insert into matchplayerresults values (%s,%s,%s,%s,%s)", (matchid,name, heroname,kills,deaths))
    conn.commit()
    cur.close()
    return '''
    <html>
    <head>
        <title>Add Results</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">
    </head>
    <body>
        <!-- Nav Bar-->
        <div id="navbar" class="collapse navbar-collapse navbar-inverse">
        <ul class="nav navbar-nav">
            <li class="active"><a href="/">Home</a></li>
            <li><a href="/NewPlayer">New Player</a></li>
        </ul>
        </div><!--/.nav-collapse -->


        <div class="container">
            <div class="starter-template">
                <!-- Main content should go here-->
                <h1>Results successfully inserted!</h1>
            </div>
        </div>
    </body>
</html>
'''
  else:
    cur.close()
    return error500()


@error(404)
def error404(error):
  return '''
  <html>
    <head>
        <title>Error 404</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">
    </head>
    <body>
        <!-- Nav Bar-->
        <div id="navbar" class="collapse navbar-collapse navbar-inverse">
        <ul class="nav navbar-nav">
            <li class="active"><a href="/">Home</a></li>
            <li><a href="/NewPlayer">New Player</a></li>
        </ul>
        </div><!--/.nav-collapse -->


        <div class="container">
            <div class="starter-template">
                <!-- Main content should go here-->
                <h1>Sorry, this page does not exist. Please go back to the home page.</h1>
            </div>
        </div>
    </body>
</html>
'''

@error(500)
def error500(error):
  return '''
  <html>
    <head>
        <title>Error 500</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">
    </head>
    <body>
        <!-- Nav Bar-->
        <div id="navbar" class="collapse navbar-collapse navbar-inverse">
        <ul class="nav navbar-nav">
            <li class="active"><a href="/">Home</a></li>
            <li><a href="/NewPlayer">New Player</a></li>
        </ul>
        </div><!--/.nav-collapse -->


        <div class="container">
            <div class="starter-template">
                <!-- Main content should go here-->
                <h1>Invalid entry or search, please try again.</h1>
            </div>
        </div>
    </body>
</html>
'''

@error(405)
def error405(error):
  return '''
  <html>
    <head>
        <title>Error 405</title>
        <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css" integrity="sha384-HSMxcRTRxnN+Bdg0JdbxYKrThecOKuH5zCYotlSAcp1+c8xmyTe9GYg1l9a69psu" crossorigin="anonymous">
    </head>
    <body>
        <!-- Nav Bar-->
        <div id="navbar" class="collapse navbar-collapse navbar-inverse">
        <ul class="nav navbar-nav">
            <li class="active"><a href="/">Home</a></li>
            <li><a href="/NewPlayer">New Player</a></li>
        </ul>
        </div><!--/.nav-collapse -->


        <div class="container">
            <div class="starter-template">
                <!-- Main content should go here-->
                <h1>You reached this page by an incorrect method, please go to the home page.</h1>
            </div>
        </div>
    </body>
</html>
'''

def resultToTable(inputresult):
  stringresult = ""
  for record in inputresult:
    name = str(record[0])
    stringresult +=('<td>'+ name+ '</Td>')
    age = str(record[1])
    stringresult +=('<td>'+ age+ '</Td>')
    team = str(record[2])
    stringresult +=('<td>'+ team+ '</Td>')
    stringresult += '<td><a href="Edit/'+name+'">Edit Record</a> </td> <td> <a href="Delete/'+name+'">Delete</a></td> <td> <a href="ShowResults/'+name+'">Show matches</a></td> <td> <a href="Add/'+name+'">Add matches</a> </td></tr></tr>\n'
  return stringresult

def resultToTable2(inputresult):
  stringresult = ""
  for record in inputresult:
    matchid = str(record[0])
    stringresult +=('<td>'+ matchid+ '</Td>')
    heroname = str(record[1])
    stringresult +=('<td>'+ heroname+ '</Td>')
    kills = str(record[2])
    stringresult +=('<td>'+ kills+ '</Td>')
    deaths = str(record[3])
    stringresult +=('<td>'+ deaths+ '</Td></tr></tr>\n')
  return stringresult

def heroOptions():
  conn = psycopg2.connect(host=url,database=database,user=user, password=password)
  cur = conn.cursor()
  cur.execute("select heroname from heroes limit 50;")
  s=cur.fetchall()
  cur.close()
  stringresult = ""
  for record in s:
    stringresult+="<option>"+record[0]+"</option>\n"
  return stringresult

def checkInteger(s):
  try:
    int(s)
    return True
  except ValueError:
    return False

run(host='localhost', port=8080, debug=True)
