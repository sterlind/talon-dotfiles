x = 0
if :
#  ^- primitive_value,logic_prefix_operator
    pass
if not :
#      ^- primitive_value,logic_prefix_operator
    pass

if x and :
#        ^- primitive_value,logic_prefix_operator
    pass

if x and not :
#            ^- primitive_value,logic_prefix_operator
    pass

if 0:
# <- logic_infix_operator
#  ^- logic_infix_operator
#   ^- logic_infix_operator
    x = 0
# ^- nothing 
    # <- nothing
    if True:
    # <- logic_infix_operator
    #   ^- logic_infix_operator
        pass
        # ^- nothing