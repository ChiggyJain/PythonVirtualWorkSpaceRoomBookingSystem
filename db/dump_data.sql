

DROP DATABASE IF EXISTS VIRTUAL_WORKSPACE;
CREATE DATABASE VIRTUAL_WORKSPACE;
COMMIT;

USE VIRTUAL_WORKSPACE;


-- Create USERS table if not exists
CREATE TABLE IF NOT EXISTS `USERS` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` char(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `username` varchar(100) NOT NULL,
  `userpassword` varchar(100) NOT NULL,
  `age` int NOT NULL DEFAULT '1',
  `gender` char(10) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'Male',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
COMMIT;

-- Insert records only if they do not exist
REPLACE INTO `USERS` 
(`id`, `name`, `username`, `userpassword`, `age`, `gender`) 
VALUES
(1, 'User1', 'user1', '24c9e15e52afc47c225b757e7bee1f9d', 28, 'Female'),
(2, 'User2', 'user2', '7e58d63b60197ceb55a1c487989a3720', 34, 'Male'),
(3, 'User3', 'user3', '92877af70a45fd6a2ed7fe81e1236b78', 25, 'Male'),
(4, 'User4', 'user4', '3f02ebe3d7929b091e3d8ccfde2f3bc6', 30, 'Female'),
(5, 'User5', 'user5', '0a791842f52a0acfbb3a783378c066b8', 27, 'Male'),
(6, 'User6', 'user6', 'affec3b64cf90492377a8114c86fc093', 32, 'Female'),
(7, 'User7', 'user7', '3e0469fb134991f8f75a2760e409c6ed', 29, 'Male'),
(8, 'User8', 'user8', '7668f673d5669995175ef91b5d171945', 31, 'Female'),
(9, 'User9', 'user9', '8808a13b854c2563da1a5f6cb2130868', 26, 'Male'),
(10, 'User10', 'user10', '990d67a9f94696b1abe2dccf06900322', 35, 'Female');
COMMIT;


-- Create TEAMS table if not exists
CREATE TABLE IF NOT EXISTS `TEAMS` (
  `id` int NOT NULL AUTO_INCREMENT,
  `team_name` char(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
COMMIT;

-- Insert records only if they do not exist
REPLACE INTO `TEAMS` 
(`id`, `team_name`) 
VALUES
(1, 'Team Alpha'),
(2, 'Team Beta'),
(3, 'Team Gamma'),
(4, 'Team Delta'),
(5, 'Team Zeta');
COMMIT;


-- Create TEAM_MEMBERS table if not exists
CREATE TABLE IF NOT EXISTS `TEAM_MEMBERS` (
  `id` int NOT NULL AUTO_INCREMENT,
  `team_id` int NOT NULL DEFAULT '0',
  `user_id` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `uniq_teamIdUserId` (`team_id`,`user_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
COMMIT;

-- Insert records only if they do not exist
REPLACE INTO `TEAM_MEMBERS` 
(`id`, `team_id`, `user_id`) 
VALUES
(1, 1, 1),
(2, 1, 2),
(3, 1, 3),
(4, 1, 4),
(5, 1, 5),
(6, 2, 6),
(7, 2, 7),
(8, 2, 8),
(9, 2, 9),
(10, 2, 10),
(11, 3, 1),
(12, 3, 2),
(13, 4, 1),
(14, 4, 2),
(15, 4, 3),
(16, 5, 4);
COMMIT;


-- Create ROOMS table if not exists
CREATE TABLE IF NOT EXISTS `ROOMS` (
  `id` int NOT NULL AUTO_INCREMENT,
  `room_type` enum('Private','Conference','Shared-Desk') NOT NULL DEFAULT 'Private',
  `room_name` varchar(20) DEFAULT NULL,
  `room_capacity` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
COMMIT;

-- Insert initial records (if needed)
REPLACE INTO `ROOMS` 
(`id`, `room_type`, `room_name`, `room_capacity`)
VALUES
(1, 'Private', 'Private Room 1', 1),
(2, 'Conference', 'Conference Room 1', 1),
(3, 'Shared-Desk', 'Shared Desk 1', 4),
(4, 'Shared-Desk', 'Shared Desk 2', 4),
(5, 'Private', 'Private Room 2', 1),
(6, 'Conference', 'Conference Room 2', 1);
COMMIT;


-- Create ROOMS table if not exists
CREATE TABLE IF NOT EXISTS `ROOMS` (
  `id` int NOT NULL AUTO_INCREMENT,
  `room_type` enum('Private','Conference','Shared-Desk') NOT NULL DEFAULT 'Private',
  `room_name` varchar(20) DEFAULT NULL,
  `room_capacity` int NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
COMMIT;

-- Insert rooms only if they do not exist
REPLACE INTO `ROOMS` (`id`, `room_type`, `room_name`, `room_capacity`) 
VALUES
(1, 'Private', 'Private-Room-1', 1),
(2, 'Private', 'Private-Room-2', 1),
(3, 'Private', 'Private-Room-3', 1),
(4, 'Private', 'Private-Room-4', 1),
(5, 'Private', 'Private-Room-5', 1),
(6, 'Private', 'Private-Room-6', 1),
(7, 'Private', 'Private-Room-7', 1),
(8, 'Private', 'Private-Room-8', 1),
(9, 'Conference', 'Conference-Room-1', 10),
(10, 'Conference', 'Conference-Room-2', 10),
(11, 'Conference', 'Conference-Room-3', 10),
(12, 'Conference', 'Conference-Room-4', 10),
(13, 'Shared-Desk', 'Shared-Desk-Room-1', 4),
(14, 'Shared-Desk', 'Shared-Desk-Room-2', 4),
(15, 'Shared-Desk', 'Shared-Desk-Room-3', 4);
COMMIT;


-- Create BOOKINGS table if not exists
CREATE TABLE IF NOT EXISTS `BOOKINGS` (
  `id` int NOT NULL AUTO_INCREMENT,
  `booked_id` varchar(200) NOT NULL,
  `room_id` int NOT NULL DEFAULT '0',
  `booked_start_datetime_slot` datetime NOT NULL,
  `booked_end_datetime_slot` datetime NOT NULL,
  `booked_reference_type` char(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `booked_reference_type_id` int NOT NULL DEFAULT '0',
  `creater_id` int NOT NULL DEFAULT '0',
  `created_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP,
  `updater_id` int NOT NULL DEFAULT '0',
  `updated_on` timestamp NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `status` enum('Booked','Cancelled') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL DEFAULT 'Booked',
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
COMMIT;













