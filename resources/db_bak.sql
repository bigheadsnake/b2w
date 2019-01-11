/*
SQLyog Enterprise v12.09 (64 bit)
MySQL - 10.1.25-MariaDB : Database - b2w
*********************************************************************
*/

/*!40101 SET NAMES utf8 */;

/*!40101 SET SQL_MODE=''*/;

/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;
CREATE DATABASE /*!32312 IF NOT EXISTS*/`b2w` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `b2w`;

/*Table structure for table `b2w_loginhistory` */

DROP TABLE IF EXISTS `b2w_loginhistory`;

CREATE TABLE `b2w_loginhistory` (
  `login` datetime NOT NULL,
  `username` varchar(100) NOT NULL,
  `cate` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`login`,`username`),
  KEY `idx_LoginHisLogin` (`login`),
  KEY `idx_LoginHisAcct` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `b2w_loginhistory` */

insert  into `b2w_loginhistory`(`login`,`username`,`cate`) values ('2019-01-04 14:21:46','bigheadsnake','administrator');
insert  into `b2w_loginhistory`(`login`,`username`,`cate`) values ('2019-01-04 14:33:51','bigheadsnake','administrator');
insert  into `b2w_loginhistory`(`login`,`username`,`cate`) values ('2019-01-04 14:36:57','bigheadsnake','administrator');
insert  into `b2w_loginhistory`(`login`,`username`,`cate`) values ('2019-01-04 14:38:48','bigheadsnake','administrator');
insert  into `b2w_loginhistory`(`login`,`username`,`cate`) values ('2019-01-04 15:31:30','bigheadsnake','administrator');
insert  into `b2w_loginhistory`(`login`,`username`,`cate`) values ('2019-01-04 16:37:17','bigheadsnake','administrator');
insert  into `b2w_loginhistory`(`login`,`username`,`cate`) values ('2019-01-04 16:39:22','bigheadsnake','administrator');
insert  into `b2w_loginhistory`(`login`,`username`,`cate`) values ('2019-01-04 16:46:28','bigheadsnake','administrator');
insert  into `b2w_loginhistory`(`login`,`username`,`cate`) values ('2019-01-07 10:06:46','bigheadsnake','administrator');
insert  into `b2w_loginhistory`(`login`,`username`,`cate`) values ('2019-01-07 10:08:57','bigheadsnake','administrator');
insert  into `b2w_loginhistory`(`login`,`username`,`cate`) values ('2019-01-07 11:10:26','bigheadsnake','administrator');
insert  into `b2w_loginhistory`(`login`,`username`,`cate`) values ('2019-01-07 11:15:38','bigheadsnake','administrator');
insert  into `b2w_loginhistory`(`login`,`username`,`cate`) values ('2019-01-08 14:04:06','bigheadsnake','administrator');
insert  into `b2w_loginhistory`(`login`,`username`,`cate`) values ('2019-01-09 13:38:01','bigheadsnake','administrator');
insert  into `b2w_loginhistory`(`login`,`username`,`cate`) values ('2019-01-09 14:45:48','bigheadsnake','administrator');
insert  into `b2w_loginhistory`(`login`,`username`,`cate`) values ('2019-01-09 14:51:45','bigheadsnake','administrator');
insert  into `b2w_loginhistory`(`login`,`username`,`cate`) values ('2019-01-09 14:52:44','bigheadsnake','administrator');
insert  into `b2w_loginhistory`(`login`,`username`,`cate`) values ('2019-01-11 15:53:16','bigheadsnake','administrator');

/*Table structure for table `b2w_users` */

DROP TABLE IF EXISTS `b2w_users`;

CREATE TABLE `b2w_users` (
  `username` varchar(100) NOT NULL,
  `password` varchar(500) NOT NULL,
  `cate` varchar(100) NOT NULL,
  `salt` varchar(100) NOT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `b2w_users` */

insert  into `b2w_users`(`username`,`password`,`cate`,`salt`) values ('bigheadsnake','e9085ebbcfbf3a33785a65f4c87efa90','administrator','TH8F');

/*Table structure for table `cargo_management` */

DROP TABLE IF EXISTS `cargo_management`;

CREATE TABLE `cargo_management` (
  `cargo_id` int(11) NOT NULL AUTO_INCREMENT,
  `cargo_category_L1` varchar(100) NOT NULL COMMENT '一级分类',
  `cargo_category_L2` varchar(100) DEFAULT NULL COMMENT '二级分类',
  `cargo_category_L3` varchar(100) DEFAULT NULL COMMENT '三级分类',
  `cargo_category_L4` varchar(100) DEFAULT NULL COMMENT '四级分类',
  `cargo_name` varchar(100) NOT NULL COMMENT '货品名称',
  `specification` varchar(100) DEFAULT NULL COMMENT '货品规格',
  `describle` varchar(500) DEFAULT NULL COMMENT '货品描述',
  PRIMARY KEY (`cargo_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

/*Data for the table `cargo_management` */

insert  into `cargo_management`(`cargo_id`,`cargo_category_L1`,`cargo_category_L2`,`cargo_category_L3`,`cargo_category_L4`,`cargo_name`,`specification`,`describle`) values (1,'Package','Inner Package',NULL,NULL,'牛皮纸泡泡包装袋','130mm*160mm+40mm',NULL);
insert  into `cargo_management`(`cargo_id`,`cargo_category_L1`,`cargo_category_L2`,`cargo_category_L3`,`cargo_category_L4`,`cargo_name`,`specification`,`describle`) values (2,'Supplies','Office Supplies',NULL,NULL,'爱普生墨盒','ME600F墨盒','共四色');

/*Table structure for table `cargo_purchase` */

DROP TABLE IF EXISTS `cargo_purchase`;

CREATE TABLE `cargo_purchase` (
  `purchase_time` datetime NOT NULL,
  `cargo_id` int(11) NOT NULL,
  `unit_price` float DEFAULT NULL,
  `amount` int(11) DEFAULT NULL,
  `total_price` float DEFAULT NULL,
  `final_price` float DEFAULT NULL,
  PRIMARY KEY (`purchase_time`,`cargo_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `cargo_purchase` */

/*Table structure for table `motor_parts` */

DROP TABLE IF EXISTS `motor_parts`;

CREATE TABLE `motor_parts` (
  `cargo_id` int(11) NOT NULL,
  `motor_make` varchar(100) DEFAULT NULL,
  `motor_model` varchar(100) DEFAULT NULL,
  `motor_model_year` year(4) DEFAULT NULL,
  `parts_name` varchar(100) DEFAULT NULL,
  `parts_make` varchar(100) DEFAULT NULL,
  `parts_desc` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`cargo_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Data for the table `motor_parts` */

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
