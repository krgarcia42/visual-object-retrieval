class ImageRecord:
    #The blueprint for our Document DB entries
    #Ensures every image has a consistent structure
    def __init__(self, image_id, url, labels, embedding):
        self.data = {
            "id": image_id,           # Unique ID from our schema
            "storage_url": url,       # Where the file is kept
            "tags": labels,           # Searchable words from the labeler
            "embedding": embedding,    # The math vector for AI search
            "metadata": {
                "version": "1.0",
                "processed": True
            }
        }

    def to_dict(self):
        """Returns the record as a dictionary for easy saving."""
        return self.data
