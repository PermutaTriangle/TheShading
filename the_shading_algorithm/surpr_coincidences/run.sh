
# printf "(1,2) ExpClasses\n"
# python gen_exp_classes.py "0 1" 5 > results/surprising_coincidence_classification_01_permlen5.txt
# printf "(1,2,3) ExpClasses\n"
# python gen_exp_classes.py "0 1 2" 9 > results/surprising_coincidence_classification_012_permlen9.txt
# printf "(2,1,3) ExpClasses\n"
# python gen_exp_classes.py "0 2 1" 9 > results/surprising_coincidence_classification_021_permlen9.txt
# 
# printf "(1,2) Shading lemma\n"
# python classify.py results/surprising_coincidence_classification_01_permlen5.txt -sl > results/surprising_coincidence_01_SL.txt
# printf "(1,2,3) Shading lemma\n"
# python classify.py results/surprising_coincidence_classification_012_permlen9.txt -sl > results/surprising_coincidence_012_SL.txt
# printf "(1,3,2) Shading lemma\n"
# python classify.py results/surprising_coincidence_classification_021_permlen9.txt -sl > results/surprising_coincidence_021_SL.txt
# 
printf "(1,2) Lemma 2\n"
python classify.py results/sl/surprising_coincidence_01_SL.txt -lemma2 > results/lemma2/surprising_coincidence_01_SL_Lemma2.txt
printf "(1,2,3) Lemma 2\n"
python classify.py results/sl/surprising_coincidence_012_SL.txt -lemma2 > results/lemma2/surprising_coincidence_012_SL_Lemma2.txt
printf "(1,3,2) Lemma 2\n"
python classify.py results/sl/surprising_coincidence_021_SL.txt -lemma2 > results/lemma2/surprising_coincidence_021_SL_Lemma2.txt
# 
# printf "(1,2) Simultaneous Shading lemma\n"
# python classify.py results/surprising_coincidence_01_SL.txt -ssl > results/surprising_coincidence_01_SSL.txt
# printf "(1,2,3) Simultaneous Shading lemma\n"
# python classify.py results/surprising_coincidence_012_SL.txt -ssl > results/surprising_coincidence_012_SSL.txt
# printf "(1,3,2) Simultaneous Shading lemma\n"
# python classify.py results/surprising_coincidence_021_SL.txt -ssl > results/surprising_coincidence_021_SSL.txt
# 
printf "(1,2) Lemma 5\n"
python classify.py results/sl/surprising_coincidence_01_SL.txt -lemma5 > results/lemma5/surprising_coincidence_01_SL_Lemma5.txt
printf "(1,2,3) Lemma 5\n"
python classify.py results/sl/surprising_coincidence_012_SL.txt -lemma5 > results/lemma5/surprising_coincidence_012_SL_Lemma5.txt
printf "(1,3,2) Lemma 5\n"
python classify.py results/sl/surprising_coincidence_021_SL.txt -lemma5 > results/lemma5/surprising_coincidence_021_SL_Lemma5.txt

printf "(1,2) Lemma 7\n"
python classify.py results/sl/surprising_coincidence_01_SL.txt -lemma7 > results/lemma7/surprising_coincidence_01_SL_Lemma7.txt
cp results/lemma7/surprising_coincidence_01_SL_Lemma7.txt  results/lemma7/surprising_coincidence_01_SL_Lemma7_0.txt
printf "(1,2,3) Lemma 7\n"
python classify.py results/sl/surprising_coincidence_012_SL.txt -lemma7 > results/lemma7/surprising_coincidence_012_SL_Lemma7.txt
cp results/lemma7/surprising_coincidence_012_SL_Lemma7.txt  results/lemma7/surprising_coincidence_012_SL_Lemma7_0.txt
printf "(1,3,2) Lemma 7\n"
python classify.py results/sl/surprising_coincidence_021_SL.txt -lemma7 > results/lemma7/surprising_coincidence_021_SL_Lemma7.txt
cp results/lemma7/surprising_coincidence_021_SL_Lemma7.txt  results/lemma7/surprising_coincidence_021_SL_Lemma7_0.txt

./run_lem7.sh
