for chunk_size in 8 16 32 64 128 256 512 1024 2048 4096
do
    echo "Chunk size: $chunk_size"
    python test.py --chunk_size $chunk_size
done