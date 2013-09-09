from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line
from kivy.config import Config
from kivy.logger import Logger
from random import randint
from kivy.core.window import Window
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button

r = randint(1, 10)/10.0
g = randint(1, 10)/10.0
b = randint(1, 10)/10.0
a = 1
line = 10

class RootWidget(Widget):
	pass

class MenuWidget(Widget):

	def init_menu(self):
		#todo: make it that even when the window is resized
		self.width = Window.width
		self.height = Window.height

class CursorWidget(Widget):

	def on_touch_down(self, touch):
		if 'pos3d' in touch.profile:
			with self.canvas:
				Color(1,1,1,1)
				touch.ud['outer_cursor'] = Ellipse(pos=(touch.x - line, touch.y - line), size=(line*2,line*2))
				Color(r, g, b, a)
				touch.ud['cursor'] = Ellipse(pos=(touch.x, touch.y), size=(1,1))

	def on_touch_move(self, touch):
		if 'pos3d' in touch.profile:
			n = 256/line*2
			cursor_size = line*2-touch.z/n*2
			if cursor_size > line*2:
				cursor_size = line*2
			touch.ud['outer_cursor'].pos = (touch.x - line, touch.y - line)
			touch.ud['cursor'].size = (cursor_size, cursor_size)
			touch.ud['cursor'].pos = (touch.x - cursor_size/2, touch.y - cursor_size/2)

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
		wid = RootWidget()
		cursor = CursorWidget()
		paint = PaintWidget()
		menu = MenuWidget()
		menu.init_menu()

		wid.add_widget(paint)
		wid.add_widget(menu)
		wid.add_widget(cursor)
		return wid

if __name__ == '__main__':
	PaintApp().run()