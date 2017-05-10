#!/usr/bin/bash

for p in {"01","012","021"}; do
    for d in {1..7}; do
        if [ ! -d results/lemma7/depth_"$d" ]; then
            mkdir results/lemma7/depth_"$d"
        fi

        if [ $d -gt 1 ]; then
            cp results/lemma7/depth_$((d - 1))/surprising_coincidence_"$p"_SL_Lemma7_final.txt results/lemma7/depth_"$d"/surprising_coincidence_"$p"_SL_Lemma7_0.txt
        else
            cp results/sl/surprising_coincidence_"$p"_SL.txt results/lemma7/depth_"$d"/surprising_coincidence_"$p"_SL_Lemma7_0.txt
        fi

        printf "\n$p Lemma 7\n"
        printf " depth $d\n"

        for i in {0..32}; do
            python classify.py results/lemma7/depth_"$d"/surprising_coincidence_"$p"_SL_Lemma7_"$i".txt -lemma7 $d > results/lemma7/depth_"$d"/surprising_coincidence_"$p"_SL_Lemma7_$((i + 1)).txt

            diff results/lemma7/depth_"$d"/surprising_coincidence_"$p"_SL_Lemma7_"$i".txt results/lemma7/depth_"$d"/surprising_coincidence_"$p"_SL_Lemma7_$((i + 1)).txt 2> /dev/null

            if [ $? -eq 0 ]; then
                cp results/lemma7/depth_"$d"/surprising_coincidence_"$p"_SL_Lemma7_$((i + 1)).txt results/lemma7/depth_"$d"/surprising_coincidence_"$p"_SL_Lemma7_final.txt
                break
            fi
        done
    done
done

