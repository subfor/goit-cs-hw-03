
-- 1) Отримати всі завдання певного користувача (user_id = 4)
SELECT * FROM tasks
WHERE user_id = 4;

-- 2) Вибрати завдання за певним статусом ('new'), використовуючи підзапит
SELECT * FROM tasks
WHERE status_id = (SELECT id FROM status WHERE name = 'new');

-- 3) Оновити статус конкретного завдання (id = 1) на 'in progress'
UPDATE tasks
SET status_id = (SELECT id FROM status WHERE name = 'in progress')
WHERE id = 1;

-- 4) Отримати список користувачів, які не мають жодного завдання
SELECT * FROM users
WHERE id NOT IN (SELECT DISTINCT user_id FROM tasks);

-- 5) Додати нове завдання для конкретного користувача (user_id = 7, статус 'new')
INSERT INTO tasks (title, description, status_id, user_id)
VALUES (
    'New Task',
    'This is a new task description',
    (SELECT id FROM status WHERE name = 'new'),
    7
);

-- 6) Отримати всі завдання, які ще не завершено (статус не 'completed')
SELECT * FROM tasks
WHERE status_id != (SELECT id FROM status WHERE name = 'completed');

-- 7) Видалити конкретне завдання (id = 31)
DELETE FROM tasks
WHERE id = 31;

-- 8) Знайти користувачів з певною електронною поштою (наприклад, містять '@example.com')
SELECT * FROM users
WHERE email LIKE '%@example.com%';

-- 9) Оновити ім'я користувача (user_id = 2)
UPDATE users
SET fullname = 'User Name'
WHERE id = 2;

-- 10) Отримати кількість завдань для кожного статусу
SELECT status.name, COUNT(tasks.id) AS task_count
FROM status
LEFT JOIN tasks ON status.id = tasks.status_id
GROUP BY status.name;

-- 11) Отримати завдання, які призначені користувачам з певною доменною частиною електронної пошти (підзапит, без JOIN)
SELECT *
FROM tasks
WHERE user_id IN (
    SELECT id FROM users WHERE email LIKE '%@example.com%'
);

-- 12) Використайте SELECT з умовою LIKE в поєднанні з JOIN, щоб вибрати завдання, призначені користувачам, чия електронна пошта містить певний домен
SELECT tasks.*
FROM tasks
JOIN users ON tasks.user_id = users.id
WHERE users.email LIKE '%@example.com%';

-- 13) Отримати список завдань, що не мають опису (NULL або порожній рядок)
SELECT * FROM tasks
WHERE description IS NULL OR description = '';

-- 14) Вибрати користувачів та їхні завдання, які є у статусі 'in progress'
SELECT users.fullname, tasks.*
FROM users
JOIN tasks ON users.id = tasks.user_id
JOIN status ON tasks.status_id = status.id
WHERE status.name = 'in progress';

-- 15) Отримати користувачів та кількість їхніх завдань
SELECT users.fullname, COUNT(tasks.id) AS task_count
FROM users
LEFT JOIN tasks ON users.id = tasks.user_id
GROUP BY users.id, users.fullname;
