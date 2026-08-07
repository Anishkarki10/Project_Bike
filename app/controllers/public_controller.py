from flask import render_template, request, redirect, url_for, flash
from app.models.bike import Bike
from app.models.inquiry import Inquiry
from app.models.settings import Settings


class PublicController:
    def __init__(self):
        self.bike_model = Bike()
        self.inquiry_model = Inquiry()
        self.settings_model = Settings()

    def _common(self):
        return {'settings': self.settings_model.get()}

    def home(self):
        data = self._common()
        data['bikes'] = self.bike_model.get_available_featured(6)
        return render_template('public/home.html', **data)

    def bikes(self):
        filters = {
            'search': request.args.get('search', '').strip() or None,
            'brand': request.args.get('brand', '').strip() or None,
            'category': request.args.get('category', '').strip() or None,
            'status': request.args.get('status', '').strip() or 'available',
            'min_price': request.args.get('min_price', '').strip() or None,
            'max_price': request.args.get('max_price', '').strip() or None,
        }
        rows = self.bike_model.get_all(**filters)
        for b in rows:
            b['images'] = self.bike_model.get_images(b['id'])
        data = self._common()
        data.update({'bikes': rows, 'brands': self.bike_model.get_brands(), 'filters': filters})
        return render_template('public/bikes.html', **data)

    def bike_detail(self, bike_id):
        bike = self.bike_model.find_by_id(bike_id)
        if not bike:
            return render_template('notfound.html'), 404
        bike['images'] = self.bike_model.get_images(bike_id)
        if bike.get('cover_image') and bike['cover_image'] not in bike['images']:
            bike['images'].insert(0, bike['cover_image'])
        if not bike['images']:
            bike['images'] = [bike.get('cover_image')] if bike.get('cover_image') else []
        bike['feature_list'] = [x.strip() for x in (bike.get('features') or '').split(',') if x.strip()]
        data = self._common(); data['bike'] = bike
        return render_template('public/bike_detail.html', **data)

    def about(self):
        return render_template('public/about.html', **self._common())

    def contact(self):
        data = self._common(); data['bikes'] = self.bike_model.get_all(status='available')
        return render_template('public/contact.html', **data)

    def submit_inquiry(self):
        name = request.form.get('name', '').strip()
        phone = request.form.get('phone', '').strip()
        message = request.form.get('message', '').strip()
        if not name or not phone or not message:
            flash('Name, phone and message are required.', 'danger')
            return redirect(request.referrer or url_for('public.contact'))

        bike_id = request.form.get('bike_id') or None
        bike_name = request.form.get('bike_interested', '').strip()
        self.inquiry_model.create({
            'name': name,
            'phone': phone,
            'email': request.form.get('email', '').strip() or None,
            'bike_id': int(bike_id) if bike_id else None,
            'bike_interested': bike_name or None,
            'message': message,
        })
        flash('Thanks! Your inquiry has been sent to Supa Auto Link.', 'success')
        if bike_id:
            return redirect(url_for('public.bike_detail', bike_id=bike_id))
        return redirect(url_for('public.contact'))
