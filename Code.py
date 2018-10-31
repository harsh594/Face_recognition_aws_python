def xmain():
 import dlib 
 import cv2 

 import os 
 import boto3
 import shutil
  
 from Excel import excel 

 print("----------------FACE DETECTION OPENS--------------------")
 stream = cv2.VideoCapture(0)
 
# Face detector
 detector = dlib.get_frontal_face_detector()
 folderName = "user"                                                        # creating the person or user folder
 folderPath = os.path.join(os.path.dirname(os.path.realpath('__file__')), folderName)
 if not os.path.exists(folderPath):
    os.makedirs(folderPath)
 
# Fancy box drawing function by Dan Masek
 def draw_border(img, pt1, pt2, color, thickness, r, d):
    x1, y1 = pt1
    x2, y2 = pt2
 
    # Top left drawing
    cv2.line(img, (x1 + r, y1), (x1 + r + d, y1), color, thickness)
    cv2.line(img, (x1, y1 + r), (x1, y1 + r + d), color, thickness)
    cv2.ellipse(img, (x1 + r, y1 + r), (r, r), 180, 0, 90, color, thickness)
 
    # Top right drawing
    cv2.line(img, (x2 - r, y1), (x2 - r - d, y1), color, thickness)
    cv2.line(img, (x2, y1 + r), (x2, y1 + r + d), color, thickness)
    cv2.ellipse(img, (x2 - r, y1 + r), (r, r), 270, 0, 90, color, thickness)
 
    # Bottom left drawing
    cv2.line(img, (x1 + r, y2), (x1 + r + d, y2), color, thickness)
    cv2.line(img, (x1, y2 - r), (x1, y2 - r - d), color, thickness)
    cv2.ellipse(img, (x1 + r, y2 - r), (r, r), 90, 0, 90, color, thickness)
 
    # Bottom right drawing
    cv2.line(img, (x2 - r, y2), (x2 - r - d, y2), color, thickness)
    cv2.line(img, (x2, y2 - r), (x2, y2 - r - d), color, thickness)
    cv2.ellipse(img, (x2 - r, y2 - r), (r, r), 0, 0, 90, color, thickness)
 j=0 
 while True:
    # read frames from live web cam stream
    (grabbed, frame) = stream.read(0)
    frame = cv2.flip(frame, 1)
    if grabbed==True:
    # resize the frames to be smaller and switch to gray scale
     gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
     
    # Make copies of the frame for transparency processing
     overlay = frame.copy()
     output = frame.copy()
 
    # set transparency value
     alpha  = 0.5
 
    # detect faces in the gray scale frame
     face_rects = detector(gray, 0)
    else:
        continue
    # loop over the face detections
    for i, d in enumerate(face_rects):
     if j%10==0:
        cv2.imwrite(folderPath + "/User" +("%s"%j)+ ".jpg",
                    frame[d.top():d.bottom(), d.left():d.right()])
     j+=1
        # draw a fancy border around the faces
     draw_border(overlay, (d.left(), d.top())  ,(d.right(), d.bottom()), (162, 255, 0), 2, 10, 10)
 
    # make semi-transparent bounding box
    cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)
 
    # show the frame
    cv2.imshow("Face Detection", output)
    key = cv2.waitKey(1) & 0xFF
 
    # press q to break out of the loop
    if key == ord("q"):
        break
    if key == ord("r"):
        print("\n%s memory freed "%folderPath)
        print("---RETURNING TO MAIN WINDOW")
        fileList = os.listdir(folderPath)
        for fileName in fileList:
         os.remove(folderPath+"/"+fileName)
        cv2.destroyAllWindows()
        stream.release()
        return
 
# cleanup
 cv2.destroyAllWindows()
 stream.release()
 
 print("\nImages stored in local storage: %s"%folderPath) 
 s3 = boto3.client('s3')
 bucket_name = 'rtfrc1'
 if os.listdir(folderPath)==[]:
     print("---No files to upload.. TRY AGAIN!!!!!")
     return

 for filename in os.listdir(folderPath):
    try: 
     s3.upload_file(folderPath+"\\"+filename, bucket_name,filename)
    except:
        print("No INTERNET CONNECTION....... ")
        fileList = os.listdir(folderPath)
        for fileName in fileList:
         os.remove(folderPath+"/"+fileName)
        print("MEMORY FREED....STOPPING PROCESS!!!!") 
        return
 print("\nImages uploaded to Bucket for Comparison")   
 
 
 rek=boto3.client('rekognition','us-east-1')
 s4 = boto3.resource('s3')
 
 l = []
 r = []
 prefix="1"
 print("\n-----------------FACE RECOGNITION WILL START---------------------------")
 bucket=s4.Bucket('testrekcomprtfrc')
 bucket1=s4.Bucket('rtfrc1')
 for xyz in bucket1.objects.all():
  for obj in bucket.objects.all():
     
     print('{0}:{1}'.format(bucket.name, obj.key))
     print('{0}:{1}'.format(bucket1.name, xyz.key))
     try:
     
      response=rek.compare_faces(SimilarityThreshold=80,
        SourceImage={
                'S3Object':
                    {'Bucket':'testrekcomprtfrc','Name':obj.key}},TargetImage={'S3Object':{
                            'Bucket':'rtfrc1','Name':xyz.key}})
      for faceMatch in response['FaceMatches']:
        position = faceMatch['Face']['BoundingBox']
        if(position):
            l.append(os.path.splitext(obj.key)[0])
            r.append(os.path.splitext(xyz.key)[0])
         
        confidence = str(faceMatch['Face']['Confidence'])
        print('The face at ' +
               str(position['Left']) + ' ' +
               str(position['Top']) +
               ' matches with ' + confidence + '% confidence')
     except:
       print(xyz.key +" has no face") 
       s4.Object('rtfrc1', xyz.key).delete()
       continue
 print("---FACE RECOGNITION COMPLETED----")   
 l=list(set(l))
 if len(l)!=1:
  print("%s People are present"%len(l))
  
 else:
    print("%s Person is present"%len(l))
 for i in l:
   print(i)
 k=[]
 folderN = "SUSPECTED PERSONS"                                                        # creating the person or user folder
 folderP= os.path.join(os.path.dirname(os.path.realpath('__file__')), folderN)
 if not os.path.exists(folderP):
    os.makedirs(folderPerson)
 for i in r:
   k.append(i+'.jpeg')
 if k==[]:
  for fileName in os.listdir(folderPath):
    shutil.copy(folderPath+'\\'+fileName, folderPerson)
    os.remove(folderPath+"\\"+fileName)  
  pass
 else:    
  fileList = os.listdir(folderPath)
  for fileName in fileList:
  
   for i in k:
     if fileName==i:  
      os.remove(folderPath+"\\"+fileName)
      break
     else:
       if i==k[len(k)-1]:
        shutil.copy(folderPath+'\\'+fileName, folderPerson)
        os.remove(folderPath+"\\"+fileName)
        break
       else:
           pass
 print("\n%s---LOCAL memory freed--- "%folderPath)
 
 s5 = boto3.resource('s3')
 bucket1=s5.Bucket('rtfrc1')
 for obj in bucket1.objects.all():
        s5.Object(bucket1.name, obj.key).delete()        
 excel(l)
 print("----------Data written in excel sheet------------")
 print("-------RETURNING TO MAIN WINDOW-------")
if __name__=='__main__':
 xmain()         