import random
from datetime import datetime, timedelta
import mysql.connector
from faker import Faker

# Conexión a la DB
connection = mysql.connector.connect(
    user='root',
    password='admin',
    host='mysql-db',
    port=3306,
    database='corporacionDB'
)

#Curso para ejecutar las queries
cursor=connection.cursor()

#Generador Faker
fake = Faker('es_AR')

#CAMBIAR: Cantidad de registros de empleados a generar
cantidad_empleados = 1000

def generar_categorias():
    categorias = [
        ('Junior', 'Resolución 101'),
        ('Semi-Senior', 'Resolución 102'),
        ('Senior', 'Resolución 103'),
        ('Trainee', 'Resolución 104'),
        ('Jefe de Área', 'Resolución 105'),
        ('Coordinador', 'Resolución 106'),
        ('Gerente', 'Resolución 107'),
        ('Director', 'Resolución 108'),
        ('Asistente Administrativo', 'Resolución 109'),
        ('Especialista', 'Resolución 110'),
    ]
    
    for nombre, resolucion in categorias:
        cursor.execute("INSERT INTO categoria (nombre, resolucion) VALUES (%s, %s)", (nombre, resolucion))
    
    connection.commit()

def generar_funciones():
    funciones = [
        ('Desarrollador Frontend', 'Resolución 201'),
        ('Desarrollador Backend', 'Resolución 202'),
        ('Analista de Datos', 'Resolución 203'),
        ('Diseñador UX/UI', 'Resolución 204'),
        ('Ejecutivo de Ventas', 'Resolución 205'),
        ('Representante de Atención al Cliente', 'Resolución 206'),
        ('Coordinador de Proyectos', 'Resolución 207'),
        ('Contador', 'Resolución 208'),
        ('Especialista en Marketing Digital', 'Resolución 209'),
        ('Ingeniero de Redes', 'Resolución 210'),
        ('Jefe de Producción', 'Resolución 211'),
        ('Consultor de Recursos Humanos', 'Resolución 212'),
        ('Analista Financiero', 'Resolución 213'),
        ('Supervisor de Logística', 'Resolución 214'),
        ('Gerente de Desarrollo de Producto', 'Resolución 215'),
    ]
    
    for nombre, resolucion in funciones:
        cursor.execute("INSERT INTO funcion (nombre, resolucion) VALUES (%s, %s)", (nombre, resolucion))
    
    connection.commit()
    
def generar_departamentos():
    departamentos = [
        ('Recursos Humanos',),
        ('Administración',),
        ('Finanzas',),
        ('Desarrollo de Software',),
        ('Atención al Cliente',),
        ('Marketing',),
        ('Ventas',),
        ('Producción',),
        ('Investigación y Desarrollo (I+D)',),
        ('Logística',),
    ]
    
    for (nombre,) in departamentos:
        cursor.execute("INSERT INTO departamento (nombre) VALUES (%s)", (nombre,))
    
    connection.commit()

# Generador de registros de domicilio 
def generate_domicilio():
    calle = fake.street_name()
    numero = fake.building_number()
    barrio = fake.city()
    localidad = fake.city()
    provincia = fake.province()
    
    # Formatear la consulta SQL para su impresión
    query = """
    INSERT INTO domicilio (calle, numero, barrio, localidad, provincia)
    VALUES (%s, %s, %s, %s, %s)
    """
    values = (calle, numero, barrio, localidad, provincia)
    
    # Imprimir la consulta en la consola para depuración
    # print(query % values)
    
    # Ejecutar la consulta
    cursor.execute(query, values)
    connection.commit()
    
    # Retornar el ID del domicilio generado
    return cursor.lastrowid


# Generador de registros de ficha médica
def generate_ficha_medica():
    fecha_creacion = fake.date_between(start_date='-1y', end_date='today')
    grupo_sanguineo = random.choice(['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-'])
    alergias = fake.text(max_nb_chars=200)
    antecedentes = fake.text(max_nb_chars=500)
    
    # Formatear la consulta SQL para su impresión
    query = """
    INSERT INTO fichaMedica (fecha_creacion, grupo_sanguineo, alergias, antecedentes)
    VALUES (%s, %s, %s, %s)
    """
    values = (fecha_creacion, grupo_sanguineo, alergias, antecedentes)
    
    # Imprimir la consulta en la consola para depuración
    # print(query % values)
    
    # Ejecutar la consulta
    cursor.execute(query, values)
    connection.commit()
    
    # Retornar el ID de la ficha médica generada
    return cursor.lastrowid


# Generador de datos personales
def generate_datos_personales():
    dni = fake.unique.random_number(digits=8)
    apellido = fake.last_name()
    nombre = fake.first_name()
    fecha_nacimiento = fake.date_of_birth(minimum_age=20, maximum_age=55)
    cuil = int(f"20{dni}{random.randint(0, 9)}")
    sexo = random.choice(['M', 'F', 'X'])
    estado_civil = random.choice(['Soltero/a', 'Casado/a', 'Divorciado/a', 'Viudo/a', 'Separado/a'])
    nivel_estudio = random.choice(['Primario', 'Secundario', 'Terciario', 'Universitario', 'Posgrado', 'Ninguno'])
    nacionalidad = fake.country()
    
    # Generar domicilio y ficha médica previamente
    domicilio_id = generate_domicilio()
    ficha_medica_id = generate_ficha_medica()

    # Formatear la consulta SQL para su impresión
    query = """
    INSERT INTO datosPersonales (
        dni, apellido, nombre, fecha_nacimiento, cuil, sexo, estado_civil, 
        nivel_estudio, nacionalidad, domicilio_id, ficha_medica_id
    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (dni, apellido, nombre, fecha_nacimiento, cuil, sexo, estado_civil, 
              nivel_estudio, nacionalidad, domicilio_id, ficha_medica_id)

    # Imprimir la consulta en la consola para depuración
    # print(query % values)

    # Ejecutar la consulta
    cursor.execute(query, values)
    connection.commit()
    
    # Retornar el ID de los datos personales generados
    return cursor.lastrowid

# Generador de Expediente
def generate_expediente():
    legajo = fake.unique.random_int(min=1000, max=9999)
    num_exp = fake.unique.random_int(min=1, max=100000)
    libro = fake.word().capitalize()
    tomo = fake.word().capitalize()
    fajos = random.randint(1, 20)
    
    # Formatear la consulta SQL para su impresión
    query = """
    INSERT INTO expediente (legajo, num_exp, libro, tomo, fajos) 
    VALUES (%s, %s, %s, %s, %s)
    """
    values = (legajo, num_exp, libro, tomo, fajos)

    # Imprimir la consulta en la consola para depuración
    #print(query % values)
    
    # Ejecutar la consulta
    cursor.execute(query, values)
    connection.commit()
    
    # Retornar el ID del expediente generado
    return cursor.lastrowid

# Generador de designacion
# Es necesario pasar el id de la novedad que marque el ingreso del empleado.
def generate_designacion(nov_id, fecha_ingreso):
    categoria_id = random.randint(1, 10)
    funcion_id = random.randint(1, 15)
    departamento_id = random.randint(1, 10)
    fecha_designacion = fecha_ingreso
    
    # Formatear la consulta SQL para su impresión
    query = """
    INSERT INTO designacion (categoria_id, funcion_id, departamento_id, fecha_designacion, novedad_id) 
    VALUES (%s, %s, %s, %s, %s)
    """
    values = (categoria_id, funcion_id, departamento_id, fecha_designacion, nov_id)

    # Imprimir la consulta en la consola para depuración
    #(query % values)
    
    # Ejecutar la consulta
    cursor.execute(query, values)
    connection.commit()
    
    # Retornar el ID de la designación generada
    return cursor.lastrowid

#Generar tardanza para un empleado dado su expediente
def generate_tardanza(exp_id):
    fecha_hora=fake.date_time_between(start_date='-60d', end_date='now')
    
    query = """
    INSERT INTO tardanza (exp_id, fecha_hora) 
    VALUES (%s, %s)
    """
    cursor.execute(query, (exp_id, fecha_hora))
    
    #print(query % (exp_id, fecha_hora))
    
    connection.commit()
    
#Generar ausencia para un empleado dado su expediente
def generate_ausencia(exp_id):
    fecha=fake.date_between(start_date='-60d', end_date='now')
    
    query = """
    INSERT INTO ausencia (exp_id, fecha) 
    VALUES (%s, %s)
    """
    #print(query % (exp_id, fecha))
    
    cursor.execute(query, (exp_id, fecha)) 
    categoria_id = random.randint(1, 10)
    funcion_id = random.randint(1, 15)
    departamento_id = random.randint(1, 10)
    
    connection.commit()  

#Generar un ascenso aleatorio para un empleado desde su fecha de ingreso
def generate_ascenso(exp_id, des_id, fecha_ingreso):
    #Generar la novedad con la información del ascenso
    tipo='Ascenso'
    fecha_emision = fake.date_between(start_date=fecha_ingreso, end_date='today')
    
    query = """
    INSERT INTO novedad (exp_id, tipo, fecha_emision) 
    VALUES (%s, %s, %s)
    """
    values = (exp_id, tipo, fecha_emision)
    
    #print(query % values)
    cursor.execute(query, values)
    
    connection.commit()
    
    #Generar el cambio de designacion
    nov_id = cursor.lastrowid
    
    categoria_id = random.randint(1, 10)
    funcion_id = random.randint(1, 15)
    departamento_id = random.randint(1, 10)
    
    query = """
    UPDATE designacion 
    SET categoria_id=%s, funcion_id=%s, departamento_id=%s, fecha_designacion=%s, novedad_id=%s 
    WHERE des_id=%s
    """
    values = (categoria_id, funcion_id, departamento_id, fecha_emision, nov_id, des_id)
    
    #print(query % values)
    cursor.execute(query, values)
    
    connection.commit()

#Generar un cambio aleatorio de departamento y categoria a un empleado por expediente
def generate_transferencia(exp_id, des_id, fecha_ingreso):
    #Generar la novedad con la información de la transferencia
    tipo='Transferencia'
    fecha_emision = fake.date_between(start_date=fecha_ingreso, end_date='today')
    
    query = """
    INSERT INTO novedad (exp_id, tipo, fecha_emision) 
    VALUES (%s, %s, %s)
    """
    values = (exp_id, tipo, fecha_emision)
    
    #print(query % values)
    cursor.execute(query, values)
    
    connection.commit()
    
    #Generar el cambio de designacion
    nov_id = cursor.lastrowid
    
    categoria_id = random.randint(1, 10)
    departamento_id = random.randint(1, 10)
    
    query = """
    UPDATE designacion 
    SET categoria_id=%s, departamento_id=%s, fecha_designacion=%s, novedad_id=%s 
    WHERE des_id = %s
    """
    values = (categoria_id, departamento_id, fecha_emision, nov_id, des_id)
    
    #print(query % values)
    cursor.execute(query, values)
    
    connection.commit()

# Generador de empleados
def generate_empleado():
    # Generar datos personales
    datos_personales_id = generate_datos_personales()
    
    # Generar expediente
    expediente_id = generate_expediente()

    fecha_ingreso = fake.date_between(start_date='-5y', end_date='today')
    
    # Generar novedad de ingreso al trabajo
    novedad_query = """
    INSERT INTO novedad (exp_id, tipo, fecha_emision, observaciones)
    VALUES (%s, 'Ingreso', %s, 'Ingreso inicial del empleado a la compañía.')
    """
    cursor.execute(novedad_query, (expediente_id, fecha_ingreso))
    
    # Imprimir la consulta de novedad
    #print(novedad_query % (expediente_id, fecha_ingreso))
    
    # Obtener el ID de la última novedad ingresada
    nov_id = cursor.lastrowid
    
    # Generar designación con la novedad generada y el expediente del empleado
    designacion_id = generate_designacion(nov_id, fecha_ingreso)
    
    horario_trabajo = fake.time(pattern="%H:%M:%S")
    
    turno = random.choice(['Part-time', 'Full-time', 'Temporal'])
    
    # Generar el registro del empleado (aquí agregamos la inserción del empleado)
    empleado_query = """
    INSERT INTO empleado (datos_personales_id, expediente_id, designacion_id ,horario_trabajo, turno, fecha_ingreso)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    
    # Imprimir la consulta del empleado
    #print(empleado_query % (datos_personales_id, expediente_id, designacion_id , horario_trabajo, turno, fecha_ingreso))
    
    cursor.execute(empleado_query, (datos_personales_id, expediente_id, designacion_id , horario_trabajo, turno, fecha_ingreso))
    
    # Confirmar los cambios en la base de datos
    connection.commit()
    
    empleado_id = cursor.lastrowid
    
    print(f"Generado empleado n°. {empleado_id}")
    
    # Por empleado generado, vamos a generar entre 0 a 8 tardanzas para el ultimo es
    cantidadTardanzas = random.randint(-3, 8) # Quiero que haya más posibilidades de que el empleado no tenga tardanzas a que sí tenga
    if(cantidadTardanzas >= 1):
        for _ in range(cantidadTardanzas):
            print(f"Tardanza {_}")
            generate_tardanza(expediente_id)
    
    # Por empleado generado, vamos a generar entre 0 a 5 ausencias para el último mes
    cantidadAusencias = random.randint(-3,5)
    if(cantidadAusencias >=1):
        for _ in range(cantidadAusencias):
            print(f"Ausencia {_}")
            generate_ausencia(expediente_id)
    
    # Por empleado generado, habra una posibilidad de 1 en 10 que haya ascendido entre 1 a 2 veces desde su ingreso
    chancesAscenso = random.randint(1,10)
    if(chancesAscenso == 1):
        cantidadAscensos = random.randint(1,2)
        for _ in range(cantidadAscensos):
            print(f"Ascenso {_}")
            generate_ascenso(expediente_id, designacion_id, fecha_ingreso)    
    
    # Por empleado generado, habra una posibilidad de 1 en 15 de que haya sido transferido de departamente desde su ingreso
    chancesTransferencia = random.randint(1,15)
    if(chancesTransferencia == 1):
        print(f"Transferencia")
        generate_transferencia(expediente_id, designacion_id, fecha_ingreso)
    

   

    
 
generar_categorias()
generar_departamentos()
generar_funciones()
    
for _ in range(cantidad_empleados):
    generate_empleado()
    
#Cerrar la conexión
connection.close()

