-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema clinic
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema clinic
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `clinic` DEFAULT CHARACTER SET utf8 ;
USE `clinic` ;

-- -----------------------------------------------------
-- Table `clinic`.`patients`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `clinic`.`patients` (
  `patient_id` SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(50) NOT NULL,
  `last_name` VARCHAR(50) NOT NULL,
  `address` VARCHAR(500) NOT NULL,
  `history` VARCHAR(500) NOT NULL,
  `case` CHAR(1) NOT NULL,
  PRIMARY KEY (`patient_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 9
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `clinic`.`invoices`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `clinic`.`invoices` (
  `invoice_id` SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `patient_id` SMALLINT UNSIGNED NOT NULL,
  `payment_date` DATE NOT NULL,
  `consulting` DECIMAL(7,2) UNSIGNED NOT NULL,
  `payment` DECIMAL(7,2) UNSIGNED NOT NULL,
  `pending` DECIMAL(7,2) NOT NULL,
  PRIMARY KEY (`invoice_id`),
  INDEX `fk_invoices_patients1_idx` (`patient_id` ASC) VISIBLE,
  CONSTRAINT `fk_invoices_patients1`
    FOREIGN KEY (`patient_id`)
    REFERENCES `clinic`.`patients` (`patient_id`)
    ON UPDATE CASCADE)
ENGINE = InnoDB
AUTO_INCREMENT = 13
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `clinic`.`next_appointment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `clinic`.`next_appointment` (
  `appointment_id` SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `patient_id` SMALLINT UNSIGNED NOT NULL,
  `date` DATE NOT NULL,
  PRIMARY KEY (`appointment_id`),
  INDEX `fk_next_appointment_patients_idx` (`patient_id` ASC) VISIBLE,
  CONSTRAINT `fk_next_appointment_patients`
    FOREIGN KEY (`patient_id`)
    REFERENCES `clinic`.`patients` (`patient_id`)
    ON UPDATE CASCADE)
ENGINE = InnoDB
AUTO_INCREMENT = 7
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `clinic`.`xray`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `clinic`.`xray` (
  `xray_id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `patient_id` SMALLINT UNSIGNED NOT NULL,
  `xray_address` VARCHAR(300) NOT NULL,
  `date` DATE NOT NULL,
  PRIMARY KEY (`xray_id`),
  INDEX `fk_xray_patients1_idx` (`patient_id` ASC) VISIBLE,
  CONSTRAINT `fk_xray_patients1`
    FOREIGN KEY (`patient_id`)
    REFERENCES `clinic`.`patients` (`patient_id`)
    ON UPDATE CASCADE)
ENGINE = InnoDB
AUTO_INCREMENT = 11
DEFAULT CHARACTER SET = utf8mb3;

USE `clinic` ;

-- -----------------------------------------------------
-- procedure createInvoice
-- -----------------------------------------------------

DELIMITER $$
USE `clinic`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `createInvoice`(
	patient_id SMALLINT,
    consulting DECIMAL(7,2),
    payment DECIMAL(7,2),
    pending DECIMAL(7,2)
)
BEGIN
	INSERT INTO invoices
    VALUES (DEFAULT,patient_id,DATE(NOW()),consulting,payment,pending);
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure insertNextAppointment
-- -----------------------------------------------------

DELIMITER $$
USE `clinic`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `insertNextAppointment`(
	patient_id SMALLINT,
    date DATE
)
BEGIN
	INSERT INTO next_appointment
    VALUES(DEFAULT, patient_id,date);
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure insertPatient
-- -----------------------------------------------------

DELIMITER $$
USE `clinic`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `insertPatient`(
	first_name VARCHAR(50),
    last_name VARCHAR(50),
    address VARCHAR(500),
    history VARCHAR(500),
    cas CHAR(1)
)
INSERT INTO patients
VALUES(DEFAULT,first_name,last_name,address,history, cas)$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure insertXray
-- -----------------------------------------------------

DELIMITER $$
USE `clinic`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `insertXray`(
	patient_id TINYINT,
    xray_address VARCHAR(300),
    date DATE
)
BEGIN
	INSERT INTO xray
    VALUES (DEFAULT, patient_id,xray_address,date);
END$$

DELIMITER ;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
