from sqlite3.dbapi2 import Cursor
from flask import Flask
from flask import render_template
from flask import request
from flask import flash
from flask import redirect, url_for
from flask import jsonify
from flask import session
from flask import g
import re

import functools
import os
import sqlite3
from sqlite3 import Error
#import yagmail as yagmail
from formularios import Login,Crearusuario,Editarusuario,Retroalimentacion,Buscarusuario,myRetroalimentacion
#from flask_login import LoginManager,login_user,logout_user,login_required,current_user

from db import get_db, close_db
from werkzeug.security import generate_password_hash, check_password_hash 





######################################
##########funciones###################



def sql_select_empleados_dict():
	strsql = "SELECT * FROM Empleados;"
	conn = get_db()
	cursorObj = conn.cursor()
	cursorObj.execute(strsql)
	empleados = cursorObj.fetchall()
	lista_empleados = [ {"numero_documento": empleado[0], "nombre": empleado[1], "apellido": empleado[2], "telefono": empleado[3], "correo": empleado[4], "id_cargo": empleado[5], "contrato": empleado[6], "tdocumento": empleado[7], "fechadeinicio": empleado[8], "fechafin": empleado[9], "salario": empleado[10], "contrasena": empleado[11], "tipousuario": empleado[12], "dependencia": empleado[13] } for empleado in empleados ]
	return lista_empleados




#validacion de contrasena
def validarcontrasena(contrasena):
    if len(contrasena) < 8:
        return False
  
    if re.search('[0-9]',contrasena) is None:
        return False
    if re.search('[A-Z]',contrasena) is None: 
        return False
    
    return True


def validarnumero(cel):
    
    if cel < 1000000000:
        return False
    if cel > 9999999999999:
        return False
     
    return True

def validarsalario(salario):
    
    if salario < 900000:
        return False
    if salario > 20000000:
        return False
     
    return True



def validardocumento(documento):

    if documento < 100000000:
        return False
    if documento > 9999999999999:
        return False
 
        return False
    if not re.search('[A-Z]',documento) is None: 
        return False
    
    return True


def validarnombreapellido(nomape):
    if re.search('[0-9]',nomape) is None:
        return False
    return True


#######################################################
###############FIN FUNCIONES###########################



app = Flask(__name__)
app.secret_key = os.urandom(24)


def login_required(view):
    @functools.wraps( view ) 
    def wrapped_view(**kwargs):
        if g.usuario is None:
            return redirect( url_for( 'index' ) )
        return view( **kwargs )
    return wrapped_view

@app.route('/',methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])

def index():
    try:
        form = Login(request.form)
        g.estado=True
        if request.method == 'POST': # and form.validate(): 
            error = None
            db = get_db()
            usuario=request.form['usuario']
            passwo=request.form['password']
            sqluser = db.execute("SELECT * FROM Empleados WHERE numero_documento='{}'"
                .format(usuario)).fetchone() 

            if sqluser is None:
                    error = "Usuario y/o contraseña no son correctos."
                    flash(error)
                    return render_template("login.html", form=form)
            else:
                    usuario_valido = check_password_hash(sqluser[11],passwo)


            if not usuario_valido:
                error = "Usuario y/o contraseña no son correctos."
                flash( error ) 
            else:
                session.clear()
                session['id_usuario']=sqluser[0] 
                session['nombre']=sqluser[1] 
                session['rol']=sqluser[12] 


                if sqluser[12]=="Superadmin":


                    return redirect("/dashboard")
                     
                if sqluser[12]=="empleado":
                        return redirect("/mis_retro")

                if sqluser[12]=="administrador":

                    return redirect("/usuarios")

        return render_template("login.html", form=form)
    except:
        flash( "ha ocurrido un error inesperado, por favor vuelva a intentar" ) 



#######################################################################
#inicio admin
@app.route('/inicioadmin')
@login_required
def inicioadmin():
    if (session['rol'] == 'administrador') :
       return render_template("inicioadmin.html")
    else:
        return('acceso denegado')

#inicio super
@app.route('/inicio')
@login_required
def inicio():
    if session['rol'] == 'Superadmin':
        return render_template("dashboard.html")
    else:
        return('acceso denegado')


#inicio empleado
@app.route('/inicioempleado')
@login_required
def inicioempleado():
      if (session['rol'] == 'empleado') :
          return render_template("inicioempleado.html")
      return('acceso denegado')

  
#crear super 
@app.route('/crearusuario',methods=['GET', 'POST'])
@login_required
def crearusuario():
   try:
        if session['rol'] == 'Superadmin' or session['rol'] == 'administrador':
            errores=None
            form = Crearusuario(request.form)

            if request.method == 'POST':
                nombre = request.form['nombre']
                apellido = request.form['apellido']
                documento = request.form['documento']
                contrasena = request.form['contrasena']
                telefono = request.form['celular']
                correo=request.form['email']
                id_cargo=request.form['cargo']
                id_contrato=request.form['contrato']
                tdocumento=request.form['tdocumento']
                fechadeinicio=request.form['fechainicio']
                fechafin=request.form['fechafinalizacion']
                salario=request.form['salario']
                tipousuario=request.form['tipousuario']
                dependencia=request.form['dependencia']
                rcontrasena=request.form['rcontrasena']

                if (contrasena!=rcontrasena):
                    errores='la contrasenas no coincide'
                    print('no coincide',errores)
        ##########validacion formato########################
                
                if not validarcontrasena(contrasena):
                    errores='la contrasena debe contener al menos una letra mayuscula y numero'
                    print('formato',errores)

                if not validarnumero(int(telefono)):
                    errores='el telefono debe tener de 10 a 16 numeros'
                    print('formato telefono',errores)

                if not validarnumero(int(documento)):
                    errores='el documento debe terner entre 10-16 numeros'
                    print('formato documento',errores)
                
                if not validarsalario(int(salario)):
                    errores='el valor del salario es inferior al permitido'
                    print('formato salario',errores)
                #flash('paso validaciones de formato')
                if errores is not None:
                    print(' ocurrio esto ',errores)
                    flash(errores)    
                    return render_template("crearusuario.html",form=form)
        ###############FIN VALIDACION FORMATO ###############################################
                ##cifrado            
                password_cifrado = generate_password_hash(contrasena)
                db = get_db()
                sqluser = db.execute("SELECT * FROM Empleados WHERE numero_documento='{}'".format(documento)).fetchone()   
                                                    

                if sqluser is None: 
                ##validacion de campos// pasar a funcion  
                    sqltel = db.execute("SELECT * FROM Empleados WHERE telefono='{}'".format(telefono)).fetchone()
                    sqlcorreo = db.execute("SELECT * FROM Empleados WHERE correo='{}'".format(correo)).fetchone()

                    if sqltel is not None:
                        print('el telefono ya existe')
                        errores='el telefono existe'

                      
                    if sqlcorreo is not None:
                        print('correo existe')
                        errores='el correo existe'

                    if errores is not None:
                        flash(errores)                                           
                        return render_template("crearusuario.html",form=form)
                #fin validacion de campos// pasar a funcion 
               
                    sqluser = db.execute("SELECT * FROM Empleados WHERE numero_documento='{}'".format(documento)).fetchone()
                    print(sqluser)
                    if sqluser is None:
                        print("no existe")
                        sqluser = db.execute("INSERT INTO Empleados (numero_documento,nombre,apellido,telefono,correo,id_cargo,contrato,tdocumento,fechadeinicio,fechafin,salario,contrasena,tipousuario,dependencia) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                        (documento,nombre,apellido,telefono,correo,id_cargo,id_contrato,tdocumento,fechadeinicio,fechafin,salario,password_cifrado,tipousuario,dependencia))
                        db.commit()
                        flash("creado" )
                        print("creado")
                    else:
                        flash("el usuario ya existe" )
            return render_template("crearusuario.html",form=form)

        else:
            return('acceso denegado')
   except:
        flash( "ha ocurrido un error inesperado, verifique los datos ingresados" ) 
        return render_template("crearusuario.html",form=form)



@app.route('/usuarios', methods=['GET'])
@login_required
def show_users():
    empleados=sql_select_empleados_dict()
    print(empleados)
    return render_template('usuarios.html', empleados=empleados)

@app.route('/retroalimentaciones', methods=['GET'])
def show_retro():
    # empleados=sql_select_empleados_dict()
    # print(empleados)
    return render_template('retroalimentaciones.html')
#######################################################################
def sql_select_retrouser_dict():
    # documento = session['numero_documento']
    documento = session.get('id_usuario')
    # documento = 9101112
    print(documento)
    conn = get_db()
    retros = conn.execute('SELECT * FROM retroalimentacion WHERE numero_documento=?;', (documento,)).fetchall()
    lista_retros = [ {"numero_documento": retro[0], "puntaje": retro[1], "retro": retro[2], "mes": retro[3], "ano": retro[4] } for retro in retros ]
    print(lista_retros)
    return lista_retros


@app.route('/mis_retro')
def show_my_retros():
    misretros=sql_select_retrouser_dict()
    print(misretros)
    return render_template('mis_retro.html', retros=misretros)

#################################################################





####ver retro mes a mes
def sql_select_ver_mi_retro(mes,ano):
    # documento = session['numero_documento']
    documento = session.get('id_usuario')
    mes=mes
    ano=ano
    conn = get_db()
    retros = conn.execute('SELECT * FROM retroalimentacion WHERE numero_documento=? and mes=? and ano;', (documento,mes,ano)).fetchall()
    lista_retros = [ {"numero_documento": retro[0], "puntaje": retro[1], "retro": retro[2], "mes": retro[3], "ano": retro[4] } for retro in retros ]
    print(lista_retros)
    return lista_retros


@app.route('/mi_retro',methods=['GET', 'POST'])
def show_my_retro():

    form = myRetroalimentacion(request.form)

    if request.method == 'POST':
        mes = request.form['mes']
        ano = request.form['ano']
        miretro=sql_select_ver_mi_retro(mes,ano)
        print('este es mi feedback')

        if miretro is not None:
            
            print(miretro)
            return render_template('mi_retro.html',form=form)
        else:
            print('no hay feedback para ese mes')
            flash('no hay feedback para este mes')
            return render_template('mi_retro.html',form=form,miretro=miretro)
    return render_template('mi_retro.html',form=form)
     


##################################################
##################################################
def sql_select_allretro():
    # documento = session['numero_documento']
    documento = session.get('id_usuario')
    # documento = 9101112
    print(documento)
    conn = get_db()
    retros = conn.execute('SELECT * FROM retroalimentacion ').fetchall()
    lista_retros = [ {"numero_documento": retro[0], "puntaje": retro[1], "retro": retro[2], "mes": retro[3], "ano": retro[4] } for retro in retros ]
    print(lista_retros)
    return lista_retros



@app.route('/allretro')
def show_all_retros():
    all_retros=sql_select_allretro()
    print(all_retros)
    return render_template('allretro.html', allretros=all_retros)



#Editar  super #############################################################################################
@app.route('/editarusuario',methods=['GET', 'POST'])
@login_required
def editarusuario():

    if session['rol'] == 'Superadmin' or session['rol'] == 'administrador':
        form=Editarusuario(request.form)
        errores=None
                     
        if request.method == 'POST':

            if 'consultar' in request.form:
                cedula=request.form['documento']
                db = get_db()
                sqluser = db.execute("SELECT * FROM Empleados WHERE numero_documento='{}'".format(cedula)).fetchone()
                milista=sqluser
                db.commit()
                db.close()
           
                if sqluser is None:
                    flash("Dato no encontrado" )
                    
                    form=Editarusuario(request.form)
                    return render_template("editarusuario_prueba.html",form=form)
                else:
                    form.documento.data=milista[0]
                    form.nombre.data=milista[1]
                    form.apellido.data=milista[2]            
                    form.celular.data=milista[3]
                    form.email.data=milista[4]
                    form.cargo.data=milista[5]
                    form.contrato.data=milista[6]
                    form.tdocumento.data=milista[7]
                   # form.fechainicio.data=''
                   #form.fechafinalizacion.data=milista[9]
                    form.salario.data=milista[10]
                    form.contrasena.data=milista[11]
                    form.tipousuario.data=milista[12]
                    form.dependencia.data=milista[13]
                
                    
                    return render_template("editarusuario_prueba.html",form=form)
            if 'guardar' in request.form:
        ##########validacion formato########################

                passwox=form.contrasena.data
                rcontrasena=form.rcontrasena.data

                if (passwox!=rcontrasena):               
                    errores='la contrasenas no coincide'
                    print('no coincide',errores)
                
                if not validarcontrasena(passwox):
                    errores='la contrasena debe contener al menos una letra mayuscula y numero'
                    print('formato',errores)

                if not validarnumero(int(form.celular.data)):
                    errores='el telefono debe tener de 10 a 16 numeros'
                    print('formato telefono',errores)

                if not validarsalario(int(form.salario.data)):
                    errores='el valor del salario es inferior al permitido'
                    print('formato salario',errores)
                #flash('paso validaciones de formato')
                if errores is not None:
                    print(' ocurrio esto ',errores)
                    flash(errores)    
                    return render_template("editarusuario_prueba.html",form=form)
        ###############FIN VALIDACION FORMATO ###############################################
         ##cifrado            
                password_cifrado = generate_password_hash(passwox)
                db = get_db()

                     
                if errores is not None:
                    flash(errores)                                           
                    return render_template("editarusuario_prueba.html",form=form)
                

                sqltel = db.execute("SELECT * FROM Empleados WHERE telefono='{}'".format(form.celular.data)).fetchone()
                sqlcorreo = db.execute("SELECT * FROM Empleados WHERE correo='{}'".format(form.email.data)).fetchone()

                if sqltel is not None:
                    if sqltel[0]!=form.documento.data:
                        print('el telefono ya existe')
                        errores='el telefono existe ',form.documento.data

                      
                if sqlcorreo is not None:
                    if sqlcorreo[0]!=form.documento.data:
                     print('el telefono ya existe')
                     errores='email ya existe'

                if errores is not None:
                    flash(errores)                                           
                    return render_template("editarusuario_prueba.html",form=form)
                      #fin validacion de campos// pasar a funcion  
               


                if  session['rol'] == 'Superadmin':
                    ql2=db.execute("UPDATE Empleados SET nombre='{}',apellido='{}',telefono='{}',correo='{}',id_cargo='{}',contrato='{}',tdocumento='{}',fechadeinicio='{}',fechafin='{}',salario='{}',contrasena='{}',dependencia='{}' WHERE numero_documento='{}'".format(form.nombre.data,
                    form.apellido.data,form.celular.data,form.email.data,form.cargo.data,form.contrato.data,form.tdocumento.data,form.fechainicio.data,form.fechafinalizacion.data
                    ,form.salario.data,password_cifrado,form.dependencia.data,form.documento.data))
               
                else:

                    ql2=db.execute("UPDATE Empleados SET nombre='{}',apellido='{}',telefono='{}',correo='{}',id_cargo='{}',contrato='{}',fechadeinicio='{}',fechafin='{}',salario='{}',contrasena='{}',dependencia='{}' WHERE numero_documento='{}'"
                    .format(form.nombre.data,form.apellido.data,form.celular.data,form.email.data,form.cargo.data,form.contrato.data,form.fechainicio.data,form.fechafinalizacion.data,form.salario.data,password_cifrado,form.dependencia.data,request.form['documento']))



                db.commit()
                db.close()
                flash("actualizacion exitosa")
                form=Editarusuario()

               #    else:
                #        flash("actualizacion exitosa")
                #        form=Editarusuario()
                    
                                  
                return render_template("editarusuario_prueba.html",form=form)
             
        return render_template("editarusuario_prueba.html",form=form)
    else:
        return('Acceso Denegado')

######################################################################################################33


#eliminar
@app.route('/eliminar',methods=['GET','POST'])
@login_required

def eliminar():
    if session['rol'] == 'Superadmin':



        form = Buscarusuario(request.form)
        if request.method == 'POST':
            cedula=request.form['documento']
        
            error = None
            db = get_db()
            cedula=request.form['documento']
            sqluser = db.execute("SELECT * FROM Empleados WHERE numero_documento='{}'".format(cedula)).fetchone()
                
            if sqluser is None:
                flash("Dato no encontrado" )
            else:
                sql=db.execute("DELETE FROM Empleados WHERE numero_documento='{}'".format(cedula))
                db.commit()
                db.close()

                flash("el dato ha sido eliminado" )
        
        return render_template("eliminar_prueba.html",form=form)
    else:
        return ('Acceso Denegado')





@app.route('/dashboard')
@login_required
def dashboard():
        if session['rol'] == 'Superadmin':
            return render_template("dashboard.html")
        else:
            return('Acesso denegado')




@app.route('/crear_retros',methods=['GET','POST'])
@login_required
def crear_retros():
    
    if session['rol'] == 'Superadmin':
   
        form = Retroalimentacion(request.form)
        if request.method == 'POST':

            cedula=request.form['documento']
            db = get_db()
            sqluser = db.execute("SELECT * FROM Empleados WHERE numero_documento='{}'".format(cedula)).fetchone()
            milista=sqluser    
            if sqluser is None:
                flash("Dato no encontrado" )
            else:
                documento = request.form['documento']
                puntaje = request.form['puntaje']
                retroalimentacion = request.form['caja']            
                mes = request.form['mes']
                ano = request.form['ano']
                

                sqluser = db.execute("INSERT INTO retroalimentacion (numero_documento,puntaje,retro,mes,ano) VALUES (?,?,?,?,?)",
                (documento,puntaje,retroalimentacion,mes,ano))
                db.commit()
                db.close()    
                flash("feedback enviado" )
    else:
        return('Acceso Denegado')
    return render_template("crear_retros.html",form=form)



@app.route('/retro',methods=['GET','POST'])
def retro():
    if session['rol'] == 'Superadmin':


        form = Retroalimentacion(request.form)
        if request.method == 'POST':

            cedula=request.form['documento']
            db = get_db()
            sqluser = db.execute("SELECT * FROM Empleados WHERE numero_documento='{}'".format(cedula)).fetchone()
            milista=sqluser    
            if sqluser is None:
                flash("Dato no encontrado" )
            else:
                documento = request.form['documento']
                puntaje = request.form['puntaje']
                retroalimentacion = request.form['caja']            
                mes = request.form['mes']
                ano = request.form['ano']
                

                sqluser = db.execute("INSERT INTO retroalimentacion (numero_documento,puntaje,retro,mes,ano) VALUES (?,?,?,?,?)",
                (documento,puntaje,retroalimentacion,mes,ano))
                db.commit()
                db.close()    
                flash("feedback enviado" )

        return render_template("retro.html",form=form)

    else:
        return('Acceso Denegado')











###############################empleado###############################################



@app.route('/retrousuario',methods=['GET','POST'])
@login_required
def retrousuario():
    form = myRetroalimentacion(request.form)
    if request.method == 'POST':

        documento=request.form['documento']
        mes = request.form['mes']
        ano = request.form['ano']
        anos=int(ano)


        if ((anos >1900) and (anos<2100)):
            db = get_db()
           

            sqluser = db.execute('SELECT * FROM retroalimentacion WHERE numero_documento = ? and mes=? and ano=? ',
            (documento,mes,ano)).fetchone()
            print(sqluser)
            db.commit()
            db.close()
            if sqluser is None:
                flash("no hay feedback para esta fecha")
            else:  
                flash("mi puntaje es {}".format(sqluser[1]))    
                form.caja.data=sqluser[2]
                   
            return render_template("retrousuario.html",form=form)
        else:
            flash("el ano no es valido, digite un ano enter 1900 y 2100")    

            

    return render_template("retrousuario.html",form=form)



@app.route('/logout')
def logout():
    session.clear()
    return render_template("login.html")



@app.before_request
def usuario_registrado():
    idusuario = session.get('id_usuario')
    if idusuario is None:
        g.usuario=None
    else:
        g.usuario=idusuario
        db = get_db()
        sqluser = db.execute('SELECT * FROM Empleados WHERE numero_documento = ?',(idusuario,)).fetchone()
        g.rol=sqluser[12]
        db.commit()


# ADICIONALES ANTONIO

