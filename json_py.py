#!/usr/bin/python
######################################################################
# Author : Aaron Benkoczy
# Date : 2018.01.04.
######################################################################
# https://stackoverflow.com/questions/28132055/not-able-to-display-multiple-json-keys-in-tkinter-gui


import fnmatch
import os
import re
import xml.etree.ElementTree as ET
import sys
from Tkinter import *
import tkFont
import ttk
import uuid
import json

class App:

    JSON_dictionary = {}


    def selectAll(event):
        print('e.get():', e.get())
        # or more universal
        print('event.widget.get():', event.widget.get())

        # select text
        event.widget.select_range(0, 'end')
        # move cursor to the end
        event.widget.icursor('end')

    def Killme():
        self.root.quit()
        self.root.destroy()

    # refresh menu
    def RefreshMenu(self):
        self._tree.delete(*self._tree.get_children())
        self.retrieve_input()
        global JSON_dictionary
        if(len(JSON_dictionary) > 0):
            self.ReReadFile()

    def ClearText(self):
        self._inputEntry.delete('1.0', END)

    def CopyText(self):
        input_string = self._inputEntry.get("1.0",END)
        self.root.withdraw()
        self.root.clipboard_clear()
        self.root.clipboard_append(input_string)
        self.root.update() # now it stays on the clipboard after the window is closed

    # double click on a node

    def is_json(myjson):
        try:
            json_object = json.loads(myjson)
        except ValueError as e:
            return False
        return True

    def retrieve_input(self):
        input_string = self._inputEntry.get("1.0",END)
        input_string = input_string.strip()
        global JSON_dictionary 
        data = JSON_dictionary
        if(len(input_string) > 0 and input_string != ""):
            # parse json string
            try:
                print("json string convert")
                data = json.loads(input_string)
            except ValueError as e:
                print(e)
                print("cannot read json string");
            # paerse perl json string    
                try:
                    print("try perl json string convert")
                    input_string = input_string.replace(" =>",":")
                    input_string = input_string.replace("\'","\"")
                    input_string = input_string.replace("undef","0")
                    input_string = " ".join(input_string.split())
                    print(input_string)
                    data = json.loads(input_string)
                except ValueError as e:
                    print(e)
                    print("cannot read perl json string");
            JSON_dictionary = data

    def JSONTree(self, Tree, Parent, Dictionary):
        for key in Dictionary :
            uid = uuid.uuid4()
            if isinstance(Dictionary[key], dict):
                Tree.insert(Parent, 'end', uid, text=key)
                self.JSONTree(Tree, uid, Dictionary[key])
            elif isinstance(Dictionary[key], list):
                Tree.insert(Parent, 'end', uid, text=key + '[]')
                self.JSONTree(Tree,
                         uid,
                         dict([(i, x) for i, x in enumerate(Dictionary[key])]))
            else:
                value = Dictionary[key]
                if isinstance(value, str) or isinstance(value, unicode):
                    value = value.replace(' ', '_')
                else:
                    value = str(value)
                Tree.insert(Parent, 'end', uid, text=key, value=value)


    def OnDoubleClick(self, event):
        selected_item = self._tree.focus()
        #value = self._tree.item(selected_item, "values") # "values when"
        value = self._tree.item(selected_item, "values")
        #print(value)
        if (len(value) > 0):

            string_line = str(value[1])
            lineArray = string_line.split(",")
            line = str(lineArray)
            line = line.replace("'", " ")
            line = line.strip()
            to_clipboard = line[line.find("/home"):line.find(": ")]
            #print(to_clipboard)
            self.root.clipboard_clear()
            self.root.clipboard_append(to_clipboard.decode('utf-8'))
            print ("===============================================================")
            print (to_clipboard.decode('utf-8'))
            print ("===============================================================")
    def __init__(self):

        self.root=Tk()
        self.root.title("Json Parser")
        self.root.geometry('10x10+0+0')
        self.dFont=tkFont.Font(family="Arial", size=14)

        # Menu elements
        self.menu = Menu(self.root)
        self.root.config(menu=self.menu)
        self.fileMenu = Menu(self.menu)
        self.menu.add_cascade(label="File", menu=self.fileMenu)
        self.fileMenu.add_command(label="Refresh", command=self.RefreshMenu)

        self._loadButton = Button(self.root, height=1, width=10, text="Load", 
                    command=lambda: self.RefreshMenu())
        self._loadButton.grid(row=0, column=1)

        self._clearButton = Button(self.root, height=1, width=10, text="Clear", 
                    command=lambda: self.ClearText())
        self._clearButton.grid(row=1, column=1)

        self._copyButton = Button(self.root, height=1, width=10, text="Copy", 
                    command=lambda: self.CopyText())
        self._copyButton.grid(row=0, column=3)

        self._inputEntry = Text(self.root, height=2, width=10, bg="grey")
        self._inputEntry.grid(row=0, column=4)
        self._inputEntry.insert(INSERT, '{"submit":"finish","responses":{"762":{"3483":["10591"],"yolo":["10594"],"3485":[10595,10596,10597],"3486":["sdfghjkl harom"]}},"comments":{"762":{}}}')

        # init tree
        self._tree = ttk.Treeview(self.root)
        #_tree.LabelEdit = TRUE
        # self._tree["columns"]=("one","two")
        self._tree["columns"]=("one")
        self._tree.heading("#0", text="Key")
        self._tree.heading("one", text="Value")
        # self._tree.heading("two", text="Place")
        self._tree.column("#0", minwidth=35, stretch=FALSE)        
        self._tree.column("one", minwidth=60, stretch=TRUE)
        # self._tree.column("two", minwidth=45, stretch=FALSE)
        self._tree.grid(row=1, column=1, stic="nsew")

        # event listener double click
        self._tree.bind("<Double-1>", self.OnDoubleClick)
        self._tree.bind('<Control-KeyRelease-a>', self.selectAll)
        #ttk.Style().configure('Treeview', rowheight=50)
        
        # scroll bar to root
        self.yscrollbar=Scrollbar(self.root, orient=VERTICAL, command=self._tree.yview)
        self.yscrollbar.pack(side=RIGHT, fill=Y)

        self.xscrollbar=Scrollbar(self.root, orient=HORIZONTAL, command=self._tree.xview)
        self.xscrollbar.pack(side=BOTTOM, fill=X)

        self._tree.configure(yscrollcommand=self.yscrollbar.set, xscrollcommand=self.xscrollbar.set)

        self.root.geometry('600x600+0+0')

        # self._loadButton.pack(side=LEFT, fill=BOTH, expand = YES)
        # self._clearButton.pack(side=LEFT, fill=BOTH, expand = YES)
        # self._copyButton.pack(side=LEFT, fill=BOTH, expand = YES)
        # self._inputEntry.pack(side=LEFT, fill=BOTH, expand = YES)
        # self._tree.pack(side=RIGHT, fill=BOTH, expand = YES)

        self._loadButton.pack(fill=X)
        self._clearButton.pack(fill=X)
        self._copyButton.pack(fill=X)
        self._inputEntry.pack(fill=X)
        self._tree.pack(fill=BOTH, expand = YES)

        global JSON_dictionary
        JSON_dictionary = {"submit":"finish","responses":{"762":{"3483":["10591"],"yolo":["10594"],"3485":[10595,10596,10597],"3486":["sdfghjkl harom"]}},"comments":{"762":{}}}

        self.ReReadFile()
        ###############################
        # lets read the content: ######

        # file name
        

        # if(len(JSON_dictionary) > 0 ):
            # self.ReReadFile()
        # else:
        #     print(JSON_dictionary + " is not a valid file")
        #     sys.exit(-1)
    # content reader

    def ReReadFile(self):

        global JSON_dictionary
        allWarnings = 0

        SSstring =""
        # open the file
        if (len(SSstring) > 0):
            # content = f.read()
            content = JSON_dictionary.strip()


            # split the content by the pointer arrow ^
            contentList = content.split("^")
            tagTypes = set()

            # the first root tag what shows "All Warnings"
            tagMap = {"[root]": 0}
            tagMap["[root]"] = self._tree.insert("", 0, "[root]", text="[All Warnings: 0]")

            tagIndex = 1

            # iterate throu the splitted elements
            for i, line in enumerate(contentList):
                #line = line.strip()

                #get the tag, like: [-Wsomething]
                if re.search("\[\-W.*\]", line):
                    #tag = "["+line[line.find("[")+1:line.find("]")]+"]"
                    tag = re.search("\[\-W.*\]", line).group()

                    # insert a tag if it is not exsist
                    if(tag not in tagTypes):
                        tagTypes.add(tag)
                        tagMap[tag] = self._tree.insert("", tagIndex, tag, text=tag + " [1]")
                        ++tagIndex

                    # update the tags child counter
                    if(len(self._tree.get_children(tagMap[tag])) > 0):
                        self._tree.item(tag, text=tag + " ["+ str(len(self._tree.get_children(tagMap[tag]))+1) +"]")

                    # Tags - column
                    tagColumn = line[line.find(": warning: ")+1:line.find("[")]

                    # Place - column
                    placeColumn = line[line.find("/home"):line.find(": ")]
                    #placeColumn = line.search("/:]", line).group()

                    # Problem - column
                    lineArray = line.splitlines()
                    problemColumn = lineArray[len(lineArray)-2]
                    #problemColumn = line[line.find("]\n"):]
                    #insert an element under the tag
                    self._tree.insert(tagMap[tag], "end", i, 
                        text=tagColumn, values=(problemColumn, placeColumn)); 

                # if can't find a tag then add it to the "root" "All warnings"
                else:
                    # Tags - column
                    tagColumn = line[line.find(": warning: ")+1:line.find("[")]
                    # Place - column
                    placeColumn = line[line.find("/home"):line.find(": ")]
                    # Problem - column
                    lineArray = line.splitlines()

                    problemColumn = lineArray[len(lineArray)-2]
                    #problemColumn = line[line.find("]\n"):]

                    #insert an element under the tag
                    self._tree.insert(tagMap["[root]"], "end", i, 
                        text=tagColumn, values=(problemColumn, placeColumn));

                allWarnings = i;

        # count all of the warnings
        # get the elements under the all warnings to the second counter
        # self._tree.item("[root]", text="[All Warnings: " + str(allWarnings) +"]"
        #     " ["+ str(len(self._tree.get_children(tagMap["[root]"]))+1) +"]")

        # data = json.load(JSON_dictionary)
        self.JSONTree(self._tree, '', JSON_dictionary)


            #self._tree.pack()
        self.root.mainloop();
if __name__ == '__main__':

    # if len(sys.argv) < 2:
    #     print("usage: " + os.path.basename(sys.argv[0]) + " [JSON_dictionary]")
    #     print("example: ")
    #     print("python " + os.path.basename(sys.argv[0]) + " \"Make.log\"")
    #     print("")
    #     print("Features:")
    #     print("- You can double click on a node to copy the path!")
    #     print("- There is a \"File > Refresh\" menu where you can reread the makelog file.")
    #     sys.exit(0)
    
    app = App()
