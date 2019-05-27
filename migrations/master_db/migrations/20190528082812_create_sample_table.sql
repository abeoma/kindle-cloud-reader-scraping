
-- +goose Up
-- SQL in section 'Up' is executed when this migration is applied
CREATE TABLE `sampletable` (
    `id` varchar(255) not null,
    `url` varchar(255) not null,
    `cache_file_path` varchar(255) not null,
    `is_found` tinyint not null,
    `category` varchar(255),
    `name` varchar(255),
    `price` varchar(255),
    `currency` varchar(255),
    `images_json` text,
    `is_listed_in_buyma` bool DEFAULT False not null, 
    `created_at` datetime DEFAULT CURRENT_TIMESTAMP() not null,
    `updated_at` datetime DEFAULT CURRENT_TIMESTAMP() not null,
    primary key (`id`),
    index (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- +goose Down
-- SQL section 'Down' is executed when this migration is rolled back
DROP TABLE `sampletable`;

