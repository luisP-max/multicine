import datetime   # Se importa datetime porque necesitamos obtener la fecha y hora exacta de cada compra

validar_asiento = lambda codigo: (             # Se usa lambda para tener al menos una función
    len(codigo) == 2 and                       # len() verifica que el código del asiento tenga exactamente 2 caracteres
    codigo[0] in "ABCD" and                    # codigo[0] toma la primera letra y verifica que sea A, B, C o D
    codigo[1].isdigit() and                    # .isdigit() verifica que el segundo carácter sea un número
    1 <= int(codigo[1]) <= 9                   # int() convierte el número a entero y verifica que esté entre 1 y 9
)

# FUNCIÓN: crear_sala()

def crear_sala():
    """
    Crea el diccionario con todos los asientos y su estado inicial.
    """
    sala = {}                     # Se crea un diccionario vacío porque es la forma más fácil de guardar asientos con su estado

    # Columna 1 
    sala["A1"] = "X"; sala["A2"] = "X"; sala["A3"] = " "   # Se usan ; para poner varias asignaciones en una misma línea
    sala["B1"] = " "; sala["B2"] = "-"; sala["B3"] = " "
    sala["C1"] = " "; sala["C2"] = " "; sala["C3"] = " "
    sala["D1"] = "X"; sala["D2"] = " "; sala["D3"] = " "

    # Columna 2
    sala["A4"] = " "; sala["A5"] = " "; sala["A6"] = " "
    sala["B4"] = " "; sala["B5"] = " "; sala["B6"] = " "
    sala["C4"] = " "; sala["C5"] = "-"; sala["C6"] = " "
    sala["D4"] = " "; sala["D5"] = " "; sala["D6"] = " "

    # Columna 3
    sala["A7"] = "-"; sala["A8"] = " "; sala["A9"] = " "
    sala["B7"] = " "; sala["B8"] = " "; sala["B9"] = " "
    sala["C7"] = " "; sala["C8"] = " "; sala["C9"] = " "
    sala["D7"] = " "; sala["D8"] = " "; sala["D9"] = " "

    return sala                   # Se retorna el diccionario para poder usarlo en todas las demás funciones

def mostrar_sala(sala):
    """
    Recibe el diccionario de la sala y devuelve el dibujo listo para imprimir.
    """
    dibujo = []                                    # Lista vacía para ir guardando cada línea del dibujo

    # Líneas de encabezado
    dibujo.append("                1     2     3           4     5     6           7     8     9")
    dibujo.append("             Columna 1                 Columna 2                 Columna 3")
    
    filas = ["A", "B", "C", "D"]                   # Lista con las filas
    
    for f in filas:                                # for recorre cada letra de fila (A, B, C, D)
        linea = f + "      "                       # Se concatena la letra de la fila + espacios para alinear
        for num in range(1, 10):                   # range(1,10) genera números del 1 al 9 (no incluye el 10)
            asiento = f + str(num)                 # str(num) convierte el número a texto para formar "A1", "A2", etc.
            estado = sala[asiento]                 # Se busca el estado del asiento en el diccionario
            linea += f"[{estado}] "                # f-string se usa porque es más legible y permite insertar variables fácilmente
            if num % 3 == 0:                       # % es operador módulo. Cada 3 asientos (fin de columna) se agrega espacio
                linea += "      "                  # Espacio grande para separar visualmente las 3 columnas
        dibujo.append(linea.rstrip())              # .rstrip() elimina espacios en blanco del final de la línea
    return "\n".join(dibujo)                       # .join() une todas las líneas con salto de línea

def esta_libre(sala, asiento):
    """
    Verifica si un asiento está disponible.
    """
    if asiento in sala and sala[asiento] == " ":   # 'in' verifica si la clave existe y == compara el valor
        return True
    return False

def son_continuos_y_libres(sala, lista_asientos):
    for asiento in lista_asientos:                 # Recorremos cada asiento que escribió el usuario
        if not validar_asiento(asiento):           # 'not' niega el resultado de la lambda
            return False, "Formato de asiento incorrecto. Usa A1, B2, etc."
    
    for asiento in lista_asientos:
        if not esta_libre(sala, asiento):
            return False, "Uno o más asientos ya están ocupados o inhabilitados"
    
    if len(lista_asientos) == 1:                   # len() devuelve cuántos elementos tiene la lista
        return True, "OK"
    
    primera_fila = lista_asientos[0][0]            # [0] toma el primer asiento y [0] toma su primera letra (la fila)
    for asiento in lista_asientos:
        if asiento[0] != primera_fila:             # != significa "diferente de"
            return False, "Todos los asientos deben estar en la misma fila"
    
    numeros = [int(asiento[1]) for asiento in lista_asientos]  # List comprehension: extrae el número de cada asiento
    numeros.sort()                                 # .sort() ordena la lista de números de menor a mayor
    if numeros[-1] - numeros[0] + 1 != len(numeros):  # numeros[-1] es el último elemento
        return False, "Los asientos deben ser continuos, sin dejar espacios libres entre ellos"
    
    return True, "OK"

def ocupar_asientos(sala, lista_asientos):
    """
    Marca los asientos seleccionados como ocupados ('X').
    """
    nueva_sala = sala.copy()                       # .copy() crea una copia para no modificar la sala original
    for asiento in lista_asientos:
        if asiento in nueva_sala:                  # Verificamos que el asiento exista antes de cambiarlo
            nueva_sala[asiento] = "X"
    return nueva_sala

def buscar_asientos_automaticos(sala, cantidad):
    """
    Asignación automática de asientos continuos.
    """
    filas = ["A", "B", "C", "D"]
    for f in filas:
        for inicio in range(1, 10 - cantidad + 2): # 10 - cantidad + 2 calcula hasta dónde puede empezar un bloque
            bloque = [f + str(inicio + i) for i in range(cantidad)]  # List comprehension para crear el bloque
            if all(esta_libre(sala, asiento) for asiento in bloque): # all() verifica que TODOS sean libres
                return bloque
    return []

def registrar_cliente(lista_clientes, id_cliente, nombre):
    """
    Registra un nuevo cliente
    """
    for c in lista_clientes:
        if c["id"] == id_cliente:                  # == compara si el ID ya existe
            return lista_clientes
    nuevo = {"id": id_cliente, "name": nombre}     # Diccionario con los datos del cliente
    lista_clientes.append(nuevo)                   # .append() agrega el nuevo cliente a la lista
    return lista_clientes

def buscar_cliente(lista_clientes, id_cliente):
    """
    Busca un cliente por su ID.
    """
    for c in lista_clientes:
        if c["id"] == id_cliente:
            return c
    return None                                    # None se retorna cuando no se encuentra el cliente

def guardar_compra(lista_compras, id_cliente, lista_asientos, fecha_hora):
    """
    Guarda una compra realizada
    """
    compra = {"client_id": id_cliente, "seats": lista_asientos, "date": fecha_hora}
    lista_compras.append(compra)
    return lista_compras

def mostrar_entradas_vendidas(lista_compras, lista_clientes):
    """
    Devuelve las entradas vendidas con nombre del cliente
    """
    resultado = []
    for compra in lista_compras:
        nombre = "Desconocido"
        for cliente in lista_clientes:
            if cliente["id"] == compra["client_id"]:
                nombre = cliente["name"]
                break
        info = {"client": nombre, "seats": ", ".join(compra["seats"]), "date": compra["date"]}  # ", ".join() une los asientos con coma
        resultado.append(info)
    return resultado

# ========================================================
# FUNCIÓN: generar_reporte(sala, lista_compras, lista_clientes)
# ========================================================
def generar_reporte(sala, lista_compras, lista_clientes):
    """
    Genera el reporte de ocupación de la sala 
    """
    total = len(sala)                              # len(sala) cuenta cuántos asientos hay en total
    disponibles = sum(1 for v in sala.values() if v == " ")  # sum() + generador cuenta asientos libres
    ocupados = sum(1 for v in sala.values() if v == "X")
    if (ocupados + disponibles) > 0:
        porcentaje = round((ocupados * 100) / (ocupados + disponibles), 2)  # round(..., 2) deja 2 decimales
    else:
        porcentaje = 0
    compradores = []
    for compra in lista_compras:
        for cliente in lista_clientes:
            if cliente["id"] == compra["client_id"] and cliente["name"] not in compradores:
                compradores.append(cliente["name"])
    compradores.sort(key=lambda n: n.lower())      # .sort() con lambda ordena sin distinguir mayúsculas/minúsculas
    reporte = {
        "total_seats": total,
        "available": disponibles,
        "occupied": ocupados,
        "disabled": total - disponibles - ocupados,
        "occupation_percentage": porcentaje,
        "clients_who_bought": compradores
    }
    return reporte

def main():
    """
    Función principal que controla todo el programa (menú y flujo).
    """
    sala = crear_sala()          # Llamamos a la función para crear la sala al inicio
    clientes = []                # Lista vacía de clientes
    compras = []                 # Lista vacía de compras
    
    print("=== SISTEMA DE MULTICINES RIWIFILMS ===")
    print("¡BIENVENIDOS!\n")
    
    continuar = True             # Bandera booleana para controlar el bucle
    
    while continuar:             # Bucle que se repite mientras continuar sea True
        print("\n--- MENÚ ---")
        print("1. Registrar cliente")
        print("2. Ver sala")
        print("3. Comprar entradas")
        print("4. Ver entradas vendidas")
        print("5. Ver reporte")
        print("6. Salir")
        
        opcion = input("Elige una opción (1-6): ").strip()   # .strip() elimina espacios al inicio y final que ponga el usuario
        
        if opcion == "1":
            print("\n--- REGISTRAR CLIENTE ---")
            idc = input("ID del cliente: ").strip()          # .strip() limpia espacios
            if idc == "" or not idc.isdigit():               # .isdigit() verifica que solo sean números
                print("Error: El ID solo puede tener números (sin letras ni espacios)")
                continue
            nom = input("Nombre del cliente: ").strip()
            if nom == "" or not nom.replace(" ", "").isalpha():  # .replace(" ", "") quita espacios para verificar solo letras
                print("Error: El nombre solo puede tener letras y espacios")
                continue
            clientes = registrar_cliente(clientes, idc, nom)
            print(f"Cliente guardado correctamente → ID: {idc} | Nombre: {nom}")  # f-string para insertar variables fácilmente
            
        elif opcion == "2":
            print(mostrar_sala(sala))
        
        elif opcion == "3":
            idc = input("ID del cliente: ").strip()
            cliente = buscar_cliente(clientes, idc)
            if cliente is None:                              # is None verifica si no encontró el cliente
                print("Cliente no encontrado. Regístralo primero.")
                continue
            try:
                cant = int(input("¿Cuántos asientos quieres comprar? "))  # int() convierte texto a número
                if cant < 1:
                    print("La cantidad debe ser mayor a 0")
                    continue
            except:
                print("Por favor escribe solo un número")
                continue
            auto = input("¿Asignación automática? (s/n): ").strip().lower()  # .lower() convierte a minúscula para aceptar S o s
            if auto == "s":
                asientos = buscar_asientos_automaticos(sala, cant)
                if len(asientos) == 0:
                    print("No hay espacio contiguo para esa cantidad.")
                    continue
                print("Asientos automáticos:", ", ".join(asientos))
            else:
                print(mostrar_sala(sala))
                texto = input("Escribe los asientos (ej: A1,A2,A3): ").strip().upper()  # .upper() convierte a mayúsculas
                asientos = [x.strip() for x in texto.split(",") if x.strip()]  # List comprehension + split() para separar por coma
            if len(asientos) != cant:
                print(f"Debes escribir exactamente {cant} asientos.")
                continue
            ok, msg = son_continuos_y_libres(sala, asientos)
            if ok:
                sala = ocupar_asientos(sala, asientos)
                fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  # strftime da formato de fecha y hora
                compras = guardar_compra(compras, idc, asientos, fecha_hora)
                print("¡COMPRA REALIZADA!")
                print("Cliente:", cliente["name"])
                print("Asientos:", ", ".join(asientos))
                print("Fecha y hora:", fecha_hora)
            else:
                print("Error:", msg)
        
        elif opcion == "4":
            entradas = mostrar_entradas_vendidas(compras, clientes)
            if len(entradas) == 0:
                print("No hay entradas vendidas todavía.")
            else:
                print("\nENTRADAS VENDIDAS:")
                for e in entradas:
                    print("Cliente:", e["client"])
                    print("Asientos:", e["seats"])
                    print("Fecha y hora:", e["date"])
                    print("---")
        
        elif opcion == "5":
            rep = generar_reporte(sala, compras, clientes)
            print("\nREPORTE DE OCUPACIÓN")
            print("Total asientos:", rep["total_seats"])
            print("Disponibles:", rep["available"])
            print("Ocupados:", rep["occupied"])
            print("Inhabilitados:", rep["disabled"])
            print("Porcentaje ocupación:", rep["occupation_percentage"], "%")
            print("Clientes que compraron:")
            if len(rep["clients_who_bought"]) == 0:
                print("Ninguno todavía")
            else:
                for nombre in rep["clients_who_bought"]:
                    print(" -", nombre)
        
        elif opcion == "6":
            print("¡Gracias por usar el sistema!")
            continuar = False               # Cambiamos la bandera a False para salir del bucle
        
        else:
            print("Opción incorrecta, intenta de nuevo.")

if __name__ == "__main__":     # Esta condición asegura que main() solo se ejecute cuando se corre este archivo directamente
    main()
