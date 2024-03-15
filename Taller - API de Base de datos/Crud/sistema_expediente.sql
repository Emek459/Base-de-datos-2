-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versión del servidor:         5.7.42-log - MySQL Community Server (GPL)
-- SO del servidor:              Win32
-- HeidiSQL Versión:             12.5.0.6677
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Volcando estructura de base de datos para sistema_expediente
CREATE DATABASE IF NOT EXISTS `sistema_expediente` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `sistema_expediente`;

-- Volcando estructura para tabla sistema_expediente.aseguradora
CREATE TABLE IF NOT EXISTS `aseguradora` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_aseguradora` varchar(100) NOT NULL,
  `ruc` varchar(20) DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  `contacto` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla sistema_expediente.cita
CREATE TABLE IF NOT EXISTS `cita` (
  `id_cita` int(11) NOT NULL AUTO_INCREMENT,
  `usuario_id` int(11) DEFAULT NULL,
  `aseguradora_id` int(11) DEFAULT NULL,
  `juzgado_id` int(11) DEFAULT NULL,
  `fecha_created` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `fecha_cita` date DEFAULT NULL,
  `status` enum('programada','realizada','cancelada') DEFAULT 'programada',
  PRIMARY KEY (`id_cita`),
  KEY `usuario_id` (`usuario_id`),
  KEY `aseguradora_id` (`aseguradora_id`),
  KEY `juzgado_id` (`juzgado_id`),
  CONSTRAINT `cita_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`usuario_id`),
  CONSTRAINT `cita_ibfk_2` FOREIGN KEY (`aseguradora_id`) REFERENCES `aseguradora` (`id`),
  CONSTRAINT `cita_ibfk_3` FOREIGN KEY (`juzgado_id`) REFERENCES `juzgado` (`id_juzgado`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla sistema_expediente.expediente
CREATE TABLE IF NOT EXISTS `expediente` (
  `expediente_id` int(11) NOT NULL AUTO_INCREMENT,
  `conductor` varchar(100) NOT NULL,
  `aseguradora_id` int(11) DEFAULT NULL,
  `numero_de_caso` varchar(50) NOT NULL,
  `tipo_de_proceso` varchar(50) DEFAULT NULL,
  PRIMARY KEY (`expediente_id`),
  KEY `aseguradora_id` (`aseguradora_id`),
  CONSTRAINT `expediente_ibfk_1` FOREIGN KEY (`aseguradora_id`) REFERENCES `aseguradora` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=16 DEFAULT CHARSET=latin1;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla sistema_expediente.juzgado
CREATE TABLE IF NOT EXISTS `juzgado` (
  `id_juzgado` int(11) NOT NULL AUTO_INCREMENT,
  `nombre_juzgado` varchar(100) NOT NULL,
  `corregimiento` varchar(100) DEFAULT NULL,
  `distrito` varchar(100) DEFAULT NULL,
  `direccion` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_juzgado`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla sistema_expediente.reporte
CREATE TABLE IF NOT EXISTS `reporte` (
  `id_reporte` int(11) NOT NULL AUTO_INCREMENT,
  `usuario_id` int(11) DEFAULT NULL,
  `expediente_id` int(11) DEFAULT NULL,
  `cita_id` int(11) DEFAULT NULL,
  `fecha` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id_reporte`),
  KEY `usuario_id` (`usuario_id`),
  KEY `expediente_id` (`expediente_id`),
  KEY `cita_id` (`cita_id`),
  CONSTRAINT `reporte_ibfk_1` FOREIGN KEY (`usuario_id`) REFERENCES `usuario` (`usuario_id`),
  CONSTRAINT `reporte_ibfk_2` FOREIGN KEY (`expediente_id`) REFERENCES `expediente` (`expediente_id`),
  CONSTRAINT `reporte_ibfk_3` FOREIGN KEY (`cita_id`) REFERENCES `cita` (`id_cita`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=latin1;

-- La exportación de datos fue deseleccionada.

-- Volcando estructura para tabla sistema_expediente.usuario
CREATE TABLE IF NOT EXISTS `usuario` (
  `usuario_id` int(11) NOT NULL AUTO_INCREMENT,
  `nombre` varchar(100) NOT NULL,
  `correo` varchar(100) NOT NULL,
  `contrasena` varchar(255) NOT NULL,
  PRIMARY KEY (`usuario_id`),
  UNIQUE KEY `correo` (`correo`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=latin1;

-- La exportación de datos fue deseleccionada.

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
