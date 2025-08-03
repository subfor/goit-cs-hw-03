import random

from db import DatabaseSession
from faker import Faker

fake = Faker()


def get_status_ids(cursor):
    cursor.execute("SELECT id FROM status ORDER BY id")
    return [row[0] for row in cursor.fetchall()]


def main():
    with DatabaseSession() as session:
        cur = session.cursor

        # Статуси (на всяк випадок)
        statuses = [("new",), ("in progress",), ("completed",)]
        cur.executemany(
            "INSERT INTO status (name) VALUES (%s) ON CONFLICT DO NOTHING", statuses
        )
        cur.connection.commit()
        status_ids = get_status_ids(cur)

        # Генеруємо та додаємо 50 юзерів
        users = [(fake.name(), fake.unique.email()) for _ in range(50)]
        cur.executemany("INSERT INTO users (fullname, email) VALUES (%s, %s)", users)
        cur.connection.commit()

        # 3. Отримуємо всі id доданих юзерів
        cur.execute("SELECT id FROM users ORDER BY id DESC LIMIT 50")
        user_ids = [row[0] for row in cur.fetchall()][
            ::-1
        ]  # реверс — щоб зберегти правильний порядок

        # Генеруємо задачі для кожного юзера, рандомною кількістю від 0 до 10 і з випадковим статусом
        all_tasks = []
        for uid in user_ids:
            for _ in range(random.randint(0, 10)):
                all_tasks.append(
                    (
                        fake.sentence(nb_words=4),
                        fake.text(max_nb_chars=70),
                        random.choice(status_ids),
                        uid,
                    )
                )

        # Вставляємо всі задачі
        cur.executemany(
            "INSERT INTO tasks (title, description, status_id, user_id) VALUES (%s, %s, %s, %s)",
            all_tasks,
        )
        cur.connection.commit()

    print("Seeding complete!")


if __name__ == "__main__":
    main()
