import csv
import getpass
from datetime import datetime
import logging

# Configuración básica de logging
logging.basicConfig(
    filename='app.log', 
    level=logging.INFO, 
    format='%(asctime)s %(levelname)s: %(message)s', 
    datefmt='%d/%m/%Y %H:%M:%S'
)

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

def verify_date_format(date_str):
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

def input_valid_date():
    while True:
        date_input = input("Fecha de vencimiento (YYYY-MM-DD): ")
        if verify_date_format(date_input):
            return date_input
        else:
            print("Formato de fecha inválido. Por favor, ingrese la fecha en formato YYYY-MM-DD.")

# Función para validar que un campo no esté vacío
def input_non_empty(prompt):
    while True:
        value = input(prompt)
        if value.strip():
            return value
        else:
            print("Este campo no puede quedar vacío. Por favor, ingrese un valor.")

# Función para cargar usuarios desde el CSV
def load_users_from_csv():
    users = {}
    try:
        with open(users_file, mode='r', newline='') as file:
            reader = csv.DictReader(file)
            for row in reader:
                users[row["username"]] = row["password"]
        logging.info("Usuarios cargados desde el archivo CSV.")
    except FileNotFoundError:
        logging.warning("No se encontró el archivo de usuarios. Necesitamos crear un usuario administrador.")
        create_first_user(users)
    except Exception as e:
        logging.exception("Error al cargar los usuarios.")
    return users

# Crear primer usuario si el archivo de usuarios no existe
def create_first_user(users):
    try:
        print("Creando el primer usuario:")
        username = input_non_empty("Ingrese el nombre de usuario: ")
        password = getpass.getpass("Ingrese la contraseña: ")
        users[username] = password
        with open(users_file, mode='w', newline='') as file:
            writer = csv.DictWriter(file, fieldnames=["username", "password"])
            writer.writeheader()
            writer.writerow({"username": username, "password": password})
        logging.info(f"Primer usuario '{username}' creado.")
    except Exception as e:
        logging.exception("Error al crear el primer usuario.")

# Autenticación de usuario
def authenticate(users):
    try:
        username = input("Usuario: ")
        password = getpass.getpass("Contraseña: ")
        
        if username in users and users[username] == password:
            logging.info(f"Autenticación exitosa para el usuario '{username}'.")
            print(f"Bienvenido {username}!")
            return True
        else:
            logging.warning(f"Falló la autenticación para el usuario '{username}'.")
            print("Usuario o contraseña incorrectos.")
            return False
    except Exception as e:
        logging.exception("Error durante la autenticación.")
        print("Ocurrió un error durante la autenticación.")
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
        logging.info("Tareas cargadas desde el archivo CSV.")
    except FileNotFoundError:
        logging.warning("No se encontró el archivo CSV de tareas. Creando uno nuevo...")
    except Exception as e:
        logging.exception("Error al cargar las tareas.")

# Guardar tareas en el CSV
def save_tasks_to_csv():
    try:
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
        logging.info("Tareas guardadas en el archivo CSV.")
    except Exception as e:
        logging.exception("Error al guardar las tareas.")

# Gestión de Tareas
def create_task():
    try:
        title = input_non_empty("Título de la tarea: ")
        description = input_non_empty("Descripción de la tarea: ")
        due_date = input_valid_date()
        label = input_non_empty("Etiqueta (urgente, trabajo, personal, etc.): ")
        task = Task(title, description, due_date, label)
        tasks.append(task)
        save_tasks_to_csv()
        logging.info(f"Tarea '{title}' creada exitosamente.")
    except Exception as e:
        logging.exception("Error al crear la tarea.")
        print("Ocurrió un error al crear la tarea.")

def list_tasks():
    try:
        if tasks:
            for index, task in enumerate(tasks):
                print(f"{index + 1}. {task}")
        else:
            print("No hay tareas.")
    except Exception as e:
        logging.exception("Error al listar las tareas.")
        print("Ocurrió un error al listar las tareas.")

def update_task():
    try:
        list_tasks()
        task_id = int(input("Número de la tarea que desea actualizar: ")) - 1
        if 0 <= task_id < len(tasks):
            tasks[task_id].title = input_non_empty("Nuevo título: ")
            tasks[task_id].description = input_non_empty("Nueva descripción: ")
            tasks[task_id].due_date = input_valid_date()
            tasks[task_id].label = input_non_empty("Nueva etiqueta: ")
            save_tasks_to_csv()
            logging.info(f"Tarea '{tasks[task_id].title}' actualizada.")
            print("Tarea actualizada exitosamente.")
        else:
            logging.warning(f"Intento de actualización fallido: Tarea con índice {task_id} no encontrada.")
            print("Tarea no encontrada.")
    except ValueError:
        logging.warning("Entrada inválida al actualizar la tarea.")
        print("Entrada inválida. Por favor, ingrese un número válido.")
    except Exception as e:
        logging.exception("Error al actualizar la tarea.")
        print("Ocurrió un error al actualizar la tarea.")

def delete_task():
    try:
        list_tasks()
        task_id = int(input("Número de la tarea que desea eliminar: ")) - 1
        if 0 <= task_id < len(tasks):
            task_title = tasks[task_id].title
            tasks.pop(task_id)
            save_tasks_to_csv()
            logging.info(f"Tarea '{task_title}' eliminada.")
            print("Tarea eliminada.")
        else:
            logging.warning(f"Intento de eliminación fallido: Tarea con índice {task_id} no encontrada.")
            print("Tarea no encontrada.")
    except ValueError:
        logging.warning("Entrada inválida al eliminar la tarea.")
        print("Entrada inválida. Por favor, ingrese un número válido.")
    except Exception as e:
        logging.exception("Error al eliminar la tarea.")
        print("Ocurrió un error al eliminar la tarea.")

# Filtrado y búsqueda
def filter_tasks():
    try:
        criteria = input("Filtrar por (fecha, etiqueta, estado): ").lower()
        if criteria == "fecha":
            date = input_valid_date()
            filtered_tasks = [task for task in tasks if task.due_date == date]
        elif criteria == "etiqueta":
            label = input("Ingrese la etiqueta: ")
            filtered_tasks = [task for task in tasks if task.label == label]
        elif criteria == "estado":
            state = input("Ingrese el estado (pending, in progress, completed): ")
            filtered_tasks = [task for task in tasks if task.state == state]
        else:
            print("Criterio inválido.")
            logging.warning("Criterio de filtrado inválido.")
            return
        
        if filtered_tasks:
            for task in filtered_tasks:
                print(task)
        else:
            logging.info("No se encontraron tareas que coincidan con el criterio.")
            print("No se encontraron tareas que coincidan con el criterio.")
    except Exception as e:
        logging.exception("Error al filtrar las tareas.")
        print("Ocurrió un error al filtrar las tareas.")

# Cambiar el estado de las tareas
def update_task_status():
    try:
        list_tasks()
        task_id = int(input("Número de la tarea que desea actualizar: ")) - 1
        if 0 <= task_id < len(tasks):
            new_status = input("Nuevo estado (pending, in progress, completed): ").lower()
            if new_status in ["pending", "in progress", "completed"]:
                tasks[task_id].state = new_status
                if new_status == "completed":
                    tasks[task_id].completed_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                save_tasks_to_csv()
                logging.info(f"Estado de la tarea '{tasks[task_id].title}' actualizado a '{new_status}'.")
                print("Estado de la tarea actualizado.")
            else:
                logging.warning("Estado inválido.")
                print("Estado inválido.")
        else:
            logging.warning(f"Intento de actualización de estado fallido: Tarea con índice {task_id} no encontrada.")
            print("Tarea no encontrada.")
    except ValueError:
        logging.warning("Entrada inválida al actualizar el estado de la tarea.")
        print("Entrada inválida. Por favor, ingrese un número válido.")
    except Exception as e:
        logging.exception("Error al actualizar el estado de la tarea.")
        print("Ocurrió un error al actualizar el estado de la tarea.")

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

        try:
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
                logging.info("Aplicación cerrada por el usuario.")
                print("Saliendo...")
                break
            else:
                logging.warning(f"Opción no válida seleccionada: {option}")
                print("Opción no válida.")
        except Exception as e:
            logging.exception("Error en el menú principal.")
            print("Ocurrió un error en el menú principal.")

# Ejecución del programa
if __name__ == "__main__":
    try:
        users = load_users_from_csv()
        if authenticate(users):
            load_tasks_from_csv()
            main_menu()
    except Exception as e:
        logging.exception("Error inesperado en la ejecución del programa.")
        print("Ocurrió un error inesperado. Por favor, revise los logs para más detalles.")