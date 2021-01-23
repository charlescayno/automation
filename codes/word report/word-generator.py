from __future__ import print_function
from mailmerge import MailMerge
from datetime import date

template = "template.docx"

document = MailMerge(template)
print(document.get_merge_fields())

document.merge(
        vds = 'vds waveforms',
        ids = 'ids waveforms'
)

document.write('template1.docx')