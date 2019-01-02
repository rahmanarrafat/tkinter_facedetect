from tkinter import *
import cv2
import PIL
from PIL import Image, ImageTk

face_cascade = cv2.CascadeClassifier('C:/opencv/sources/data/haarcascades/haarcascade_frontalface_default.xml')
root = Tk()


class App:
    def __init__(self, window, window_title,video_source = 0):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source

        self.vid = MyVideoCapture(self.video_source)

        self.judul = Label(window, text="Face Detection", font=("Times New Roman", 20))
        self.judul.pack()

        self.canvas =  Canvas(window,width = self.vid.width, height = self.vid.height)
        self.canvas.pack(side = "left")

        self.canvas1 = Canvas(window)
        self.canvas1.pack(side = "right" ,fill= BOTH)

        self.btn_snapshot = Button(window, text="Snapshot", width=10, command=self.snapshot, relief = GROOVE)
        self.btn_snapshot.pack(side = "left", padx=10, pady=10,  anchor=CENTER, expand=True)

        self.delay = 15
        self.update()

        self.window.mainloop()

    def snapshot(self):
        ret, frame = self.vid.get_frame()
        img = cv2.resize(frame, (720, 576), interpolation=cv2.INTER_LINEAR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        faces = face_cascade.detectMultiScale(img, 1.2, 4)
        for (x, y, w, h) in faces:
            y = y
            cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 0), 0)
            face = img[y:y + h, x:x + w]
        cv2.imwrite("face.jpg", face)
        self.openimage()

    def openimage(self):
        fc = Image.open('face.jpg')
        self.canvas1.image = ImageTk.PhotoImage(fc)
        self.canvas1.create_image(3, 3, image=self.canvas1.image, anchor=NW)

    def update(self):
        ret, frame = self.vid.get_frame()
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
            self.canvas.create_image(0, 0, image=self.photo, anchor=NW)
        self.window.after(self.delay, self.update)

class MyVideoCapture:
    def __init__(self, video_source = 0):
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened():
            raise ValueError ("Unable to Open", video_source)
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def get_frame(self):
        if self.vid.isOpened():
            ret,frame = self.vid.read()
            if ret:
                self.img = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                self.faces = face_cascade.detectMultiScale(self.img, 1.2, 4)
                for (x, y, w, h) in self.faces:
                    y = y
                    cv2.rectangle(self.img, (x, y), (x + w, y + h), (255, 0, 0), 2)
                    self.face = self.img[y:y + h, x:x + w]
                return(ret, self.img)
            else:
                return (ret, None)
        #else:
            #return (ret, None)

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()


App(root, "Face Detection")
