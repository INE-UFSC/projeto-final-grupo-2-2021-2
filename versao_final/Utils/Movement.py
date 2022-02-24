def gerar_equação_vetorial_reta(p1, p2):
    def funcao(x):
        sub = ((p2[0] - p1[0]) * x, (p2[1] - p1[1]) * x)
        ponto = (p1[0] + sub[0], p1[1] + sub[1])
        return ponto

    return funcao


class NodeHeap():
    def __init__(self, index, value) -> None:
        self.value = value
        self.index = index

    @property
    def parent(self):
        return (self.index-1) // 2

    @property
    def left(self):
        return self.index * 2 + 1

    @property
    def right(self):
        return self.index * 2 + 2


class MinHeap():
    def __init__(self, array: list) -> None:
        self.heap = array

    def printHeap(self) -> None:
        for node in self.heap:
            print(node.value.f, node.value.position)

    def insert(self, value) -> None:
        newIndex = len(self.heap)
        newNode = NodeHeap(newIndex, value)
        self.heap.append(newNode)

        self.__increase_value(newNode)

    def minimun(self) -> int:
        if len(self.heap) > 0:
            return self.heap[0].value

    def popMinimum(self) -> int:
        if len(self.heap) == 0:
            return None

        min = self.heap.pop(0)  # Extract the min element

        if len(self.heap) > 0:
            last = self.heap.pop()  # Extract the last element

            last.index = 0  # Update the index of node object
            self.heap.insert(0, last)

            self.__decrease_value(last)  # Heapify the node object

        return min.value

    def update(self, index, new_value) -> None:
        if index >= len(self.heap):
            return None

        node = self.heap[index]  # Get the updated node
        prev_value = node.value  # Get the prev value
        node.value = new_value  # Update the value

        if new_value > prev_value:
            self.__increase_value(node)
        else:
            self.__decrease_value(node)

    def __increase_value(self, node: NodeHeap) -> None:
        # While node not the first and his parent is minor
        while node.index >= 1 and self.heap[node.parent].value > node.value:
            self.__swap(self.heap, node.index, node.parent)

    def __decrease_value(self, node: NodeHeap) -> None:
        while True:
            # If left child runs out
            if node.left >= len(self.heap):
                break

            # Only left child
            if node.right >= len(self.heap):
                nodeLeft = self.heap[node.left]
                if nodeLeft.value < node.value:
                    self.__swap(self.heap, node.index, node.left)
                else:
                    # If current node is bigger
                    break

            # Both children
            else:
                nodeLeft = self.heap[node.left]
                nodeRight = self.heap[node.right]

                # If the current node is lesser, finish the decrease
                if node.value < max(nodeLeft.value, nodeRight.value):
                    break

                # if left child is lesser, swap them
                if nodeLeft.value < nodeRight.value:
                    self.__swap(self.heap, node.index, node.left)
                # if right child is lesser, swap them
                else:
                    self.__swap(self.heap, node.index, node.right)

    def __swap(self, array, i, j):
        nodeI = self.heap[i]
        nodeJ = self.heap[j]

        # Inverte a posição do nodeI e nodeJ no array
        array[i], array[j] = array[j], array[i]
        # Atualiza a posição dos node dentro do objeto
        nodeJ.index, nodeI.index = nodeI.index, nodeJ.index

    def __len__(self) -> int:
        return len(self.heap)


class Node:
    def __init__(self, position: tuple, parent) -> None:
        self.parent: Node = parent
        self.position = position

        self.f = 0  # Distance
        self.g = 0  # Start-Node
        self.h = 0  # Node-End

    def __gt__(self, x) -> bool:
        if type(x) == type(self):
            if self.f == x.f:
                return self.h > self.h
            else:
                return self.f > x.f
        else:
            print('Invalid Type')
            return False

    def __lt__(self, x) -> bool:
        if type(x) == type(self):
            if self.f == x.f:
                return self.h < self.h
            else:
                return self.f < x.f
        else:
            print('Invalid Type')
            return False

    def __le__(self, x) -> bool:
        if type(x) == type(self):
            if self.f == x.f:
                return self.h <= self.h
            else:
                return self.f <= x.f
        else:
            print('Invalid Type')
            return False

    def __ge__(self, x) -> bool:
        if type(x) == type(self):
            if self.f == x.f:
                return self.h >= self.h
            else:
                return self.f >= x.f
        else:
            print('Invalid Type')
            return False

    def __eq__(self, x) -> bool:
        if type(x) == type(self):
            return self.position == x.position
        else:
            print('Invalid Type')
            return False

    def __ne__(self, x) -> bool:
        if type(x) == type(self):
            return self.position != x.position
        else:
            print('Invalid Type')
            return False


class AStar:
    def __init__(self, matrix: list, valid_points: list) -> None:
        self.__matrix = matrix
        self.__x = len(matrix)
        self.__y = len(matrix[0])
        self.__end = ()
        self.__open_list = MinHeap([])
        self.__closed_nodes = []
        self.__valid_points = valid_points

    def search_path(self, start_position: tuple, end_position: tuple, diagonal=False) -> list:
        if not self.__validate_positions([start_position, end_position]):
            print('Input inválido')
            return []

        start_node = Node(start_position, None)

        self.__open_list = MinHeap([])
        self.__closed_nodes = []

        self.__open_list.insert(start_node)
        self.__end = end_position

        while len(self.__open_list) > 0:
            current_node = self.__open_list.popMinimum()

            x = current_node.position[0]
            y = current_node.position[1]

            self.__closed_nodes.append(current_node)

            if self.__check_finish(current_node, end_position):
                return self.__get_traceback(start_node, current_node)

            children = self.__search_children_sides(current_node)
            for child in children:
                self.__update_queue_side(current_node, child)

            if diagonal:
                children = self.__search_children_diagonal(current_node)
                for child in children:
                    self.__update_queue_diagonal(current_node, child)

    def __search_children_sides(self, node: Node) -> list:
        children = []
        possible_positions = [
            (node.position[0], node.position[1] - 1),
            (node.position[0] - 1, node.position[1]),
            (node.position[0], node.position[1] + 1),
            (node.position[0] + 1, node.position[1]),
        ]

        for position in possible_positions:
            if self.__validate_position(position):
                if self.__not_in_closed(position):
                    child_node = Node(position, node)
                    children.append(child_node)

        return children

    def __search_children_diagonal(self, node: Node) -> list:
        children = []
        possible_positions = [
            (node.position[0] - 1, node.position[1] - 1),
            (node.position[0] + 1, node.position[1] + 1),
            (node.position[0] - 1, node.position[1] + 1),
            (node.position[0] + 1, node.position[1] - 1),
        ]

        for position in possible_positions:
            if self.__validate_position(position):
                if self.__not_in_closed(position):
                    child_node = Node(position, node)
                    children.append(child_node)

        return children

    def __update_queue_side(self, current_node, child: Node) -> None:
        child.g = current_node.g + 1
        child.h = ((child.position[0] - self.__end[0]) ** 2) + \
            ((child.position[1] - self.__end[1]) ** 2)
        child.f = child.g + child.h

        for index, heapNode in enumerate(self.__open_list.heap):
            if heapNode.value == child:
                if heapNode.value.g > child.g:
                    heapNode.value.parent = current_node
                    heapNode.value.g = current_node.g + 1
                    self.__open_list.update(index, child)
                    return None
                else:
                    return None

        self.__open_list.insert(child)

    def __update_queue_diagonal(self, current_node, child: Node) -> None:
        child.g = current_node.g + 1.5
        child.h = ((child.position[0] - self.__end[0]) ** 2) + \
            ((child.position[1] - self.__end[1]) ** 2)
        child.f = child.g + child.h

        node, index = self.__get_if_in_open(child)
        if node == None:
            self.__open_list.insert(child)
            return None
        else:
            if node.g > child.g:
                node.parent = current_node
                node.g = current_node.g + 1
                self.__open_list.update(index, child)

        for index, heapNode in enumerate(self.__open_list.heap):
            if heapNode.value == child:
                if heapNode.value.g > child.g:
                    heapNode.value.parent = current_node
                    heapNode.value.g = current_node.g + 1
                    self.__open_list.update(index, child)
                    return None
                else:
                    return None

        self.__open_list.insert(child)

    def __check_finish(self, current_node, end_position) -> bool:
        return current_node.position == end_position

    def __get_traceback(self, start_node: Node, current_node: Node):
        path = []
        current = current_node

        while current != start_node:
            path.insert(0, current.position)
            current = current.parent

        return path

    def __validate_positions(self, position_list: list) -> bool:
        for position in position_list:
            valid = self.__validate_position(position)
            if not valid:
                return False
        return True

    def __validate_position(self, position: tuple) -> bool:
        if len(position) != 2:
            return False

        if position[0] < 0 or position[0] > self.__x - 1:
            return False

        if position[1] < 0 or position[1] > self.__y - 1:
            return False

        if self.__matrix[position[0]][position[1]] not in self.__valid_points:
            return False

        return True

    def __not_in_closed(self, position: tuple):
        for node in self.__closed_nodes[::-1]:
            if node.position == position:
                return False
        return True

    def __get_if_in_open(self, position):
        for index, node in enumerate(self.__open_list.heap[::-1]):
            if node.value.position == position:
                return node.value, index

        return None, None
