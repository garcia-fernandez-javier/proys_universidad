# Práctica P3: Definición y Modificación de Datos en SQL

Práctica académica individual de la asignatura **Bases de Datos I** (curso 2023/24, convocatoria enero). Se diseña, crea y manipula un esquema relacional en **Oracle SQL** que modela una plataforma de música en streaming, cubriendo desde la creación de tablas y restricciones hasta modificaciones de datos, vistas, índices y control de transacciones.

---

## 📂 Contenido del repositorio

| Archivo | Descripción |
|--------|-------------|
| `bdi112-p3-esquema.sql` | Definición del esquema: `CREATE TABLE`, restricciones de integridad y `ALTER TABLE` para FK circular |
| `bdi112-p3-insert.sql` | Datos de prueba: `INSERT` en las cinco tablas con gestión de FK circulares mediante `DISABLE`/`ENABLE CONSTRAINT` |
| `bdi112-p3-ejer.sql` | Resolución de los ejercicios 2–9: `UPDATE`, `DELETE`, `ALTER TABLE`, `CREATE VIEW`, índices y control transaccional |

---

## 🗄️ Esquema de la base de datos

La base de datos modela una plataforma de streaming musical con cinco tablas:

```
usuario ──────────────────────────────────────────────────┐
  id_usuario (PK) · nombre · email · telefono             │
  tipo · cuota · invitador (FK→usuario) · ultimo_acceso   │
         │                                                │
         └──► lista ◄─────────────────────────────────────┘
                (usuario, num_lista) PK · nombre · descripcion
                         │
                         └──► lista_cancion
                                (usuario, lista, album, cancion) PK · fecha

banda ◄────────────────────────┐
  id_artista (PK) · nombre     │
  pais_origen · a_fundacion    │
  lider (FK→musico)            │
                               │
musico ────────────────────────┘
  id_musico (PK) · nombre · banda (FK→banda)
```

### Restricciones destacadas
- `usuario`: clave alternativa en `email` y en `telefono`; check XOR que exige exactamente uno de los dos; check que impide que un usuario se invite a sí mismo; dominio de `tipo` limitado a cuatro valores (`GRATUITO`, `PREMIUM INDIVIDUAL`, `PREMIUM DOS`, `PREMIUM FAMILIAR`)
- `lista`: check `num_lista > 0`
- `banda ↔ musico`: FK circular resuelta con `ALTER TABLE musico ADD CONSTRAINT` tras la creación de ambas tablas
- `lista_cancion`: FK compuesta hacia `lista(usuario, num_lista)`

---

## 📋 Ejercicios implementados

### Ej. 1 — Inserción de datos (`bdi112-p3-insert.sql`)
Población completa del esquema con datos de prueba:
- **12 usuarios** con distintos tipos de cuenta y red de invitaciones entre ellos
- **11 listas** de reproducción distribuidas entre varios usuarios
- **5 bandas**: Eurythmics, Queen, Radio Futura, Vetusta Morla, The Strokes
- **19 músicos** agrupados por banda
- Canciones de listas referenciando álbumes A001–A014

Las FK circulares (`usuario_fk_invitador`, `banda_fk_id_musico`) se deshabilitan durante la inserción y se rehabilitan al finalizar.

---

### Ej. 2 — Modificación de cuotas (`UPDATE` + `ROLLBACK`)
Descuento del 5 % en la cuota de los usuarios que han invitado a dos o más personas, usando subconsulta con `GROUP BY / HAVING`. Se verifica el estado antes y después, y se deshace con `ROLLBACK`.

### Ej. 3 — Cambio de clave primaria (`UPDATE` en cascada manual)
Renombrado del usuario `U001` → `U901` propagando el cambio a todas las tablas que lo referencian (`lista_cancion`, `lista`, `usuario.invitador`) mediante deshabilitación temporal de constraints, actualización en orden y rehabilitación en orden inverso. Finaliza con `COMMIT`.

### Ej. 4 — Borrado condicional de filas (`DELETE`)
Eliminación de usuarios GRATUITOS cuyo `ultimo_acceso` es anterior al 19/11/2019 y que no hayan invitado a nadie, usando subconsulta con `NOT IN`.

### Ej. 5 — Borrado en cascada manual (`DELETE` multitabla)
Borrado completo del usuario `U236` junto con sus listas y canciones, deshabilitando temporalmente las FK para evitar errores de integridad referencial durante el proceso.

### Ej. 6 — Eliminación de columnas (`ALTER TABLE DROP COLUMN`)
Eliminación de `pais_origen` y `a_fundacion` de la tabla `banda`. Se razona que Oracle no permite eliminar ambas columnas en una sola sentencia `DROP COLUMN`.

### Ej. 7 — Vista `datos_usuario`
- **Creación:** vista que muestra nombre, tipo, cuota, número de listas, número de canciones y días de desconexión (`TRUNC(SYSDATE - ultimo_acceso)`) para usuarios no GRATUITOS, con `LEFT JOIN` a `lista` y `lista_cancion`
- **Modificación:** `CREATE OR REPLACE VIEW` para reflejar el IVA del 21 % en la cuota (`cuota * 1.21`)
- **Verificación:** se inserta el usuario `U299 CHOPIN` y se comprueba que aparece en la vista ya con la cuota incrementada, demostrando que las vistas reflejan el estado actual de las tablas en el momento de la consulta

### Ej. 8 — Verificación de aserto de integridad
Consulta con `NOT EXISTS` para comprobar que el `lider` de cada banda es músico de esa misma banda. El resultado vacío confirma que el aserto se cumple sobre los datos cargados.

### Ej. 9 — Índices y plan de ejecución
- Análisis del coste de una consulta filtrada por `usuario.tipo` (coste inicial: 6)
- Creación del índice `idx_tipo_usuario ON usuario(tipo)`
- El índice es utilizado por el optimizador, pero el coste sube a 15: ilustra que un índice sobre una columna de baja cardinalidad puede ser contraproducente en Oracle

---

## 🛠️ Tecnología

- **SGBD:** Oracle Database (SQL*Plus / SQL Developer)
- **Lenguaje:** SQL con extensiones Oracle (`CHAR`, `VARCHAR2`, `NUMBER`, `TO_DATE`, `TRUNC`, `SYSDATE`)
- **Control de transacciones:** `COMMIT` / `ROLLBACK`
- **DDL dinámico:** `DISABLE` / `ENABLE CONSTRAINT` para gestión de FK circulares

---

## 🧑‍💻 Autor

Javier García Fernández — Equipo bdi112  
Grado en Ciencia e Ingeniería de Datos  
Bases de Datos I — Curso 2023/24
