#!/bin/sh
if [ ! -d "themes/minimal-black" ]; then
    echo "Adding submodule"
    git submodule add https://gitlab.com/jimchr12/hugo-minimal-black.git themes/minimal-black
fi

# Install dependancies
cd themes/minimal-black
npm install
cd ../..

# Set about alternative as about page
if [ -f "themes/minimal-black/layouts/_default/about-alternative.html" ]; then
    echo "Setting about-alternative as the main about page"
    rm themes/minimal-black/layouts/_default/about.html
    mv themes/minimal-black/layouts/_default/about-alternative.html themes/minimal-black/layouts/_default/about.html
fi

# Start server
hugo server -D