from unittest import result
from flask_app.config.mysqlconnection import connectToMySQL
from datetime import datetime
import math
from flask import flash
from flask_app.models import models_user

# from flask_app.controllers import controllers_post

class Post:
    db_name = 'final_schema'
    def __init__(self,db_data):
        self.id = db_data['id']
        self.title = db_data['title']
        self.content = db_data['content']
        self.user_id = db_data['user_id']
        self.created_at = db_data['created_at']
        self.updated_at = db_data['updated_at']
        self.user = None

    def time_span(self):
        now = datetime.now()
        delta = now - self.created_at
        print(delta.days)
        print(delta.total_seconds())
        if delta.days > 0:
            return f"{delta.days} days ago"
        elif (math.floor(delta.total_seconds() / 60)) >= 60:
            return f"{math.floor(math.floor(delta.total_seconds() / 60)/60)} hours ago"
        elif delta.total_seconds() >= 60:
            return f"{math.floor(delta.total_seconds() / 60)} minutes ago"
        else:
            return f"{math.floor(delta.total_seconds())} seconds ago"

    @classmethod
    def get_one(cls,data):
        query = "SELECT * FROM posts WHERE id = %(id)s;"
        results = connectToMySQL(cls.db_name).query_db(query,data)
        return cls( results[0] )

    # @classmethod
    # def get_one(cls,data):
    #     query = "SELECT * FROM posts JOIN users ON posts.user_id = users.id WHERE posts.id = %(id)s;"
    #     results = connectToMySQL(cls.db_name).query_db(query,data)

    #     post = cls(results[0])
    #     post.user = results[0]['username']
    #     return post

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM posts;"
        results =  connectToMySQL(cls.db_name).query_db(query)
        all_posts = []
        for row in results:
            print("c" * 50)
            print(row)
            post = cls(row)
            post_data={
                "id": row["user_id"]
            }
            post.user=models_user.User.get_one(post_data)
            all_posts.append(post)
        return all_posts

    @classmethod
    def save(cls,data):
        print("A" * 50)
        print(data)
        query = "INSERT INTO posts (title, content, user_id) VALUES (%(title)s,%(content)s,%(user_id)s);"
        print(query, "%" * 60)
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def delete(cls,data):
        query = "DELETE FROM posts WHERE posts.id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @classmethod
    def update(cls, data):
        query = "UPDATE posts SET title=%(title)s, content=%(content)s, updated_at=NOW() WHERE id = %(id)s;"
        return connectToMySQL(cls.db_name).query_db(query,data)

    @staticmethod
    def validate_post(post):
        is_valid = True
        if len(post['title']) < 1:
            is_valid = False
            flash("Title must have at least 1 character", "post")
        if len(post['content']) < 1:
            is_valid = False
            flash("Content must have at least 1 character","post")
        return is_valid
