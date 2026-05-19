from database import db



class Consultas(db.Model):
    __tablename__ = 'consultas'
    id_consulta = db.Column(db.Integer, primary_key=True)
    fecha = db.Column(db.DateTime, nullable=False)
    diagnostico = db.Column(db.String(200), nullable=False)
    tratamiento = db.Column(db.String(200), nullable=False)
    id_medico = db.Column(db.Integer, db.ForeignKey('medicos.id'), nullable=False)
    id_paciente = db.Column(db.Integer, db.ForeignKey('pacientes.id'), nullable=False)
    
    #relacion con medico
    medico = db.relationship('Medico', back_populates='consultas')
    #relacion con paciente
    paciente = db.relationship('Pacientes', back_populates='consultas')
    
    
    def __init__(self, fecha, diagnostico, tratamiento, id_paciente, id_medico):
       
        self.id_paciente = id_paciente
        self.id_medico = id_medico
        self.fecha = fecha
        self.diagnostico = diagnostico
        self.tratamiento = tratamiento

    def save(self):
        db.session.add(self)
        db.session.commit()

    @staticmethod    
    def get_all():
        return Consultas.query.all()
    
    @staticmethod    
    def get_by_id(consulta_id):
        return Consultas.query.get(consulta_id)
    
    def update(self, fecha=None, diagnostico=None, tratamiento=None, id_paciente=None, id_medico=None):
        if fecha and diagnostico and tratamiento and id_paciente and id_medico:
            self.fecha = fecha
            self.diagnostico = diagnostico
            self.tratamiento = tratamiento
            self.id_paciente = id_paciente
            self.id_medico = id_medico
        db.session.commit()
    
    def delete(self):
        db.session.delete(self)
        db.session.commit()