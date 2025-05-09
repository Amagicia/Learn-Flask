-- MySQL dump 10.13  Distrib 8.0.40, for Win64 (x86_64)
--
-- Host: localhost    Database: attendance
-- ------------------------------------------------------
-- Server version	8.0.40

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `attendance`
--

DROP TABLE IF EXISTS `attendance`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `attendance` (
  `enrollment_no` varchar(20) NOT NULL,
  `subject_code` varchar(20) NOT NULL,
  `attendance_date` date NOT NULL,
  `RFID_SCAN` time DEFAULT NULL,
  `attendance_status` enum('P','A','L') DEFAULT 'A',
  UNIQUE KEY `enrollment_no` (`enrollment_no`,`subject_code`,`attendance_date`),
  KEY `subject_code` (`subject_code`),
  CONSTRAINT `attendance_ibfk_1` FOREIGN KEY (`enrollment_no`) REFERENCES `registration` (`Enrollment_NO`),
  CONSTRAINT `attendance_ibfk_2` FOREIGN KEY (`subject_code`) REFERENCES `subject` (`Subject_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `attendance`
--

LOCK TABLES `attendance` WRITE;
/*!40000 ALTER TABLE `attendance` DISABLE KEYS */;
INSERT INTO `attendance` VALUES ('20','BT301','2025-01-01','20:41:08','P'),('20','BT302','2024-12-31','00:16:50','P'),('20','BT304','2024-12-30','22:28:01','P'),('20','BT305','2025-01-02','15:05:43','P'),('25','BT301','2025-01-01','20:29:32','P'),('25','BT302','2024-12-31','00:16:40','P'),('25','BT305','2025-01-02','15:05:25','P'),('54','BT301','2025-01-01','20:06:38','P'),('54','BT302','2024-12-31','00:16:30','P'),('54','BT304','2024-12-30','23:49:53','P'),('54','BT305','2025-01-02','15:00:44','P'),('77','BT301','2025-01-01','20:29:48','P'),('77','BT302','2024-12-31','00:14:37','P'),('77','BT305','2025-01-02','15:07:08','P');
/*!40000 ALTER TABLE `attendance` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `registration`
--

DROP TABLE IF EXISTS `registration`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `registration` (
  `Name` varchar(50) NOT NULL,
  `Enrollment_NO` varchar(20) NOT NULL,
  `Phone_NO` varchar(10) NOT NULL,
  `Email` varchar(50) NOT NULL,
  `RFID_ID` varchar(50) DEFAULT NULL,
  `password` varchar(555) DEFAULT NULL,
  `Address` varchar(100) NOT NULL,
  `Total_Present` int DEFAULT NULL,
  PRIMARY KEY (`Enrollment_NO`),
  UNIQUE KEY `Email` (`Email`),
  UNIQUE KEY `RFID_ID` (`RFID_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `registration`
--

LOCK TABLES `registration` WRITE;
/*!40000 ALTER TABLE `registration` DISABLE KEYS */;
INSERT INTO `registration` VALUES ('Ak','0822','78906','akhaga',NULL,'scrypt:32768:8:1$b35WolQy83F5V0ae$6a806513506b2852e7ca2ccb159186dcf47824ff9d4ff43b48ab899392881e006cf9d89d30ed6859d1e04e29041e0824a7239ea8aa2f9bb3403a2396e3568c11','dfdfgyftyfgf',NULL),('Aman Tiwari','20','6386201692','amntwri0323@gmail.com','A359AF3A','scrypt:32768:8:1$umEM6uPM6jGf5UxS$4660d43be441516e2c83ec2162da0270d1ac17a9ce81573abf19f438105d5dbc6d2582ce0afd3896758fef6fee5e7f0e04ae53f3c2daad86df75629ebeb011bc','Jaunpur',1),('Harsh','25','762367','ahkjh@gmail.com','B9C6B0D4','scrypt:32768:8:1$3QAkROju2wQzGLII$57db40805d9c94a406b341eeab0bf02fb75a700ca4a67d6d6356626f6ebaafcbf47c1024f9b4bb75772defd70a5cf59700efc56c5fa63571c1eac271ce6d2a2c','ahshh',1),('Bhumika','44','12345678','bhumika@gmail.com',NULL,'scrypt:32768:8:1$pyWAzfLbnbgrRlU6$2f74471239ee9c97458d3317e5911b675de64f638c98024a5e1f5c262a2ba605a0dfcdd01622d6247115383b4fc9aa758ced86df1f66941e0ef55ed1f15328b7','Indore',NULL),('Deepak Parashar','54','52326','depp@gmail.com','05E51E3C','scrypt:32768:8:1$7z5ztwxo2RMGYkpG$15bb77a9af9319d05846e12f1ebdf8cb8ef89f3dd5bcd29a24f0d7743b718fe5b115df7152f66bdabcb61f5e01f512886a9ee3461dcac90c6f9333be9496b6e4','indore',1),('hardika','77','6723562387','hardika@gmail.com','8593113C','scrypt:32768:8:1$NSLQJrIft6bmacrc$bf4c505d9d1d5d2837a30029e09f4c7dce833fe76a65d071a7a8e9cfa527e0fd43cddabc31cd9047e41d1ee5e30241212c7dd3dd9f64f9f510200692851853d2','Tejaji,Nagar',1),('Ramesh','88','477676','bVAVbnn@gmail.com',NULL,'scrypt:32768:8:1$HRLcdVfikCyel0xo$3c96d7988d51e34e5f70f14f585ebbee31c8e0aa952982f646e57017a82ba44570fb2f965650623a08867b8fa637983af0f9e064f69424fc18d184602a767684','nbvhsdjhjhgjh',NULL);
/*!40000 ALTER TABLE `registration` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `schedule`
--

DROP TABLE IF EXISTS `schedule`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `schedule` (
  `id` int NOT NULL AUTO_INCREMENT,
  `subject_code` varchar(10) NOT NULL,
  `day` enum('Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday') NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_subject_day` (`subject_code`,`day`),
  CONSTRAINT `schedule_ibfk_1` FOREIGN KEY (`subject_code`) REFERENCES `subject` (`Subject_code`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `schedule`
--

LOCK TABLES `schedule` WRITE;
/*!40000 ALTER TABLE `schedule` DISABLE KEYS */;
INSERT INTO `schedule` VALUES (3,'BT301','Monday','09:00:00','10:00:00'),(6,'BT301','Tuesday','09:00:00','10:00:00'),(7,'BT302','Monday','02:05:00','06:06:00'),(8,'BT305','Monday','00:00:00','01:00:00'),(9,'BT303','Monday','11:20:00','12:40:00'),(10,'BT304','Monday','21:10:00','23:56:00'),(11,'BT302','Tuesday','00:07:00','10:07:00'),(12,'BT303','Tuesday','11:25:00','12:00:00'),(13,'BT304','Tuesday','13:29:00','16:29:00'),(14,'BT301','Wednesday','19:58:00','23:59:00'),(15,'BT305','Thursday','12:17:00','20:17:00'),(16,'BT305','Friday','00:30:00','01:30:00'),(17,'BT301','Friday','17:55:00','19:55:00');
/*!40000 ALTER TABLE `schedule` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subject`
--

DROP TABLE IF EXISTS `subject`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subject` (
  `Subject_name` varchar(100) NOT NULL,
  `Subject_code` varchar(20) NOT NULL,
  `Total_classes` int DEFAULT NULL,
  PRIMARY KEY (`Subject_code`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subject`
--

LOCK TABLES `subject` WRITE;
/*!40000 ALTER TABLE `subject` DISABLE KEYS */;
INSERT INTO `subject` VALUES ('EEE','BT301',1),('Mathematics','BT302',1),('DIGITAL LOGIC','BT303',0),('DSA','BT304',1),('OOPM','BT305',0);
/*!40000 ALTER TABLE `subject` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teacher`
--

DROP TABLE IF EXISTS `teacher`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teacher` (
  `username` varchar(100) NOT NULL,
  `password` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teacher`
--

LOCK TABLES `teacher` WRITE;
/*!40000 ALTER TABLE `teacher` DISABLE KEYS */;
INSERT INTO `teacher` VALUES ('Divya','123');
/*!40000 ALTER TABLE `teacher` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2025-04-13  7:13:51
