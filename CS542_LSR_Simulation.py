
# coding: utf-8

# In[21]:




# In[2]:

#!/usr/bin/env python

#Python libraries required to execute the program
import Tkinter as tk
from tkMessageBox import *
from tkFileDialog  import askopenfilename 
source_router=-1
dest_router=-1
router_deleted=-1
adjancency_matrix=[]
valid_matrix=False;
import io
import json
import matplotlib.pyplot as plt

#function to display multiple shortest paths present in the network topology
def dfs_paths( start, goal):
    stack = [(goal, [goal])]
    while stack:
        (vertex, path) = stack.pop()
        for next in set(previous[vertex]) - set(path):
            if next == start:
                yield [next] + path
            else:
                stack.append((next,[next] + path))

#function to process the input file (topology.txt)                
def process_file(fname):
    global adjacency_matrix
    adjacency_matrix = []
    if(not fname.endswith('.txt') ):
        print "Invalid file format"
        return
    try:
        with open(fname) as f:
            adjacency_matrix=[(map(int,x.split(" "))) for x in f]     
        print adjacency_matrix
        if(len(adjacency_matrix)<8):
            print "File should have atleast 8 nodes";
            return;
        print "\nThe matrix is:\n"

        for line in adjacency_matrix :
            for item in line :
                print item, 
            print
            
    except IOError, e:
        print "File not found"
        
#function to set distances based on the topology file inputted by the user
def set_distances(adjacency_matrix):

    global distances
    global nodes
    
    distances = {}
    nodes = []

    num_nodes = len(adjacency_matrix)

    for i in xrange(num_nodes):
        tempdict = {}
        for j in xrange(num_nodes):
            if i!=j and adjacency_matrix[i][j]!=-1:
                tempdict[j+1] = adjacency_matrix[i][j]
        distances[i+1] = tempdict
        nodes.append(i+1)
        
#function to evaluate the shortest path using djiktra's algorithm
def dijkstra(start):

    global distances
    global nodes
    global unvisited
    global previous
    global visited
    global interface

    nodes_traverse=list(nodes);
    unvisited = {node: None for node in nodes}
    previous = {node: [] for node in nodes}
    interface = {node: [] for node in nodes}
    visited = {node: None for node in nodes}

    current = int(start)
    currentDist = 0
    unvisited[current] = currentDist
    tempdict1=[];

    for x in nodes:
        for next, distance in distances[current].items():
            newDist = currentDist + distance
            if unvisited[next] is not None and unvisited[next]< newDist: 
                continue
                
            if not unvisited[next] or unvisited[next] > newDist:
                unvisited[next] = newDist
                previous[next]=[current]
                
                if not interface[current]:
                    interface[next]=[next];
                else:
                    interface[next]=list(interface[current])
            elif unvisited[next] == newDist:
                unvisited[next] = newDist
                previous[next].append(current)
                if not interface[current]:
                    interface[next].append(next);
                else:
                    for temp in interface[current]:
                        interface[next].append(temp);
        visited[current] = currentDist
        nodes_traverse.remove(current)
        
        elements = [node for node in unvisited.items() if node[1] and node[0] in nodes_traverse]
        
        if not elements:
            break;
        
        current, currentDist = sorted(elements, key = lambda x: x[1])[0]

#GUI implementation begins

#Function to modify the topology. In case the router is deleted the link between the routers are computed as -1 and the results and the results are recomputed
def modify_topology():
    if not adjacency_matrix:
        showinfo('No', 'Topology cannot be modified without building a network topology. Please build a valid topology using Option 1') 
        return
    window = tk.Toplevel(root)
    window.title("Modify Topology")
    tk.Label(window, text="Router to be deleted").grid(row=0)
    deleted_router = tk.Entry(window)
    deleted_router.grid(row=0, column=1)
    global router_deleted;
    def callback():
        global router_deleted;
        global source_router;
        global dest_router;
        a=1
        user_input= int(deleted_router.get());
        user_input = user_input - 1;
        router_deleted=user_input;
        str_router_matrix="";
        if(int(deleted_router.get())==source_router):
            source_router=-1
        if(int(deleted_router.get())==dest_router):
            dest_router=-1
            
        if int(deleted_router.get()) not in nodes:
            showinfo('No', 'Invalid Router.! Please enter a valid router') 
            return
            
        for i in range(len(adjacency_matrix)):
            adjacency_matrix[i][user_input]=-1;
            adjacency_matrix[user_input][i]=-1;
        for line in adjacency_matrix :
            for item in line :
                str_router_matrix=str_router_matrix+ "\t" + str(item); 
            l=tk.Label(window,text=str_router_matrix);
            l.grid(row=a+1)
            a=a+1
            str_router_matrix=""
        set_distances(adjacency_matrix)
        window1 = tk.Toplevel(root)
        window1.title("Connection Table")
        #make scrollbar for canvas
        cScrollbar = tk.Scrollbar(window1)
        cScrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        canvas = tk.Canvas(window1)

        #attach canvas to scrollbar
        canvas.config(yscrollcommand=cScrollbar.set)
        cScrollbar.config(command=canvas.yview) 
        #make frame and put everything in frame
        frame = tk.Frame(window1)
        #window.config(yscrollcommand=scroll.set)
        #scroll.config(command=window.yview)
        for source_router1 in range(len(adjacency_matrix)):
            if(source_router1==user_input):continue
            source_router1= source_router1+1;
            set_distances(adjacency_matrix)
            dijkstra(source_router1)
            t_list=[];
            """st_label="Connection table for "+str(source_router);
            l=tk.Label(window,text=st_label, justify=tk.LEFT);"""
            row_pos=((source_router1-1)*(len(adjacency_matrix)+2))
            #l.grid(row=row_pos+1)
            for key in interface:
                t_list=[]
                list_str=''
                for t in list(set(interface[key])):
                    t_list=list(dfs_paths( source_router1, t))
                    for s in t_list:
                        if(len(s[1:])>1):
                            if(s[len(s)-1]==key):
                                s=[];
                        if(len(s)>0):
                            list_str=list_str+", "+str(s[1:])
                list_str=list_str[1:]
                """l=tk.Label(window,text=str(key)+"\t\t"+list_str, justify=tk.LEFT);
                l.grid(row=key+row_pos)"""
                e1 = tk.Entry(frame, relief=tk.RIDGE, width=50 )
                e1.grid(row=row_pos, sticky=tk.NSEW)
                e1.insert(tk.END, 'Connection table for router %d' % (source_router1))
                e1.configure(state='readonly')
                e = tk.Entry(frame, relief=tk.RIDGE )
                e.grid(row=key+row_pos, sticky=tk.NSEW)
                e.insert(tk.END, '%s\t%s' % (str(key), list_str))
                e.configure(state='readonly')
            e2 = tk.Entry(frame, relief=tk.RIDGE )
            e2.grid(row=row_pos+len(adjacency_matrix)+1, sticky=tk.NSEW)
            e2.insert(tk.END, '\n')
            e2.configure(state='readonly')
        def callback1():
            global dest_router;
            global source_router
            window2 = tk.Toplevel(root)
            rd=router_deleted+1
            print "router_deleted:%d" % rd
            print "dest_router:%d" % dest_router
            print "source_router in callback1:%d" % source_router
            def callback2():
                global dest_router;
                global source_router
                if(source_router==rd or source_router==-1):
                    source_router=int(e3.get())
                if(dest_router==rd or dest_router==-1):
                    dest_router=int(e4.get())
                if source_router not in nodes:
                    showinfo('No', 'Invalid Router.! Please enter a valid source router') 
                    return
                if dest_router not in nodes:
                    showinfo('No', 'Invalid Router.! Please enter a valid destination router') 
                    return
                dijkstra(source_router)
                t_idx=1;
                e = tk.Entry(window2, relief=tk.RIDGE, width=50 )
                e.grid(row=t_idx+3, sticky=tk.NSEW)
                e.insert(tk.END, 'Paths from source router %d to destination router %d:' % (source_router, dest_router) )
                e.configure(state='readonly')
                for t_list in list(dfs_paths( source_router, dest_router)):
                    e = tk.Entry(window2, relief=tk.RIDGE )
                    e.grid(row=t_idx+4, sticky=tk.NSEW)
                    e.insert(tk.END, '%s -> %d' % (str(t_list),unvisited[dest_router]))
                    e.configure(state='readonly')
                    t_idx=t_idx+1;
            if(rd==source_router or source_router==-1):
                tk.Label(window2, text="Source Router").grid(row=0)
                e3 = tk.Entry(window2)
                e3.grid(row=0, column=1)
                b3=tk.Button(window2, text="Submit", width=10, command=callback2)
                b3.grid(row=0, column=2)
            if(rd==dest_router or dest_router==-1):
                tk.Label(window2, text="Destination Router").grid(row=1)
                e4 = tk.Entry(window2)
                e4.grid(row=1, column=1)
                b4=tk.Button(window2, text="Submit", width=10, command=callback2)
                b4.grid(row=0, column=2)
            dijkstra(source_router)
            t_idx=1;
            e = tk.Entry(window2, relief=tk.RIDGE, width=50 )
            e.grid(row=t_idx+3, sticky=tk.NSEW)
            e.insert(tk.END, 'Paths from source router %d to destination router %d:' % (source_router, dest_router) )
            e.configure(state='readonly')
            for t_list in list(dfs_paths( source_router, dest_router)):
                e = tk.Entry(window2, relief=tk.RIDGE )
                e.grid(row=t_idx+4, sticky=tk.NSEW)
                e.insert(tk.END, '%s -> %d' % (str(t_list),unvisited[dest_router]))
                e.configure(state='readonly')
                t_idx=t_idx+1;
        b1=tk.Button(frame, text="Shortest Path", width=10, command=callback1)
        b1.grid(row=0, column=2)
        frame.pack(fill=tk.BOTH, expand=tk.YES)
        canvas.create_window(0,0, anchor = tk.NW, window = frame)
        canvas.pack(fill=tk.BOTH, expand=tk.YES)
        window1.update_idletasks()
        canvas.config(scrollregion=canvas.bbox(tk.ALL))
    b=tk.Button(window, text="Submit", width=10, command=callback)
    b.grid(row=0, column=2)
    router_deleted=-1;
    
#function to display the network topology in a new window    
def network_topology():
    global valid_matrix;
    global source_router
    global dest_router
    global router_deleted
    global adjacency_matrix

    source_router=-1
    dest_router=-1
    router_deleted=-1
    adjacency_matrix=[]
    valid_matrix=False;
    str_router_matrix="";
    name= askopenfilename()
    process_file(name);
    window = tk.Toplevel(root)
    window.title("Network Topology")
    if(len(adjacency_matrix)<8):
        showinfo('No', 'Number of nodes should be greater than or equal to 8') 
        return
    for i in range(len(adjacency_matrix)):
        for j in range(len(adjacency_matrix)):
            if(i==j):
                if(adjacency_matrix[i][j]>0):
                    valid_matrix=False
                    break;
            else:
                if(adjacency_matrix[i][j]>0):
                    valid_matrix=True;
                    break;
    if(valid_matrix==False):
        showinfo('No', 'Invalid Router table. Please upload another file');
        return
    for line in adjacency_matrix :
            for item in line :
                str_router_matrix=str_router_matrix+ "\t" + str(item); 
            l=tk.Label(window,text=str_router_matrix);
            l.pack()
            str_router_matrix=""
    set_distances(adjacency_matrix)

#function to display the connection table in a new window
def connection_table():
    global router_deleted;
    if not adjacency_matrix:
        showinfo('No', 'Connection table cannot be created without building a network topology. Please build a valid topology using Option 1') 
        return
    window1 = tk.Toplevel(root)
    window1.title("Connection Table")
    #make scrollbar for canvas
    cScrollbar = tk.Scrollbar(window1)
    cScrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    canvas = tk.Canvas(window1)

    #attach canvas to scrollbar
    canvas.config(yscrollcommand=cScrollbar.set)
    cScrollbar.config(command=canvas.yview) 
    #make frame and put everything in frame
    frame = tk.Frame(window1)
    #window.config(yscrollcommand=scroll.set)
    #scroll.config(command=window.yview)
    for source_router1 in range(len(adjacency_matrix)):
        print "source_router1:%d" %source_router1
        if(source_router1 == router_deleted):continue
        source_router1= source_router1+1;
        set_distances(adjacency_matrix)
        dijkstra(source_router1)
        print "source_router after dj:%d" %source_router1
        t_list=[];
        """st_label="Connection table for "+str(source_router);
        l=tk.Label(window,text=st_label, justify=tk.LEFT);"""
        row_pos=((source_router1-1)*(len(adjacency_matrix)+2))
        #l.grid(row=row_pos+1)
        for key in interface:
            print "key:%d" %key
            t_list=[]
            list_str=''
            for t in list(set(interface[key])):
                t_list=list(dfs_paths( source_router1, t))
                for s in t_list:
                    if(len(s[1:])>1):
                        if(s[len(s)-1]==key):
                            s=[];
                    if(len(s)>0):
                        list_str=list_str+", "+str(s[1:])
            list_str=list_str.replace(",","",1)
            """l=tk.Label(window,text=str(key)+"\t\t"+list_str, justify=tk.LEFT);
            l.grid(row=key+row_pos)"""
            e1 = tk.Entry(frame, relief=tk.RIDGE, width=50 )
            e1.grid(row=row_pos, sticky=tk.NSEW)
            e1.insert(tk.END, 'Connection table for router %d' % (source_router1))
            e1.configure(state='readonly')
            e = tk.Entry(frame, relief=tk.RIDGE )
            e.grid(row=key+row_pos, sticky=tk.NSEW)
            e.insert(tk.END, '%s\t%s' % (str(key), list_str))
            e.configure(state='readonly')
        e2 = tk.Entry(frame, relief=tk.RIDGE )
        e2.grid(row=row_pos+len(adjacency_matrix)+1, sticky=tk.NSEW)
        e2.insert(tk.END, '\n')
        e2.configure(state='readonly')
    frame.pack(fill=tk.BOTH, expand=tk.YES)
    canvas.create_window(0,0, anchor = tk.NW, window = frame)
    canvas.pack(fill=tk.BOTH, expand=tk.YES)
    window1.update_idletasks()
    canvas.config(scrollregion=canvas.bbox(tk.ALL))
        
#function to display the destination router in a new window    
def destination_router():
    if not adjacency_matrix:
        showinfo('No', 'Shortest Path cannot be created without building a network topology. Please build a valid topology using Option 1') 
        return
    window = tk.Toplevel(root)
    window.title("Shortest Path")
    tk.Label(window, text="Source Router").grid(row=0)
    e1 = tk.Entry(window)
    e1.grid(row=0, column=1)
    tk.Label(window, text="Destination Router").grid(row=1)
    e2 = tk.Entry(window)
    e2.grid(row=1, column=1)
    def callback():
        st_list=''
        global e_len;
        global dest_router;
        global source_router;
        
        source_router=int(e1.get())
        dest_router=int(e2.get())
        if source_router not in nodes:
            showinfo('No', 'Invalid Router.! Please enter a valid source router') 
            return
        if dest_router not in nodes:
            showinfo('No', 'Invalid Router.! Please enter a valid destination router') 
            return
        
        
        dijkstra(source_router)
        t_idx=1;
        e = tk.Entry(window, relief=tk.RIDGE, width=80 )
        e.grid(row=t_idx+3, sticky=tk.NSEW)
        e.insert(tk.END, 'Paths from source router %d to destination router %d:' % (source_router, dest_router) )
        e.configure(state='readonly')
        for t_list in list(dfs_paths( source_router, dest_router)):
            st_list=st_list+'%d. %s -> %d; ' % (t_idx, str(t_list),unvisited[dest_router])
            t_idx=t_idx+1;
        t_idx=1
        e = tk.Entry(window, relief=tk.RIDGE)
        e.grid(row=t_idx+4, sticky=tk.NSEW)
        e.insert(tk.END, st_list)
        e.configure(state='readonly')
        st_list='';
    b=tk.Button(window, text="Submit", width=10, command=callback)
    b.grid(row=2, column=1)
    
    
    
#function to quit the simulation            
def quit():
    if askyesno('Verify', 'Really quit?'):
        root.destroy()
    else:
        showinfo('No', 'Quit has been cancelled')
        
#main function to display the commands that will be displayed as a welcome screen
root = tk.Tk()
root.title("Link State Routing")
root.state('zoomed')
tk.Label(root, text="CS542 Link State Routing Simulation",fg="blue",  font="Times 14 bold").pack()
tk.Button(text='1. Create a Network Topology', command=network_topology, width=40, font="Times 12 bold").pack(pady=10)
tk.Button(text='2. Build a Connection Table', command=connection_table, width=40 , font="Times 12 bold").pack(pady=10)
tk.Button(text='3. Shortest Path to Destination Router', command=destination_router, width=40, font="Times 12 bold").pack(pady=10)
tk.Button(text='4. Modify a topology', command=modify_topology, width=40, font="Times 12 bold").pack(pady=10)
tk.Button(text='5. Exit', command=quit, width=40, font="Times 12 bold").pack(pady=10)


root.mainloop()



