from flask import abort, make_response, jsonify
from app import db



def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        response = {"error": f"{cls.__name__} id {model_id} is invalid"}
        abort(make_response(response, 400))
        
    query = db.select(cls).where(cls.id == model_id)
    model = db.session.scalar(query)

    if not model:
        response = {"error": f"{cls.__name__} {model_id} not found"}
        abort(make_response(response, 404))

    return model


def create_model(cls, model_data):
    try:
        new_model = cls.from_dict(model_data)
    except (KeyError, ValueError) as e:
        response = {"details": "Invalid data"}
        abort(make_response(response, 400)) 

    db.session.add(new_model)
    db.session.commit()

    return new_model.to_dict()


def delete_model(model_instance):
    # print("🤖 DELETING:", model_instance, type(model_instance))
    db.session.delete(model_instance)
    db.session.commit()

    return jsonify({}), 204


def get_models_with_filters_and_sort(cls, filters=None):
    query = db.select(cls)

    if filters:
        for attribute, value in filters.items():
            if attribute == "sort":
                continue
            if hasattr(cls, attribute):
                query = query.where(getattr(cls, attribute).ilike(f"%{value}%"))
    
    sort = filters.get("sort")
    if sort == "asc":
        query = query.order_by(cls.title.asc())
    elif sort == "desc":
        query = query.order_by(cls.title.desc())
    else:
        query = query.order_by(cls.id)


    models = db.session.scalars(query.order_by(cls.id))
    return [model.to_dict() for model in models]

