import threading
import time
import logging
import random
#import queue
import string

import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint
from pyfingerprint import EnroleNewUser
from videocontroller.vidCapture import VideoCaptureStream
from videocontroller.faceDetect import FaceDetect





class VidController(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(VidController,self).__init__()
        self.target = target
        self.name = name
        self.faceDetect = False
        
        
        self.vidStream = VideoCaptureStream()    
    
    def startStream(self):
        self.vidStream.startStream()
        
    def stopStream(self):
        self.vidStream.stopStream()
        
    def enableFaceDetect(self):
        self.faceDetect = True 
        print("Set FD Algo Active")
        
    
    def run(self):      
        #will start the vide o streaming
        print('Video Stream Starting ...')
        while(True):
            self.startStream() 
            if(self.faceDetect == True):
                self.vidStream.recogniseFace()
            
            #time.sleep(0.3)
       
    def getFace(self):
        return self.vidStream.getFace()
        
    def storeFace(self, uid, offset):
        return self.vidStream.storeFace(uid, offset)
            
            
            
                                

   

class FpController(threading.Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs=None, verbose=None):
        super(FpController,self).__init__()
        self.target = target
        self.name = name
        self.score = 0.0
        self.uId = 0
        self.nextId = 0
        
        
        self.fpR = PyFingerprint('/dev/ttyUSB0', 57600, 0xFFFFFFFF, 0x00000000)
        self.newUser = EnroleNewUser.EnroleUser(self.fpR) 
        
        

        if ( self.fpR.verifyPassword() == False ):
            raise ValueError('The given fingerprint sensor password is wrong!')
        return    
        
    
    
    
    def run(self):      
        #will search for fingerprints   
        print('Scan for fingerprint thread starting...')
        self.fpScanEnable = True
        while(self.fpScanEnable == True):  
            self.uId = -1
            self.score = -1
            ## Wait that finger is read
            if( self.fpR.readImage() == True ):
                ## Converts read image to characteristics and stores it in charbuffer 1
                self.fpR.convertImage(0x01)
                ## Searchs template
                result = self.fpR.searchTemplate()
                self.uId = result[0]
                self.score = result[1]
                print("fp " + str(result[0]))
                while(self.fpR.readImage() == True): #detect finger off sensor
                    pass
                time.sleep(1)
                                

    def getScore(self):
        #get score of current finger 
        return (self.uId, self.score)
        


    
class MasterController: #controls the lock state
    def __init__(self):
        self.users = dict() #main data store for users
        self.MAX_USERS = 1 # increse this to add more users
        self.userCount = 0
        self.searchRun = True
        self.lock = False
        self.fpCtlr = FpController() 
        self.vidCtlr = VidController()
        return
        
    class UserAc:
        def __init__(self, id):
            self.id = id    
            self.fpCnt = 0
            self.faceCnt = 0
             
        def getFpCnt(self):
            return self.fpCnt
        def getFaceCnt(self): 
            return self.faceCnt
    
    def setState(self, lock):
        if(self.lock != lock):
            self.lock = lock
            if(self.lock):
                print("Lock State is LOCKED")
            else:
                print("Lock State is UNLOCKED")


    def startFpSearcher(self):
        self.fpCtlr.start() #now start the search for users
       
        while(self.searchRun):
            #print(self.fpCtlr.getScore()) #return user id and confidence
            (uid,score) = self.fpCtlr.getScore()
            
            lock = True
            if(score > 70):
                lock = False
            self.setState(lock)
            
            if(uid in self.users):
                if(self.users[uid].getFaceCnt() < 10):
                    #capt frame
                    print("store user img id " + str(uid))
                    faceCaptured = 0
                    while(faceCaptured == 0):
                        faceCaptured = self.vidCtlr.storeFace(uid, self.users[uid].getFaceCnt()+1)
                    self.users[uid].fpCnt +=1
                    self.users[uid].faceCnt += 1                    
                else :
                    self.searchRun = False
            
            time.sleep(0.5)
            

    def enrollKeyUser(self, uid): 
        self.fpCtlr.newUser.enroleUser(uid) #enroll key user at location 1, this could br passed in also 
        self.users[uid]= MasterController.UserAc(uid)
        faceCaptured = 0
        while(faceCaptured == 0):
            faceCaptured = self.vidCtlr.storeFace(uid, uid)
        if(faceCaptured > 0):
            self.users[uid].faceCnt += 1
        print("Facecount")
        print((self.users[uid].getFaceCnt()))
        
            
        
    def startVidCapture(self):
        self.vidCtlr.start()
     

    
    def start(self): 
        vid_match = 0 
        fp_score = 0       
    
        (id, score) = self.fpCtlr.getScore()
        fp_score = score
        print(fp_score)
    
    def train(self):
        fd = FaceDetect()
        fd.train()
        self.vidCtlr.enableFaceDetect()
    
   

        
            
            
            

if __name__ == "__main__":
    mc = MasterController()
    
    mc.startVidCapture()
   
    mc.enrollKeyUser(1) #this will be a new user of the lock
    
    while(mc.searchRun == True): 
       mc.startFpSearcher() #kick off the fp search thread
    
    
    mc.train() #train classifier
    


    
