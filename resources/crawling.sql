use restaurant_crawler;

drop table if exists restaurant;
create table restaurant (
    restaurant_id int auto_increment primary key,
    name varchar(255) not null,
    branch varchar(255),
    cuisine_type varchar(255),
    created_dt timestamp default current_timestamp,
    crawled_dt timestamp
);

INSERT INTO restaurant (name, branch, cuisine_type)
VALUES
('Kimchi House', 'Gangnam', '한식'),
('Panda Express', 'Downtown', '중식'),
('Sushi King', 'Shibuya', '일식'),
('Olive Garden', 'Times Square', '이탈리아 요리'),
('Le Gourmet', 'Champs-Élysées', '프랑스 요리');


drop table if exists blog;
create table blog (
    blog_id int auto_increment primary key,
    restaurant_id int not null,
    title varchar(255) not null,
    link text not null,
    link_unique_key varchar(255) not null unique,
    blog_platform varchar(255) not null,
    created_dt timestamp default current_timestamp,
    crawled_dt timestamp,

    foreign key (restaurant_id) references restaurant(restaurant_id)
);

INSERT INTO blog (restaurant_id, title, link, link_unique_key, blog_platform)
VALUES
(1, 'Great Korean Food at Kimchi House', 'http://example.com/blog1', 'http://example.com/blog1', 'Naver'),
(2, 'Authentic Chinese Cuisine at Panda Express', 'http://example.com/blog2', 'http://example.com/blog2', 'Daum'),
(3, 'Fresh Sushi at Sushi King', 'http://example.com/blog3', 'http://example.com/blog3', 'Naver'),
(4, 'Delicious Italian Dishes at Olive Garden', 'http://example.com/blog4', 'http://example.com/blog4', 'Tistory'),
(5, 'Fine Dining at Le Gourmet', 'http://example.com/blog5', 'http://example.com/blog5', 'Naver');

drop table if exists content;
create table content (
    content_id int auto_increment primary key,
    restaurant_id int not null,
    blog_id int not null,
    content text,
    created_dt timestamp default current_timestamp,

    foreign key (restaurant_id) references restaurant(restaurant_id),
    foreign key (blog_id) references blog(blog_id)
);

INSERT INTO content (restaurant_id, blog_id, content)
VALUES
(1, 1, 'The Kimchi House in Gangnam offers a variety of traditional Korean dishes with a modern twist.'),
(2, 2, 'Panda Express in Downtown serves delicious and authentic Chinese food with quick service.'),
(3, 3, 'Sushi King in Shibuya has the freshest sushi and a cozy atmosphere.'),
(4, 4, 'Olive Garden at Times Square provides a fantastic Italian dining experience with a wide selection of wines.'),
(5, 5, 'Le Gourmet in Champs-Élysées offers a luxurious dining experience with exquisite French cuisine.');