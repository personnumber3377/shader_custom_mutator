#version 300 es
        precision mediump float;
        out vec4 out_fragColor;
        uniform float u;
        void main()
        {
            if (false) {
                out_fragColor = vec4(u);
            }
            out_fragColor = vec4(0.0);
        }