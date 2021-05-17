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

        self.capstream.set(3,640/2) # set Width
        self.capstream.set(4,480/2) # set Height
        self.frame = 0
        self.gray = 0 
        self.streamOn = False
        self.faceCascade = cv2.CascadeClassifier('./videocontroller/haarcascade_frontalface_alt.xml')
        self.lock = True



    def __del__(self):
        """
        Destructor
        """
        self.capstream.release()
        cv2.destroyAllWindows()
    
    def stopStream(self):
        self.streamOn = False

        
    def startStream(self):
        self.streamOn = True
        
    
        ret, self.frame = self.capstream.read()
        #if (frame.empty()):
         #   print("ERROR! blank frame grabbed\n")
            
        #self.frame = cv2.flip(frame, -1) # Flip camera vertically
        self.gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        
        cv2.imshow('frame', self.frame)
        #cv2.imshow('gray', gray)
        
        k = cv2.waitKey(10) 
            
        
        
    
    def getFace(self):
        faceCascade = cv2.CascadeClassifier('./videocontroller/haarcascade_frontalface_alt.xml')
    
        ret, frame = self.capstream.read()               
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        faces = faceCascade.detectMultiScale(gray,scaleFactor=1.3, minNeighbors=5,minSize=(20, 20))
        print(len(faces))

        for (x,y,w,h) in faces:
            cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = gray[y:y+h, x:x+w]

        cv2.imshow('video',frame)
        cv2.waitKey(0)
        cv2.destroyAllWindows()    
        self.capstream.release()


    def storeFace(self, uid, offset):
        
        
        
        faces = self.faceCascade.detectMultiScale(self.gray, scaleFactor=1.3, minNeighbors=5,minSize=(20, 20))
        

        for (x,y,w,h) in faces:
            cv2.rectangle(self.frame,(x,y),(x+w,y+h),(255,0,0),2)
            roi_gray = self.gray[y:y+h, x:x+w]

            # Save the captured imageinto the datasets folder
            cv2.imwrite("./videocontroller/dataset/User_" + str(uid) + '.' + str(offset)  + ".jpg", self.gray[y:y+h,x:x+w])

        
        return len(faces)
    
    def recogniseFace(self):
                
        recognizer = cv2.face.LBPHFaceRecognizer_create()
        recognizer.read('./videocontroller/trainer/trainer.yml')
        cascadePath = "./videocontroller/haarcascade_frontalface_alt.xml"
        faceCascade = cv2.CascadeClassifier(cascadePath)

       

        #iniciate id counter
        id = 0


        # Define min window size to be recognized as a face
        minW = 0.1*self.capstream.get(3)
        minH = 0.1*self.capstream.get(4)

        
        
        faces = faceCascade.detectMultiScale(self.gray,scaleFactor=1.3, minNeighbors=5,minSize=(20, 20))
        

        for(x,y,w,h) in faces:
            cv2.rectangle(self.frame, (x,y), (x+w,y+h), (0,255,0), 2)
            id, confidence = recognizer.predict(self.gray[y:y+h,x:x+w])

            # Check if confidence is less them 100 ==> "0" is perfect match 
            if (confidence < 100):
                self.setState(False)
            else:
                self.setState(True)
    
    def setState(self, lock):
        if(self.lock != lock):
            self.lock = lock
            if(self.lock):
                print("Lock State is LOCKED")
            else:
                print("Lock State is UNLOCKED")
            
         
        
        

        
         
 
