from flask import Flask, render_template, request, redirect, url_for, session, jsonify
import os


app = Flask(__name__)
app.secret_key = os.environ.get('FLASK_SECRET_KEY', 'supersecretkey')
app.config['UPLOAD_FOLDER'] = 'static/css/images/'

@app.route('/upload_image', methods=['POST'])
def upload_image():
    image_type = request.form['image_type']
    
    if 'image' not in request.files:
        return redirect(request.url)
    
    file = request.files['image']
    
    if file.filename == '':
        return redirect(request.url)
    
    if file and file.filename.endswith(('png', 'jpg', 'jpeg', 'gif')):
        # Tentukan nama file berdasarkan jenis gambar yang diupload
        filename = f"{image_type}.png"
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)
        return redirect(url_for('admin_dashboard'))  # Redirect ke halaman admin dashboard
    
    return redirect(request.url)


# Dummy admin credentials
admin_username = "admin"
admin_password = "1234"

# Data placeholder for programs
programs = {
    "rekayasa-perangkat-lunak": [
        "Dasar Pemrograman",
        "Pemrograman Berorientasi Objek",
        "Pengembangan Aplikasi Web",
        "Sistem Basis Data",
        "Pemrograman Mobile"
    ],
    "teknik-komputer-dan-jaringan": [
        "Dasar Jaringan Komputer",
        "Administrasi Server",
        "Keamanan Jaringan",
        "Jaringan Nirkabel",
        "Manajemen Infrastruktur Jaringan"
    ],
    "multimedia": [
        "Desain Grafis",
        "Animasi 2D dan 3D",
        "Produksi Video",
        "Editing Audio",
        "Penyiaran Multimedia"
    ],
    "teknik-transmisi-telekomunikasi": [
        "Dasar Sistem Telekomunikasi",
        "Elektronika dan Microcontroller",
        "Transmisi Satelit [VSAT.IP]",
        "Transmisi Radio [BTS]",
        "Transmisi Fiber Optic [FTTH]"
    ]
}

# Data placeholder for events and other information
events = [
   
]

@app.route('/delete_event/<int:event_index>', methods=['POST'])
def delete_event(event_index):
    if not session.get('admin'):
        return redirect(url_for('admin_login'))

    # Check if the index is within the range of events
    if 0 <= event_index < len(events):
        events.pop(event_index)
    
    return redirect(url_for('admin_dashboard'))


# Route for homepage
@app.route('/')
def home():
    return render_template('index.html', events=events)

# Route for admin login
@app.route('/admin', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == admin_username and password == admin_password:
            session['admin'] = True
            return redirect(url_for('admin_dashboard'))
        else:
            return "Gagal Login", 403
    return render_template('admin_login.html')

# Route for admin dashboard
@app.route('/admin/dashboard', methods=['GET', 'POST'])
def admin_dashboard():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    
    if request.method == 'POST':
        # Handle new event addition
        new_event = {
            "title": request.form['event_title'],
            "date": request.form['event_date'],
            "description": request.form['event_description']
        }
        events.append(new_event)
    
    return render_template('admin_dashboard.html', programs=programs, events=events)

# Route to update program data
@app.route('/update_program', methods=['POST'])
def update_program():
    if not session.get('admin'):
        return redirect(url_for('admin_login'))
    program = request.form['program']
    details = request.form['details'].split('\n')
    programs[program] = details
    return redirect(url_for('admin_dashboard'))

# Route to get package information for a specific program
@app.route('/get_package/<program_id>')
def get_package(program_id):
    package_info = programs.get(program_id, [])
    return jsonify(package_info)

# Route to logout
@app.route('/logout')
def logout():
    session.pop('admin', None)
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
