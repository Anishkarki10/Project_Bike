"""Seed a few sample bikes from the original Figma/React prototype.
Run: python seed_data.py
"""
from app.models.database import Database
from app.models.bike import Bike

Database.ensure_database()
Database.create_tables()
model = Bike()

if model.get_all():
    print('Bikes already exist. Seed skipped.')
    raise SystemExit

samples = [
    {
        'name':'Yamaha MT-15 V2','brand':'Yamaha','model':'MT-15 V2','category':'motorcycle','year':2023,
        'engine_cc':155,'km_travelled':12500,'price':425000,'original_price':None,'fuel_type':'Petrol',
        'transmission':'Manual 6-speed','colour':'Ice Fluo / Cyan Storm','condition_text':'Excellent','owners':1,
        'reg_number':'BA 1 PA 2345','short_description':'Low-km 2023 Yamaha MT-15 V2 in excellent condition. Full service history available.',
        'full_description':'A premium street bike in excellent condition. Maintained regularly with no major accident history.',
        'features':'LED Headlight, Slipper Clutch, USD Forks, ABS','known_issues':'','service_info':'Last serviced at 12,000 km.',
        'doc_info':'Original blue book available.','status':'available',
        'cover_image':'https://images.unsplash.com/photo-1568772068505-d006fb2d47d7?w=1000&h=700&fit=crop&auto=format'
    },
    {
        'name':'Honda CB Hornet 160R','brand':'Honda','model':'CB Hornet 160R','category':'motorcycle','year':2022,
        'engine_cc':160,'km_travelled':18200,'price':280000,'original_price':320000,'fuel_type':'Petrol',
        'transmission':'Manual 5-speed','colour':'Sports Red','condition_text':'Good','owners':1,
        'reg_number':'BA 2 KHA 4501','short_description':'Well-maintained Honda CB Hornet 160R in Sports Red.',
        'full_description':'A dependable everyday commuter with clean mechanical condition and minor cosmetic wear.',
        'features':'Digital Instrument Cluster, Monoshock Rear Suspension, Disc Brakes','known_issues':'Minor surface scratches.',
        'service_info':'Regular servicing done every 3,000 km.','doc_info':'Blue book available.','status':'available',
        'cover_image':'https://images.unsplash.com/photo-1601556402552-23ce8f2b31fc?w=1000&h=700&fit=crop&auto=format'
    },
    {
        'name':'Bajaj Pulsar NS200','brand':'Bajaj','model':'Pulsar NS200','category':'motorcycle','year':2021,
        'engine_cc':200,'km_travelled':24800,'price':310000,'original_price':None,'fuel_type':'Petrol',
        'transmission':'Manual 6-speed','colour':'Granite Black','condition_text':'Good','owners':1,'reg_number':'',
        'short_description':'Powerful 200cc street bike with sporty performance and affordable pricing.',
        'full_description':'Popular performance commuter with a strong engine and practical ownership costs.',
        'features':'Liquid-Cooled Engine, Perimeter Frame, Dual Disc Brakes, Digital Console','known_issues':'Small cosmetic dent on fuel tank.',
        'service_info':'Serviced regularly.','doc_info':'','status':'available',
        'cover_image':'https://images.unsplash.com/photo-1676246751280-16f3d4d0db7a?w=1000&h=700&fit=crop&auto=format'
    },
    {
        'name':'Honda Activa 6G','brand':'Honda','model':'Activa 6G','category':'scooter','year':2023,
        'engine_cc':110,'km_travelled':8900,'price':185000,'original_price':None,'fuel_type':'Petrol',
        'transmission':'CVT Automatic','colour':'Matte Red','condition_text':'Excellent','owners':1,'reg_number':'',
        'short_description':'Low-km city scooter in near-new condition.','full_description':'Fuel-efficient and easy to ride for daily Kathmandu commuting.',
        'features':'Silent Start, LED Headlamp, External Fuel Fill, Combi Brake System','known_issues':'','service_info':'Serviced at authorised centre.',
        'doc_info':'Blue book available.','status':'available',
        'cover_image':'https://images.unsplash.com/photo-1766758196181-49cf3f1ebd69?w=1000&h=700&fit=crop&auto=format'
    },
]

for item in samples:
    model.save(item)
print(f'Seeded {len(samples)} sample bikes.')
