#version 300 es
        precision mediump float;
        out vec4 out_fragColor;
        uniform bool u;
        void main()
        {
            if (false) {
                if (u) {
                    out_fragColor = vec4(1.0);
                }
            }
            out_fragColor = vec4(0.0);
        }