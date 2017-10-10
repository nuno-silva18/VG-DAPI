--
-- Database: `vg_dapi`
--
DROP DATABASE IF EXISTS `vg_dapi`;
CREATE DATABASE IF NOT EXISTS `vg_dapi`;
USE `vg_dapi`;



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
  `name` tinytext NOT NULL,
  `description` text,
  `publishers` tinytext NOT NULL,
  `developers` tinytext NOT NULL,
  `dateUS` date,
  `dateJP` date,
  `dateEU` date,
  `HLTB_Main` smallint,
  `HLTB_Complete` smallint,
  `IMDB_score` float,
  `IMDB_userscore` float,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB;


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
  `steam_score` tinyint,
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
  `name` tinytext NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB;


-- --------------------------------------------------------

--
-- Table structure for table `gamegenre`
--

CREATE TABLE IF NOT EXISTS `gamegenre` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `genreID` int(11) NOT NULL,
  `gameID` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB;


ALTER TABLE `gamegenre` ADD CONSTRAINT gamegenre_genre_fk FOREIGN KEY (  `genreID` ) REFERENCES  `vg_dapi`.`genre` (`id`) 
ON DELETE CASCADE ON UPDATE CASCADE ;

ALTER TABLE `gamegenre` ADD CONSTRAINT gamegenre_game_fk FOREIGN KEY (`gameID`) REFERENCES `vg_dapi`.`game`(`id`) 
ON DELETE CASCADE ON UPDATE CASCADE;


