## Fractalize Map

There's two main files in this program:

* record-clicks.html
* fractalize-map.py

The first one allows you to reclick if you want new points (and displays photo.jpg as a reference).

The second one takes those points and fractalizes them.

----

## record-clicks.html

To use record-clicks.html, first open it in your browser (I used Firefox). It relies on jQuery, but loading the files locally wasn't making Firefox happy, so open the console and type:

    run($)

and then start clicking and they will show up in your console. Then copy the text from the console and run:

    sed -e "1d; s/.* //;" > my-filename-for-this-island.points

then paste the copied text into your terminal to convert it into the right format.

----

## fractalize-map.py

Using this one is as simple as just running:

    python fractalize-map.py

It accepts two optional arguments (well... If you have one, you have to have the other, too).

* CHANGE_SCALE
* SUBDIVISIONS

* CHANGE_SCALE *

This changes how much variation there is with each point. A larger value will make very large changes every time it subdivides. I find that 0.005 works pretty well.

* SUBDIVISIONS *

This changes how many times it subdivides the line. If you set this equal to 100, it will split each line segment 100 times and fractalize those new points.  I usually use 1000 here.

A full example of running the program is:

    python fractalize-map.py 0.005 1000

