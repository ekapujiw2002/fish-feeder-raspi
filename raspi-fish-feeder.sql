/*
Navicat MySQL Data Transfer

Source Server         : localhost mysql
Source Server Version : 50515
Source Host           : localhost:3306
Source Database       : raspi-fish-feeder

Target Server Type    : MYSQL
Target Server Version : 50515
File Encoding         : 65001

Date: 2017-10-16 16:47:21
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `feed_schedule`
-- ----------------------------
DROP TABLE IF EXISTS `feed_schedule`;
CREATE TABLE `feed_schedule` (
  `id` int(11) NOT NULL DEFAULT '0',
  `aktif` int(11) DEFAULT NULL,
  `senin` int(11) DEFAULT NULL,
  `selasa` int(11) DEFAULT NULL,
  `rabu` int(11) DEFAULT NULL,
  `kamis` int(11) DEFAULT NULL,
  `jumat` int(11) DEFAULT NULL,
  `sabtu` int(11) DEFAULT NULL,
  `minggu` int(11) DEFAULT NULL,
  `jam` longtext,
  `berat` double DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- ----------------------------
-- Records of feed_schedule
-- ----------------------------
INSERT INTO `feed_schedule` VALUES ('1', '1', '1', '0', '0', '0', '0', '1', '0', '17:28:0', '1');
INSERT INTO `feed_schedule` VALUES ('2', '0', '1', '1', '1', '0', '0', '0', '0', '12:35:0', '1');
INSERT INTO `feed_schedule` VALUES ('3', '0', '0', '1', '1', '1', '1', '0', '0', '9:10:0', '1');
INSERT INTO `feed_schedule` VALUES ('4', '1', '0', '1', '0', '1', '1', '0', '0', '5:0:0', '0.5');
INSERT INTO `feed_schedule` VALUES ('5', '0', '0', '1', '0', '1', '0', '0', '0', '14:12:0', '0.5');
