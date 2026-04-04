from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Item

items_bp = Blueprint("items", __name__)

@items_bp.route("/", methods=["GET"])
def get_items():
    items = Item.query.all()
    return jsonify([{
        "item_id": i.item_id,
        "name": i.name,
        "category": i.category,
        "report_type": i.report_type,
        "status": i.status,
        "location": i.location,
        "description": i.description,
        "contact_info": i.contact_info,
        "date_reported": str(i.date_reported)
    } for i in items])

@items_bp.route("/", methods=["POST"])
@jwt_required()
def create_item():
    data = request.json
    user_id = get_jwt_identity()
    from datetime import datetime
    date_str = data.get("date_reported")
    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None
    item = Item(
        user_id=user_id,
        name=data["name"],
        category=data["category"],
        report_type=data["report_type"],
        status="Active",
        location=data["location"],
        date_reported=date_obj,
        description=data.get("description"),
        contact_info=data.get("contact_info")
    )
    db.session.add(item)
    db.session.commit()
    return jsonify({"message": "Item reported"}), 201

@items_bp.route("/<int:id>", methods=["PUT"])
@jwt_required()
def update_item(id):
    item = Item.query.get_or_404(id)
    if str(item.user_id) != get_jwt_identity():
        return jsonify({"message": "Unauthorized"}), 403
    data = request.json
    item.name = data.get("name", item.name)
    item.category = data.get("category", item.category)
    item.report_type = data.get("report_type", item.report_type)
    item.location = data.get("location", item.location)
    item.description = data.get("description", item.description)
    item.contact_info = data.get("contact_info", item.contact_info)
    db.session.commit()
    return jsonify({"message": "Updated"})

@items_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_item(id):
    item = Item.query.get_or_404(id)
    if str(item.user_id) != get_jwt_identity():
        return jsonify({"message": "Unauthorized"}), 403
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Deleted"})

@items_bp.route("/<int:id>/status", methods=["PATCH"])
@jwt_required()
def update_status(id):
    item = Item.query.get_or_404(id)
    data = request.json
    item.status = data["status"]
    db.session.commit()
    return jsonify({"message": "Status updated"})

@items_bp.route("/mine", methods=["GET"])
@jwt_required()
def get_my_items():
    user_id = get_jwt_identity()
    items = Item.query.filter_by(user_id=user_id).all()
    return jsonify([{
        "item_id": i.item_id,
        "name": i.name,
        "category": i.category,
        "report_type": i.report_type,
        "status": i.status,
        "location": i.location
    } for i in items])