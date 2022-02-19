from talon import Module, speech_system, cron
from talon.grammar import Phrase

mod = Module()

sample_stacks = []
phrase_stack = []

def on_pre_phrase(d):
    sample_stacks.append([])
    phrase_stack.append(d)

def on_post_phrase(_):
    phrase_stack.pop()
    for sample in sample_stacks.pop():
        speech_system._on_audio_frame(sample)

speech_system.register("post:phrase", on_post_phrase)
speech_system.register("pre:phrase", on_pre_phrase)

@mod.action_class
class Actions:
    def rephrase(phrase: Phrase):
        """Reevaluate phrase"""
        if not phrase:
            return

        current_phrase = phrase_stack[-1]
        ts = current_phrase["_ts"]
        start = phrase.words[0].start - ts
        end   = phrase.words[-1].end - ts
        samples = current_phrase["samples"]
        pstart  = int(start * 16_000)
        pend    = int(end   * 16_000)

        sample_stacks[-1].append(samples[pstart:pend])
        