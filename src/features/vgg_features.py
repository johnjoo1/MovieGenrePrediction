from src.utils.initialize import *

with open('data/interim/poster_movies.pckl','rb') as f:
    poster_movies=pickle.load(f)

from keras.applications.vgg16 import VGG16
from keras.preprocessing import image
from keras.applications.vgg16 import preprocess_input
import numpy as np
import pickle

model = VGG16(weights='imagenet', include_top=False)

# Extract the objects in the image as detected by VGG16
allnames=os.listdir(poster_folder)
imnames=[j for j in allnames if j.endswith('.jpg')]
feature_list=[]
genre_list=[]
file_order=[]
print ("Starting extracting VGG features for scraped images. This will take time, Please be patient...")
print ("Total images = ",len(imnames))
failed_files=[]
succesful_files=[]
i=0
for mov in poster_movies:
    i+=1
    mov_name=mov['original_title']
    mov_name1=mov_name.replace(':','/')
    poster_name=mov_name.replace(' ','_')+'.jpg'
    if poster_name in imnames:
        img_path=poster_folder+poster_name
        try:
            img = image.load_img(img_path, target_size=(224, 224))
            succesful_files.append(poster_name)
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            x = preprocess_input(x)
            features = model.predict(x)
            file_order.append(img_path)
            feature_list.append(features)
            genre_list.append(mov['genre_ids'])
            if np.max(np.asarray(feature_list))==0.0:
                print('problematic',i)
            if i%250==0 or i==1:
                print ("Working on Image : ",i)
        except:
            failed_files.append(poster_name)
            continue
        
    else:
        continue
print ("Done with all features, pickling for future use!")


list_pickled=(feature_list,file_order,failed_files,succesful_files,genre_list)
with open('data/processed/posters_new_features.pkl','wb') as f:
    pickle.dump(list_pickled,f)
print("Features dumped to pickle file")
