from tree import Tree

try:
    tree = Tree('IN10270')
    print(tree.run())
except Exception as e:
    print(f'ERROR {e}')