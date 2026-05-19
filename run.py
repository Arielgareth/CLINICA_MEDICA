from flask import Flask, request, redirect, url_for
from controlers import consultas_controler, medicos_controler, pacientes_controler
from database import db
import os


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///clinica.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

app.register_blueprint(medicos_controler.medico_bp)
app.register_blueprint(pacientes_controler.paciente_bp)
app.register_blueprint(consultas_controler.consulta_bp)

with app.app_context():
    db.create_all()

@app.context_processor
def inject_active_path():
    def is_active(path):
        return 'active' if path in request.path else ''
    return (dict(is_active=is_active))

@app.route('/')
def home():
    try:
        return redirect(url_for('consulta_bp.create'))
    except Exception:
        return redirect('/consultas/create')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(
        host='0.0.0.0',
        port=int(os.environ.get('PORT', 5000)),
        debug=True
    )


