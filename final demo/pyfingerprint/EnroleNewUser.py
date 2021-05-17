import threading
import time
import logging
import random
#import queue
import string

import hashlib
class EnroleUser(object):
    def __init__(self, fpR):
        self.fpR = fpR 
        
    def enroleUser(self, id):
    
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
        
        positionNumber = self.fpR.storeTemplate(id)
        
        print('User fp stored @ ' + str(positionNumber))
        
        
