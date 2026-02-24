#!/usr/bin/env python3

import os
import re
import subprocess
import shutil
import zipfile
import sys
import time

ZIP_DEFAULT = "backend-repo.zip"

def abort(msg):
    print(f"\n❌ ERROR: {msg}")
    print("🛑 Proceso abortado.")
    sys.exit(1)

def run(cmd, cwd=None):
    result = subprocess.run(cmd, cwd=cwd)
    if result.returncode != 0:
        abort(f"Error ejecutando: {' '.join(cmd)}")

print("🚀 Laravel Backend Generator (Robust Edition)")
print("------------------------------------------------")

if not os.path.isfile(ZIP_DEFAULT):
    abort(f"No se encontró {ZIP_DEFAULT} en el directorio actual.")

project_name = input("📁 Nombre del nuevo proyecto: ").strip()
db_name = input("🛢 Nombre de la base de datos: ").strip()
db_port = input("🐳 Puerto MySQL (ej: 3307): ").strip()

# Crear carpeta
os.makedirs(project_name, exist_ok=True)

# Descomprimir
print("📦 Descomprimiendo proyecto...")
with zipfile.ZipFile(ZIP_DEFAULT, 'r') as zip_ref:
    zip_ref.extractall(project_name)

os.chdir(project_name)

# Detectar carpeta interna
items = os.listdir(".")
folders = [f for f in items if os.path.isdir(f)]

if len(folders) == 1:
    inner = folders[0]
    for item in os.listdir(inner):
        shutil.move(os.path.join(inner, item), ".")
    shutil.rmtree(inner)

if not os.path.exists("docker-compose.yml"):
    abort("No se encontró docker-compose.yml")

# Eliminar container_name
with open("docker-compose.yml", "r") as f:
    lines = f.readlines()

with open("docker-compose.yml", "w") as f:
    for line in lines:
        if "container_name" not in line:
            f.write(line)

# Reemplazar DB y puerto
with open("docker-compose.yml", "r") as f:
    content = f.read()

content = content.replace("MYSQL_DATABASE: laravel_backend",
                          f"MYSQL_DATABASE: {db_name}")

content = content.replace('"3306:3306"',
                          f'"{db_port}:3306"')

with open("docker-compose.yml", "w") as f:
    f.write(content)

# Configurar .env
if not os.path.exists(".env.example"):
    abort("No existe .env.example")

shutil.copy(".env.example", ".env")

with open(".env", "r") as f:
    env = f.read()

env = re.sub(r"DB_USERNAME=.*", "DB_USERNAME=laravel", env)
env = re.sub(r"DB_PASSWORD=.*", "DB_PASSWORD=root", env)
env = re.sub(r"DB_DATABASE=.*", f"DB_DATABASE={db_name}", env)
env = re.sub(r"DB_HOST=.*", "DB_HOST=db", env)

with open(".env", "w") as f:
    f.write(env)

# Levantar contenedores
print("🐳 Construyendo contenedores...")
run(["docker", "compose", "-p", project_name, "up", "-d", "--build"])

# Esperar MySQL real
print("⏳ Esperando que MySQL esté listo...")
while True:
    try:
        result = subprocess.run(
            ["docker", "compose", "-p", project_name, "exec", "-T", "db",
             "mysqladmin", "ping", "-h", "localhost", "-uroot", "-proot"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        if b"mysqld is alive" in result.stdout:
            break
    except:
        pass
    time.sleep(3)

# Crear base de datos manualmente
run([
    "docker", "compose", "-p", project_name,
    "exec", "-T", "db",
    "mysql", "-uroot", "-proot",
    "-e", f"CREATE DATABASE IF NOT EXISTS {db_name};"
])

# Dar permisos
run([
    "docker", "compose", "-p", project_name,
    "exec", "-T", "db",
    "mysql", "-uroot", "-proot",
    "-e", f"GRANT ALL PRIVILEGES ON {db_name}.* TO 'laravel'@'%'; FLUSH PRIVILEGES;"
])

# Obtener ID real del contenedor app
result = subprocess.check_output(
    ["docker", "compose", "-p", project_name, "ps", "-q", "app"]
).decode().strip()

if not result:
    abort("No se encontró el contenedor app.")

app_container = result

# Composer + artisan
run(["docker", "exec", app_container, "composer", "update"])
run(["docker", "exec", app_container, "php", "artisan", "key:generate"])
run(["docker", "exec", app_container, "php", "artisan", "jwt:secret"])
run(["docker", "exec", app_container, "php", "artisan", "migrate", "--seed"])

# Git
if os.path.exists(".git"):
    shutil.rmtree(".git")

run(["git", "init"])
run(["git", "add", "."])
run(["git", "commit", "-m", "Initial backend setup"])

repo_url = input("📡 URL del nuevo repositorio: ").strip()

run(["git", "remote", "add", "origin", repo_url])
run(["git", "branch", "-M", "main"])
run(["git", "push", "-u", "origin", "main"])

print("\n------------------------------------------------")
print("✅ Backend creado correctamente 🚀")
print("🌐 API disponible en http://localhost:8000")
print("------------------------------------------------")