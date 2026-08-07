import os
import time
from flask import render_template, request, redirect, url_for, flash, session, current_app
from werkzeug.utils import secure_filename
from app.models.user import User
from app.models.bike import Bike
from app.models.inquiry import Inquiry
from app.models.settings import Settings
import config


class AdminController:
    def __init__(self):
        self.user_model = User()
        self.bike_model = Bike()
        self.inquiry_model = Inquiry()
        self.settings_model = Settings()

    def login(self):
        if session.get('admin_id'):
            return redirect(url_for('admin.dashboard'))
        if request.method == 'POST':
            email = request.form.get('email', '').strip().lower()
            password = request.form.get('password', '')
            user = self.user_model.find_by_email(email)
            if not user or user.get('role') != 'admin' or not self.user_model.check_password(user['password'], password):
                flash('Invalid admin email or password.', 'danger')
                return render_template('admin/login.html')
            session.clear()
            session['admin_id'] = user['id']
            session['admin_name'] = user['name']
            session['role'] = user['role']
            return redirect(url_for('admin.dashboard'))
        return render_template('admin/login.html')

    def logout(self):
        session.clear()
        flash('Logged out successfully.', 'success')
        return redirect(url_for('admin.login'))

    def dashboard(self):
        return render_template('admin/dashboard.html',
            counts=self.bike_model.counts(),
            bikes=self.bike_model.get_all()[:5],
            inquiries=self.inquiry_model.get_all_with_bike()[:5],
            new_inquiries=self.inquiry_model.count_new())

    def bikes(self):
        return render_template('admin/bikes.html',
            bikes=self.bike_model.get_all(status=request.args.get('status') or None,
                                          brand=request.args.get('brand') or None,
                                          search=request.args.get('search') or None),
            brands=self.bike_model.get_brands(),
            new_inquiries=self.inquiry_model.count_new())

    def _allowed_image(self, filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in config.ALLOWED_IMAGE_EXTENSIONS

    def _save_file(self, file_obj):
        if not file_obj or not file_obj.filename or not self._allowed_image(file_obj.filename):
            return None
        name = secure_filename(file_obj.filename)
        name = f'{int(time.time()*1000)}_{name}'
        file_obj.save(os.path.join(current_app.config['BIKE_UPLOAD_FOLDER'], name))
        return name

    def _form_data(self, old_cover=None):
        def int_or(v, default=0):
            try: return int(v)
            except: return default
        def float_or_none(v):
            try: return float(v) if v not in (None, '') else None
            except: return None
        cover = self._save_file(request.files.get('cover_image')) or old_cover
        return {
            'name': request.form.get('name', '').strip(),
            'brand': request.form.get('brand', '').strip(),
            'model': request.form.get('model', '').strip(),
            'category': request.form.get('category', 'motorcycle'),
            'year': int_or(request.form.get('year')),
            'engine_cc': int_or(request.form.get('engine_cc')),
            'km_travelled': int_or(request.form.get('km_travelled')),
            'price': float_or_none(request.form.get('price')) or 0,
            'original_price': float_or_none(request.form.get('original_price')),
            'fuel_type': request.form.get('fuel_type', 'Petrol'),
            'transmission': request.form.get('transmission', '').strip(),
            'colour': request.form.get('colour', '').strip(),
            'condition_text': request.form.get('condition_text', '').strip(),
            'owners': int_or(request.form.get('owners'), 1),
            'reg_number': request.form.get('reg_number', '').strip(),
            'short_description': request.form.get('short_description', '').strip(),
            'full_description': request.form.get('full_description', '').strip(),
            'features': request.form.get('features', '').strip(),
            'known_issues': request.form.get('known_issues', '').strip(),
            'service_info': request.form.get('service_info', '').strip(),
            'doc_info': request.form.get('doc_info', '').strip(),
            'status': request.form.get('status', 'available'),
            'cover_image': cover,
        }

    def add_bike(self):
        if request.method == 'POST':
            data = self._form_data()
            if not data['name'] or not data['brand'] or not data['model'] or not data['price']:
                flash('Name, brand, model and price are required.', 'danger')
                return render_template('admin/bike_form.html', bike=data, mode='add', new_inquiries=self.inquiry_model.count_new())
            bike_id = self.bike_model.save(data)
            for idx, file_obj in enumerate(request.files.getlist('gallery_images')):
                filename = self._save_file(file_obj)
                if filename: self.bike_model.add_image(bike_id, filename, idx)
            flash('Bike added successfully.', 'success')
            return redirect(url_for('admin.bikes'))
        return render_template('admin/bike_form.html', bike=None, mode='add', new_inquiries=self.inquiry_model.count_new())

    def edit_bike(self, bike_id):
        bike = self.bike_model.find_by_id(bike_id)
        if not bike:
            flash('Bike not found.', 'danger')
            return redirect(url_for('admin.bikes'))
        if request.method == 'POST':
            data = self._form_data(bike.get('cover_image'))
            self.bike_model.update(bike_id, data)
            new_gallery = request.files.getlist('gallery_images')
            if any(f and f.filename for f in new_gallery):
                self.bike_model.clear_images(bike_id)
                for idx, file_obj in enumerate(new_gallery):
                    filename = self._save_file(file_obj)
                    if filename: self.bike_model.add_image(bike_id, filename, idx)
            flash('Bike updated successfully.', 'success')
            return redirect(url_for('admin.bikes'))
        bike['images'] = self.bike_model.get_images(bike_id)
        return render_template('admin/bike_form.html', bike=bike, mode='edit', new_inquiries=self.inquiry_model.count_new())

    def delete_bike(self, bike_id):
        self.bike_model.delete_by_id(bike_id)
        flash('Bike deleted successfully.', 'success')
        return redirect(url_for('admin.bikes'))

    def toggle_bike_status(self, bike_id):
        self.bike_model.toggle_status(bike_id)
        flash('Bike status updated.', 'success')
        return redirect(url_for('admin.bikes'))

    def inquiries(self):
        return render_template('admin/inquiries.html', inquiries=self.inquiry_model.get_all_with_bike(), new_inquiries=self.inquiry_model.count_new())

    def update_inquiry(self, inquiry_id):
        status = request.form.get('status', 'new')
        if status not in {'new','contacted','closed'}: status='new'
        self.inquiry_model.update_status(inquiry_id, status)
        flash('Inquiry status updated.', 'success')
        return redirect(url_for('admin.inquiries'))

    def settings(self):
        settings = self.settings_model.get()
        if request.method == 'POST':
            data = dict(settings)
            for key in ['business_name','phone','email','address','opening_hours','tiktok','facebook','instagram','about_content']:
                data[key] = request.form.get(key, '').strip()
            logo = request.files.get('logo')
            if logo and logo.filename and self._allowed_image(logo.filename):
                filename = self._save_file(logo)
                if filename: data['logo'] = 'uploads/bikes/' + filename
            self.settings_model.update(data)
            flash('Settings saved successfully.', 'success')
            return redirect(url_for('admin.settings'))
        return render_template('admin/settings.html', settings=settings, new_inquiries=self.inquiry_model.count_new())
