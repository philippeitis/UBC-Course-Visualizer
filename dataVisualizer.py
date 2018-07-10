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

    def get_parent_node(self):
        if self.parentNode:
            return(self.parentNode)
        else:
            return(False)

    def get_branch_num(self):
        return(len(self.branches))

def main(args):
    return 0
    
def navigateTree(parentNode):
    if parentNode.get_branch_num() == 0:
        return(False)

    else:
        for branch in parentNode.branches:
            branchParent = branch.get_parent_node()
            if branchParent:
                print("Parent of " + branch.title + " is " + branchParent.title)
            else:
                print(branch.title)
            navigateTree(branch)

def navigateTreex(parentNode):
    for branch in parentNode.branches:
        print(branch.title)
        for branchx in branch.branches:
            print(branchx.title)

def initializeDrawTree(parentNode):
    from graphviz import Digraph
    dot = Digraph(comment='CPSC340')
    dot.attr(compound='true')
    dot.attr(bgcolor='grey', label='CPSC340', fontcolor='white')
    clusternum = 0
    for branch in parentNode.branches:
        string = 'cluster' + str(clusternum)

            
        dot.edge(branch.title,'CPSC340')
        clusternum += 1

    dot.render('test-output/CPSC340x.gv', view=True)  # doctest: +SKIP
    return dot
   
def CPSC340():
    import time
    preReqs = 'One of MATH 152, MATH 221, MATH 223 and one of MATH 200, MATH 217, MATH 226, MATH 253, MATH 263 and one of STAT 200, STAT 203, STAT 241, STAT 251, COMM 291, ECON 325, ECON 327, PSYC 218, PSYC 278, PSYC 366, MATH 302, STAT 302, MATH 318, BIOL 300; and either (a) CPSC 221 or (b) all of CPSC 260, EECE 320 and one of CPSC 210, EECE 210, EECE 309.'

    preReqKWList = ["one of", "either", "or", "all of", "and"]
    newBranchKW = "and"
    subBranchKW = "either"
    escapeBranchKW = "or"

    parentNode = node('CPSC340')
    parentNode.set_type('ROOT')

    nchooseDict = {"one of":1,"two of":2,"three of":3,"four of":4,"all of":'all'}

    preReqList = []
    preReqsx = preReqs.split(" ")
    for i in range(1,len(preReqsx)):
        department = preReqsx[i-1]
        code = preReqsx[i]

        
        if department.lower() + ' ' + code in preReqKWList:
            preReqList.append(department + ' ' + code)

        elif code in preReqKWList:
            preReqList.append(code)

        courseCode = True
        
        for letter in department:
            try:
                letter = float(letter)
                courseCode = False
                break
            except ValueError:    
                if letter.islower():
                    courseCode = False
                    break

        if courseCode:
            courseCode = str(department) + ' ' + str(code)
            for character in (",",";","."):
                courseCode = courseCode.strip(character)
            preReqList.append(courseCode)

    parentNode.set_branch(node("Initial"))
    activeNode = parentNode.get_last_branch()
    activeNode.set_parent_node(parentNode)
    activeNode.set_nchoose(nchooseDict[preReqList[0].lower()])

    i = 0
   
    for string in preReqList[1:]:
        i+=1
        if string.lower() in newBranchKW:
            break
        elif string.lower() in subBranchKW:
            break
        elif string.lower() in escapeBranchKW:
            break
        activeNode.set_branch(node(string))
        currNode = activeNode.get_last_branch()
        currNode.set_nchoose(0)
    
    print(i)
    a = 0
    b = 0
    activeNode.get_parent_node()

    for string in preReqList[i:]:
        if string.lower() in newBranchKW:
            a += 1
            print("Setting new branch, switching from: " + activeNode.title)

            activeNode = activeNode.get_parent_node()   # Goes to active node's parent node (either is after and)
            activeNode.set_branch(node(string+str(a)))         # Makes new node
            currNode = activeNode.get_last_branch()     # Goes to new node
            currNode.set_parent_node(activeNode)        # Sets active node as parent
            activeNode = currNode                       # Switches operation to new node

            print("New branch set, switching to new node: " + activeNode.title)
            print("")

        elif string.lower() in subBranchKW:
            print("Going to parent node from: " + activeNode.title)

            activeNode.set_branch(node(string))         # Creates new node
            currNode = activeNode.get_last_branch()     # Goes to new node
            currNode.set_parent_node(activeNode)        # Sets parent node of new node
            currNode.set_nchoose(1)                     # Sets nchoose
            activeNode = currNode                       # Switches active node
            
            print("Active node is now: " + activeNode.title)
            print("")

        elif string.lower() in escapeBranchKW:
            print("Going to parent branch from: " + activeNode.title)
            activeNode = activeNode.get_parent_node()   # Goes to parent node
            print("Parent node is: " + activeNode.title)
            activeNode.set_branch(node(string+str(b)))
            currNode = activeNode.get_last_branch()
            currNode.set_parent_node(activeNode)
            activeNode = currNode
            b+=1
            activeNode.set_branch(node(string+str(b)))
            currNode = activeNode.get_last_branch()
            currNode.set_parent_node(activeNode)
            activeNode = currNode
            print("Active node is now: " + activeNode.title)
            print("")

        elif string.lower() in nchooseDict.keys():
            print('choose ' + str(nchooseDict[string.lower()]))
            activeNode.set_nchoose(nchooseDict[string.lower()])

        else:
            activeNode.set_branch(node(string))
            currNode = activeNode.get_last_branch()
            currNode.set_type('CHILD')
            print("Active node: " + activeNode.title)
            print("Course code being added: " + string)



    print("No more string processing.")

    navigateTreex(parentNode)
    initializeDrawTree(parentNode)

CPSC340()

def demoPlotter():
    
    from graphviz import Digraph

    dot = Digraph(comment='CPSC340')
    dot  #doctest: +ELLIPSIS
    dot.attr(compound='true')
    dot.attr(bgcolor='grey', label='CPSC340', fontcolor='white')

    with dot.subgraph(name = 'cluster2') as Z:
        Z.attr(bgcolor='grey', label='Either (a)', fontcolor='white')
        Z.node('H','CPSC 221')
        with Z.subgraph(name = 'cluster0') as E:
            E.attr(bgcolor='grey', label=' or (b)', fontcolor='white')
            E.node('F','One of \n CPSC 210, \n EECE 210, \n EECE 309')
            E.node('G','All of \n CPSC 260, \n EECE 320')

    with dot.subgraph(name = 'cluster1') as dot2:
        dot.attr(bgcolor='grey', label='', fontcolor='white')
        dot2.node('A', 'CPSC340')
        dot2.node('B', 'One of \n MATH 152, \n MATH 221, \n MATH 223')
        dot2.node('C', 'One of \n MATH 200, \n MATH 217, \n MATH 226, \n MATH 253, \n MATH 263')
        dot2.node('D', 'One of \n STAT 200, \n STAT 203, \n STAT 241, \n STAT 251, \n COMM 291, \n ECON 325, \n ECON 327, \n PSYC 218, \n PSYC 278, \n PSYC 366, \n MATH 302, \n STAT 302, \n MATH 318, \n BIOL 300')

    dot.edge('F','H',ltail='cluster0',lhead='cluster2')
    dot.edge('H','F',ltail='cluster2',lhead='cluster0')
    dot.edge('H','A',ltail='cluster2',lhead='cluster0')
    dot.edges(['BA', 'CA', 'DA'])
    dot.render('test-output/CPSC340.gv', view=True)  # doctest: +SKIP

plotter()
if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))
