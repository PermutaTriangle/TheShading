

#function dopatt {
    #for i in {0..32}; do
        #python classify.py results/surprising_coincidence_01_SL_Lemma7_$i.txt -lemma7 > results/surprising_coincidence_01_SL_Lemma7_$((i + 1)).txt

        #diff results/surprising_coincidence_01_SL_Lemma7_$i.txt results/surprising_coincidence_01_SL_Lemma7_$((i + 1)).txt 2> /dev/null

        #if [ $? -eq 0 ]; then
            #break
        #fi
    #done
#}

#for p in {"01","012","021"}; do
    p="01"
    for d in {2..7}; do
        if [ ! -d results/lemma7/depth_"$d" ]; then
            mkdir results/lemma7/depth_"$d"
        fi

        cp results/lemma7/depth_$((d - 1))/surprising_coincidence_"$p"_SL_Lemma7_final.txt results/lemma7/depth_"$d"/surprising_coincidence_"$p"_SL_Lemma7_0.txt
        #if [ $d -gt 2 ]; then
            #cp results/lemma7/depth_$((d - 1))/surprising_coincidence_"$p"_SL_Lemma7_final.txt results/lemma7/depth_"$d"/surprising_coincidence_"$p"_SL_Lemma7_0.txt
        #else
            #cp results/sl/surprising_coincidence_01_SL.txt results/lemma7/depth_"$d"/surprising_coincidence_"$p"_SL_Lemma7_0.txt
        #fi

        for i in {0..32}; do
            python classify.py results/lemma7/depth_"$d"/surprising_coincidence_"$p"_SL_Lemma7_"$i".txt -lemma7 $d > results/lemma7/depth_"$d"/surprising_coincidence_"$p"_SL_Lemma7_$((i + 1)).txt

            diff results/lemma7/depth_"$d"/surprising_coincidence_"$p"_SL_Lemma7_"$i".txt results/lemma7/depth_"$d"/surprising_coincidence_"$p"_SL_Lemma7_$((i + 1)).txt 2> /dev/null

            if [ $? -eq 0 ]; then
                cp results/lemma7/depth_"$d"/surprising_coincidence_"$p"_SL_Lemma7_$((i + 1)).txt results/lemma7/depth_"$d"/surprising_coincidence_"$p"_SL_Lemma7_final.txt
                break
            fi
        done
    done
#done

