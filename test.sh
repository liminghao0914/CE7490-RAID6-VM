for chunk_size in 256 # 4 8 16 32 64 128 256 512 1024 2048 4096
do
    for num_disk in 8 # 10 12 14 16 18 20 22 24 
    do
        for filename in "SampleJPGImage_500kbmb.jpeg" "SampleJPGImage_1mbmb.jpeg" "SampleJPGImage_2mbmb.jpeg" "SampleJPGImage_5mbmb.jpeg" "SampleJPGImage_10mbmb.jpeg" "SampleJPGImage_15mbmb.jpeg" "SampleJPGImage_20mbmb.jpeg"
        do
            echo "Chunk size: $chunk_size"
            python test.py \
                --chunk_size $chunk_size \
                --num_disk $num_disk \
                --filename $filename \
                --use_vm
        done
    done
done