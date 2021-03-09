from tkinter import *
from PIL import Image, ImageTk
import tkinter.messagebox
import tkinter.filedialog
import dlib
import cv2
import time
import os


class Picture(object):
    def __init__(self, init_window_name):
        self.window = init_window_name
        self.image_path = []
        self.img_num = 0
        self.welcome_path = './welcome.jpg'  # 初始化图片

    def init_window(self):
        self.window.geometry('800x520+500+100')
        self.window.resizable(0, 0)  # 防止用户调整尺寸
        self.window.title("人脸检测工具")
        self.menubar = Menu(self.window)
        self.filemenu = Menu(self.window, tearoff=0)
        self.aboutmenu = Menu(self.window, tearoff=0)
        self.menubar.add_cascade(label='文件', menu=self.filemenu)
        self.menubar.add_cascade(label='关于', menu=self.aboutmenu)
        self.filemenu.add_command(label='打开', command=self.select_file)
        self.aboutmenu.add_command(label='版本号: 1.0')
        self.aboutmenu.add_command(label='作者: Humy')

        self.welcome = Label(self.window, text='人脸检测', fg='white', bg='#f58f98', font=('Arial', 12), width=34,
                             height=2).place(x=230, y=10)
        self.img_open = Image.open(self.welcome_path).resize((258, 258))
        self.image = ImageTk.PhotoImage(self.img_open)
        self.label_img = Label(self.window, image=self.image)
        self.label_img.place(x=250, y=100)

        self.var_path = StringVar()

        self.path = Label(self.window, textvariable=self.var_path,
                          highlightcolor='red', font=('Arial', 12), height=1).place(x=250, y=380)

        self.submit = Button(self.window, text='提交', font=('Arial', 12), fg='white', width=10, height=1,
                             command=self.submit_cmd, bg='#f58f98', state=DISABLED)
        self.submit.place(x=320, y=430)

        self.window.config(menu=self.menubar)
        self.window.mainloop()

    def select_file(self):
        self.filename = tkinter.filedialog.askopenfilename()
        img_open = Image.open(self.filename).resize((258, 258))
        image = ImageTk.PhotoImage(img_open)
        self.label_img.configure(image=image)
        self.label_img.image = image
        self.submit['state'] = NORMAL

    def submit_cmd(self):
        save_filename, info = self.face_detect(self.filename)
        if save_filename != '':
            img_open = Image.open(save_filename).resize((258, 258))
            info = "人脸个数为:"+str(info)
            self.var_path.set(info)
            image = ImageTk.PhotoImage(img_open)
            self.label_img.configure(image=image)
            self.label_img.image = image
        else:
            self.var_path.set(info)

    def load_img(self, path):
        img = cv2.imread(path)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # opencv默认图片通道为bgr,使用dlib需要转为rgb通道
        return img

    def face_detect(self, img_path):
        detector = dlib.get_frontal_face_detector()
        img = self.load_img(img_path)
        faces = detector(img, 1)
        face_nums = len(faces)
        if face_nums > 0:
            for face in faces:
                cv2.rectangle(img, (face.left(), face.top()), (face.right(), face.bottom()), (0, 0, 255), 2)
            t = time.localtime(time.time())
            timeInfo = '{}{}{}{}{}{}.jpg'.format(t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min, t.tm_sec)
            save_file = os.path.join('./face', timeInfo)
            cv2.imwrite(save_file, cv2.cvtColor(img, cv2.COLOR_RGB2BGR))
            return save_file, face_nums
        else:
            info = '没有发现人脸！'
            return '', info


if __name__ == "__main__":
    windows = Tk()
    picture = Picture(windows)
    picture.init_window()
