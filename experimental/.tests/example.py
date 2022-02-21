x = 0
if :
#  ^- statement,primitive_value,logic_prefix_operator
    pass
if not :
#      ^- statement,primitive_value,logic_prefix_operator
    pass

if x and :
#        ^- statement,primitive_value,logic_prefix_operator
    pass

if x and not :
#            ^- statement,primitive_value,logic_prefix_operator
    pass

if 0:
# <- statement,logic_infix_operator
#  ^- statement,logic_infix_operator
#   ^- statement,logic_infix_operator
    x = 0
# ^- statement 
    # <- statement
    if True:
    # <- logic_infix_operator,statement
    #   ^- logic_infix_operator,statement
        pass
        # ^- statement