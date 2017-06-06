#!/usr/bin/bash
#SBATCH --job-name=TSA-FL2

source ~/permenv/bin/activate

pwd

for d in {6..7}; do
    if [ ! -d results/lemma7_pruned_fl2/depth_"$d" ]; then
        mkdir results/lemma7_pruned_fl2/depth_"$d"
    fi

    cp results/lemma7_pruned_fl2/depth_$((d - 1))/surprising_coincidence_021_SL_Lemma7_final.txt results/lemma7_pruned_fl2/depth_"$d"/surprising_coincidence_021_SL_Lemma7_0.txt

    printf "\n$p Lemma 7\n"
    printf " depth $d\n"

    for i in {0..32}; do
        printf "  iteration $i\n"
        if [ ! -f results/lemma7_pruned_fl2/depth_"$d"/surprising_coincidence_021_SL_Lemma7_"$i".txt ]; then
            printf "========= origin file not found\n"
            break
        fi
        python classify.py results/lemma7_pruned_fl2/depth_"$d"/surprising_coincidence_021_SL_Lemma7_"$i".txt -lemma7 $d -proof "results/proofs/lemma7/021-fl2" --force_len 1 > results/lemma7_pruned_fl2/depth_"$d"/surprising_coincidence_021_SL_Lemma7_$((i + 1)).txt

        diff results/lemma7_pruned_fl2/depth_"$d"/surprising_coincidence_021_SL_Lemma7_"$i".txt results/lemma7_pruned_fl2/depth_"$d"/surprising_coincidence_021_SL_Lemma7_$((i + 1)).txt

        if [ $? -eq 0 ]; then
            cp results/lemma7_pruned_fl2/depth_"$d"/surprising_coincidence_021_SL_Lemma7_$((i + 1)).txt results/lemma7_pruned_fl2/depth_"$d"/surprising_coincidence_021_SL_Lemma7_final.txt
            break
        fi
    done
done
