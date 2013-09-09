from kivy.app import App
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse, Line
from kivy.config import Config
from kivy.logger import Logger
from random import randint

class PaintWidget(Widget):


	def initiate(self):
		pass


	def on_touch_down(self, touch):
		with self.canvas:
			touch.ud['cr'] = randint(1, 10)/10.0
			touch.ud['cg'] = randint(1, 10)/10.0
			touch.ud['cb'] = randint(1, 10)/10.0

			if 'pos3d' not in touch.profile:
				touch.ud['line'] = Line(points=(touch.x, touch.y))
			if 'pos3d' in touch.profile:
				Color(1,1,1)
				touch.ud['outer_cursor'] = Ellipse(pos=(touch.x - 10, touch.y - 10), size=(20,20))
				Color(touch.ud['cr'], touch.ud['cg'], touch.ud['cb'])
				touch.ud['cursor'] = Ellipse(pos=(touch.x, touch.y), size=(1,1))
				touch.ud['drawn'] = False

	def on_touch_move(self, touch):

		if 'pos3d' not in touch.profile:
			touch.ud['line'].points += [touch.x, touch.y]
		if 'pos3d' in touch.profile:
			#if touch.z > 40 and touch.ud['drawn'] == True:
	

			cursor_size = 20.0-touch.z/13.0
			if cursor_size > 20:
				cursor_size = 20
			touch.ud['outer_cursor'].pos = (touch.x - 10, touch.y - 10)
			touch.ud['cursor'].size = (cursor_size, cursor_size)
			touch.ud['cursor'].pos = (touch.x - cursor_size/2, touch.y - cursor_size/2)
			if touch.z <= 0:
				try:
					touch.ud['line'].points += [touch.x, touch.y]
				except KeyError:
					with self.canvas:
						Color(touch.ud['cr'], touch.ud['cg'], touch.ud['cb'])
						touch.ud['line'] = Line(points=(touch.x, touch.y), width=5)
						touch.ud['drawn'] = True
			#touch.ud['line'].width = abs((300-touch.z)/50)

	def on_touch_up(self, touch):
		#print 'touchup'
		if 'pos3d' in touch.profile:
			self.canvas.remove(touch.ud['cursor'])
			self.canvas.remove(touch.ud['outer_cursor'])


class PaintApp(App):
	def build(self):
		wid = PaintWidget()
		wid.initiate()
		return wid

if __name__ == '__main__':
	PaintApp().run()