
CREATE TABLE lugar_cultural (
    Cod_Localidad int,
    IdProvincia int,
    IdDepartamento int,
    Categoria varchar(255),
    Provincia varchar(255),
    Localidad varchar(255),
    Nombre varchar(255),
    Domicilio varchar(255),
    CP varchar(255),
    Telefono varchar(255),
    Mail varchar(255),
    Web varchar(255),
    Fecha_carga varchar(255)
);

CREATE TABLE totales_categoria (
    Provincia varchar(255),
    Bibliotecas_Populares int,
    Espacios_de_Exhibición_Patrimonial int,
    Salas_de_cine int,
    Total int,
    Fecha_carga varchar(255)
)

CREATE TABLE totales_cines (
    Provincia varchar(255)
    Pantallas int
    Butacas int
    espacio_INCAA int
    Fecha_carga varchar(255)
)