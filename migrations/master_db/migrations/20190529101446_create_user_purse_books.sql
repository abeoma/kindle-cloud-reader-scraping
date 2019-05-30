
-- +goose Up
-- SQL in section 'Up' is executed when this migration is applied
CREATE TABLE `user_purse_books` (
    `id` varchar(255) not null,
    `user_id` varchar(255) not null,
    `asin` varchar(255) not null,
    `title` varchar(255),
    `author` varchar(255),
    `image_src` varchar(255),
    `created_at` datetime DEFAULT CURRENT_TIMESTAMP() not null,
    `updated_at` datetime DEFAULT CURRENT_TIMESTAMP() not null,
    primary key (`id`),
    foreign key (`user_id`) references users(`id`),
    index (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- +goose Down
-- SQL section 'Down' is executed when this migration is rolled back
DROP TABLE `user_purse_books`;

