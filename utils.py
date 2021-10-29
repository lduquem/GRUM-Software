from os import register_at_fork
import datetime
import re
from validate_email import validate_email

pass_reguex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&.])[A-Za-z\d@$!%*?&.]{8,}$"
user_reguex = "^[a-zA-Z0-9_.-]+$"
F_ACTIVE = 'ACTIVE'
F_INACTIVE = 'INACTIVE'
EMAIL_APP = 'EMAIL_APP'
REQ_ACTIVATE = 'REQ_ACTIVATE'
REQ_FORGOT = 'REQ_FORGOT'
U_UNCONFIRMED = 'UNCONFIRMED'
U_CONFIRMED = 'CONFIRMED'


def isEmailValid(email):
    #error = 'Correo invalido'
    is_valid = validate_email(email)

    return is_valid


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



def validarfecha(fecha1,fecha2):

    if fecha1 > fecha2:
        return False
    return True


   # f1=str(fecha1.split('-'))
   # f2=str(fecha2.split('-'))
    
   # if f1[0]>f2[0]:
    #    return False

    #elif f1[0]==f2[0]:

     #   if f1[1]>f2[1]:
     #       return False
    
   # elif f1[1]==f2[1]:

    #    if f1[2]>f2[2]:
     #       return False
    #else:
     #   return True










            















   
    pass

