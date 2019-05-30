
-- +goose Up
-- SQL in section 'Up' is executed when this migration is applied
CREATE TABLE `users` (
    `id` varchar(255) not null,
    `email` varchar(255) not null,
    `password` varchar(255) not null,
    `name` varchar(255) not null,
    `created_at` datetime DEFAULT CURRENT_TIMESTAMP() not null,
    `updated_at` datetime DEFAULT CURRENT_TIMESTAMP() not null,
    primary key (`id`, `email`),
    index (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- +goose Down
-- SQL section 'Down' is executed when this migration is rolled back
DROP TABLE `users`;

