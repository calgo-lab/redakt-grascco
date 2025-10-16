# redakt-grascco

For developing NER models based on [GraSCCo_PHI](https://zenodo.org/records/11502329) corpus.

## About GraSCCo corpus

GraSCCo - short for <u>Gra</u>z <u>S</u>ynthetic <u>C</u>linical text <u>Co</u>rpus - is a collection of artificially generated semi-structured and unstructured German-language clinical summaries designed to support research in clinical Natural Language Processing (cNLP).

Research Article: [GRASCCO — The First Publicly Shareable, Multiply-Alienated German Clinical Text Corpus](https://ebooks.iospress.nl/doi/10.3233/SHTI220805)<br>
Zenodo Data Repository: https://zenodo.org/records/6539131

Later, the corpus was annotated with PHI (Protected Health Information) entities. The annotations were exported XMI and JSON formats created with the INCEpTION annotation platform.

Research Article: [De-Identifying GRASCCO – A Pilot Study for the De-Identification of the German Medical Text Project (GeMTeX) Corpus](https://ebooks.iospress.nl/doi/10.3233/SHTI240853) <br>
Zenodo Data Repository: https://zenodo.org/records/11502329

## Data pre-processing and insights

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


## Data preparation for NER model fine-tuning

Before preparing a 5-fold cross-validation setup, to evenly distribute rarely present entities:

1. files containing labels with one entity - **CONTACT_EMAIL - Weil.txt**, **NAME_EXT - Fleischmann.txt**, **NAME_RELATIVE - Amanda_Alzheimer.txt** and **NAME_USERNAME - Tupolev_3.txt**  are kept in the training set, if we keep aside these files from any split, we loose significant amount of tokens and other entities that are present in these files.

2. files containing labels with two entities (e.g. **LOCATION_COUNTRY - Recklinghausen.txt, Waldenström.txt**) are split such that one file goes to train set and the other to test set.

3. files containing labels with three or more entities (e.g. **CONTACT_FAX**) are split such that one file goes to train set, one to dev set and the other to test set.


After this setup - train/dev/test sets contains the following files in every fold along with fold-wise rest of the files:

| Train (7)                  | Dev (2)            | Test (4)                    |
|----------------------------|--------------------|-----------------------------|
| Weil.txt<br>Fleischmann.txt<br>Amanda_Alzheimer.txt<br>Tupolev_3.txt<br>Schielaug.txt<br>Waldenström.txt<br>Theodor.txt| Schuh.txt<br>Dupuytren.txt | Joubert.txt<br>Meulengracht.txt<br>Recklinghausen.txt<br>Boeck.txt |

In the next step, with the rest 50 files a 5-fold cross validation split is performed - to create 5 separate train(60%)/dev(20%)/test(20%) sets with rolling.

| Stat/Label           | Fold 1                                 | Fold 2                                   | Fold 3                                   | Fold 4                                   | Fold 5                                   |
|-----------------------|------------------------------------------|------------------------------------------|------------------------------------------|------------------------------------------|------------------------------------------|
| Total Files           | Train: 37<br>Dev: 12<br>Test: 14         | Train: 37<br>Dev: 12<br>Test: 14         | Train: 37<br>Dev: 12<br>Test: 14         | Train: 37<br>Dev: 12<br>Test: 14         | Train: 37<br>Dev: 12<br>Test: 14         |
| Total Sentences       | Train: 1527<br>Dev: 626<br>Test: 719     | Train: 1759<br>Dev: 664<br>Test: 449     | Train: 1973<br>Dev: 394<br>Test: 505     | Train: 1944<br>Dev: 450<br>Test: 478     | Train: 1768<br>Dev: 423<br>Test: 681     |
| Total Tokens          | Train: 21923<br>Dev: 8713<br>Test: 11356 | Train: 25161<br>Dev: 10605<br>Test: 6226 | Train: 29160<br>Dev: 5475<br>Test: 7357  | Train: 28668<br>Dev: 6606<br>Test: 6718  | Train: 26561<br>Dev: 5967<br>Test: 9464  |
| Total Entities        | Train: 821<br>Dev: 282<br>Test: 336      | Train: 877<br>Dev: 321<br>Test: 241      | Train: 950<br>Dev: 226<br>Test: 263      | Train: 919<br>Dev: 248<br>Test: 272      | Train: 885<br>Dev: 257<br>Test: 297      |
| Train Files           | Amanda_Alzheimer.txt<br>Baastrup.txt<br>Beuerle.txt<br>Colon_Fake_A.txt<br>Colon_Fake_B.txt<br>Colon_Fake_C.txt<br>Colon_Fake_D.txt<br>Colon_Fake_E.txt<br>Colon_Fake_G.txt<br>Colon_Fake_I.txt<br>Colon_Fake_K.txt<br>Ehrenberger.txt<br>Fleischmann.txt<br>Haefner.txt<br>Jenninger.txt<br>Koenig.txt<br>Leitner.txt<br>Meyr.txt<br>Neubauer.txt<br>Osler.txt<br>Queisser.txt<br>Quervain.txt<br>Rieser.txt<br>Schielaug.txt<br>Stölzl.txt<br>Sudeck.txt<br>Theodor.txt<br>Tupolev_1.txt<br>Tupolev_2.txt<br>Tupolev_3.txt<br>Tupolev_4.txt<br>Utz.txt<br>Vogler.txt<br>Waldenström.txt<br>Weil.txt<br>Xavier.txt<br>Ypsilanti.txt | Albers.txt<br>Amanda_Alzheimer.txt<br>Baastrup.txt<br>Clausthal.txt<br>Colon_Fake_A.txt<br>Colon_Fake_E.txt<br>Colon_Fake_F.txt<br>Colon_Fake_G.txt<br>Colon_Fake_I.txt<br>Colon_Fake_J.txt<br>Colon_Fake_K.txt<br>Dewald.txt<br>Ehrenberger.txt<br>Fleischmann.txt<br>Gebauer.txt<br>Jadassohn.txt<br>Kawasaki.txt<br>Meyr.txt<br>Neubauer.txt<br>Osler.txt<br>Praechtel.txt<br>Queisser.txt<br>Quervain.txt<br>Rieser.txt<br>Schielaug.txt<br>Stölzl.txt<br>Sudeck.txt<br>Theodor.txt<br>Tupolev_1.txt<br>Tupolev_2.txt<br>Tupolev_3.txt<br>Vogler.txt<br>Waldenström.txt<br>Wankel.txt<br>Weil.txt<br>Xavier.txt<br>Ypsilanti.txt | Albers.txt<br>Amanda_Alzheimer.txt<br>Baastrup.txt<br>Cajal.txt<br>Clausthal.txt<br>Colon_Fake_E.txt<br>Colon_Fake_F.txt<br>Colon_Fake_G.txt<br>Colon_Fake_H.txt<br>Colon_Fake_I.txt<br>Colon_Fake_J.txt<br>Dewald.txt<br>Ehrenberger.txt<br>Fabry.txt<br>Fleischmann.txt<br>Fuss.txt<br>Gebauer.txt<br>Ilgner.txt<br>Jadassohn.txt<br>Kawasaki.txt<br>Obradovic.txt<br>Popovic.txt<br>Praechtel.txt<br>Queisser.txt<br>Rieser.txt<br>Schielaug.txt<br>Schnitzler.txt<br>Theodor.txt<br>Tupolev_1.txt<br>Tupolev_3.txt<br>Vogler.txt<br>Waldenström.txt<br>Wankel.txt<br>Weber.txt<br>Weil.txt<br>Xavier.txt<br>Zezelj.txt | Albers.txt<br>Amanda_Alzheimer.txt<br>Beuerle.txt<br>Cajal.txt<br>Clausthal.txt<br>Colon_Fake_B.txt<br>Colon_Fake_C.txt<br>Colon_Fake_D.txt<br>Colon_Fake_F.txt<br>Colon_Fake_H.txt<br>Colon_Fake_J.txt<br>Dewald.txt<br>Fabry.txt<br>Fleischmann.txt<br>Fuss.txt<br>Gebauer.txt<br>Haefner.txt<br>Ilgner.txt<br>Jadassohn.txt<br>Jenninger.txt<br>Kawasaki.txt<br>Koenig.txt<br>Leitner.txt<br>Obradovic.txt<br>Popovic.txt<br>Praechtel.txt<br>Schielaug.txt<br>Schnitzler.txt<br>Theodor.txt<br>Tupolev_3.txt<br>Tupolev_4.txt<br>Utz.txt<br>Waldenström.txt<br>Wankel.txt<br>Weber.txt<br>Weil.txt<br>Zezelj.txt | Amanda_Alzheimer.txt<br>Beuerle.txt<br>Cajal.txt<br>Colon_Fake_A.txt<br>Colon_Fake_B.txt<br>Colon_Fake_C.txt<br>Colon_Fake_D.txt<br>Colon_Fake_H.txt<br>Colon_Fake_K.txt<br>Fabry.txt<br>Fleischmann.txt<br>Fuss.txt<br>Haefner.txt<br>Ilgner.txt<br>Jenninger.txt<br>Koenig.txt<br>Leitner.txt<br>Meyr.txt<br>Neubauer.txt<br>Obradovic.txt<br>Osler.txt<br>Popovic.txt<br>Quervain.txt<br>Schielaug.txt<br>Schnitzler.txt<br>Stölzl.txt<br>Sudeck.txt<br>Theodor.txt<br>Tupolev_2.txt<br>Tupolev_3.txt<br>Tupolev_4.txt<br>Utz.txt<br>Waldenström.txt<br>Weber.txt<br>Weil.txt<br>Ypsilanti.txt<br>Zezelj.txt |
| Dev Files             | Albers.txt<br>Clausthal.txt<br>Colon_Fake_F.txt<br>Colon_Fake_J.txt<br>Dewald.txt<br>Dupuytren.txt<br>Gebauer.txt<br>Jadassohn.txt<br>Kawasaki.txt<br>Praechtel.txt<br>Schuh.txt<br>Wankel.txt | Cajal.txt<br>Colon_Fake_H.txt<br>Dupuytren.txt<br>Fabry.txt<br>Fuss.txt<br>Ilgner.txt<br>Obradovic.txt<br>Popovic.txt<br>Schnitzler.txt<br>Schuh.txt<br>Weber.txt<br>Zezelj.txt | Beuerle.txt<br>Colon_Fake_B.txt<br>Colon_Fake_C.txt<br>Colon_Fake_D.txt<br>Dupuytren.txt<br>Haefner.txt<br>Jenninger.txt<br>Koenig.txt<br>Leitner.txt<br>Schuh.txt<br>Tupolev_4.txt<br>Utz.txt | Colon_Fake_A.txt<br>Colon_Fake_K.txt<br>Dupuytren.txt<br>Meyr.txt<br>Neubauer.txt<br>Osler.txt<br>Quervain.txt<br>Schuh.txt<br>Stölzl.txt<br>Sudeck.txt<br>Tupolev_2.txt<br>Ypsilanti.txt | Baastrup.txt<br>Colon_Fake_E.txt<br>Colon_Fake_G.txt<br>Colon_Fake_I.txt<br>Dupuytren.txt<br>Ehrenberger.txt<br>Queisser.txt<br>Rieser.txt<br>Schuh.txt<br>Tupolev_1.txt<br>Vogler.txt<br>Xavier.txt |
| Test Files            | Boeck.txt<br>Cajal.txt<br>Colon_Fake_H.txt<br>Fabry.txt<br>Fuss.txt<br>Ilgner.txt<br>Joubert.txt<br>Meulengracht.txt<br>Obradovic.txt<br>Popovic.txt<br>Recklinghausen.txt<br>Schnitzler.txt<br>Weber.txt<br>Zezelj.txt | Beuerle.txt<br>Boeck.txt<br>Colon_Fake_B.txt<br>Colon_Fake_C.txt<br>Colon_Fake_D.txt<br>Haefner.txt<br>Jenninger.txt<br>Joubert.txt<br>Koenig.txt<br>Leitner.txt<br>Meulengracht.txt<br>Recklinghausen.txt<br>Tupolev_4.txt<br>Utz.txt | Boeck.txt<br>Colon_Fake_A.txt<br>Colon_Fake_K.txt<br>Joubert.txt<br>Meulengracht.txt<br>Meyr.txt<br>Neubauer.txt<br>Osler.txt<br>Quervain.txt<br>Recklinghausen.txt<br>Stölzl.txt<br>Sudeck.txt<br>Tupolev_2.txt<br>Ypsilanti.txt | Baastrup.txt<br>Boeck.txt<br>Colon_Fake_E.txt<br>Colon_Fake_G.txt<br>Colon_Fake_I.txt<br>Ehrenberger.txt<br>Joubert.txt<br>Meulengracht.txt<br>Queisser.txt<br>Recklinghausen.txt<br>Rieser.txt<br>Tupolev_1.txt<br>Vogler.txt<br>Xavier.txt | Albers.txt<br>Boeck.txt<br>Clausthal.txt<br>Colon_Fake_F.txt<br>Colon_Fake_J.txt<br>Dewald.txt<br>Gebauer.txt<br>Jadassohn.txt<br>Joubert.txt<br>Kawasaki.txt<br>Meulengracht.txt<br>Praechtel.txt<br>Recklinghausen.txt<br>Wankel.txt |
| DATE                  | Train: 398<br>Dev: 158<br>Test: 138      | Train: 448<br>Dev: 128<br>Test: 118      | Train: 462<br>Dev: 108<br>Test: 124      | Train: 456<br>Dev: 114<br>Test: 124      | Train: 412<br>Dev: 114<br>Test: 168      |
| NAME_PATIENT          | Train: 88<br>Dev: 35<br>Test: 43         | Train: 99<br>Dev: 38<br>Test: 29         | Train: 113<br>Dev: 24<br>Test: 29        | Train: 113<br>Dev: 24<br>Test: 29        | Train: 102<br>Dev: 24<br>Test: 40        |
| NAME_DOCTOR           | Train: 91<br>Dev: 24<br>Test: 39         | Train: 96<br>Dev: 39<br>Test: 19         | Train: 106<br>Dev: 19<br>Test: 29        | Train: 98<br>Dev: 29<br>Test: 27         | Train: 103<br>Dev: 27<br>Test: 24        |
| NAME_TITLE            | Train: 84<br>Dev: 23<br>Test: 32         | Train: 84<br>Dev: 32<br>Test: 23         | Train: 91<br>Dev: 23<br>Test: 25         | Train: 90<br>Dev: 25<br>Test: 24         | Train: 92<br>Dev: 24<br>Test: 23         |
| LOCATION_CITY         | Train: 32<br>Dev: 9<br>Test: 18          | Train: 29<br>Dev: 20<br>Test: 10         | Train: 36<br>Dev: 12<br>Test: 11         | Train: 35<br>Dev: 13<br>Test: 11         | Train: 39<br>Dev: 13<br>Test: 7          |
| ID                    | Train: 37<br>Dev: 6<br>Test: 15          | Train: 32<br>Dev: 13<br>Test: 13         | Train: 33<br>Dev: 11<br>Test: 14         | Train: 28<br>Dev: 12<br>Test: 18         | Train: 34<br>Dev: 16<br>Test: 8          |
| LOCATION_ZIP          | Train: 20<br>Dev: 5<br>Test: 13          | Train: 17<br>Dev: 13<br>Test: 8          | Train: 21<br>Dev: 8<br>Test: 9           | Train: 21<br>Dev: 9<br>Test: 8           | Train: 25<br>Dev: 8<br>Test: 5           |
| LOCATION_HOSPITAL     | Train: 20<br>Dev: 7<br>Test: 9           | Train: 25<br>Dev: 9<br>Test: 2           | Train: 28<br>Dev: 2<br>Test: 6           | Train: 23<br>Dev: 6<br>Test: 7           | Train: 22<br>Dev: 7<br>Test: 7           |
| LOCATION_STREET       | Train: 19<br>Dev: 5<br>Test: 12          | Train: 17<br>Dev: 12<br>Test: 7          | Train: 22<br>Dev: 7<br>Test: 7           | Train: 20<br>Dev: 7<br>Test: 9           | Train: 22<br>Dev: 9<br>Test: 5           |
| AGE                   | Train: 16<br>Dev: 2<br>Test: 6           | Train: 14<br>Dev: 5<br>Test: 5           | Train: 18<br>Dev: 4<br>Test: 2           | Train: 17<br>Dev: 1<br>Test: 6           | Train: 16<br>Dev: 5<br>Test: 3           |
| CONTACT_PHONE         | Train: 7<br>Dev: 5<br>Test: 6            | Train: 7<br>Dev: 9<br>Test: 2            | Train: 11<br>Dev: 5<br>Test: 2           | Train: 9<br>Dev: 5<br>Test: 4            | Train: 9<br>Dev: 7<br>Test: 2            |
| CONTACT_FAX           | Train: 2<br>Dev: 3<br>Test: 2            | Train: 2<br>Dev: 3<br>Test: 2            | Train: 2<br>Dev: 3<br>Test: 2            | Train: 2<br>Dev: 3<br>Test: 2            | Train: 2<br>Dev: 3<br>Test: 2            |
| LOCATION_COUNTRY      | Train: 1<br>Dev: 0<br>Test: 1            | Train: 1<br>Dev: 0<br>Test: 1            | Train: 1<br>Dev: 0<br>Test: 1            | Train: 1<br>Dev: 0<br>Test: 1            | Train: 1<br>Dev: 0<br>Test: 1            |
| LOCATION_ORGANIZATION | Train: 1<br>Dev: 0<br>Test: 1            | Train: 1<br>Dev: 0<br>Test: 1            | Train: 1<br>Dev: 0<br>Test: 1            | Train: 1<br>Dev: 0<br>Test: 1            | Train: 1<br>Dev: 0<br>Test: 1            |
| PROFESSION            | Train: 1<br>Dev: 0<br>Test: 1            | Train: 1<br>Dev: 0<br>Test: 1            | Train: 1<br>Dev: 0<br>Test: 1            | Train: 1<br>Dev: 0<br>Test: 1            | Train: 1<br>Dev: 0<br>Test: 1            |
| CONTACT_EMAIL         | Train: 1<br>Dev: 0<br>Test: 0            | Train: 1<br>Dev: 0<br>Test: 0            | Train: 1<br>Dev: 0<br>Test: 0            | Train: 1<br>Dev: 0<br>Test: 0            | Train: 1<br>Dev: 0<br>Test: 0            |
| NAME_EXT              | Train: 1<br>Dev: 0<br>Test: 0            | Train: 1<br>Dev: 0<br>Test: 0            | Train: 1<br>Dev: 0<br>Test: 0            | Train: 1<br>Dev: 0<br>Test: 0            | Train: 1<br>Dev: 0<br>Test: 0            |
| NAME_RELATIVE         | Train: 1<br>Dev: 0<br>Test: 0            | Train: 1<br>Dev: 0<br>Test: 0            | Train: 1<br>Dev: 0<br>Test: 0            | Train: 1<br>Dev: 0<br>Test: 0            | Train: 1<br>Dev: 0<br>Test: 0            |
| NAME_USERNAME         | Train: 1<br>Dev: 0<br>Test: 0            | Train: 1<br>Dev: 0<br>Test: 0            | Train: 1<br>Dev: 0<br>Test: 0            | Train: 1<br>Dev: 0<br>Test: 0            | Train: 1<br>Dev: 0<br>Test: 0            |

Due to (1) curation, the test set contains only the rest 15 labels.


## Selected PLMs and frameworks

Three separate transformers based pre-trained language models are fine-tuned for the NER downstream task on the GraSCCo corpus using the FLERT approach (i.e., Flair’s transformer embeddings with extended context via use_context=True in TransformerWordEmbeddings class):

1. 🤗 [google-bert/bert-base-german-cased](https://huggingface.co/google-bert/bert-base-german-cased) (<b>aka</b> bert-base-german-cased)
2. 🤗 [xlm-roberta-large](https://huggingface.co/FacebookAI/xlm-roberta-large) (<b>aka</b> xlm-roberta-large)
3. 🤗 [deepset/gelectra-large](https://huggingface.co/deepset/gelectra-large) (<b>aka</b> gelectra-large)

Additionally, checkpoint of NER models fine-tuned on the CodE Alltag corpus are further fine-tuned with classification head for labels present in GraSCCo corpus:

GitHub: [calgo-lab/redakt-codealltag](https://github.com/calgo-lab/redakt-codealltag)

4. calgo-lab/codealltag-ner-bert-base-german-cased-flert-175k [K=5] (<b>aka</b> codealltag-bert-base-german-cased)
5. calgo-lab/codealltag-ner-xlm-roberta-large-flert-175k [K=5] (<b>aka</b> codealltag-xlm-roberta-large)
6. calgo-lab/codealltag-ner-gelectra-large-flert-175k [K=4] (<b>aka</b> codealltag-gelectra-large)

## System setup

The experiments were performed on a system with following configuration:

| Package      | Version      |
|-------------|-------------|
| datasets    | 4.0.0       |
| flair       | 0.15.1      |
| pyarrow     | 20.0.0      |
| tokenizers  | 0.21.4      |
| torch       | 2.7.1+cu128 |
| transformers| 4.49.0      |

## Fine-tuning parameters
The following hyperparameters were used for fine-tuning all the three models:

* learning_rate: "5e-05"
* mini_batch_size: "1"
* max_epochs: "35"
* shuffle: "True"
* context_size: "64"
* LinearScheduler | warmup_fraction: '0.1'


## Experiments 

📊 View experiments on [Weights & Biases](https://wandb.ai/sksdotsauravs-dev/redakt-grascco?nw=nwusersksdotsauravs)


## Overall model performance

NER performance comparison of all models on the test set with mean and standard deviation over 5-folds cross validation setup:

<b>(micro avg)</b>:

| Model                             | Precision      | Recall         | F1-score       | Support   |
|:----------------------------------|:---------------|:---------------|:---------------|:----------|
| bert-base-german-cased            | 0.7976 ± 0.015 | 0.8304 ± 0.019 | 0.8135 ± 0.010 | 280 ± 33  |
| codealltag-bert-base-german-cased | 0.8539 ± 0.037 | 0.8688 ± 0.023 | 0.8611 ± 0.029 | 280 ± 33  |
| xlm-roberta-large                 | 0.8761 ± 0.028 | 0.8954 ± 0.022 | 0.8854 ± 0.022 | 280 ± 33  |
| codealltag-xlm-roberta-large      | <b>0.8773 ± 0.026</b> | <b>0.9047 ± 0.019</b> | <b>0.8907 ± 0.022</b> | 280 ± 33  |
| gelectra-large                    | 0.8746 ± 0.029 | 0.8986 ± 0.015 | 0.8863 ± 0.020 | 280 ± 33  |
| codealltag-gelectra-large         | 0.8604 ± 0.036 | 0.8890 ± 0.020 | 0.8743 ± 0.027 | 280 ± 33  |

![ner_micro_avg](reports/figures/entity_prediction_performance_comparison_of_models_paired_micro_avg.jpg)

<b>(macro avg)</b>:

| Model                             | Precision      | Recall         | F1-score       | Support   |
|:----------------------------------|:---------------|:---------------|:---------------|:----------|
| bert-base-german-cased            | 0.5256 ± 0.029 | 0.5553 ± 0.038 | 0.5277 ± 0.025 | 280 ± 33  |
| codealltag-bert-base-german-cased | 0.5667 ± 0.073 | 0.5976 ± 0.062 | 0.5728 ± 0.068 | 280 ± 33  |
| xlm-roberta-large                 | 0.6141 ± 0.057 | 0.6405 ± 0.043 | 0.6190 ± 0.047 | 280 ± 33  |
| codealltag-xlm-roberta-large      | <b>0.6151 ± 0.058</b> | <b>0.6459 ± 0.052</b> | <b>0.6243 ± 0.056</b> | 280 ± 33  |
| gelectra-large                    | 0.5645 ± 0.049 | 0.6187 ± 0.016 | 0.5815 ± 0.037 | 280 ± 33  |
| codealltag-gelectra-large         | 0.5596 ± 0.041 | 0.6057 ± 0.027 | 0.5742 ± 0.035 | 280 ± 33  |

![ner_macro_avg](reports/figures/entity_prediction_performance_comparison_of_models_paired_macro_avg.jpg)

<b>(weighted avg)</b>:

| Model                             | Precision      | Recall         | F1-score       | Support   |
|:----------------------------------|:---------------|:---------------|:---------------|:----------|
| bert-base-german-cased            | 0.8037 ± 0.011 | 0.8304 ± 0.019 | 0.8129 ± 0.010 | 280 ± 33  |
| codealltag-bert-base-german-cased | 0.8508 ± 0.034 | 0.8688 ± 0.023 | 0.8562 ± 0.027 | 280 ± 33  |
| xlm-roberta-large                 | <b>0.8828 ± 0.025</b> | 0.8954 ± 0.022 | 0.8856 ± 0.022 | 280 ± 33  |
| codealltag-xlm-roberta-large      | 0.8796 ± 0.026 | <b>0.9047 ± 0.019</b> | <b>0.8893 ± 0.023</b> | 280 ± 33  |
| gelectra-large                    | 0.8773 ± 0.027 | 0.8986 ± 0.015 | 0.8846 ± 0.019 | 280 ± 33  |
| codealltag-gelectra-large         | 0.8642 ± 0.032 | 0.8890 ± 0.020 | 0.8735 ± 0.025 | 280 ± 33  |

![ner_weighted_avg](reports/figures/entity_prediction_performance_comparison_of_models_paired_weighted_avg.jpg)

<br>

## Label-wise model performance

<b>(DATE):</b>

| Model                             | Precision      | Recall         | F1-score       | Support   |
|:----------------------------------|:---------------|:---------------|:---------------|:----------|
| bert-base-german-cased            | 0.9152 ± 0.032 | 0.9484 ± 0.039 | 0.9314 ± 0.034 | 134 ± 18  |
| codealltag-bert-base-german-cased | 0.9602 ± 0.019 | 0.9768 ± 0.017 | 0.9683 ± 0.015 | 134 ± 18  |
| xlm-roberta-large                 | <b>0.9698 ± 0.019</b> | 0.9742 ± 0.020 | <b>0.9720 ± 0.018</b> | 134 ± 18  |
| codealltag-xlm-roberta-large      | 0.9680 ± 0.016 | 0.9747 ± 0.016 | 0.9713 ± 0.015 | 134 ± 18  |
| gelectra-large                    | 0.9622 ± 0.020 | <b>0.9793 ± 0.021</b> | 0.9706 ± 0.019 | 134 ± 18  |
| codealltag-gelectra-large         | 0.9623 ± 0.019 | 0.9738 ± 0.017 | 0.9679 ± 0.017 | 134 ± 18  |

![ner_date](reports/figures/entity_prediction_performance_comparison_of_models_paired_date.jpg)

<b>(NAME_DOCTOR):</b>

| Model                             | Precision      | Recall         | F1-score       | Support   |
|:----------------------------------|:---------------|:---------------|:---------------|:----------|
| bert-base-german-cased            | 0.7080 ± 0.092 | 0.8175 ± 0.042 | 0.7542 ± 0.048 | 27 ± 6    |
| codealltag-bert-base-german-cased | 0.6835 ± 0.061 | 0.8732 ± 0.063 | 0.7665 ± 0.061 | 27 ± 6    |
| xlm-roberta-large                 | 0.8141 ± 0.025 | <b>0.9926 ± 0.015</b> | <b>0.8943 ± 0.017</b> | 27 ± 6    |
| codealltag-xlm-roberta-large      | 0.7152 ± 0.087 | 0.9249 ± 0.033 | 0.8046 ± 0.066 | 27 ± 6    |
| gelectra-large                    | <b>0.8197 ± 0.037</b> | 0.9537 ± 0.031 | 0.8809 ± 0.023 | 27 ± 6    |
| codealltag-gelectra-large         | 0.7665 ± 0.083 | 0.9217 ± 0.071 | 0.8358 ± 0.073 | 27 ± 6    |

![ner_name_doctor](reports/figures/entity_prediction_performance_comparison_of_models_paired_name_doctor.jpg)

<b>(NAME_PATIENT):</b>

| Model                             | Precision      | Recall         | F1-score       | Support   |
|:----------------------------------|:---------------|:---------------|:---------------|:----------|
| bert-base-german-cased            | 0.7027 ± 0.111 | 0.6761 ± 0.120 | 0.6874 ± 0.112 | 34 ± 6    |
| codealltag-bert-base-german-cased | 0.7942 ± 0.086 | 0.7204 ± 0.091 | 0.7529 ± 0.077 | 34 ± 6    |
| xlm-roberta-large                 | <b>0.8968 ± 0.088</b> | 0.8006 ± 0.122 | 0.8428 ± 0.101 | 34 ± 6    |
| codealltag-xlm-roberta-large      | 0.8853 ± 0.089 | <b>0.8564 ± 0.103</b> | <b>0.8704 ± 0.096</b> | 34 ± 6    |
| gelectra-large                    | 0.8849 ± 0.087 | 0.8147 ± 0.091 | 0.8463 ± 0.079 | 34 ± 6    |
| codealltag-gelectra-large         | 0.8757 ± 0.108 | 0.8218 ± 0.085 | 0.8463 ± 0.089 | 34 ± 6    |

![ner_name_patient](reports/figures/entity_prediction_performance_comparison_of_models_paired_name_patient.jpg)

<b>(NAME_TITLE):</b>

| Model                             | Precision      | Recall         | F1-score       | Support   |
|:----------------------------------|:---------------|:---------------|:---------------|:----------|
| bert-base-german-cased            | 0.8131 ± 0.112 | 0.8722 ± 0.096 | 0.8411 ± 0.103 | 25 ± 3    |
| codealltag-bert-base-german-cased | 0.8089 ± 0.104 | 0.8562 ± 0.118 | 0.8310 ± 0.108 | 25 ± 3    |
| xlm-roberta-large                 | 0.8818 ± 0.108 | <b>0.9303 ± 0.059</b> | <b>0.9040 ± 0.084</b> | 25 ± 3    |
| codealltag-xlm-roberta-large      | 0.8375 ± 0.086 | 0.9095 ± 0.058 | 0.8713 ± 0.071 | 25 ± 3    |
| gelectra-large                    | <b>0.8958 ± 0.072</b> | 0.8875 ± 0.090 | 0.8913 ± 0.080 | 25 ± 3    |
| codealltag-gelectra-large         | 0.8756 ± 0.079 | 0.8911 ± 0.080 | 0.8829 ± 0.078 | 25 ± 3    |

![ner_name_title](reports/figures/entity_prediction_performance_comparison_of_models_paired_name_title.jpg)

<b>(ID):</b>

| Model                             | Precision      | Recall         | F1-score       | Support   |
|:----------------------------------|:---------------|:---------------|:---------------|:----------|
| bert-base-german-cased            | 0.7730 ± 0.109 | 0.7234 ± 0.099 | 0.7445 ± 0.090 | 13 ± 3    |
| codealltag-bert-base-german-cased | <b>0.8914 ± 0.082</b> | 0.7556 ± 0.142 | 0.8147 ± 0.116 | 13 ± 3    |
| xlm-roberta-large                 | 0.8345 ± 0.088 | 0.8305 ± 0.109 | 0.8308 ± 0.090 | 13 ± 3    |
| codealltag-xlm-roberta-large      | 0.8709 ± 0.063 | <b>0.9002 ± 0.083</b> | <b>0.8830 ± 0.060</b> | 13 ± 3    |
| gelectra-large                    | 0.7266 ± 0.123 | 0.7812 ± 0.062 | 0.7457 ± 0.069 | 13 ± 3    |
| codealltag-gelectra-large         | 0.7138 ± 0.184 | 0.8371 ± 0.138 | 0.7672 ± 0.166 | 13 ± 3    |

![ner_id](reports/figures/entity_prediction_performance_comparison_of_models_paired_id.jpg)

<b>(LOCATION_CITY):</b>

| Model                             | Precision      | Recall         | F1-score       | Support   |
|:----------------------------------|:---------------|:---------------|:---------------|:----------|
| bert-base-german-cased            | 0.8388 ± 0.138 | 0.7230 ± 0.101 | 0.7709 ± 0.100 | 11 ± 3    |
| codealltag-bert-base-german-cased | 0.8133 ± 0.172 | 0.7412 ± 0.108 | 0.7737 ± 0.138 | 11 ± 3    |
| xlm-roberta-large                 | 0.7991 ± 0.137 | 0.6374 ± 0.186 | 0.7053 ± 0.168 | 11 ± 3    |
| codealltag-xlm-roberta-large      | 0.8656 ± 0.111 | 0.7482 ± 0.101 | 0.7990 ± 0.094 | 11 ± 3    |
| gelectra-large                    | 0.8667 ± 0.130 | 0.7300 ± 0.094 | 0.7923 ± 0.109 | 11 ± 3    |
| codealltag-gelectra-large         | <b>0.8985 ± 0.129</b> | <b>0.7793 ± 0.108</b> | <b>0.8294 ± 0.104</b> | 11 ± 3    |

![ner_location_city](reports/figures/entity_prediction_performance_comparison_of_models_paired_location_city.jpg)

<b>(LOCATION_STREET):</b>

| Model                             | Precision      | Recall         | F1-score       | Support   |
|:----------------------------------|:---------------|:---------------|:---------------|:----------|
| bert-base-german-cased            | 0.5724 ± 0.183 | 0.6343 ± 0.173 | 0.5984 ± 0.176 | 8 ± 2     |
| codealltag-bert-base-german-cased | 0.8157 ± 0.115 | 0.9143 ± 0.114 | 0.8590 ± 0.103 | 8 ± 2     |
| xlm-roberta-large                 | 0.7343 ± 0.200 | 0.8079 ± 0.139 | 0.7667 ± 0.174 | 8 ± 2     |
| codealltag-xlm-roberta-large      | 0.9429 ± 0.114 | 0.9429 ± 0.114 | 0.9429 ± 0.114 | 8 ± 2     |
| gelectra-large                    | 0.8333 ± 0.149 | 0.9428 ± 0.070 | 0.8818 ± 0.113 | 8 ± 2     |
| codealltag-gelectra-large         | <b>0.9714 ± 0.057</b> | <b>0.9714 ± 0.057</b> | <b>0.9714 ± 0.057</b> | 8 ± 2     |

![ner_location_street](reports/figures/entity_prediction_performance_comparison_of_models_paired_location_street.jpg)

<b>(LOCATION_ZIP):</b>

| Model                             | Precision      | Recall         | F1-score       | Support   |
|:----------------------------------|:---------------|:---------------|:---------------|:----------|
| bert-base-german-cased            | 0.7932 ± 0.144 | 0.9278 ± 0.099 | 0.8516 ± 0.119 | 8 ± 2     |
| codealltag-bert-base-german-cased | 0.8657 ± 0.152 | 0.9100 ± 0.111 | 0.8859 ± 0.132 | 8 ± 2     |
| xlm-roberta-large                 | <b>0.9778 ± 0.044</b> | <b>0.9846 ± 0.031</b> | <b>0.9802 ± 0.025</b> | 8 ± 2     |
| codealltag-xlm-roberta-large      | 0.9556 ± 0.089 | 0.9750 ± 0.05  | 0.9647 ± 0.071 | 8 ± 2     |
| gelectra-large                    | 0.8871 ± 0.104 | 0.9528 ± 0.058 | 0.9168 ± 0.077 | 8 ± 2     |
| codealltag-gelectra-large         | 0.6296 ± 0.297 | 0.6831 ± 0.249 | 0.6513 ± 0.277 | 8 ± 2     |

![ner_location_zip](reports/figures/entity_prediction_performance_comparison_of_models_paired_location_zip.jpg)

<b>(CONTACT_PHONE):</b>

| Model                             | Precision      | Recall         | F1-score       | Support   |
|:----------------------------------|:---------------|:---------------|:---------------|:----------|
| bert-base-german-cased            | 0.2908 ± 0.173 | 0.5833 ± 0.247 | 0.3800 ± 0.202 | 3 ± 1     |
| codealltag-bert-base-german-cased | 0.4000 ± 0.192 | 0.7000 ± 0.245 | 0.4984 ± 0.205 | 3 ± 1     |
| xlm-roberta-large                 | 0.2133 ± 0.150 | 0.3833 ± 0.233 | 0.2717 ± 0.183 | 3 ± 1     |
| codealltag-xlm-roberta-large      | 0.3607 ± 0.158 | 0.6167 ± 0.145 | 0.4486 ± 0.164 | 3 ± 1     |
| gelectra-large                    | 0.3155 ± 0.160 | 0.5667 ± 0.133 | 0.3989 ± 0.162 | 3 ± 1     |
| codealltag-gelectra-large         | <b>0.4250 ± 0.150</b> | <b>0.7167 ± 0.194</b> | <b>0.5295 ± 0.164</b> | 3 ± 1     |

![ner_contact_phone](reports/figures/entity_prediction_performance_comparison_of_models_paired_contact_phone.jpg)

<b>(LOCATION_HOSPITAL):</b>

| Model                             | Precision      | Recall         | F1-score       | Support   |
|:----------------------------------|:---------------|:---------------|:---------------|:----------|
| bert-base-german-cased            | 0.2764 ± 0.071 | 0.5032 ± 0.278 | 0.3464 ± 0.116 | 6 ± 2     |
| codealltag-bert-base-german-cased | 0.3571 ± 0.202 | 0.5302 ± 0.326 | 0.4029 ± 0.212 | 6 ± 2     |
| xlm-roberta-large                 | 0.3394 ± 0.097 | 0.5651 ± 0.249 | 0.4119 ± 0.117 | 6 ± 2     |
| codealltag-xlm-roberta-large      | 0.3583 ± 0.082 | 0.4540 ± 0.093 | 0.3915 ± 0.068 | 6 ± 2     |
| gelectra-large                    | <b>0.3765 ± 0.114</b> | <b>0.6714 ± 0.242</b> | <b>0.4641 ± 0.118</b> | 6 ± 2     |
| codealltag-gelectra-large         | 0.3260 ± 0.112 | 0.5698 ± 0.294 | 0.4091 ± 0.162 | 6 ± 2     |

![ner_location_hospital](reports/figures/entity_prediction_performance_comparison_of_models_paired_location_hospital.jpg)

<b>(CONTACT_FAX):</b>

| Model                             | Precision      | Recall         | F1-score       | Support   |
|:----------------------------------|:---------------|:---------------|:---------------|:----------|
| bert-base-german-cased            | 0.0000 ± 0.000 | 0.0000 ± 0.000 | 0.0000 ± 0.000 | 2 ± 0     |
| codealltag-bert-base-german-cased | 0.0000 ± 0.000 | 0.0000 ± 0.000 | 0.0000 ± 0.000 | 2 ± 0     |
| xlm-roberta-large                 | <b>0.2000 ± 0.400</b> | <b>0.1000 ± 0.200</b> | <b>0.1333 ± 0.267</b> | 2 ± 0     |
| codealltag-xlm-roberta-large      | 0.1000 ± 0.200 | 0.1000 ± 0.200 | 0.1000 ± 0.200 | 2 ± 0     |
| gelectra-large                    | 0.0000 ± 0.000 | 0.0000 ± 0.000 | 0.0000 ± 0.000 | 2 ± 0     |
| codealltag-gelectra-large         | 0.0000 ± 0.000 | 0.0000 ± 0.000 | 0.0000 ± 0.000 | 2 ± 0     |

![ner_contact_fax](reports/figures/entity_prediction_performance_comparison_of_models_paired_contact_fax.jpg)

<b>(AGE):</b>

| Model                             | Precision      | Recall         | F1-score       | Support   |
|:----------------------------------|:---------------|:---------------|:---------------|:----------|
| bert-base-german-cased            | <b>1.0000 ± 0.000</b> | 0.7200 ± 0.254 | 0.8100 ± 0.185 | 3 ± 1     |
| codealltag-bert-base-german-cased | 0.9100 ± 0.111 | 0.7867 ± 0.176 | 0.8388 ± 0.138 | 3 ± 1     |
| xlm-roberta-large                 | 0.9500 ± 0.100 | <b>1.0000 ± 0.000</b> | <b>0.9714 ± 0.057</b> | 3 ± 1     |
| codealltag-xlm-roberta-large      | 0.9667 ± 0.067 | 0.8867 ± 0.157 | 0.9167 ± 0.105 | 3 ± 1     |
| gelectra-large                    | 0.9000 ± 0.200 | 1.0000 ± 0.000 | 0.9333 ± 0.133 | 3 ± 1     |
| codealltag-gelectra-large         | 0.9500 ± 0.100 | 0.9200 ± 0.160 | 0.9214 ± 0.102 | 3 ± 1     |

![ner_age](reports/figures/entity_prediction_performance_comparison_of_models_paired_age.jpg)

<b>(LOCATION_COUNTRY):</b>

| Model                             | Precision      | Recall         | F1-score       | Support   |
|:----------------------------------|:---------------|:---------------|:---------------|:----------|
| bert-base-german-cased            | 0.2000 ± 0.400 | 0.2000 ± 0.400 | 0.2000 ± 0.400 | 1 ± 0     |
| codealltag-bert-base-german-cased | 0.2000 ± 0.400 | 0.2000 ± 0.400 | 0.2000 ± 0.400 | 1 ± 0     |
| xlm-roberta-large                 | <b>0.6000 ± 0.490</b> | <b>0.6000 ± 0.490</b> | <b>0.6000 ± 0.490</b> | 1 ± 0     |
| codealltag-xlm-roberta-large      | 0.4000 ± 0.490 | 0.4000 ± 0.490 | 0.4000 ± 0.490 | 1 ± 0     |
| gelectra-large                    | 0.0000 ± 0.000 | 0.0000 ± 0.000 | 0.0000 ± 0.000 | 1 ± 0     |
| codealltag-gelectra-large         | 0.0000 ± 0.000 | 0.0000 ± 0.000 | 0.0000 ± 0.000 | 1 ± 0     |

![ner_location_country](reports/figures/entity_prediction_performance_comparison_of_models_paired_location_country.jpg)

<b>(LOCATION_ORGANIZATION):</b>

| Model                             | Precision      | Recall         | F1-score       | Support   |
|:----------------------------------|:---------------|:---------------|:---------------|:----------|
| bert-base-german-cased            | 0.0000 ± 0.000 | 0.0000 ± 0.000 | 0.0000 ± 0.000 | 1 ± 0     |
| codealltag-bert-base-german-cased | 0.0000 ± 0.000 | 0.0000 ± 0.000 | 0.0000 ± 0.000 | 1 ± 0     |
| xlm-roberta-large                 | 0.0000 ± 0.000 | 0.0000 ± 0.000 | 0.0000 ± 0.000 | 1 ± 0     |
| codealltag-xlm-roberta-large      | 0.0000 ± 0.000 | 0.0000 ± 0.000 | 0.0000 ± 0.000 | 1 ± 0     |
| gelectra-large                    | 0.0000 ± 0.000 | 0.0000 ± 0.000 | 0.0000 ± 0.000 | 1 ± 0     |
| codealltag-gelectra-large         | 0.0000 ± 0.000 | 0.0000 ± 0.000 | 0.0000 ± 0.000 | 1 ± 0     |

![ner_location_organization](reports/figures/entity_prediction_performance_comparison_of_models_paired_location_organization.jpg)

<b>(PROFESSION):</b>

| Model                             | Precision      | Recall         | F1-score       | Support   |
|:----------------------------------|:---------------|:---------------|:---------------|:----------|
| bert-base-german-cased            | 0.0000 ± 0.000 | 0.0000 ± 0.000 | 0.0000 ± 0.000 | 1 ± 0     |
| codealltag-bert-base-german-cased | 0.0000 ± 0.000 | 0.0000 ± 0.000 | 0.0000 ± 0.000 | 1 ± 0     |
| xlm-roberta-large                 | 0.0000 ± 0.000 | 0.0000 ± 0.000 | 0.0000 ± 0.000 | 1 ± 0     |
| codealltag-xlm-roberta-large      | 0.0000 ± 0.000 | 0.0000 ± 0.000 | 0.0000 ± 0.000 | 1 ± 0     |
| gelectra-large                    | 0.0000 ± 0.000 | 0.0000 ± 0.000 | 0.0000 ± 0.000 | 1 ± 0     |
| codealltag-gelectra-large         | 0.0000 ± 0.000 | 0.0000 ± 0.000 | 0.0000 ± 0.000 | 1 ± 0     |

![ner_profession](reports/figures/entity_prediction_performance_comparison_of_models_paired_profession.jpg)


## Best models per architecture

Based on <b>weighted avg</b> F1-score:

| Model                             | Fold | Precision | Recall | F1-score |
|-----------------------------------|------|-----------|--------|----------|
| bert-base-german-cased            | K5   | 0.8073    | 0.8653 | 0.8315   |
| codealltag-bert-base-german-cased | K1   | 0.8827    | 0.8869 | 0.8808   |
| xlm-roberta-large                 | K5   | 0.9158    | <b>0.9360</b> | <b>0.9234</b>   |
| codealltag-xlm-roberta-large      | K5   | 0.9107    | 0.9259 | 0.9159   |
| gelectra-large                    | K1   | <b>0.9180</b>    | 0.8988 | 0.9048   |
| codealltag-gelectra-large         | K5   | 0.8843    | 0.9192 | 0.8995   |