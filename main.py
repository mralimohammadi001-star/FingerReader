from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView 
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.spinner import Spinner
from backend.records import Records
import jdatetime
from kivy.uix.screenmanager import ScreenManager, Screen

class ReportLayout(ScrollView):
    def __init__(self ,**kwargs):
        super().__init__(**kwargs)
        self.records = {}
        self.bar_width = 15
        self.bar_color = [.1 ,.5 ,1 ,1]
        self.scroll_type = ['bars' ,'content']

    def recive_rec(self ,records):
        self.root_box = BoxLayout(orientation='vertical' ,size_hint_y=None)
        return_btn = Button(text='Return to Filters' ,size_hint_y=None ,font_size=64 ,background_color=[.5 ,.75 ,.25 ,1])
        return_btn.bind(on_press=self.su_enter)
        self.root_box.add_widget(return_btn)
        self.records = records.group_by_day()

        for recs ,date ,index in zip(self.records.values() ,self.records.keys() ,range(len(self.records.keys()))):
            box = BoxLayout(orientation='vertical' ,size_hint_y=None)
            box.add_widget(Label(text=f'[b]{str(date)}[/b]' ,font_size=40 ,size_hint_y=None ,markup=True))
            for rec in recs :
                in_box = BoxLayout(orientation='horizontal' ,size_hint_y=None)
                in_box.add_widget(Label(text=rec.person ,font_size=24 ,size_hint=[0.25 ,None]))
                in_box.add_widget(Label(text=str(rec.date_time.time()) ,font_size=24 ,size_hint=[0.5 ,None]))
                if rec.movement == 'login' :
                    in_box.add_widget(Label(text=rec.movement ,font_size=24 ,size_hint=[0.25 ,None] ,color=[0.1 ,.3 ,.9 ,1]))
                else:
                    in_box.add_widget(Label(text=rec.movement ,font_size=24 ,size_hint=[0.25 ,None] ,color=[0.9 ,.3 ,0.1 ,1]))
                box.add_widget(in_box)
            box.height = sum([child.height for child in box.children])
            self.root_box.add_widget(box)
        
        self.root_box.bind(minimum_height=self.root_box.setter('height'))
        self.add_widget(self.root_box)

    def su_enter(self ,instance):
        self.remove_widget(self.root_box)
        kivy.sm.current = 'enter'
        self.records = {}

class EnterLayout(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        mybox = BoxLayout(orientation='vertical' ,size_hint_y=None)
        self.widgets = [None] * 36
        boxes = [None] * 13
        self.rec = None

        self.widgets[0] = CheckBox(size_hint_y=None ,height=32 ,size_hint_x=0.1)
        self.widgets[0].bind(active=self.call_back)
        self.widgets[1] = Label(size_hint_x=0.37 ,text='Enter records path' ,font_size=17 ,size_hint_y=None ,height=32 ,disabled=True)
        self.widgets[2] = TextInput(hint_text='Records path' ,multiline=False ,font_size=17 ,size_hint_y=None ,height=32 ,disabled=True)

        self.widgets[3] = CheckBox(size_hint_y=None ,height=32 ,size_hint_x=0.1)
        self.widgets[3].bind(active=self.call_back)
        self.widgets[4] = Label(size_hint_x=0.37 ,text='Enter person code ' ,font_size=17 ,size_hint_y=None ,height=32 ,disabled=True)
        self.widgets[5] = TextInput(hint_text='Person code' ,multiline=False ,font_size=17 ,size_hint_y=None ,height=32 ,disabled=True)

        self.widgets[6] = CheckBox(size_hint_y=None ,height=32 ,size_hint_x=0.1)
        self.widgets[6].bind(active=self.call_back)
        self.widgets[7] = Label(size_hint_x=0.37 ,text='Enter persons movement' ,font_size=17 ,size_hint_y=None ,height=32 ,disabled=True)
        self.widgets[8] = Spinner(text='Click!' ,values=['login' ,'logout'],font_size=17 ,size_hint_y=None ,height=32 ,disabled=True)

        self.widgets[9] = CheckBox(size_hint_y=None ,height=32 ,size_hint_x=0.05 ,group='filter')
        self.widgets[9].bind(active=self.call_back)
        self.widgets[10] = Label(size_hint_x=0.3 ,markup=True ,text='[b]Quick datetime filters[/b]' ,font_size=24 ,size_hint_y=None ,height=32)

        self.widgets[11] = CheckBox(size_hint_y=None ,height=32 ,size_hint_x=0.05 ,group='quick filter' ,disabled=True)
        self.widgets[11].bind(active=self.call_back)
        self.widgets[12] = Label(size_hint_x=0.3 ,text='Today' ,font_size=22 ,size_hint_y=None ,height=32 ,disabled=True)

        self.widgets[13] = CheckBox(size_hint_y=None ,height=32 ,size_hint_x=0.05 ,group='quick filter' ,disabled=True)
        self.widgets[13].bind(active=self.call_back)
        self.widgets[14] = Label(size_hint_x=0.3 ,text='This Week' ,font_size=18 ,size_hint_y=None ,height=32 ,disabled=True)

        self.widgets[15] = CheckBox(size_hint_y=None ,height=32 ,size_hint_x=0.05 ,group='quick filter' ,disabled=True)
        self.widgets[15].bind(active=self.call_back)
        self.widgets[16] = Label(size_hint_x=0.3 ,text='This Month' ,font_size=18 ,size_hint_y=None ,height=32 ,disabled=True)

        self.widgets[17] = CheckBox(size_hint_y=None ,height=32 ,size_hint_x=0.05 ,group='quick filter' ,disabled=True)
        self.widgets[17].bind(active=self.call_back)
        self.widgets[18] = Label(size_hint_x=0.3 ,text='Last Week' ,font_size=18 ,size_hint_y=None ,height=32 ,disabled=True)

        self.widgets[19] = CheckBox(size_hint_y=None ,height=32 ,size_hint_x=0.05 ,group='quick filter' ,disabled=True)
        self.widgets[19].bind(active=self.call_back)
        self.widgets[20] = Label(size_hint_x=0.3 ,text='Last Month' ,font_size=18 ,size_hint_y=None ,height=32 ,disabled=True)

        self.widgets[21] = CheckBox(size_hint_y=None ,height=32 ,size_hint_x=0.05 ,group='filter')
        self.widgets[21].bind(active=self.call_back)
        self.widgets[22] = Label(size_hint_x=0.3 ,markup=True ,text='[b]Custom datetime filter[/b]' ,font_size=24 ,size_hint_y=None ,height=32)

        self.widgets[23] = Label(size_hint_x=0.2 ,text='From Date' ,font_size=18 ,size_hint_y=None ,height=32 ,disabled=True)
        self.widgets[24] = TextInput(hint_text='YYYY-mm-dd' ,multiline=False ,font_size=17 ,size_hint=(.3 ,None) ,height=32 ,disabled=True)
        self.widgets[25] = CheckBox(size_hint_y=None ,height=32 ,size_hint_x=0.05 ,disabled=True)
        self.widgets[25].bind(active=self.call_back)
        self.widgets[26] = Label(size_hint_x=0.2 ,text=' - Time' ,font_size=18 ,size_hint_y=None ,height=32 ,disabled=True)
        self.widgets[27] = TextInput(hint_text='HH:MM:SS' ,multiline=False ,font_size=17 ,size_hint=(.3 ,None) ,height=32 ,disabled=True)

        self.widgets[28] = Label(size_hint_x=0.2 ,text='To Date' ,font_size=18 ,size_hint_y=None ,height=32 ,disabled=True)
        self.widgets[29] = TextInput(hint_text='YYYY-mm-dd' ,multiline=False ,font_size=17 ,size_hint=(.3 ,None) ,height=32 ,disabled=True)
        self.widgets[30] = CheckBox(size_hint_y=None ,height=32 ,size_hint_x=0.05 ,disabled=True)
        self.widgets[30].bind(active=self.call_back)
        self.widgets[31] = Label(size_hint_x=0.2 ,text=' - Time' ,font_size=18 ,size_hint_y=None ,height=32 ,disabled=True)
        self.widgets[32] = TextInput(hint_text='HH:MM:SS' ,multiline=False ,font_size=17 ,size_hint=(.3 ,None) ,height=32 ,disabled=True)

        self.widgets[33] = Button(text='submit' ,size_hint=(1 ,None) ,height = 32)
        self.widgets[33].bind(on_press=self.submit)
        self.widgets[34] = CheckBox(size_hint_y=None ,height=32 ,size_hint_x=0.05 ,active=True)
        self.widgets[35] = Label(size_hint_x=0.2 ,text='Insert names' ,font_size=18 ,size_hint_y=None ,height=32)

        boxes[0] = GridLayout(cols=3,size_hint_y=None ,spacing=13 ,padding=[13 ,5 ,13 ,5])
        boxes[0].add_widget(self.widgets[0])
        boxes[0].add_widget(self.widgets[1])
        boxes[0].add_widget(self.widgets[2])
        boxes[0].height = max([child.height for child in boxes[0].children]) + 13

        boxes[1] = GridLayout(cols=3,size_hint_y=None ,spacing=13 ,padding=[13 ,5 ,13 ,5])
        boxes[1].add_widget(self.widgets[3])
        boxes[1].add_widget(self.widgets[4])
        boxes[1].add_widget(self.widgets[5])
        boxes[1].height = max([child.height for child in boxes[1].children]) + 13

        boxes[2] = GridLayout(cols=3,size_hint_y=None ,spacing=13 ,padding=[13 ,5 ,13 ,5])
        boxes[2].add_widget(self.widgets[6])
        boxes[2].add_widget(self.widgets[7])
        boxes[2].add_widget(self.widgets[8])
        boxes[2].height = max([child.height for child in boxes[2].children]) + 13

        boxes[3] = GridLayout(cols=2 ,size_hint=(.4 ,None) ,padding=[20] * 4 ,spacing=20)
        boxes[3].add_widget(self.widgets[9])
        boxes[3].add_widget(self.widgets[10])
        boxes[3].height = max([child.height for child in boxes[3].children]) + 13

        boxes[4] = GridLayout(cols=2 ,size_hint=(.25 ,None) ,padding=[60 ,5 ,20 ,5] ,spacing=13)
        boxes[4].add_widget(self.widgets[11])
        boxes[4].add_widget(self.widgets[12])
        boxes[4].height = max([child.height for child in boxes[4].children]) + 13

        boxes[5] = GridLayout(cols=2 ,size_hint=(.25 ,None) ,padding=[60 ,5 ,20 ,5] ,spacing=13)
        boxes[5].add_widget(self.widgets[13])
        boxes[5].add_widget(self.widgets[14])
        boxes[5].height = max([child.height for child in boxes[5].children]) + 13

        boxes[6] = GridLayout(cols=2 ,size_hint=(.25 ,None) ,padding=[60 ,5 ,20 ,5] ,spacing=13)
        boxes[6].add_widget(self.widgets[15])
        boxes[6].add_widget(self.widgets[16])
        boxes[6].height = max([child.height for child in boxes[6].children]) + 13

        boxes[7] = GridLayout(cols=2 ,size_hint=(.25 ,None) ,padding=[60 ,5 ,20 ,5] ,spacing=13)
        boxes[7].add_widget(self.widgets[17])
        boxes[7].add_widget(self.widgets[18])
        boxes[7].height = max([child.height for child in boxes[7].children]) + 13

        boxes[8] = GridLayout(cols=2 ,size_hint=(.25 ,None) ,padding=[60 ,5 ,20 ,5] ,spacing=13)
        boxes[8].add_widget(self.widgets[19])
        boxes[8].add_widget(self.widgets[20])
        boxes[8].height = max([child.height for child in boxes[8].children]) + 13

        boxes[9] = GridLayout(cols=2 ,size_hint=(.4 ,None) ,padding=[20] * 4 ,spacing=20)
        boxes[9].add_widget(self.widgets[21])
        boxes[9].add_widget(self.widgets[22])
        boxes[9].height = max([child.height for child in boxes[9].children]) + 13

        boxes[10] = GridLayout(cols=5 ,size_hint=(1 ,None) ,padding=[60 ,5 ,20 ,5] ,spacing=5)
        boxes[10].add_widget(self.widgets[23])
        boxes[10].add_widget(self.widgets[24])
        boxes[10].add_widget(self.widgets[25])
        boxes[10].add_widget(self.widgets[26])
        boxes[10].add_widget(self.widgets[27])
        boxes[10].height = max([child.height for child in boxes[10].children]) + 13

        boxes[11] = GridLayout(cols=5 ,size_hint=(1 ,None) ,padding=[60 ,5 ,20 ,5] ,spacing=5)
        boxes[11].add_widget(self.widgets[28])
        boxes[11].add_widget(self.widgets[29])
        boxes[11].add_widget(self.widgets[30])
        boxes[11].add_widget(self.widgets[31])
        boxes[11].add_widget(self.widgets[32])
        boxes[11].height = max([child.height for child in boxes[11].children]) + 13

        boxes[12] = BoxLayout(size_hint=(1 ,None) ,padding=[60 ,5 ,20 ,5] ,spacing=5)
        boxes[12].add_widget(self.widgets[33])
        boxes[12].add_widget(self.widgets[34])
        boxes[12].add_widget(self.widgets[35])
        boxes[12].height = max([child.height for child in boxes[12].children]) + 13


        for box in boxes:
            mybox.add_widget(box)
        mybox.height = mybox.minimum_height

        mybox.bind(minimum_height=mybox.setter('height'))
        self.add_widget(mybox)
        self.height = max([child.height for child in self.children])

    def call_back(self ,instanse ,value):
        if instanse == self.widgets[0] :
            if value :
                self.widgets[1].disabled = False
                self.widgets[2].disabled = False
            else :
                self.widgets[1].disabled = True
                self.widgets[2].disabled = True
                self.widgets[2].text = ''

        if instanse == self.widgets[3] :
            if value :
                self.widgets[4].disabled = False
                self.widgets[5].disabled = False
            else :
                self.widgets[4].disabled = True
                self.widgets[5].disabled = True
                self.widgets[5].text = ''

        if instanse == self.widgets[6] :
            if value :
                self.widgets[7].disabled = False
                self.widgets[8].disabled = False
            else :
                self.widgets[7].disabled = True
                self.widgets[8].disabled = True
                self.widgets[8].text = 'Click!'

        if instanse == self.widgets[9] :
            if value :
                self.widgets[11].disabled = False
                self.widgets[12].disabled = False
                self.widgets[13].disabled = False
                self.widgets[14].disabled = False
                self.widgets[15].disabled = False
                self.widgets[16].disabled = False
                self.widgets[17].disabled = False
                self.widgets[18].disabled = False
                self.widgets[19].disabled = False
                self.widgets[20].disabled = False
            else :
                self.widgets[11].disabled = True
                self.widgets[11].active = False
                self.widgets[12].disabled = True
                self.widgets[13].disabled = True
                self.widgets[13].active = False
                self.widgets[14].disabled = True
                self.widgets[15].disabled = True
                self.widgets[15].active = False
                self.widgets[16].disabled = True
                self.widgets[17].disabled = True
                self.widgets[17].active = False
                self.widgets[18].disabled = True
                self.widgets[19].disabled = True
                self.widgets[19].active = False
                self.widgets[20].disabled = True


        if instanse == self.widgets[11] :
            if value :
                self.widgets[12].disabled = False
            else :
                self.widgets[12].disabled = True
        
        if instanse == self.widgets[13] :
            if value :
                self.widgets[14].disabled = False
            else :
                self.widgets[14].disabled = True

        if instanse == self.widgets[15] :
            if value :
                self.widgets[16].disabled = False
            else :
                self.widgets[16].disabled = True

        if instanse == self.widgets[17] :
            if value :
                self.widgets[18].disabled = False
            else :
                self.widgets[18].disabled = True

        if instanse == self.widgets[19] :
            if value :
                self.widgets[20].disabled = False
            else :
                self.widgets[20].disabled = True

        if instanse == self.widgets[21] :
            if value :
                self.widgets[23].disabled = False
                self.widgets[24].disabled = False
                self.widgets[25].disabled = False
                self.widgets[28].disabled = False
                self.widgets[29].disabled = False
                self.widgets[30].disabled = False
            else :
                self.widgets[23].disabled = True
                self.widgets[24].disabled = True
                self.widgets[25].disabled = True
                self.widgets[25].active = False
                self.widgets[28].disabled = True
                self.widgets[29].disabled = True
                self.widgets[30].disabled = True
                self.widgets[30].active = False

        if instanse == self.widgets[25] :
            if value :
                self.widgets[26].disabled = False
                self.widgets[27].disabled = False
            else :
                self.widgets[26].disabled = True
                self.widgets[27].disabled = True
                self.widgets[27].text = ''
        
        if instanse == self.widgets[30] :
            if value :
                self.widgets[31].disabled = False
                self.widgets[32].disabled = False
            else :
                self.widgets[31].disabled = True
                self.widgets[32].disabled = True
                self.widgets[32].text = ''

    def submit(self ,instanse) :
        self.rec = Records([])

        if self.widgets[0].active :
            if self.rec.read(str(self.widgets[2].text)) :
                self.widgets[33].text = 'Invalid file location'
                return
            self.widgets[33].text = 'submit'
        else :
            if self.rec.read('data/1_attlog.dat') :
                self.widgets[33].text = 'data/1_attlog.dat Not found'
                return
            self.widgets[33].text = 'submit'
        
        try:
            if self.widgets[3].active :
                self.rec = self.rec.by_person(str(self.widgets[5].text))
                self.widgets[33].text = 'submit'
        except Exception as e :
            self.widgets[33].text = 'Invalid person code'
            return

        if self.widgets[6].active :
            self.rec = self.rec.by_movement(str(self.widgets[8].text))
        
        if self.widgets[11].active :
            self.rec = self.rec.by_today()

        if self.widgets[13].active :
            self.rec = self.rec.by_this_week()

        if self.widgets[15].active :
            self.rec = self.rec.by_this_month()

        if self.widgets[17].active :
            self.rec = self.rec.by_last_week()

        if self.widgets[19].active :
            self.rec = self.rec.by_last_month()


        if self.widgets[21].active :
            try :
                if self.widgets[25].active :
                    datetime_str = f'{self.widgets[24].text} {self.widgets[27].text}'
                    from_datetime = jdatetime.datetime.strptime(datetime_str ,'%Y-%m-%d %H:%M:%S')
                else :
                    from_datetime = jdatetime.datetime.strptime(self.widgets[24].text ,'%Y-%m-%d').replace(hour=0 ,minute=0 ,second=0)

                if self.widgets[30].active :
                    datetime_str = f'{self.widgets[29].text} {self.widgets[32].text}'
                    to_datetime = jdatetime.datetime.strptime(datetime_str ,'%Y-%m-%d %H:%M:%S')
                else:
                    to_datetime = jdatetime.datetime.strptime(self.widgets[29].text ,'%Y-%m-%d').replace(hour=23 ,minute=59 ,second=59)

                self.widgets[33].text = 'submit'
            except Exception as erorr :
                self.widgets[33].text = 'Invalid date / time'
                return

            self.rec = self.rec.by_datetime(from_datetime ,to_datetime)
        
        try :
            if self.widgets[34].active :
                self.rec = self.rec.get_names('data/persons.json')
                self.widgets[33].text = 'submit'
        except Exception as e :
            self.widgets[33].text = 'data/persons.json Not found'
            return
        kivy.get_report(self.rec)
        

class Report(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = ReportLayout()
        self.add_widget(self.layout)

    def recive(self ,records):
        self.layout.recive_rec(records=records)

class Enter(Screen):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.layout = EnterLayout()
        self.add_widget(self.layout)

class MyApp(App):
    def build(self):
        self.sm = ScreenManager()
        self.enter = Enter(name='enter')
        self.report = Report(name='report')
        self.sm.add_widget(self.enter)
        self.sm.add_widget(self.report)
        self.sm.current = 'enter'

        return self.sm

    def get_report(self ,records):
        self.report.recive(records)
        self.sm.current = 'report'

kivy = MyApp()
kivy.run()
