import random

import users

users_map = {
    1: users.User(1, "user1@email.com", 494629130,
        {
            1: ["email", "telegram", "personal_account"],
            2: ["email", "telegram"],
        }
    ),
    2: users.User(2, "user2@email.com", 494629131,
        {
            1: ["email", "telegram", "personal_account"],
            2: ["email", "personal_account"],
            3: ["email"],
        }
    ),
    3: users.User(3, "user3@email.com", 494629132,
        {
            1: ["email", "telegram", "personal_account"],
            2: ["telegram", "personal_account"],
            3: ["telegram"],
        }
    ),
}


def random_theme_and_message(min_value, max_value):
    theme_id = random.randint(min_value, max_value)
    return theme_id, "Random theme message"
