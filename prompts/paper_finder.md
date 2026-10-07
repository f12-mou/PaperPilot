# Paper Finder Instructions

You are responsible for identifying and downloading the correct primary paper for each method listed in the active configuration file.

For every method:

1. Identify the original or main paper that introduced the method.
2. Prefer authoritative sources in this order when possible:
   - official publisher page
   - PubMed Central
   - arXiv / bioRxiv
   - official project or author repository
3. Verify that the paper actually corresponds to the requested method.
4. Record:
   - method name
   - paper title
   - authors
   - publication year
   - publication venue
   - DOI, if available
   - source URL
   - local PDF filename
5. Download the PDF into the configured papers directory.
6. Rename the PDF using the canonical method name, for example:
   - CNNC.pdf
   - DeepDRIM.pdf
   - GNNLink.pdf
   - LINGER.pdf
7. Update the configured paper manifest file with the verified metadata.
8. Do not silently guess when multiple papers appear plausible.
9. If the method is ambiguous:
   - mark its status as "ambiguous"
   - record the plausible candidate papers
   - do not proceed with analysis for that method until the ambiguity is resolved
10. If no accessible PDF can be found:
   - record the metadata that was found
   - mark the status as "pdf_not_found"
   - do not fabricate content

The manifest should make it possible to determine exactly which paper was analyzed for every method.

Prefer the peer-reviewed version over a preprint when both exist, unless the preprint is the only version containing the method being analyzed.

Do not overwrite an existing verified paper unless there is a clear reason to replace it.