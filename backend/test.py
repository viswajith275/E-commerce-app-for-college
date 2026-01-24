import os

def delete_images(file_path: str):
    abs_path = os.path.dirname(os.path.abspath(__file__))
    print(file_path[22::])
    new_path = os.path.join(abs_path, file_path[22::])
    print(new_path, abs_path)

    if os.path.exists(new_path):

        try:
            os.remove(new_path)
            
        except:
            print('not exist')

delete_images('http://localhost:8000/static/images/f80d37de-ddbd-4cd1-9857-76fa0548fa77.jpeg')

#finally 22 aan slice 