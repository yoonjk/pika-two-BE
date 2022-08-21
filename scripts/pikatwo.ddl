-- pikatwo.alembic_version definition

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;


-- pikatwo.company definition

CREATE TABLE `company` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(256) NOT NULL,
  `type` varchar(100) NOT NULL,
  `category` varchar(100) NOT NULL,
  `is_certificated` tinyint(1) NOT NULL,
  `created_dt` datetime DEFAULT CURRENT_TIMESTAMP,
  `modified_dt` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=161 DEFAULT CHARSET=utf8mb3;


-- pikatwo.financial_product definition

CREATE TABLE `financial_product` (
  `id` int NOT NULL AUTO_INCREMENT,
  `bank_name` varchar(100) NOT NULL,
  `product_name` varchar(100) NOT NULL,
  `description` varchar(100) NOT NULL,
  `link` varchar(100) NOT NULL,
  `code` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb3;


-- pikatwo.job_post definition

CREATE TABLE `job_post` (
  `id` int NOT NULL AUTO_INCREMENT,
  `title` varchar(256) NOT NULL,
  `content` varchar(1024) NOT NULL,
  `start_dt` datetime NOT NULL,
  `end_dt` datetime NOT NULL,
  `type` varchar(100) NOT NULL,
  `company_id` int NOT NULL,
  `created_dt` datetime DEFAULT CURRENT_TIMESTAMP,
  `modified_dt` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `company_id` (`company_id`),
  CONSTRAINT `job_post_ibfk_1` FOREIGN KEY (`company_id`) REFERENCES `company` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=165 DEFAULT CHARSET=utf8mb3;


-- pikatwo.`user` definition

CREATE TABLE `user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nickname` varchar(256) DEFAULT NULL,
  `gender` varchar(64) NOT NULL,
  `profession` varchar(256) NOT NULL,
  `cur_company_id` int NOT NULL,
  `email` varchar(256) NOT NULL,
  `work_start_dt` datetime NOT NULL,
  `account` varchar(256) NOT NULL,
  `birth_yr` int NOT NULL,
  `created_dt` datetime DEFAULT CURRENT_TIMESTAMP,
  `modified_dt` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  UNIQUE KEY `email` (`email`),
  UNIQUE KEY `nickname` (`nickname`),
  KEY `cur_company_id` (`cur_company_id`),
  CONSTRAINT `user_ibfk_1` FOREIGN KEY (`cur_company_id`) REFERENCES `company` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1191 DEFAULT CHARSET=utf8mb3;


-- pikatwo.wage definition

CREATE TABLE `wage` (
  `id` int NOT NULL AUTO_INCREMENT,
  `amount` int DEFAULT NULL,
  `user_id` int NOT NULL,
  `company_id` int NOT NULL,
  `yr` int DEFAULT NULL,
  `created_dt` datetime DEFAULT CURRENT_TIMESTAMP,
  `modified_dt` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `user_id` (`user_id`),
  KEY `company_id` (`company_id`),
  CONSTRAINT `wage_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `wage_ibfk_2` FOREIGN KEY (`company_id`) REFERENCES `company` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4341 DEFAULT CHARSET=utf8mb3;


-- pikatwo.apply definition

CREATE TABLE `apply` (
  `id` int NOT NULL AUTO_INCREMENT,
  `job_post_id` int NOT NULL,
  `user_id` int NOT NULL,
  `status` varchar(100) NOT NULL,
  `created_dt` datetime DEFAULT CURRENT_TIMESTAMP,
  `modified_dt` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `job_post_id` (`job_post_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `apply_ibfk_1` FOREIGN KEY (`job_post_id`) REFERENCES `job_post` (`id`),
  CONSTRAINT `apply_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=107 DEFAULT CHARSET=utf8mb3;


-- pikatwo.comment definition

CREATE TABLE `comment` (
  `id` int NOT NULL AUTO_INCREMENT,
  `content` varchar(1024) NOT NULL,
  `commenter_id` int NOT NULL,
  `company_id` int NOT NULL,
  `created_dt` datetime DEFAULT CURRENT_TIMESTAMP,
  `modified_dt` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `commenter_id` (`commenter_id`),
  KEY `company_id` (`company_id`),
  CONSTRAINT `comment_ibfk_1` FOREIGN KEY (`commenter_id`) REFERENCES `user` (`id`),
  CONSTRAINT `comment_ibfk_2` FOREIGN KEY (`company_id`) REFERENCES `company` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb3;


-- pikatwo.deposit definition

CREATE TABLE `deposit` (
  `id` int NOT NULL AUTO_INCREMENT,
  `deposit_amount` int DEFAULT NULL,
  `deposit_dt` datetime DEFAULT NULL,
  `user_id` int NOT NULL,
  `created_dt` datetime DEFAULT CURRENT_TIMESTAMP,
  `modified_dt` datetime DEFAULT CURRENT_TIMESTAMP,
  `memo` varchar(1024) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `deposit_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=48720 DEFAULT CHARSET=utf8mb3;


-- pikatwo.favorite_companies definition

CREATE TABLE `favorite_companies` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `company_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `user_id` (`user_id`),
  KEY `company_id` (`company_id`),
  CONSTRAINT `favorite_companies_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`),
  CONSTRAINT `favorite_companies_ibfk_2` FOREIGN KEY (`company_id`) REFERENCES `company` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=54 DEFAULT CHARSET=utf8mb3;


-- pikatwo.memo definition

CREATE TABLE `memo` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `memo` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `id` (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `memo_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `user` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1224 DEFAULT CHARSET=utf8mb3;
