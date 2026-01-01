#version 300 es
        precision highp float;
        centroid in float vary;
        out vec4 color;
        void main() {
           color = vec4(0.0, true ? vary : 0.0, 0.0, 1.0);
        }