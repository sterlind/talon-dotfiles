(twice|second): core.repeat_command(1)
(thrice|third): core.repeat_command(2)
# -1 because we are repeating, so the initial command counts as one
<number_small> times: core.repeat_command(number_small-1)