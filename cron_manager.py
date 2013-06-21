#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
#
#


#(crontab -l ; echo "0 * * * * wget -O - -q http://www.example.com/cron.php") | crontab -
from gi.repository import Gtk
import MySQLdb
import os
import re



class Crud_GUI:
    
    def __init__(self):
        self.HOUR = 0
        self.MINUTE = 1
        self.DAY_OF_WEEK = 2
        self.COMMAND = 3
        self.builder = Gtk.Builder()
        self.builder.add_from_file("cron_gtk.glade")
        self.handlers = {"on_combobox1_changed":self.on_combobox1_changed,
                         "onDeleteWindow":self.onDeleteWindow,
                         "onHelpMenu":self.onHelpMenu,
                         "on_button1_activate":self.on_button1_activate,
                         "onAboutDialog":self.onAboutDialog,
                         "onCloseAbout":self.onCloseAbout,
                         "on_close_task_add":self.on_close_task_add,
                         "on_close_task_exists":self.on_close_task_exists,
                         }
        self.builder.connect_signals(self.handlers)
        self.window = self.builder.get_object("window")
        self.window.connect("destroy", Gtk.main_quit)
        self.window.show_all()
        self.builder.get_object("grid2").hide()

    def __del__(self,*args):
        print "Deleted"
        #Gtk.main_quit(*args)


    def on_combobox1_changed(self, *args):
        print args[0].get_active()

    def onDeleteWindow(self, *args):
        Gtk.main_quit(*args)
                
    def onHelpMenu(self,*args):
        print "help"
        
    def on_button1_activate(self, *args):
        params = self.__getArgs(args[0])
        print params
        valid = self.__validate_params(params)
        if valid == False: 
            self.__show_error(args[0])
        elif valid == True:
            print "valid"
            self.__hide_error(args[0])
            if self.existsTask(params[self.COMMAND]):
                print "exists"
                self.__show_task_exists()
            else:
                print "not exists (add)"
                self.__show_task_add()
                os.system("(crontab -l ; echo \"%s %s * * %i %s\") | crontab " % (params[self.MINUTE],params[self.HOUR],params[self.DAY_OF_WEEK],params[self.COMMAND]))

                

    def __show_task_add(self):
        self.dialog_add = self.builder.get_object("dialog1")
        self.dialog_add.show_all()

    def on_close_task_add(self,*args):
        print "add"
        self.dialog_add = self.builder.get_object("dialog1")
        self.dialog_add.hide()


    def __show_task_exists(self):
        self.dialog_exists = self.builder.get_object("dialog2")
        self.dialog_exists.show_all()

    def on_close_task_exists(self,*args):
        print "exists"
        self.dialog_exists = self.builder.get_object("dialog2")
        self.dialog_exists.hide()
    
    def __show_error(self,grid):
        grid.get_child_at(1,4).show()

    def __hide_error(self,grid):
        grid.get_child_at(1,4).hide()

    def __validate_params(self, params):
        (hours, minutes,day,command) = params
        try:
            hours = int(hours)
            minutes = int(minutes)
            return ( hours >= 0 and hours <= 23 and minutes >= 0 and minutes <= 59)
        except:
            return False
        
        
    def __getArgs(self,grid):
        hours = grid.get_child_at(1,0).get_text()
        minutes = grid.get_child_at(1,1).get_text()
        day = (grid.get_child_at(1,2).get_active()+1)%7
        command = grid.get_child_at(1,3).get_text()
        return (hours, minutes,day,command)

    def onAboutDialog(self, *args):
        self.about = self.builder.get_object("aboutdialog1")
        self.about.show_all()

    def onCloseAbout(self, *args):
        self.about = self.builder.get_object("aboutdialog1")
        self.about.hide()

    def getCronTasks(self):
        return os.popen("crontab -l").read()

    def existsTask(self,task,cronTasks):
        return self.__existsTask(task,cronTasks)

    def existsTask(self,task):
        return self.__existsTask(task,self.getCronTasks())

    def __existsTask(self,task,cronTasks):
        print task
        print cronTasks
        tasksArray = self.__cleanCronTasks(cronTasks)

        myTask_elem = self.__format_task(task)

        tasks_elems = []

        for t in tasksArray:
            tc = self.__format_task(t)
            if tc: tasks_elems.append(tc)

        for t_e in tasks_elems:
            print t_e

        return self.__existsTaskElem(myTask_elem,tasks_elems)

    def __existsTaskElem(self,myTask_elem,tasks_elems):

        print "comparando:\n",myTask_elem,"con \n"
        print tasks_elems
        cuenta_args = 0

        for t in tasks_elems:
            if myTask_elem[0]==t[0]:
                if (not myTask_elem[1] and not myTask_elem[1]): 
                    return True #si encuentro mismo comando sin args
                if len(myTask_elem[1])==len(t[1]): #igual num de args
                    for t_arg in myTask_elem[1]: #compruebo todos los args
                        if t_arg in t[1]:
                            cuenta_args+=1
                    if cuenta_args==len(myTask_elem[1]): #mismo nombre,mismo num args, mismos args 
                        return True
                    cuenta_args = 0

        return False



    

    def __format_task(self,task):
        args_pat = '(\-\S+(?:\s+[^\-]\S*\s*)?)+'
        t = re.sub("\s+", " ", task)
        command = re.findall("^\s*(\S+)\s*",t)
        ar = re.findall(args_pat,t)
        if not not command: #commando no nulo []                                                 
            return (command[0],ar)
        return None

    def __cleanCronTasks(self,cronTasksStr):
        tasksCleaned = re.sub("^\s*(\S\s+){5}", "", cronTasksStr,0,re.MULTILINE)
        tasksArray = re.split("\n",tasksCleaned)
        return tasksArray


    
def main():
        window = Crud_GUI()
        Gtk.main()
        return 0

if __name__ == '__main__':
        main()

