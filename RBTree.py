from Const import Const

# c = Const(dict={'_BLACK': True, '_RED': False})


class RBNode:
	def __init__(self, key, color=Const.BLACK):
		self.key = key
		self.color = color
		self.pre = None
		self.left = None
		self.right = None


class BinTree:
	def __init__(self):
		self.root = None
	
	def print_tree(self, cur, output_format, indent='', last='updown'):
		if cur is None:
			return
		content = output_format(cur)
		
		next_indent = '{0}{1}{2}'.format(indent, ' ' if 'up' in last else '│', " " * len(content))
		self.print_tree(cur.right, output_format, indent=next_indent, last='up')
		
		if last == 'up':
			start_shape = '┌'
		elif last == 'down':
			start_shape = '└'
		elif last == 'updown':
			start_shape = ' '
		else:
			start_shape = '├'
		
		if cur.right is not None and cur.left is not None:
			end_shape = '┤'
		elif cur.right is None and cur.left is not None:
			end_shape = '┐'
		elif cur.right is not None and cur.left is None:
			end_shape = '┘'
		else:
			end_shape = ''
		
		print('{0}{1}{2}{3}'.format(indent, start_shape, content, end_shape))
		next_indent = '{0}{1}{2}'.format(indent, ' ' if 'down' in last else '│', " " * len(content))
		self.print_tree(cur.left, output_format, indent=next_indent, last='down')


class RBTree(BinTree):
	def __init__(self):
		super().__init__()
		self.nil = RBNode(key=None)
		self.root = self.nil

	@staticmethod
	def value_func(node: RBNode):
		"""used in super function 'print_tree' as 'output_format' parameter"""
		return str(node.key) + '(BLACK)' if node.color else str(node.key) + '( RED )'
	
	@staticmethod
	def _change_parent(p, past, cur):
		if p.left == past:
			p.left = cur
			return
		if p.right == past:
			p.right = cur
			return
		raise Exception('this node is not children of input parent')
	
	# left rotate and right rotate do not change color of node
	def _rotate_left(self, x: RBNode):
		# input: x, y
		if x.right == self.nil:
			return
		y = x.right
		
		x.right = y.left
		if y.left != self.nil:
			y.left.pre = x
		y.pre = x.pre
		
		if x.pre == self.nil:
			self.root = y
		else:
			self._change_parent(x.pre, x, y)
		y.left = x
		x.pre = y
		return
	
	def _rotate_right(self, x: RBNode):
		# input: x, y
		if x.left == self.nil:
			return
		y = x.left
		
		x.left = y.right
		if y.right != self.nil:
			y.right.pre = x
		y.pre = x.pre
		
		if x.pre == self.nil:
			self.root = y
		else:
			self._change_parent(x.pre, x, y)
		y.right = x
		x.pre = y
		return
	
	def _insert_fix_up(self, z: RBNode):
		# recolor and rebalance
		while z.pre.color == Const.RED:
			# 'cause z.pre is red, so z.pre must has its pre which black color
			if z.pre == z.pre.pre.left:
				y = z.pre.pre.right
				# z.pre and z.uncle both red, direct dyeing
				if y.color == Const.RED:
					z.pre.color = Const.BLACK
					y.color = Const.BLACK
					z.pre.pre.color = Const.RED
					z = z.pre.pre
				# z.pre and z.uncle have diff color, z is right node of z.pre, left rotate
				elif z == z.pre.right:
					z = z.pre
					self._rotate_left(z)
				# z.pre and z.uncle have diff color, z is left node of z.pre, right rotate
				else:
					z.pre.color = Const.BLACK
					z.pre.pre.color = Const.RED
					self._rotate_right(z.pre.pre)
				# while case 1 be run, z go up 2 layers
				# while case 2 be run, z remain its layer
				# while case 3 be run, loop stop, 'cause z.pre.color be set black
			else:
				# same as above but exchange 'left' and 'right'
				y = z.pre.pre.left
				if y.color == Const.RED:
					z.pre.color = Const.BLACK
					y.color = Const.BLACK
					z.pre.pre.color = Const.RED
					z = z.pre.pre
				elif z == z.pre.left:
					z = z.pre
					self._rotate_right(z)
				else:
					z.pre.color = Const.BLACK
					z.pre.pre.color = Const.RED
					self._rotate_left(z.pre.pre)
		self.root.color = Const.BLACK
	
	def insert(self, new_n: RBNode):
		"""
		in fact insert red node in rb-tree.
		while insert red do not break rule of rb-tree, just do it.
		else fix up.
		"""
		# find the place of new node should be insert
		x = self.root
		y = self.nil
		while x != self.nil:
			y = x
			if new_n.key < x.key:
				x = x.left
			else:
				x = x.right
		# insert
		new_n.pre = y
		if y == self.nil:
			self.root = new_n
		elif new_n.key < y.key:
			y.left = new_n
		else:
			y.right = new_n
		
		# set left node as nil
		new_n.left = self.nil
		new_n.right = self.nil
		new_n.color = Const.RED
		self._insert_fix_up(new_n)
		
		return
	
	def tree_minimum(self, x: RBNode):
		while x.left != self.nil:
			x = x.left
		return x
	
	def tree_successor(self, x: RBNode):
		if x.right != self.nil:
			return self.tree_minimum(x.right)
		y = x.pre
		while y != self.nil and x == y.right:
			x = y
			y = y.pre
		return y
	
	def _delete_fix_up(self, x: RBNode):
		"""
		fix up rb-tree while color of x is black.
		'cause y is black, x inherit its black, so x have a extra black
		the meaning of this func is solve the problem of extra black.
		
		push extra black node up to x.pre, meanwhile keep x and x.brother
		have same num of black.
		lend a black node from path root to x.brother or x.brother.children,
		transfer extra black node to x.pre, if x.pre still black, remain loop.
		"""
		while x != self.root and x.color == Const.BLACK:
			if x == x.pre.left:
				w = x.pre.right
				# x.brother is red, left rotate
				# the meaning of this step is assure x.brother is black and
				# make x.pre is red so loop can end in this time
				if w.color == Const.RED:
					w.color = Const.BLACK
					x.pre.color = Const.RED
					self._rotate_left(x.pre)
					w = x.pre.right
				# now x.brother must be black, x.brother has 2 black children,
				# set x.brother with red, put extra black mean to x.pre, so
				# num of black node between path root to x with path root
				# is equal
				if w.left.color == Const.BLACK and w.right.color == Const.BLACK:
					w.color = Const.RED
					x = x.pre
				# x.brother's right is black, left is red, right rotate
				# the meaning of this step is push red node up to x.brother,
				# so scene jump to case 2
				elif w.right.color == Const.BLACK:
					w.left.color = Const.BLACK
					w.color = Const.RED
					self._rotate_right(w)
					w = x.pre.right
				# x.brother's right is red, left is black, left rotate x.pre
				# now, path root to y have a new black node, so extra black fix up
				# finished
				else:
					w.color = x.pre.color
					x.pre.color = Const.BLACK
					w.right.color = Const.BLACK
					self._rotate_left(x.pre)
					x = self.root
			else:
				w = x.pre.left
				if w.color == Const.RED:
					w.color = Const.BLACK
					x.pre.color = Const.RED
					self._rotate_right(x.pre)
					w = x.pre.left
				if w.left.color == Const.BLACK and w.right.color == Const.BLACK:
					w.color = Const.RED
					x = x.pre
				elif w.left.color == Const.BLACK:
					w.right.color = Const.BLACK
					w.color = Const.RED
					self._rotate_left(w)
					w = x.pre.left
				else:
					w.color = x.pre.color
					x.pre.color = Const.BLACK
					w.left.color = Const.BLACK
					self._rotate_right(x.pre)
					x = self.root
			# self.print_tree(self.root, self.value_func)
		x.color = Const.BLACK
		return
	
	def delete(self, z: RBNode):
		"""
		find z.successor or z.left as y, replace content in z with y's,
		except color to prevent break rule in node z. so in fact, we delete
		y rather than z, then x(one of children of y) go up replace y,
		structure of rb-tree should be fixed up while color of x break rule.
		"""
		# y = z or y = z.successor
		if z.left == self.nil or z.right == self.nil:
			y = z
		else:
			y = self.tree_successor(z)
		# pick one of children of y, replace y with it
		if y.left != self.nil:
			x = y.left
		else:
			x = y.right
		x.pre = y.pre
		# if y.pre == nil, y == z == root
		if y.pre == self.nil:
			self.root = x
		elif y == y.pre.left:
			# go up x to y
			y.pre.left = x
		else:
			# same as above
			y.pre.right = x

		# if y == z, direct go up y.left, this step have done in above
		if y != z:
			# replace z with y
			z.key = y.key
			# copy y's satellite data into z
		# if y.color == red, op of delete red do not break rule of rb-tree
		if y.color == Const.BLACK:
			self._delete_fix_up(x)
		return y
	
	def search(self, key: [int, float, str]):
		x = self.root
		while x != self.nil and x.key != key:
			if x.key < key:
				x = x.right
			else:
				x = x.left
		return x


if __name__ == '__main__':
	import random
	
	def main():
		random.seed(2)
		
		insert_list = [].copy()
		rbt = RBTree()
		# test insert
		for i in range(20):
			key = random.randint(0, 100)
			rbt.insert(RBNode(key=key))
			insert_list.append(key)
		rbt.print_tree(rbt.root, RBTree.value_func)
		print(insert_list)
		
		# test search
		key = insert_list[random.randint(0, len(insert_list))]
		aim = rbt.search(key=key)
		print(aim.key)
		
		# test delete
		rbt.delete(aim)
		rbt.print_tree(rbt.root, RBTree.value_func)
		
	main()
