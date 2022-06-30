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
import pandas as pd
import os
import win32timezone

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
def AddAnObserver(ObserverName):
    if(os.path.exists('ObserverName.csv')==False):
        df=pd.DataFrame([[0,'Nobody',0]],columns=['id','name','score'])
        df.to_csv('ObserverName.csv')        
    df=pd.read_csv('ObserverName.csv')
    df=df.drop('Unnamed: 0',axis = 1) 
    #搜索一下是否有重名的
    if ObserverName in df.name.values:
        print("Welcome "+ObserverName)
        return
    df1=pd.DataFrame([[len(df),ObserverName,0]],columns=df.columns)
    df=df.append(df1)
    
    #print(df)
    df.to_csv('ObserverName.csv')
   #这个方法需要用户首先将 每种sense建立一个文件夹，里面的每张图片用condition名字命名，函数会提取场景名称和条件名称
def GetSenseNamesAndConditaionNames_MulLevFolder(sensesPath):
    #读取path下文件夹名称
    import os
    senseNames=os.listdir(sensesPath)
    df=pd.DataFrame(columns=['SenseNames'])
    dfCs = pd.DataFrame(columns=['ConditionNames'])
    conditionnameslist=[]
    for senses in senseNames:
        if senses[-4:] in ['.csv']:
            continue
        df1 = pd.DataFrame([[senses]],columns=['SenseNames'])
        df = df.append(df1)
        conditionnames = os.listdir(sensesPath+'/'+senses)
        conditionnameslist.append(conditionnames)

    for conditionnames in conditionnameslist:
        for name in conditionnames:
            if name in dfCs.ConditionNames.values:
                continue
            df1 = pd.DataFrame([[name]],columns=['ConditionNames'])
            dfCs = dfCs.append(df1)
    return df,dfCs

#Image page

class LoadDialog(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    cwdir = ObjectProperty(None)
    
class EnterObserverName(FloatLayout):
    cancel = ObjectProperty(None)
    enter = ObjectProperty(None)
    cwdir = ObjectProperty(None)
Factory.register("EnterObserverName",cls=EnterObserverName)#注册一个类？

class LoadFolder(FloatLayout):
    load = ObjectProperty(None)
    cancel = ObjectProperty(None)
    cwdir = ObjectProperty(None)
Factory.register("LoadDialog",cls=LoadDialog)#注册一个类？

#用snames，cname 构件对比图像对序列，写到csv中
#这个函数包含几列 id SenseName Condition1 Condition2 Path1 Path2
def MakeCmpPairList(SensesNames,ConditionNames,workPath):
    
    if(os.path.exists(workPath+'/'+'CmpPair.csv')==False):
        df=pd.DataFrame(columns=['id','SenseName','Condition1','Condition2','Path1','Path2','selection'])
        df.to_csv(workPath+'/'+'CmpPair.csv')
    df=pd.read_csv(workPath+'/'+'CmpPair.csv')
    df=df.drop('Unnamed: 0',axis = 1) 
    
    for Sense in SensesNames.SenseNames.values:
        for i,c in enumerate(ConditionNames.ConditionNames.values):
            for j,c1 in enumerate(ConditionNames.ConditionNames.values[i+1:]):
                path1 = workPath+'/'+Sense+'/'+c
                path2 = workPath+'/'+Sense+'/'+c1
                if(os.path.exists(path1)==True and os.path.exists(path2)==True):
                    tmpdf = df.loc[(df.SenseName==Sense)&(df.Condition1==c)&(df.Condition2==c1)]
                    if (len(tmpdf)>0):
                        df.loc[(df.SenseName==Sense)&(df.Condition1==c)&(df.Condition2==c1)].Path1.values[0]=path1
                        df.loc[(df.SenseName==Sense)&(df.Condition1==c)&(df.Condition2==c1)].Path2.values[0]=path2
                    else:
                        df1 = pd.DataFrame([[len(df),Sense,c.split('.')[0],c1.split('.')[0],path1,path2,'no']],columns=['id','SenseName','Condition1','Condition2','Path1','Path2','selection'])
                        df = df.append(df1)
    a=len(df)
    df = df.drop_duplicates(['SenseName','Condition1','Condition2'],keep='first')
    b=len(df)
    if (b<a):
       print("you enter the same data!!!")
    df.to_csv(workPath+'/'+'CmpPair.csv')
class ImagePage(BoxLayout):
    ImagePathList = []
    imgpairIndex = -1
    imgpairIndex_Cur =-1
    labelWidget=None
    ObserverName = 0
    SenceList=[]
    SenceNames=[]
    SenceId=0
    Condition_1list=[]
    Condition_2list=[]
    SensePath=None
    df_Sences=None
    df_Conditions=None
    PreOrNext = -1
    ComPairSelet = None
    img1 = None
    img2 = None
    def __init__(self,**kwargs):
        super().__init__(**kwargs)
        self.labelWidget=Label(text="show process id",size_hint=(0.1,0.05),pos_hint={'x':0.45,'y':0})
        self.add_widget(self.labelWidget)
    def JugeCmpPairIsSelected(self):
        observer=self.ObserverName
        sencename = 'DarkOnePiece'
        index = self.imgpairIndex
        if(os.path.exists(self.SensePath+'/CmpData.csv')==False):
            return -1
        df = pd.read_csv(self.SensePath+'/CmpData.csv')
        df1 = pd.read_csv(self.SensePath+'/CmpPair.csv')
        df1 = df1.drop('Unnamed: 0',axis = 1) 
        if (observer not in df1.iloc[index].selection):
            return -1
        else:
            sencename = df1.iloc[index].SenseName
            a = df.loc[(df.observer==observer) & (df.condition_1==df1.iloc[index].Condition1) & (df.condition_2==df1.iloc[index].Condition2) & (df.scene==sencename)]
            return a.selection.values[0]
    def selectfolder(self):
        print("selectfolder")
        content = LoadFolder(load=self.openfolder,cancel=self.dismiss_popup,cwdir=os.getcwd())
        self._popup = Popup(title="Load Folder",content=content,size_hint=(.9,.9))
        self._popup.open()
    def openfolder(self,path,filename):
        if(len(filename)==0):
            self.SensePath = path
        else:
            self.SensePath = filename
        if(os.path.exists(self.SensePath)==False):
            return
        self.df_Sences,self.df_Conditions=GetSenseNamesAndConditaionNames_MulLevFolder(self.SensePath)
        MakeCmpPairList(self.df_Sences,self.df_Conditions,self.SensePath)
        self.dismiss_popup()
    def openfile(self,path,filename):
        print(path,filename)
    def SelectWhichOne(self,LorR):
        if (self.ObserverName == 0):
            print("Please Enter AbserverName")
            return
        if (self.SensePath == None):
            print("Please Select Your WorkPath")
            return
        fullpath = self.SensePath+'/'+'CmpData.csv'
        if(os.path.exists(fullpath)==False):
            df=pd.DataFrame(columns=['observer','session_id','scene','condition_1','condition_2','selection','criterion'])
            df.to_csv(fullpath,index=False)        
            
        df=pd.read_csv(fullpath)
        #df=df.drop('Unnamed: 0',axis = 1) 
        senceidlist = np.argwhere(self.SenceNames==self.SenceList[self.imgpairIndex_Cur])
        if (len(senceidlist)>0):
            self.SenceId = senceidlist[0][0]
        else:
            print("No Sense List")
        df2=pd.read_csv(self.SensePath+'/'+'CmpPair.csv')
        df2=df2.drop('Unnamed: 0',axis = 1) 

        #print(img1.shape,img2.shape)
        #self.img1 = cv_imread(self.ImagePathList[self.imgpairIndex][0])
        #self.img2 = cv_imread(self.ImagePathList[self.imgpairIndex][1])
        if (LorR == 0):
            df1=pd.DataFrame([[self.ObserverName,self.SenceId,self.SenceList[self.imgpairIndex_Cur],self.Condition_1list[self.imgpairIndex_Cur],self.Condition_2list
            [self.imgpairIndex_Cur],0,'perceptual']],columns=['observer','session_id','scene','condition_1','condition_2','selection','criterion'])    
            #self.img1=cv2.rectangle(self.img1,(50,50),(int(self.img1.shape[0]/5),int(self.img1.shape[0]/5)),(0,0,255),20)
        else:
            df1=pd.DataFrame([[self.ObserverName,self.SenceId,self.SenceList[self.imgpairIndex_Cur],self.Condition_1list[self.imgpairIndex_Cur],self.Condition_2list[self.imgpairIndex_Cur],1,'perceptual']],columns=['observer','session_id','scene','condition_1','condition_2','selection','criterion'])
            #self.img2=cv2.rectangle(self.img2,(50,50),(int(img1.shape[0]/5),int(img1.shape[0]/5)),(0,0,255),20)
        
        
        
        
        #kivy_showcvimg(self.img1,self.ids.img_det)
        #kivy_showcvimg(self.img2,self.ids.img_det1)
        #print(df2.selection.values[self.imgpairIndex_Cur],self.ObserverName)
        if(df2.selection.values[self.imgpairIndex_Cur]=='no'):
            df2.selection.values[self.imgpairIndex_Cur]=''
        df2.selection.values[self.imgpairIndex_Cur]=df2.selection.values[self.imgpairIndex_Cur]+','+self.ObserverName
        df2.to_csv(self.SensePath+'/'+'CmpPair.csv')
        df=df.append(df1)
        df = df.drop_duplicates(['observer','scene','condition_1','condition_2'],keep='last')
        df.to_csv(fullpath,index=False)
        self.imgpairIndex = self.imgpairIndex - 1
        self.show_nextPairImgs()
        
    def back_index(*args):
        App.get_running_app().screen_manager.current="Index_page"#这个页面返回是Index_page
        App.get_running_app().screen_manager.transition.direction = 'right'
    def back_video(self,*args):
        App.get_running_app().screen_manager.current="Video_page"
        App.get_running_app().screen_manager.transition.direction = 'left'
    def dismiss_popup(self):
        self._popup.dismiss()
        
    def EnterObserverName(self):
        print("EnterObserverName")
        content = EnterObserverName(enter=self.AddAnObs,cancel=self.dismiss_popup,cwdir=os.getcwd())
        self._popup = Popup(title="Enter AbserverName",content=content,size_hint=(.4,.4))
        self._popup.open()
        
    def AddAnObs(self,name):
        self.ObserverName = name
        AddAnObserver(self.ObserverName)
        self.imgpairIndex = 0
        self.imgpairIndex_Cur= 0
        self.PreOrNext = 1
        self.dismiss_popup()
    def show_load(self):
        content = LoadDialog(load=self._load,cancel=self.dismiss_popup,cwdir=os.getcwd())
        self._popup = Popup(title="Load Image",content=content,size_hint=(.9,.9))
        self._popup.open()
    def Analysis(self):
        import os
        if (self.SensePath==None):
            print("Pleae Set Folder!")
            return
        
        cmd = 'copy '+self.SensePath+'\\'+"CmpData.csv" + ' ex3_tmo_cmp_data.csv'
        print(cmd)
        os.system(cmd)
        os.system('.\ex3_tmo_cmp_step1_scale.exe')
        os.system('.\plot.exe')
        cmd = 'copy '+'ex3_tmo_cmp_scaled.csv '+self.SensePath+'\\'+"result.csv"
        print(cmd)
        os.system(cmd)
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
    def show_nextPairImgs(self):
        PairNum = len(self.ImagePathList)
        if (self.ObserverName==0):
            print("Please Enter your name")
            self.EnterObserverName()
            return
        if (PairNum==0):
            self.GetImgPathList()
            print("Load Image Pairs\n")
            PairNum = len(self.ImagePathList)
            if (PairNum==0):
                print("Pleae select folder or load a pairlist")
        if (self.imgpairIndex>=PairNum):
            print("Out Of index")
            return

        if (self.PreOrNext == 0):
            self.imgpairIndex = self.imgpairIndex + 2
       # if (self.PreOrNext == 0 and self.imgpairIndex>0):
        #    self.imgpairIndex = self.imgpairIndex + 2
        #elif (self.PreOrNext == 0 and self.imgpairIndex==0):
        #    self.imgpairIndex = self.imgpairIndex + 1
        df = pd.read_csv('Senses/CmpData.csv')
        df1 = pd.read_csv('Senses/CmpPair.csv')
        df1 = df1.drop('Unnamed: 0',axis = 1) 
        if (self.imgpairIndex>=0 and self.imgpairIndex<PairNum): 
            
                
            self.img1 = cv_imread(self.ImagePathList[self.imgpairIndex][0])
            self.img2 = cv_imread(self.ImagePathList[self.imgpairIndex][1])
            img1 = self.img1
            img2 = self.img2
            if (self.JugeCmpPairIsSelected() == 0):
                img1=cv2.rectangle(img1,(50,50),(int(img1.shape[0]/5),int(img1.shape[0]/5)),(0,0,255),20)
            if (self.JugeCmpPairIsSelected() == 1):
                img2=cv2.rectangle(img2,(50,50),(int(img1.shape[0]/5),int(img1.shape[0]/5)),(0,0,255),20)
            img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGBA)
            img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGBA)
            img1 = cv2.flip(img1, 0) # 旋转
            img2 = cv2.flip(img2, 0) # 旋转

            kivy_showcvimg(img1,self.ids.img_det)
            kivy_showcvimg(img2,self.ids.img_det1)
            self.labelWidget.text = str(self.imgpairIndex+1)+'/'+str(PairNum)
            self.imgpairIndex = self.imgpairIndex + 1
            self.imgpairIndex_Cur = self.imgpairIndex -1
            self.PreOrNext = 1

    def show_prePairImgs(self):
        print(self.imgpairIndex)
        if (self.ObserverName==0):
            print("Please Enter your name")
            self.EnterObserverName()
            return
        if (len(self.ImagePathList)==0):
            self.GetImgPathList()
            
            
        if (self.PreOrNext == 1):
            if(self.imgpairIndex>=0):
                self.imgpairIndex = self.imgpairIndex - 2
        '''if (self.PreOrNext == 1 and self.imgpairIndex<len(self.ImagePathList)):
            self.imgpairIndex = self.imgpairIndex - 2
        elif (self.PreOrNext == 1 and self.imgpairIndex==len(self.ImagePathList)):
            self.imgpairIndex = self.imgpairIndex - 1'''
        if (self.imgpairIndex>=0 and self.imgpairIndex<len(self.ImagePathList)):
            self.img1 = cv_imread(self.ImagePathList[self.imgpairIndex][0])
            self.img2 = cv_imread(self.ImagePathList[self.imgpairIndex][1])
            img1 = self.img1
            img2 = self.img2
            if (self.JugeCmpPairIsSelected() == 0):
                img1=cv2.rectangle(img1,(50,50),(int(img1.shape[0]/5),int(img1.shape[0]/5)),(0,0,255),20)
            if (self.JugeCmpPairIsSelected() == 1):
                img2=cv2.rectangle(img2,(50,50),(int(img1.shape[0]/5),int(img1.shape[0]/5)),(0,0,255),20)
            img1 = cv2.cvtColor(img1, cv2.COLOR_BGR2RGBA)
            img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGBA)
            img1 = cv2.flip(img1, 0) # 旋转
            img2 = cv2.flip(img2, 0) # 旋转
            

            kivy_showcvimg(img1,self.ids.img_det)
            kivy_showcvimg(img2,self.ids.img_det1)  
            self.labelWidget.text = str(self.imgpairIndex + 1)+'/'+str(len(self.ImagePathList))
            if(self.imgpairIndex==0):
                print("第一张了")
            if(self.imgpairIndex>=0):
                self.imgpairIndex = self.imgpairIndex - 1
                self.imgpairIndex_Cur = self.imgpairIndex +1
            self.PreOrNext = 0

    def GetImgPathList(self):
        if (self.SensePath == None): 
            print("Please Set your workPath")
            return
        fullpath = self.SensePath + '/'+'CmpPair.csv'
        if(os.path.exists(fullpath)==False):
            return self.ImagePathList
        df = pd.read_csv(fullpath)
        #df = df.drop('Unnamed: 0',axis = 1) 
        #print(df)
        self.imgpairIndex = 0
        for i,id in enumerate(df.SenseName.values):
            self.ImagePathList.append([df.Path1.values[i],df.Path2.values[i]])
        for i,id in enumerate(df.SenseName.values):
            self.SenceList.append(df.SenseName.values[i])
            self.Condition_1list.append(df.Condition1.values[i])
            self.Condition_2list.append(df.Condition2.values[i])
        self.SenceNames=df.SenseName.drop_duplicates().values
        
        #self.ComPairSelet = df.selection.values
        '''cmppairSelet = df.selection.values[self.imgpairIndex]
        li = cmppairSelet.split(',')
        if li[0]=='no':
            return self.ImagePathList
        reslist = np.argwhere(self.ObserverName not in li)
        print(len(reslist),reslist)
        if(len(reslist)>0 ):
            self.imgpairIndex = reslist[0][0] #
        else:
            print("您已经完成测试")'''
        #reslist = np.argwhere(self.ObserverName not in li)
        #if(len(reslist)==0):
         #   print("您已经完成测试")
        #print(self.SenceList,self.SenceNames,self.Condition_1list,self.Condition_2list)
        return self.ImagePathList
        
class LabelBoxLayout(BoxLayout):
    def __init__(self,**kwargs):
        super(LabelBoxLayout, self).__init__(**kwargs)
        #设置引用时，markup属性必须设置为真（True、1）
        #将Label文本标记，单击Lable文本时会触发绑定的事件，单击hello文本则不会
        label_ref=Label(text='你好[ref=label]Label[/ref]',markup=True,color=(.9,.2,.1,1))
        label_ref.bind(on_ref_press=self.print_it)
        self.add_widget(label_ref)
    @staticmethod
    def print_it(*args):
        print('print_it已经运行')
        
class LaneDetectApp(App):
    def build(self):
        Window.fullscreen=0
        Window.size=(1000,400)
        self.icon = "./static/icon.ico" 
        self.title = "主观指标客观评价App"
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