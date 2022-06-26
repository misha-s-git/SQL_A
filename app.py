import json
import datetime

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from models import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///mybase.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JSON_AS_ASCII'] = False
db = SQLAlchemy(app)


@app.route('/users', methods=['GET', 'POST'])
def get_users():
    if request.method == 'GET':
        result = []
        for user in User.query.all():
            result.append(user.to_dict())
        return jsonify(result)
    if request.method == 'POST':
        user = json.loads(request.data)
        user_obj = User(
            id=user['id'],
            first_name=user['first_name'],
            last_name=user['last_name'],
            age=user['age'],
            email=user['email'],
            role=user['role'],
            phone=user['phone']
        )
        db.session.add(user_obj)
        db.session.commit()
        db.session.close()
        return "Пользователь создан в базе данных", 200


@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def one_user(user_id):
    if request.method == 'GET':
        user = User.query.get(user_id)
        if user is None:
            return "Не найдено"
        else:
            return jsonify(user.to_dict())
    elif request.method == 'PUT':
        user_data = json.loads(request.data)
        user = db.session.query(User).get(user_id)
        if user is None:
            return "Пользователь не найден!", 404
        user.first_name = user_data['first_name']
        user.last_name = user_data['last_name']
        user.phone = user_data['phone']
        user.role = user_data['role']
        user.email = user_data['email']
        user.age = user_data['age']
        db.session.add(user)
        db.session.commit()
        return f"Объект с id {user_id} успешно изменён!", 200
    elif request.method == 'DELETE':
        user = db.session.query(User).get(user_id)
        if user is None:
            return "Пользователь не найден", 404
        db.session.delete(user)
        db.session.commit()
        db.session.close()
        return f"Объект с id {user_id} успешно удален!", 200



@app.route('/orders', methods=['GET', 'POST'])
def orders():
    if request.method == 'GET':
        result = []
        for order in Order.query.all():
            result.append(order.to_dict())
        return jsonify(result)
    if request.method == 'POST':
        order = json.loads(request.data)
        month_star, day_start, year_start = [int(o) for o in order['start_date'].split("/")]
        month_end, day_end, year_end = order['end_date'].split("/")
        order_obj = Order(
            id=order['id'],
            name=order['name'],
            description=order['description'],
            start_date=datetime.date(year=year_start, month=month_star, day=day_start),
            end_date=datetime.date(year=int(year_end), month=int(month_end), day=int(day_end)),
            address=order['address'],
            price=order['price'],
            customer_id=order['customer_id'],
            executor_id=order['executor_id']
        )
        db.session.add(order_obj)
        db.session.commit()
        db.session.close()
        return "Заказ создан в базе данных", 200


@app.route('/orders/<int:order_id>', methods=['GET', 'PUT', 'DELETE'])
def one_order(order_id):
    if request.method == 'GET':
        order = Order.query.get(order_id)
        if order is None:
            return "Заказ не найден"
        else:
            return jsonify(order.to_dict())


@app.route('/offers', methods=['GET', 'POST'])
def offers():
    if request.method == 'GET':
        result = []
        for offer in Offer.query.all():
            result.append(offer.to_dict())
        return jsonify(result)
    if request.method == 'POST':
        offer = json.loads(request.data)
        offer_obj = Offer(
            id=offer['id'],
            order_id=offer['order_id'],
            executor_id=offer['executor_id']
        )
        db.session.add(offer_obj)
        db.session.commit()
        db.session.close()
        return "Предложение создано в базе данных", 200


@app.route('/offers/<int:offer_id>', methods=['GET', 'PUT', 'DELETE'])
def one_offer(offer_id):
    if request.method == 'GET':
        offer = Offer.query.get(offer_id)
        if offer is None:
            return "Предложение не найдено"
        else:
            return jsonify(offer.to_dict())


if __name__ == '__main__':
    app.run()
