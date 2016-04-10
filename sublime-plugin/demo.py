# 记录光标
# 选中效果
# 时间函数
# from .Edit import Edit as Edit

debug = 0
ctrlz = 0

size = 0
x = 0
y = 0

import sublime, sublime_plugin, time
import urllib
# ip = "http://121.201.7.39"
ip = "http://0.0.0.0:5000"
def post(timestamp, command):
	data = {'timestamp':str(timestamp), 'command':str(command)}
	f = urllib.request.urlopen(url = ip, data = urllib.parse.urlencode(data).encode("ascii"))
	print('ok')
	if f.read() != b'ok':
		print("opps!")
		post(timestamp, command)

class My_undoCommand(sublime_plugin.WindowCommand):
	def run(self):
		if debug:
			print(11)
		global ctrlz
		ctrlz = 1
		self.window.run_command('undo')

class My_redoCommand(sublime_plugin.WindowCommand):
	def run(self):
		if debug:
			print(22)
		global ctrlz
		ctrlz = 1
		self.window.run_command('redo')


class ExampleCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		global size, x, y, ctrlz
		# print(self.view.sel())
		# print(self.view.size())

		region = self.view.sel()[0]
		if debug:
			print("#", region.a, region.b) 
		if ctrlz == 0:
			if x == y:
				# x = region.a
				# y = region.b
				if size < self.view.size():
					if debug:
						print(x, y,
							self.view.substr(sublime.Region(x, x + self.view.size() - size)), time.time())
					post(time.time(),str(x) + ' ' +str(y) + ' ' +
							self.view.substr(sublime.Region(x, x + self.view.size() - size)))
					# print(time.time())
				# 反着删除的情况？ Ins
				elif size > self.view.size():
					if debug:
						print(x, x + self.view.size() - size, "")
					post(time.time(),str(x+ self.view.size() - size) + ' ' + str(x)+" ")

			else:
				left = min(x, y)
				right = max(x, y)
				if debug:
					print(left, right, "", time.time())
				post(time.time(), str(left) + ' '+str(right) +' ')
		else:
			# caution! 
			if debug:
				print("@@@")
			len = size - self.view.size()
			if len < 0:
				if debug:
					print(x+len, x+len, self.view.substr(sublime.Region(x + len, x)), time.time())
				post(time.time(), str(x+len) + ' ' +str(x+len) + ' ' + str(self.view.substr(sublime.Region(x + len, x))))
			else:
				if debug:
					print(x, x+len, "", time.time())
				post(time.time(),str(x) + ' ' + str(x+len)+ ' ')
			ctrlz = 0;

		'''
		print(region.a, region.b) 
		if size < self.view.size():
			print("insert",
				region.b-(self.view.size() - size),
				self.view.substr(sublime.Region(region.b-(self.view.size() - size), region.b)))
		elif size > self.view.size():
			print("delete",
				self.view.substr(sublime.Region(region.b-(self.view.size() - size), region.b)))
		'''
		if debug:
			print("#", region.a, region.b) 
		x = region.a
		y = region.b
		size = self.view.size()
		# for region in self.view.sel():
		# 	print(region)
		# 	print(self.view.substr(sublime.Region(region.a-1, region.b)))  
		# print(self.view.change_count())
		# print(self.view.substr(sublime.Region(0, self.view.size())))


class Example1Command(sublime_plugin.TextCommand):
	def run(self, edit):
		region = self.view.sel()[0]
		global x, y
		x = region.a
		y = region.b
		if debug:
			print("@", region.a, region.b) 

class KeyBindingListener(sublime_plugin.EventListener):
    # def on_window_command(self, window, name, args):
    #     print("The window command name is: " + name)
    #     print("The are: " + str(args))

    def on_modified(self, view):
    	view.run_command('example') 
    	# print(1)a 

    def on_selection_modified(self, view):
    	view.run_command('example1') 

