#!/bin/bash
# Script para revertir el repositorio al commit 774620ce1630a6489fb1af9b44f2a3bbe248d2f8
#
# USO: ./revert_to_774620ce.sh
# NOTA: Si el script no es ejecutable, usa: chmod +x revert_to_774620ce.sh
#
# ADVERTENCIA: Este script usa 'git reset --hard' y 'git push --force'
# Asegúrate de entender lo que hace antes de ejecutarlo.

set -e  # Exit on any error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Commit objetivo
TARGET_COMMIT="774620ce1630a6489fb1af9b44f2a3bbe248d2f8"

echo -e "${YELLOW}========================================${NC}"
echo -e "${YELLOW}Script de Reversión a Commit 774620ce${NC}"
echo -e "${YELLOW}========================================${NC}"
echo ""

# Verificar que estamos en un repositorio git
if [ ! -d ".git" ]; then
    echo -e "${RED}ERROR: No estás en un repositorio git${NC}"
    echo "Ejecuta este script desde el directorio raíz del repositorio"
    exit 1
fi

# Verificar que el repositorio es el correcto
REPO_URL=$(git remote get-url origin 2>/dev/null || echo "")
if [[ ! "$REPO_URL" =~ "redactor-informe-D2" ]]; then
    echo -e "${RED}ERROR: Este no parece ser el repositorio correcto${NC}"
    echo "URL del remoto: $REPO_URL"
    echo "Se esperaba un repositorio llamado 'redactor-informe-D2'"
    read -p "¿Deseas continuar de todos modos? (s/N): " confirm
    if [[ ! "$confirm" =~ ^[sS]$ ]]; then
        echo "Operación cancelada"
        exit 1
    fi
fi

# Advertencia final
echo -e "${RED}ADVERTENCIA:${NC} Este script va a:"
echo "  1. Hacer checkout a la rama 'main'"
echo "  2. Descartar TODOS los cambios locales"
echo "  3. Hacer reset duro al commit $TARGET_COMMIT"
echo "  4. Forzar el push al remoto (reescribiendo el historial)"
echo ""
echo -e "${YELLOW}Esto va a ELIMINAR todos los commits posteriores al commit objetivo${NC}"
echo ""
read -p "¿Estás SEGURO de que deseas continuar? (escribe 'SI' en mayúsculas): " confirm

if [ "$confirm" != "SI" ]; then
    echo "Operación cancelada"
    exit 0
fi

echo ""
echo -e "${GREEN}Iniciando proceso de reversión...${NC}"
echo ""

# Paso 1: Checkout a main
echo "Paso 1: Cambiando a rama 'main'..."
git checkout main || {
    echo -e "${RED}ERROR: No se pudo hacer checkout a main${NC}"
    exit 1
}
echo -e "${GREEN}✓ Checkout a main exitoso${NC}"
echo ""

# Paso 2: Fetch del remoto (intentar unshallow primero)
echo "Paso 2: Descargando historial del remoto..."
if git fetch --unshallow 2>/dev/null; then
    echo -e "${GREEN}✓ Repositorio completo descargado${NC}"
else
    echo "Repositorio no es shallow, haciendo fetch normal..."
    git fetch --all || {
        echo -e "${RED}ERROR: No se pudo hacer fetch del remoto${NC}"
        exit 1
    }
    echo -e "${GREEN}✓ Fetch exitoso${NC}"
fi
echo ""

# Paso 3: Verificar que el commit objetivo existe
echo "Paso 3: Verificando que el commit objetivo existe..."
if git cat-file -e "$TARGET_COMMIT" 2>/dev/null; then
    echo -e "${GREEN}✓ Commit objetivo encontrado${NC}"
else
    echo -e "${RED}ERROR: El commit $TARGET_COMMIT no existe en el repositorio${NC}"
    echo "Verifica que el commit hash sea correcto"
    exit 1
fi
echo ""

# Paso 4: Mostrar información del commit objetivo
echo "Información del commit objetivo:"
git log -1 --pretty=format:"  Commit: %H%n  Autor: %an <%ae>%n  Fecha: %ad%n  Mensaje: %s%n" "$TARGET_COMMIT"
echo ""
echo ""

# Confirmación final
read -p "¿Confirmas que este es el commit correcto? (s/N): " confirm_commit
if [[ ! "$confirm_commit" =~ ^[sS]$ ]]; then
    echo "Operación cancelada"
    exit 0
fi
echo ""

# Paso 5: Reset duro
echo "Paso 5: Haciendo reset duro al commit objetivo..."
git reset --hard "$TARGET_COMMIT" || {
    echo -e "${RED}ERROR: No se pudo hacer reset al commit${NC}"
    exit 1
}
echo -e "${GREEN}✓ Reset exitoso${NC}"
echo ""

# Paso 6: Mostrar estado actual
echo "Estado después del reset:"
git log -1 --oneline
echo ""

# Paso 7: Push forzado
echo "Paso 7: Haciendo push forzado al remoto..."
read -p "¿Proceder con 'git push --force'? (s/N): " confirm_push
if [[ ! "$confirm_push" =~ ^[sS]$ ]]; then
    echo -e "${YELLOW}ADVERTENCIA: El reset local fue exitoso pero NO se actualizó el remoto${NC}"
    echo "Para sincronizar el remoto más tarde, ejecuta:"
    echo "  git push --force origin main"
    exit 0
fi

git push --force origin main || {
    echo -e "${RED}ERROR: No se pudo hacer push forzado${NC}"
    echo "Puedes intentar manualmente con: git push --force origin main"
    exit 1
}
echo -e "${GREEN}✓ Push forzado exitoso${NC}"
echo ""

# Verificación final
echo -e "${GREEN}========================================${NC}"
echo -e "${GREEN}¡Reversión completada exitosamente!${NC}"
echo -e "${GREEN}========================================${NC}"
echo ""
echo "Estado final:"
echo "  Commit actual: $(git rev-parse HEAD)"
echo "  Rama: $(git branch --show-current)"
echo ""
echo "Archivos en el repositorio:"
ls -1
echo ""
echo -e "${GREEN}El repositorio local y remoto ahora están en el commit 774620ce${NC}"
