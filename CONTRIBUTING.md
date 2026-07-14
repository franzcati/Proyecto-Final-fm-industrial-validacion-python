# Guía de contribución

Cada integrante debe trabajar desde su propia cuenta de GitHub y en una rama
separada. No se deben compartir cuentas.

## Ramas sugeridas

- `jorge/documentacion-situacion-actual`
- `bryan/lectura-validaciones-csv`
- `nicol/calculos-reportes-pruebas`
- `franz/integracion-git-informe`

La asignación debe ajustarse al aporte real del equipo antes de la entrega.

## Flujo de trabajo

1. Actualizar la rama principal: `git pull origin main`.
2. Crear la rama: `git switch -c nombre/tarea`.
3. Modificar y probar los archivos.
4. Guardar cambios: `git add .`.
5. Crear un commit descriptivo: `git commit -m "Agregar validación de pedidos"`.
6. Publicar la rama: `git push -u origin nombre/tarea`.
7. Crear un Pull Request hacia `main`.
8. Otro integrante revisa y aprueba antes de hacer merge.

## Reglas

- Un commit debe representar un cambio claro y verificable.
- No subir contraseñas, datos sensibles ni archivos temporales.
- No borrar el trabajo de otro integrante sin conversarlo.
- Cada Pull Request debe explicar qué se cambió y cómo se probó.
