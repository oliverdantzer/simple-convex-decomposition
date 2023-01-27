import pygame
import pygamedraw
import vintersect
import numpy as np
import vmath
import vector

# return indices of all of list except indices[i] and indices[i] - 1
def all_indices_except_around(list_length: int, indices: list[int]):
    def idx_at(i, length):
        if i == -1:
            return length - 1
        elif i == length:
            return 0
        else:
            return i
    
    if type(indices) == int:
        indices = [indices]
    do_not_add = set()
    for index in indices:
        if index < 0 or index >= list_length:
            raise ValueError("Invalid index: outside of list range")
        for idx in (idx_at(index - 1, list_length), index):  # if testing indices[i]+1, add: , idx_at(index + 1, list_length)
            do_not_add.add(idx)
    updated_indices = [i for i in range(list_length)]
    for idx in do_not_add:
        updated_indices.remove(idx)
    return updated_indices



# return 2 lists, one is elements of lis in range including range endpoints, other is elements outside of range including range endpoints
def partition_lists(lis, range):
    if range[1] < range[0]:
        # partition 1
        p1 = lis[range[0]:]
        p1.extend(lis[:range[1] + 1])

        # partition 2
        p2 = lis[range[1]:range[0] + 1]
    else:
        # partition 1
        p1 = lis[range[0]:range[1] + 1]

        # partition 2
        p2 = lis[range[1]:]
        p2.extend(lis[:range[0] + 1])

    if len(p1) < 3 or len(p2) < 3:
        raise ValueError("Invalid polygon partitioning: partition size must be 3 or greater")

    return [p1, p2]





class Polygon:
    # if array is list[vmath.Vector] it will be treated 
    def __init__(self, point_array: list[vmath.Vector]):
        if type(point_array) != list:
            raise TypeError("array must be of type list[vmath.Vector]")
        if len(point_array) < 3:
            raise ValueError("array must be of size 3 or greater to be a polygon.")
        if type(point_array[0]) == vmath.Vector:
            self.point_array = point_array
            self.vector_array = []  # ordered array of all pos+dir vectors in the polygon

            # iterate through pos vectors to create pos+dir vectors
            for i in range(len(point_array) - 1):
                self.vector_array.append(vector.Vector(point_array[i], point_array[i + 1] - point_array[i]))  # vector between pos and next pos is dir vector
            # add last pos+dir vector connecting last point and first point
            self.vector_array.append(vector.Vector(point_array[len(point_array) - 1], point_array[0] - point_array[len(point_array) - 1]))
        else:
            raise TypeError("array must be of type list[vmath.Vector]")
        
    

    def is_simple(self) -> bool:
        # for each vector, test if point at pos intersects the next vector
        if vector.Vector(self.vector_array[len(self.vector_array) - 1].pos, vmath.Vector([0, 0])).intersects(self.vector_array[0]):
                    return False
        for i in range(len(self.vector_array) - 1):
            if vector.Vector(self.vector_array[i].pos, vmath.Vector([0, 0])).intersects(self.vector_array[i + 1]):
                    return False

        print(0)
        for j in range(0 + 2, len(self.vector_array) - 1):
            print(0, j)
            if self.vector_array[0].intersects(self.vector_array[j]):
                return False
        print("i")
    
        #compare each vector with all except ones next to them
        for i in range(1, len(self.vector_array)):
            for j in range(i + 2, len(self.vector_array)):
                print(i, j)
                if self.vector_array[i].intersects(self.vector_array[j]):
                    return False
        
        return True


    def draw(self, screen) -> None:
        for vect in self.vector_array:
            vect.draw(screen)
    
    def __repr__(self) -> str:
        return(str(self.vector_array))



class SimplePolygon:
    def __init__(self, p: Polygon) -> None:
        if not p.is_simple():
            print(p.vector_array)
            raise ValueError("p must be a simple polygon")
        self.p = p
        self.direction_from_first_elem: vmath.Side # from first elem and going forwards, this side of the side will face into the polygon's area
        self.is_convex: bool = True

        first_side = self.p.vector_array[0].dir.side_relative_to(self.p.vector_array[-1].dir)
        angle_sum = self.p.vector_array[0].dir.angle_relative_to(self.p.vector_array[-1].dir).to_float()
        for i in range(1, len(self.p.vector_array)):
            if self.p.vector_array[i].dir.side_relative_to(self.p.vector_array[i - 1].dir) != first_side:
                self.is_convex = False
            angle_sum += self.p.vector_array[i].dir.angle_relative_to(self.p.vector_array[i - 1].dir).to_float()
        if angle_sum == 0:
            for i in range(len(self.p.vector_array)):
                print(self.p.vector_array[i].pos)
            print(self.is_convex)
            # raise ValueError("Sum of polygon angles == 0")
        else:
            self.direction_from_first_elem = vmath.Side(angle_sum)
    
    """
    def is_convex(self):
        side = self.p.vector_array[len(self.p.vector_array) - 1].dir.side_relative_to(self.p.vector_array[0].dir)
        for i in range(len(self.p.vector_array) - 1):
            if self.p.vector_array[i].dir.side_relative_to(self.p.vector_array[i + 1].dir) not in (0, side):
                return False
        return True
    """
    
    def partition_vector(self, start: int, end: int) -> vector.Vector:
        pos = self.p.vector_array[start].pos
        dir = self.p.vector_array[end].pos - pos
        return vector.Vector(pos, dir)

    def valid_partition(self, start: int, end: int) -> bool:
        if end < start:
            end, start = start, end
        partition_vector = self.partition_vector(start, end)
        # return false if vector points outside of polygon immediately
        print(partition_vector.dir.side_relative_to(self.p.vector_array[start].dir).dir)
        print(self.direction_from_first_elem.dir)

        if end in (start - 1, start, start + 1):
            return False
        
        part_uv = partition_vector.dir.unit_vector()
        if part_uv in (self.p.vector_array[start - 1].dir.unit_vector(), self.p.vector_array[start].dir.unit_vector()):
            print("Vector equal to start/start-1")
            return False

        if not partition_vector.dir.side_of_angle(self.p.vector_array[start - 1].dir, self.p.vector_array[start].dir, vmath.Side(-self.direction_from_first_elem.dir)):
            print("Vector points wrong way")
            return False
        
        # if partition_vector.dir.side_relative_to(self.p.vector_array[start].dir).dir != self.direction_from_first_elem.dir:
        #     print("Vector points wrong way relative to start vector")
        #     return False
        # if partition_vector.dir.side_relative_to(self.p.vector_array[start - 1].dir).dir != self.direction_from_first_elem.dir:
        #     print("Vector points wrong way relative to vector previous to start vector")
        #     return False
        
        #return false if vector intersects any vector except the two it starts next to and the two it ends next to
        for i in all_indices_except_around(len(self.p.vector_array), (start, end)):
            if partition_vector.intersects(self.p.vector_array[i]):
                print("Vector intersects another vector")
                return False
        
        return True

    def find_partition(self):
        for start in range(len(self.p.vector_array)):
            for end in all_indices_except_around(len(self.p.vector_array), start):
                if self.valid_partition(start, end):
                    return (start, end)
        print(self.p)
        raise ValueError("No partition found")
            


    def draw(self, screen):
        self.p.draw(screen)


class ConvexPolygon:
    def __init__(self, sp: SimplePolygon):
        if not sp.is_convex:
            raise ValueError("sp must be a convex simple polygon")
        self.sp = sp

    def draw(self, screen):
        self.sp.draw(screen)


class ConvexPolygonsGroup:
    def __init__(self, sp: SimplePolygon):
        def partition_convex(point_array: list[vmath.Vector], group: list) -> None:
            sp = SimplePolygon(Polygon(point_array))
            if sp.is_convex:
                group.append(ConvexPolygon(sp))
                return
            
            partition_range = sp.find_partition()
            partitions = partition_lists(point_array, partition_range)
            for partition in partitions:
                try:
                    test = SimplePolygon(Polygon(partition))
                except:
                    print(Polygon(point_array).vector_array, partition_range)
                partition_convex(partition, group)
        
        if type(sp) != SimplePolygon:
            raise TypeError("sp must be polygon.SimplePolygon")

        self.group = []
        partition_convex(sp.p.point_array, self.group)

    def draw(self, screen):
        for cp in self.group:
            cp.draw(screen)
