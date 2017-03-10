printf "(1,2) Shading lemma\n"
python classify.py surprising_coincidence_classification_01_permlen5.txt -sl > surprising_coincidence_01_SL.txt
printf "(1,2,3) Shading lemma\n"
python classify.py surprising_coincidence_classification_012_permlen9.txt -sl > surprising_coincidence_012_SL.txt
printf "(1,3,2) Shading lemma\n"
python classify.py surprising_coincidence_classification_021_permlen9.txt -sl > surprising_coincidence_021_SL.txt

#printf "(1,2) Simultaneous Shading lemma\n"
#python classify.py surprising_coincidence_classification_01_permlen5.txt -ssl > surprising_coincidence_01_SSL.txt
#printf "(1,2,3) Simultaneous Shading lemma\n"
#python classify.py surprising_coincidence_classification_012_permlen9.txt -ssl > surprising_coincidence_012_SSL.txt
#printf "(1,3,2) Simultaneous Shading lemma\n"
#python classify.py surprising_coincidence_classification_021_permlen9.txt -ssl > surprising_coincidence_021_SSL.txt

printf "(1,2) Lemma 2\n"
python classify.py surprising_coincidence_01_SL.txt -lemma2 > surprising_coincidence_01_SL_Lemma2.txt
printf "(1,2,3) Lemma 2\n"
python classify.py surprising_coincidence_012_SL.txt -lemma2 > surprising_coincidence_012_SL_Lemma2.txt
printf "(1,3,2) Lemma 2\n"
python classify.py surprising_coincidence_021_SL.txt -lemma2 > surprising_coincidence_021_SL_Lemma2.txt

printf "(1,2) Lemma 5\n"
python classify.py surprising_coincidence_01_SL.txt -lemma5 > surprising_coincidence_01_SL_Lemma5.txt
printf "(1,2,3) Lemma 5\n"
python classify.py surprising_coincidence_012_SL.txt -lemma5 > surprising_coincidence_012_SL_Lemma5.txt
printf "(1,3,2) Lemma 5\n"
python classify.py surprising_coincidence_021_SL.txt -lemma5 > surprising_coincidence_021_SL_Lemma5.txt
