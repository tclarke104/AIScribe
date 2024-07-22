from app.extensions import db

class Recording(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    transcription = db.Column(db.Text)
    fileId = db.Column(db.Text)
    note = db.Column(db.Text)

    def __repr__(self):
        return f'<Recording "{self.text}">'