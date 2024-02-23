import os
from include.texttoimage import gen_image_from_prompt
from include.basemodel import BaseModel
MAX_IMAGES = 3

output_dir = "generated_images"
current_dir = os.path.dirname(os.path.abspath(__file__))

image_cnt = 0
image_model = BaseModel()
namelist_file = os.path.join(current_dir, 'flashcard.txt')

with open(namelist_file) as f:
    for line in f:
        line = line.strip()
        
        if not line:
            continue            
        if line.startswith('#'):
            category = line[1:].strip().lower().replace(" ", "_")
            continue
        else:
            object = line         

        # Create required directories 
        category = "general" if category == "" else category 
        category = category.lower().replace(" ", "_")
        image_dir = os.path.join(output_dir, category)
        if not os.path.exists(image_dir):
            os.makedirs(image_dir)
        reject_dir = os.path.join(image_dir, "reject")
        if not os.path.exists(reject_dir):
            os.makedirs(reject_dir)

        # Generate image only if it doesn't already exist
        filename = object.lower().replace(" ","_") + ".png"
        filepath = os.path.join(image_dir, filename)
        if not os.path.exists(filepath):
            print(category + ": " + object) 
            prompt = object + " logo in original colors on a light background, flat image" 
            image = gen_image_from_prompt(image_model, category, object, prompt)
            f = open(filepath, 'wb')
            f.write(image)

        image_cnt += 1
        if image_cnt >= MAX_IMAGES:
            break

                
