# Task Manager Application

## Descripción
Esta es una aplicación de línea de comandos para gestionar tareas, que incluye la funcionalidad de crear, consultar, actualizar y eliminar tareas. Cada tarea tiene un título, descripción, fecha de vencimiento y etiquetas para facilitar la organización. Además, se pueden gestionar los estados de las tareas (pendiente, en progreso, completada), realizar búsquedas y filtrados, y se requiere autenticación mediante nombre de usuario y contraseña.

## Instalación
1. Clona este repositorio:
   ```bash
   git clone https://github.com/Equipo-11-PDS/tarea-1-PDS.git
   ```
2. Navega al directorio del proyecto:
   ```bash
   cd tarea-1-PDS
   ```

## Uso
1. Ejecuta el programa:
   ```bash
   python main.py
   ```
2. Si es la primera vez que ejecutas el programa, se te pedirá crear un usuario administrador.
3. Una vez autenticado, utiliza el menú para gestionar tus tareas:
   - Crear tarea
   - Listar tareas
   - Actualizar tarea
   - Eliminar tarea
   - Filtrar tareas
   - Cambiar estado de tareas

4. Los logs de las operaciones se almacenan en el archivo `app.log`.

## Cómo contribuir
1. Haz un fork de este repositorio.
2. Crea una rama con tu nueva funcionalidad o corrección de errores:
   ```bash
   git checkout -b nueva-funcionalidad
   ```
3. Realiza tus cambios y haz un commit:
   ```bash
   git commit -m "Añadir nueva funcionalidad"
   ```
4. Sube tus cambios a tu rama:
   ```bash
   git push origin nueva-funcionalidad
   ```
5. Crea un Pull Request en GitHub.

## Licencia
Este proyecto está bajo la licencia MIT. Consulta el archivo [LICENSE](./LICENSE) para más detalles.