from flask import request, redirect, url_for,Blueprint

from models.pacientes_model import Pacientes
from views import pacientes_view

paciente_bp = Blueprint('paciente', __name__, url_prefix='/pacientes')

@paciente_bp.route('/')
def index():
    pacientes = Pacientes.get_all()
    return pacientes_view.list(pacientes)

@paciente_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        nombre = request.form['nombre']
        edad = request.form['edad']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
        
        
        paciente = Pacientes(nombre=nombre, edad=edad, direccion=direccion, telefono=telefono)
        paciente.save()
        
        return redirect(url_for('paciente.index'))
    return pacientes_view.create()

@paciente_bp.route('/edit/<int:paciente_id>', methods=['GET', 'POST'])
def edit(paciente_id):
    paciente = Pacientes.get_by_id(paciente_id)
    if request.method == 'POST':
        nombre = request.form['nombre']
        edad = request.form['edad']
        direccion = request.form['direccion']
        telefono = request.form['telefono']
       
        
        paciente.update(nombre=nombre, edad=edad, direccion=direccion, telefono=telefono)
        
        return redirect(url_for('paciente.index'))
    return pacientes_view.edit(paciente)

@paciente_bp.route('/delete/<int:paciente_id>', methods=['POST'])
def delete(paciente_id):
    paciente = Pacientes.get_by_id(paciente_id)
    paciente.delete()
    return redirect(url_for('paciente.index'))