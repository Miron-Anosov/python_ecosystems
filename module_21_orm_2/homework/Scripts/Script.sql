-- Вставка данных в таблицу "authors"
INSERT INTO authors (name, surname, id) VALUES 
    ('Leo', 'Tolstoy', 1),
    ('Ernest', 'Hemingway', 2),
    ('Jane', 'Austen', 3),
    ('Fyodor', 'Dostoevsky', 4),
    ('Agatha', 'Christie', 5);

-- Вставка данных в таблицу "students"
INSERT INTO students (name, surname, phone, email, average_score, scholarship, id) VALUES
    ('John', 'Doe', '+7(901) 123-45-67', 'john@example.com', 4.5, 1, 1),
    ('Alice', 'Smith', '+7(902) 234-56-78', 'alice@example.com', 3.8, 0, 2),
    ('Michael', 'Johnson', '+7(903) 345-67-89', 'michael@example.com', 4.0, 1, 3),
    ('Emily', 'Williams', '+7(904) 456-78-90', 'emily@example.com', 3.2, 0, 4),
    ('William', 'Brown', '+7(905) 567-89-01', 'william@example.com', 4.1, 1, 5);

-- Вставка данных в таблицу "books"
INSERT INTO books (name, count, release_date, author_id, id) VALUES
    ('War and Peace', 30, '1869-01-01', 1, 1),
    ('The Old Man and the Sea', 15, '1952-09-01', 2, 2),
    ('Pride and Prejudice', 20, '1813-01-28', 3, 3),
    ('Crime and Punishment', 25, '1866-01-01', 4, 4),
    ('Murder on the Orient Express', 10, '1934-01-01', 5, 5),
    ('Anna Karenina', 25, '1877-01-01', 1, 6),
    ('For Whom the Bell Tolls', 20, '1940-10-21', 2, 7),
    ('Sense and Sensibility', 20, '1811-10-30', 3, 8),
    ('The Brothers Karamazov', 15, '1880-11-12', 4, 9),
    ('The Murder of Roger Ackroyd', 15, '1926-06-01', 5, 10);

-- Вставка данных в таблицу "receiving_books"
INSERT INTO receiving_books (book_id, student_id, date_of_issue, date_of_return, id) VALUES
    (1, 1, '2023-03-01', '2023-04-01', 1),
    (2, 1, '2023-03-15', NULL, 2),
    (5, 1, '2023-06-01', NULL, 8),
    (9, 1, '2023-06-15', '2023-06-25', 16),
    (10, 1, '2024-02-25', '2024-03-01', 18),
    (2, 2, '2023-04-01', NULL, 3),
    (1, 2, '2023-03-15', '2023-04-10', 10),
    (7, 2, '2023-06-15', NULL, 14),
    (5, 2, '2024-02-27', '2023-02-29', 19),
    (6, 2, '2024-02-20', '2023-02-22', 20),
    (3, 3, '2023-04-10', NULL, 4),
    (5, 3, '2023-06-15', NULL, 9),
    (2, 3, '2023-04-01', '2023-04-25', 11),
    (10, 3, '2023-05-01', '2023-05-10', 17),
    (3, 4, '2023-04-20', NULL, 5),
    (4, 4, '2023-05-01', NULL, 6),
    (6, 4, '2023-05-01', NULL, 13),
    (5, 4, '2024-02-27', '2023-02-28', 21),
    (9, 4, '2024-02-20', '2023-02-27', 22),
    (4, 5, '2023-05-15', NULL, 7),
    (3, 5, '2023-05-15', '2023-06-08', 12),
    (8, 5, '2023-05-01', '2023-05-10', 15);
