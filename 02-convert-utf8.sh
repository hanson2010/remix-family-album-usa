# 01-original (GB18030) -> 02-utf8: convert to UTF-8, strip trailing whitespace and CR, delete subtitle 0 (lines 1-9)
mkdir -p 02-utf8
for file in 01-original/*.srt; do
    out=02-utf8/$(basename "$file")
    iconv -f gb18030 -t utf-8 "$file" > "$out"
    sed -i 's/\s*\r\?$//' "$out"
    sed -i '1,9d' "$out"
done
