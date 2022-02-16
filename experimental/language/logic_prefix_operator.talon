tag: user.logic_prefix_operator
-

not [<phrase>]:
    user.code_replace_target("logic_prefix_operator", "not $$")
    user.rephrase(phrase or "")