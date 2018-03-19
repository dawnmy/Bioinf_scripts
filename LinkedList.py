class ListNode(object):
    def __init__(self, x):
        self.val = x
        self.next = None


class LinkedList(object):
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def __str__(self):
        current = self.head
        values = []
        while current:

            values.append(str(current.val))
            current = current.next

        return " -> ".join(values)

    def add(self, val):
        new_node = ListNode(val)
        if self.head is None:
            self.head = new_node
        else:
            self.tail.next = new_node

        self.tail = new_node
        self.size += 1

    def rm_value(self, v):
        previous = None
        current = self.head

        while current is not None:
            if current.val == v:
                if previous is None:
                    self.head = current.next
                else:
                    previous.next = current.next

                self.size -= 1

            previous = current
            current = current.next

    def rm_index(self, idx):
        previous = None
        current = self.head
        current_idx = 0

        while current is not None:
            if current_idx == idx:
                if previous is None:
                    self.head = current.next
                else:
                    previous.next = current.next

                self.size -= 1

            previous = current
            current = current.next
            current_idx += 1

    def insert(self, idx, v):
        current = self.head
        previous = None
        current_idx = 0
        node = ListNode(v)

        while current is not None:
            if current_idx == idx:
                if previous is None:
                    self.head = node
                    # current.next
                else:
                    previous.next = node

                node.next = current
                self.size += 1

            previous = current
            current = current.next
            current_idx += 1

    def reverse(self):
        previous = None
        current = self.head
        while current:
            tmp = current
            current = current.next
            tmp.next = previous
            previous = tmp
            self.head = previous


if __name__ == "__main__":
    LL = LinkedList()
    for i in range(0, 10):
        LL.add(i)
