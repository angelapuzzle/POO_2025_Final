CREATE TABLE t_ciudades(
  Id_Departamento INTEGER NOT NULL,
  Id_Ciudad INTEGER NOT NULL,
  Nombre_Departamento TEXT,
  Nombre_Ciudad TEXT,
  PRIMARY KEY(Id_Departamento, Id_Ciudad));


CREATE TABLE [t_participantes](
  [Id] BIGINT(15) PRIMARY KEY NOT NULL UNIQUE, 
  [Nombre] VARCHAR(50), 
  [Direccion] VARCHAR(50), 
  [Celular] INTEGER(10), 
  [Entidad] VARCHAR(50), 
  [Fecha] DATE(10), 
  [Id_Departamento] INTEGER REFERENCES [t_ciudades]([Id_Departamento]), 
  [Id_Ciudad] INTEGER REFERENCES [t_ciudades]([Id_Ciudad]));

.mode csv
.import t_ciudades.csv t_ciudades