import re
from dataclasses import asdict
from datetime import datetime

from app.exc.lead_except import WrongPhoneFormat
from app.models.lead_model import Lead
from flask import Blueprint, current_app, jsonify, request
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.exc import UnmappedInstanceError

bp = Blueprint("lead", __name__)

@bp.route("/lead", methods=["POST"])
def create():
    data = request.get_json()
    try:
        check_phone = bool(re.fullmatch('\(\d{2}\)\d{4,5}\-\d{4}', data['phone']))
        if not check_phone:
            raise WrongPhoneFormat

        new_lead = Lead(
            name=data["name"],
            email=data["email"],
            phone=data["phone"],
            creation_date=datetime.now(),
            last_visit=datetime.now(),
        )
        session = current_app.db.session

        session.add(new_lead)
        session.commit()

        remove_id = asdict(new_lead)
        del remove_id['id']
        return jsonify(remove_id), 201            
    
    except WrongPhoneFormat:
        return {'error': 'wrong phone format'}, 400

    except IntegrityError:
        return {'error': 'email or/and phone already registered'}, 409

@bp.route("/lead", methods=["GET"])
def get_all():
    query = Lead.query.order_by(desc(Lead.visits)).all() 
    if not query:
        return {'error': 'no data found'}, 404
    return jsonify(query), 200


@bp.route("/lead", methods=["PATCH"])
def patch():
    try:
        data_email = request.get_json()['email']
        if type(data_email) != str:
            raise TypeError
            
    except KeyError:
        return {'error': 'wrong parameter or/and value'}, 400
        
    except TypeError:
        return {'error': 'wrong parameter or/and value'}, 400

    try:
        patch_query = Lead.query.filter_by(email=data_email).first()
        patch_query.last_visit = datetime.now()
        patch_query.visits = patch_query.visits + 1
    except AttributeError:
        return {'error': 'no data found'}, 404

    session = current_app.db.session

    session.add(patch_query)
    session.commit()
    return '', 204

@bp.route("/lead", methods=['DELETE'])
def delete():
    try:
        data_email = request.get_json()['email']
        if type(data_email) != str:
            raise TypeError
            
    except KeyError:
        return {'error': 'wrong parameter or/and value'}, 400
        
    except TypeError:
        return {'error': 'wrong parameter or/and value'}, 400
               
    try:
        patch_query = Lead.query.filter_by(email=data_email).first()
        
        session = current_app.db.session
        
        session.delete(patch_query)
        session.commit()
    except UnmappedInstanceError:
        return {'error': 'no data found'}, 404

    return '', 204

