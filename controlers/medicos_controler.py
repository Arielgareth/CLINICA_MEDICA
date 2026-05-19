from flask import request, redirect, url_for,Blueprint
from werkzeug.security import generate_password_hash
from models.medicos_model import Medico
from views import medicos_view

medico_bp = Blueprint('medico', __name__, url_prefix='/medicos')

@medico_bp.route('/')
def index():
    medicos = Medico.get_all()
    return medicos_view.list(medicos)

@medico_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        nombre = request.form['nombre']
        especialidad = request.form['especialidad']
        telefono = request.form['telefono']
        email = request.form['email']
        password = request.form['password']
        
        medico = Medico(nombre=nombre, especialidad=especialidad, telefono=telefono, email=email, password=password)
        medico.save()
        
        return redirect(url_for('medico.index'))
    return medicos_view.create()

@medico_bp.route('/edit/<int:medico_id>', methods=['GET', 'POST'])
def edit(medico_id):
    medico = Medico.get_by_id(medico_id)
    if request.method == 'POST':
        nombre = request.form['nombre']
        especialidad = request.form['especialidad']
        telefono = request.form['telefono']
        email = request.form['email']
        password = request.form['password']
        
        medico.update(nombre=nombre, especialidad=especialidad, telefono=telefono, email=email, password=password)
        
        return redirect(url_for('medico.index'))
    return medicos_view.edit(medico)

@medico_bp.route('/delete/<int:medico_id>', methods=['POST'])
def delete(medico_id):
    medico = Medico.get_by_id(medico_id)
    medico.delete()
    return redirect(url_for('medico.index'))