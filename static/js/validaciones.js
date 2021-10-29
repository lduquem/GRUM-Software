

function buscarUsuario(){

    usuarioe=document.getElementById("busuario").value;
    if (usuarioe=="123456"){
        mostrarInfo()
        return false
    }else{
        alert("no se ha encontrado el usuario")
        return false
    }
}


function mostrarInfo(){
    alert("funcion mostrar info del usuario en construccion")
    textarea=document.getElementById(mostrar).value
    alert(textarea)
    



}

function eliminarUsuario(){

    usuarioe=document.getElementById("busuario").value;
    if (usuarioe=="123456"){
        alert("usuario eliminado chanchan")
        return false
    }else{
        alert("no se ha encontrado el usuario")
        return false
    }
}



function validar(){

    usuario=document.getElementById("usuario").value;
    password=document.getElementById("password").value; 
    bolita=document.getElementById("confirmar").checked;

    if (usuario==""){
        alert("el campo usuario esta vacio")
        return false
    }else if (password.length<8){
        alert("la contrasena debe contener minimo 8 caracteres")
        return false

    }else if (bolita==false){
        alert("debe aceptar las politicas de privacidad")
        return false

    }else{
        redirecionarUrl()
        return false

          
    }


}



function redirecionarUrl(){
    usuario=document.getElementById("usuario").value;
    password=document.getElementById("password").value; 


    if (usuario=="superadmin" && password=="superadmin"){
        window.location="superadmin.html";



    }else if(usuario=="admin" && password=="administrador"){
        window.location="admin.html";


    }else if(usuario=="empleado" && password=="empleado"){
        window.location="usuario.html";
    }else{
        alert("Datos errados")
    }





}