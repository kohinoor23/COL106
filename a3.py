#The program solves the problem statement by using Range Trees. We create a primary tree (X tree) of points based on 
#order of #x coordinates, and every node in this tree contains reference to a list of nodes in subtree rooted at this node.
#This list is sorted ob based of y coordinates of tuples.


class Node:     
    def __init__(self, val, left, right, ylist) -> None:
        self.val=val
        self.left=left
        self.right=right
        self.ylist=ylist

def in_order(root, iolist):    #Appends the inorder traversal of tree rooted at node into iolist
    if not root:
        return
    
    in_order(root.left, iolist)
    iolist.append(root.val)
    in_order(root.right, iolist)

def merge_sorted(l1, l2):      #Returns a sorted list by merging two sorted lists
    n1=len(l1)
    n2=len(l2)
    l=[]
    a=0
    b=0

    for i in range(n1+n2):
        if a>=n1:
            l.extend(l2[b:])
            break

        if b>=n2:
            l.extend(l1[a:])
            break

        if l1[a][1]<l2[b][1]:
            l.append(l1[a])
            a+=1

        else:
            l.append(l2[b])
            b+=1

    return l

def CreateYList(val, l1, l2):                 #Creates ylist associated with a node in X tree.
    l=merge_sorted(merge_sorted(l1, l2), [val])
    return l 


def tree_leaf(val, left, right, ytree):       #Returns a left node of X tree.
    node=Node(val, left, right, [val])
    return node

def BuildDB(S):                              #Returns the root to the AVL tree (X tree) created using tuples in list S.
    if len(S)==0:
        return None

    if len(S)==1:
        return tree_leaf(S[0], None, None, S[0])

    

    x=S[len(S)//2]
    L=S[:len(S)//2]
    R=S[1+len(S)//2:]
    Ltree=BuildDB(L)
    Rtree=BuildDB(R) if len(R)>0 else None

    tree=Node(x, Ltree, Rtree, CreateYList(x, Ltree.ylist, Rtree.ylist if Rtree else []))
    return tree

def Parents(root, x):                     #Returns the list of ancestors(or possible ancestors) of node with value x(if x not in tree)
    l=[]
    
    while root is not None:
        l.append(root)
        if root.val[0]==x:
            break

        elif root.val[0]>x:
            root=root.left

        else:
            root=root.right
    
    return l

def getLCA(Tree, x1, x2):                #Returns (possible)Least common ancestor of node with values x1, x2(if absent).
    L1=Parents(Tree, x1)
    L2=Parents(Tree, x2)

    N1=len(L1)
    N2=len(L2)
    if N1>N2:
        L1,L2=L2,L1
        N1,N2=N2,N1

    for i in range(0, N1):
        if L2[N1-i-1]==L1[-i+N1-1]:
            return L2[N1-i-1]

def is_Leaf(node:Node):
    return node.left==node.right==None

def in_range(x, r1, r2):                        
    return r1<=x<=r2


def in_range_tup(t, x1, x2, y1, y2):                            
    return in_range(t[0], x1, x2) and in_range(t[1], y1, y2)


def binary_search(arr, x, enable=0):      #enable to toggle least upper bound or greatest lower bound in case x does not exist.
    low = 0
    high = len(arr) - 1
    mid = 0

    while low <= high:

        mid = (high + low) // 2

        if arr[mid][1] < x:
            low = mid + 1

        elif arr[mid][1] > x:
            high = mid - 1

        else:
            return mid

    if enable==0:
        if arr[mid][1]>x:
            return mid

        else:
            return mid+1 if mid+1<len(arr) else -1

    else:
        if arr[mid][1]<x:
            return mid

        else:
            return mid-1 if mid-1>=0 else -1

def RangeQuery_Y(arr, r1, r2, l):         #Appends tuples (x,y) in arr with r1<=y<=r2 to answer list 
    y1=binary_search(arr, r1, 0)
    y2=binary_search(arr, r2, 1)

    if y1==-1 or y2==-1:
        return

    else:
        l.extend(arr[y1: y2+1])  

#RangeQuery_X
#First, we find nodes v1 and v2 closest to end points of the range of allowed x coordinates. 
#Then, we visit all nodes on path from lca to v1 and v2. If any node lies in the given x range, we apply RangeQuery_Y
#to appropriate child of this node.
def RangeQuery_X(Tree, x1, x2, y1, y2, l):            
    node_lca=getLCA(Tree, x1, x2)
    if in_range_tup(node_lca.val, x1, x2, y1, y2):
        l.append(node_lca.val) 

    v=node_lca.left
    if v:
        while is_Leaf(v)==False:
            if in_range_tup(v.val, x1, x2, y1, y2):
                l.append(v.val)
            if x1<=v.val[0]:
                if v.right:
                    RangeQuery_Y(v.right.ylist, y1, y2, l)
                
                if v.left:
                    v=v.left   
                else:
                    break          
                

            else:
                if v.right:
                    v=v.right
                else:
                    break
        if is_Leaf(v):
            if in_range_tup(v.val, x1, x2, y1, y2):
                l.append(v.val) 

    v=node_lca.right
    if v:            
        while is_Leaf(v)==False:
            if in_range_tup(v.val, x1, x2, y1, y2):
                l.append(v.val)  
            if v.val[0]<=x2:
                if v.left:
                    RangeQuery_Y(v.left.ylist, y1, y2, l)

                if v.right:
                    v=v.right
                else:
                    break

            else:
                if v.left:
                    v=v.left

                else:
                    break
            
        if is_Leaf(v):
            if in_range_tup(v.val, x1, x2, y1, y2):
                l.append(v.val)   

class PointDatabase:
    def __init__(self, pointlist):
        pointlist.sort()
        self.tree=BuildDB(pointlist)

    def searchNearby(self, tup, d):
        if self.tree==None:
            return []
        l=[]
        RangeQuery_X(self.tree, tup[0]-d, tup[0]+d, tup[1]-d, tup[1]+d, l)
        return l











    
