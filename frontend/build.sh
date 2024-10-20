#!/bin/bash

rm -r ../server/react-app/*

cd app || exit
rm -r Dist/
npm install
npm run build
cp -r Dist/* ../../server/react-app/

cd ../landing
rm -r Dist/ 
npm install
npm run build
cp -r Dist/* ../../server/react-app/

echo "

Build and copy completed

"