tag: user.statement
-

^if [<phrase>]$: user.code_upsert("statement", "if $0:", "$$\n\tif $0:", phrase or "")
^while [<phrase>]$: user.code_upsert("statement", "while $0:", "$$\n\twhile $0:", phrase or "")
