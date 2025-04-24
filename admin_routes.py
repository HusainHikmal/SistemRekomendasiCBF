from flask import Blueprint, render_template, request, redirect, url_for, flash
from data_handler import get_db_connection
from auth import admin_required

# Blueprint for admin routes with prefix /admin
admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/', methods=['GET'])
@admin_required
def admin_dashboard():
    """Display list of smartphones for admin"""
    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM smartphone")
        smartphones = cursor.fetchall()
    return render_template('admin/index.html', smartphones=smartphones)

@admin_bp.route('/create', methods=['GET', 'POST'])
@admin_required
def create_smartphone():
    """Show form and process new smartphone"""
    if request.method == 'POST':
        f = request.form
        spec = (
            f"{f['brand']} {f['chipset']} {f['ram']} RAM "
            f"{f['storage']} Storage {f['battery']} {f['main_camera']} "
            f"{f['size']}-inch {f['lcd']} {f['band_1']}"
        )
        with get_db_connection() as conn:
            conn.execute(
                '''INSERT INTO smartphone (
                    phone, brand, chipset, prices, ram, storage, performance, battery,
                    main_camera, system_operation, size, lcd, band_1, images,
                    release_month, release_year, specification
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                (
                    f['phone'], f['brand'], f['chipset'], f['prices'], f['ram'],
                    f['storage'], f['performance'], f['battery'], f['main_camera'],
                    f['system_operation'], f['size'], f['lcd'], f['band_1'], f['images'],
                    f['release_month'], f['release_year'], spec
                )
            )
            conn.commit()
        flash('Smartphone berhasil ditambahkan!', 'success')
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('admin/add_smartphone.html')

@admin_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
@admin_required
def edit_smartphone(id):
    """Show form pre-filled and update smartphone"""
    with get_db_connection() as conn:
        phone = conn.execute('SELECT * FROM smartphone WHERE id = ?', (id,)).fetchone()
    if request.method == 'POST':
        f = request.form
        spec = (
            f"{f['brand']} {f['chipset']} {f['ram']} RAM "
            f"{f['storage']} Storage {f['battery']} {f['main_camera']} "
            f"{f['size']}-inch {f['lcd']} {f['band_1']}"
        )
        with get_db_connection() as conn:
            conn.execute(
                '''UPDATE smartphone SET
                   phone=?, brand=?, chipset=?, prices=?, ram=?, storage=?,
                   performance=?, battery=?, main_camera=?, system_operation=?,
                   size=?, lcd=?, band_1=?, images=?, release_month=?, release_year=?,
                   specification=? WHERE id=?''',
                (
                    f['phone'], f['brand'], f['chipset'], f['prices'], f['ram'],
                    f['storage'], f['performance'], f['battery'], f['main_camera'],
                    f['system_operation'], f['size'], f['lcd'], f['band_1'], f['images'],
                    f['release_month'], f['release_year'], spec, id
                )
            )
            conn.commit()
        flash('Smartphone berhasil diperbarui!', 'success')
        return redirect(url_for('admin.admin_dashboard'))
    return render_template('admin/edit_smartphone.html', smartphone=phone)

@admin_bp.route('/delete/<int:id>', methods=['POST'])
@admin_required
def delete_smartphone(id):
    """Delete a smartphone"""
    with get_db_connection() as conn:
        conn.execute('DELETE FROM smartphone WHERE id = ?', (id,))
        conn.commit()
    flash('Smartphone berhasil dihapus!', 'success')
    return redirect(url_for('admin.admin_dashboard'))