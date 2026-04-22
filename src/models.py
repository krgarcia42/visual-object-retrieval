class ImageRecord:
    #The blueprint for our Document DB entries
    #Ensures every image has a consistent structure
    def __init__(self, image_id, url, labels, embedding):
        self.data = {
            "id": image_id,           #unique ID from schema
            "storage_url": url,       #where the file is kept
            "tags": labels,           #searchable words from labeler
            "embedding": embedding,    #math vector for AI search
            "metadata": {
                "version": "1.0",
                "processed": True
            }
        }

    def to_dict(self):
        #Returns the record as a dictionary for easy saving
        return self.data
