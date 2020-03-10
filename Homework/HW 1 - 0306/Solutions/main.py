import os

# Define the name of the directory to be created
path = 'data/'

# Number of desired files
samples = 100

# Making the directory safely
try:
    if not os.path.exists(path):
        os.makedirs(path)
        print ("Successfully created the directory %s " % path)
    else:
        print("Path already exists")
except OSError:
    print ("Creation of the directory %s failed" % path)
    
# Makes the txt files and writes in them
for X in range(samples):
    with open(path+'00'+str(X)+'.txt', "w") as f:   # Opens file and casts as f 
        f.write(str(X))                             # Writing file number inside file

# Makes a files.txt and writes the paths of all the new files in it
for file in os.listdir(path):                       # Loops all files inside desired path
    if file.endswith(".txt"):                       # Finds only the ones that are .txt
        with open('files.txt', "a+") as f:          
            f.write(os.path.join(path, file+'\n'))
