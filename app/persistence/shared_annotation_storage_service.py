from app.models.shared_annotation import SharedAnnotation


class SharedAnnotationStorageService():
    def __init__(self):
        pass

    @staticmethod
    def save(data):
        annotation = SharedAnnotation(
            user_id=data["current_user_id"],
            annotation_id=data["annotation_id"],
            token=data["token"],
            share_type=data.get("share_type"),
            recipient_user_id=data.get("recipient_user_id"),
            role=data.get("role")
        )
        id = annotation.save()
        return id

    @staticmethod
    def get(data):
        data = SharedAnnotation.find(data, one=True)
        return data

    @staticmethod
    def get_by_id(id):
        data = SharedAnnotation.find_by_id(id)
        return data

    @staticmethod
    def update(id, data):
        data = SharedAnnotation.update({"_id": id}, {"$set": data}, many=False)
        return data

    @staticmethod
    def delete(id):
        data = SharedAnnotation.delete({"_id": id})
        return data
