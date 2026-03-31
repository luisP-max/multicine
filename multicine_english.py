import datetime   # Imported because we need to get the exact date and time of each purchase

validar_asiento = lambda codigo: (             # Lambda is used because the PDF requires at least one lambda function
    len(codigo) == 2 and                       # len() checks that the seat code has exactly 2 characters
    codigo[0] in "ABCD" and                    # codigo[0] takes the first letter and checks it is A, B, C or D
    codigo[1].isdigit() and                    # .isdigit() checks that the second character is a number
    1 <= int(codigo[1]) <= 9                   # int() converts the number and checks it is between 1 and 9
)

# FUNCTION: crear_sala()

def crear_sala():
    """
    Creates the dictionary with all seats and their initial state.
    """
    sala = {}                     # An empty dictionary is created because it is the easiest way to store seats with their status

    # Column 1 
    sala["A1"] = "X"; sala["A2"] = "X"; sala["A3"] = " "   # Semicolon is used to put multiple assignments on the same line
    sala["B1"] = " "; sala["B2"] = "-"; sala["B3"] = " "
    sala["C1"] = " "; sala["C2"] = " "; sala["C3"] = " "
    sala["D1"] = "X"; sala["D2"] = " "; sala["D3"] = " "

    # Column 2
    sala["A4"] = " "; sala["A5"] = " "; sala["A6"] = " "
    sala["B4"] = " "; sala["B5"] = " "; sala["B6"] = " "
    sala["C4"] = " "; sala["C5"] = "-"; sala["C6"] = " "
    sala["D4"] = " "; sala["D5"] = " "; sala["D6"] = " "

    # Column 3
    sala["A7"] = "-"; sala["A8"] = " "; sala["A9"] = " "
    sala["B7"] = " "; sala["B8"] = " "; sala["B9"] = " "
    sala["C7"] = " "; sala["C8"] = " "; sala["C9"] = " "
    sala["D7"] = " "; sala["D8"] = " "; sala["D9"] = " "

    return sala                   # The dictionary is returned so it can be used in all other functions

def mostrar_sala(sala):
    """
    Receives the room dictionary and returns the drawing ready to print.
    """
    dibujo = []                                    # Empty list to store each line of the drawing

    # Header lines
    dibujo.append("                1     2     3           4     5     6           7     8     9")
    dibujo.append("             Column 1                 Column 2                 Column 3")
    
    filas = ["A", "B", "C", "D"]                   # List with the rows
    
    for f in filas:                                # for loop goes through each row letter (A, B, C, D)
        linea = f + "      "                       # The row letter is concatenated with spaces for alignment
        for num in range(1, 10):                   # range(1,10) generates numbers from 1 to 9 (does not include 10)
            asiento = f + str(num)                 # str(num) converts the number to text to form "A1", "A2", etc.
            estado = sala[asiento]                 # The seat status is looked up in the dictionary
            linea += f"[{estado}] "                # f-string is used because it is more readable and allows inserting variables easily
            if num % 3 == 0:                       # % is the modulo operator. Every 3 seats (end of column) a space is added
                linea += "      "                  # Large space to visually separate the 3 columns
        dibujo.append(linea.rstrip())              # .rstrip() removes trailing whitespace from the line
    return "\n".join(dibujo)                       # .join() joins all lines with a newline

def esta_libre(sala, asiento):
    """
    Checks if a seat is available.
    """
    if asiento in sala and sala[asiento] == " ":   # 'in' checks if the key exists and == compares the value
        return True
    return False

def son_continuos_y_libres(sala, lista_asientos):
    for asiento in lista_asientos:                 # We go through each seat the user entered
        if not validar_asiento(asiento):           # 'not' negates the result of the lambda
            return False, "Incorrect seat format. Use A1, B2, etc."
    
    for asiento in lista_asientos:
        if not esta_libre(sala, asiento):
            return False, "One or more seats are already occupied or disabled"
    
    if len(lista_asientos) == 1:                   # len() returns how many elements the list has
        return True, "OK"
    
    primera_fila = lista_asientos[0][0]            # [0] takes the first seat and [0] takes its first letter (the row)
    for asiento in lista_asientos:
        if asiento[0] != primera_fila:             # != means "different from"
            return False, "All seats must be in the same row"
    
    numeros = [int(asiento[1]) for asiento in lista_asientos]  # List comprehension: extracts the number from each seat
    numeros.sort()                                 # .sort() sorts the list of numbers from smallest to largest
    if numeros[-1] - numeros[0] + 1 != len(numeros):  # numeros[-1] is the last element
        return False, "Seats must be contiguous, without leaving free spaces between them"
    
    return True, "OK"

def ocupar_asientos(sala, lista_asientos):
    """
    Marks the selected seats as occupied ('X').
    """
    nueva_sala = sala.copy()                       # .copy() creates a copy so the original room is not modified
    for asiento in lista_asientos:
        if asiento in nueva_sala:                  # We check that the seat exists before changing it
            nueva_sala[asiento] = "X"
    return nueva_sala

def buscar_asientos_automaticos(sala, cantidad):
    """
    Automatic assignment of contiguous seats.
    """
    filas = ["A", "B", "C", "D"]
    for f in filas:
        for inicio in range(1, 10 - cantidad + 2): # 10 - cantidad + 2 calculates where a block can start
            bloque = [f + str(inicio + i) for i in range(cantidad)]  # List comprehension to create the block
            if all(esta_libre(sala, asiento) for asiento in bloque): # all() checks that ALL are free
                return bloque
    return []

def registrar_cliente(lista_clientes, id_cliente, nombre):
    """
    Registers a new client
    """
    for c in lista_clientes:
        if c["id"] == id_cliente:                  # == compares if the ID already exists
            return lista_clientes
    nuevo = {"id": id_cliente, "name": nombre}     # Dictionary with the client's data
    lista_clientes.append(nuevo)                   # .append() adds the new client to the list
    return lista_clientes

def buscar_cliente(lista_clientes, id_cliente):
    """
    Searches for a client by ID.
    """
    for c in lista_clientes:
        if c["id"] == id_cliente:
            return c
    return None                                    # None is returned when the client is not found

def guardar_compra(lista_compras, id_cliente, lista_asientos, fecha_hora):
    """
    Saves a completed purchase
    """
    compra = {"client_id": id_cliente, "seats": lista_asientos, "date": fecha_hora}
    lista_compras.append(compra)
    return lista_compras

def mostrar_entradas_vendidas(lista_compras, lista_clientes):
    """
    Returns sold tickets with the client's name
    """
    resultado = []
    for compra in lista_compras:
        nombre = "Unknown"
        for cliente in lista_clientes:
            if cliente["id"] == compra["client_id"]:
                nombre = cliente["name"]
                break
        info = {"client": nombre, "seats": ", ".join(compra["seats"]), "date": compra["date"]}  # ", ".join() joins seats with commas
        resultado.append(info)
    return resultado

def generar_reporte(sala, lista_compras, lista_clientes):
    """
    Generates the room occupancy report
    """
    total = len(sala)                              # len(sala) counts how many seats there are in total
    disponibles = sum(1 for v in sala.values() if v == " ")  # sum() + generator counts free seats
    ocupados = sum(1 for v in sala.values() if v == "X")
    if (ocupados + disponibles) > 0:
        porcentaje = round((ocupados * 100) / (ocupados + disponibles), 2)  # round(..., 2) leaves 2 decimal places
    else:
        porcentaje = 0
    compradores = []
    for compra in lista_compras:
        for cliente in lista_clientes:
            if cliente["id"] == compra["client_id"] and cliente["name"] not in compradores:
                compradores.append(cliente["name"])
    compradores.sort(key=lambda n: n.lower())      # .sort() with lambda sorts without distinguishing uppercase/lowercase
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
    Main function that controls the entire program (menu and flow).
    """
    sala = crear_sala()          # We call the function to create the room at the start
    clientes = []                # Empty list of clients
    compras = []                 # Empty list of purchases
    
    print("=== RIWIFILMS MULTICINEMA SYSTEM ===")
    print("WELCOME!\n")
    
    continuar = True             # Boolean flag to control the loop
    
    while continuar:             # Loop that repeats while continuar is True
        print("\n--- MENU ---")
        print("1. Register client")
        print("2. View room")
        print("3. Buy tickets")
        print("4. View sold tickets")
        print("5. View report")
        print("6. Exit")
        
        opcion = input("Choose an option (1-6): ").strip()   # .strip() removes spaces at the beginning and end
        
        if opcion == "1":
            print("\n--- REGISTER CLIENT ---")
            idc = input("Client ID: ").strip()          
            if idc == "" or not idc.isdigit():               
                print("Error: The ID can only contain numbers (no letters or spaces)")
                continue
            nom = input("Client name: ").strip()
            if nom == "" or not nom.replace(" ", "").isalpha():  
                print("Error: The name can only contain letters and spaces")
                continue
            clientes = registrar_cliente(clientes, idc, nom)
            print(f"Client saved successfully → ID: {idc} | Name: {nom}")  
            
        elif opcion == "2":
            print(mostrar_sala(sala))
        
        elif opcion == "3":
            idc = input("Client ID: ").strip()
            cliente = buscar_cliente(clientes, idc)
            if cliente is None:                              
                print("Client not found. Please register first.")
                continue
            try:
                cant = int(input("How many seats do you want to buy? "))  
                if cant < 1:
                    print("The quantity must be greater than 0")
                    continue
            except:
                print("Please enter only a number")
                continue
            auto = input("Automatic assignment? (y/n): ").strip().lower()  
            if auto == "y":
                asientos = buscar_asientos_automaticos(sala, cant)
                if len(asientos) == 0:
                    print("There is no contiguous space for that quantity.")
                    continue
                print("Automatic seats:", ", ".join(asientos))
            else:
                print(mostrar_sala(sala))
                texto = input("Enter the seats (example: A1,A2,A3): ").strip().upper()  
                asientos = [x.strip() for x in texto.split(",") if x.strip()]  
            if len(asientos) != cant:
                print(f"You must enter exactly {cant} seats.")
                continue
            ok, msg = son_continuos_y_libres(sala, asientos)
            if ok:
                sala = ocupar_asientos(sala, asientos)
                fecha_hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")  
                compras = guardar_compra(compras, idc, asientos, fecha_hora)
                print("¡PURCHASE COMPLETED!")
                print("Client:", cliente["name"])
                print("Seats:", ", ".join(asientos))
                print("Date and time:", fecha_hora)
            else:
                print("Error:", msg)
        
        elif opcion == "4":
            entradas = mostrar_entradas_vendidas(compras, clientes)
            if len(entradas) == 0:
                print("No tickets have been sold yet.")
            else:
                print("\nSOLD TICKETS:")
                for e in entradas:
                    print("Client:", e["client"])
                    print("Seats:", e["seats"])
                    print("Date and time:", e["date"])
                    print("---")
        
        elif opcion == "5":
            rep = generar_reporte(sala, compras, clientes)
            print("\nOCCUPANCY REPORT")
            print("Total seats:", rep["total_seats"])
            print("Available:", rep["available"])
            print("Occupied:", rep["occupied"])
            print("Disabled:", rep["disabled"])
            print("Occupancy percentage:", rep["occupation_percentage"], "%")
            print("Clients who bought:")
            if len(rep["clients_who_bought"]) == 0:
                print("None yet")
            else:
                for nombre in rep["clients_who_bought"]:
                    print(" -", nombre)
        
        elif opcion == "6":
            print("Thank you for using the system!")
            continuar = False               # Change flag to False to exit the loop
        
        else:
            print("Invalid option, please try again.")

if __name__ == "__main__":     # This condition ensures that main() is only executed when this file is run directly
    main()