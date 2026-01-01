#version 300 es
        uniform B { uint e; } b[3];
        mediump float f() { return .0; }
        void main() { f(), b[0].e; }