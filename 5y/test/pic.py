def CaptureImage():
	imageName = 'DontCare.jpg' #Just a random string
	cap = cv2.VideoCapture(0)
	while(True):
	    # Capture frame-by-frame
	    ret, frame = cap.read()

	    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #For capture image in monochrome
	    rgbImage = frame #For capture the image in RGB color space

	    # Display the resulting frame
	    cv2.imshow('Webcam',rgbImage)
	    #Wait to press 'q' key for capturing
	    if cv2.waitKey(1) & 0xFF == ord('q'):
	        #Set the image name to the date it was captured
	        imageName = str(time.strftime("%Y_%m_%d_%H_%M_%S")) + '.jpg'
	        #Save the image
	        cv2.imwrite(imageName, rgbImage)
	        break
	# When everything done, release the capture
	cap.release()
	cv2.destroyAllWindows()
	#Returns the captured image's name
	return imageName
