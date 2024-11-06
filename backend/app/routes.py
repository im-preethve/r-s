from flask import Blueprint, request, jsonify, render_template, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from app.models import User, MenuItem, Order, OrderItem
from app import db, bcrypt
import os

main = Blueprint('main', __name__)

# Serve the index page
@main.route('/')
def index():
    return render_template('index.html')

# Route to serve CSS files
@main.route('/css/<path:filename>')
def serve_css(filename):
    return send_from_directory('css', filename)

# Route to serve JS files
@main.route('/js/<path:filename>')
def serve_js(filename):
    return send_from_directory('js', filename)

# Route to serve images
@main.route('/images/<path:filename>')
def serve_images(filename):
    return send_from_directory('images', filename)

# Authentication routes
@main.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email already exists'}), 400
        
    hashed_password = bcrypt.generate_password_hash(data['password']).decode('utf-8')
    user = User(
        username=data['username'],
        email=data['email'],
        password=hashed_password
    )
    
    db.session.add(user)
    db.session.commit()
    
    return jsonify({'message': 'Registration successful'}), 201

@main.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    
    if user and bcrypt.check_password_hash(user.password, data['password']):
        login_user(user)
        return jsonify({
            'message': 'Login successful',
            'user': {
                'id': user.id,
                'username': user.username,
                'is_admin': user.is_admin
            }
        }), 200
    
    return jsonify({'error': 'Invalid credentials'}), 401

@main.route('/logout')
@login_required
def logout():
    logout_user()
    return jsonify({'message': 'Logout successful'}), 200

# Menu routes
@main.route('/menu/view')
def view_menu():
    menu_items = MenuItem.query.all()
    return jsonify([{
        'id': item.id,
        'name': item.name,
        'description': item.description,
        'price': item.price,
        'image_url': item.image_url
    } for item in menu_items]), 200

@main.route('/menu/add', methods=['POST'])
@login_required
def add_menu_item():
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
        
    data = request.get_json()
    item = MenuItem(
        name=data['name'],
        description=data['description'],
        price=data['price'],
        image_url=data.get('image_url')
    )
    
    db.session.add(item)
    db.session.commit()
    
    return jsonify({'message': 'Menu item added successfully'}), 201

# Order routes
@main.route('/api/order', methods=['POST'])
@login_required
def api_place_order():
    data = request.get_json()

    # Validate input data
    if not data or 'order' not in data or 'quantity' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    # Find the menu item (you may need to adjust this to fit your data structure)
    menu_item = MenuItem.query.filter_by(name=data['order']).first()
    if not menu_item:
        return jsonify({'error': 'Menu item not found'}), 404

    total_amount = menu_item.price * int(data['quantity'])

    # Create a new order
    order = Order(
        user_id=current_user.id,
        total_amount=total_amount,
        status='Pending'
    )

    db.session.add(order)
    db.session.flush()  # Get the order ID

    # Create order items
    order_item = OrderItem(
        order_id=order.id,
        menu_item_id=menu_item.id,
        quantity=int(data['quantity'])
    )
    db.session.add(order_item)
    db.session.commit()

    return jsonify({'message': 'Order placed successfully', 'order_id': order.id}), 201
@main.route('/order/view')
@login_required
def view_orders():
    if current_user.is_admin:
        orders = Order.query.all()
    else:
        orders = Order.query.filter_by(user_id=current_user.id).all()
    
    return jsonify([{
        'id': order.id,
        'user_id': order.user_id,
        'status': order.status,
        'order_time': order.order_time.isoformat(),
        'total_amount': order.total_amount,
        'items': [{
            'menu_item_id': item.menu_item_id,
            'quantity': item.quantity
        } for item in order.items]
    } for order in orders]), 200

@main.route('/order/update_status/<int:id>', methods=['PUT'])
@login_required
def update_order_status(id):
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    order = Order.query.get_or_404(id)
    
    order.status = data['status']
    db.session.commit()
    
    return jsonify({'message': 'Order status updated successfully'}), 200

@main.route('/menu/update/<int:id>', methods=['PUT'])
@login_required
def update_menu_item(id):
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.get_json()
    item = MenuItem.query.get_or_404(id)
    
    item.name = data.get('name', item.name)
    item.description = data.get('description', item.description)
    item.price = data.get('price', item.price)
    item.image_url = data.get('image_url', item.image_url)
    
    db.session.commit()
    
    return jsonify({'message': 'Menu item updated successfully'}), 200

@main.route('/menu/delete/<int:id>', methods=['DELETE'])
@login_required
def delete_menu_item(id):
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    item = MenuItem.query.get_or_404(id)
    db.session.delete(item)
    db.session.commit()
    
    return jsonify({'message': 'Menu item deleted successfully'}), 200
