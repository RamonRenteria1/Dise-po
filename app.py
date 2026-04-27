from flask import Flask, render_template, request, redirect, url_for, session, flash
from GestorTareas import GestorTareas


app = Flask(__name__)

app.secret_key = 't123123dsfcvxz'

gestor = GestorTareas()


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        gestor = GestorTareas()
        
        usuario = gestor.obtener_usuario2(email, password)
        
        if usuario:
            
            session['usuario_id'] = usuario['_id']
            session['nombre'] = usuario['username']
            flash(f'Bienvenido {usuario["username"]}', 'success')
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

        
        if not nombre or not email or not password:
            flash("Todos los campos son obligatorios", "error")
            return redirect(url_for("registro"))
        
        
        if password != confirmar:
            flash("Las contraseñas no coinciden", "error")
            return redirect(url_for("registro"))

        
        nuevo_usuario = {
            "username": nombre,
            "email": email,
            "password": password 
        }
        
        if  gestor.usuarios.find_one({"email": email}):
            flash("El Correo Ya Esta Registrado", "danger")
            return redirect(url_for('registro'))
        
        try:
            
            gestor.usuarios.insert_one(nuevo_usuario)
            flash('Registro exitoso. Ya puedes iniciar sesión.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            flash(f"Error al guardar en la base de datos: {e}", "error")
            return redirect(url_for('registro'))

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