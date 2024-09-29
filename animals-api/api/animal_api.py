from flask import Blueprint, request, jsonify
from models.animal import Animal, db
from broker.message_sender import BasicMessageSender
from config import Config
animal_blueprint = Blueprint('user_api', __name__)

@animal_blueprint.route('/healthcheck',methods=['GET'])
def health_check():
    return jsonify({'status': 'healthy'}), 200


@animal_blueprint.route('/animals/<int:id>', methods=['GET'])
def get_animal(id):
    """returns an animals based on its id 
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
    definitions:
      Animal:
        type: object
        properties:
            Name:
                type: string
            id:
                type: integer
            specie:
                type: string
            category:
                type: string
            habitat: 
                type: string
    responses:
      200:
        description: A animal correpoding the provided id
        schema:
          $ref: '#/definitions/Animal'
    """
    animal = Animal.query.get(id)

    if animal:
         
        return jsonify({
            'id': animal.id,
            'name': animal.name,
            'specie': animal.specie,
            'category': animal.category,
            'habitat': animal.habitat
        }), 200
    else:
        return jsonify({'error': 'Animal not found'}), 404

@animal_blueprint.route('/animals',methods=['GET'])
def list_animals():
    """returns animals list 
    ---
    definitions:
      Animals: 
        type: array
        items:
            $ref: '#definitions/Animal'
      Animal:
        type: object
        properties:
            Name:
                type: string
            id:
                type: integer
            specie:
                type: string
            category:
                type: string
            habitat: 
                type: string
    responses:
      200:
        description: A animal correpoding the provided id
        schema:
          $ref: '#/definitions/Animals'
    """
    animals = db.session.execute(db.select(Animal).order_by(Animal.name)).scalars()
    json_animals=  [{
            'id': animal.id,
            'name': animal.name,
            'specie': animal.specie,
            'category': animal.category,
            'habitat': animal.habitat
        } for animal in animals]
    
    return jsonify(json_animals), 200

@animal_blueprint.route('/animals', methods=['POST'])
def post_animal():
    """inserts a new animal animals list 
    ---
    description: Post a animal
    """
    data = request.get_json()
    name = data.get('name')
    specie = data.get('specie'),
    category = data.get('category'),
    habitat = data.get('habitat')

    
    animal = Animal(name=name, specie=specie,category=category,habitat=habitat)
    
    try:
        db.session.add(animal)
        db.session.commit()
        sender = BasicMessageSender(Config.BROKER_HOST,Config.BROKER_USERNAME,Config.BROKER_PASSWORD)
        sender.declare_queue('animal_created')
        sender.send_message(exchange='',routing_key="animal_created",body=animal.__json__())
        return jsonify({'message': f"Animal {animal.name} created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'error': str(e)}), 500