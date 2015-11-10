#!/bin/bash

sips --resampleWidth 256 icon.png --out icon_256_tmp.png
sips -p 256 256 icon_256_tmp.png --out icon_padded_tmp.png
sips -s format icns icon_padded_tmp.png --out icon.icns
rm -f *_tmp.png
