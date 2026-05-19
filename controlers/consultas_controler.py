from flask import request, redirect, url_for,Blueprint, send_file
from datetime import datetime
from openpyxl import Workbook
from io import BytesIO



from models.consultas_model import Consultas
from models.medicos_model import Medico
from models.pacientes_model import Pacientes

from views import consultas_view

consulta_bp = Blueprint('consulta', __name__, url_prefix='/consultas')

@consulta_bp.route('/')
def index():
    consultas = Consultas.get_all()
    return consultas_view.list(consultas)

@consulta_bp.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        fecha_str = request.form['fecha']

        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        diagnostico = request.form['diagnostico']
        tratamiento = request.form['tratamiento']
        id_paciente = request.form['id_paciente']
        id_medico = request.form['id_medico']
        
        
        consulta = Consultas(fecha=fecha, diagnostico=diagnostico, tratamiento=tratamiento, id_paciente=id_paciente, id_medico=id_medico)
        consulta.save()
        
        return redirect(url_for('consulta.index'))
    medicos = Medico.query.all()
    pacientes = Pacientes.query.all()
    return consultas_view.create(medicos, pacientes)

@consulta_bp.route('/edit/<int:consulta_id>', methods=['GET', 'POST'])
def edit(consulta_id):
    consulta = Consultas.get_by_id(consulta_id)
    if request.method == 'POST':
        fecha_str = request.form['fecha']
        fecha = datetime.strptime(fecha_str, '%Y-%m-%d').date()
        diagnostico = request.form['diagnostico']   
        tratamiento = request.form['tratamiento']
        id_paciente = request.form['id_paciente']
        id_medico = request.form['id_medico']

       
        
        consulta.update(fecha=fecha, diagnostico=diagnostico, tratamiento=tratamiento, id_paciente=id_paciente, id_medico=id_medico)
        
        return redirect(url_for('consulta.index'))
    medicos = Medico.query.all()
    pacientes = Pacientes.query.all()
    return consultas_view.edit(consulta, medicos, pacientes)

@consulta_bp.route('/delete/<int:consulta_id>', methods=['POST'])
def delete(consulta_id):
    consulta = Consultas.get_by_id(consulta_id)
    consulta.delete()
    return redirect(url_for('consulta.index'))


@consulta_bp.route('/export/excel')
def export_excel():

    consultas = Consultas.get_all()

    wb = Workbook()
    ws = wb.active
    ws.title = "Consultas"

    # Encabezados
    ws.append([
        'ID',
        'Fecha',
        'Diagnostico',
        'Tratamiento',
        'Medico',
        'Paciente'
    ])

    # Datos
    for c in consultas:
        ws.append([
            c.id_consulta,
            str(c.fecha),
            c.diagnostico,
            c.tratamiento,
            c.medico.nombre,
            c.paciente.nombre
        ])

    # Guardar en memoria
    archivo = BytesIO()
    wb.save(archivo)
    archivo.seek(0)

    return send_file(
        archivo,
        as_attachment=True,
        download_name='consultas.xlsx',
        mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )