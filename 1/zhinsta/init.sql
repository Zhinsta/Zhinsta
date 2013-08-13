CREATE TABLE `user` (
    `ukey` varchar(255) NOT NULL,
    `access_token` varchar(255) NOT NULL,
    `username` varchar(255) NOT NULL,
    `pic` varchar(255) NOT NULL,
    `date_created` datetime NOT NULL,
	PRIMARY KEY (`ukey`)
) ENGINE=InnoDB CHARSET=utf8;
CREATE TABLE `follow` (
    `ukey` varchar(128) NOT NULL,
    `follow_ukey` varchar(128) NOT NULL,
    `date_created` datetime NOT NULL,
	PRIMARY KEY (`ukey`, `follow_ukey`)
) ENGINE=InnoDB CHARSET=utf8;
CREATE TABLE `like` (
    `ukey` varchar(128) NOT NULL,
    `media` varchar(128) NOT NULL,
    `date_created` datetime NOT NULL,
	PRIMARY KEY (`ukey`, `media`)
) ENGINE=InnoDB CHARSET=utf8;
