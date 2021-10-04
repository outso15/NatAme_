from http import HTTPStatus
from flask import Blueprint, Response, request, render_template, url_for, redirect, flash,jsonify
from werkzeug.wrappers import response
from connect_db import connect
#from models import User,get_user
#from app import login_manager
#from flask_login import current_user, login_user, login_required
import sys
import json 

#import pandas as pd

home = Blueprint("home", __name__, url_prefix="/home")
pago = Blueprint("pago", __name__, url_prefix="/pago")
shopCart = Blueprint("shopcart", __name__, url_prefix="/shopcart")
shopCart2 = Blueprint("shopcart2", __name__, url_prefix="/shopcart2")
shopBag = Blueprint("shopbag", __name__, url_prefix="/shopbag")
categories = Blueprint("categories", __name__, url_prefix="/categories")
login = Blueprint("login", __name__, url_prefix="/login")
register = Blueprint("register", __name__, url_prefix="/register")

RESPONSE_BODY = {"message": "", "data": [], "errors": [], "metadata": []}

dict={}

@home.route("/", methods=["GET"])
def show_product():
    
    conexion = connect()
    for datos in conexion.sentenciaCompuesta("select N_NOMCATEGORIA from categoria where K_CATEGORIA_PERTENECE is null"):
        RESPONSE_BODY["data"] += datos
    conexion.close()
    
    categoria1=RESPONSE_BODY["data"][1]
    
    return render_template('home.html',categoria1=categoria1)

@shopBag.route("/", methods=["GET"])
def show_product():
    return render_template('shopbag.html')

@pago.route("/", methods=["GET"])
def show_product():
    conexion = connect()
    consulta1 =[]
    consulta2=[]
    longitud=[]
    
    #SELECT pr.n_nomproducto, i.v_precio_unidad FROM PAIS p, REGION r, PRODUCTO pr, INVENTARIO i WHERE UPPER(p.n_nombre_pais)='COLOMBIA' AND p.k_pais=r.K_pais AND UPPER(r.n_nombre_region)='CARIBE' AND i.k_pais=r.K_pais AND i.k_region=r.k_region AND i.k_producto=pr.k_producto   
    for datos in conexion.sentenciaCompuesta(" select u.n_usuario, m.n_detalle_metodo_pago from metodo_de_pago m, cliente c, usuario u  where c.k_identificacion=m.k_identificacion_cli and u.k_identificacion='21113'and u.k_identificacion=c.k_identificacion"):
        consulta1.append(datos[0])
        consulta2.append(datos[1])
        
    
        
    print (consulta1)  
    nombre=consulta1[0]
    print  (dict)
    consulta3=[]
    #if request.method=='POST':
    for datos in conexion.sentenciaCompuesta(" select k_clienterep from representante_cliente rc, cliente c, usuario u where rc.i_tipoid_cli=c.k_tipoid and rc.q_identificacion_cli= c.k_identificacion and u.n_usuario='"+ str(nombre) + "' and c.k_tipoid=u.k_tipoid and c.k_identificacion=u.k_identificacion"):
        consulta3.append(datos[0])
    print(consulta3)

    m_pago=[]
    

    if request.method=='POST':
        dat = request.form
        for key,value in dat.items():
            #print(key," : ", value)
            if value !='Inactivo    ':
                m_pago.append(key)
                #cantidad.append(value)

    
        
    return render_template('pago.html',consulta1=nombre,consulta2=consulta2)

@shopCart.route("/", methods=["GET","POST"])
def show_product():
    '''
    #Funciona
    conexion = connect()
    consulta1 =[]
    consulta2 =[]
    
    for datos in conexion.sentenciaCompuesta("SELECT i.v_precio_unidad FROM PAIS p, REGION r, PRODUCTO pr, INVENTARIO i WHERE UPPER(p.n_nombre_pais)='COLOMBIA' AND p.k_pais=r.K_pais AND UPPER(r.n_nombre_region)='CARIBE' AND i.k_pais=r.K_pais AND i.k_region=r.k_region AND i.k_producto=pr.k_producto"):
        consulta1.append(datos[0])
      
    for datos in conexion.sentenciaCompuesta("SELECT pr.n_nomproducto FROM PAIS p, REGION r, PRODUCTO pr, INVENTARIO i WHERE UPPER(p.n_nombre_pais)='COLOMBIA' AND p.k_pais=r.K_pais AND UPPER(r.n_nombre_region)='CARIBE' AND i.k_pais=r.K_pais AND i.k_region=r.k_region AND i.k_producto=pr.k_producto"):
        consulta2.append(datos[0])
   
    categoria= {'precio':consulta1,'nombre':consulta2}
    #precio= consulta["precio"]
    longitud=[]
    for i in range(len(categoria["nombre"])):
        longitud.append(i)

    print(longitud)
    #categoria=consulta["precio"]
    return render_template('shopcart.html',categoria=categoria,longitud=longitud)
    '''
    conexion = connect()
    consulta1 =[]
    consulta2 =[]  
    consulta3 =[]
    #SELECT pr.n_nomproducto, i.v_precio_unidad FROM PAIS p, REGION r, PRODUCTO pr, INVENTARIO i WHERE UPPER(p.n_nombre_pais)='COLOMBIA' AND p.k_pais=r.K_pais AND UPPER(r.n_nombre_region)='CARIBE' AND i.k_pais=r.K_pais AND i.k_region=r.k_region AND i.k_producto=pr.k_producto   
    for datos in conexion.sentenciaCompuesta(" SELECT  pr.n_nomproducto, i.v_precio_unidad, i.K_PRODUCTO FROM PAIS p, REGION r, PRODUCTO pr, INVENTARIO i WHERE UPPER(p.n_nombre_pais)='COLOMBIA' AND p.k_pais=r.K_pais AND UPPER(r.n_nombre_region)='CARIBE' AND i.k_pais=r.K_pais AND i.k_region=r.k_region AND i.k_producto=pr.k_producto order by pr.n_nomproducto asc"):
        consulta1.append(datos[0])
        consulta2.append(datos[1])
        consulta3.append(datos[2])
    #print (consulta1)  
    categoria= {'nombre':consulta1,'precio':consulta2, 'id':consulta3}
    #precio= consulta["precio"]
    #print (categoria)
    longitud=[]
    for i in range(len(categoria["nombre"])):
        longitud.append(i)

    #print(categoria)
    #categoria=consulta["precio"]
    
    producto=[]
    cantidad=[]
    longitud_1=[]
    compra={'producto':producto,'cantidad':cantidad}
    
    if request.method=='POST':
        dat = request.form 
        for key,value in dat.items():
            #print(key," : ", value)
            if value !='0':
                producto.append(key)
                cantidad.append(value)
        
        
        print(compra)
        consulta1_1 =[]
        consulta2_1 =[]  
        consulta3_1 =[]
        consulta4_1 =[]
        
        for i in range(len(compra["producto"])):
            for datos in conexion.sentenciaCompuesta(" SELECT  pr.n_nomproducto, i.v_precio_unidad, i.K_PRODUCTO FROM PAIS p, REGION r, PRODUCTO pr, INVENTARIO i WHERE UPPER(p.n_nombre_pais)='COLOMBIA' AND p.k_pais=r.K_pais AND UPPER(r.n_nombre_region)='CARIBE' AND i.k_pais=r.K_pais AND i.k_region=r.k_region AND i.k_producto=pr.k_producto AND i.k_producto='"+ str(compra['producto'][i]) + "' order by pr.n_nomproducto asc"):
                consulta1_1.append(datos[0])
                consulta2_1.append(datos[1])
                consulta3_1.append(datos[2])
        print(consulta1_1)     
        
        
        for i in range(len(compra["producto"])):
            longitud_1.append(i)
            consulta4_1.append(int(cantidad[i])*int(consulta2_1[i]))
        
        dict['nombre']= consulta1_1
        dict['precio']= consulta2_1
        dict['id']= consulta3_1
        dict['total']= consulta4_1
        dict['longitud_1']=longitud_1
        categoria_1= {'nombre':consulta1_1,'precio':consulta2_1, 'id':consulta3_1,'total':consulta4_1}
        print(categoria_1)
        print(longitud_1)
        #consulta4_1.sum()      
        subtotal= sum(consulta4_1)
        
        return render_template('shopcart2.html',categoria_1=categoria_1,longitud_1=longitud_1,compra=compra,subtotal=subtotal)
        
    else:
        return render_template('shopcart.html',categoria=categoria,longitud=longitud)
    #return ?
    '''
    return render_template('shopcart.html',categoria=categoria,longitud=longitud)
    '''
@shopCart2.route("/", methods=["GET","POST"])
def show_product():
    producto=[]
    cantidad=[]
    compra={'producto':producto,'cantidad':cantidad}
    if request.method=='POST':
        dat = request.form 
        for key,value in dat.items():
            #print(key," : ", value)
            if value !='0':
                producto.append(key)
                cantidad.append(value)
        print(compra)
        return render_template('home.html')
    print("entro")
    return(compra)
    





######################## Metodos para las rutas de categories ######################################

@categories.route("/", methods=["GET"])
def show_product():
    conexion = connect()
    for datos in conexion.sentenciaCompuesta("select N_NOMCATEGORIA from categoria"):
        RESPONSE_BODY["data"] += datos
    conexion.close()
    categorias = RESPONSE_BODY["data"]
    return render_template('categories.html', categorias=categorias)
     
######################## Metodos para las rutas del login ######################################

@register.route("/", methods=["GET"])
def show_product():
    return render_template('register.html')

def vaciar_RESPONSE():
    RESPONSE_BODY = {"message": "", "data": [], "errors": [], "metadata": []}
'''
@login.route('/', methods=['GET'])
def login_get():
    return render_template('login.html')

@login.route('/', methods=['POST'])
def login_post():
    usuario = request.form.get('username')
    password = request.form.get('password')
    user = get_user(usuario)
    if not user or not user.check_password(password):
        flash('Por favor revisa tus credenciales e intenta de nuevo.')
        return redirect(url_for('login.login_get')) 
    login_user(user, remember=False)
    return redirect(url_for('home.show_product'))
    '''