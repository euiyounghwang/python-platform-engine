-- Active: 1715042518972@@localhost@5432@postgres@postgres
SELECT * FROM postgres.user;
SELECT * FROM postgres.users_tb_topic;

-- Generated by the database client.
CREATE TABLE postgres."user"(
    user_id varchar(255) NOT NULL,
    user_name varchar(30) NOT NULL,
    user_age integer NOT NULL,
    created_at timestamp DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE postgres."users_tb_topic"(
    user_id varchar(255) NOT NULL,
    user_name varchar(30) NOT NULL,
    user_age integer NOT NULL,
    created_at timestamp DEFAULT CURRENT_TIMESTAMP
);

INSERT INTO postgres.user (user_id, user_name, user_age) VALUES ('euiyoung', 'ehwang', 11);
INSERT INTO postgres.user (user_id, user_name, user_age) VALUES ('test', 'ehwang', 12);
INSERT INTO postgres.user (user_id, user_name, user_age) VALUES ('test1', '12', 12);
INSERT INTO postgres.user (user_id, user_name, user_age) VALUES ('add', '12', 12);
INSERT INTO postgres.user (user_id, user_name, user_age) VALUES ('addd', '12', 12);
INSERT INTO postgres.user (user_id, user_name, user_age) VALUES ('with-consumer', '12', 12);
INSERT INTO postgres.user (user_id, user_name, user_age) VALUES ('with-consumer1', '12', 12);
INSERT INTO postgres.user (user_id, user_name, user_age) VALUES ('with-consumer2', '12', 12);
INSERT INTO postgres.user (user_id, user_name, user_age) VALUES ('aa', '12', 12);
INSERT INTO postgres.user (user_id, user_name, user_age) VALUES ('cc', '12', 12);