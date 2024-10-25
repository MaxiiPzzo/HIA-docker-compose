USE corporacionDB;

CREATE TABLE `fichaMedica` (
  `fim_id` bigint PRIMARY KEY AUTO_INCREMENT,
  `fecha_creacion` date NOT NULL,
  `grupo_sanguineo` varchar(3) NOT NULL,
  `alergias` text,
  `antecedentes` text
);

CREATE TABLE `domicilio` (
  `doc_id` bigint PRIMARY KEY AUTO_INCREMENT,
  `calle` varchar(150) NOT NULL,
  `numero` smallint,
  `barrio` varchar(100),
  `localidad` varchar(100) NOT NULL,
  `provincia` varchar(100) NOT NULL
);

CREATE TABLE `datosPersonales` (
  `dtp_id` bigint PRIMARY KEY AUTO_INCREMENT,
  `dni` bigint UNIQUE,
  `apellido` varchar(100) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `fecha_nacimiento` date NOT NULL,
  `cuil` bigint UNIQUE,
  `sexo` char(1) NOT NULL,
  `estado_civil` varchar(50),
  `nivel_estudio` varchar(100),
  `nacionalidad` varchar(100),
  `domicilio_id` bigint UNIQUE NOT NULL,
  `ficha_medica_id` bigint UNIQUE NOT NULL
);

CREATE TABLE `personaGrupoFamiliar` (
  `pgf_id` bigint PRIMARY KEY,
  `nombre` varchar(100) NOT NULL,
  `dni` bigint UNIQUE,
  `apellido` varchar(100) NOT NULL,
  `fecha_nac` date NOT NULL
);

CREATE TABLE `grupoFamiliar` (
  `emp_id` bigint,
  `persona_gf` bigint,
  `vinculo` varchar(50),
  PRIMARY KEY (`emp_id`, `persona_gf`)
);

CREATE TABLE `categoria` (
  `cat_id` smallint PRIMARY KEY AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `resolucion` varchar(50)
);

CREATE TABLE `funcion` (
  `fun_id` smallint PRIMARY KEY AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL,
  `resolucion` varchar(50)
);

CREATE TABLE `departamento` (
  `dep_id` smallint PRIMARY KEY AUTO_INCREMENT,
  `nombre` varchar(50) NOT NULL
);

CREATE TABLE `designacion` (
  `des_id` bigint PRIMARY KEY AUTO_INCREMENT,
  `categoria_id` smallint NOT NULL,
  `funcion_id` smallint NOT NULL,
  `departamento_id` smallint NOT NULL,
  `fecha_designacion` date NOT NULL,
  `novedad_id` bigint UNIQUE
);

CREATE TABLE `designacionAudit` (
  `id` bigint PRIMARY KEY AUTO_INCREMENT,
  `des_id` bigint NOT NULL,
  `novedad_id` bigint NOT NULL, -- Permitira agrupar a los registros del historia por novedad
  `nombre_columna` varchar(50) NOT NULL,
  `valor_anterior` smallint,
  `valor_nuevo` smallint,
  `fecha_cambio` date DEFAULT (CURRENT_DATE)
);

CREATE TABLE `empleado` (
  `emp_id` bigint PRIMARY KEY AUTO_INCREMENT,
  `datos_personales_id` bigint UNIQUE,
  `expediente_id` bigint UNIQUE NOT NULL,
  `designacion_id` bigint UNIQUE NOT NULL,
  `fecha_ingreso` date,
  `horario_trabajo` time,
  `turno` ENUM ('Part-time', 'Full-time', 'Temporal')
);

CREATE TABLE `ausencia` (
  `aus_id` bigint PRIMARY KEY AUTO_INCREMENT,
  `exp_id` bigint NOT NULL,
  `fecha` date NOT NULL DEFAULT (CURRENT_DATE)
);

CREATE TABLE `tardanza` (
  `tar_id` bigint PRIMARY KEY AUTO_INCREMENT,
  `exp_id` bigint NOT NULL,
  `fecha_hora` timestamp NOT NULL DEFAULT (CURRENT_TIMESTAMP)
);

CREATE TABLE `novedad` (
  `nov_id` bigint PRIMARY KEY AUTO_INCREMENT,
  `exp_id` bigint NOT NULL,
  `tipo` ENUM('Ingreso', 'Ascenso', 'Reingreso', 'Transferencia', 'Promoción', 'Salida') NOT NULL,
  `fecha_emision` date NOT NULL DEFAULT (CURRENT_DATE),
  `observaciones` text
);

CREATE TABLE `sancion` (
  `san_id` bigint PRIMARY KEY,
  `nombre` varchar(100),
  `articulo` varchar(100),
  `fecha_emision` date DEFAULT (CURRENT_DATE),
  `observacion` text,
  `exp_id` bigint
);

CREATE TABLE `parteMedico` (
  `pmd_id` bigint PRIMARY KEY,
  `fecha_emision` date NOT NULL DEFAULT (CURRENT_DATE),
  `motivo` text NOT NULL,
  `dias_discapacidad` integer NOT NULL,
  `par_id` bigint UNIQUE NOT NULL
);

CREATE TABLE `parte` (
  `par_id` bigint PRIMARY KEY,
  `exp_id` bigint NOT NULL,
  `tipo` ENUM ('Médico', 'Licencia', 'Accidente', 'Disciplinario', 'Permiso Ausencia') NOT NULL,
  `fecha_inicio` date NOT NULL,
  `fecha_finalizacion` date NOT NULL,
  `observaciones` text,
  `estado` varchar(50)
);

CREATE TABLE `expediente` (
  `exp_id` bigint PRIMARY KEY AUTO_INCREMENT,
  `legajo` int UNIQUE,
  `num_exp` int,
  `libro` varchar(50),
  `tomo` varchar(50),
  `fajos` bigint
);

CREATE TABLE `titulo` (
  `tit_id` bigint PRIMARY KEY,
  `exp_id` bigint NOT NULL,
  `nombre` varchar(50),
  `nombre_institucion` varchar(100),
  `fecha_emision` date,
  `matricula` bigint
);

-- CONFIGURACIÓN DE CLAVES FORANEAS

ALTER TABLE `datosPersonales` ADD FOREIGN KEY (`domicilio_id`) REFERENCES `domicilio` (`doc_id`);

ALTER TABLE `datosPersonales` ADD FOREIGN KEY (`ficha_medica_id`) REFERENCES `fichaMedica` (`fim_id`);

ALTER TABLE `grupoFamiliar` ADD FOREIGN KEY (`emp_id`) REFERENCES `empleado` (`emp_id`) ON DELETE CASCADE;

ALTER TABLE `grupoFamiliar` ADD FOREIGN KEY (`persona_gf`) REFERENCES `personaGrupoFamiliar` (`pgf_id`) ON DELETE RESTRICT;

ALTER TABLE `designacion` ADD FOREIGN KEY (`categoria_id`) REFERENCES `categoria` (`cat_id`);

ALTER TABLE `designacion` ADD FOREIGN KEY (`departamento_id`) REFERENCES `departamento` (`dep_id`);

ALTER TABLE `designacion` ADD FOREIGN KEY (`funcion_id`) REFERENCES `funcion` (`fun_id`);

ALTER TABLE `designacion` ADD FOREIGN KEY (`novedad_id`) REFERENCES `novedad` (`nov_id`);

ALTER TABLE `empleado` ADD FOREIGN KEY (`datos_personales_id`) REFERENCES `datosPersonales` (`dtp_id`) ON DELETE RESTRICT; 

ALTER TABLE `empleado` ADD FOREIGN KEY (`designacion_id`) REFERENCES `designacion` (`des_id`) ON DELETE RESTRICT;

ALTER TABLE `empleado` ADD FOREIGN KEY (`expediente_id`) REFERENCES `expediente` (`exp_id`) ON DELETE RESTRICT;

ALTER TABLE `ausencia` ADD FOREIGN KEY (`exp_id`) REFERENCES `expediente` (`exp_id`);

ALTER TABLE `tardanza` ADD FOREIGN KEY (`exp_id`) REFERENCES `expediente` (`exp_id`);

ALTER TABLE `novedad` ADD FOREIGN KEY (`exp_id`) REFERENCES `expediente` (`exp_id`);

ALTER TABLE `sancion` ADD FOREIGN KEY (`exp_id`) REFERENCES `expediente` (`exp_id`);

ALTER TABLE `parteMedico` ADD FOREIGN KEY (`par_id`) REFERENCES `parte` (`par_id`);

ALTER TABLE `parte` ADD FOREIGN KEY (`exp_id`) REFERENCES `expediente` (`exp_id`);

ALTER TABLE `titulo` ADD FOREIGN KEY (`exp_id`) REFERENCES `expediente` (`exp_id`);

ALTER TABLE `designacionAudit` ADD FOREIGN KEY (`des_id`) REFERENCES `designacion` (`des_id`);

ALTER TABLE `designacionAudit` ADD FOREIGN KEY (`novedad_id`) REFERENCES `novedad` (`nov_id`);

-- TRIGGERS PARA TABLA AUDIT DE DESIGNACION
DELIMITER //
CREATE TRIGGER trg_designacion_insert
AFTER INSERT ON designacion
FOR EACH ROW
BEGIN

    INSERT INTO `designacionAudit` (
        des_id, novedad_id, nombre_columna, valor_nuevo
    ) VALUES (
       NEW.des_id, NEW.novedad_id, 'categoria_id', NEW.categoria_id
    );

    INSERT INTO `designacionAudit` (
        des_id, novedad_id, nombre_columna, valor_nuevo
    ) VALUES (
       NEW.des_id, NEW.novedad_id, 'funcion_id', NEW.funcion_id
    );

    INSERT INTO `designacionAudit` (
        des_id, novedad_id, nombre_columna, valor_nuevo
    ) VALUES (
       NEW.des_id, NEW.novedad_id, 'departamento_id', NEW.departamento_id
    );

END//
DELIMITER ;

DELIMITER //
CREATE TRIGGER trg_designacion_update
AFTER UPDATE ON designacion
FOR EACH ROW
BEGIN

  IF OLD.categoria_id <> NEW.categoria_id THEN
    INSERT INTO designacionAudit (des_id, novedad_id, nombre_columna, valor_anterior, valor_nuevo, fecha_cambio)
    VALUES (NEW.des_id, NEW.novedad_id, 'categoria_id', OLD.categoria_id, NEW.categoria_id, CURRENT_DATE);
  END IF;

  IF OLD.funcion_id <> NEW.funcion_id THEN
    INSERT INTO designacionAudit (des_id, novedad_id, nombre_columna, valor_anterior, valor_nuevo, fecha_cambio)
    VALUES (NEW.des_id, NEW.novedad_id, 'funcion_id', OLD.funcion_id, NEW.funcion_id, CURRENT_DATE);
  END IF;

  IF OLD.departamento_id <> NEW.departamento_id THEN
    INSERT INTO designacionAudit (des_id, novedad_id, nombre_columna, valor_anterior, valor_nuevo, fecha_cambio)
    VALUES (NEW.des_id, NEW.novedad_id, 'departamento_id', OLD.departamento_id, NEW.departamento_id, CURRENT_DATE);
  END IF;

END;//
DELIMITER ;

DELIMITER //
CREATE TRIGGER trg_designacion_delete
AFTER DELETE ON designacion
FOR EACH ROW
BEGIN

    INSERT INTO `designacionAudit` (
        des_id, novedad_id, nombre_columna, valor_anterior
    ) VALUES (
       OLD.des_id, OLD.novedad_id, 'categoria_id', OLD.categoria_id
    );

    INSERT INTO `designacionAudit` (
        des_id, novedad_id, nombre_columna, valor_anterior
    ) VALUES (
       OLD.des_id, OLD.novedad_id, 'funcion_id', OLD.funcion_id
    );

    INSERT INTO `designacionAudit` (
        des_id, novedad_id, nombre_columna, valor_anterior
    ) VALUES (
       OLD.des_id, OLD.novedad_id, 'departamento_id', OLD.departamento_id
    );

END//
DELIMITER ;