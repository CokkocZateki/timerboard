--
-- Table structure for table `timer`
--

DROP TABLE IF EXISTS `timer`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `timer` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `system` varchar(12) DEFAULT NULL,
  `planet` varchar(6) DEFAULT NULL,
  `moon` int(11) DEFAULT NULL,
  `owner` varchar(12) DEFAULT NULL,
  `time` datetime DEFAULT NULL,
  `notes` varchar(240) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

