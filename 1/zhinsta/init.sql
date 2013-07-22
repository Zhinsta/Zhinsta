CREATE TABLE `user` (
    `ukey` char(32) NOT NULL,
    `access_token` varchar(255) NOT NULL,
    `username` varchar(255) NOT NULL,
    `date_created` datetime NOT NULL,
	PRIMARY KEY (`ukey`)
) ENGINE=InnoDB CHARSET=utf8;
