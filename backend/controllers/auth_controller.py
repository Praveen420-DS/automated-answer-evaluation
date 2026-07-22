from flask import jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from datetime import timedelta

from database.mongodb import users_collection


class AuthController:

    @staticmethod
    def register(data):

        users = users_collection()

        if users.find_one({"email": data["email"]}):

            return jsonify({

                "success": False,

                "message": "Email already exists"

            }),409

        user = {

            "fullName": data["fullName"],

            "email": data["email"],

            "password": generate_password_hash(
                data["password"]
            ),

            "role": data.get("role","student")

        }

        users.insert_one(user)

        return jsonify({

            "success":True,

            "message":"Registration Successful"

        }),201

    @staticmethod
    def login(data):

        user = users_collection().find_one({

            "email":data["email"]

        })

        if not user:

            return jsonify({

                "success":False,

                "message":"User Not Found"

            }),404

        if not check_password_hash(

            user["password"],

            data["password"]

        ):

            return jsonify({

                "success":False,

                "message":"Invalid Password"

            }),401

        token=create_access_token(

            identity=user["email"],

            additional_claims={

                "role":user["role"]

            },

            expires_delta=timedelta(days=1)

        )

        return jsonify({

            "success":True,

            "token":token,

            "role":user["role"],

            "name":user["fullName"]

        })