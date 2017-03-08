
#printf "(1,2) Simultaneous Shading lemma\n"
#python classify.py surprising_coincidence_classification_01_permlen5.txt -ssl > surprising_coincidence_01_SSL.txt
#printf "(1,2,3) Simultaneous Shading lemma\n"
#python classify.py surprising_coincidence_classification_012_permlen9.txt -ssl > surprising_coincidence_012_SSL.txt
#printf "(1,3,2) Simultaneous Shading lemma\n"
#python classify.py surprising_coincidence_classification_021_permlen9.txt -ssl > surprising_coincidence_021_SSL.txt

#printf "(1,2,3) TSA1 - depth 1\n"
#python classify.py surprising_coincidence_classification_012_permlen9.txt -tsa1 1 > surprising_coincidence_012_TSA1_depth1.txt
printf "(1,2) TSA1 - depth 1\n"
python classify.py surprising_coincidence_classification_01_permlen5.txt -tsa1 1 > surprising_coincidence_01_TSA1_depth1.txt
printf "(1,3,2) TSA1 - depth 1\n"
python classify.py surprising_coincidence_classification_021_permlen9.txt -tsa1 1 > surprising_coincidence_021_TSA1_depth1.txt
