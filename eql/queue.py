
class Queue(list):
    def push(self, t):
        self.append(t)
    def pop(self):
        return super().pop(0)
    def empty(self):
        return len(self) == 0

class Stack(Queue):
    def pop(self):
        return list.pop(self, len(self) - 1)
    def peek(self):
        if not self:
            return None
        return self[-1]
