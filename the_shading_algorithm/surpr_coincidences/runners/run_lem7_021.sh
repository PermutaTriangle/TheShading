#!/usr/bin/bash
#SBATCH --job-name=ShadingLemma021

source ~/permenv/bin/activate

for d in {5..7}; do
    if [ ! -d results/lemma7/depth_"$d" ]; then
        mkdir results/lemma7/depth_"$d"
    fi

    printf "\n$p Lemma 7\n"
    printf " depth $d\n"

    for i in {0..32}; do
        python classify.py results/lemma7/depth_"$d"/surprising_coincidence_021_SL_Lemma7_"$i".txt -lemma7 $d > results/lemma7/depth_"$d"/surprising_coincidence_021_SL_Lemma7_$((i + 1)).txt

        diff results/lemma7/depth_"$d"/surprising_coincidence_021_SL_Lemma7_"$i".txt results/lemma7/depth_"$d"/surprising_coincidence_021_SL_Lemma7_$((i + 1)).txt 2> /dev/null

        if [ $? -eq 0 ]; then
            cp results/lemma7/depth_"$d"/surprising_coincidence_021_SL_Lemma7_$((i + 1)).txt results/lemma7/depth_"$d"/surprising_coincidence_021_SL_Lemma7_final.txt
            break
        fi
    done
done
