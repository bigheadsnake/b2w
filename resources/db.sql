CREATE DATABASE /*!32312 IF NOT EXISTS*/`b2w` /*!40100 DEFAULT CHARACTER SET utf8 */;

USE `b2w`;

/*Table structure for table `b2w_loginhistory` */

CREATE TABLE `b2w_loginhistory` (
  `login` datetime NOT NULL,
  `username` varchar(100) NOT NULL,
  `cate` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`login`,`username`),
  KEY `idx_LoginHisLogin` (`login`),
  KEY `idx_LoginHisAcct` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `b2w_users` */

CREATE TABLE `b2w_users` (
  `username` varchar(100) NOT NULL,
  `password` varchar(500) NOT NULL,
  `cate` varchar(100) NOT NULL,
  `salt` varchar(100) NOT NULL,
  PRIMARY KEY (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

/*Table structure for table `cargo_purchase` */

CREATE TABLE `cargo_purchase` (
  `cargo_id` int(11) NOT NULL AUTO_INCREMENT,
  `cargo_category_L1` varchar(100) NOT NULL,
  `cargo_category_L2` varchar(100) DEFAULT NULL,
  `cargo_category_L3` varchar(100) DEFAULT NULL,
  `cargo_category_L4` varchar(100) DEFAULT NULL,
  `cargo_name` varchar(100) NOT NULL,
  `specification` varchar(100) DEFAULT NULL,
  `desc` varchar(500) DEFAULT NULL,
  PRIMARY KEY (`cargo_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;