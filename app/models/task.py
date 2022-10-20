from email.policy import default
from hashlib import new
from turtle import title

from sqlalchemy import delete, insert, true, asc, desc
from . import db

from sqlalchemy.event import listen

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=False)
    deadline = db.Column(db.DateTime(), nullable=False)
    created = db.Column(db.DateTime(), nullable=False, 
                        default=db.func.current_timestamp())

    @classmethod
    def new(cls, title, description, deadline):
        return Task(title=title, description=description, deadline=deadline)

    @classmethod
    def get_by_page(cls, page, per_page=10, sort='asc'):
        sort_by =  asc(Task.id) if sort=='asc' else desc(Task.id)
        p_object = Task.query.order_by(sort_by).paginate(page=page, per_page=per_page, error_out=True, max_per_page=None)        
        res = (p_object.items, p_object.page, p_object.prev_num, p_object.next_num, p_object.pages)
        print(res)
        return res

    def save(self):
        try:
            db.session.add(self)
            db.session.commit()
            return (True,"Task saved successfully")
        except Exception as ex:
            return (False,"An exception occurred while the task was saving.", ex)

    def delete(self):
        try:
            db.session.delete(self)
            db.session.commit()
            return (True,"Task saved successfully")
        except Exception as ex:
            return (False,"An exception occurred while the task was deleting.", ex)

    def __str__(self) -> str:
        return self.title

""" Deprecated by use of marshmallow
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'deadline': self.deadline,
            'created': self.created
        }
"""
def insert_tasks(*args, **kwargs):
    db.session.add(
        Task(title='Title 1', description='Description 1', deadline='2022-10-09 12:00:00')        
    )
    db.session.add(
        Task(title='Title 2', description='Description 2', deadline='2022-10-20 12:00:00')
    )
    db.session.commit()


listen(Task.__table__, 'after_create', insert_tasks)