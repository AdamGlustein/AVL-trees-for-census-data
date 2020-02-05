from lab0_utilities import *

class Languages:
	def __init__(self):
		self.data_by_year = {}

	def build_trees_from_file(self, file_object):
		lines = file_object.readlines()
		if len(lines) == 0: # checking null case
			return self.data_by_year
		# Constructing dictionary from lines
		for x in range(1,len(lines)): # skip title line
			data = lines[x].split(",") # cuts into three parts: year, language, count
			year = int(data[0])
			language = data[1]
			count = int(data[2])
			stat = LanguageStat(language, year, count)
			root = Node(stat)
			if year in self.data_by_year: # key exists			
				self.data_by_year[year].balanced_insert(root)
			else: # new year, new tree
				self.data_by_year[year] = BalancingTree(root)
		return self.data_by_year
	

	def query_by_name(self, language_name):
		d = {}
		for key in self.data_by_year: # key is the year
			if self.data_by_year[key].search_by_language(language_name): # if in year
				d[key] = self.data_by_year[key].search_by_language(language_name).count # extracts count by finding language 
		return d
		
	def query_by_count(self, threshold = 0):
		d = {}
		for key in self.data_by_year:
			M = []
			L = self.data_by_year[key].preorder()
			for stat in L:
				if stat.val.count > threshold:
					M.append(stat.val.name)
			d[key] = M
		return d

class BalancingTree:
	def __init__(self, root_node):
		self.root = root_node
		
	def search_by_language(self, language_name): # HELPER: searches for a statistic by language in a year's tree, returns LanguageStat object (or False)
		if self.root == None:  
			return False
		if self.root.val.name == language_name:        
			return self.root.val
		# if base cases not met, continue searching 
		if language_name < self.root.val.name:
			return BalancingTree(self.root.left).search_by_language(language_name)
		else:
			return BalancingTree(self.root.right).search_by_language(language_name)	
		
	def preorder(self): # HELPER: returns preorder traversal of the tree's nodes (list)
		if self.root:
			return [self.root] + BalancingTree(self.root.left).preorder() + BalancingTree(self.root.right).preorder()
		else:
			return []
		
				
	def balanced_insert(self, node, curr = None):
		curr = curr if curr else self.root  # curr = curr if non-empty, equals root else
		self.insert(node, curr) 
		self.balance_tree(node)

	def insert(self, node, curr = None):
		if node == None: # null case
			return None
		curr = curr if curr else self.root
		# insert at correct location in BST
		if node._val < curr._val:
			if curr.left is not None:
				self.insert(node, curr.left)
			else:
				node.parent = curr
				curr.left = node
				self.update_all_bf_above(node)
		else:
			if curr.right is not None:
				self.insert(node, curr.right)
			else:
				node.parent = curr
				curr.right = node
				self.update_all_bf_above(node)
		return


	def balance_tree(self, node):
		if self.is_balanced():
			return 
		
		if self.find_balance_factor(node) < -1: # left heavy
			if self.find_balance_factor(node.left) < 0: # LL
				self.right_rotate(node)
			else: # LR
				self.left_rotate(node.left)
				self.right_rotate(node)
			
		elif self.find_balance_factor(node) > 1: # right heavy 
			if self.find_balance_factor(node.right) > 0: # RR
				self.left_rotate(node)
			else: # RL
				self.right_rotate(node.right)
				self.left_rotate(node)

		
		return self.balance_tree(node.parent)		
				

	def update_height(self, node):
		node.height = 1 + max(self.height(node.left), self.height(node.right))
		
	def update_bf(self, node):
		node.bf = self.height(node.right) - self.height(node.left)
		
	def update_all_bf_above(self, node):
		if node:
			self.update_bf(node)
			self.update_all_bf_above(node.parent)

	def height(self, node):
		if node is not None:
			return 1 + max(self.height(node.left), self.height(node.right))
		else:
			return 0
		
	def left_rotate(self, z):
		y = z.right
		y.parent = z.parent
		if y.parent is None:
			self.root = y
		else:
			if y.parent.left is z:
				y.parent.left = y
			elif y.parent.right is z:
				y.parent.right = y
		z.right = y.left
		if z.right is not None:
			z.right.parent = z
		y.left = z
		z.parent = y
		self.update_height(z)
		self.update_height(y)
		self.update_all_bf_above(z)


	def right_rotate(self, z):
		y = z.left
		y.parent = z.parent
		if y.parent is None:
			self.root = y
		else:
			if y.parent.left is z:
				y.parent.left = y
			elif y.parent.right is z:
				y.parent.right = y		
		z.left = y.right
		if z.left is not None:
			z.left.parent = z
		y.right = z
		z.parent = y
		self.update_height(z)
		self.update_height(y)	
		self.update_all_bf_above(z)		
		
		
	def find_balance_factor(self, node):
		if node:
			return node.bf		 
		return None


	def is_balanced(self):
		# preorder traversal to check that all nodes are balanced
		L = self.preorder()
		for node in L:
			bf = self.find_balance_factor(node)
			if abs(bf) > 1:
				return False
		return True
	

if __name__ == "__main__":
	f = open('ca_languages.csv')
	ca = Languages()
	ca.build_trees_from_file(f)
	print(ca.query_by_name("English"))
	print(ca.query_by_count(500000))
	print(ca.data_by_year[1951].is_balanced())
