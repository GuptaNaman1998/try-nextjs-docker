CREATE TABLE PUBLIC.user_db(
usr_id text,
username text,
category text
);

CREATE TABLE PUBLIC.product_db(
usr_id text,
username text,
subscription_active boolean,
duration int,
day_1 jsonb,
day_2 jsonb,
day_3 jsonb,
day_4 jsonb,
day_5 jsonb,
day_6 jsonb,
day_7 jsonb
);
