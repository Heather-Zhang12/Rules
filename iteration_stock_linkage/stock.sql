/*
Navicat MySQL Data Transfer

Source Server         : MYSQL51
Source Server Version : 50136
Source Host           : localhost:3306
Source Database       : platelinkage

Target Server Type    : MYSQL
Target Server Version : 50136
File Encoding         : 65001

Date: 2016-11-02 19:31:08
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for stock
-- ----------------------------
DROP TABLE IF EXISTS `stock`;
CREATE TABLE `stock` (
  `chWindCode` varchar(255) DEFAULT NULL,
  `chCode` varchar(255) DEFAULT NULL,
  `nDate` varchar(255) DEFAULT NULL,
  `nTime` varchar(255) DEFAULT NULL,
  `nOpen` varchar(255) DEFAULT NULL,
  `nHigh` varchar(255) DEFAULT NULL,
  `nLow` varchar(255) DEFAULT NULL,
  `nClose` varchar(255) DEFAULT NULL,
  `iVolume` varchar(255) DEFAULT NULL,
  `iTurover` varchar(255) DEFAULT NULL,
  `nMatchItems` varchar(255) DEFAULT NULL,
  `nInterest` varchar(255) DEFAULT NULL,
  `nTrend` int(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
