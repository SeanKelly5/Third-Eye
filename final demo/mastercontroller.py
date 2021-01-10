import threading
import time
import logging
import random
#import queue
import string

import hashlib
from pyfingerprint.pyfingerprint import PyFingerprint

MAX_USERS = 1 #increase this to add a new user
BUF_SIZE = 10
#q = queue.Queue(BUF_SIZE)

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

        if ( self.fpR.verifyPassword() == False ):
            raise ValueError('The given fingerprint sensor password is wrong!')
        return    
        
    
    def enrollUser(self): #master user
        self.fpR.clearDatabase() #clear all templates
        print('Waiting for Master User...')

        ## Wait that finger is read
        while ( self.fpR.readImage() == False ):
            pass

        ## Converts read image to characteristics and stores it in charbuffer 1
        self.fpR.convertImage(0x01)

        ## Checks if finger is already enrolled
        result = self.fpR.searchTemplate()
        positionNumber = result[0]

        if ( positionNumber >= 0 ):
            print('Template already exists at position #' + str(positionNumber))
            exit(0)

        print('Remove finger...')
        time.sleep(1)

        print('Waiting for same finger again...')

        ## Wait that finger is read again
        while ( self.fpR.readImage() == False ):
            pass

        ## Converts read image to characteristics and stores it in charbuffer 2
        self.fpR.convertImage(0x02)

        ## Compares the charbuffers
        if ( self.fpR.compareCharacteristics() == 0 ):
            raise Exception('Fingers do not match')

        ## Creates a template
        self.fpR.createTemplate()

        ## Saves template at  position number 1 key user
        self.nextId = 1
        positionNumber = self.fpR.storeTemplate(self.nextId)
        

        self.nextId += 1
        
   
    
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
                while(self.fpR.readImage() == True): #detect finger off sensor
                    pass
                
                                

    def getScore(self):
        #get score of current finger 
        return (self.uId, self.score)
        


    
class MasterController: #controls the lock state
    def __init__(self):
        self.MAX_USERS = 1 # increse this to add more users
        self.userCount = 0
        self.fpCtlr = FpController() 
        #self.vidCtlr = VidController()
        return

    def startFpSearcher(self):
        self.fpCtlr.start() #now start the search for users
        ## for test
        while(True):
            print(self.fpCtlr.getScore())
            time.sleep(0.5) # sleep so searcher completes

    def enrollKeyUser(self): 
        self.fpCtlr.enrollUser() #enroll key user at location 1
        #self.vidCtlr.captureUser(1)
        
    def startVidCapture(self):
        pass

    
    def start(self): 
        vid_match = 0 
        fp_score = 0
        
        if(self.vidCtlr.isReady()): #if user is recognised with video 
            match = self.vidCtlr.identify()
        else:
            (id, score) = self.fpCtlr.getScore()
            fp_score = score
            if(score > 70):
                self.vidCtlr.captureUser(id)
        if(vid_match | fp_score > 70):
            pass ##unlock
            
            

if __name__ == "__main__":
    mc = MasterController()
    mc.enrollKeyUser()
    mc.startFpSearcher() #kick off the fp search thread
    mc.startVidCapture()

    #mc.start()

    

# At init I must get X pics of the user first before running the NN - Use the FP reader to ident the user and trigger the camera
# To enroll a new user the face of existing and finger print on new user     
