# from dotenv import load_dotenv
# load_dotenv()  # akan otomatis memuat .env di root, atau .env.production jika kamu atur namanya


from flask import Flask, redirect, url_for
from config import Config

from auth import auth_bp
from admin_routes import admin_bp
from recommendation import rec_bp

# print(Config.DATABASE_PATH, Config.SECRET_KEY)
app = Flask(__name__)
app.template_folder = 'templates'
app.config.from_object(Config)

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(rec_bp)



# Redirect root to login
@app.route('/')
def root():
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    app.run(debug=False)
    from waitress import serve
    serve(app, host='0.0.0.0', port=8000)