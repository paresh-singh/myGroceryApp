from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Section(db.Model): 
    s_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False )
    prod = db.relationship('Product' , backref="sec" ) # Product is capital as it references the class
    
class Product(db.Model):
    p_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False )
    key = db.Column(db.Integer, db.ForeignKey("section.s_id")) # section is small as thats how it is supposed to be
    md = db.Column(db.String, nullable = False ) #manufacturing date
    ed = db.Column(db.String, nullable = False ) #expiry date
    units = db.Column(db.String, nullable = False ) # units
    rate = db.Column(db.Integer, nullable = False ) # value without units
    quantity = db.Column(db.Integer, default=1)
        
class Users(db.Model):
    u_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False )
    email = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False ) 
      
class Admin(db.Model):
    a_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String, nullable = False )
    email = db.Column(db.String, nullable = False)
    password = db.Column(db.String, nullable = False ) 
    
class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    prod_id = db.Column(db.Integer, db.ForeignKey('product.p_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.u_id'), nullable=False)
    quantity = db.Column(db.Integer, default=1)
    product = db.relationship('Product', backref='cart')
    user = db.relationship('Users', backref='cart')
    
    