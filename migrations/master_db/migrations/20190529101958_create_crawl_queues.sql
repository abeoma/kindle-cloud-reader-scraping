
-- +goose Up
-- SQL in section 'Up' is executed when this migration is applied
CREATE TABLE `crawl_queues` (
    `id` varchar(255) not null,
    `user_id` varchar(255) not null,
    `priority` int unsigned not null,
    `crawl_status` int unsigned not null,
    `crawl_error` varchar(255),
    `error_message` varchar(255),
    `crawled_on` datetime DEFAULT CURRENT_TIMESTAMP(),
    `crawled_end` datetime DEFAULT CURRENT_TIMESTAMP(),
    `created_at` datetime DEFAULT CURRENT_TIMESTAMP() not null,
    `updated_at` datetime DEFAULT CURRENT_TIMESTAMP() not null,
    primary key (`id`),
    foreign key (`user_id`) references users(`id`),
    index (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- +goose Down
-- SQL section 'Down' is executed when this migration is rolled back
DROP TABLE `crawl_queues`;

