# redakt-grascco

For developing NER models based on [GraSCCo_PHI](https://zenodo.org/records/11502329) corpus.

## About GraSCCo Corpus

GraSCCo - short for <u>Gra</u>z <u>S</u>ynthetic <u>C</u>linical text <u>Co</u>rpus - is a collection of artificially generated semi-structured and unstructured German-language clinical summaries designed to support research in clinical Natural Language Processing (cNLP).

Research Article: [GRASCCO — The First Publicly Shareable, Multiply-Alienated German Clinical Text Corpus](https://ebooks.iospress.nl/doi/10.3233/SHTI220805)<br>
Zenodo Data Repository: https://zenodo.org/records/6539131

Later, the corpus was annotated with PHI (Protected Health Information) entities. The annotations were exported XMI and JSON formats created with the INCEpTION annotation platform.

Research Article: [De-Identifying GRASCCO – A Pilot Study for the De-Identification of the German Medical Text Project (GeMTeX) Corpus](https://ebooks.iospress.nl/doi/10.3233/SHTI240853) <br>
Zenodo Data Repository: https://zenodo.org/records/11502329

## Data Preparation

For feature analysis and data preparation to fine-tune NER models, [JSON exports](data/raw/11502329/grascco_phi_annotation_json) of the corpus are utilized.

The following keys are used to extract relevant information from the JSON files:
1. **%FEATURE_STRUCTURES** - the root object key that contains arrays of sentences, tokens, whole text and PHI information, each object in these arrays contains a **%TYPE** key to identify the type of information
2. **de.tudarmstadt.ukp.dkpro.core.api.metadata.type.DocumentMetaData** - the value of **%TYPE** key - used to access document-level metadata, such as title
3. **de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Sentence** - the value of **%TYPE** key - used to access sentence-level boundaries
4. **de.tudarmstadt.ukp.dkpro.core.api.segmentation.type.Token** - the value of **%TYPE** key - used to access token-level boundaries
5. **uima.cas.Sofa** - the value of **%TYPE** key - used to access the whole text of the document
6. **webanno.custom.PHI** - the value of **%TYPE** key - used to access PHI entity-level boundaries and labels

The processing and extraction done can be tracked in [src/data_handlers/grascco_data_handler.py](src/data_handlers/grascco_data_handler.py) script.

While extracting data, some inconsistencies were found in the annotations - 

**(a)** Label key (**kind**) was missing for the last entity (**AGE**) in **Queisser.txt** [document](data/raw/11502329/grascco_phi_annotation_json/Queisser.txt_phi.json).

| Document Title  | Boundary     | Token  | Sentence                     |
|-----------------|--------------|--------|------------------------------|
| Queisser.txt    | (1219, 1221) | 49     | Untersuchungsbefund: 49jähr. |

This entity with missing label was fixed manually by marking it as an **AGE** entity.

<br>
The final statistics of the processed annotations are as follows:

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

**(b)** Wrong counts for two labels, **LOCATION_CITY** and **LOCATION_ZIP**, were reported in the original [Research Article](https://ebooks.iospress.nl/doi/10.3233/SHTI240853), values swapped in consequent rows.

 N | Label                  | Count | Count (RA) | Note
---| -----------------------| ----- |------------|---------------------------------
01 | DATE                   | 694   | 694        |
02 | NAME\_PATIENT          | 166   | 166        |
03 | NAME\_DOCTOR           | 154   | 154        |
04 | NAME\_TITLE            | 139   | 139        |
05 | LOCATION\_CITY         | 59    | 38         | Wrong count in RA, actual is 59
06 | ID                     | 58    | 58         |
07 | LOCATION\_ZIP          | 38    | 59         | Wrong count in RA, actual is 38
08 | LOCATION\_HOSPITAL     | 36    | 36         |
09 | LOCATION\_STREET       | 36    | 36         |
10 | AGE                    | 24    | 23         | Manually fixed one missing label
11 | CONTACT\_PHONE         | 18    | 18         |
12 | CONTACT\_FAX           | 7     | 7          |
13 | LOCATION\_COUNTRY      | 2     | 2          |
14 | LOCATION\_ORGANIZATION | 2     | 2          |
15 | PROFESSION             | 2     | 2          |
16 | CONTACT\_EMAIL         | 1     | 1          |
17 | NAME\_EXT              | 1     | 1          |
18 | NAME\_RELATIVE         | 1     | 1          |
19 | NAME\_USERNAME         | 1     | 1          |

List of all LOCATION_CITY (59) entities in different documents:
```
1. Alt-Neudorf, 2. Bad Arolsen, 3. Belgrad, 4. Berlin, 5. Berlin, 6. Berlin, 7. Berlin, 8. Berlin, 9. Berlin, 10. Bruchsal, 11. Crailsheim, 12. Flensburg, 13. Flensburg, 14. Flensburg, 15. Freiburg, 16. Freudenbrunn, 17. Gingen, 18. Graz, 19. Heidelberg, 20. Heidelberg, 21. Herborn, 22. Holzhausen, 23. Holzhausen, 24. Jena, 25. Kiel, 26. Klagenfurt, 27. Klagenfurt, 28. Klagenfurt, 29. Klagenfurt, 30. Klein Haasbeck, 31. Klein Haasbeck, 32. Klein Haasbeck, 33. Krefeld, 34. Krefeld, 35. München, 36. Neudorf, 37. Neukirchen, 38. Neustadt, 39. Neustadt, 40. Neustadt, 41. Neustadt, 42. Neustadt, 43. Neustadt, 44. Neustadt, 45. Neustadt, 46. Opfing, 47. Opfing, 48. Opfing, 49. St. Anna im Tale, 50. St. Johann am Bergle, 51. Stuttgart, 52. Trüllikon (ZH), 53. Villach, 54. Villach, 55. Weimar, 56. Wiesental, 57. Wiesental, 58. Wilhelmsburg, 59. Wilhelmsburg
```

List of all LOCATION_ZIP (38) entities in different documents:
```
1. 01334, 2. 09221, 3. 10117, 4. 10117, 5. 10247, 6. 12299, 7. 20223, 8. 20223, 9. 24937, 10. 24941, 11. 33455, 12. 33455, 13. 34443, 14. 35745, 15. 47809, 16. 47809, 17. 69115, 18. 72119, 19. 73333, 20. 76646, 21. 8010, 22. 9010, 23. 9011, 24. 9020, 25. 91022, 26. A-2236, 27. A-2236, 28. A-2236, 29. A-3336, 30. A-3337, 31. A-8120, 32. A-9011, 33. A-9011, 34. A-9011, 35. A-9011, 36. A-9011, 37. A-9012, 38. A-9580
```

<br>

**Rarely (count <= 10)** present labels and entities:

| Label                | Entity                            | Document Title          | Begin | End  |
|----------------------|-----------------------------------|-------------------------|-------|------|
| CONTACT_EMAIL        | termin.dot@uniklinik-berlin.de    | Weil.txt                | 392   | 422  |
| CONTACT_FAX          | 02216/325-15338                   | Dupuytren.txt           | 206   | 221  |
| CONTACT_FAX          | 0816/333-13284                    | Joubert.txt             | 141   | 155  |
| CONTACT_FAX          | +43 (453) 14-592-12098            | Meulengracht.txt        | 195   | 217  |
| CONTACT_FAX          | +43(0)333 775-8422334             | Schielaug.txt           | 171   | 192  |
| CONTACT_FAX          | +43(0)333 775-8447334             | Schuh.txt               | 187   | 208  |
| CONTACT_FAX          | +43(0)333 775-8447339             | Schuh.txt               | 331   | 352  |
| CONTACT_FAX          | 030 110-2619 o. 2452              | Weil.txt                | 371   | 391  |
| LOCATION_COUNTRY     | USA                               | Recklinghausen.txt      | 203   | 206  |
| LOCATION_COUNTRY     | Peru                              | Waldenström.txt         | 1020  | 1024 |
| LOCATION_ORGANIZATION| BVA                               | Joubert.txt             | 442   | 445  |
| LOCATION_ORGANIZATION| Alpen-Adria-Universität Kragenfurt| Theodor.txt             | 2686  | 2720 |
| NAME_EXT             | Fuß                               | Fleischmann.txt         | 5579  | 5582 |
| NAME_RELATIVE        | Alois Alzheimer                   | Amanda_Alzheimer.txt    | 6126  | 6141 |
| NAME_USERNAME        | WinA.                             | Tupolev_3.txt           | 298   | 303  |
| PROFESSION           | Floristin                         | Boeck.txt               | 1572  | 1581 |
| PROFESSION           | Maschinenbauingenieur             | Theodor.txt             | 2608  | 2629 |

A separate pandas [dataframe](data/grascco_ner_data.csv) is prepared with rows for all the documents and with additionally prepared BIOES tagged tokenized text per document to facilitate fine-tuning and evaluation.

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


Before preparing a 5-fold train/dev/test split, to evenly distribute rarely present entities: 

1. files containing labels with one entity - **CONTACT_EMAIL - Weil.txt**, **NAME_EXT - Fleischmann.txt**, **NAME_RELATIVE - Amanda_Alzheimer.txt** and **NAME_USERNAME - Tupolev_3.txt**  are kept in the training set, if we keep aside these files from any split, we loose significant amount of tokens and other entities that are present in these files.

2. files containing labels with two entities (e.g. **LOCATION_COUNTRY - Recklinghausen.txt, Waldenström.txt**) are split such that one file goes to train set and the other to test set.

3. files containing labels with three or more entities (e.g. **CONTACT_FAX**) are split such that one file goes to train set, one to dev set and the other to test set.


After this setup - train/dev/test sets contains the following files in every fold along with fold-wise rest of the files:

| Train                      | Dev                | Test                        |
|----------------------------|--------------------|-----------------------------|
| Weil.txt<br>Fleischmann.txt<br>Amanda_Alzheimer.txt<br>Tupolev_3.txt<br>Schielaug.txt<br>Waldenström.txt<br>Theodor.txt| Schuh.txt<br>Dupuytren.txt | Joubert.txt<br>Meulengracht.txt<br>Recklinghausen.txt<br>Boeck.txt |

In the next step, 5 more files are selected randomly for test set excluding the files from the table above.

Finally, with the rest 45 files a 5-fold split is performed to create train/dev sets.

| Label/Stat           | K-1                                   | K-2                                   | K-3                                   | K-4                                   | K-5                                   |
|----------------------|---------------------------------------|---------------------------------------|---------------------------------------|---------------------------------------|---------------------------------------|
| Total Files          | Train: 43<br>Dev: 11<br>Test: 9       | Train: 42<br>Dev: 12<br>Test: 9       | Train: 42<br>Dev: 12<br>Test: 9       | Train: 43<br>Dev: 11<br>Test: 9       | Train: 43<br>Dev: 11<br>Test: 9       |
| Total Sentences      | Train: 2004<br>Dev: 579<br>Test: 289  | Train: 2209<br>Dev: 374<br>Test: 289  | Train: 2198<br>Dev: 385<br>Test: 289  | Train: 2019<br>Dev: 564<br>Test: 289  | Train: 2018<br>Dev: 565<br>Test: 289  |
| Total Tokens         | Train: 29065<br>Dev: 7868<br>Test: 5059| Train: 30587<br>Dev: 6346<br>Test: 5059| Train: 31192<br>Dev: 5741<br>Test: 5059| Train: 29654<br>Dev: 7279<br>Test: 5059| Train: 29019<br>Dev: 7914<br>Test: 5059|
| Total Entities       | Train: 1028<br>Dev: 216<br>Test: 195  | Train: 972<br>Dev: 272<br>Test: 195   | Train: 1023<br>Dev: 221<br>Test: 195  | Train: 969<br>Dev: 275<br>Test: 195   | Train: 952<br>Dev: 292<br>Test: 195   |
| DATE                 | Train: 523<br>Dev: 84<br>Test: 87     | Train: 471<br>Dev: 136<br>Test: 87    | Train: 521<br>Dev: 86<br>Test: 87     | Train: 470<br>Dev: 137<br>Test: 87    | Train: 483<br>Dev: 124<br>Test: 87    |
| NAME_PATIENT         | Train: 119<br>Dev: 27<br>Test: 20     | Train: 121<br>Dev: 25<br>Test: 20     | Train: 122<br>Dev: 24<br>Test: 20     | Train: 115<br>Dev: 31<br>Test: 20     | Train: 119<br>Dev: 27<br>Test: 20     |
| NAME_DOCTOR          | Train: 105<br>Dev: 28<br>Test: 21     | Train: 108<br>Dev: 25<br>Test: 21     | Train: 109<br>Dev: 24<br>Test: 21     | Train: 109<br>Dev: 24<br>Test: 21     | Train: 98<br>Dev: 35<br>Test: 21      |
| NAME_TITLE           | Train: 94<br>Dev: 26<br>Test: 19      | Train: 96<br>Dev: 24<br>Test: 19      | Train: 99<br>Dev: 21<br>Test: 19      | Train: 98<br>Dev: 22<br>Test: 19      | Train: 87<br>Dev: 33<br>Test: 19      |
| LOCATION_CITY        | Train: 39<br>Dev: 11<br>Test: 9       | Train: 35<br>Dev: 15<br>Test: 9       | Train: 34<br>Dev: 16<br>Test: 9       | Train: 36<br>Dev: 14<br>Test: 9       | Train: 36<br>Dev: 14<br>Test: 9       |
| ID                   | Train: 41<br>Dev: 4<br>Test: 13       | Train: 32<br>Dev: 13<br>Test: 13      | Train: 31<br>Dev: 14<br>Test: 13      | Train: 37<br>Dev: 8<br>Test: 13       | Train: 33<br>Dev: 12<br>Test: 13      |
| LOCATION_ZIP         | Train: 24<br>Dev: 8<br>Test: 6        | Train: 23<br>Dev: 9<br>Test: 6        | Train: 22<br>Dev: 10<br>Test: 6       | Train: 23<br>Dev: 9<br>Test: 6        | Train: 20<br>Dev: 12<br>Test: 6       |
| LOCATION_HOSPITAL    | Train: 25<br>Dev: 7<br>Test: 4        | Train: 28<br>Dev: 4<br>Test: 4        | Train: 27<br>Dev: 5<br>Test: 4        | Train: 24<br>Dev: 8<br>Test: 4        | Train: 25<br>Dev: 7<br>Test: 4        |
| LOCATION_STREET      | Train: 23<br>Dev: 7<br>Test: 6        | Train: 22<br>Dev: 8<br>Test: 6        | Train: 21<br>Dev: 9<br>Test: 6        | Train: 21<br>Dev: 9<br>Test: 6        | Train: 18<br>Dev: 12<br>Test: 6       |
| AGE                  | Train: 19<br>Dev: 4<br>Test: 1        | Train: 19<br>Dev: 4<br>Test: 1        | Train: 20<br>Dev: 3<br>Test: 1        | Train: 18<br>Dev: 5<br>Test: 1        | Train: 18<br>Dev: 5<br>Test: 1        |
| CONTACT_PHONE        | Train: 7<br>Dev: 7<br>Test: 4         | Train: 9<br>Dev: 5<br>Test: 4         | Train: 8<br>Dev: 6<br>Test: 4         | Train: 9<br>Dev: 5<br>Test: 4         | Train: 7<br>Dev: 7<br>Test: 4         |
| CONTACT_FAX          | Train: 2<br>Dev: 3<br>Test: 2         | Train: 2<br>Dev: 3<br>Test: 2         | Train: 2<br>Dev: 3<br>Test: 2         | Train: 2<br>Dev: 3<br>Test: 2         | Train: 1<br>Dev: 4<br>Test: 2         |
| LOCATION_COUNTRY     | Train: 1<br>Dev: 0<br>Test: 1         | Train: 0<br>Dev: 1<br>Test: 1         | Train: 1<br>Dev: 0<br>Test: 1         | Train: 1<br>Dev: 0<br>Test: 1         | Train: 1<br>Dev: 0<br>Test: 1         |
| LOCATION_ORGANIZATION| Train: 1<br>Dev: 0<br>Test: 1         | Train: 1<br>Dev: 0<br>Test: 1         | Train: 1<br>Dev: 0<br>Test: 1         | Train: 1<br>Dev: 0<br>Test: 1         | Train: 1<br>Dev: 0<br>Test: 1         |
| PROFESSION           | Train: 1<br>Dev: 0<br>Test: 1         | Train: 1<br>Dev: 0<br>Test: 1         | Train: 1<br>Dev: 0<br>Test: 1         | Train: 1<br>Dev: 0<br>Test: 1         | Train: 1<br>Dev: 0<br>Test: 1         |
| CONTACT_EMAIL        | Train: 1<br>Dev: 0<br>Test: 0         | Train: 1<br>Dev: 0<br>Test: 0         | Train: 1<br>Dev: 0<br>Test: 0         | Train: 1<br>Dev: 0<br>Test: 0         | Train: 1<br>Dev: 0<br>Test: 0         |
| NAME_EXT             | Train: 1<br>Dev: 0<br>Test: 0         | Train: 1<br>Dev: 0<br>Test: 0         | Train: 1<br>Dev: 0<br>Test: 0         | Train: 1<br>Dev: 0<br>Test: 0         | Train: 1<br>Dev: 0<br>Test: 0         |
| NAME_RELATIVE        | Train: 1<br>Dev: 0<br>Test: 0         | Train: 1<br>Dev: 0<br>Test: 0         | Train: 1<br>Dev: 0<br>Test: 0         | Train: 1<br>Dev: 0<br>Test: 0         | Train: 1<br>Dev: 0<br>Test: 0         |
| NAME_USERNAME        | Train: 1<br>Dev: 0<br>Test: 0         | Train: 1<br>Dev: 0<br>Test: 0         | Train: 1<br>Dev: 0<br>Test: 0         | Train: 1<br>Dev: 0<br>Test: 0         | Train: 1<br>Dev: 0<br>Test: 0         |

Due to (1) curation, the test set contains only the rest 15 labels.


Three separate transformers based language models are fine-tuned for the NER downstream task on these annotations of GraSCCo corpus:

1. google-bert/bert-base-german-cased
2. FacebookAI/xlm-roberta-large
3. deepset/gelectra-large

## Model Performance

(macro avg):

| Model              | Precision     | Recall        | F1-score      |
|--------------------|---------------|---------------|---------------|
| gBERT-base         | 0.51 ± 0.040  | 0.57 ± 0.046  | 0.53 ± 0.044  |
| XLM-RoBERTa-large  | 0.61 ± 0.019  | 0.62 ± 0.047  | 0.60 ± 0.036  |
| gELECTRA-large     | 0.56 ± 0.043  | 0.61 ± 0.030  | 0.58 ± 0.038  |

(micro avg):

| Model              | Precision     | Recall        | F1-score      |
|--------------------|---------------|---------------|---------------|
| gBERT-base         | 0.79 ± 0.045  | 0.84 ± 0.035  | 0.81 ± 0.040  |
| XLM-RoBERTa-large  | 0.84 ± 0.022  | 0.87 ± 0.023  | 0.85 ± 0.021  |
| gELECTRA-large     | 0.83 ± 0.040  | 0.87 ± 0.021  | 0.85 ± 0.030  |
