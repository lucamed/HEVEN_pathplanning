import os
from PIL import Image
import random

bsdir = os.path.dirname(os.path.abspath(__file__))+'\data'
os.mkdir(bsdir)

sign=Image.open("sign.jpg")
c_sign=sign.crop((10,65,130,195))
s_size=c_sign.size
s_a=s_size[0]
s_b=s_size[-1]

road=Image.open("road.jpg")

r_size=road.size
r_a=r_size[0]
r_b=r_size[-1]

r_range_a=r_a-s_a
r_range_b=r_b-s_b

for i in range(0,100) :
    
    c_road=road.copy()
    p_a=random.randrange(0,r_range_a)
    p_b=random.randrange(0,r_range_b)
    c_road.paste(c_sign,(p_a,p_b))

    os.chdir(bsdir)
    c_road.save('road_00{}.jpg'.format(i))

