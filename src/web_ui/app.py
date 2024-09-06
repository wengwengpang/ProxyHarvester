from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from src.database.db_manager import DBManager
from src.proxy_checker.checker import ProxyChecker
import os

def create_app():
    app = Flask(__name__)
    app.config.from_object('config')

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    db_manager = DBManager(app.config['DATABASE_PATH'])
    proxy_checker = ProxyChecker()

    @login_manager.user_loader
    def load_user(user_id):
        return db_manager.get_user_by_id(user_id)

    @app.route('/')
    @login_required
    def index():
        proxies = db_manager.get_all_valid_proxies()
        return render_template('dashboard.html', proxies=proxies)

    @app.route('/api/test_proxy', methods=['POST'])
    @login_required
    def test_proxy():
        proxy_id = request.json['proxy_id']
        proxy = db_manager.get_proxy_by_id(proxy_id)
        result = proxy_checker.run_check([proxy])[0]
        if result['is_valid']:
            db_manager.update_proxy(proxy_id, result)
            return jsonify({'success': True, 'latency': result['latency']})
        else:
            db_manager.delete_proxy(proxy_id)
            return jsonify({'success': False})

    @app.route('/export')
    @login_required
    def export_proxies():
        proxies = db_manager.get_all_valid_proxies()
        export_data = []
        for proxy in proxies:
            export_data.append({
                'ip': proxy['ip'],
                'port': proxy['port'],
                'type': [proxy['protocol']],
                'protocol': [proxy['protocol'].upper()],
                'country': proxy['country'],
                'area': '',
                'score': int(10 - min(proxy['latency'] * 10, 9)),
                'updateTime': proxy['last_checked'],
                'source': proxy['provider'],
                'check_count': 1,
                'fail_count': 0,
                'region': '',
                'anonymity': proxy['anonymity'],
                'speed': proxy['speed'],
            })
        return jsonify(export_data)

    from .auth import auth_bp
    app.register_blueprint(auth_bp)

    return app
