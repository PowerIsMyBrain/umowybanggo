-- zapytanie pobierające dane postów
SELECT * FROM posts 
-- zapytanie edytujące posta
UPDATE posts SET title='Nowy tytuł', content='Nowy treść' WHERE id=1;
-- zapytanie dodając nowy post do bazy danych
INSERT INTO posts (title, author_id, created_at) VALUES ('Tytuł postu', 2, '2021-09-30');
-- zapytanie usuwające post z bazy danych
DELETE FROM posts WHERE id = 4;


-- zapytanie pobierajace wszystkich użytkowników
SELECT * FROM users;
-- zapytanie dodawajace nowego uzytkownika do systemu
INSERT INTO users(username, email, password, created_at) VALUES('nowyUzyszk', 'email@test.pl', '$2b$10$QYdVh5786lHGj');
--zapytanie edytujące dane użytkownika
UPDATE users SET email='nowa@email.pl', password='hasło' WHERE id=5;
--zapytanie usuwające użytkownika z systemu
DELETE FROM users WHERE id=6;

-- zapytanie pobierające wszyskie komentarze
SELECT c.* FROM comments AS c JOIN posts AS p ON c.post_id = p.id;
-- zapytanie usuwające komentarze 
DELETE FROM comments WHERE id=4;

-- zapytanie pobierające wszystkich subskrybentów
SELECT * FROM subscriptions WHERE user_id=(SELECT id FROM users WHERE username="Janek");

-- zapytanie pobierajace team
SELECT t.* FROM teams AS t JOIN members AS m ON t.id = m.team_id WHERE m.user_id=(SELECT id FROM users WHERE username="Janek");
-- zapytanie aktualizujące team
INSERT  INTO teams(name) VALUES('Zespół A'),('Zespół B');

-- zapytanie pobierające autorów
SELECT u.* FROM users AS u JOIN posts AS p ON u.id=p.author_id GROUP BY u.id ORDER BY COUNT(*)


