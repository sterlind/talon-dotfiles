from talon import Context, actions
import re

ctx = Context()

@ctx.action_class("user")
class UserActions:
    def insert_formatted_snippet(snippet: str):
        lines = snippet.split("\n")
        lowest = None
        result = []

        for k, line in enumerate(lines):
            segments = []
            tail = 0
            removed = 0
            for m in re.finditer(r"\$(\d+)", line):
                segments.append(line[tail : m.start(1) - 1])

                tail = m.end(1)
                marker_num = int(m.group(1))

                # Put the cursor at the lowest marker, besides $0 (if we have a choice)
                if not lowest or ((lowest[0] > marker_num or lowest[0] == 0) and marker_num > 0):
                    lowest = (int(m.group(1)), k, m.start(1) - 1 - removed)

                # Keep track of the marker characters we got rid of.
                removed += len(m.group(1))

            segments.append(line[tail:])
            result.append("".join(segments))

        if not lowest:
            lowest = (None, len(lines) - 1, len(result[-1]))

        result_text = "\n".join(result)
        actions.insert(result_text)

        # Navigate back to the best marker.
        times_up = len(result) - 1 - lowest[1]
        times_left = len(result[lowest[1]]) - lowest[2]
        for _ in range(times_up):
            actions.edit.up()
        actions.edit.line_end()
        for _ in range(times_left):
            actions.edit.left()