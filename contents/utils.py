import uuid

def images_directory_path(instance, filename):
    if (instance.__class__.__name__).lower() == 'image':
        return '/'.join([str(instance.item.__class__.__name__).lower(), 
                        str(instance.__class__.__name__).lower(), 
                        str(instance.item.name),
                        str(uuid.uuid4().hex + ".png")
                    ])
    else:    
        ext = filename.split(".")[-1]
        return '/'.join([str(instance.item.__class__.__name__).lower(), 
                        str(instance.__class__.__name__).lower(), 
                        str(instance.item.name), 
                        str(uuid.uuid4().hex + "." + ext)
                    ])