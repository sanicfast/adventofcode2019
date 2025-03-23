import numpy as np

def get_data(loc):
    with open(loc) as f:
        rawdata = f.read()
    image_enc= [int(i) for i in rawdata] # convert str to list
    if len(image_enc)>20: 
        rows,cols=6,25
    else:
        rows,cols=2,2
    layers = len(image_enc)/(rows*cols)
    # # Define the shape of the 3D array (e.g., 2 layers, 3 rows, 4 columns)
    shape = (layers,rows,cols)
    # # Ensure the list length matches the total size of the 3D array
    if len(image_enc) != np.prod(shape):
        raise ValueError("List size does not match the specified shape.")
    # # Fill the 3D array
    array_3d = np.array(image_enc).reshape([int(i) for i in shape])
    return array_3d
def p1(array_3d):
    min_zero_count=np.inf
    for i,layer in enumerate(array_3d):
        zero_count=(layer==0).sum()
        min_zero_count = min(zero_count,min_zero_count)
        if zero_count==min_zero_count:
            min_zero_layer=i

    print('p1:',(array_3d[min_zero_layer]==1).sum()*(array_3d[min_zero_layer]==2).sum())
    
# array_3d=get_data('./data/day8_ex2.txt')
array_3d=get_data('./data/day8.txt')
p1(array_3d)


# initialize our picture with all missing pixels
picture=np.zeros((array_3d.shape[1],array_3d.shape[2]))+2
for layer in array_3d:
    # print(picture)
    # print(layer)
    missing_mask = picture==2
    if missing_mask.sum()==0: #no need to look further if we've populated all our pixels
        print('finished early')
        break
    nonmissing_mask = layer!=2
    new_pixels_to_fill = missing_mask * nonmissing_mask
    picture[new_pixels_to_fill]=layer[new_pixels_to_fill]
    # print('need to fill\n',missing_mask)
    # print('can fill her\n',nonmissing_mask)
    # print('fill it up  \n',new_pixels_to_fill)
print('p2:')

for i in picture.tolist():
    print(''.join(['#' if j==1 else ' ' for j in i]))
###  #  # #### ###  ###  
#  # #  #    # #  # #  # 
#  # #  #   #  ###  #  # 
###  #  #  #   #  # ###  
# #  #  # #    #  # #    
#  #  ##  #### ###  #    