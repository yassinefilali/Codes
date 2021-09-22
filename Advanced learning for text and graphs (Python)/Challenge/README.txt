############### h-index prediction challenge ###############

In order to run the codes from scratch :

1 - Run the paper_representations.py file to generate paper_embeddings
(If you want the roBERTa embedding, first generate the abstracts_processed.txt
then run the script roberta_text_embedding.txt)

2 - Run the author_representations.pu file to generate the author embeddings.

3 - Run submission.py file.

Remarks : 

- In submission.py there are several commented blocks, which represent tested
approaches that did not yield better results than the actual structure of the code.

- The clustering.csv and centrality.csv are files where we stone the result of
functions applied on the graph, which take quite some time to run. We did this in order
to make the code faster otherwise, it would take hours to run du to the complexity
of certain algorithms.
 