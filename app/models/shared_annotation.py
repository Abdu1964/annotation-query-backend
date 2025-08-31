from pymongoose.mongo_types import Types, Schema
import datetime

class SharedAnnotation(Schema):
    schema_name = 'shared_annotation'

    # Attributes
    id = None
    user_id = None
    annotation_id = None
    token = None
    created_at = None
    updated_at = None
    recipient_user_id = None
    share_type = None

    def __init__(self, **kwargs):
        self.schema = {
            "user_id": {
                "type": Types.String,
                "required": True,
            },
            "annotation_id": {
                "type": Types.String,
                "required": True,
            },
            "token": {
                "type": Types.String,
                "required": True,
            },
            "share_type": {"type": Types.String, "required": True, "default": "public"},
            "recipient_user_id": {"type": Types.String, "required": False},
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
        return f"""user_id: {self.user_id}, annotation_id: {self.annotation_id}, token: {self.token},
            recipient_user_id: {self.recipient_user_id}, share_type: {self.share_type}
        created_at: {self.created_at}, updated_at: {self.updated_at}
        """
