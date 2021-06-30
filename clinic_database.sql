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
  `name` VARCHAR(50) NOT NULL,
  `phoneNo` DECIMAL(10,0) NULL DEFAULT NULL,
  `address` VARCHAR(250) NOT NULL,
  `history` VARCHAR(255) NOT NULL,
  PRIMARY KEY (`patient_id`))
ENGINE = InnoDB
AUTO_INCREMENT = 6
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `clinic`.`appointment`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `clinic`.`appointment` (
  `appointment_id` SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `patient_id` SMALLINT UNSIGNED NOT NULL,
  `date` DATE NOT NULL,
  PRIMARY KEY (`appointment_id`),
  INDEX `fk_next_appointment_patients_idx` (`patient_id` ASC) INVISIBLE,
  CONSTRAINT `fk_next_appointment_patients`
    FOREIGN KEY (`patient_id`)
    REFERENCES `clinic`.`patients` (`patient_id`)
    ON UPDATE CASCADE)
ENGINE = InnoDB
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `clinic`.`cases`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `clinic`.`cases` (
  `case_id` SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
  `patient_id` SMALLINT UNSIGNED NOT NULL,
  `date` DATE NOT NULL,
  `N/O` CHAR(1) NOT NULL,
  PRIMARY KEY (`case_id`),
  INDEX `fk_case_patients1_idx` (`patient_id` ASC) VISIBLE,
  CONSTRAINT `fk_case_patients1`
    FOREIGN KEY (`patient_id`)
    REFERENCES `clinic`.`patients` (`patient_id`)
    ON UPDATE CASCADE)
ENGINE = InnoDB
AUTO_INCREMENT = 4
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
  `pending` DECIMAL(7,2) UNSIGNED NOT NULL,
  PRIMARY KEY (`invoice_id`),
  INDEX `fk_invoices_patients1_idx` (`patient_id` ASC) VISIBLE,
  CONSTRAINT `fk_invoices_patients1`
    FOREIGN KEY (`patient_id`)
    REFERENCES `clinic`.`patients` (`patient_id`)
    ON UPDATE CASCADE)
ENGINE = InnoDB
AUTO_INCREMENT = 20
DEFAULT CHARACTER SET = utf8mb3;


-- -----------------------------------------------------
-- Table `clinic`.`xray`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `clinic`.`xray` (
  `xray_id` SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
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
DEFAULT CHARACTER SET = utf8mb3;

USE `clinic` ;

-- -----------------------------------------------------
-- Placeholder table for view `clinic`.`daily_revenue`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `clinic`.`daily_revenue` (`invoice_id` INT, `name` INT, `date` INT, `payment` INT);

-- -----------------------------------------------------
-- Placeholder table for view `clinic`.`monthly_revenue`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `clinic`.`monthly_revenue` (`invoice_id` INT, `name` INT, `date` INT, `payment` INT);

-- -----------------------------------------------------
-- Placeholder table for view `clinic`.`yearly_revenue`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `clinic`.`yearly_revenue` (`invoice_id` INT, `name` INT, `date` INT, `payment` INT);

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
-- procedure insertAppointment
-- -----------------------------------------------------

DELIMITER $$
USE `clinic`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `insertAppointment`(
	patient_id SMALLINT,
    date DATE
)
BEGIN
	INSERT INTO appointment
    VALUES(DEFAULT, patient_id,date);
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure insertCase
-- -----------------------------------------------------

DELIMITER $$
USE `clinic`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `insertCase`(
	patient_id INT,
	date DATE,
	N_O CHAR(1)
)
BEGIN
	INSERT INTO cases
    VALUES(DEFAULT,patient_id,date,N_O);
END$$

DELIMITER ;

-- -----------------------------------------------------
-- procedure insertPatient
-- -----------------------------------------------------

DELIMITER $$
USE `clinic`$$
CREATE DEFINER=`root`@`localhost` PROCEDURE `insertPatient`(
	name VARCHAR(50),
    phoneno DECIMAL(10),
    address VARCHAR(250),
    history VARCHAR(255)
)
INSERT INTO patients
VALUES(DEFAULT,name,phoneno,address,history)$$

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

-- -----------------------------------------------------
-- View `clinic`.`daily_revenue`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `clinic`.`daily_revenue`;
USE `clinic`;
CREATE  OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `clinic`.`daily_revenue` AS select `i`.`invoice_id` AS `invoice_id`,`p`.`name` AS `name`,date_format(`i`.`payment_date`,'%d/%m/%Y') AS `date`,`i`.`payment` AS `payment` from (`clinic`.`invoices` `i` join `clinic`.`patients` `p` on((`p`.`patient_id` = `i`.`patient_id`))) where (cast(`i`.`payment_date` as date) = cast(now() as date)) order by `i`.`invoice_id`;

-- -----------------------------------------------------
-- View `clinic`.`monthly_revenue`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `clinic`.`monthly_revenue`;
USE `clinic`;
CREATE  OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `clinic`.`monthly_revenue` AS select `i`.`invoice_id` AS `invoice_id`,`p`.`name` AS `name`,date_format(`i`.`payment_date`,'%d/%m/%Y') AS `date`,`i`.`payment` AS `payment` from (`clinic`.`invoices` `i` join `clinic`.`patients` `p` on((`p`.`patient_id` = `i`.`patient_id`))) where (month(`i`.`payment_date`) = month(now())) order by `i`.`invoice_id`;

-- -----------------------------------------------------
-- View `clinic`.`yearly_revenue`
-- -----------------------------------------------------
DROP TABLE IF EXISTS `clinic`.`yearly_revenue`;
USE `clinic`;
CREATE  OR REPLACE ALGORITHM=UNDEFINED DEFINER=`root`@`localhost` SQL SECURITY DEFINER VIEW `clinic`.`yearly_revenue` AS select `i`.`invoice_id` AS `invoice_id`,`p`.`name` AS `name`,date_format(`i`.`payment_date`,'%d/%m/%Y') AS `date`,`i`.`payment` AS `payment` from (`clinic`.`invoices` `i` join `clinic`.`patients` `p` on((`p`.`patient_id` = `i`.`patient_id`))) where (year(`i`.`payment_date`) = year(now())) order by `i`.`invoice_id`;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
