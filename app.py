from flask import Flask, render_template, request, redirect, url_for, session, flash
import GestorTareas 


app = Flask(__name__)
app.secret_key = '3432432'

usuarios_registrados = {}

@app.route('/', methods=['GET', 'POST'])
def login():
    gestor = GestorTareas()
    if gestor:
        if gestor.obtener_usuario2("Hola@gmail.com", "1234"):
            return render_template('login.html')
        else :
            pass
    else: 
        return render_template('ErrorConceccion.html')
    
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