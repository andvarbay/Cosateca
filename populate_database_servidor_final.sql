DROP TABLE IF EXISTS ListadoProducto;
DROP TABLE IF EXISTS CategoriaProducto;
DROP TABLE IF EXISTS Valoracion;
DROP TABLE IF EXISTS LogroUsuario;
DROP TABLE IF EXISTS EstadisticaUsuario;
DROP TABLE IF EXISTS Prestamo;
DROP TABLE IF EXISTS Mensaje;
DROP TABLE IF EXISTS Chat;
DROP TABLE IF EXISTS Reporte;
DROP TABLE IF EXISTS Listado;
DROP TABLE IF EXISTS Notificacion;
DROP TABLE IF EXISTS Producto;
DROP TABLE IF EXISTS Usuario;
DROP TABLE IF EXISTS Categoria;
DROP TABLE IF EXISTS Logro;
DROP TABLE IF EXISTS Estadistica;
DROP TABLE IF EXISTS listadoproducto;
DROP TABLE IF EXISTS categoriaproducto;
DROP TABLE IF EXISTS valoracion;
DROP TABLE IF EXISTS logrousuario;
DROP TABLE IF EXISTS estadisticausuario;
DROP TABLE IF EXISTS prestamo;
DROP TABLE IF EXISTS mensaje;
DROP TABLE IF EXISTS chat;
DROP TABLE IF EXISTS reporte;
DROP TABLE IF EXISTS listado;
DROP TABLE IF EXISTS notificacion;
DROP TABLE IF EXISTS producto;
DROP TABLE IF EXISTS usuario;
DROP TABLE IF EXISTS categoria;
DROP TABLE IF EXISTS logro;
DROP TABLE IF EXISTS estadistica;


CREATE TABLE estadistica (
    idEstadistica INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(40),
    descripcion VARCHAR(200)
);

CREATE TABLE logro(
    idLogro INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(30),
    descripcion VARCHAR(200)
);

CREATE TABLE categoria(
	idCategoria INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
	nombre varchar(20) NOT NULL UNIQUE
);

CREATE TABLE usuario (
    idUsuario INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(20),
    apellidos VARCHAR(50),
    correo VARCHAR(80) NOT NULL UNIQUE,
    contrasena VARCHAR(80) NOT NULL,
    nombreUsuario VARCHAR(20) NOT NULL UNIQUE,
    ubicacion VARCHAR(20),
    idProductosFavoritos VARCHAR(30) DEFAULT '',
    idUsuariosFavoritos VARCHAR(30) DEFAULT '',
    fotoPerfil VARCHAR(100),
    rol enum('administrador','usuario')
);

CREATE TABLE producto (
    idProducto INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(30) NOT NULL,
    descripcion VARCHAR(300),
    disponibilidad BOOLEAN NOT NULL,
    idPropietario INT NOT NULL,
    idCategorias VARCHAR(20),
    fechaSubida DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fotoProducto VARCHAR(100),
    FOREIGN KEY (idPropietario) REFERENCES usuario(idUsuario) ON DELETE CASCADE
);

CREATE TABLE estadisticausuario(
    idEstadisticaUsuario INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    idEstadistica INT NOT NULL,
    idUsuario INT NOT NULL,
    valor INT DEFAULT 0,
    FOREIGN KEY (idEstadistica) REFERENCES estadistica(idEstadistica),
    FOREIGN KEY (idUsuario) REFERENCES usuario(idUsuario)
);

CREATE TABLE logrousuario(
    idLogroUsuario INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    idLogro INT NOT NULL,
    idUsuario INT NOT NULL,
    fechaObtencion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (idLogro) REFERENCES logro(idLogro),
    FOREIGN KEY (idUsuario) REFERENCES usuario(idUsuario)
);

CREATE TABLE notificacion(
    idNotificacion INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    idUsuario INT NOT NULL,
    texto VARCHAR(100),
    fechaHora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (idUsuario) REFERENCES usuario(idUsuario) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE listado (
    idListado INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(20) NOT NULL DEFAULT 'Nuevo listado',
    idPropietario INT NOT NULL,
    FOREIGN KEY (idPropietario) REFERENCES usuario(idUsuario) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE reporte (
    idReporte INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    idEmisor INT NOT NULL,
    idReceptor INT NOT NULL,
    idProducto INT,
    descripcion VARCHAR(200),
    fechaHora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (idEmisor) REFERENCES usuario(idUsuario) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (idReceptor) REFERENCES usuario(idUsuario) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (idProducto) REFERENCES producto(idProducto) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE prestamo (
    idPrestamo INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    fechaInicio DATE NOT NULL,
    fechaFin DATE NOT NULL,
    idProducto INT,
    idArrendador INT NOT NULL,
    idArrendatario INT NOT NULL,
    condiciones VARCHAR(300) NOT NULL,
    estado enum('Pendiente', 'Aceptado', 'Denegado', 'Finalizado'),
    FOREIGN KEY (idProducto) REFERENCES producto(idProducto) ON UPDATE CASCADE ON DELETE SET NULL,
    FOREIGN KEY (idArrendador) REFERENCES usuario(idUsuario) ON UPDATE CASCADE,
    FOREIGN KEY (idArrendatario) REFERENCES usuario(idUsuario) ON UPDATE CASCADE
);

CREATE TABLE valoracion(
    idValoracion INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    idEmisor INT NOT NULL,
    idReceptor INT NOT NULL,
    puntuacion INT NOT NULL,
    comentario VARCHAR(300),
    idProducto INT,
    FOREIGN KEY (idProducto) REFERENCES producto(idProducto) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (idEmisor) REFERENCES usuario(idUsuario) ON UPDATE CASCADE,
    FOREIGN KEY (idReceptor) REFERENCES usuario(idUsuario) ON UPDATE CASCADE
);

CREATE TABLE chat (
    idChat INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    idUsuarioArrendador INT NOT NULL,
    idUsuarioArrendatario INT NOT NULL,
    idProducto INT,
    FOREIGN KEY (idProducto) REFERENCES producto(idProducto) ON UPDATE CASCADE ON DELETE CASCADE,
    FOREIGN KEY (idUsuarioArrendador) REFERENCES usuario(idUsuario) ON UPDATE CASCADE,
    FOREIGN KEY (idUsuarioArrendatario) REFERENCES usuario(idUsuario) ON UPDATE CASCADE
);

CREATE TABLE mensaje (
    idMensaje INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    idEmisor INT NOT NULL,
    fechaHora DATETIME NOT NULL,
    texto VARCHAR(200),
    idChat INT NOT NULL,
    FOREIGN KEY (idChat) REFERENCES chat(idChat) ON UPDATE CASCADE ON DELETE CASCADE
);

CREATE TABLE categoriaproducto(
    idCategoriaProducto INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    idCategoria INT NOT NULL,
    idProducto INT NOT NULL,

    FOREIGN KEY (idCategoria) REFERENCES categoria(idCategoria) ON DELETE CASCADE,
    FOREIGN KEY (idProducto) REFERENCES producto(idProducto) ON DELETE CASCADE
);

CREATE TABLE listadoproducto(
    idListadoProducto INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    idListado INT NOT NULL,
    idProducto INT,
    idUsuario INT,
    fechaAdicion DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (idListado) REFERENCES listado(idListado) ON DELETE CASCADE,
    FOREIGN KEY (idProducto) REFERENCES producto(idProducto) ON DELETE CASCADE,
    FOREIGN KEY (idUsuario) REFERENCES usuario(idUsuario) ON DELETE CASCADE
);

-- Inserts estadísticas
INSERT INTO estadistica(nombre, descripcion) VALUES
    ('Productos subidos', 'Número de productos de Cosateca subidos por tí'),
    ('Comentarios publicados', 'Número de comentarios en productos publicados'),
    ('Usuarios en favoritos','Número de usuarios guardados como favoritos'),
    ('Productos en favoritos', 'Número de productos en favoritos'),
    ('Préstamos realizados', 'Número de préstamos en los que has participado'),
    ('Préstamos como arrendador', 'Número de veces que has prestado un producto'),
    ('Préstamos como arrendatario', 'Número de veces que te han prestado un producto'),
    ('Valoraciones recibidas', 'Número de comentarios que has recibido en un producto o en tu perfil');

-- Insetrs logros
INSERT INTO logro(nombre, descripcion) VALUES 
    ('Bienvenido a Cosateca', 'Has creado una cuenta en Cosateca'),
    ('Proveedor novato', 'Has subido tu primer producto'),
    ('Proveedor intermedio', 'Has subido un total de 5 productos'),
    ('Proveedor experto', 'Has subido un total de 10 productos'),
    ('Repartiendo amor', 'Has guardado un usuario en favoritos'),
    -- 5
    -- 10
    -- 1  producto fav
    -- 5
    -- 10
    -- crear lista personalizddo
    -- 5
    -- 10
    -- añadir 1 a lista pers
    -- 5
    -- 10
    -- apatrullando la ciudad reporte
    ('Libertad de expresión', 'Publica tu primera valoración'),
    ('Valorando el mercado', 'Has valorado 5 productos o usuarios'),
    ('El juez', 'Has valorado 10 productos o usuarios'),
    ('En el punto de mira', 'Recibe tu primera valoracion de otro usuario'),
    ('La vieja confiable', 'Has recibido un total de 5 valoraciones'),
    ('Solo Dios puede juzgarme', 'Has recibido un total de 10 valoraciones'),
    ('Negocio local','Participa en tu primer préstamo.'),
    ('Hombre de negocios','Participa en 5 préstamos.'),
    ('Usuario de honor','Participa en 10 préstamos.'),
    ('Arrendador primerizo','Participa en tu primer préstamo como arrendador.'),
    ('Arrendador ocasional','Participa 5 préstamos como arrendador.'),
    ('Arrendando que es gerundio','Participa en 10 préstamos como arrendador.'),
    ('Arrendatario primerizo','Participa en tu primer préstamo como arrendatario.'),
    ('Arrendatario ocasional','Participa en 5 préstamos como arrendatario.'),
    ('Arrendatando que es gerundio','Participa en 10 préstamos como arrendatario.');

-- Inserts Categorias
INSERT INTO categoria(nombre) VALUES 
    ('Indumentaria'),
    ('Carpintería'),
    ('Mecánica'),
    ('Eléctrico'),
    ('Juguetes'),
    ('Material Deportivo');

-- Inserts Usuarios
INSERT INTO usuario(nombre, apellidos, correo, contrasena, nombreUsuario, ubicacion, rol) VALUES 
    ('Pablo', 'Vazquez', 'pablester@gmail.com', MD5('pablester123'), 'pablester', 'Monesterio', 'usuario'),
    ('Sergio', 'Delgado', 'serginho@gmail.com', MD5('serginho123'), 'serginho', 'Monesterio', 'usuario'),
    ('Antonio', 'Gonzalez', 'antoniokroos14@gmail.com', MD5('antoniokroos14123'), 'antoniokroos14', 'Monesterio', 'usuario'),
    ('Carlos', 'Vasco', 'alteza@gmail.com', MD5('sutremendalteza123'), 'carlosv', 'Monesterio', 'usuario');

-- Inserts Productos
INSERT INTO producto(nombre, descripcion, disponibilidad, idPropietario, idCategorias, fechaSubida) VALUES 
    ('Taladradora eléctrica','Con potente motor de 2 velocidades. Atornilladora taladradora electrica, con portabrocas extraible para un cambio rapido y sin herramientas.', TRUE, 1, '2,3,4', '2023-07-12 19:08:40'),
    ('Pies de gato escalada','Talla 43, perfectos para hacer escalada en el rocodromo.', TRUE, 3, '6', '2023-07-08 11:21:10'),
    ('Serrucho 400 mm', 'Serrucho fabricado en acero templado con mango de plastico y hoja antioxido de 40 cm. Tiene un angulo de corte de 90° y 8 dientes por pulgada.', TRUE, 2, '2', '2023-07-20 13:08:33');

-- Inserts Notificaciones
INSERT INTO notificacion(idUsuario, texto) VALUES
    (1, 'Tu Cuenta ha sido creada con exito'),
    (2, 'Tu Cuenta ha sido creada con exito'),
    (3, 'Tu Cuenta ha sido creada con exito'),
    (4, 'Tu Cuenta ha sido creada con exito');

-- Inserts Listados
INSERT INTO listado(nombre,idPropietario) VALUES 
    ('Usuarios Favoritos', 1),
    ('Usuarios Favoritos', 2),
    ('Usuarios Favoritos', 3),
    ('Usuarios Favoritos', 4),
    ('Productos Favoritos', 1),
    ('Productos Favoritos', 2),
    ('Productos Favoritos', 3),
    ('Productos Favoritos', 4),
    ('Mi lista', 1),
    ('Carpintería jardín', 4),
    ('Boda de mis primos',2),
    ('aaaaaaaa', 2);

-- Inserts Reportes
INSERT INTO reporte(idEmisor, idReceptor, idProducto, descripcion) VALUES 
    (2,1,1,'La herramienta no funciona. Deberían eliminar al usuario de la plataforma. Estoy muy enfadado.'),
    (1,3,2, 'Me dijo que los pies de gato eran de la talla 43, pero le quedan bien a mi sobrina que tiene un 34.'),
    (1,2,3, 'Esta sierra no corta, los arboles de mi jardín se ríen de mí.');

-- Inserts Prestamos
INSERT INTO prestamo(fechaInicio, fechaFin, idProducto, idArrendador, idArrendatario, condiciones, estado) VALUES 
    ('2023-07-23', '2023-08-01', 3, 2, 3, 'El producto sera devuelto en mano el dia estipulado', 'Finalizado'),
    ('2023-07-26', '2023-08-02', 2, 3, 1, 'En caso de que los rompa, tiene que abonar 10 euros', 'Finalizado');

-- Inserts Valoraciones
INSERT INTO valoracion(idEmisor,idReceptor,puntuacion,comentario,idProducto) VALUES
    (3,2,5,'Muy educado y puntual',null),
    (1,3,0,'Miente con la talla, son un 34 no un 43',2);

-- Inserts EstadísticasUsuarios
INSERT INTO estadisticausuario(idEstadistica,idUsuario, valor) VALUES
    (1,1,0),(2,1,1),(3,1,0),(4,1,1),(5,1,0),(6,1,0),(7,1,1),(8,1,1),
    (1,2,1),(2,2,0),(3,2,1),(4,2,1),(5,2,0),(6,2,0),(7,2,0),(8,2,1),
    (1,3,1),(2,3,1),(3,3,1),(4,3,2),(5,3,0),(6,3,0),(7,3,1),(8,3,1),
    (1,4,0),(2,4,0),(3,4,0),(4,4,0),(5,4,0),(6,4,0),(7,4,0),(8,4,0);

-- Inserts LogrosUsuarios
INSERT INTO logrousuario(idLogro, idUsuario, fechaObtencion) VALUES
    (1,1,'2023-06-08'),(1,2,'2023-06-09'),(1,3,'2023-06-10'),(1,4,'2023-06-11'),
    (2,1,'2023-06-08'),(2,2,'2023-06-09'),(2,3,'2023-06-10'),
    (12,1,'2023-06-08'),(12,2,'2023-06-09'),(12,3,'2023-06-10'),
    (18,1,'2023-06-08'),(15,2,'2023-06-09'),(18,3,'2023-06-10'),(15,3,'2023-06-11'),
    (6,1,'2023-06-08'),(9,2,'2023-06-09'),(6,3,'2023-06-10'),(9,3,'2023-06-11');

-- Inserts Chats
INSERT INTO chat(idUsuarioArrendador, idUsuarioArrendatario, idProducto) VALUES 
    (2,3,3),(3,1,2);

-- Inserts Mensajes
INSERT INTO mensaje(idEmisor, fechaHora, texto, idChat) VALUES 
    (3, '2023-07-23 11:08:40', 'Buenas tardes, estoy interesado en este producto', 1),
    (3, '2023-07-23 11:08:45', 'Me lo podria prestar hasta el dia 1 de Agosto?', 1),
    (2, '2023-07-23 12:43:44', 'Buenas tardes, caballero', 1),
    (3, '2023-07-23 11:08:40', 'Estupendo, asi no lo tengo aqui escupando espacio jajaja', 1);

-- Inserts CategoriasProductos
INSERT INTO categoriaproducto(idCategoria,idProducto) VALUES
    (6,2),
    (6,3),
    (4,1),
    (2,1);

-- Inserts ListadosProductos
INSERT INTO listadoproducto(idListado,idProducto,idUsuario) VALUES
    (6,2,null),
    (6,3,null),
    (4,null,1),
    (2,null,3);