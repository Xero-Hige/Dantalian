SET @OLD_UNIQUE_CHECKS = @@UNIQUE_CHECKS, UNIQUE_CHECKS = 0;
SET @OLD_FOREIGN_KEY_CHECKS = @@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS = 0;
SET @OLD_SQL_MODE = @@SQL_MODE, SQL_MODE = 'TRADITIONAL,ALLOW_INVALID_DATES';

-- -----------------------------------------------------
-- Schema dantalian
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `dantalian`
  DEFAULT CHARACTER SET utf8;
USE `dantalian`;

-- -----------------------------------------------------
-- Table `dantalian`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `dantalian`.`users` (
  `iduser`    INT          NOT NULL AUTO_INCREMENT,
  `username`  VARCHAR(45)  NOT NULL,
  `userpass`  VARCHAR(128) NOT NULL,
  `creation` TIMESTAMP    NULL,
  PRIMARY KEY (`iduser`),
  UNIQUE INDEX `username_UNIQUE` (`username` ASC)
)
  ENGINE = InnoDB;

SET SQL_MODE = @OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS = @OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS = @OLD_UNIQUE_CHECKS;