/*
Asignatura: Bases de Datos I
Curso: 2023/24
Convocatoria: enero

Practica: P3. Definicion y Modificacion de Datos en SQL

Equipo de practicas: bdi112
 Integrante 1: Javier Garcia Fernandez
*/

-- EJERCICIO 1. Insertar filas

-- Se recomienda INCLUIR AQUI una sentencia DELETE para cada tabla,
-- en el orden inverso al de insercion, pues eso permite la ejecucion
-- repetida de este script, mientras se depura el codigo

DELETE FROM musico;

DELETE FROM banda;

DELETE FROM lista_cancion;

DELETE FROM lista;

DELETE FROM usuario;

-- Insercion de datos en las tablas del esquema 

-- USUARIO --> 12 filas
ALTER TABLE usuario
DISABLE CONSTRAINT usuario_fk_invitador;

INSERT INTO USUARIO (id_usuario, nombre, email, telefono, tipo, cuota, invitador, ultimo_acceso)
VALUES ('U001', 'CASILDA', NULL, '+34555111000', 'PREMIUM INDIVIDUAL', 12, NULL, TO_DATE('15/01/2023', 'dd/mm/yyyy'));

INSERT INTO USUARIO (id_usuario, nombre, email, telefono, tipo, cuota, invitador, ultimo_acceso)
VALUES ('U035', 'BONIFACIO', NULL, '+34555444000', 'PREMIUM INDIVIDUAL', 12, 'U590', TO_DATE('16/06/2022', 'dd/mm/yyyy'));

INSERT INTO USUARIO (id_usuario, nombre, email, telefono, tipo, cuota, invitador, ultimo_acceso)
VALUES ('U590', 'NICANOR', 'nica@mail.com', NULL, 'GRATUITO', 0, 'U001', TO_DATE('25/02/2019', 'dd/mm/yyyy'));

INSERT INTO USUARIO (id_usuario, nombre, email, telefono, tipo, cuota, invitador, ultimo_acceso)
VALUES ('U112', 'TULIO', NULL, '+34555222000', 'PREMIUM DOS', 15, 'U001', TO_DATE('09/11/2022', 'dd/mm/yyyy'));

INSERT INTO USUARIO (id_usuario, nombre, email, telefono, tipo, cuota, invitador, ultimo_acceso)
VALUES ('U624', 'RENATA', 'rena@mail.com', NULL, 'GRATUITO', 0, 'U464', TO_DATE('21/12/2018', 'dd/mm/yyyy'));

INSERT INTO USUARIO (id_usuario, nombre, email, telefono, tipo, cuota, invitador, ultimo_acceso)
VALUES ('U252', 'MELANIO', NULL, '+34555333000', 'GRATUITO', 0, 'U112', TO_DATE('06/10/2019', 'dd/mm/yyyy'));

INSERT INTO USUARIO (id_usuario, nombre, email, telefono, tipo, cuota, invitador, ultimo_acceso)
VALUES ('U464', 'SILVANA', 'silv@mail.com', NULL, 'GRATUITO', 0, 'U112', TO_DATE('24/05/2020', 'dd/mm/yyyy'));

INSERT INTO USUARIO (id_usuario, nombre, email, telefono, tipo, cuota, invitador, ultimo_acceso)
VALUES ('U840', 'ANACLETA', 'anac@mail.com', NULL, 'GRATUITO', 0, 'U001', TO_DATE('14/02/2019', 'dd/mm/yyyy'));

INSERT INTO USUARIO (id_usuario, nombre, email, telefono, tipo, cuota, invitador, ultimo_acceso)
VALUES ('U555', 'TURIANO', 'turi@mail.com', NULL, 'GRATUITO', 0, 'U035', TO_DATE('15/06/2019', 'dd/mm/yyyy'));

INSERT INTO USUARIO (id_usuario, nombre, email, telefono, tipo, cuota, invitador, ultimo_acceso)
VALUES ('U236', 'JEREMIAS', 'jere@mail.com', NULL, 'PREMIUM DOS', 14, 'U840', TO_DATE('29/01/2023', 'dd/mm/yyyy'));

INSERT INTO USUARIO (id_usuario, nombre, email, telefono, tipo, cuota, invitador, ultimo_acceso)
VALUES ('U371', 'ROSAURA', NULL, '+34555555000', 'PREMIUM FAMILIAR', 25, NULL, TO_DATE('26/10/2018', 'dd/mm/yyyy'));

INSERT INTO USUARIO (id_usuario, nombre, email, telefono, tipo, cuota, invitador, ultimo_acceso)
VALUES ('U747', 'URBANO', 'urba@mail.com', NULL, 'GRATUITO', 0, 'U464', TO_DATE('30/11/2019', 'dd/mm/yyyy'));

ALTER TABLE usuario
ENABLE CONSTRAINT usuario_fk_invitador;

-- LISTA --> 11 filas
ALTER TABLE lista
DISABLE CONSTRAINT lista_fk_usuario;

INSERT INTO LISTA (usuario, num_lista, nombre, descripcion)
VALUES ('U001', 1, 'FIESTA!', 'Musica disco');
INSERT INTO LISTA (usuario, num_lista, nombre, descripcion)
VALUES ('U001', 2, 'RELAX', NULL);
INSERT INTO LISTA (usuario, num_lista, nombre, descripcion)
VALUES ('U001', 3, 'VIAJES', 'Para no dormirse al volante');

INSERT INTO LISTA (usuario, num_lista, nombre, descripcion)
VALUES ('U840', 1, 'RUNNING OUT', 'Correr por el monte');
INSERT INTO LISTA (usuario, num_lista, nombre, descripcion)
VALUES ('U840', 2, 'RUNNING IN', 'Correr por la ciudad');

INSERT INTO LISTA (usuario, num_lista, nombre, descripcion)
VALUES ('U464', 1, 'MI LISTA', 'Mientras programo SQL');

INSERT INTO LISTA (usuario, num_lista, nombre, descripcion)
VALUES ('U236', 1, 'FAVORITAS', NULL);
INSERT INTO LISTA (usuario, num_lista, nombre, descripcion)
VALUES ('U236', 2, 'TEMAZOS', 'Para venirse arriba');

INSERT INTO LISTA (usuario, num_lista, nombre, descripcion)
VALUES ('U371', 1, 'MI LISTA', NULL);

INSERT INTO LISTA (usuario, num_lista, nombre, descripcion)
VALUES ('U747', 1, 'MI LISTA', NULL);
INSERT INTO LISTA (usuario, num_lista, nombre, descripcion)
VALUES ('U747', 2, 'MI OTRA LISTA', NULL);

ALTER TABLE lista
ENABLE CONSTRAINT lista_fk_usuario;

-- LISTA_CANCION --> 63 filas

INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U001', 1, 'A001', 1, TO_DATE('01/01/2021', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U001', 1, 'A002', 2, TO_DATE('01/01/2021', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U001', 1, 'A003', 7, TO_DATE('03/03/2021', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U001', 1, 'A004', 4, TO_DATE('01/01/2021', 'dd/mm/yyyy'));

INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U001', 2, 'A001', 2, TO_DATE('22/06/2022', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U001', 2, 'A002', 4, TO_DATE('09/04/2022', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U001', 2, 'A003', 6, TO_DATE('03/03/2022', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U001', 2, 'A004', 2, TO_DATE('01/01/2023', 'dd/mm/yyyy'));

INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U001', 3, 'A010', 3, TO_DATE('10/05/2022', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U001', 3, 'A011', 5, TO_DATE('21/07/2022', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U001', 3, 'A012', 7, TO_DATE('30/03/2022', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U001', 3, 'A013', 3, TO_DATE('07/07/2022', 'dd/mm/yyyy'));

INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U840', 1, 'A006', 5, TO_DATE('01/01/2019', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U840', 1, 'A014', 6, TO_DATE('10/01/2019', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U840', 1, 'A012', 5, TO_DATE('12/01/2019', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U840', 1, 'A010', 6, TO_DATE('12/01/2019', 'dd/mm/yyyy'));

INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U840', 2, 'A014', 2, TO_DATE('01/02/2019', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U840', 2, 'A006', 2, TO_DATE('10/02/2019', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U840', 2, 'A002', 5, TO_DATE('12/02/2019', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U840', 2, 'A002', 1, TO_DATE('12/02/2019', 'dd/mm/yyyy'));

INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U464', 1, 'A002', 6, TO_DATE('14/09/2019', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U464', 1, 'A011', 5, TO_DATE('10/05/2020', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U464', 1, 'A003', 4, TO_DATE('10/05/2020', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U464', 1, 'A014', 3, TO_DATE('10/05/2020', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U464', 1, 'A001', 6, TO_DATE('20/05/2020', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U464', 1, 'A010', 5, TO_DATE('21/05/2020', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U464', 1, 'A002', 4, TO_DATE('22/05/2020', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U464', 1, 'A013', 3, TO_DATE('24/05/2020', 'dd/mm/yyyy'));

INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U236', 1, 'A005', 1, TO_DATE('12/01/2021', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U236', 1, 'A005', 2, TO_DATE('12/01/2021', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U236', 1, 'A005', 3, TO_DATE('12/01/2021', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U236', 1, 'A005', 4, TO_DATE('12/01/2021', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U236', 1, 'A005', 5, TO_DATE('12/01/2021', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U236', 1, 'A005', 6, TO_DATE('12/01/2021', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U236', 1, 'A005', 7, TO_DATE('12/01/2021', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U236', 1, 'A004', 1, TO_DATE('12/01/2021', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U236', 1, 'A004', 2, TO_DATE('12/01/2021', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U236', 1, 'A004', 3, TO_DATE('12/01/2021', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U236', 1, 'A004', 4, TO_DATE('12/01/2021', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U236', 1, 'A004', 5, TO_DATE('12/01/2021', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U236', 1, 'A004', 6, TO_DATE('12/01/2021', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U236', 1, 'A004', 7, TO_DATE('12/01/2021', 'dd/mm/yyyy'));

INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U236', 2, 'A007', 1, TO_DATE('29/08/2022', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U236', 2, 'A007', 2, TO_DATE('29/08/2022', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U236', 2, 'A013', 3, TO_DATE('20/08/2022', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U236', 2, 'A013', 4, TO_DATE('22/09/2022', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U236', 2, 'A013', 5, TO_DATE('31/08/2022', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U236', 2, 'A009', 3, TO_DATE('28/02/2023', 'dd/mm/yyyy'));

INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U371', 1, 'A009', 1, TO_DATE('26/01/2018', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U371', 1, 'A009', 7, TO_DATE('12/04/2018', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U371', 1, 'A008', 1, TO_DATE('30/05/2018', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U371', 1, 'A006', 1, TO_DATE('22/07/2018', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U371', 1, 'A006', 7, TO_DATE('31/08/2018', 'dd/mm/yyyy'));

INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U747', 1, 'A003', 1, TO_DATE('26/01/2019', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U747', 1, 'A009', 3, TO_DATE('27/01/2019', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U747', 1, 'A008', 3, TO_DATE('12/02/2019', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U747', 1, 'A011', 2, TO_DATE('28/02/2019', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U747', 1, 'A006', 7, TO_DATE('28/02/2019', 'dd/mm/yyyy'));

INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U747', 2, 'A003', 1, TO_DATE('29/01/2019', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U747', 2, 'A008', 3, TO_DATE('12/02/2019', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U747', 2, 'A009', 3, TO_DATE('22/03/2019', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U747', 2, 'A011', 2, TO_DATE('30/03/2019', 'dd/mm/yyyy'));
INSERT INTO LISTA_CANCION (usuario, lista, album, cancion, fecha)
VALUES ('U747', 2, 'A006', 7, TO_DATE('31/03/2019', 'dd/mm/yyyy'));

-- BANDA --> 5 filas
ALTER TABLE banda
DISABLE CONSTRAINT banda_fk_id_musico;

INSERT INTO BANDA ( id_artista, nombre, pais_origen, a_fundacion, lider)
VALUES ('B001', 'EURYTHMICS', 'Reino Unido', 1980, 'M001');
INSERT INTO BANDA ( id_artista, nombre, pais_origen, a_fundacion, lider)
VALUES ('B002', 'QUEEN', 'Reino Unido', 1970, 'M003');
INSERT INTO BANDA ( id_artista, nombre, pais_origen, a_fundacion, lider)
VALUES ('B003', 'RADIO FUTURA', 'Espana', 1979, 'M007');
INSERT INTO BANDA ( id_artista, nombre, pais_origen, a_fundacion, lider)
VALUES ('B004', 'VETUSTA MORLA', 'Espana', 1998, 'M010');
INSERT INTO BANDA ( id_artista, nombre, pais_origen, a_fundacion, lider)
VALUES ('B005', 'THE STROKES', 'Estados Unidos', 1998, 'M015');

/*
ALTER TABLE banda
ENABLE CONSTRAINT banda_fk_id_musico;
*/

-- MUSICO --> 19 filas
-- EURYTHMICS
ALTER TABLE musico
DISABLE CONSTRAINT musico_fk_id_album;

INSERT INTO MUSICO (id_musico, nombre, banda)
VALUES ('M001', 'ANNIE LENNOX', 'B001');
INSERT INTO MUSICO (id_musico, nombre, banda)
VALUES ('M002', 'DAVID A. STEWART', 'B001');
-- QUEEN
INSERT INTO MUSICO (id_musico, nombre, banda)
VALUES ('M003', 'FREDDY MERCURY', 'B002');
INSERT INTO MUSICO (id_musico, nombre, banda)
VALUES ('M004', 'BRIAN MAY', 'B002');
INSERT INTO MUSICO (id_musico, nombre, banda)
VALUES ('M005', 'ROGER TAYLOR', 'B002');
INSERT INTO MUSICO (id_musico, nombre, banda)
VALUES ('M006', 'JOHN DEACON', 'B002');
-- RADIO FUTURA
INSERT INTO MUSICO (id_musico, nombre, banda)
VALUES ('M007', 'SANTIAGO AUSERON', 'B003');
INSERT INTO MUSICO (id_musico, nombre, banda)
VALUES ('M008', 'LUIS AUSERON', 'B003');
INSERT INTO MUSICO (id_musico, nombre, banda)
VALUES ('M009', 'ENRIQUE SIERRA', 'B003');
-- VETUSTA MORLA
INSERT INTO MUSICO (id_musico, nombre, banda)
VALUES ('M010', 'PUCHO', 'B004');
INSERT INTO MUSICO (id_musico, nombre, banda)
VALUES ('M011', 'DAVID EL INDIO', 'B004');
INSERT INTO MUSICO (id_musico, nombre, banda)
VALUES ('M012', 'JORGE GONZALEZ', 'B004');
INSERT INTO MUSICO (id_musico, nombre, banda)
VALUES ('M013', 'GUILLERMO GALVAN', 'B004');
INSERT INTO MUSICO (id_musico, nombre, banda)
VALUES ('M014', 'JUANMA LATORRE', 'B004');
-- THE STROKES
INSERT INTO MUSICO (id_musico, nombre, banda)
VALUES ('M015', 'JULIAN CASABLANCAS', 'B005');
INSERT INTO MUSICO (id_musico, nombre, banda)
VALUES ('M016', 'NICK VALENSI', 'B005');
INSERT INTO MUSICO (id_musico, nombre, banda)
VALUES ('M017', 'ALBERT HAMMOND JR.', 'B005');
INSERT INTO MUSICO (id_musico, nombre, banda)
VALUES ('M018', 'NICOLAI GRAITURE', 'B005');
INSERT INTO MUSICO (id_musico, nombre, banda)
VALUES ('M019', 'FABRIZIO MORETTI', 'B005');

ALTER TABLE musico
ENABLE CONSTRAINT musico_fk_id_album;

-- THE END