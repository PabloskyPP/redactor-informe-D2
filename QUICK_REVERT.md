# Comandos Rápidos para Revertir

## Comando de Una Línea

Si confías en el script y quieres ejecutarlo sin interacción:

```bash
bash revert_to_774620ce.sh
```

## Comando Manual Directo

Si prefieres hacerlo manualmente sin el script:

```bash
git checkout main && \
git fetch --unshallow 2>/dev/null || git fetch --all && \
git reset --hard 774620ce1630a6489fb1af9b44f2a3bbe248d2f8 && \
git push --force origin main
```

## Verificación Rápida

```bash
# Verificar que estás en el commit correcto
git rev-parse HEAD
# Debe mostrar: 774620ce1630a6489fb1af9b44f2a3bbe248d2f8

# Verificar que no existe el archivo incorrecto
test ! -f "et --hard bf36603" && echo "OK: Archivo no existe" || echo "ERROR: Archivo todavía existe"
```

## En Caso de Error

Si algo sale mal y necesitas volver al estado anterior:

```bash
# Ver el log para encontrar el commit anterior
git reflog

# Volver al commit anterior (reemplaza COMMIT_HASH con el hash del commit)
git reset --hard COMMIT_HASH
git push --force origin main
```

## Contacto

Para más detalles, consulta `REVERT_INSTRUCTIONS.md`
