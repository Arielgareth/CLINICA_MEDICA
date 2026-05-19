from database import db



class Pacientes(db.Model):
    __tablename__ = 'pacientes'
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    direccion = db.Column(db.String(200), nullable=False)
    telefono = db.Column(db.String(20), nullable=False)

    #relacion con consultas
    consultas = db.relationship('Consultas', back_populates='paciente',cascade='all, delete-orphan', lazy=True)



    def __init__(self, nombre, edad, direccion, telefono):
        self.nombre = nombre
        self.edad = edad
        self.direccion = direccion
        self.telefono = telefono


    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod    
    def get_all():
        return Pacientes.query.all()
    
    
    @staticmethod
    def get_by_id(paciente_id):
        return Pacientes.query.get(paciente_id)
    
    def update(self, nombre=None, edad=None, direccion=None, telefono=None):
        if nombre and edad and direccion and telefono:
            self.nombre = nombre
            self.edad = edad
            self.direccion = direccion
            self.telefono = telefono
      
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()