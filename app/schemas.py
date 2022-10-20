
from marshmallow import Schema,fields
from marshmallow.validate import Length

class TaskSchema(Schema):
    class Meta:
        #Indica los campos que se van a serializar
        fields = ('id', 'title', 'description', 'deadline')

class ParamTaskSchema(Schema):
    title = fields.Str(required=True, validate=Length(max=50))
    description = fields.Str(required=True, validate=Length(max=200))
    deadline = fields.DateTime(required=True)

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)
param_task = ParamTaskSchema()