import pygame
import numpy as np


pygame.init()

clock=pygame.time.Clock()


#set up the window to draw
displayinfo=pygame.display.Info()
max_x=2*1024
max_y=2*768
if displayinfo.current_w*0.9<max_x:
    max_x=int(displayinfo.current_w*0.9)
if displayinfo.current_h*0.8<max_y:
    max_y=int(displayinfo.current_h*0.8)
resolution=(max_x,max_y)
screen=pygame.display.set_mode(resolution,pygame.DOUBLEBUF | pygame.HWSURFACE)

def gen_noise_1(width,height,spacing):
    noise_array=np.zeros((width,height))
    grad_array=np.random.rand(width//spacing+2,height//spacing+2,2)*2-1

    for x in range(width):
        for y in range(height):
            x0=(x//spacing)
            x1=x0+1
            y0=(y//spacing)
            y1=y0+1

            sx=(x%spacing)/spacing
            sy=(y%spacing)/spacing

            n0=np.dot(grad_array[x0,y0],np.array([sx,sy]))
            n1=np.dot(grad_array[x1,y0],np.array([sx-1,sy]))
            ix0=n0+(n1-n0)*sx

            n0=np.dot(grad_array[x0,y1],np.array([sx,sy-1]))
            n1=np.dot(grad_array[x1,y1],np.array([sx-1,sy-1]))
            ix1=n0+(n1-n0)*sx

            value=ix0+(ix1-ix0)*sy
            noise_array[x,y]=value
    def fade(t):
        return t*t*t*(t*(t*6-15)+10)

    noise_array=fade((noise_array-np.min(noise_array))/(np.max(noise_array)-np.min(noise_array)))
    return noise_array

def gen_noise_2(width,height,invscale):
    np.random.seed()
    #noise_array=np.random.rand(width,height)
    noise_array=np.random.normal(size=(width,height))
    fft_array=np.fft.fft2(noise_array)
    filter=np.zeros((width,height))
    for x in range(width):
        for y in range(height):
            dist=np.sqrt(x**2+y**2)
            filter[x,y]=np.exp(-dist*dist/(2*invscale*invscale))
    fft_array=fft_array*filter
    noise_array=np.fft.ifft2(fft_array).real
    #make it return 0-1
    return (noise_array-np.min(noise_array))/(np.max(noise_array)-np.min(noise_array))

    #return (255*(noise_array-np.min(noise_array))/(np.max(noise_array)-np.min(noise_array))).astype(np.uint8)

def gen_noise_3(width,height,scale):
    amp_array=np.random.normal(size=(scale,scale))
    phase_array=np.random.rand(scale,scale)*2*np.pi
    noise_array=np.zeros((width,height))
    for i in range(scale):
        for j in range(scale):
            for x in range(width):
                for y in range(height):
                    noise_array[x,y]+=amp_array[i,j]*np.cos(2*np.pi*(i*x/width + j*y/height)+phase_array[i,j])                    
    return (noise_array-np.min(noise_array))/(np.max(noise_array)-np.min(noise_array))    

def upscale(array,scale):
    width=array.shape[0]
    height=array.shape[1]
    new_array=np.zeros((width*scale,height*scale))
    for x in range(width*scale):
        for y in range(height*scale):
            new_array[x,y]=array[x//scale,y//scale]
    return new_array

#make a height array
height_array=gen_noise_3(640,480,8)
water_level=0.5

#build the image from the arrays
rgb_array=np.zeros((height_array.shape[0],height_array.shape[1],3))
for i in range(height_array.shape[0]):
    for j in range(height_array.shape[1]):
        if height_array[i,j]<water_level:
            rgb_array[i,j,0]=0
            rgb_array[i,j,1]=0
            rgb_array[i,j,2]=255*abs(water_level-height_array[i,j])+100
        else:
            if height_array[i,j]>0.9:
                rgb_array[i,j,0]=255
                rgb_array[i,j,1]=255
                rgb_array[i,j,2]=255
            elif height_array[i,j]>0.6:
                rgb_array[i,j,1]=255*(1/(1-water_level))*(height_array[i,j]-water_level)
                
            else:
                rgb_array[i,j,0]=139
                rgb_array[i,j,1]=69
                rgb_array[i,j,2]=19

            #rgb_array[i,j,2]=val
            #rgb_array[i,j,0]=(height_array[i,j]-water_level)*255//(255-water_level)
            #rgb_array[i,j,1]=(height_array[i,j]-water_level)*255//(255-water_level)
            #rgb_array[i,j,2]=(height_array[i,j]-water_level)*255//(255-water_level)

#print(noise_array)
#noise_surface=pygame.surfarray.make_surface((noise_array*255).astype(np.uint8).T)


#print(type((rgb_array*255).astype(np.uint8).T))
#print(rgb_array*255)
noise_surface=pygame.surfarray.make_surface((rgb_array).astype(np.uint8))
screen_surface=pygame.transform.scale(noise_surface,resolution)
screen.blit(screen_surface,(0,0))


running=True
while running:
    for event in pygame.event.get():
        if event.type==pygame.KEYDOWN:
            if event.key==pygame.K_ESCAPE:
                running=False
    time_delta=clock.tick(60)/1000.0
    pygame.display.flip()

pygame.quit()