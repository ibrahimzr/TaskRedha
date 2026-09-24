CREATE TABLE IF NOT EXISTS "user" (
    id SERIAL PRIMARY KEY,
    username VARCHAR NOT NULL UNIQUE,
    email VARCHAR NOT NULL UNIQUE,
    hashed_password VARCHAR NOT NULL,
    role VARCHAR NOT NULL DEFAULT 'customer',
    is_active BOOLEAN NOT NULL DEFAULT TRUE
);

CREATE TABLE IF NOT EXISTS author (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL,
    email VARCHAR
);

CREATE TABLE IF NOT EXISTS author_profile (
    author_id INTEGER PRIMARY KEY REFERENCES author(id),
    bio VARCHAR NOT NULL DEFAULT '',
    website VARCHAR
);

CREATE TABLE IF NOT EXISTS genre (
    id SERIAL PRIMARY KEY,
    name VARCHAR NOT NULL UNIQUE
);

CREATE TABLE IF NOT EXISTS book (
    id SERIAL PRIMARY KEY,
    title VARCHAR NOT NULL,
    author_id INTEGER NOT NULL REFERENCES author(id),
    price DOUBLE PRECISION NOT NULL,
    stock INTEGER NOT NULL DEFAULT 0
);

CREATE TABLE IF NOT EXISTS book_genre (
    book_id INTEGER NOT NULL REFERENCES book(id),
    genre_id INTEGER NOT NULL REFERENCES genre(id),
    PRIMARY KEY(book_id,genre_id)
);

CREATE TABLE IF NOT EXISTS "order" (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES "user"(id),
    book_id INTEGER NOT NULL REFERENCES book(id),
    quantity INTEGER NOT NULL,
    total_price DOUBLE PRECISION NOT NULL,
    status VARCHAR NOT NULL DEFAULT 'pending',
    created_at TIMESTAMP NOT NULL
);

CREATE INDEX IF NOT EXISTS ix_book_author_id ON book(author_id);
CREATE INDEX IF NOT EXISTS ix_book_genre_genre_id ON book_genre(genre_id);
CREATE INDEX IF NOT EXISTS ix_order_user_id ON "order"(user_id);
CREATE INDEX IF NOT EXISTS ix_order_book_id ON "order"(book_id);
