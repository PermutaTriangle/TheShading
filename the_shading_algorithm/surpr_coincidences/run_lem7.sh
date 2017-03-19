

#function dopatt {
    #for i in {0..32}; do
        #python classify.py results/surprising_coincidence_01_SL_Lemma7_$i.txt -lemma7 > results/surprising_coincidence_01_SL_Lemma7_$((i + 1)).txt

        #diff results/surprising_coincidence_01_SL_Lemma7_$i.txt results/surprising_coincidence_01_SL_Lemma7_$((i + 1)).txt 2> /dev/null

        #if [ $? -eq 0 ]; then
            #break
        #fi
    #done
#}

for p in {"01","012","021"}; do
    for i in {0..32}; do
        python classify.py results/lemma7/surprising_coincidence_"$p"_SL_Lemma7_"$i".txt -lemma7 > results/lemma7/surprising_coincidence_"$p"_SL_Lemma7_$((i + 1)).txt

        diff results/lemma7/surprising_coincidence_"$p"_SL_Lemma7_"$i".txt results/lemma7/surprising_coincidence_"$p"_SL_Lemma7_$((i + 1)).txt 2> /dev/null

        if [ $? -eq 0 ]; then
            break
        fi
    done
done

