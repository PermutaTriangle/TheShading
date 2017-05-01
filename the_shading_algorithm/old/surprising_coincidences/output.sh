seq 0 160 | xargs printf "%03d\n" | while read num; do
    echo "$num"
    ls C${num}_132_1
done
