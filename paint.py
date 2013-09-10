from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line
from random import randint
from kivy.core.window import Window
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.properties import NumericProperty

r = NumericProperty(0.5)
g = 0.5
b = 0.5
a = 1
line = 10
manager = ScreenManager()

class PaintScreen(Screen):
	pass

class ColorScreen(Screen):
	pass

class StrokeScreen(Screen):
	pass

class MenuScreen(Screen):
	pass

class MainMenuWidget(Widget):
	pass

class StrokePickerWidget(Widget):
	pass

class ColorPickerWidget(Widget):
	
	def set_color(self, sr, sg, sb, sa):
		print r
		


class MenuWidget(Widget):

	def init_menu(self):

		pass


class CursorWidget(Widget):

	def on_touch_down(self, touch):
		pass

	def on_touch_move(self, touch):
		if 'pos3d' in touch.profile:
			n = 256/line*2
			cursor_size = line*2-touch.z/n*2
			if cursor_size > line*2:
				cursor_size = line*2
			try:
				touch.ud['outer_cursor'].pos = (touch.x - line, touch.y - line)
				touch.ud['cursor'].size = (cursor_size, cursor_size)
				touch.ud['cursor'].pos = (touch.x - cursor_size/2, touch.y - cursor_size/2)
			except KeyError:
				with self.canvas:
					Color(1,1,1,1)
					touch.ud['outer_cursor'] = Ellipse(pos=(touch.x - line, touch.y - line), size=(line*2,line*2))
					Color(r, g, b, a)
					touch.ud['cursor'] = Ellipse(pos=(touch.x, touch.y), size=(1,1))

	def on_touch_up(self, touch):
		#print 'touchup'
		if 'pos3d' in touch.profile:
			try:
				self.canvas.remove(touch.ud['cursor'])
				self.canvas.remove(touch.ud['outer_cursor'])
			except:
				pass
			#Window.screenshot(name='screenshot%(counter)04d.jpg')


class PaintWidget(Widget):


	def on_touch_down(self, touch):
		with self.canvas:

			if 'pos3d' not in touch.profile:
				touch.ud['line'] = Line(points=(touch.x, touch.y))
			if 'pos3d' in touch.profile:
				touch.ud['drawn'] = False

	def on_touch_move(self, touch):
		if 'pos3d' not in touch.profile:
			touch.ud['line'].points += [touch.x, touch.y]
		if 'pos3d' in touch.profile:
			#if touch.z > 40 and touch.ud['drawn'] == True:

			if touch.z <= 0:
				try:
					touch.ud['line'].points += [touch.x, touch.y]
				except KeyError:
					with self.canvas:
						Color(r, g, b, a)
						touch.ud['line'] = Line(points=(touch.x, touch.y), width=line)
						touch.ud['drawn'] = True
			#touch.ud['line'].width = abs((300-touch.z)/50)



class PaintApp(App):
	def build(self):
		self.manager = manager
		self.win = Window
		self.r = r

		

		paint_screen = PaintScreen(name='paint screen')
		paint = PaintWidget()
		menu = MenuWidget()
		menu.init_menu()
		paint_screen.add_widget(paint)
		paint_screen.add_widget(menu)
		paint_screen.add_widget(CursorWidget())
		manager.add_widget(paint_screen)
		mainmenu = MainMenuWidget()
		menu_screen = MenuScreen(name='menu screen')
		menu_screen.add_widget(CursorWidget())
		menu_screen.add_widget(mainmenu)
		colorpicker = ColorPickerWidget()
		strokepicker = StrokePickerWidget()
		color_screen = ColorScreen(name='color screen')
		color_screen.add_widget(CursorWidget())
		color_screen.add_widget(colorpicker)
		stroke_screen = StrokeScreen(name='stroke screen')
		stroke_screen.add_widget(CursorWidget())
		stroke_screen.add_widget(strokepicker)
		manager.add_widget(menu_screen)
		manager.add_widget(color_screen)
		manager.add_widget(stroke_screen)
		
		return manager

if __name__ == '__main__':
	PaintApp().run()