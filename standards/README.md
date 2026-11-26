# Standards library

Put the source documents here as **text-searchable PDFs**. Claude will only
quote requirements from these files.

| Document | Where to get it | Notes |
|---|---|---|
| NCC Volume One, the edition(s) your projects use | ABCB website (free, registration required) | Name the file with its edition, e.g. `NCC-2022-Vol1.pdf` |
| Disability (Access to Premises – Buildings) Standards 2010, incl. Access Code | Federal Register of Legislation (free) | Use the current compilation |
| AS 1428.1 (and 1428.4.1 etc. if held) | Standards Australia / your subscription | **Licensed.** Check that your subscription allows storing it here. |
| AS 2890.6 (accessible parking) | Your subscription | Licensed, as above |
| EFSG (SINSW projects) | SINSW | Check the access conditions |

After adding or replacing files, run:

```bash
python3 tools/standards.py index
```

Scanned (image-only) PDFs can't be searched. The index command will warn you
if a file has no text.

Licensed Standards: this repository must stay **private**. If ADCO's
subscription doesn't allow copies in a repository, keep them out and the
review will mark those requirements `NOT IN LIBRARY`.
