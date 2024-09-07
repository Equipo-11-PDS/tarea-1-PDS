import csv
import getpass
from datetime import datetime

# Simulación de base de datos
users_file = "users.csv"
tasks_file = "tasks.csv"
tasks = []

# Clase Tarea
class Task:
    def __init__(self, title, description, due_date, label, state="pending", completed_at=None):
        self.title = title
        self.description = description
        self.due_date = due_date
        self.label = label
        self.state = state
        self.completed_at = completed_at

    def __repr__(self):
        return f"Tarea: {self.title} | Estado: {self.state} | Vencimiento: {self.due_date}"

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

# Cargar tareas desde el CSV
def load_tasks_from_csv():
    try:
        with open(tasks_file, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                task = Task(
                    row["title"],
                    row["description"],
                    row["due_date"],
                    row["label"],
                    row["state"],
                    row["completed_at"] if row["completed_at"] != '' else None
                )
                tasks.append(task)
    except FileNotFoundError:
        print("No se encontró el archivo CSV de tareas. Creando uno nuevo...")

# Guardar tareas en el CSV
def save_tasks_to_csv():
    with open(tasks_file, mode='w', newline='') as file:
        fieldnames = ["title", "description", "due_date", "label", "state", "completed_at"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        for task in tasks:
            writer.writerow({
                "title": task.title,
                "description": task.description,
                "due_date": task.due_date,
                "label": task.label,
                "state": task.state,
                "completed_at": task.completed_at if task.completed_at else ''
            })

# Gestión de Tareas
def create_task():
    title = input("Título de la tarea: ")
    description = input("Descripción de la tarea: ")
    due_date = input("Fecha de vencimiento (YYYY-MM-DD): ")
    label = input("Etiqueta (urgente, trabajo, personal, etc.): ")
    task = Task(title, description, due_date, label)
    tasks.append(task)
    save_tasks_to_csv()
    print("Tarea creada exitosamente.")

def list_tasks():
    if tasks:
        for index, task in enumerate(tasks):
            print(f"{index + 1}. {task}")
    else:
        print("No hay tareas.")

def update_task():
    list_tasks()
    task_id = int(input("Número de la tarea que desea actualizar: ")) - 1
    if 0 <= task_id < len(tasks):
        tasks[task_id].title = input("Nuevo título: ")
        tasks[task_id].description = input("Nueva descripción: ")
        tasks[task_id].due_date = input("Nueva fecha de vencimiento (YYYY-MM-DD): ")
        tasks[task_id].label = input("Nueva etiqueta: ")
        save_tasks_to_csv()
        print("Tarea actualizada exitosamente.")
    else:
        print("Tarea no encontrada.")

def delete_task():
    list_tasks()
    task_id = int(input("Número de la tarea que desea eliminar: ")) - 1
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        save_tasks_to_csv()
        print("Tarea eliminada.")
    else:
        print("Tarea no encontrada.")

# Filtrado y búsqueda
def filter_tasks():
    criteria = input("Filtrar por (fecha, etiqueta, estado): ").lower()
    if criteria == "fecha":
        date = input("Ingrese la fecha (YYYY-MM-DD): ")
        filtered_tasks = [task for task in tasks if task.due_date == date]
    elif criteria == "etiqueta":
        label = input("Ingrese la etiqueta: ")
        filtered_tasks = [task for task in tasks if task.label == label]
    elif criteria == "estado":
        state = input("Ingrese el estado (pending, in progress, completed): ")
        filtered_tasks = [task for task in tasks if task.state == state]
    else:
        print("Criterio inválido.")
        return
    
    if filtered_tasks:
        for task in filtered_tasks:
            print(task)
    else:
        print("No se encontraron tareas que coincidan con el criterio.")

# Cambiar el estado de las tareas
def update_task_status():
    list_tasks()
    task_id = int(input("Número de la tarea que desea actualizar: ")) - 1
    if 0 <= task_id < len(tasks):
        new_status = input("Nuevo estado (pending, in progress, completed): ").lower()
        if new_status in ["pending", "in progress", "completed"]:
            tasks[task_id].state = new_status
            if new_status == "completed":
                tasks[task_id].completed_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            save_tasks_to_csv()
            print("Estado de la tarea actualizado.")
        else:
            print("Estado inválido.")
    else:
        print("Tarea no encontrada.")

# Menú principal
def main_menu():
    while True:
        print("\n--- Gestión de Tareas ---")
        print("1. Crear tarea")
        print("2. Listar tareas")
        print("3. Actualizar tarea")
        print("4. Eliminar tarea")
        print("5. Filtrar tareas")
        print("6. Cambiar estado de tarea")
        print("7. Salir")

        option = input("Seleccione una opción: ")
        if option == "1":
            create_task()
        elif option == "2":
            list_tasks()
        elif option == "3":
            update_task()
        elif option == "4":
            delete_task()
        elif option == "5":
            filter_tasks()
        elif option == "6":
            update_task_status()
        elif option == "7":
            print("Saliendo...")
            break
        else:
            print("Opción no válida.")

# Ejecución del programa
if __name__ == "__main__":
    users = load_users_from_csv()
    if authenticate(users):
        load_tasks_from_csv()
        main_menu()
