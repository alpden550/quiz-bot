import redis
import os
import json
from dotenv import load_dotenv


def get_user(db, user_id):
    user = db.get(user_id)
    if user:
        return json.loads(user)


def create_user(db, user_id, question, answer):
    user = {
        'question': question,
        'last_answer': answer,
    }
    db.set(user_id, json.dumps(user))


def update_user(db, user_id, question, answer):
    user = json.loads(db.get(user_id))

    user.update({'question': question, 'last_answer': answer})
    db.set(user_id, json.dumps(user))


def clear_user(db, user_id):
    db.set(user_id, '')


def save_user(db, user_id, question, answer):
    user = get_user(db, user_id)
    if user:
        update_user(db, user_id, question, answer)
    else:
        create_user(db, user_id, question, answer)


def main():
    load_dotenv()
    db_url = os.getenv('REDIS_DATABASE')
    db_port = os.getenv('REDIS_PORT')
    db_password = os.getenv('REDIS_PSWRD')

    db = redis.StrictRedis(
        host=db_url, port=db_port, password=db_password,
        charset='utf-8', decode_responses=True)


if __name__ == "__main__":
    load_dotenv()
    main()
