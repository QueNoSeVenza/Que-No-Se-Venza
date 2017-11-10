/*
 * Lazy Line Painter - Path Object
 * Generated using 'SVG to Lazy Line Converter'
 *
 * http://lazylinepainter.info
 * Copyright 2013, Cam O'Connell
 *
 */

var svgData = {
  "logo": {
      "strokepath": [
          {
              "path": "m 136.46454,126.08997 4.71095,0 c 23.61635,0 23.65424,36.3161 0,36.3161 l -18.25154,0 0,17.9987 c 0,24.2802 -36.177898,24.44734 -36.177898,0 l 0,-37.72731",
              "duration": 800
          },
          {
              "path": "m 86.746052,140.72544 -6.938551,6.94354",
              "duration": 200
          },
          {
              "path": "m 93.704083,147.66898 -6.938552,-6.94354",
              "duration": 200
          },
          {
              "path": "m 73.548034,162.70323 -4.710954,0 c -23.616342,0 -23.654242,-36.3161 0,-36.3161 l 18.251544,0 0,-17.9987 c 0,-24.280201 36.177896,-24.447343 36.177896,0 l 0,37.7273",
              "duration": 800
          },
          {
              "path": "m 123.26652,148.06777 6.93855,-6.94355",
              "duration": 200
          },
          {
              "path": "m 116.30848,141.12422 6.93858,6.94355",
              "duration": 200
          }
      ],
      "dimensions": {
          "width": 210,
          "height": 209
      }
  }
};


/*
 Setup and Paint your lazyline!
 */

 $(document).ready(function(){
   $("#logo").lazylinepainter({
    "svgData": svgData,
     "strokeWidth": 6,
     "strokeColor": "#ff3b30"
 }).lazylinepainter('paint');
 });
