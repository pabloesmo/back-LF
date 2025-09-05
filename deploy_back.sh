#!/bin/bash
# Script para desplegar el backend paso a paso

# Salir si hay cualquier error
set -e

# Variable para mensaje numerado
COMMIT_MSG="Backend commit con fecha: $(date +'%Y-%m-%d_%H-%M-%S')"

echo "Añadiendo cambios..."
git add .

echo "Haciendo commit con mensaje: $COMMIT_MSG"
git commit -m "$COMMIT_MSG" || echo "Sin cambios para commitear"

echo "Pusheando a remoto..."
git push

echo "🚀 Backend desplegado correctamente"
