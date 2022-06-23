from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(80), unique=False, nullable=False)
    is_active = db.Column(db.Boolean(), unique=False, nullable=False)

# transforma la clase en un string, similar a template string de JS
    def __repr__(self):
        return '<User %r>' % self.username

# mapeo, transforma el objeto en un diccionario donde tenga key.id con su id, ya no devuelve el objeto (la instancia de una clase) sino que devuelve un diccionario
    def serialize(self):
        return {
            "id": self.id,
            "email": self.email,
            # do not serialize the password, its a security breach
        }

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(120), unique=True, nullable=False)
    done = db.Column(db.Boolean(), unique=False, nullable=False)
    # user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    # user = db.relationship(User)

# transforma la clase en un string, similar a template string de JS
    def __repr__(self):
        return '<Task %r>' % self.text

# mapeo, transforma el objeto en un diccionario donde tenga key.id con su id, ya no devuelve el objeto (la instancia de una clase) sino que devuelve un diccionario
    def serialize(self):
        return {
            "id": self.id,
            "text": self.text,
            "done": self.done,
            # do not serialize the password, its a security breach
        }