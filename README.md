# redakt-grascco

For developing NER models based on [GraSCCo_PHI](https://zenodo.org/records/11502329) corpus.

GraSCCo - short for Graz Synthetic Clinical text Corpus - is a collection of artificially generated semi-structured and unstructured German-language clinical summaries designed to support research in clinical Natural Language Processing (cNLP).

https://ebooks.iospress.nl/doi/10.3233/SHTI220805
https://zenodo.org/records/6539131

These documents underwent rigorous alienation steps - textual paraphrasing, anonymization, and restructuring - to remove any privacy-sensitive information derived from real clinical texts. This transformation allows GraSCCo to be fully shareable with no legal restrictions.

To evaluate its utility, GraSCCo was compared to other real, non-shareable clinical corpora. The study found that GraSCCo captures sufficient linguistic characteristics to approximate real clinical language use - making it an effective resource for training clinical language models, though not necessarily domain-specific models.

Later, the corpus was annotated PHI (Protected Health Information) entities. The annotations were exported XMI and JSON formats created with the INCEpTION annotation platform.

https://ebooks.iospress.nl/doi/10.3233/SHTI240853
https://zenodo.org/records/11502329


The following metrics are based on processing of JSON exports of the annotations ([see data/raw/11502329/grascco_phi_annotation_json folder](data/raw/11502329/grascco_phi_annotation_json)).


| Metric                   | Value      |
| ------------------------ | ---------- |
| Total files              | **63**     |
| Total sentences          | **2,872**  |
| Total tokens             | **41,992** |
| Total labels             | **19**     |
| Total annotated entities | **1,439**  |
