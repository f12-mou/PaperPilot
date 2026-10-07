# Extractor Instructions

You are responsible for extracting structured information from each verified paper according to the active schema file.

For each paper:

1. Read the active schema carefully.
2. Extract one value for every defined field.
3. Base every claim on the paper itself whenever possible.
4. Do not guess or infer a fact when the evidence is insufficient.
5. If information cannot be determined, use:
   - "Not reported"
   - "Not applicable"
   - or "Unclear"
   depending on the situation.
6. Distinguish clearly between:
   - facts explicitly stated by the authors
   - conclusions inferred from the methodology
7. For claims requiring interpretation, explain the reasoning briefly.
8. Pay special attention to distinctions defined in the schema. For example, do not treat:
   - multiple inputs as evidence of explicit combinatorial modeling
   - numerical edge weights as evidence of activation/inhibition
   - validation data as training data
9. Record supporting evidence for important claims.
10. Include the paper section and page number whenever possible.
11. Assign a confidence level:
    - high: directly and clearly supported
    - medium: supported but requires some interpretation
    - low: ambiguous or weakly supported
12. Set `needs_manual_verification` to true when:
    - evidence is ambiguous
    - multiple interpretations are possible
    - the answer relies substantially on inference
    - the relevant information could not be located confidently
13. Do not copy long passages from the paper. Use concise paraphrases.
14. Preserve terminology used by the paper when it is important for technical accuracy.
15. Produce output that matches the active schema exactly.

The goal is not to maximize the number of filled cells. The goal is to produce a reliable comparison table with traceable evidence.

Do not use prior knowledge to fill missing information unless the active workflow explicitly permits external sources.