#!/usr/bin/env python3
"""Generate the Writer's Notebook handout in the OP1/MRP house style.

Clones OP1 Why You Write.docx so styles.xml, numbering.xml, the theme and the
embedded Inter fonts all carry over untouched; only word/document.xml is
rebuilt. That is why this matches the other handouts rather than approximating
them.
"""
import zipfile, re, sys
from pathlib import Path
from xml.sax.saxutils import escape

SITE = Path("/home/todd/Repos/tce284-fa26")
TPL = SITE / "week-01-trust-the-gush/OP1 Why You Write.docx"
OUT = SITE / "writers-notebook/Writers Notebook Guidelines.docx"

RPR = '<w:rPr><w:rtl w:val="0"/></w:rPr>'
RPR_B = '<w:rPr><w:b w:val="1"/><w:bCs w:val="1"/><w:rtl w:val="0"/></w:rPr>'
RPR_I = '<w:rPr><w:i w:val="1"/><w:iCs w:val="1"/><w:rtl w:val="0"/></w:rPr>'

_pid = [0x100]
def pid():
    _pid[0] += 1
    return f"{_pid[0]:08X}"


def runs(text: str) -> str:
    """**bold** and *italic* inline markers -> Word runs."""
    out = []
    for part in re.split(r'(\*\*[^*]+\*\*|\*[^*]+\*)', text):
        if not part:
            continue
        if part.startswith("**"):
            rpr, body = RPR_B, part[2:-2]
        elif part.startswith("*"):
            rpr, body = RPR_I, part[1:-1]
        else:
            rpr, body = RPR, part
        out.append(f'<w:r>{rpr}<w:t xml:space="preserve">{escape(body)}</w:t></w:r>')
    return "".join(out)


def title(text):
    b = '<w:b w:val="1"/><w:bCs w:val="1"/><w:sz w:val="24"/><w:szCs w:val="24"/>'
    return (f'<w:p w14:paraId="{pid()}"><w:pPr><w:spacing w:after="0" w:lineRule="auto"/>'
            f'<w:rPr>{b}</w:rPr></w:pPr><w:r><w:rPr>{b}<w:rtl w:val="0"/></w:rPr>'
            f'<w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>')


def head(text):
    return (f'<w:p w14:paraId="{pid()}"><w:pPr><w:pStyle w:val="Heading2"/><w:rPr/></w:pPr>'
            f'<w:r>{RPR}<w:t xml:space="preserve">{escape(text)}</w:t></w:r></w:p>')


def para(text):
    return f'<w:p w14:paraId="{pid()}"><w:pPr><w:rPr/></w:pPr>{runs(text)}</w:p>'


def bullet(text):
    return (f'<w:p w14:paraId="{pid()}"><w:pPr><w:numPr><w:ilvl w:val="0"/>'
            f'<w:numId w:val="1"/></w:numPr><w:spacing w:after="0" w:afterAutospacing="0"/>'
            f'<w:ind w:left="720" w:hanging="360"/><w:rPr><w:u w:val="none"/></w:rPr></w:pPr>'
            f'{runs(text)}</w:p>')


BORDERS = ('<w:tcBorders><w:top w:color="000000" w:space="0" w:sz="4" w:val="single"/>'
           '<w:left w:color="000000" w:space="0" w:sz="4" w:val="single"/>'
           '<w:bottom w:color="000000" w:space="0" w:sz="4" w:val="single"/>'
           '<w:right w:color="000000" w:space="0" w:sz="4" w:val="single"/></w:tcBorders>'
           '<w:tcMar><w:top w:w="40.0" w:type="dxa"/><w:left w:w="108.0" w:type="dxa"/>'
           '<w:bottom w:w="40.0" w:type="dxa"/><w:right w:w="108.0" w:type="dxa"/></w:tcMar>')
COLS = [1500, 620, 2900, 2900, 2805]      # = 10725, the house table width


def table(rows, cols=None):
    cols = cols or COLS
    grid = "".join(f'<w:gridCol w:w="{w}"/>' for w in cols)
    trs = []
    for cells in rows:
        tcs = []
        for w, txt in zip(cols, cells):
            tcs.append(f'<w:tc><w:tcPr>{BORDERS}</w:tcPr>'
                       f'<w:p w14:paraId="{pid()}"><w:pPr><w:spacing w:after="0"/>'
                       f'<w:rPr/></w:pPr>{runs(txt)}</w:p></w:tc>')
        trs.append('<w:tr><w:trPr><w:cantSplit w:val="0"/>'
                   f'<w:tblHeader w:val="0"/></w:trPr>{"".join(tcs)}</w:tr>')
    return ('<w:tbl><w:tblPr><w:tblStyle w:val="Table1"/>'
            '<w:tblW w:w="10725.0" w:type="dxa"/><w:jc w:val="left"/>'
            '<w:tblInd w:w="-3.0" w:type="dxa"/><w:tblBorders>'
            '<w:top w:color="000000" w:space="0" w:sz="4" w:val="single"/>'
            '<w:left w:color="000000" w:space="0" w:sz="4" w:val="single"/>'
            '<w:bottom w:color="000000" w:space="0" w:sz="4" w:val="single"/>'
            '<w:right w:color="000000" w:space="0" w:sz="4" w:val="single"/>'
            '<w:insideH w:color="000000" w:space="0" w:sz="4" w:val="single"/>'
            '<w:insideV w:color="000000" w:space="0" w:sz="4" w:val="single"/>'
            '</w:tblBorders><w:tblLayout w:type="fixed"/><w:tblLook w:val="0000"/></w:tblPr>'
            f'<w:tblGrid>{grid}</w:tblGrid>{"".join(trs)}</w:tbl>')


B = []
B += [title("Your Writer's Notebook"), title("TCE 284 FA26 (Edwards)"), title("50 points possible")]

B += [head("1. What's This All About?")]
B += [para("Writers keep notebooks. Not because someone collects them, but because writing that "
           "matters almost never arrives finished. It arrives as a fragment, an overheard line, a "
           "question you cannot let go of. The notebook is where those land so they are not lost.")]
B += [para("This is a quarter of your grade, and it is the only part of this course graded on "
           "**practice rather than polish**. Nothing in here gets red-penned. Spelling does not "
           "count. Sentences that fall apart do not count against you. What counts is that you "
           "wrote, often, and that you were actually thinking while you did it.")]
B += [para("You will write in it in nearly every class and on your own. Expect **25 to 40 "
           "entries** by December.")]

B += [head("2. What Goes In It")]
for t in ["Every **free-write**, including the Week 1 *why do we write?* baseline and the daily openers",
          "In-class **quick-writes and exercises**",
          "Your currere **gushes, brainstorms, and storyboard notes**",
          "Your research **topic map and source notes**",
          "The Week 15 **Look-Back Letter** to the writer who answered *why do we write?* on the first day",
          "Anything else you want to keep: lines you overheard, images, questions, false starts"]:
    B += [bullet(t)]
B += [para("**Your timed One-Pager gushes do not go here.** Each one is submitted on sheet two of "
           "the One-Pager PDF it produced. It is the same writing either way, and it belongs with "
           "the piece it became. Nothing gets counted twice.")]

B += [head("3. Where You Keep It")]
B += [para("**Journaler** is the recommended home and makes turning it in one click. A physical "
           "notebook is completely fine — photograph or scan it. The one exception is the five "
           "**timed One-Pager drafts**, which happen in Journaler because the edit-lock is what "
           "keeps a timed draft honest.")]

B += [head("4. How It Has to Be Organized")]
B += [para("Every notebook is turned in the same way, whether you kept it in Journaler or on "
           "paper. Journaler produces this for you when you choose **Bundle → PDF**. On paper, "
           "you produce it yourself. Three things:")]
for t in ["**Date every entry.** A notebook is a record of a practice over time, and an undated entry cannot show that.",
          "**Number every entry**, 1 to however many you have, in date order. Not page numbers — *entry* numbers, so we can both say “entry 17” and mean the same thing.",
          "**Put a Contents list at the front**: number, date, word count, and the opening words of each entry."]:
    B += [bullet(t)]
B += [para("If you keep a paper notebook, number your entries as you go rather than at the end. "
           "Numbering forty entries in December is an evening you will not enjoy.")]
B += [para("**You do not turn in the whole notebook.** You turn in a **report** — about eight to "
           "ten pages — and the Contents list stands in for everything else. That is deliberate. "
           "Deciding what is worth another reader's time is the same judgment this course asks of "
           "you on every One-Pager. Your report contains:")]
B += [table([
    ["**Cover**", "The counts, and where each required thing is"],
    ["**Part 1**", "Contents — every entry, numbered, dated, with its word count"],
    ["**Part 2**", "Your four required entries, in full"],
    ["**Part 3**", "Your Look-Back Letter"],
    ["**Part 4**", "The three entries you flagged, in full"],
    ["**Part 5**", "Your threads, and your reading of one"],
], cols=[1755, 8970])]

B += [head("5. Flag Three Entries")]
B += [para("When you turn the notebook in, **mark three entries you want read closely** — one "
           "from each act of the course. Write their numbers on the cover. Those three, and only "
           "those three, are what I read for the *Thinking on the page* row below.")]
B += [para("Two reasons. Everything else stays genuinely unjudged, which is the promise this "
           "notebook runs on: you should be able to write badly in it, or write about something "
           "difficult, without wondering how it will be scored. And choosing which three is "
           "itself an act of judgment. Pick the ones where something happened, not the ones that "
           "are tidiest.")]

B += [head("6. Threads, and Writing Your Reading of One")]
B += [para("**A thread is anything that keeps coming back.** Your grandmother. The blank page. A "
           "room you keep describing. A question you cannot leave alone. You name it, and you put "
           "that name on every entry it turns up in — three entries, ten, however many it takes.")]
B += [para("**Before you turn the notebook in, pick one thread and write your reading of it.** "
           "Two questions: *what runs through these?* and *what is in the last one that is not in "
           "the first?* That second one is the whole reason the dates matter. It is not a summary "
           "of what you wrote. It is what you now see that you could not see while writing any "
           "single entry.")]
B += [para("If you cannot see a thread yet, that is normal. In Journaler, the Threads view has a "
           "panel called **What keeps coming back**: words you have used in several entries, with "
           "a count. It is a word count, not a reading — it tells you what recurs, not what "
           "matters, and some of it will be noise. It cannot see paraphrase either, so "
           "*grandmother · grandma · her kitchen* read as three unrelated words. Click one, read "
           "those entries together, and decide for yourself. **The noticing is the assignment.**")]

B += [head("7. What “Thinking on the Page” Means")]
B += [para("You do not have to sound reflective. **Performed reflection is the thing this row is "
           "designed to catch**, and it is easy to spot: it travels in a straight line to a "
           "conclusion you already held before you started. Real thinking does something else.")]
for t in ["**It turns.** You arrive somewhere you were not heading. *“I thought this was about — actually, no.”* That mid-entry change of direction is the clearest signature there is.",
          "**It connects.** An image, a question, or a line comes back weeks later, changed. An entry argues with a reading. Something here shows up in a One-Pager, the currere, or the research project.",
          "**It goes specific.** Under every claim there is an instance. Depth is not intensity of feeling. It is being willing to name the actual thing, and to follow a thought past its first answer."]:
    B += [bullet(t)]

B += [head("Important Dates / Deadlines")]
for t in ["**Every class session.** Aim for about one entry per meeting. Write between sessions too.",
          "**Week 1.** The *why do we write?* baseline free-write. Keep it — you write back to it in Week 15.",
          "**Week 15, Wednesday, December 2, in class.** The Look-Back Letter, written during our last session, so your notebook is complete on the day you hand it in.",
          "**Notebook due Wednesday, December 2 at 11:59 p.m.**, with your three entries flagged. The standing 48-hour grace applies here as it does everywhere else."]:
    B += [bullet(t)]

B += [head("8. How Will My Work Be Assessed?")]
B += [para("Scores land on whole points. Required entries are graded on **presence only** — a "
           "required entry that is present but thin is never counted against you twice.")]
B += [table([
    ["**Part**", "**Pts**", "**Full marks**", "**Partial**", "**None**"],
    ["**Kept practice**", "20",
     "25 or more dated entries, spread across the whole term at roughly one per session. The notebook shows a habit: you wrote when it was going well and when it was not.",
     "15–24 entries, or the term is uneven — long silences, or a stretch written all at once. Twenty-eight entries dated in November is not a practice.",
     "Fewer than 15 entries, or nothing dated, so no practice can be seen."],
    ["**Required entries**", "5",
     "All four present: the Week 1 baseline, currere gushes and brainstorms, the topic map, and source notes.",
     "One missing.", "Two or more missing."],
    ["**Look-Back Letter**", "10",
     "Written in our last class, to the writer who answered *why do we write?* on day one.",
     "Present but perfunctory.", "Missing."],
    ["**Thinking on the page**", "15",
     "From your three flagged entries **and your reading of a thread**: the thinking moves. Entries turn — you arrive somewhere you were not heading. Your reading names something real that changed between the first entry and the last, and points at the evidence.",
     "Real thinking is visible. You go past the first answer more than once, and the thread reading sees something, even if it stays general. **Or:** honest and present, but mostly arriving where you started.",
     "The entries report rather than think, or perform a reflection they have not done. No thread reading, or one that only lists what the entries were about."],
])]

SECTPR = ('<w:sectPr><w:pgSz w:h="15840" w:w="12240" w:orient="portrait"/>'
          '<w:pgMar w:bottom="720" w:top="720" w:left="720" w:right="720" '
          'w:header="720" w:footer="720"/><w:pgNumType w:start="1"/></w:sectPr>')

zin = zipfile.ZipFile(TPL)
tpl_doc = zin.read("word/document.xml").decode("utf-8")
head_xml = tpl_doc[:tpl_doc.index("<w:body>") + len("<w:body>")]
new_doc = head_xml + "".join(B) + SECTPR + "</w:body></w:document>"

OUT.parent.mkdir(parents=True, exist_ok=True)
zout = zipfile.ZipFile(OUT, "w", zipfile.ZIP_DEFLATED)
for item in zin.infolist():
    data = new_doc.encode("utf-8") if item.filename == "word/document.xml" else zin.read(item.filename)
    zout.writestr(item, data)
zout.close(); zin.close()
print(f"wrote {OUT}  ({OUT.stat().st_size:,} bytes)")
