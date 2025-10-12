from pymongoose.mongo_types import Types, Schema
import datetime

class User(Schema):
    schema_name = 'user'

    # Attributes
    id = None
    user_id = None
    data_source = None
    created_at = None
    updated_at = None
    species = None

    def __init__(self, **kwargs):
        self.schema = {
            "user_id": {
                "type": Types.String,
                "required": True,
            },
            "species": {
                "type": Types.String,
                "required": True,
                "default": "human"
            },
            "data_source": any,
           "created_at": {
                "type": Types.Date,
                "required": True,
                "default": datetime.datetime.now()
            },
            "updated_at": {
                "type": Types.Date,
                "required": True,
                "default": datetime.datetime.now()
            }
        }

        super().__init__(self.schema_name, self.schema, kwargs)

    def __str__(self):
        return f"""user_id: {self.user_id}, data_source: {self.data_source}, species: {self.species}, 
        created_at: {self.created_at}, updated_at: {self.updated_at}
        """
