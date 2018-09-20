#!/usr/bin/python3
#-模拟系统的计算器功能
#-实现一个简单的可以进行加减法操作的计算器
#-使用Tkinter
#-操作步骤
	#-画GUI
	#-给每个控件配置相应的事件
	#-写逻辑代码

#第一步：画出图形界面上部分
from decimal import Decimal
from tkinter import *
root = Tk()
#定义面板的大小
root.geometry('300x380')
root.title('Johnnies Calculate')

#定义面板
frame_show = Frame(width = 500,height = 150,bg = '#dddddd' )	##dddddd是十六进制
frame_show.pack()

#定义顶部区域
sv = StringVar()
sv.set('0')#初始显示０

show_lable = Label(frame_show,textvariable = sv,bg = 'gray',width = 12,height = 1,\
	font = ('黑体',20,'bold'),justify = LEFT,anchor = 'e')
show_lable.pack(padx = 10,pady = 10)
#frame_show.pack()

#按键区域
def delete():
	global num1,num2,All
	if All != '':
		if All[-1].isdigit():
			if All == num1:
				num1 = num1[0:len(num1)-1]
			else :
				num2 = num2[0:len(num2)-1]
		All = All[0:len(All)-1]
		sv.set(All)

def clear():
	global num1,num2,operator,All
	num1 = ''
	num2 = ''
	operator = ''
	All = ''
	sv.set('0')

def fan():
	global num1,num2,operator,All
	if All != '':
		if All[-1].isdigit() and num2 == '':
			if All[0] == '-':
				num1 = str(abs(float(num1)))
				All = num1
			else :
				Num1 = float(num1)*(-1)
				num1 = str(Num1)
				All = num1
		elif All[-1].isdigit() and num2 != '':
			Num2 = float(num2)*(-1)
			All = All.replace(num2,str(Num2))
			num2 = str(Num2)
		else :
			pass
		sv.set(All)

def ce():
	sv.set('0')

frame_bord = Frame(width = 500,height = 350,bg = '#cccccc')
button_del = Button(frame_bord,text = '←',width = 3,height = 1,command = delete)
button_del.grid(row = 0,column = 0)

button_clear = Button(frame_bord,text = 'C',width = 3,height = 1,command = clear)
button_clear.grid(row = 0,column = 1)

button_fan = Button(frame_bord,text = '±',width = 3,height = 1,command = fan)
button_fan.grid(row = 0,column = 2)

button_ce = Button(frame_bord,text = 'CE',width = 3,height = 1,command = ce)
button_ce.grid(row = 0,column = 3)

'''
考虑一下几种情况：
	１、按下数字
	２、按下操作符
	３、只考虑两个操作数操作，不考虑发杂情况
'''
num1 = ''
num2 = ''
operator = ''
All = '' 

def change(num):
	'''
	按下一个数字需要考虑两种情况：
		１、数字属于第一个操作数
		２、数字属于第二个操作数
		３、判断书否属于第一个操作数，可以通过operator判断
	'''
	global num1,num2,operator,All
	#加入操作数是None，表明肯定是第一个操作数
	if operator == '=':
		if num != '.':
			operator = ''
			num1 = str(num)
			All = num1
			sv.set(All)
	elif operator == '':
		if num == '.' and num1 == '':
			pass
		elif num == '.' and '.' in num1:
			pass
		else :
			num1 = num1+str(num)
			All = All+str(num)
			#如果是第一个操作数，则显示第一个操作数
			sv.set(All)
	else :
		if num == '.' and num2 == '':
			pass
		elif num == '.' and '.' in num2:
			pass
		else :
			num2 = num2+str(num)
			All = All+str(num)
			#如果是第二个操作数，则应显示完整的计算式子
			sv.set(All)
#计算两个数之间的和
def res(s):
	if s[0] == '-':
		for i in s[1:len(s)]:
			if i in ['+','-','*','/']:
				op = i
				li = s.split(op)
				if s.count('-') == 3:
					Al = i+'Decimal(li[1])'+i+i+'Decimal(li[3])'
				elif s.count('-') == 2 and i == '-':
					Al = i+'Decimal(li[1])'+i+'Decimal(li[2])'
				else :
					Al = 'Decimal(li[0])'+i+'Decimal(li[1])'
				return(eval(Al))
				break
	else :
		for i in s:
			if i in ['+','-','*','/']:
				op = i
				li = s.split(op)
				if s.count('-') == 2:
					Al = 'Decimal(li[0])'+i+i+'Decimal(li[2])'
				else :
					Al = 'Decimal(li[0])'+i+'Decimal(li[1])'
				return(eval(Al))
				break

def operation(op):
	global num1,num2,operator,All
	if op == '-' and num1 == '':
		All = All+op
		sv.set(op)
		print(All)
	elif num1 != '' and All[-1].isdigit() and op in ['+','-','×','÷'] and num2 == '':
		operator = op
		All = All+op
		sv.set(All)
		print(All)
	elif op == '-' and All[-2].isdigit() and All[-1] in ['+','-','×','÷'] and num2 == '':
		operator = op
		All = All+op
		sv.set(All)
		print(All)
	elif num2 !='' and num2[-1].isdigit() and op in ['+','-','×','÷']:
		operator = op
		All = All.replace('×','*')
		All = All.replace('÷','/')
		num1 = str(eval("res(All)"))
		All = num1+operator
		sv.set(All)
		print(All)
		num2 = ''
	elif num2 !='' and num2[-1].isdigit() and op == '=':
		if operator != '=':
			operator = op
			All = All.replace('×','*')
			All = All.replace('÷','/')
			num1 = str(eval("res(All)"))
			All = num1
			sv.set(All)
			print(All)
			num2 = ''
	elif All == num1 and op == '=':
		sv.set(All)
		print(All)

#数字键
'''
def change(num):
	print(num)
'''
b_1 = Button(frame_bord,text = '1',width = 2,height = 1,command = lambda:change(1))
b_1.grid(row = 1,column = 0)

b_2 = Button(frame_bord,text = '2',width = 2,height = 1,command = lambda:change(2))
b_2.grid(row = 1,column = 1)

b_3 = Button(frame_bord,text = '3',width = 2,height = 1,command = lambda:change(3))
b_3.grid(row = 1,column = 2)

b_4 = Button(frame_bord,text = '4',width = 2,height = 1,command = lambda:change(4))
b_4.grid(row = 2,column = 0)

b_5 = Button(frame_bord,text = '5',width = 2,height = 1,command = lambda:change(5))
b_5.grid(row = 2,column = 1)

b_6 = Button(frame_bord,text = '6',width = 2,height = 1,command = lambda:change(6))
b_6.grid(row = 2,column = 2)

b_7 = Button(frame_bord,text = '7',width = 2,height = 1,command = lambda:change(7))
b_7.grid(row = 3,column = 0)

b_8 = Button(frame_bord,text = '8',width = 2,height = 1,command = lambda:change(8))
b_8.grid(row = 3,column = 1)

b_9 = Button(frame_bord,text = '9',width = 2,height = 1,command = lambda:change(9))
b_9.grid(row = 3,column = 2)

b_0 = Button(frame_bord,text = '0',width = 2,height = 1,command = lambda:change(0))
b_0.grid(row = 4,column = 0)

b_point = Button(frame_bord,text = '·',width = 2,height = 1,command = lambda:change('.'))
b_point.grid(row = 4,column = 1)

'''
#运算符
def operation(op):
	print(op)
'''
b_jia = Button(frame_bord,text = '+',width = 2,height = 1,command = lambda:operation('+'))
b_jia.grid(row = 1,column = 3)

b_jian = Button(frame_bord,text = '-',width = 2,height = 1,command = lambda:operation('-'))
b_jian.grid(row = 2,column = 3)

b_cheng = Button(frame_bord,text = '×',width = 2,height = 1,command = lambda:operation('×'))
b_cheng.grid(row = 3,column = 3)

b_chu = Button(frame_bord,text = '÷',width = 2,height = 1,command = lambda:operation('÷'))
b_chu.grid(row = 4,column = 3)

b_rst = Button(frame_bord,text = '=',width = 2,height = 1,command = lambda:operation('='))
b_rst.grid(row = 4,column = 2)

frame_bord.pack(padx = 10,pady = 10)

root.mainloop()
