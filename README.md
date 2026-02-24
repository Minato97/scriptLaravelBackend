# 🚀 Laravel Backend Auto Generator

Herramienta CLI en Python para generar automáticamente un backend Laravel basado en Docker a partir de un ZIP base.

Automatiza completamente:

- 📦 Descompresión del proyecto base
- 🐳 Configuración dinámica de Docker
- 🛢 Creación automática de base de datos
- 🔐 Generación de APP_KEY y JWT_SECRET
- 🔄 Migraciones y seeders
- 🔗 Inicialización y push a repositorio Git
- 🖥 Compatible con Windows, macOS y Linux

---

## 🧠 Requisitos

Antes de usar la herramienta necesitas:

- Python 3.8+
- Docker
- Docker Compose v2
- Git

Verifica que estén instalados:

```bash
docker --version
docker compose version
python --version
git --version
```

---

## 📁 Estructura esperada

Debes tener en la misma carpeta:

```bash
backend_generator.py
backend-repo.zip
```

`backend-repo.zip` debe contener:

- Proyecto Laravel base
- docker-compose.yml
- docker/php/Dockerfile
- docker/nginx/default.conf
- .env.example

---

## 🚀 Cómo usar

### macOS / Linux

```bash
python3 backend_generator.py
```

### Windows

```bash
python backend_generator.py
```

---

## 🛠 Flujo de ejecución automático

El script solicitará:

- 📁 Nombre del proyecto
- 🛢 Nombre de la base de datos
- 🐳 Puerto MySQL
- 📡 URL del repositorio Git

Luego ejecuta automáticamente:

1. Crea carpeta del proyecto
2. Descomprime el ZIP base
3. Elimina `container_name` del docker-compose
4. Configura base de datos dinámica
5. Genera archivo `.env`
6. Levanta contenedores Docker
7. Espera MySQL correctamente
8. Crea base de datos manualmente
9. Otorga permisos al usuario
10. Ejecuta:
   - `composer update`
   - `php artisan key:generate`
   - `php artisan jwt:secret`
   - `php artisan migrate --seed`
11. Inicializa repositorio Git
12. Hace push automático al repositorio remoto

---

## 🌐 Accesos finales

Una vez finalizado el proceso:

- API → http://localhost:8000
- phpMyAdmin → http://localhost:8080
- MySQL → localhost:PUERTO_ELEGIDO

---

## 🧩 Características técnicas

- No usa nombres fijos de contenedor
- No depende de `shell=True`
- Espera MySQL con `mysqladmin ping`
- Crea base y permisos automáticamente
- Compatible con volúmenes existentes
- Multiplataforma real

---

## 🧨 Problemas comunes

### ❌ Error de permisos MySQL

Solución:

```bash
docker compose -p NOMBRE_PROYECTO down -v
```

Luego vuelve a ejecutar el script.

---

## 🏗 Próximas mejoras

- Detección automática de puerto libre
- Generación automática de README del proyecto creado
- Soporte PostgreSQL
- CLI tipo `backend new proyecto`
- Publicación como paquete pip
- Compilación a .exe multiplataforma

---

## 👨‍💻 Autor

Creado por **minato97**

---

## 📜 Licencia

Este proyecto es de **uso libre**.  
Puedes usarlo y distribuirlo sin restricciones.