#version 300 es
        precision mediump float;
        out vec4 out_fragColor;
        uniform float u;
        void main()
        {
            out_fragColor = vec4(true ? 0.0 : u);
        }