--
-- Database: `vg_dapi`
--
DROP DATABASE IF EXISTS `vg_dapi`;
CREATE DATABASE IF NOT EXISTS `vg_dapi`;
USE `vg_dapi`;


/*!40101 SET NAMES utf8mb4 */;
-- --------------------------------------------------------

--
-- Table structure for table `users`
--

 
CREATE TABLE IF NOT EXISTS `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT, 
  `name` varchar(100) DEFAULT NULL,
  `email` varchar(255) NOT NULL,
  `password_hash` text NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE( `email`)
) ENGINE=InnoDB;


-- -------------------------------------------------------

--
-- Table structure for table `user_sessions`
--

CREATE TABLE `user_sessions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL,
  `device_uuid` int(11) NOT NULL,
  `is_logged_in` int(11) NOT NULL,
  `last_updated` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY(`id`),
  UNIQUE(`device_uuid`,`user_id`)
) ENGINE=InnoDB;

-- Constraints for table `user_sessions`
--
ALTER TABLE `user_sessions`
  ADD CONSTRAINT `sessions_fk` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;



-- --------------------------------------------------------

--
-- Table structure for table `platform`
--

CREATE TABLE IF NOT EXISTS `platform` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `family`tinytext NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB;

-- --------------------------------------------------------

--
-- Table structure for table `game`
--

CREATE TABLE IF NOT EXISTS `game` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` text,
  `publishers` tinytext NOT NULL,
  `developers` tinytext NOT NULL,
  `dateUS` tinytext,
  `dateJP` tinytext,
  `dateEU` tinytext,
  `HLTB_Main` smallint,
  `HLTB_Complete` smallint,
  FULLTEXT (name, description),
  FULLTEXT (name),
  FULLTEXT (description),
  PRIMARY KEY (`id`),
  UNIQUE KEY (`name`)
) ENGINE=InnoDB;

ALTER TABLE `game` CONVERT TO CHARACTER SET utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `gameplatform`
--

CREATE TABLE IF NOT EXISTS `gameplatform` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `platformID` int(11) NOT NULL,
  `gameID` int(11) NOT NULL,
  `price` float,
  `metacritic` tinyint,
  `metacritic_user` tinyint,
  `metacritic_number_reviews` smallint,
  `steamID` int(11),
  `steam_score` tinytext,
  `amazon_price` float,
  `amazon_link` text,
  PRIMARY KEY (`id`),
  UNIQUE KEY `platCombo` (`platformID`,`gameID`)
) ENGINE=InnoDB;


ALTER TABLE `gameplatform` ADD CONSTRAINT gameplatform_platform_fk FOREIGN KEY (  `platformID` ) REFERENCES  `vg_dapi`.`platform` (`id`) 
ON DELETE CASCADE ON UPDATE CASCADE ;

ALTER TABLE `gameplatform` ADD CONSTRAINT gameplatform_game_fk FOREIGN KEY (`gameID`) REFERENCES `vg_dapi`.`game`(`id`) 
ON DELETE CASCADE ON UPDATE CASCADE;


-- --------------------------------------------------------

--
-- Table structure for table `genre`
--

CREATE TABLE IF NOT EXISTS `genre` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB;
ALTER TABLE `genre` ADD UNIQUE(`name`);
ALTER TABLE `genre` CONVERT TO CHARACTER SET utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `gamegenre`
--

CREATE TABLE IF NOT EXISTS `gamegenre` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `genreID` int(11) NOT NULL,
  `gameID` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `gameGenreCombo` (`genreID`,`gameID`)
) ENGINE=InnoDB;


ALTER TABLE `gamegenre` ADD CONSTRAINT gamegenre_genre_fk FOREIGN KEY (  `genreID` ) REFERENCES  `vg_dapi`.`genre` (`id`) 
ON DELETE CASCADE ON UPDATE CASCADE ;

ALTER TABLE `gamegenre` ADD CONSTRAINT gamegenre_game_fk FOREIGN KEY (`gameID`) REFERENCES `vg_dapi`.`game`(`id`) 
ON DELETE CASCADE ON UPDATE CASCADE;


INSERT INTO `platform` (`id`, `name`, `family`) VALUES
(1, 'Playstation 4', 'Playstation'),
(2, 'Xbox One', 'Xbox'),
(3, 'Nintendo Switch', 'Nintendo'),
(4, 'Steam', 'PC');

DELIMITER ;;;
CREATE FUNCTION `LEVENSHTEIN`(s1 VARCHAR(255), s2 VARCHAR(255)) RETURNS int(11) DETERMINISTIC
BEGIN
    DECLARE s1_len, s2_len, i, j, c, c_temp, cost INT;
    DECLARE s1_char CHAR;
    DECLARE cv0, cv1 VARBINARY(256);
    SET s1_len = CHAR_LENGTH(s1), s2_len = CHAR_LENGTH(s2), cv1 = 0x00, j = 1, i = 1, c = 0;
    IF s1 = s2 THEN
        RETURN 0;
    ELSEIF s1_len = 0 THEN
        RETURN s2_len;
    ELSEIF s2_len = 0 THEN
        RETURN s1_len;
    ELSE
        WHILE j <= s2_len DO
            SET cv1 = CONCAT(cv1, UNHEX(HEX(j))), j = j + 1;
        END WHILE;
        WHILE i <= s1_len DO
            SET s1_char = SUBSTRING(s1, i, 1), c = i, cv0 = UNHEX(HEX(i)), j = 1;
            WHILE j <= s2_len DO
                SET c = c + 1;
                IF s1_char = SUBSTRING(s2, j, 1) THEN SET cost = 0; ELSE SET cost = 1; END IF;
                SET c_temp = CONV(HEX(SUBSTRING(cv1, j, 1)), 16, 10) + cost;
                IF c > c_temp THEN SET c = c_temp; END IF;
                SET c_temp = CONV(HEX(SUBSTRING(cv1, j+1, 1)), 16, 10) + 1;
                IF c > c_temp THEN SET c = c_temp; END IF;
                SET cv0 = CONCAT(cv0, UNHEX(HEX(c))), j = j + 1;
            END WHILE;
            SET cv1 = cv0, i = i + 1;
        END WHILE;
    END IF;
    RETURN c;
END;;;
DELIMITER ;;;
CREATE FUNCTION `LEVENSHTEIN_RATIO`(s1 VARCHAR(255), s2 VARCHAR(255)) RETURNS int(11) DETERMINISTIC
BEGIN
    DECLARE s1_len, s2_len, max_len INT;
    SET s1_len = LENGTH(s1), s2_len = LENGTH(s2);
    IF s1_len > s2_len THEN SET max_len = s1_len; ELSE SET max_len = s2_len; END IF;
    RETURN ROUND((1 - LEVENSHTEIN(s1, s2) / max_len) * 100);
END;;;