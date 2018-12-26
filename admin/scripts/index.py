DROP INDEX `base_data_pubtime` ON `base_data`;
CREATE INDEX `base_data_pubtime` ON `base_data` (`pubtime`);