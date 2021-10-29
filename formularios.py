from wtforms import Form, StringField,TextAreaField,IntegerField,PasswordField, BooleanField, SelectField, SubmitField,DateTimeField,TextAreaField, validators 
from wtforms.fields.html5 import EmailField
from wtforms.fields.html5 import DateField

class Crearusuario(Form):

    nombre = StringField('Nombres', [validators.DataRequired(), validators.Length(min=4,max=25)], render_kw={"class": "form-control"} )
    apellido=StringField("Apellidos",[validators.DataRequired(), validators.Length(min=4,max=25)], render_kw={"class": "form-control"} )
    tdocumento=SelectField("Tipo de documento",choices=[("Cédula de ciudadanía","Cédula de ciudadanía"),("Cédula de extranjería","Cédula de extranjería"),("Pasaporte","Pasaporte")], render_kw={"class": "form-control"})
    documento=IntegerField("Número de documento:",[validators.DataRequired(), validators.Length(min=8,max=12)], render_kw={"class": "form-control"} )
    email=EmailField("Correo electrónico",[validators.DataRequired(), validators.Email()], render_kw={"class": "form-control"})
    celular=IntegerField("Celular",[validators.DataRequired(), validators.Length(min=8,max=12)], render_kw={"class": "form-control"})
    contrato=SelectField("Tipo de contrato",choices=[("Término indefinido","Término indefinido"),("Término fijo","Término fijo"),("Obra labor","Obra labor")], render_kw={"class": "form-control"})
    cargo=SelectField("Cargo",choices=[("Gerente general","Gerente general"),("Director de producción","Director de producción"),("Coordinador de operaciones","Coordinador de operaciones"), ("Operario de producción", "Operario de producción"), ("Director comercial", "Director comercial"), ("Ejecutivo comercial", "Ejecutivo comercial")], render_kw={"class": "form-control"})
    dependencia=SelectField("Dependencia",choices=[("Administración","Administración"),("Producción","Producción"),("Comercial","Comercial"), ("Logística", "Logística")], render_kw={"class": "form-control"})
    salario=IntegerField("Salario",[validators.DataRequired('Dato requerido.')], render_kw={"class": "form-control"})
    tipousuario=SelectField("Rol",choices=[("Superadmin","Superadministrador"),("administrador","Administrador"),("empleado","Empleado")], render_kw={"class": "form-control"})
    contrasena=PasswordField("Contraseña",[validators.DataRequired('Dato requerido.'), validators.Length(min=8,max=24)], render_kw={"type": "password", "class": "form-control"})
    rcontrasena=PasswordField("Confirmar contraseña:",[validators.DataRequired('Dato requerido.'), validators.Length(min=8,max=24)], render_kw={"type": "password", "class": "form-control"} )
    fechainicio=DateField("Fecha de inicio", render_kw={"class": "form-control"})
    fechafinalizacion=DateField("Fecha de terminación", render_kw={"class": "form-control"})
    enviar=SubmitField("Guardar", render_kw={"class": "btn btn-block btn-outline-primary btn-lg"})

class Editarusuario(Form):

    nombre=StringField("Nombres", render_kw={"class": "form-control"})
    apellido=StringField("Apellidos", render_kw={"class": "form-control"})
    tdocumento=SelectField("Tipo de documento",choices=[("cedula","cedula"),("nit","nit"),("pasaporte","pasaporte")], render_kw={"class": "form-control"})
    documento=StringField("Número de documento", render_kw={"class": "form-control"})
    email=EmailField("Correo electrónico", render_kw={"class": "form-control"})
    celular=StringField("Teléfono", render_kw={"class": "form-control"})
    contrato=SelectField("Tipo de contrato",choices=[("indefinido","indefinido"),("termino fijo","termino fijo"),("prestacion de servicio","prestacion de servicio")], render_kw={"class": "form-control"})
    cargo=SelectField("Cargo",choices=[("cargo1","cargo1"),("cargo2","cargo2"),("cargo3","cargo3")], render_kw={"class": "form-control"})
    dependencia=SelectField("Dependencia",choices=[("dependencia1"),("dependencia2"),("dependencia3")], render_kw={"class": "form-control"})
    salario=StringField("Salario", render_kw={"class": "form-control"})
    tipousuario=SelectField("Rol",choices=[("Superadmin","Superadmin"),("administrador","administrador"),("empleado","empleado")], render_kw={"class": "form-control"})
    contrasena=PasswordField("Contraseña:", render_kw={"class": "form-control"})
    rcontrasena=PasswordField("Confirmar contraseña:", render_kw={"class": "form-control"})
    fechainicio=DateField("Fecha de inicio", render_kw={"class": "form-control"})
    fechafinalizacion=DateField("Fecha de terminación", render_kw={"class": "form-control"})

    guardar=SubmitField("Actualizar", render_kw={"class": "btn btn-block btn-outline-primary btn-lg"})
    consultar=SubmitField("Consultar", render_kw={"class": "btn btn-block btn-outline-primary btn-lg"})







class Login(Form):
    usuario = IntegerField('Documento',
    [ 
        validators.DataRequired(message='Dato requerido.'), 
        validators.Length(min=4,max=25,message="el usuario debe tener minimo 4 caracteres")
    ], render_kw={"class": "form-control"})  
    password = PasswordField('Contraseña',
    [ 
        validators.DataRequired(message='Dato requerido.'), 
        validators.Length(min=8,max=25,message="contrasena debe tener minimo 8 caracteres")
    ], render_kw={"class": "form-control"})
    enviar = SubmitField('Iniciar sesión', render_kw={"class": "btn btn-outline-primary btn-lg"})


class Retroalimentacion(Form):

    documento=StringField('Ingrese el Documento ',[validators.DataRequired(),validators.Length(max=20)])
    puntaje=IntegerField('Ingrese puntaje entre 1-10 ',[validators.DataRequired(),validators.Length(min=1,max=2)])
    mes=SelectField("mes",choices=[("enero","enero"),("febrero","febrero"),("marzo","marzo"),("abril","abril"),("mayo","mayo"),("junio","junio"),("julio","julio"),
    ("agosto","agosto"),("septiembre","septiembre"),("octubre","octubre"),("noviembre","noviembre")
    ,("diciembre","diciembre")])
    ano=IntegerField("ano",[validators.DataRequired(),validators.Length(min=4,max=4)])
    caja = TextAreaField(u'Ingrese el feedback',[validators.DataRequired()])
    enviar=SubmitField('Enviar')


class Buscarusuario(Form):
    documento=StringField("Número de documento", render_kw={"class": "form-control"})
    buscar=SubmitField("Eliminar", render_kw={"class": "btn btn-block btn-outline-primary btn-lg"})


class myRetroalimentacion(Form):

    documento=StringField('mi documento ')
    puntaje=IntegerField('mi puntaje ')
#    mes=StringField("Seleccione mes ",[validators.DataRequired(),validators.Length(min=4,max=4)])
    mes=SelectField("seleccione mes",choices=[("enero","enero"),("febrero","febrero"),("marzo","marzo"),("abril","abril"),("mayo","mayo"),("junio","junio"),("julio","julio"),
    ("agosto","agosto"),("septiembre","septiembre"),("octubre","octubre"),("noviembre","noviembre")
    ,("diciembre","diciembre")])
    ano=IntegerField("digite ano")
    caja = TextAreaField(u'mi feedback')
    enviar=SubmitField('Enviar')


