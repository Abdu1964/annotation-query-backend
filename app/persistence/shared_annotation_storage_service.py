from app.models.shared_annotation import SharedAnnotation


class SharedAnnotationStorageService():
    def __init__(self):
        pass

    @staticmethod
    def save(data):
        data = SharedAnnotation(
            user_id=data["current_user_id"],
            annotation_id=data["annotation_id"],
            token=data["token"]
        )

        id = data.save()
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

    @staticmethod
    def delete(id):
        data = SharedAnnotation.delete({"_id": id})
        return data
