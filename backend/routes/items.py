import os
from flask import Blueprint, request, jsonify, send_from_directory
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import db, Item
from werkzeug.utils import secure_filename

items_bp = Blueprint("items", __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads')
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Complete ADNU buildings with floors
ADNU_BUILDINGS = [
    {"building": "Gonzaga Hall", "floors": ["Grounds", "1st Floor", "2nd Floor", "3rd Floor", "4th Floor"]},
    {"building": "Martyr's Hall", "floors": ["Grounds", "1st Floor", "2nd Floor", "3rd Floor"]},
    {"building": "Rizal Library", "floors": ["Grounds", "1st Floor", "2nd Floor", "3rd Floor"]},
    {"building": "Kostka Hall", "floors": ["Grounds", "1st Floor", "2nd Floor", "3rd Floor", "4th Floor"]},
    {"building": "Xavier Hall", "floors": ["Grounds", "1st Floor", "2nd Floor", "3rd Floor"]},
    {"building": "Bellarmine Hall", "floors": ["Grounds", "1st Floor", "2nd Floor", "3rd Floor"]},
    {"building": "Canisius Hall", "floors": ["Grounds", "1st Floor", "2nd Floor"]},
    {"building": "Arrupe Hall", "floors": ["Grounds", "1st Floor", "2nd Floor", "3rd Floor"]},
    {"building": "Chapel", "floors": ["Grounds", "1st Floor"]},
    {"building": "Covered Court", "floors": ["Grounds"]},
    {"building": "Cafeteria", "floors": ["Grounds"]},
    {"building": "Main Gate Area", "floors": ["Grounds"]},
    {"building": "Parking Area", "floors": ["Grounds"]},
]

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def delete_image_file(image_url):
    if image_url:
        for fname in image_url.split(','):
            file_path = os.path.join(UPLOAD_FOLDER, fname.strip())
            if os.path.exists(file_path):
                os.remove(file_path)

# Serve uploaded images
@items_bp.route("/uploads/<filename>")
def serve_image(filename):
    return send_from_directory(UPLOAD_FOLDER, filename)

# Get all ADNU buildings and floors
@items_bp.route("/buildings", methods=["GET"])
def get_buildings():
    return jsonify(ADNU_BUILDINGS)

# Get all items (exclude logged-in user's items if exclude_user is passed)
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

# Get single item detail
@items_bp.route("/<int:id>", methods=["GET"])
def get_item(id):
    i = Item.query.get_or_404(id)
    return jsonify({
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
        "user_id": i.user_id,
        "created_at": str(i.created_at)
    })

@items_bp.route("/", methods=["POST"])
@jwt_required()
def create_item():
    user_id = get_jwt_identity()
    from datetime import datetime

    print("FILES RECEIVED:", request.files)
    print("FORM DATA:", request.form)

    name = request.form.get("name")
    category = request.form.get("category")
    report_type = request.form.get("report_type")
    location = request.form.get("location")
    floor = request.form.get("floor")
    date_str = request.form.get("date_reported")
    description = request.form.get("description")
    contact_info = request.form.get("contact_info")

    if not name or not category or not report_type or not location or not date_str:
        return jsonify({"message": "Missing required fields"}), 400

    date_obj = datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None

    image_filenames = []
    files = request.files.getlist('images')
    print("IMAGE FILES LIST:", files)
    for file in files:
        print("FILE:", file.filename)
        if file and file.filename != '' and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            unique_filename = f"{user_id}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}_{filename}"
            save_path = os.path.join(UPLOAD_FOLDER, unique_filename)
            file.save(save_path)
            print("SAVED TO:", save_path)
            image_filenames.append(unique_filename)

    image_filename = ','.join(image_filenames) if image_filenames else None
    print("FINAL IMAGE URL:", image_filename)

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

# Update item
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

    # Handle multiple photo update
    files = request.files.getlist('images')
    if files and any(f.filename != '' for f in files):
        # delete old images
        if item.image_url:
            for old_file in item.image_url.split(','):
                delete_image_file(old_file.strip())
        new_filenames = []
        for file in files:
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                unique_filename = f"{get_jwt_identity()}_{datetime.now().strftime('%Y%m%d%H%M%S%f')}_{filename}"
                file.save(os.path.join(UPLOAD_FOLDER, unique_filename))
                new_filenames.append(unique_filename)
        if new_filenames:
            item.image_url = ','.join(new_filenames)

    db.session.commit()
    return jsonify({"message": "Updated"})

# Delete item
@items_bp.route("/<int:id>", methods=["DELETE"])
@jwt_required()
def delete_item(id):
    item = Item.query.get_or_404(id)
    if str(item.user_id) != get_jwt_identity():
        return jsonify({"message": "Unauthorized"}), 403

    # Delete image file from uploads folder
    delete_image_file(item.image_url)

    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Deleted"})

# Update status only
@items_bp.route("/<int:id>/status", methods=["PATCH"])
@jwt_required()
def update_status(id):
    item = Item.query.get_or_404(id)
    data = request.json
    item.status = data["status"]
    db.session.commit()
    return jsonify({"message": "Status updated"})

# Get logged-in user's own items
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
        "user_id": i.user_id,
        "date_reported": str(i.date_reported),
        "description": i.description,
        "contact_info": i.contact_info
    } for i in items])