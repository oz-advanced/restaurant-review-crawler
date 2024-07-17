
drop table if exists blog;
create table blog (
    blog_id int auto_increment primary key,
    title varchar(255),
    link text,
    content text
);
