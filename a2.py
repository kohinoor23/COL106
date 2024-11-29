class HeapPriorityQueue:

    def __init__(self, contents, node_pos):
        self._data=contents[:]

    #node_pos is an array whose ith element gives the index of [i, T[i]] in the heap.
        self._node_pos=node_pos
        
        if len(self._data)>1:
            self.BuildHeap()

    def _parent(self, j):  #Returns index of parent of node in the HEAP
        return (j-1)//2

    def _left(self, j):  #Returns index of left child of nide in the HEAP
        return 2*j+1

    def _right(self, j):
        return 2*j+2      #Return index of right child of node in the HEAP

    def __len__ (self):
        return len(self._data)

    def _has_left(self, j):
        return self._left(j) < len(self._data) # index beyond end of list?

    def _has_right(self, j):
        return self._right(j) < len(self._data)
    #Swaps 2 nodes in the heap
    def _swap(self, i, j):               
        self._data[i], self._data[j]=self._data[j], self._data[i]          
        swap_nodes(self._node_pos, self._data[i][0], self._data[j][0])    #Update position array

    #Heap up jth node in the heap
    def HeapUp(self, j):
        parent=self._parent(j)
        if j>0:
            if order_gt(self._data[parent], self._data[j]):
                self._swap(j, parent)
                self.HeapUp(parent)

    #Heap down jth node in the heap
    def HeapDown(self, j):
        if self._has_left(j):
            left=self._left(j)
            small_child=left
            if self._has_right(j):
                right=self._right(j)
                if order_gt(self._data[left],self._data[right]):
                    small_child=right
                    
            
            if order_gt(self._data[j], self._data[small_child]) or self._data[j][1]<0:
                self._swap(j, small_child)
                self.HeapDown(small_child)
            
    #Build heap using bottom up heap construction method(FastBuildHeap)
    def BuildHeap(self):
        start=self._parent(len(self)-1)
        for j in range(start, -1, -1):
            self.HeapDown(j)
    
    #Returns minimum element in the heap
    def min(self):
    

        item=self._data[0]
        return item
    
    #Returns the node_pos array
    def node_pos(self):
        return self._node_pos

    #Changes the value of a node in the heap and moves it to ensure min_heap structure.
    def Change_Key(self, i, t):
        t1=self._data[self._node_pos[i]][1]
        self._data[self._node_pos[i]][1]=t
        if 0<=t<=t1 or (t1<0 and t>0):
            self.HeapUp(self._node_pos[i])
        
        else:
            self.HeapDown(self._node_pos[i])


    #Set next collision time = -1(Treated as infinity/no collision) after collision.
    def collided_1(self):
        self._data[0][1]=-1

    #Makes changes to the velocities, positions and times of last collision of the 2 objects who collide.
    def simulate(self, collide, balls, times, time):
        m1, x1, u1=balls[collide[0]]
        m2, x2, u2=balls[collide[0]+1]

        #Updating velocities
        balls[collide[0]][2]=v_one(m1, m2, u1, u2)
        balls[collide[0]+1][2]=v_two(m1, m2, u1, u2)

        #Updating positions
        balls[collide[0]][1]+=u1*(collide[1]-(times[collide[0]]))
        balls[collide[0]+1][1]=balls[collide[0]][1]

        #Updating times of last collisions
        times[collide[0]]=collide[1]
        times[collide[0]+1]=collide[1] 
    
#Function to compare two nodes in the heap.
def order_gt(l1, l2):
        i1, t1=l1
        i2, t2=l2
        if t2>0:
            if (t2<t1) or (t2==t1 and i2<i1) or t1<0:
                return 1
        return 0

#Swapping two ndoes in a list
def swap_nodes(l,a,b):
    l[a], l[b]= l[b], l[a]

#Find collision time between 2 objects.
def col_time(l1, l2):
    m1, x1, v1=l1
    m2, x2, v2=l2
    if v1==v2:
        return -1
    return ((x2-x1)/(v1-v2) if (x2-x1)/(v1-v2)>=0 else -1)

#Helper to calculate post-collision velocity
def v_two(m1, m2, u1, u2):
    return ((2*m1*u1)-(m1-m2)*u2)/(m1+m2)

def v_one(m1,m2,u1,u2):
    return ((2*m2*u2)+(m1-m2)*u1)/(m1+m2)

def t_right_col():
    pass


def listCollisions(M,x,v,m,T):
    n_balls=len(M)
    balls=[]                                    #Array to store info. about each object.
    Collisions=[]
    time=0
    for i in range(n_balls):
        balls.append([M[i], x[i], v[i]])

    times=[0]*n_balls                           #Array to store time of last collision for each object
    node_pos=list(range(0,n_balls-1))
    heap_init=[]

    for i in range(n_balls-1):
        heap_init.append([i, col_time(balls[i], balls[i+1])])

    heap=HeapPriorityQueue(heap_init, node_pos)      #The heap used for solving the problem.
    cnt=0                                            #Counter for number of collisions
    
    
    while (cnt<m and time<=T):
        
        #Extracting time and partice which collides
        collide=(heap.min())[:]

        #Update running time of simulation
        time=collide[1]
        
        if time>T:
            break

        if collide[1]>=0:
            heap.simulate(collide, balls, times, time)
            Collisions.append((round(collide[1],4), collide[0], round(balls[collide[0]][1], 4)))
            heap.collided_1()      #Set time after collision to -1
            heap.HeapDown(heap._node_pos[collide[0]])
            cnt+=1
        
        else:
            break

        #Making changes to neighbours of particles which collided.
        if collide[0]>0 and collide[0]<=n_balls-3:
            m0, x0, v0=balls[collide[0]-1]
            x0=x0+v0*(time-times[collide[0]-1])
            new_t=(time + col_time([m0, x0, v0], balls[collide[0]]) if col_time([m0, x0, v0], balls[collide[0]])>=0 else -1)
            heap.Change_Key(collide[0]-1, new_t)

            m4, x4, v4=balls[collide[0]+2]
            x4=x4+v4*(time-times[collide[0]+2])
            new_t=(time + col_time(balls[collide[0]+1], [m4, x4, v4]) if col_time(balls[collide[0]+1], [m4, x4, v4])>=0 else -1)
            heap.Change_Key(collide[0]+1, new_t)

            

        elif collide[0]>n_balls-3 and collide[0]>0:
            m0, x0, v0=balls[collide[0]-1]
            x0=x0+v0*(time-times[collide[0]-1])
            new_t=(time + col_time([m0, x0, v0], balls[collide[0]]) if col_time([m0, x0, v0], balls[collide[0]])>=0 else -1)
            heap.Change_Key(collide[0]-1, new_t)

        else:
            m4, x4, v4=balls[collide[0]+2]
            x4=x4+v4*(time-times[collide[0]+2])
            new_t=(time + col_time(balls[collide[0]+1], [m4, x4, v4]) if col_time(balls[collide[0]+1], [m4, x4, v4])>=0 else -1)
            heap.Change_Key(collide[0]+1, new_t)

    #Return the required solution list.
    return(Collisions)

            
        
        






# print(listCollisions([1.0, 5.0], [1.0, 2.0], [3.0, 5.0], 100, 100.0))
# print(listCollisions([1.0, 1.0, 1.0, 1.0], [-2.0, -1.0, 1.0, 2.0], [0.0, -1.0, 1.0, 0.0], 5,5.0))
# print(listCollisions([10000.0, 1.0, 100.0], [0.0, 1.0, 2.0], [0.0, 0.0, -1.0], 6, 10.0))
# print(listCollisions([10000.0, 1.0, 100.0], [0.0, 1.0, 2.0], [0.0, 0.0, -1.0], 100, 1.5))






    
