import re

tts_loc = '../../../tortoise-tts/tortoise'

def convert_to_dicts(block):
    # Regular expression pattern
    pattern = r'<(.*?)>(.*?)</\1>'
    
    # Find all matches in the block
    matches = re.findall(pattern, block, re.DOTALL)

    result = []
    current_speaker = None
    current_line = ""

    for speaker, line in matches:
        line = line.strip().replace('\n', ' ').replace('"', '')
        
        if speaker == current_speaker and len(current_line) + len(line) <= 200:
            current_line += " " + line
        else:
            if current_speaker is not None:
                result.append({'speaker': current_speaker, 'line': current_line.strip()})
            current_speaker = speaker
            current_line = line

    # Add the last speaker's lines to the result
    if current_speaker is not None:
        result.append({'speaker': current_speaker, 'line': current_line.strip()})

    return result

text = """
<garnt> - I like that, I like the aesthetic. </garnt>
<connor> - Yeah, I like that too.
- Yeah, yeah. </connor>
<connor> - I think it's just cool. </connor>
<connor> - I think the problem is </connor>
<connor> that it's a lot of times,
it's just kind of like, </connor>
<connor> oh, cool, you're wearing a scarf with your shirt, </connor>
<connor> and it's like, oh, cool, </connor>
<connor> I'm gonna wear a scarf
with my shirt now as well. </connor>
<connor> - Yeah, yeah, exactly. </connor>
<connor> - It's just, it's like, </connor>
<connor> it's just like, yeah, yeah,
I'm gonna do that as well. </connor>
<connor> - And then you end up having </connor>
<connor> like three scarves on your neck, </connor>
<connor> and you look like a complete idiot, </connor>
<joey> 'cause no one would ever wear three scarves. </joey>
<connor> - I don't know, if I was
a rich person, I'd probably wear, </connor>
<connor> I'd probably wear like three scarves. </connor>
<connor> - I'd probably just wear one
scarf that was like, </connor>
<joey> really long and like,
you know, just like, </joey>
<joey> just like have that one scarf
that was like, oh, </joey>
<joey> it's like just like, you know, </joey>
<joey> you're just like, oh,
I'm just gonna wear this. </joey>
<connor> I'm just gonna wear it
until it gets old, </connor>
<connor> and then I'll probably
just have a scarf burning ceremony. </connor>
<connor> - I don't, I just don't know. </connor>
<connor> - I don't know. </connor>
<connor> I don't know.
- I don't know. </connor>
<joey> I think that's the only
reason why I don't wear one, </joey>
<connor> I think it's just like, </connor>
<connor> I don't know how to wear it right. </connor>
<connor> - I know how to wear it
right, I know I know how to wear it, </connor>
<connor> but I know that if I wear
a scarf, I'll end up with, </connor>
<connor> I'll end up looking like a fucking idiot, </connor>
<joey> so I don't want to risk it. </joey>
<joey> - So we didn't, so
we didn't have a scarf, </joey>
"""

result = convert_to_dicts(text)
result

out = '@echo off\n\n'

for i, l in enumerate(result):
    speaker = l['speaker']
    line = l['line']
    to_run = f'python {tts_loc}/do_tts.py --text "{line}" --voice "{speaker}" --output_path "results/llama/llama_{i}/" --preset "fast"'
    out += to_run + '\n'

f = open('create_audio.bat', 'w')
f.write(out)
f.close()
