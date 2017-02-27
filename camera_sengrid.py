import sendgrid
import cv2


def get_image(camera):
    # read is the easiest way to get a full image out of a VideoCapture object.
    retval, im = camera.read()
    return im


def _take_picture(camera, archivo="test_image.png"):
    # Camera 0 is the integrated web cam on my netbook
    # Ramp the camera - these frames will be discarded and are only used to allow v4l2
    # to adjust light levels, if necessary
    print("Taking image...")
    # Take the actual image we want to keep
    camera_capture = get_image(camera)
    # A nice feature of the imwrite method is that it will automatically choose the
    # correct format based on the file extension you provide. Convenient!
    cv2.imwrite(archivo, camera_capture)
    # You'll want to release the camera, otherwise you won't be able to create a new
    # capture object until your script exits
    #del(camera)


def _take_movie(cap):
    fourcc = cv2.cv.CV_FOURCC('X','V','I','D')
    out = cv2.VideoWriter('output.avi',fourcc, 20.0, (352,288))
    cant = 0 
    print "capturando video"
    while(cant < 150):
      ret, frame = cap.read()
      if ret==True:
        #frame = cv2.flip(frame,0)
        out.write(frame)
        print "FRAME CAPTURADO %d" % cant
      cant+=1
    print "video capturado"
    #out.release()

def send_email_image(camera):
    sg = sendgrid.SendGridClient('<sengrid api key>')
    message = sendgrid.Mail()
    message.add_to('<to_email>')
    message.set_subject('SOSPECHOSOS EN LA PUERTA IMAGENES')
    #message.set_html('Body')
    message.set_text('Esta persona esta fuera de la casa')
    message.set_from('<from email>')
    _take_picture(camera,"1.png")
    message.add_attachment('sospechoso.png', '/root/1.png')
    _take_picture(camera, "2.png")
    message.add_attachment('sospechoso_foto2.png', '/root/2.png')
    _take_picture(camera, "3.png")
    message.add_attachment('sospechoso_foto3.png', '/root/3.png')
    status, msg = sg.send(message)
    print("IMAGE SEND STATUS", status)


def send_email_movie(camera):
    sg = sendgrid.SendGridClient('<sengrid api key>')
    message = sendgrid.Mail()
    message.add_to('<to email>')
    message.set_subject('SOSPECHOSOS EN LA PUERTA VIDEO')
    #message.set_html('Body')
    message.set_text('Esta persona esta fuera de la casa')
    message.set_from('<From email>')
    _take_movie(camera)
    message.add_attachment('video.avi', '/root/output.avi')
    status, msg = sg.send(message)
    print("MOVIE SEND STATUS", status)


print "SISTEMA DE VIGILANCIA V.00"
camera_port = 0
faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
#Number of frames to throw away while the camera adjusts to light levels
# Now we can initialize the camera capture object with the cv2.VideoCapture class.
# All it needs is the index to a camera port.
camera = cv2.VideoCapture(camera_port)
# Set width and height
camera.set(3,352)
camera.set(4,288)
print("Taking image...")
# Take the actual image we want to keep
qty = 0
while(1):
    image = get_image(camera)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Detect faces in the image
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags = cv2.cv.CV_HAAR_SCALE_IMAGE
    )
    print "Found {0} faces!".format(len(faces))
    qty = len(faces)
    if qty > 0:
        send_email_image(camera)
        send_email_movie(camera)
camera.release()




