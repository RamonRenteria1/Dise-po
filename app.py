from flask import Flask, render_template, request, redirect, url_for, session, flash
from GestorTareas import GestorTareas


app = Flask(__name__)

app.secret_key = 't123123dsfcvxz'

gestor = GestorTareas()
gestor.crear_usuario("Ramon", "reymon@gmail.com", "123456")


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        gestor = GestorTareas()
        
        usuario = gestor.obtener_usuario2(email, password)
        
        if usuario:
            
            session['usuario_id'] = usuario['_id']
            session['nombre'] = usuario['nombre']
            flash(f'Bienvenido {usuario["nombre"]}', 'success')
            return redirect(url_for('tareas'))
        else:
            
            flash('Correo o contraseña incorrectos.', 'danger')
            
    return render_template('login.html')
@app.route('/recuperar')
def recuperar():
    
    return render_template('recuperar.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        password = request.form.get('password')
        confirmar = request.form.get('confirmar_password')

        if password != confirmar:
            flash('Las contraseñas no coinciden.', 'danger')
            return render_template('registro.html')

        if email in usuarios_registrados:
            flash('Este correo ya está registrado.', 'danger')
            return render_template('registro.html')

        
        usuarios_registrados[email] = {
            "nombre": nombre,
            "password": password
        }
        
        flash('Registro exitoso. Ya puedes iniciar sesión.', 'success')
        return redirect(url_for('login'))

    return render_template('registro.html')

@app.route('/tareas')
def tareas():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    return render_template('tareas.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)