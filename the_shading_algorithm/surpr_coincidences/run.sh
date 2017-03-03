python classify.py ../surprising_coincidence_classification_012_permlen9.txt -tsa1 1 > surprising_coincidence_012_TS1_depth1.txt
python classify.py ../surprising_coincidence_classification_021_permlen9.txt -tsa1 1 > surprising_coincidence_021_TS1_depth1.txt

python classify.py surprising_coincidence_classification_01_permlen5.txt -ssl > surprising_coincidence_01_SSL.txt
python classify.py surprising_coincidence_classification_012_permlen9.txt -ssl > surprising_coincidence_012_SSL.txt
python classify.py surprising_coincidence_classification_021_permlen9.txt -ssl > surprising_coincidence_021_SSL.txt
