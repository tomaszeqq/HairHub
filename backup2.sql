-- MySQL dump 10.13  Distrib 8.0.35, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: Fryzjerzy
-- ------------------------------------------------------
-- Server version	8.2.0

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
-- Table structure for table `Details`
--

DROP TABLE IF EXISTS `Details`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Details` (
  `Detail_ID` int NOT NULL AUTO_INCREMENT,
  `Service_ID` int NOT NULL,
  `Salon_ID` int NOT NULL,
  `Time` int NOT NULL,
  `Price` float NOT NULL,
  PRIMARY KEY (`Detail_ID`),
  KEY `Salon_ID` (`Salon_ID`),
  KEY `fk_Service_ID` (`Service_ID`),
  CONSTRAINT `Details_ibfk_1` FOREIGN KEY (`Salon_ID`) REFERENCES `Hair_Salon` (`Salon_ID`),
  CONSTRAINT `fk_Service_ID` FOREIGN KEY (`Service_ID`) REFERENCES `Services` (`Service_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Details`
--

LOCK TABLES `Details` WRITE;
/*!40000 ALTER TABLE `Details` DISABLE KEYS */;
/*!40000 ALTER TABLE `Details` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Exceptions`
--

DROP TABLE IF EXISTS `Exceptions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Exceptions` (
  `Exception_ID` int NOT NULL AUTO_INCREMENT,
  `Salon_ID` int NOT NULL,
  `Opening_Hour` time NOT NULL,
  `Closing_Hour` time NOT NULL,
  `Starting_Date` date NOT NULL,
  `Ending_Date` date NOT NULL,
  PRIMARY KEY (`Exception_ID`),
  KEY `Salon_ID` (`Salon_ID`),
  CONSTRAINT `Exceptions_ibfk_1` FOREIGN KEY (`Salon_ID`) REFERENCES `Hair_Salon` (`Salon_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Exceptions`
--

LOCK TABLES `Exceptions` WRITE;
/*!40000 ALTER TABLE `Exceptions` DISABLE KEYS */;
/*!40000 ALTER TABLE `Exceptions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Hair_Salon`
--

DROP TABLE IF EXISTS `Hair_Salon`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Hair_Salon` (
  `Salon_ID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) NOT NULL,
  `Address` varchar(45) NOT NULL,
  `Owner` varchar(45) NOT NULL,
  `Has_Parking` tinyint(1) NOT NULL,
  `Phone_Number` varchar(14) NOT NULL,
  PRIMARY KEY (`Salon_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Hair_Salon`
--

LOCK TABLES `Hair_Salon` WRITE;
/*!40000 ALTER TABLE `Hair_Salon` DISABLE KEYS */;
/*!40000 ALTER TABLE `Hair_Salon` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Liked_Salons`
--

DROP TABLE IF EXISTS `Liked_Salons`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Liked_Salons` (
  `Liked_Salon_ID` int NOT NULL AUTO_INCREMENT,
  `User_ID` int NOT NULL,
  `Salon_ID` int NOT NULL,
  PRIMARY KEY (`Liked_Salon_ID`),
  KEY `User_ID` (`User_ID`),
  KEY `Salon_ID` (`Salon_ID`),
  CONSTRAINT `Liked_Salons_ibfk_1` FOREIGN KEY (`User_ID`) REFERENCES `Users` (`User_ID`),
  CONSTRAINT `Liked_Salons_ibfk_2` FOREIGN KEY (`Salon_ID`) REFERENCES `Hair_Salon` (`Salon_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Liked_Salons`
--

LOCK TABLES `Liked_Salons` WRITE;
/*!40000 ALTER TABLE `Liked_Salons` DISABLE KEYS */;
/*!40000 ALTER TABLE `Liked_Salons` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Opening_Hours`
--

DROP TABLE IF EXISTS `Opening_Hours`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Opening_Hours` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Salon_ID` int NOT NULL,
  `Week_Day` int NOT NULL,
  `Opening_Hour` time NOT NULL,
  `Closing_Hour` time NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `Salon_ID` (`Salon_ID`),
  CONSTRAINT `Opening_Hours_ibfk_1` FOREIGN KEY (`Salon_ID`) REFERENCES `Hair_Salon` (`Salon_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Opening_Hours`
--

LOCK TABLES `Opening_Hours` WRITE;
/*!40000 ALTER TABLE `Opening_Hours` DISABLE KEYS */;
/*!40000 ALTER TABLE `Opening_Hours` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Opinions`
--

DROP TABLE IF EXISTS `Opinions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Opinions` (
  `Opinion_ID` int NOT NULL AUTO_INCREMENT,
  `User_ID` int NOT NULL,
  `Salon_ID` int NOT NULL,
  `Stars_1_2_3_4_5` int NOT NULL,
  `Description` longtext NOT NULL,
  PRIMARY KEY (`Opinion_ID`),
  KEY `Salon_ID` (`Salon_ID`),
  KEY `User_ID` (`User_ID`),
  CONSTRAINT `Opinions_ibfk_1` FOREIGN KEY (`Salon_ID`) REFERENCES `Hair_Salon` (`Salon_ID`),
  CONSTRAINT `Opinions_ibfk_2` FOREIGN KEY (`User_ID`) REFERENCES `Users` (`User_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Opinions`
--

LOCK TABLES `Opinions` WRITE;
/*!40000 ALTER TABLE `Opinions` DISABLE KEYS */;
/*!40000 ALTER TABLE `Opinions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Reports`
--

DROP TABLE IF EXISTS `Reports`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Reports` (
  `Report_ID` int NOT NULL AUTO_INCREMENT,
  `User_ID` int NOT NULL,
  `Report_Date` datetime NOT NULL,
  `Report_Description` longtext NOT NULL,
  PRIMARY KEY (`Report_ID`),
  KEY `fk_User_ID` (`User_ID`),
  CONSTRAINT `fk_User_ID` FOREIGN KEY (`User_ID`) REFERENCES `Users` (`User_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Reports`
--

LOCK TABLES `Reports` WRITE;
/*!40000 ALTER TABLE `Reports` DISABLE KEYS */;
/*!40000 ALTER TABLE `Reports` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Services`
--

DROP TABLE IF EXISTS `Services`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Services` (
  `Service_ID` int NOT NULL AUTO_INCREMENT,
  `Salon_ID` int NOT NULL,
  `Name` varchar(45) NOT NULL,
  `Description` longtext NOT NULL,
  PRIMARY KEY (`Service_ID`),
  KEY `Salon_ID` (`Salon_ID`),
  CONSTRAINT `Services_ibfk_1` FOREIGN KEY (`Salon_ID`) REFERENCES `Hair_Salon` (`Salon_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Services`
--

LOCK TABLES `Services` WRITE;
/*!40000 ALTER TABLE `Services` DISABLE KEYS */;
/*!40000 ALTER TABLE `Services` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Users`
--

DROP TABLE IF EXISTS `Users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Users` (
  `User_ID` int NOT NULL AUTO_INCREMENT,
  `Name` varchar(45) NOT NULL,
  `Surname` varchar(45) NOT NULL,
  `Email_Address` varchar(45) NOT NULL,
  `Phone_Number` varchar(14) NOT NULL,
  `Password` varchar(45) NOT NULL,
  `Moderator` int NOT NULL,
  `Administrator` tinyint(1) NOT NULL,
  PRIMARY KEY (`User_ID`)
) ENGINE=InnoDB AUTO_INCREMENT=8 DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Users`
--

LOCK TABLES `Users` WRITE;
/*!40000 ALTER TABLE `Users` DISABLE KEYS */;
INSERT INTO `Users` VALUES (1,'Szymon','Jastrzębski','szymon@wp.pl','505 505 505','dupa123',0,0);
/*!40000 ALTER TABLE `Users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Workers`
--

DROP TABLE IF EXISTS `Workers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `Workers` (
  `Worker_ID` int NOT NULL AUTO_INCREMENT,
  `Salon_ID` int NOT NULL,
  `Name` varchar(45) NOT NULL,
  `Surname` varchar(45) NOT NULL,
  `Description` longtext NOT NULL,
  `Password` varchar(45) NOT NULL,
  PRIMARY KEY (`Worker_ID`),
  KEY `Salon_ID` (`Salon_ID`),
  CONSTRAINT `Workers_ibfk_1` FOREIGN KEY (`Salon_ID`) REFERENCES `Hair_Salon` (`Salon_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Workers`
--

LOCK TABLES `Workers` WRITE;
/*!40000 ALTER TABLE `Workers` DISABLE KEYS */;
/*!40000 ALTER TABLE `Workers` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-01-04 14:08:58
