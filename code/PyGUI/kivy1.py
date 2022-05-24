import kivy 
from kivy.app import App 
from kivy.uix.floatlayout import FloatLayout 
from kivy.uix.boxlayout import BoxLayout 
from kivy.uix.label import Label 
from kivy.uix.button import Button 
from kivy.uix.filechooser import FileChooserIconView
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.filechooser import FileChooserLayout

from kivy.properties import ObjectProperty 
from kivy.uix.popup import Popup 
from kivy.factory import Factory 
from kivy.uix.screenmanager import Screen,ScreenManager # from kivy.clock import Clock 
from kivy.graphics.texture import Texture 
from kivy.uix.camera import Camera 
from kivy.properties import BooleanProperty, NumericProperty 
import os 
import cv2 
import numpy as np 
import logging 
from kivy.core.window import Window
#from sample_lane_detection import *

kivy.require('2.0.0')

#indexPage
class IndexPage(FloatLayout):

    def __init__(self,**kwargs):
        super().__init__(**kwargs)
    def page_go(*args):
        App.get_running_app().screen_manager.current="Image_page"
        App.get_running_app().screen_manager.transition.direction = 'left'#这个是过长动画的方向


def detect_img(img):
    #print(img)
    return img
def cv_imread(filePath):
    with open(filePath,mode="rb") as f:
        img_buff = np.frombuffer(f.read(),dtype=np.uint8)
    cv_img = cv2.imdecode(img_buff,-1)
    return cv_img
def kivy_showcvimg(img,win):
    img_buff = img.tostring()
    img_texture = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt='rgba')
    img_texture.blit_buffer(img_buff, colorfmt='rgba', bufferfmt='ubyte')
    win.texture = img_texture
#Image page
class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    cwdir = ObjectProperty(None)
class LoadFolder(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    cwdir = ObjectProperty(None)
Factory.register("LoadDialog",cls=LoadDialog)#注册一个类？

class ImagePage(BoxLayout):
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
    def selectfolder(self):
        print("selectfolder")
        content = LoadFolder(load=self.openfile,cancel=self.dismiss_popup,cwdir=os.getcwd())
        self._popup = Popup(title="Load Folder",content=content,size_hint=(.9,.9))
        self._popup.open()
    def openfile(self,path,filename):
        print(path,filename)
    def back_index(*args):
        App.get_running_app().screen_manager.current="Index_page"#这个页面返回是Index_page
        App.get_running_app().screen_manager.transition.direction = 'right'
    def back_video(self,*args):
        App.get_running_app().screen_manager.current="Video_page"
        App.get_running_app().screen_manager.transition.direction = 'left'
    def dismiss_popup(self):
        self._popup.dismiss()
    def show_load(self):
        content = LoadDialog(load=self._load,cancel=self.dismiss_popup,cwdir=os.getcwd())
        self._popup = Popup(title="Load Image",content=content,size_hint=(.9,.9))
        self._popup.open()
    def _load(self,path,filename):
        print(path,filename)
        self.dismiss_popup()
        logging.info("path:{},filename:{}".format(path,filename))
        print("filename")
        img = cv_imread(filename)
        img = detect_img(img)
        print(img.shape)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGBA)
        #cv2.imshow(img)
        img = cv2.flip(img, 0) # 旋转
        #cv2.imshow(img)
        print("after flip",img.shape)
        kivy_showcvimg(img,self.ids.img_det)
        kivy_showcvimg(img,self.ids.img_det1)
        #img_buff = img.tostring()
        #img_texture = Texture.create(size=(img.shape[1], img.shape[0]), colorfmt='rgba')
        #img_texture.blit_buffer(img_buff, colorfmt='rgba', bufferfmt='ubyte')
        #self.ids.img_det.texture = img_texture
        

class LaneDetectApp(App):
    def build(self):
        Window.fullscreen=0
        Window.size=(1000,400)
        self.icon = "./static/icon.ico" 
        self.title = "智能车道线检测App"
        self.load_kv("./index.kv") # 需要创建一个index.kv 
        self.load_kv("./image.kv")
        self.screen_manager = ScreenManager()
        pages = {"Index_page":IndexPage(),"Image_page":ImagePage(),}

        for item,page in pages.items(): 
            print(item)
            self.default_page = page
             # 添加页面
            screen = Screen(name=item)
            screen.add_widget(self.default_page) # 向屏幕管理器添加页面
            self.screen_manager.add_widget(screen)
        return self.screen_manager


LaneDetectApp().run()