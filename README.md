# redakt-grascco

For developing NER models based on [GraSCCo_PHI](https://zenodo.org/records/11502329) corpus.

GraSCCo - short for Graz Synthetic Clinical text Corpus - is a collection of artificially generated semi-structured and unstructured German-language clinical summaries designed to support research in clinical Natural Language Processing (cNLP).

https://ebooks.iospress.nl/doi/10.3233/SHTI220805 <br>
https://zenodo.org/records/6539131

These documents underwent rigorous alienation steps - textual paraphrasing, anonymization, and restructuring - to remove any privacy-sensitive information derived from real clinical texts. This transformation allows GraSCCo to be fully shareable with no legal restrictions.

To evaluate its utility, GraSCCo was compared to other real, non-shareable clinical corpora. The study found that GraSCCo captures sufficient linguistic characteristics to approximate real clinical language use - making it an effective resource for training clinical language models, though not necessarily domain-specific models.

Later, the corpus was annotated with PHI (Protected Health Information) entities. The annotations were exported XMI and JSON formats created with the INCEpTION annotation platform.

https://ebooks.iospress.nl/doi/10.3233/SHTI240853 <br>
https://zenodo.org/records/11502329

The following metrics are based on processing of [JSON exports](data/raw/11502329/grascco_phi_annotation_json) of the annotations .


| Metric                   | Value      |
| ------------------------ | ---------- |
| Total Files              | **63**     |
| Total Sentences          | **2,872**  |
| Total Tokens             | **41,992** |
| Total Labels             | **19**     |
| Total Annotated Entities | **1,439**  |

While the [annotation guideline](data/raw/11502329/_Annoguide____GeMTeX___DeID.pdf) lists in total 23 labels but only 19 can be found in these annotations.

Such missing labels are:

1. **CONTACT_URL**
2. **LOCATION_STATE**
3. **LOC_OTHER**
4. **NAME_OTHER**

 N | Label                  | Count |
---| -----------------------| ----- |
01 | DATE                   | 694   |
02 | NAME\_PATIENT          | 166   |
03 | NAME\_DOCTOR           | 154   |
04 | NAME\_TITLE            | 139   |
05 | LOCATION\_CITY         | 59    |
06 | ID                     | 58    |
07 | LOCATION\_ZIP          | 38    |
08 | LOCATION\_HOSPITAL     | 36    |
09 | LOCATION\_STREET       | 36    |
10 | AGE                    | 24    |
11 | CONTACT\_PHONE         | 18    |
12 | CONTACT\_FAX           | 7     |
13 | LOCATION\_COUNTRY      | 2     |
14 | LOCATION\_ORGANIZATION | 2     |
15 | PROFESSION             | 2     |
16 | CONTACT\_EMAIL         | 1     |
17 | NAME\_EXT              | 1     |
18 | NAME\_RELATIVE         | 1     |
19 | NAME\_USERNAME         | 1     |


Due to insufficient number of entities for labels, such as - 

1. **CONTACT_EMAIL (1)**
2. **NAME_EXT (1)**
3. **NAME_RELATIVE (1)**
4. **NAME_USERNAME (1)**

\- documents containing these entities were made part of train set. Due to this curation, the test set contains only the rest 15 labels.

A separate pandas dataframe is prepared with rows for all the documents and with additionally prepared BIOES tagged tokenized text per document.

Columns:<br>

1. **ID**
2. **document_title**
3. **document_text**
4. **sentences**
5. **tokens**
6. **entities**
7. **sentence_count**
8. **token_count**
9. **entity_count**
10. **label_wise_entity_count**
11. **bioes_text**


Three separate transformers based language models are fine-tuned for the NER downstream task on these annotations of GraSCCo corpus:

1. google-bert/bert-base-german-cased
2. FacebookAI/xlm-roberta-large
3. deepset/gelectra-large