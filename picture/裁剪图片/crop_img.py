import os


os.chdir(r'C:\bat\ÏÂÔØ\ÍøÒ³ppt')

def crop_img(path, box):
    import PIL
    f = PIL.Image.open(path)
    xsize,ysize = f.size
    f.crop(box).save(path.split('.')[0]+'_new.'+path.split('.')[-1])
           
    return(0)
    
for path in [str(i)+'.png' for i in range(1,63,1)]:
    crop_img(path = path, box = (346,0,1223,686))