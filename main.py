import csv
import getpass
from datetime import datetime

# Simulación de base de datos
users_file = "users.csv"
# Función para cargar usuarios desde el CSV
def load_users_from_csv():
    users = {}
    try:
        with open(users_file, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                users[row["username"]] = row["password"]
    except FileNotFoundError:
        print("No se encontró el archivo de usuarios. Necesitamos crear un usuario administrador.")
        create_first_user(users)
    return users
    
# Crear primer usuario si el archivo de usuarios no existe
def create_first_user(users):
    print("Creando el primer usuario:")
    username = input("Ingrese el nombre de usuario: ")
    password = getpass.getpass("Ingrese la contraseña: ")
    users[username] = password
    with open(users_file, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=["username", "password"])
        writer.writeheader()
        writer.writerow({"username": username, "password": password})
    print(f"Usuario '{username}' creado exitosamente.")

# Autenticación de usuario
def authenticate(users):
    username = input("Usuario: ")
    password = getpass.getpass("Contraseña: ")
    
    if username in users and users[username] == password:
        print(f"Bienvenido {username}!")
        return True
    else:
        print("Usuario o contraseña incorrectos.")
        return False
# Ejecución del programa
if __name__ == "__main__":
    users = load_users_from_csv()
