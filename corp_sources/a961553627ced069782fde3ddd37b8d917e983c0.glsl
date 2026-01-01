#version 300 es
        precision mediump float;
        out vec4 out_fragColor;
        uniform float u;
        float f() {
            return u;
        }
        void main()
        {
            out_fragColor = vec4(0.0);
        }