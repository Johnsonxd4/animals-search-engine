from flask import Blueprint, request, jsonify
from models.animal import Animal, db
from broker.message_sender import BasicMessageSender
from config import Config
import logging

LOGGER = logging.getLogger('animals_api')
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
      404:
        description: Animal not found
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
    """Create a new animal
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: "Leo"
            specie:
              type: string
              example: "Lion"
            category:
              type: string
              example: "Mammal"
            habitat:
              type: string
              example: "Savanna"
    responses:
      201:
        description: Animal created successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Animal Leo created successfully"
      400:
        description: Bad request
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Error message describing what went wrong"
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
        sender.send_message(exchange='',routing_key="animal_created",body=animal.to_json())
        return jsonify({'message': f"Animal {animal.name} created successfully"}), 201
    except Exception as e:
        db.session.rollback()
        LOGGER.error(e)
        return jsonify({'error': str(e)}), 400



@animal_blueprint.route('/animals/<int:id>', methods=['PUT'])
def put_animal(id: int):
    """ Updates an existing animal
    ---
    parameters:
      - name: id
        in: path
        type: integer
        required: true
        description: ID of the animal to update

      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            name:
              type: string
              example: "Leo"
            specie:
              type: string
              example: "Lion"
            category:
              type: string
              example: "Mammal"
            habitat:
              type: string
              example: "Savanna"
    responses:
      200:
        description: Animal updated successfully
        schema:
          type: object
          properties:
            message:
              type: string
              example: "Animal updated successfully"
            animal:
              type: object
              properties:
                id:
                  type: integer
                  example: 1
                name:
                  type: string
                  example: "Leo"
                specie:
                  type: string
                  example: "Lion"
                category:
                  type: string
                  example: "Mammal"
                habitat:
                  type: string
                  example: "Savanna"
      400:
        description: Bad request
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Error message describing what went wrong"
      404:
        description: Animal not found
        schema:
          type: object
          properties:
            error:
              type: string
              example: "Animal not found"
    """

    data = request.get_json()
    name: String = data.get('name')
    specie: String = data.get('specie'),
    category: String = data.get('category'),
    habitat: String  = data.get('habitat')

    animal: Animal = db.session.query(Animal).get(id)
    if not animal:
        return jsonify({'error': 'Animal not found'}), 404
    
    animal.name = name
    animal.specie = specie
    animal.category = category
    animal.habitat = habitat
    try:
        db.session.commit()
        sender = BasicMessageSender(Config.BROKER_HOST,Config.BROKER_USERNAME,Config.BROKER_PASSWORD)
        sender.declare_queue('animal_updated')
        sender.send_message(exchange='',routing_key="animal_updated",body=animal.to_json())
        return jsonify(animal.to_json()), 200
    except Exception as e:
        db.session.rollback()
        print(e)
        return jsonify({'error': str(e)}), 400