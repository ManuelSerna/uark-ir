#************************************************
# Queue class
# FIFO
# This implementation assumes that every unused element in the queue is None.
# Author: Manuel Serna-Aguilera
#************************************************

class Queue():
    #=============================
    # Init
    '''
    Input:
        length: length of queue
    Return: NA
    '''
    #=============================
    def __init__(self, length):
        self.length = length
        self.head = 0 # head 'pointer', stores first element to be removed/dequeued
        self.tail = 0 # tail 'pointer', stores most recently-inserted element
        self.Q = []   # Q is a py list of constant size
        
        for i in range(length):
            self.Q = self.Q + [None]

    #=============================
    '''
    Check if queue is full
    
    - If head is at index zero and tail happens to index this as the next "available" spot, then the the queue is full with the head at the beginning and the last element inserted is at the very end of the array.
    We do this by utilizing our assumption that there are no more null elements.
    
    - If both above conditions are false, thus we can insert.
    
    Input: NA
    Return: bool
    '''
    #=============================
    def is_full(self):
        if self.head == self.tail and self.Q[self.tail] != None:
            return True
        else:
            return False
    
    #=============================
    # Check if queue is empty
    '''
    If value at head is null, thus our queue must be empty.
    
    Input: NA
    Return: bool
    '''
    #=============================
    def is_empty(self):
        if self.Q[self.head] == None:
            return True
        else:
            return False
    
    #=============================
    # Insert/enqueue
    '''
    Input:
       x: element to insert
    Return: NA
    '''
    #=============================
    def enqueue(self, x):
        if self.is_full():
            #raise Exception("Queue overflow!")
            #print(' NOTICE: Too full! Not insering {}'.format(x))
            pass
        else:
            self.Q[self.tail] = x
            if self.tail == self.length-1:
                self.tail = 0
            else:
                self.tail += 1
    
    #=============================
    # Return/dequeue
    '''
    Input: NA
    Return:
        x: element at position 'self.head'
         -OR-
        None: if queue is empty
    '''
    #=============================
    def dequeue(self):
        if self.is_empty():
            return None
        else:
            x = self.Q[self.head]
            self.Q[self.head] = None # maintain assumption
            if self.head == self.length-1:
                self.head = 0
            else:
                self.head += 1
            return x
    
    #=============================
    # Print contents of queue
    # Input: NA
    # Return: NA
    #=============================
    def print_queue(self):
        print(self.Q)
