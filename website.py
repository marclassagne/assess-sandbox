from bottle import run, template, static_file, view, Bottle, request, response
from sys import argv
import sys
import random
import json
import fit
import codecs
import methods
import plot
import kcalc
import latex_render
import draw_tree
import os
import export_xlsx
import import_xlsx
import traceback
import time
import selecteur

app = Bottle()
mdp = []


@app.route('/admin')
@view('authentification')
def export():
    return {'get_url':  app.get_url}


@app.route('/auth', method="POST")
def auth():
    global mdp
    reader = codecs.getreader("utf-8")
    query = json.load(reader(request.body))
    if query['type'] == "authentification":
        if check_passwd(query['mdp']):
            response.set_cookie("mdp", query['mdp'])
            return {'success': True}
        elif check_admin(query['mdp']):
            return {'success': "admin", 'mdp': mdp}
        else:
            return {'success': False}

    elif query['type'] == "admin":
        if check_admin(query['mdp']):
            mdp = query['newmdp']
            f = open('passwd.txt', 'w')
            f.write(";;".join(mdp))
            f.close()
            return {'success': True}
        else:
            return {'success': False}


@app.route('/export')
@view('export')
def export():
    if check_passwd(request.get_cookie("mdp")) == False:
        return template('authentification', get_url=app.get_url)
    return {'get_url':  app.get_url}


@app.route('/import')
@view('import')
def imports():
    if check_passwd(request.get_cookie("mdp")) == False:
        return template('authentification', get_url=app.get_url)
    return {'get_url':  app.get_url}


@app.route('/')
@app.route('/attributes')
@view('attributes')
def attributes():
    if check_passwd(request.get_cookie("mdp")) == False:
        return template('authentification', get_url=app.get_url)
    return {'get_url':  app.get_url}


@app.route('/questions')
@view('questions')
def questions():
    if check_passwd(request.get_cookie("mdp")) == False:
        return template('authentification', get_url=app.get_url)
    return {'get_url':  app.get_url}


@app.route('/k_calculus')
@view('k_calculus')
def k_calculus():
    if check_passwd(request.get_cookie("mdp")) == False:
        return template('authentification', get_url=app.get_url)
    return {'get_url':  app.get_url}


@app.route('/settings')
@view('settings')
def settings():
    if check_passwd(request.get_cookie("mdp")) == False:
        return template('authentification', get_url=app.get_url)
    return {'get_url':  app.get_url}


@app.route('/credits')
@view('credits')
def credits():
    if check_passwd(request.get_cookie("mdp")) == False:
        return template('authentification', get_url=app.get_url)
    return {'get_url':  app.get_url}

# Test qualitative attributes


@app.route('/words')
@view('words')
def words():
    if check_passwd(request.get_cookie("mdp")) == False:
        return template('authentification', get_url=app.get_url)
    return {'get_url':  app.get_url}


@app.route('/qualitative')
@view('qualitative')
def qualitative():
    if check_passwd(request.get_cookie("mdp")) == False:
        return template('authentification', get_url=app.get_url)
    return {'get_url':  app.get_url}






@app.route('/ajax', method="POST")
def ajax():
    if check_passwd(request.get_cookie("mdp")) == False:
        return template('authentification', get_url=app.get_url)
    reader = codecs.getreader("utf-8")
    query = json.load(reader(request.body))
    
    
    """
    query = {'type': 'export_xlsx', 
             'data': 
                 {'attributes': 
                  [{'type': 'Quantitative', 'name': 'pieniche', 'unit': 'euros', 'val_min': 20, 'val_med': ['40', '60', '80'], 'val_max': 100, 'method': 'PE', 'mode': 'Normal', 'completed': 'False', 'checked': True, 'questionnaire': {'number': 3, 'points': {'40': 0.43, '60': 0.86, '80': 0.82}, 'utility': {}}, 'fonction': 'exponential', 'numero': 0, 'pts': {'points': [1, 2, 3], 'coord': [[40, 0.43], [60, 0.86], [80, 0.82], [20, 0], [100, 1]], 'exp': {'a': -1.963679476149352, 'b': 0.028213793872664365, 'c': 1.116885624561104, 'r2': 0.9669098127318985}, 'quad': {'a': -0.5720588230939125, 'b': 0.00016102941154695627, 'c': 0.03182352938563475, 'r2': 0.9609977126945451}, 'pow': {'a': 2.2107646754127557, 'b': 1.3371874567609472, 'c': -4.168783582605269, 'r2': 0.9633217332780892}, 'lin': {'a': 0.0125, 'b': -0.25, 'r2': 0.7480678661997344}, 'expo-power': {'a': -1825.2176950884375, 'b': -7.508435131653395, 'c': 4.5317707067475485e-05, 'r2': 0.9498855834689701}}}, 
                   {'type': 'Quantitative', 'name': 'ccxw', 'unit': 'cxw', 'val_min': 10, 'val_med': ['32.5', '55', '77.5'], 'val_max': 100, 'method': 'PE', 'mode': 'Normal', 'completed': 'False', 'checked': True, 'questionnaire': {'number': 3, 'points': {'55': 0.76, '32.5': 0.32, '77.5': 0.96}, 'utility': {}}, 'fonction': '', 'numero': 0}], 
                  'k_calculus': 
                  [{'method': 'multiplicative', 'active': True, 'k': [], 'GK': None, 'GU': None}, 
                   {'method': 'multilinear', 'active': False, 'k': [], 'GK': None, 'GU': None}], 
                  'settings': 
                   {'decimals_equations': '2', 'decimals_dpl': '8', 'proba_ce': '0.3', 'proba_le': '0.3', 'language': 'french', 'display': 'trees'}
                 }
            }
    """
    
    
    
    
    
    
    
    if query['type'] == "question":
        if query['method'] == 'PE':
            return methods.PE(float(query['min_interval']), float(query['max_interval']), float(query['proba']), int(query['choice']), str(query['mode']))
        elif query['method'] == 'LE':
            return methods.LE(float(query['min_interval']), float(query['max_interval']), float(query['proba']), int(query['choice']), str(query['mode']))
        elif query['method'] == 'CE_Constant_Prob':
            return methods.CE(float(query['min_interval']), float(query['max_interval']), float(query['gain']), int(query['choice']), str(query['mode']))
        else:
            return query['method']

    elif query['type'] == "calc_util":
        return fit.regressions(query['points'])

    elif query['type'] == "calc_util_multi":
        return fit.multipoints(query['points'])

    elif query['type'] == "k_calculus":
        if query['number'] == 2:
            return kcalc.calculk2(query['k']['k1'], query['k']['k2'])
        elif query['number'] == 3:
            return kcalc.calculk3(query['k']['k1'], query['k']['k2'], query['k']['k3'])
        elif query['number'] == 4:
            return kcalc.calculk4(query['k']['k1'], query['k']['k2'], query['k']['k3'], query['k']['k4'])
        elif query['number'] == 5:
            return kcalc.calculk5(query['k']['k1'], query['k']['k2'], query['k']['k3'], query['k']['k4'], query['k']['k5'])
        elif query['number'] == 6:
            return kcalc.calculk6(query['k']['k1'], query['k']['k2'], query['k']['k3'], query['k']['k4'], query['k']['k5'], query['k']['k6'])

    elif query['type'] == "utility_calculus_multiplicative":
        return kcalc.calculUtilityMultiplicative(query['k'], query['utility'], query['virgule'])
    elif query['type'] == "utility_calculus_multilinear":
        return kcalc.calculUtilityMultilinear(query['k'], query['utility'], query['virgule'])

    elif query['type'] == "svg":
        dictionary = query['data']
        min_ = float(query['min'])
        max_ = float(query['max'])
        liste_cord = query['liste_cord']
        width = query['width']
        liste = query['liste']
        return plot.generate_svg_plot(dictionary, min_, max_, liste_cord, width, liste)

    elif query['type'] == "svgg":
        dictionary = query['data']
        min = float(query['min'])
        max = float(query['max'])
        liste_cord = query['liste_cord']
        width = query['width']
        choice = query['choice']
        return plot.generate_svg_plot2(dictionary, min, max, liste_cord, width, choice)

    elif query['type'] == "svg_QUALI":
        dictionary = query['data']
        list_names = query['list_names']
        width = query['width']
        return plot.generate_svg_plot_QUALI(dictionary, list_names, width)

    elif query['type'] == "pie_chart":
        names = query['names']
        probas = query['probas']
        return plot.pie_chart(names, probas)
    
    elif query['type'] == "demande_de_transformation":
        return selecteur.selecteur1(query['data'],query['numero'])

    elif query['type'] == "export_xlsx":
        return export_xlsx.generate_fichier(query['data'])

    elif query['type'] == "export_xlsx_option":
        return export_xlsx.generate_fichier_with_specification(query['data'])

    elif query['type'] == "latex_render":
        return latex_render.render(query['formula'])

    elif query['type'] == "tree":
        return draw_tree.draw(query['gain'], query['upper_label'], query['bottom_label'], query['upper_proba'], query['bottom_proba'], query['assess_type'])


# export a file (download)
@app.route('/export_download/fichier:path#.+#', name='export')
def export(path):
    if check_passwd(request.get_cookie("mdp")) == False:
        return template('authentification', get_url=app.get_url)
    val = static_file('fichier' + path + '.xlsx', root='')
    
    
    #os.remove('fichier' + path + '.xlsx')
    return val


# import a file (upload)
@app.route('/upload', method='POST')
@view('import_success')
def do_upload():
    if check_passwd(request.get_cookie("mdp")) == False:
        return template('authentification', get_url=app.get_url)
    try:

        upload = request.files.get('upload')
        name, ext = os.path.splitext(upload.filename)
        if ext not in ('.xlsx'):
            return {'get_url':  app.get_url, 'success': 'false', 'data_fail': "File extension not allowed. You must import xlsx only", 'data': ''}

        # we add a random name to the file:
        r = random.randint(1, 1000)
        file_path = str(r) + "{file}".format(path="", file=upload.filename)
        upload.save(file_path)
        val = import_xlsx.importation(file_path)
        if val['success'] == True:
            print("import ok")
            return {'get_url':  app.get_url, 'success': 'true', 'data': json.dumps(val['data']), 'data_fail': ''}
        else:
            return {'get_url':  app.get_url, 'success': 'false', 'data_fail': val['data'], 'data': ''}
    except:
        return {'get_url':  app.get_url, 'success': 'false', 'data_fail': traceback.format_exc(), 'data': ''}


# all static files for the website
@app.route('/static/:path#.+#', name='static')
def static(path):
    return static_file(path, root='static')


@app.route('/equations/:path#.+#', name='equations')
def equations(path):
    return static_file(path, root='equations')

# for authentification


def check_passwd(passwd):
    for m in mdp:
        if m == passwd:
            return True
    return False


def check_admin(passwd):
    if passwd == "assess2admin2015":
        return True
    return False

print("-----------Assess load successfully-----------")

with open("passwd.txt") as f:
    mdp = f.readline().split(";;")
    # print(mdp)


# for local or heroku app
try:
    if argv[1] == "local":  # for local application, add local param: "$python website.py local"
        run(app, host='localhost', port=9853, debug=True)
    else:
        app.run(host='0.0.0.0', port=argv[1])
except:
    # print("You need to specify an argument (local for local testing: python website.py local")
    print("cd C:\\Users\\Yossef\\Desktop\\Assess-master")
    print("python website.py local")
