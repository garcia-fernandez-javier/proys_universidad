/*
Asignatura: Bases de Datos I
Curso: 2023/24
Convocatoria: enero

Practica: P3. Definicion y Modificacion de Datos en SQL

Equipo de practicas: bdi122
 Integrante 1: Javier Garcia Fernandez
*/

-- EJERCICIO 0. Corregir/mejorar script de creacion

-- opcional:
-- Sentencias DROP para re-ejecucion del script
-- en el orden inverso al de creacion


DROP TABLE lista_cancion;

DROP TABLE banda CASCADE CONSTRAINTS;

DROP TABLE musico;

DROP TABLE lista;

DROP TABLE usuario;    


-- Sentencias CREATE (y ALTER) para crear las tablas del esquema
-- en el orden que evite errores de integridad referencial

-- Para los identificadores, si son alfanumericos, char(4)
-- Si son numericos, number(2)
-- Para un nombre, varchar(30) (los textos van en comillas simples)
-- Para las fechas completas, un date



CREATE TABLE usuario(
    id_usuario      CHAR(4)                             NOT NULL,
    nombre          VARCHAR2(30)                        NOT NULL,
    email           VARCHAR2(30)                        NULL,
    telefono        NUMBER(12,0)                        NULL,
    tipo            VARCHAR (30) DEFAULT 'GRATUITO'     NOT NULL,
    cuota           NUMBER(4,2)                         NOT NULL,
    invitador       CHAR(4)                             NULL,
    ultimo_acceso   DATE                                NOT NULL,
    
    
    CONSTRAINT usuario_pk PRIMARY KEY(id_usuario),
    CONSTRAINT usuario_ak1 UNIQUE(email),
    CONSTRAINT usuario_ak2 UNIQUE(telefono),
    CONSTRAINT usuario_fk_invitador
        FOREIGN KEY (invitador) REFERENCES usuario(id_usuario),
        -- ON DELETE SET NULL
        -- ON UPDATE CASCADE
    
    CONSTRAINT usuario_chek
        CHECK ((email IS NOT NULL AND telefono IS NULL) OR
               (email IS NULL AND telefono IS NOT NULL)),
        CHECK (id_usuario != invitador),
        CHECK (tipo IN ('GRATUITO', 'PREMIUM INDIVIDUAL', 
                        'PREMIUM DOS','PREMIUM FAMILIAR'))
);


CREATE TABLE lista(
    usuario         CHAR(4)         NOT NULL,
    num_lista       NUMBER(2)       NOT NULL,
    nombre          VARCHAR2(30)    NOT NULL,
    descripcion     VARCHAR(30)     NULL,
    
    CONSTRAINT lista_pk PRIMARY KEY(usuario, num_lista),
    CONSTRAINT lista_fk_usuario
        FOREIGN KEY (usuario) REFERENCES usuario(id_usuario),
        -- ON DELETE CASCADE
        -- ON UPDATE CASCADE

    CONSTRAINT lista_chek
        CHECK (num_lista > 0)
);


CREATE TABLE musico(
    id_musico       CHAR(4)         NOT NULL,
    nombre          VARCHAR2(30)    NOT NULL,
    banda           CHAR(4)         NOT NULL,

    CONSTRAINT musico_pk PRIMARY KEY(id_musico)
);


CREATE TABLE banda(
    id_artista      CHAR(4)         NOT NULL,
    nombre          VARCHAR2(30)    NOT NULL,
    pais_origen     VARCHAR2(30)    NULL,
    a_fundacion     NUMBER(2)       NOT NULL,
    lider           CHAR(4)         NOT NULL, 
    
    CONSTRAINT banda_pk PRIMARY KEY(id_artista),
    CONSTRAINT banda_ak1 UNIQUE(nombre),
    CONSTRAINT banda_ak2 UNIQUE(lider),
    
    CONSTRAINT banda_fk_id_musico
        FOREIGN KEY (lider) REFERENCES musico(id_musico)
        -- ON DELETE NO ACTION
        -- ON UPDATE CASCADE
);


CREATE TABLE lista_cancion(
    usuario         CHAR(4)         NOT NULL,
    lista           NUMBER(2)       NOT NULL,
    album           CHAR(4)    NOT NULL,
    cancion         NUMBER(2)      NOT NULL,
    fecha           DATE            NOT NULL,
    
    CONSTRAINT lista_cancion_pk PRIMARY KEY(usuario, lista, album, cancion),

    CONSTRAINT lista_fk1_usuario_lista
        FOREIGN KEY (usuario,lista) REFERENCES lista(usuario, num_lista)
        -- ON DELETE CASCADE
        -- ON UPDATE CASCADE
    -- CONSTRAINT lista_fk2_usuario_lista
        -- FOREIGN KEY (album,cancion) REFERENCES cancion(id_usuario, num_lista)
        -- ON DELETE CASCADE
        -- ON UPDATE CASCADE
);


ALTER TABLE musico ADD
    CONSTRAINT musico_fk_id_album
        FOREIGN KEY (banda) REFERENCES banda(id_artista);
        -- ON DELETE NO ACTION
        -- ON UPDATE CASCADE