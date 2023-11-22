from flask import Flask, render_template, request, redirect, flash, url_for 
from modules_1 import * 


#*********************************Notes***********************************

# SQLAlchemy is ORM (Object Relation Mapper)-> can do the same funciton of sql using python

#**********************************CONFIGURATION***************************

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///grocery.sqlite3"
app.secret_key = 'Myfirstapp' # Used for flash messages
db.init_app(app)
app.app_context().push()
    
#**********************************Admin*****************************
@app.route('/adminSections/<int:id>' , methods=['GET','POST'])
def adminSections(id):  
    sections = Section.query.all() 
    products = Product.query.all()
    admin = Admin.query.get(id)
    if request.method == 'POST':
        quantity = request.form.get('quantity')
        quantity = int(quantity)
        p_id = request.form.get('p_id')
        prod = Product.query.get(p_id = p_id)
        prod.quantity += quantity
        db.session.commit()
    return render_template('section.html', sections = sections , products = products , admin=admin)

@app.route('/sections', methods=['GET','POST'])  
def section():  
    sections = Section.query.all() 
    products = Product.query.all()
    if request.method == 'POST':
        quantity = request.form.get('quantity')
        quantity = int(quantity)
        product_id = request.form.get('p_id')
        prod = Product.query.get(f'{product_id}')
        prod.quantity += quantity
        db.session.commit()
    return render_template('section.html', sections = sections , products = products , admin=None)

@app.route('/addSection' , methods=['GET' , 'POST'])
def add_section():  
    if request.method == 'POST':
        name_here = request.form.get('name_there')
        if Section.query.filter_by(name = name_here).first() :
            flash("Section already present", category='error')
            return render_template('addsec.html')
            
        s1 = Section(name = name_here )
        db.session.add(s1)
        db.session.commit()
        return redirect('/sections')
    return render_template('addsec.html')
     
@app.route('/showSection/<int:id>' , methods=['GET' , 'POST'])
def show_sec(id):
    s1 = Section.query.get(id)
    p1 = s1.prod
    return render_template('secprod.html' , s1 = s1, p1 = p1)   
   
@app.route('/update_section/<int:id>' ,  methods=['GET' , 'POST'])
def update_sec(id):
    s1 = Section.query.get(id)
    if request.method == 'POST':  
        name = request.form.get('s_name')
        if Section.query.filter_by(name = name).first() :
            flash("Section name already present", category='error')
            return render_template('update_sec.html',s1=s1)
        s1.name = name 
        db.session.commit()
        return redirect('/sections') 
    return render_template('update_sec.html',s1=s1)
   
@app.route('/delete_section/<int:id>' ,  methods=['GET'])
def delete_sec(id):
    s1 = Section.query.get(id)
    if s1.prod : 
        flash('Section isn\'t empty, Clear the products first', category='error')
        return redirect('/sections')
    db.session.delete(s1)
    db.session.commit()
    return  redirect('/sections')   
 
@app.route('/searchAdmin', methods=['POST'])
def search_admin():
    sections = Section.query.all()
    searched = request.form.get('search').strip().lower()
    products = Product.query.filter(
        (Product.name.ilike(f'%{searched}%')) |  
        (Product.sec.has(Section.name.ilike(f'%{searched}%'))) |  
        (Product.ed.ilike(f'%{searched}%')) | 
        (Product.rate.ilike(f'%{searched}%'))  
    ).all()
    return render_template('admin_search.html' ,sections = sections , products = products, searched=searched)
   
@app.route('/products' , methods=['GET'])
def product():  
    p1 = Product.query.all() 
    return render_template('getprod.html', p1 = p1)

@app.route('/addProduct' , methods=['GET' , 'POST'])
def add_product():  
    sections = Section.query.all()
    if request.method == 'POST':
        name_here = request.form.get('name_there')
        md = request.form.get('man_date')
        ed = request.form.get('exp_date')
        rate = request.form.get('rate')
        units = request.form.get('units')
        key = request.form.get('sname')
        quantity = request.form.get('quantity')
        p1 = Product(name = name_here, md = md, ed = ed, rate = rate, quantity = quantity, units = units, key = key)
        db.session.add(p1)
        db.session.commit()
        return redirect('/sections')
    return render_template('addprod.html', s = sections)
    
@app.route('/update_product/<int:id>' ,  methods=['GET' , 'POST'])
def update_prod(id):
    p1 = Product.query.get(id)
    section = Section.query.all()
    if request.method == 'POST':  
        name = request.form.get('p_name')
        md = request.form.get('man_date')
        ed = request.form.get('exp_date')
        rate = request.form.get('rate')
        units = request.form.get('units')
        quantity = request.form.get('quantity')
        if md :
            p1.md = md
        if ed : 
            p1.ed = ed
        p1.name = name 
        p1.rate = rate 
        p1.units = units 
        p1.quantity = quantity 
        db.session.commit()
        return redirect('/sections')  
    return render_template('update_prod.html', p1=p1, section=section)
    
@app.route('/delete_product/<int:id>' ,  methods=['GET'])
def delete_prod(id):
    p1 = Product.query.get(id)
    db.session.delete(p1)
    db.session.commit()
    return redirect('/sections')        


#********************************Users*********************************
@app.route('/home/<int:id>' , methods=['GET' , 'POST'])
def home(id):
    sections = Section.query.all()
    products = Product.query.all()
    user = Users.query.get(id)
    cart = Cart.query.filter_by(user_id=user.u_id).first()
    if request.method == 'POST':
        quantity = request.form.get('quantity')
        quantity = int(quantity)
        p_id = request.form.get('p_id') 
        if cart :
            cart_item = Cart.query.filter_by(user_id=user.u_id, prod_id=p_id).first()
            if cart_item:
                cart_item.quantity += quantity
            else:
                cart_item = Cart(prod_id=p_id, quantity=quantity, user_id=user.u_id)
                db.session.add(cart_item)
        else:
            cart_item = Cart(prod_id=p_id, quantity=quantity, user_id=user.u_id)
            db.session.add(cart_item)
        db.session.commit()
        
    return render_template('home.html', sections = sections , products = products, user=user)

@app.route('/search/<int:id>', methods=['POST'])
def search(id):
    sections = Section.query.all()
    user = Users.query.get(id)
    searched = request.form.get('search').strip().lower()
    products = Product.query.filter(
        (Product.name.ilike(f'%{searched}%')) |  
        (Product.sec.has(Section.name.ilike(f'%{searched}%'))) |  
        (Product.ed.ilike(f'%{searched}%')) | 
        (Product.rate.ilike(f'%{searched}%'))  
    ).all()
    return render_template('user_search.html' ,sections = sections , products = products, user=user, searched=searched)

@app.route('/prod/<int:id>/<int:sec_id>' , methods=['GET'])
def prod(id,sec_id):
    sections = Section.query.all()
    s1 = Section.query.get(sec_id)
    products = s1.prod
    user = Users.query.get(id)
    return render_template('user_products.html' ,sections = sections ,s1=s1, products = products, user=user)

@app.route('/allProducts/<int:id>' , methods=['GET'] )
def allProducts(id):
    sections = Section.query.all()
    products = Product.query.all()
    user = Users.query.get(id)
    return render_template('user_allProd.html' ,sections = sections , products = products, user=user)

@app.route('/cart/<int:id>', methods=['GET' , 'POST'])
def cart(id):
    sections = Section.query.all()
    products = Product.query.all()
    user = Users.query.get(id)
    cart = Cart.query.filter_by(user_id=user.u_id).first()
    total = sum(item.product.rate * item.quantity for item in user.cart)

    if request.method == 'POST':
        pass 
    return render_template('cart.html',sections = sections , product = products, user=user, cart=cart,total=total)

@app.route('/update_cart/<int:id>/<int:prod_id>', methods=['POST'])
def update_cart(id, prod_id):
    new_quantity = int(request.form.get('quantity'))
    cart_item = Cart.query.filter_by(user_id=id, prod_id=prod_id).first()
    if cart_item:
        cart_item.quantity = new_quantity
        db.session.commit()
    return redirect(url_for('cart', id=id))

@app.route('/remove_from_cart/<int:id>/<int:prod_id>', methods=['GET'])
def remove_from_cart(id, prod_id):
    cart_item = Cart.query.filter_by(user_id=id, prod_id=prod_id).first()
    if cart_item:
        db.session.delete(cart_item)
        db.session.commit()
    return redirect(url_for('cart', id=id))

@app.route('/checkout/<int:id>', methods=['GET'])
def checkout(id):
    user = Users.query.get(id)
    cart_items = Cart.query.filter_by(user_id=id).all()
    for cart_item in cart_items:
        product = Product.query.get(cart_item.prod_id)
        if product.quantity >= cart_item.quantity:
            product.quantity -= cart_item.quantity
            cart_item.quantity = 0
        else:
            flash(f'Insufficient quantity of {product.name} available in stock.', category='error')
            return redirect(url_for('cart', id=user.u_id))
    
    flash(f'Order placed', category='success') 
    Cart.query.filter_by(user_id=id).delete() 
    db.session.commit()
    return redirect(url_for('cart', id=user.u_id))


#********************************Login*********************************


@app.route('/' , methods = ['GET', 'POST'])
def login():   
    if request.method=='POST':
        email = request.form.get('email')
        password = request.form.get('password') 
        user = Users.query.filter_by(email=email).first()
        if user : 
            if user.password == password : 
                return redirect(url_for('home', id=user.u_id))
            else :  
                flash('Incorrect password' , category='error')    
        else : 
            flash('User doesn\'t exist' , category='error')
            
    return render_template('login.html')

@app.route('/admin' , methods = ['GET', 'POST'])
def admin():   
    if request.method=='POST':
        email = request.form.get('email')
        password = request.form.get('password')
        admin = Admin.query.filter_by(email=email).first()
        if admin : 
            if admin.password == password : 
                flash('Logged in successfully')
                return redirect(url_for('adminSections', id=admin.a_id))
            else :  
                flash('Incorrect password' , category='error')    
        else : 
            flash('Admin doesn\'t exist' , category='error')

    return render_template('admin.html')

@app.route('/sign' , methods = ['GET', 'POST'])
def sign():  
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('Name')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = Users.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        else:
            new_user = Users(email=email,name=name,password=password1)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created')
            return redirect('/')

    
    return render_template('sign_up.html')

if __name__ == "__main__":
    app.run(debug=True)

