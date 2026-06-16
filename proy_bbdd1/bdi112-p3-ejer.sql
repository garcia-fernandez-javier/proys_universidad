/*
Asignatura: Bases de Datos I
Curso: 2023/24
Convocatoria: enero

Practica: P3. Definicion y Modificacion de Datos en SQL

Equipo de practicas: bdi112
 Integrante 1: Javier Garcia Fernandez
*/

--------------------------------------------------------------------------------------
-- EJERCICIO 2. Modificar valores de una columna

-- a)
-- Mostramos los valores tal cual
SELECT id_usuario, nombre, cuota
FROM usuario 
WHERE id_usuario IN (
    SELECT invitador
    FROM usuario
    GROUP BY invitador
    HAVING COUNT(*) >= 2);

-- b)
-- Modificamos el valor de la cuota segun la especificacion del enunciado
UPDATE usuario
SET cuota = cuota * 0.95
WHERE id_usuario IN (
    SELECT invitador
    FROM usuario
    GROUP BY invitador
    HAVING COUNT(*) >= 2);

-- Mostramos para ver el cambio
SELECT id_usuario, nombre, cuota
FROM usuario 
WHERE id_usuario IN (
    SELECT invitador
    FROM usuario
    GROUP BY invitador
    HAVING COUNT(*) >= 2);
    
-- c)
ROLLBACK;
-- Los datos han vuelto a su estado original
SELECT id_usuario, nombre, cuota
FROM usuario 
WHERE id_usuario IN (
    SELECT invitador
    FROM usuario
    GROUP BY invitador
    HAVING COUNT(*) >= 2);

--------------------------------------------------------------------------------------
-- EJERCICIO 3. Modificar el valor de una clave primaria.

-- Desactivamos las restricciones de integridad necesarias 
ALTER TABLE usuario
DISABLE CONSTRAINT usuario_fk_invitador;

ALTER TABLE lista
DISABLE CONSTRAINT lista_fk_usuario;

ALTER TABLE usuario
DISABLE CONSTRAINT usuario_pk;

ALTER TABLE lista_cancion
DISABLE CONSTRAINT lista_fk1_usuario_lista;


-- Empezamos cambiando los datos en la tabla lista_cancion del usuario U001
UPDATE lista_cancion
SET usuario = 'U901'
WHERE usuario = 'U001';

-- Cambiamos lista el usuario propietario de las lista de U001 
UPDATE lista
SET usuario = 'U901'
WHERE usuario = 'U001';

-- Cambiamos el usuario invitador de usuarios invitados por U001 en USUARIO
UPDATE usuario
SET invitador = 'U901'
WHERE invitador = 'U001';

-- Por ultimo, en usuario Cambiamos el id_usuario del usuario U001 por U901
UPDATE usuario
SET id_usuario = 'U901'
WHERE id_usuario = 'U001';

-- Volvemos a habilitar las restricciones en orden inverso 
ALTER TABLE lista_cancion
ENABLE CONSTRAINT lista_fk1_usuario_lista;

ALTER TABLE usuario
ENABLE CONSTRAINT usuario_pk;

ALTER TABLE lista
ENABLE CONSTRAINT lista_fk_usuario;

ALTER TABLE usuario
ENABLE CONSTRAINT usuario_fk_invitador;


-- Comprobaciones

SELECT *
FROM usuario
WHERE id_usuario = 'U901';

--Esta consulta debe salir en blanco si no hay datos del U001.
SELECT *
FROM usuario
WHERE id_usuario = 'U001';

SELECT *
FROM lista
WHERE usuario = 'U901';

--Tambien en blanco
SELECT *
FROM LISTA
WHERE usuario = 'U001';

SELECT *
FROM LISTA_CANCION
WHERE usuario = 'U901';

--Tambien en blanco
SELECT *
FROM LISTA_CANCION
WHERE usuario = 'U001';

-- Hacemos los cambios permanentes
COMMIT;


--------------------------------------------------------------------------------------
-- EJERCICIO 4. Borrar algunas filas de una tabla.

-- NO HAYAN CREADO NINGULA LISTA


DELETE FROM USUARIO
WHERE id_usuario IN (SELECT id_usuario
                     FROM USUARIO
                     WHERE tipo = 'GRATUITO'
                       AND ultimo_acceso < TO_DATE('19/11/2019', 'dd/mm/yyyy')
                       AND id_usuario NOT IN (SELECT invitador
                                              FROM usuario
                                              WHERE invitador IS NOT NULL));

COMMIT;


--------------------------------------------------------------------------------------
-- EJERCICIO 5. Borrar algunas filas de varias tablas.

-- a)

-- primero desactivamos las tablas que puedan dar problemas
ALTER TABLE usuario
DISABLE CONSTRAINT usuario_fk_invitador;

ALTER TABLE lista
DISABLE CONSTRAINT lista_fk_usuario;

-- procedemos al borrado
DELETE FROM lista
WHERE usuario = 'U236';

DELETE FROM lista_cancion
WHERE usuario = 'U236';

DELETE FROM usuario
WHERE id_usuario = 'U236';

-- las volvemos a activar en orden inverso
ALTER TABLE lista
ENABLE CONSTRAINT lista_fk_usuario;

ALTER TABLE usuario
ENABLE CONSTRAINT usuario_fk_invitador;

COMMIT;


--------------------------------------------------------------------------------------
-- EJERCICIO 6. Eliminar algunas columnas.

-- a)

ALTER TABLE banda DROP COLUMN pais_origen;
ALTER TABLE banda DROP COLUMN a_fundacion;


-- b) No, no creo que sea posible hacerlo en una sola sentencia.


--------------------------------------------------------------------------------------
-- EJERCICIO 7. Crear y manipular una vista.

-- a)

CREATE VIEW datos_usuario AS
SELECT U.nombre usuario, tipo tipo, cuota cuota, 
       COUNT(DISTINCT num_lista) listas, COUNT(cancion) canciones, 
       TRUNC(SYSDATE - ultimo_acceso) desconexion
FROM usuario U LEFT JOIN lista L ON id_usuario = L.usuario
               LEFT JOIN lista_cancion LC ON L.usuario = LC.usuario AND num_lista = lista
WHERE tipo != 'GRATUITO'
GROUP BY U.nombre, tipo, cuota, ultimo_acceso;

-- b)

SELECT *
FROM datos_usuario
ORDER BY usuario;

-- c)
-- Usamos create or replace porque la vista ya esta creada, y luego modificamos 
-- el campo 'couta'.

CREATE OR REPLACE VIEW datos_usuario AS
SELECT U.nombre usuario, tipo tipo, cuota * 1.21 cuota, 
       COUNT(DISTINCT num_lista) listas, COUNT(cancion) canciones, 
       TRUNC(SYSDATE - ultimo_acceso) desconexion
FROM usuario U LEFT JOIN lista L ON id_usuario = L.usuario
               LEFT JOIN lista_cancion LC ON L.usuario = LC.usuario AND num_lista = lista
WHERE tipo != 'GRATUITO'
GROUP BY U.nombre, tipo, cuota, ultimo_acceso;

-- d)

INSERT INTO usuario (id_usuario, nombre, email, telefono, tipo, cuota, 
                        invitador, ultimo_acceso)
VALUES ('U299', 'CHOPIN', NULL, '+34555111300', 'PREMIUM DOS', 14, NULL, SYSDATE);

-- e)

SELECT *
FROM datos_usuario
ORDER BY usuario;

/*
Si aparece y tambien se le aplica el 21%.

En el momento que se realiza una consulta, la vista permite ver reflejados
los datos actuales de la tabla usuario. En conclusion, si se inserta un
nuevo usuario, se mostrara en la vista cuando se haga una consulta a posteriori.
Lo mismo sucede con el incremento del 21%
*/

COMMIT;


--------------------------------------------------------------------------------------
-- EJERCICIO 8. Restricciones de integridad.

SELECT *
FROM banda
WHERE NOT EXISTS (SELECT *
                  FROM musico
                  WHERE id_musico = lider AND banda = id_artista);

-- Como el resultado de esta SELECT es una tabla vacia, significa que 
-- se cumple el aserto


--------------------------------------------------------------------------------------
-- EJERCICIO 9. Creación y uso de índices.

-- a)

-- Coste tiene como valor 6

-- b)

CREATE INDEX idx_tipo_usuario ON usuario(tipo);

-- c)

-- El coste no ha mejorado sino todo lo contrario. Ahora este tiene un valor de 15
-- El indice que he creado se ha utilizado
