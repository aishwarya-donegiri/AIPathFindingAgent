# -*- coding: utf-8 -*-
"""
Created on Wed Sep 25 21:17:46 2019

@author: Aishwarya
"""

from queue import PriorityQueue
from math import sqrt

global pq
global dr
global dc
dr=[-1,+1,0,0,-1,-1,+1,+1]
dc=[0,0,+1,-1,-1,+1,+1,-1]
file=open("input_100.txt", "r")
contents=file.readlines()
#print (contents)
algorithm=contents[0]
#print (algorithm)
#algorithm=algorithm
rc=contents[1].split()
#print(rc)
W=int(rc[0])
H=int(rc[1])
#print (H,W)

start=contents[2].split()
sc=int(start[0])
sr=int(start[1])
#print (sr,sc)

el_diff=int(contents[3])

no_of_targets=int(contents[4])
#print (no_of_targets)


targets=[]
#print (contents[5].split())
for i in range(no_of_targets):
    #print (i)
    targets.append(contents[5+i].split())
    tc=int(targets[i][0])
    tr=int(targets[i][1])
    targets[i]=(tr,tc)
updated_targets=set(targets)
updated_target_count=len(updated_targets)
#print (targets)


m=[[0]*W for i in range(H)]
for j in range(H):
    #print ("j",j)
    row=contents[5+no_of_targets+j].split()
    print (row)
    for k in range(W):
        #print (j,k)
        m[j][k]=int(row[k])
file.close()
#print (m)
###########################################################


def find_path(row,column):
        #print ("im here")
        #print(row,column)
        global parent
        path=[]
        i=(row,column)
        if i not in parent:
            return 0
        while i!=(sc,sr):
            path.append(i)
            i=parent[i]
        path.append((sc,sr))
        path.reverse()
        return path  

def goal_test(row,column):
        #print("--------------")
        #print (row,column)
        if (row,column) in targets:
            #print("True")
            return True
        else:
            return False
        
def run_target():
    paths={}
    global f
    f=open("ip_op.txt","w")
    for i in targets:
        #print (i)
        c=i[1]
        r=i[0]
        #print(i)
        if i in paths:
            #print (i)
            #print ("here")
            continue
        
        path=find_path(c,r)
        if path==0:
            paths[(r,c)]="FAIL"
            continue
        print (len(path))
        path_str =''
        for position in path:
            #print(position)
            for i in range(len(position)):
                path_str += str(position[i])
                if(i==0):
                    path_str += ','
                else:
                    path_str += ' '
        
        paths[(r,c)]=path_str
     
    
    for i in targets:
        
        f.write(paths[i])
        f.write('\n')
     
def in_pq(row,column):
    for i in pq.queue:
        if (i[1]==(row,column)):
            return True
        else:
            return False
    
    #find the cost in the priority queue
def total_cost(row,column):
    for i in pq.queue:
        if (i[1]==(row,column)):
            return i[0]
   
#replace value of cost in priority queue         
def replace_cost(row,column):
    #print ("im replaced")
    for i in pq.queue:
        if i[1]==(row,column):
            i[0]=path_cost

##########################################################
#Breadth First Search
def bfs(H,W,m,sr,sc,el_diff):
    #print(H,W,m,sr,sc,el_diff)
    #global temp
    #temp=[]
    global count
    count=min(no_of_targets,updated_target_count)
    #print(count)
    r_c=[(sr,sc)]
    global parent
    parent={}
    parent[(sc,sr)]=(-1,-1)
    target=False
    
        
    #find the neighbours
    def find_neighbours_bfs(r,c):
        global count
        for i in range(8):
            (rr,cc)=(r+dr[i],c+dc[i])
            #print("----------")
            #print(rr,cc)
            #boundary conditions
            if rr<0 or cc<0:
                #print ("------")
                continue
            
            if rr>=H or cc>=W:
                #print ("------")
                continue
                
            #elevation difference
            if (abs(m[r][c]-m[rr][cc])>el_diff):
                #print ('im here')
                continue
                        
            #check if (rr,cc) is visited
            if (cc,rr) in parent:
                #print ("------")
                continue
            
            r_c.append((rr,cc))
            parent[(cc,rr)]=(c,r)
            
            
            
            
    
    if len(r_c)==0:
        return 0
    while len(r_c)>0:
        r,c=r_c.pop(0)
        #print ((r,c))
        if goal_test(r,c):
            #print(temp)
            #print ("goal")
            #temp.append((r,c))
            count-=1
            #print (count)
            if (count==0):
                #print("im done")
                target=True
                break
        #find the neighbouring nodes of (r,c)
        find_neighbours_bfs(r,c)    
         
    
    if len(r_c)==0 and count!=0:
        target=True
        
    if target:
        run_target()
        #print ("target")
        
#########################################################################################
#UCS
def ucs(H,W,m,sr,sc,el_diff):
    #pq is the priority queue holding the values of rows and columns
    global pq
    pq=PriorityQueue()
    cost=0
    global path_cost
    global parent
    parent={}
    parent[(sc,sr)]=(-1,-1)
    global count
    count=min(no_of_targets,updated_target_count)
    #print (parent[(sr,sc)])
    node=[0,(sr,sc)]
    pq.put(node)
    #print (pq.queue)
    
    target=False
    
        
    #find the neighbours
    def find_neighbours_ucs(cost,r,c):
        global path_cost
        path_cost=0
        for i in range(8):
            (rr,cc)=(r+dr[i],c+dc[i])
            
            #boundary conditions
            if rr<0 or cc<0:
                continue
            if rr>=H or cc>=W:
                continue
                
            #elevation difference
            if (abs(m[r][c]-m[rr][cc])>el_diff):
                continue
                
            #assigning path cost
            if i<4:
                path_cost=cost+10
            if i>=4:
                path_cost=cost+14
                
            #child is not explored or in the priority queue
            if not (((cc,rr) in parent) or in_pq(rr,cc)):
                pq.put([path_cost,(rr,cc)])
                parent[(cc,rr)]=(c,r)
                    
            #altering the path_cost if its lower than previous cost
            elif in_pq(rr,cc):
                if (total_cost(rr,cc)>path_cost):
                    replace_cost(rr,cc)
                    parent[(cc,rr)]=(c,r)
                            
            #explored[rr][cc]=True               
            #print ("--------",path_cost,(rr,cc))
            #print (next_level)
        
    
    
    #explored[sr][sc]=True
    if pq.empty():
        #print ("empty")
        return 0
    while not pq.empty():
        cost,(r,c)=pq.get()
        #print (cost,(r,c))
        
        if goal_test(r,c):
            #print(temp)
            #print ("goal")
            #temp.append((r,c))
            count-=1
            #print (count)
            if (count==0):
                #print("im done")
                target=True
                break
        
        
        #find the neighbouring nodes of (r,c)
        find_neighbours_ucs(cost,r,c)
    if pq.empty() and count!=0:
        target=True
    
    #print (count)
    if target:
        run_target()
        
        
####################################################################################
        
def a_star(H,W,m,sr,sc,el_diff,tr,tc):
    #pq is the priority queue holding the values of rows and columns
    global pq
    pq=PriorityQueue()
    cost=0
    paths={}
    global path_cost
    global parent
    parent={}
    parent[(sc,sr)]=(-1,-1)
    #print (parent[(sr,sc)])
    node=[0,(sr,sc)]
    pq.put(node)
    #print (pq.queue)
    target=False
    
    #check if goal is reached
    def goal_test(row,column):
        if ((row,column)==(tr,tc)):
            #print (target)
            #print (path_count)
            return True
        else:
            return False
     
    #check if ordered pair is in priority queue
                
        
    #find the neighbours
    def find_neighbours_astar(cost,r,c):
        global path_cost
        path_cost=0
        for i in range(8):
            (rr,cc)=(r+dr[i],c+dc[i])
            
            #boundary conditions
            if rr<0 or cc<0:
                continue
            if rr>=H or cc>=W:
                continue
                
            #elevation difference
            if (abs(m[r][c]-m[rr][cc])>el_diff):
                continue
                
            #assigning path cost
            if i<4:
                path_cost=cost+10
            if i>=4:
                path_cost=cost+14
            path_cost+=abs(m[rr][cc]-m[r][c])
            heuristic=(sqrt((tr-rr)**2 + (tc-cc)**2))*10+abs(m[rr][cc]-m[tr][tc])
            path_cost+=heuristic
                
            #child is not explored or in the priority queue
            if not (((cc,rr) in parent) or in_pq(rr,cc)):
                pq.put([path_cost,(rr,cc)])
                parent[(cc,rr)]=(c,r)
                    
            #altering the path_cost if its lower the previous cost
            elif in_pq(rr,cc):
                if (total_cost(rr,cc)>path_cost):
                    replace_cost(rr,cc)
                    parent[(cc,rr)]=(c,r)
                            
                            
            #print ("--------",path_cost,(rr,cc))
            #print ("----------------",pq.queue)
        
    
    
    if pq.empty():
        #print ("empty")
        return 0
    while not pq.empty():
        cost,(r,c)=pq.get()
        #print ('\n','\n',cost,(r,c))
        if goal_test(r,c):
            #print ("goal")
            target=True
            #print (target)
            #final_cost=cost
            print ("-------------",cost)
            break
        
        #find the neighbouring nodes of (r,c)
        find_neighbours_astar(cost,r,c)    
    
    if target:
        #print(target)
        global f
        if (tr,tc) in paths:
            f.write(paths[(tr,tc)])
            f.write("\n")
        else:
            path=find_path(tc,tr)
            print (len(path))
            path_str =''
            for position in path:
                #print(position)
                for i in range(len(position)):
                    path_str += str(position[i])
                    if(i==0):
                        path_str += ','
                    else:
                        path_str += ' '
            paths[(r,c)]=path_str
            f.write(path_str)
            f.write("\n")
            
    else:
        paths[(r,c)]="FAIL"
        f.write("FAIL")
        f.write("\n")
        
        
#####################################################################################        
if (algorithm=="BFS\n"):
    print ("BFS")
    bfs(H,W,m,sr,sc,el_diff)
    f.close()
    
if (algorithm=="UCS\n"):
    print ("UCS")
    ucs(H,W,m,sr,sc,el_diff)
    f.close()
    
if(algorithm=="A*\n"):
    print ("A*")
    #print (len(targets))
    f=open("op.txt","w")
    for i in range(len(targets)):
        tr=targets[i][0]
        tc=targets[i][1]
        #print (tr,tc)
        a_star(H,W,m,sr,sc,el_diff,tr,tc)
    f.close()