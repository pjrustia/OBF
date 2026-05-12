import os
from flask import Blueprint, request, jsonify, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Item
from werkzeug.utils import secure_filename

items_bp = Blueprint("items", __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@items_bp.route("/uploads/<filename>")
def serve_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

@items_bp.route("/", methods=["GET"])
def get_items():
    exclude_user = request.args.get("exclude_user")
    query = Item.query
    if exclude_user:
        query = query.filter(Item.user_id != exclude_user)
    items = query.all()
    return jsonify([{
        "item_id": i.item_id,
        "name": i.name,
        "category": i.category,
        "report_type": i.report_type,
        "status": i.status,
        "location": i.location,
        "floor": i.floor,
        "description": i.description,
        "contact_info": i.contact_info,
        "date_reported": str(i.date_reported),
        "image_url": i.image_url,
        "user_id": i.user_id
    } for i in items])

@items_bp.route("/", methods=["POST"])
@jwt_required()
def create_item():
    user_id = get_jwt_identity()
    from datetime import datetime

    name = request.form.get("name")
    category = request.form.get("category")
    report_type = request.form.get("report_type")
    location = request.form.get("location")
    floor = request.form.get("floor")
    date_str = request.form.get("date_reported")
    description = request.form.get("description")
    contact_info = request.form.get("contact_info")

    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None

    # Handle photo upload
    image_filename = None
    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename != '' and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_filename = f"{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
            file.save(os.path.join(UPLOAD_FOLDER, unique_filename))
            image_filename = unique_filename

    item = Item(
        user_id=user_id,
        name=name,
        category=category,
        report_type=report_type,
        status="Active",
        location=location,
        floor=floor,
        date_reported=date_obj,
        description=description,
        contact_info=contact_info,
        image_url=image_filename
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

    from datetime import datetime

    item.name = request.form.get("name", item.name)
    item.category = request.form.get("category", item.category)
    item.report_type = request.form.get("report_type", item.report_type)
    item.location = request.form.get("location", item.location)
    item.floor = request.form.get("floor", item.floor)
    item.description = request.form.get("description", item.description)
    item.contact_info = request.form.get("contact_info", item.contact_info)

    if 'image' in request.files:
        file = request.files['image']
        if file and file.filename != '' and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_filename = f"{get_jwt_identity()}_{datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
            file.save(os.path.join(UPLOAD_FOLDER, unique_filename))
            item.image_url = unique_filename

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
        "location": i.location,
        "floor": i.floor,
        "image_url": i.image_url,
        "user_id": i.user_id
    } for i in items])