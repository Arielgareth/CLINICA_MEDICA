from database import db
from werkzeug.security import generate_password_hash, check_password_hash



class Medico(db.Model):
    __tablename__ = 'medicos'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    especialidad = db.Column(db.String(100), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)

    #relacion con consultas
    consultas = db.relationship('Consultas', back_populates='medico',cascade='all, delete-orphan', lazy=True)

    def __init__(self, nombre, especialidad, telefono, email, password):
        self.nombre = nombre
        self.especialidad = especialidad
        self.telefono = telefono
        self.email = email
        self.password = self.hash_password(password)

    @staticmethod
    def hash_password(password):
        return generate_password_hash(password)
    
    def verify_password(self, password):
        return check_password_hash(self.password, password)
    
    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod    
    def get_all():
        return Medico.query.all()
    
    @staticmethod
    def get_by_id(medico_id):
        return Medico.query.get(medico_id)
    
    def update(self, nombre=None, especialidad=None, telefono=None, email=None, password=None):
        if nombre:
            self.nombre = nombre
        if especialidad:
            self.especialidad = especialidad
        if telefono:
            self.telefono = telefono
        if email:
            self.email = email
        if password:
            self.password = self.hash_password(password)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()