#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  dataVisualizer.py
#  
#  Copyright 2018 Philippe Solodov
#  
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#  
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#  
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#  
#
  
class node():
    def __init__ (self,title):
        self.title = title
        self.types = ["ROOT","PARENT","CHILD"]
        self.type = ""
        self.branches = []
        self.nchoose = 0
        self.parentNode = False

    def set_type(self,typeOfNode):
        self.type = typeOfNode
    
    def get_types():
        return(self.types)
        
    def get_type(self):
		return(self.type)
		
    def set_branches(self,branches):
        for branch in branches:
            self.branches.append(branch)

    def set_branch(self,branch):
        self.branches.append(branch)

    def get_last_branch(self):
        return(self.branches[-1])

    def set_nchoose(self,nchoose):
        self.nchoose = nchoose

    def set_parent_node(self,parentNode):
        self.parentNode = parentNode

    def get_branches(self):
        return self.branches

    def switch_to_child_node(self,title):
        # Creates a child node and switches the active node to the child node
        # No idea if this should be in a seperate function but whatever

        self.set_branch(node(title))          # Creates new node
        currNode = self.get_last_branch()     # Goes to new node
        currNode.set_parent_node(self)        # Sets parent node of new node
        return currNode
        

    def get_parent_node(self):
        if self.parentNode:
            return(self.parentNode)
        else:
            return(False)

    def get_branch_num(self):
        return(len(self.branches))

    def gen_title(self):
        for branch in self.branches:
            if 'either' in branch.title:
                return("Choose either:")

        parentNodex = self.parentNode
        for branch in parentNodex.branches:
            if 'either' in branch.title:
                return("Or")
        return("Choose " + str(self.nchoose) + " of:")

    def trim(self):
        if len(self.branches) == 1:
            parentNodex = self.parentNode
            self = self.branches[0]
            self.parentNode = parentNodex


        return self

def navigateTree(parentNode):
    
    # Goes through all the branches of the parent node recursively
    # Probably recursively
    
	for branch in parentNode.get_branches():
		if branch.get_type() != 'CHILD':
			print(parentNode.title + "->" + branch.title)
			print("Choose " + str(branch.nchoose) + " of:")
		else:
			print(branch.title)
		navigateTree(branch)

def initializeDrawTree(parentNode):
    from graphviz import Digraph
    dot = Digraph(comment=parentNode.title)
    dot.attr(compound='true',label='')
    
    dot.node('CPSC340',color='#71ABFF',style='filled')
    dot.node_attr.update(color='#0D47CE', style='filled',shape='box')
    
    graph = drawTree(dot,parentNode)
    
    graph.render('test-output/' + parentNode.title + '.gv', view=True)
    return dot

def drawTree(graph,parentNode,num=0):
    titlex = 'cluster' + str(num)
    num+=1
    titley = 'cluster' + str(num-2)
    if num == 0:
        graph.attrs('node', color = 'white', style = 'filled')
    with graph.subgraph(name = titlex,comment='Hello world!') as graphx:
        for branch in parentNode.branches:
            branch = branch.trim()
            if branch.type != 'CHILD':
                graph.node(branch.title,branch.gen_title(), shape = 'box',color='#356FF6')
                if num-2 >= 0:
                    print(titley)
                    graph.edge(branch.title,branch.parentNode.title, lhead=titley,ltail=titlex)
                else:
                    graph.edge(branch.title,branch.parentNode.title)
            else:
                graph.edge(branch.title,branch.parentNode.title)

                
            drawTree(graphx,branch,num)
    return graph

# Decent code, needs improvement   
def coursePreReqTreeGen(courseCode,preReqs=False):
    print(preReqs)
	
    preReqKWList = ("one of","two of", "three of", "either", "or", "all of", "and")
    
    # To make expanding these easier, I have left them as lists in case new key words appear
    newBranchKW = ("and")
    subBranchKW = ("either")
    escapeBranchKW = ("or")
    nchooseDict = {"one of":1,"two of":2,"three of":3,"all of":'all'}

    preReqList = []
    preReqs = preReqs.split(" ")
    
    for i in range(1,len(preReqs)):
        department = preReqs[i-1]
        code = preReqs[i]

        if department.lower() + ' ' + code in preReqKWList:
            preReqList.append(department + ' ' + code)

        elif code in preReqKWList:
            preReqList.append(code)

        preReq = True
        
        for letter in department:
            try:
				#Check if it's a number: if it is, then not a pre-req
                letter = int(letter)
                preReq = False
                break
            except ValueError:
				# If it isn't a number, check if it's lower case.
                if letter.islower():
                    preReq = False
                    break

        if preReq:
            preReq = str(department) + ' ' + str(code)
            for character in (",",";","."):
                preReq = preReq.strip(character)
            preReqList.append(preReq)

    # Initializing tree with parent node and name
    parentNode = node(courseCode)
    parentNode.set_type('ROOT')

    # Creating branch (node) for first pre-reqs, setting active node (node being operated on)
    # Setting information
    activeNode = parentNode.switch_to_child_node("Initial")
    activeNode.set_nchoose(nchooseDict[preReqList[0].lower()])

    i = 0
   
    # This code exists solely for the initial node
    for string in preReqList[1:]:
        i+=1
        string = string.lower()

        if string in newBranchKW:
            break
        elif string in subBranchKW:
            break
        elif string in escapeBranchKW:
            break
        currNode = activeNode.switch_to_child_node(string.upper())
        currNode.set_type('CHILD')
    a = 0
    b = 0

    # Traverses the list and creates nodes with branches for each pre-requisite
    for string in preReqList[i:]:
		
        string = string.lower()
        if string in newBranchKW:
            a += 1

            # This creates a new branch from the parent of the branch and switches to the new branch if 'and' is detected: creates a new branch in parallel to the current one and switches to it

            activeNode = activeNode.get_parent_node()   # Goes to active node's parent node (either is after and)
            activeNode = activeNode.switch_to_child_node(string+str(a))


        elif string in subBranchKW:

            # This creates a new branch from the active branch and switches to the new branch if 'either' is detected: creates a new branch below the current one and switches to it

            activeNode = activeNode.switch_to_child_node(string)
            activeNode.set_nchoose(1)

        elif string in escapeBranchKW:

            # This creates a new branch from the parent of the active branch, switches to it, and creates a new branch from the new branch if 'or' is detected

            activeNode = activeNode.get_parent_node()   # Goes to parent node

            activeNode = activeNode.switch_to_child_node(string+str(b))
            activeNode.set_nchoose(1)
    
            b+=1
            a+=1

            activeNode = activeNode.switch_to_child_node('and'+str(a))
            activeNode.set_nchoose(1)


        elif string in nchooseDict.keys():
            activeNode.set_nchoose(nchooseDict[string])

        else:
            currNode = activeNode.switch_to_child_node(string.upper())
            currNode.set_type('CHILD')


    navigateTree(parentNode)
    initializeDrawTree(parentNode)
    
def main(args):
    return 0

if __name__ == '__main__':
    import sys
    coursePreReqTreeGen('CPSC340','One of MATH 152, MATH 221, MATH 223 and one of MATH 200, MATH 217, MATH 226, MATH 253, MATH 263 and one of STAT 200, STAT 203, STAT 241, STAT 251, COMM 291, ECON 325, ECON 327, PSYC 218, PSYC 278, PSYC 366, MATH 302, STAT 302, MATH 318, BIOL 300; and either (a) CPSC 221 or (b) all of CPSC 260, EECE 320 and one of CPSC 210, EECE 210, EECE 309.')
    sys.exit(main(sys.argv))
