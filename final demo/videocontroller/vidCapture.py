import numpy as np
import cv2

class VideoCaptureStream(object):

    """
        Manages Video Capture
    """

    def __init__(self):
        """
        Constructor
        """
        self.capstream = cv2.VideoCapture(0)
        print("Video Stream COnstruct")

        self.capstream.set(3,640) # set Width
        self.capstream.set(4,480) # set Height



    def __del__(self):
        """
        Destructor
        """
        self.capstream.release()
        cv2.destroyAllWindows()

        
    def startStream(self):
    
        ret, frame = self.capstream.read()
        #if (frame.empty()):
         #   print("ERROR! blank frame grabbed\n")
            
        frame = cv2.flip(frame, -1) # Flip camera vertically
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        cv2.imshow('frame', frame)
        cv2.imshow('gray', gray)
        
        k = cv2.waitKey(30) & 0xff
         
 
