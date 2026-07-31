from __future__ import print_function
from mailmerge import MailMerge
from datetime import date

template = "template.docx"

document = MailMerge(template)
print(document.get_merge_fields())

document.merge(
        vds = 'vds label',
        ids = 'ids label'
)

document.write('template1.docx')