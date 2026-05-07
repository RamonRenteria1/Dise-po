from flask import Flask, render_template, request, redirect, url_for, session, flash
from GestorTareas import GestorTareas
from datetime import datetime

app = Flask(__name__)
app.secret_key = 't123123dsfcvxz'
gestor = GestorTareas()

@app.route('/', methods=['GET', 'POST'])
def login():
    if 'usuario_id' in session:
        return redirect(url_for('tareas'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        usuario = gestor.obtener_usuario2(email, password)
        
        if usuario:
            session['usuario_id'] = str(usuario['_id'])
            session['nombre'] = usuario.get('username', 'Usuario')
            flash(f'Bienvenido {session["nombre"]}', 'success')
            return redirect(url_for('tareas'))
        else:
            flash('Correo o contraseña incorrectos.', 'danger')
            
    return render_template('login.html')

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form.get('nombre') 
        email = request.form.get('email')
        password = request.form.get('password')
        confirmar = request.form.get('confirmar_password')

        if not nombre or not email or not password:
            flash("Todos los campos son obligatorios", "danger")
            return redirect(url_for("registro"))
        
        if password != confirmar:
            flash("Las contraseñas no coinciden", "danger")
            return redirect(url_for("registro"))

        if gestor.usuarios.find_one({"email": email}):
            flash("El Correo Ya Esta Registrado", "danger")
            return redirect(url_for('registro'))
        
        try:
            nuevo_usuario = {
                "username": nombre,
                "email": email,
                "password": password,
                "fecha_registro": datetime.now()
            }
            gestor.usuarios.insert_one(nuevo_usuario)
            flash('Registro exitoso. Ya puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f"Error: {e}", "danger")
            return redirect(url_for('registro'))

    return render_template('registro.html')

@app.route('/tareas', methods=['GET', 'POST'])
def tareas():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
    
    u_id = session['usuario_id']

    if request.method == 'POST':

        titulo = request.form.get('titulo')
        descripcion = request.form.get('descripcion')
        fecha_texto = request.form.get('fecha_limite')
        
        fecha_objeto = None
        if fecha_texto:
            try:
                fecha_objeto = datetime.strptime(fecha_texto, '%Y-%m-%d')
            except ValueError:
                fecha_objeto = None

        gestor.crear_tarea(u_id, titulo, descripcion, fecha_objeto)
        
        flash('Tarea publicada correctamente')
        return redirect(url_for('tareas'))

    p = gestor.obtener_tareas_usuario(u_id, "pendiente")
    prog = gestor.obtener_tareas_usuario(u_id, "en_progreso")
    e = gestor.obtener_tareas_usuario(u_id, "completada")
    can = gestor.obtener_tareas_usuario(u_id, "cancelada")
    
    return render_template('tareas.html', pendientes=p, en_progreso=prog, entregadas=e, canceladas=can)

@app.route('/actualizar_estado/<tarea_id>/<nuevo_estado>')
def actualizar_estado(tarea_id, nuevo_estado):
    if 'usuario_id' in session:
        gestor.actualizar_estado_tarea(tarea_id, nuevo_estado)
        flash(f'Tarea movida a {nuevo_estado}')
    return redirect(url_for('tareas'))

@app.route('/eliminar/<tarea_id>')
def eliminar_tarea(tarea_id):
    if 'usuario_id' in session:
        gestor.eliminar_tarea(tarea_id)
        flash('Tarea eliminada correctamente.')
    return redirect(url_for('tareas'))

@app.route('/cancelar_tarea/<tarea_id>', methods=['POST'])
def cancelar_tarea(tarea_id):
    if 'usuario_id' in session:
        
        motivo = request.form.get('motivo_cancelacion')
        
        gestor.cancelar_tarea_con_motivo(tarea_id, motivo)
        flash('Tarea cancelada')
    return redirect(url_for('tareas'))

@app.route('/editar/<tarea_id>', methods=['GET', 'POST'])
def editar_tarea(tarea_id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        titulo = request.form['titulo']
        descripcion = request.form['descripcion']

        gestor.editar_tarea(tarea_id, titulo, descripcion)
        flash('Tarea actualizada correctamente.')
        return redirect(url_for('tareas'))

    tarea_actual = gestor.obtener_tarea(tarea_id)
    return render_template('editar.html', tarea=tarea_actual)

@app.route('/logout')
def logout():
    session.clear()
    flash("Sesión cerrada correctamente", "info")
    return redirect(url_for('login'))

@app.route('/recuperar')
def recuperar():
    return render_template('recuperar.html')

if __name__ == '__main__':
    app.run(debug=True)