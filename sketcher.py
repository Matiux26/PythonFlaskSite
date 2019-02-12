import cv2
import numpy as np
import uuid

class draw():
    drawing = False # true if mouse is pressed
    mode = True # if True, draw rectangle. Press 'm' to toggle to curve
    ix,iy = -1,-1
    img = np.zeros((28,28,1), np.uint8)
    # mouse callback function
    def draw_line(this,event,x,y,flags,param):
        global ix,iy,ix2,iy2,drawing,mode
    
        if event == cv2.EVENT_LBUTTONDOWN:
            this.drawing = True
            ix,iy = x,y
    
        elif event == cv2.EVENT_MOUSEMOVE:
            if this.drawing == True:
                ix2,iy2 = ix,iy
                ix,iy = x,y
                if this.mode == True:
					#cv.Line(this.img, pt1, pt2, color, thickness=1, lineType=8, shift=0)
                    cv2.line(this.img,(ix,iy),(ix2,iy2),(0,0,0),1,cv2.LINE_AA)
    
        elif event == cv2.EVENT_LBUTTONUP:
            this.drawing = False
            if this.mode == True:
                cv2.line(this.img,(ix,iy),(ix2,iy2),(0,0,0),1,cv2.LINE_AA)
    
    def main(this):
        this.img = np.zeros((28,28,1), np.uint8)
        this.img[:] = 255
        cv2.namedWindow('press escape to save')
        cv2.setMouseCallback('press escape to save',this.draw_line)
        while(1):
            cv2.imshow('press escape to save',this.img)
            k = cv2.waitKey(1) & 0xFF
            if k == ord('m'):
                this.mode = not this.mode
            elif k == 27:
                unique_filename = str(uuid.uuid4())
                unique_path = unique_filename+".png"
                cv2.imwrite("C:/Users/Glina/.spyder-py3/ProjektFlask_mateusz_gliniecki_17928/static/"+unique_filename+".png", this.img)
                break    
        cv2.destroyAllWindows()
        return unique_path,this.img
    
if __name__ == '__main__':
    drw = draw()
    drw.main()
    