import time
import tkinter
import tkinter.ttk



##Progressbar 可以解释为进度条，主要是当做一个工作进度的指针，在这个控件中会有一个指针，由此指针可以了解工作进度。其构造方法如下：
##Progressbar(父对象, options, ...)



##length 进度条的长度，默认是100像素
##mode 模式
##orient 进度条方向，HORIZONTAL(默认)或者是VERTICAL
##maximum 进度条的最大值，默认是100像素
##value   进度条的目前值
 
##这里介绍mode参数：
##determinate：一个指针会从起点移至终点，通常当我们知道所需工作时间时，可以使用此模式，这是默认模式
##indeterminate：一个指针会在起点和终点间来回移动，通常当我们不知道工作所需时间时，可以使用此模式

def show():
    # 进度值最大值
    progressbarOne['maximum'] = 5
    # 进度值初始值
    progressbarOne['value'] = 0
    for i in range(10):
        time.sleep(1)
        progressbarOne['value'] += 1
        root.update()

root = tkinter.Tk()
root.geometry('150x120')

progressbarOne = tkinter.ttk.Progressbar(root,mode='indeterminate' )
progressbarOne.pack(side=tkinter.TOP)

confirm_button=tkinter.Button(root,text="确定",command=show)
confirm_button.pack(side=tkinter.TOP)
root.mainloop()
