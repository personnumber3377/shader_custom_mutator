#version 300 es
        precision mediump float;
        out vec4 out_fragColor;
        uniform vec4 u;
        void main()
        {
            if (false) {
                out_fragColor = u, vec4(1.0);
            }
            out_fragColor = vec4(0.0);
        }